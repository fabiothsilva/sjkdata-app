# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 22:31:18 2025

Functions to process data and help to build an streamlit app

@author: Fabio
"""

import streamlit as st


@st.cache_data
def ibge_data():
    """
    Function to get basic populational data from IBGE, specifically for the
    city of São José dos Campos, SP - Brasil

    Returns a data dictionary, if theres no request errors
    
    Returns a string with a message error if there is a request error
    -------
    data = {
            'Category': ["Feminino", "Masculino", "Total"],
            'Value': [int(total_feminino), int(total_masculino), 
                      (int(total_feminino)+int(total_masculino))]
        }
    """

    import requests

    link_masculino = "https://servicodados.ibge.gov.br/api/v3/agregados/10089/periodos/2022/variaveis/93?localidades=N6[3549904]&classificacao=2[4]|58[95253]|2661[32776]|1[6795]"

    link_feminino = "https://servicodados.ibge.gov.br/api/v3/agregados/10089/periodos/2022/variaveis/93?localidades=N6[3549904]&classificacao=2[5]|58[95253]|2661[32776]|1[6795]"

    dados_masculino = requests.get(link_masculino).json()

    dados_feminino = requests.get(link_feminino).json()

    total_masculino = dados_masculino[0]["resultados"][0]["series"][0]["serie"]["2022"]

    total_feminino = dados_feminino[0]["resultados"][0]["series"][0]["serie"]["2022"]

    data = {
        'Category': ["👩🏿Feminino", "🧔Masculino", "👨‍👩‍👧‍👦Total"],
        'Value': [int(total_feminino), int(total_masculino),
                  (int(total_feminino)+int(total_masculino))]
    }

    return data


def folha_prefeitura(file_path: str):
    """
    Function to get the top 10 salaries and the top bottom salaries of the payment
    receipt of the cityhall from São José dos campos.
    You need to manually download the csv file, since there is no API on their
    website.

    Returns Two dataframes, one with the top 10 salaries and one with the bottom
    10 salaries.
    
    For the botton 10, only payments above the minimum wage were considered, since
    there was some strange outliers, like a high negative value and many zeroes.
    
    top 10 example

   NOME  REMUNERACAO_MES
7473      ROBSON         47150.06
2282      DENISE         43202.76
6825    PATRICIA         41845.49
7676        ROSE         41025.98
3362    GABRIELA         38617.95
1826  COSTANTINO         38550.62
7010    POLYANNA         37975.22
220      ALCIONE         37610.94
1139     ARNALDO         36686.04
5712      MARCOS         36566.86

    bottom 10 example
    
    NOME  REMUNERACAO_MES
115     ADRIANA          1811.26
677         ANA          1821.60
842       ANDRE          1828.50
723         ANA          1831.85
2191     DEBORA          1850.94
2654       ELIS          1852.88
4431     JOVANA          1852.88
1159    AUGUSTA          1852.88
6559    NATALIA          1855.11
2739  ELIZABETH          1871.12
    -------
    
    """
    import pandas as pd

    def simplificar_nome(nome):
        partes = nome.split()
        if len(partes) >= 2:
            return f"{partes[0]} {partes[1][0]}."
        else:
            return partes[0]

    df_folha_prefeitura = pd.read_csv(file_path, encoding='latin-1', sep=";")

    df_folha_prefeitura = df_folha_prefeitura.rename(columns={
        "MÊS": "MES",
        "TEMPO DE SERVIÇO (ANOS)": "ANOS_SERVICO",
        "REMUNERAÇÃO DO MÊS": "REMUNERACAO_MES",
        "VERBA EVENTUAL": "VERBA_EVENTUAL"
    })

    df_folha_prefeitura["REMUNERACAO_MES"] = pd.to_numeric(
        df_folha_prefeitura["REMUNERACAO_MES"].str.replace('.', '',
                                                           regex=False).str.replace(',', '.', regex=False))
    df_folha_prefeitura["VERBA_EVENTUAL"] = pd.to_numeric(
        df_folha_prefeitura["VERBA_EVENTUAL"].str.replace('.', '',
                                                          regex=False).str.replace(',', '.', regex=False))

    df_agrupado = df_folha_prefeitura.groupby(
        'NOME')['REMUNERACAO_MES'].sum().reset_index()
    df_agrupado = df_agrupado.sort_values(by='REMUNERACAO_MES',
                                          ascending=False)

    df_agr_top10 = df_agrupado.head(10).sort_values(by='REMUNERACAO_MES',
                                                    ascending=False)

    df_agr_top10['NOME'] = df_agr_top10['NOME'].apply(simplificar_nome)

    df_agr_bottom10 = df_agrupado[df_agrupado['REMUNERACAO_MES'] >= 1804]

    df_agr_bottom10['NOME'] = df_agr_bottom10['NOME'].apply(simplificar_nome)

    df_agr_bottom10 = df_agr_bottom10.tail(10).sort_values(by='REMUNERACAO_MES',
                                                           ascending=True)

    return df_agr_top10, df_agr_bottom10

def folha_camara(file_path:str):
    """
    

    Parameters
    ----------
    file_path : str
        DESCRIPTION.

    Returns
    -------
    None.

    """
    import pandas as pd
    
    df_folha_camara = pd.read_csv(file_path, sep = ";")
    
    df_folha_camara = df_folha_camara.rename(columns={
    "Nome do Servidor":"NOME",
    "Cargo":"CARGO",
    "Salário Bruto":"SALARIO_BRUTO",
})
    
    df_folha_camara = df_folha_camara[["NOME","CARGO","SALARIO_BRUTO"]]
    
    df_folha_camara["SALARIO_BRUTO"] = pd.to_numeric(
        df_folha_camara["SALARIO_BRUTO"]\
        .str.replace('.', '', regex=False)\
        .str.replace(',', '.', regex=False)
        )

    def corrige_cargo(cargo:str) -> str:
        if cargo.startswith("."):
          cargo = cargo[1:]
          return cargo

        else:
          return cargo

    def corrige_nome(nome:str) -> str:
        lista_nome = nome.split()
    
        if len(lista_nome) == 2:
          nome = lista_nome[0] + " " + lista_nome[1][0:2] +"."
          return nome
    
        elif len(lista_nome) >= 3:
          nome = lista_nome[0] + " " + lista_nome[1][0:2] + ". " +\
              lista_nome[1][0] + "."
          return nome
    
        else:
          return lista_nome[0]



    df_folha_camara["CARGO"] = df_folha_camara["CARGO"].apply(corrige_cargo)
    
    df_folha_camara["NOME"] = df_folha_camara["NOME"].apply(corrige_nome)
    
    df_top10 = df_folha_camara.sort_values(
        by='SALARIO_BRUTO', 
        ascending=False
        ).head(10)
    
    df_bottom10 = df_folha_camara[df_folha_camara['SALARIO_BRUTO']>=1804]\
        .sort_values(
            by='SALARIO_BRUTO', 
            ascending=True
            ).head(10)
        
    df_cargo_agr = pd.DataFrame(
        df_folha_camara[["CARGO","SALARIO_BRUTO"]].groupby(
        "CARGO")["SALARIO_BRUTO"].max().sort_values(ascending=False)
        )
    
    df_cargo_agr.reset_index(inplace=True)

    df_cargo_top10 = df_cargo_agr.sort_values(
        by='SALARIO_BRUTO', ascending=False).head(10)
    
    df_cargo_bottom10 = df_cargo_agr[df_cargo_agr['SALARIO_BRUTO'] >= 1804].sort_values(
        by= "SALARIO_BRUTO", ascending=True).head(10)


    return df_top10, df_bottom10, df_cargo_top10, df_cargo_bottom10

def folha_cargo_prefeitura(file_names:str, file_roles:str):
    import pandas as pd
    
    df_names = pd.read_csv(
    file_names, 
    encoding='latin-1', 
    sep= ";")
    
    df_roles = pd.read_csv(
    file_roles,
    encoding="latin-1",
    sep= ";",
    index_col=False)
    
    #tratando df_names    
    df_names = df_names.rename(
    columns={
        "REMUNERAÇÃO DO MÊS": "REMUNERACAO"
    })
    
    df_names["NOME"] = df_names["NOME"].str.strip()

    df_names["REMUNERACAO"] = df_names["REMUNERACAO"].str.replace(".", "")\
    .str.replace(",",".").astype(float)
    
    df_names = df_names[["NOME", "REMUNERACAO"]]
    
    #tratando df_roles
    df_roles = df_roles[["NOME", "CARGO", "DESCRICAO"]]
    
    df_roles["NOME"] = df_roles["NOME"].str.strip()

    df_roles["CARGO"] = df_roles["CARGO"].str.strip()
    
    df_roles["DESCRICAO"] = df_roles["DESCRICAO"].str.strip()
    
    #juntando as base de dados
    df_complete = pd.merge(df_names, df_roles, on="NOME")
    
    #subtituindo cargos NaN pela descrição do cargo
    df_complete.loc[df_complete["CARGO"] == "-", "CARGO"] =\
    df_complete.loc[df_complete["CARGO"] == "-", "DESCRICAO"]
    
    #criando o df desejado
    df_cargo_salary = df_complete[["CARGO", "REMUNERACAO"]]
    
    df_cargo_salary = df_cargo_salary.groupby("CARGO", as_index=False).max()
    
    df_t10_cargo = df_cargo_salary.sort_values(
        by="REMUNERACAO", 
        ascending=False).head(10)
    
    df_b10_cargo = df_cargo_salary.sort_values(
        by="REMUNERACAO", 
        ascending=True).head(10)
    
    #salario prefeito para ser usado como referencia
    mayor_salary = df_cargo_salary.loc[
    df_cargo_salary["CARGO"] == "PREFEITO",
    "REMUNERACAO"].values[0]
    
    return df_t10_cargo, df_b10_cargo, mayor_salary

def data_map(file_path):
    import pandas as pd
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter
    
    df =pd.read_csv(file_path, encoding='latin-1', sep=';')
    
    df.rename(
    columns={
        "VALOR_CONTRATO":"VALOR"
        
    },
    inplace=True
    )
    
    def adj_address (address):
      pieces = address.split("-")
    
      if "." in pieces[0]:
        pieces[0] = pieces[0].replace(".", "")
      
      elif " x " in pieces[0]:
        pieces[0] = pieces[0].replace(" x ", "")
    
      else:
        pieces[0] = pieces[0]
    
      full_address = (pieces[0].strip() + 
                      "," + 
                      #pieces[1].strip()+
                      "São José dos Campos, SP")
      return full_address
  
    df["ENDERECO"] = df["ENDERECO"].apply(adj_address)
    
    address_list = df["ENDERECO"].to_list()
    
    # Inicializa o geolocalizador
    geolocator = Nominatim(user_agent="fabio_geolacator_2025")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    
    
    # Função para obter latitude e longitude
    def obter_lat_long(endereco):
        try:
            location = geolocator.geocode(endereco, language="pt")
            if location:
                return location.latitude, location.longitude
            else:
                return None, None
        except:
            return None, None
        
    import time

    dados = []
    
    for endereco in address_list:
        lat, lon = obter_lat_long(endereco)
        dados.append({'endereço': endereco, 'latitude': lat, 'longitude': lon})
        time.sleep(1)  # Evita sobrecarregar o serviço

    df_address = pd.DataFrame(dados)
    
    df.reset_index(inplace=True)
    
    df_address.reset_index(inplace=True)
    
    df_final = df.merge(df_address, left_on="index", right_on="index")
    
    filt = ["VALOR", "PERC_REALIZADO", "latitude", "longitude"]
    
    df_final = df_final[filt]
    
    df_final = df_final.dropna()
    
    df_final['PERC_REALIZADO'] = df_final[
        'PERC_REALIZADO'].str.replace('%', '')\
        .str.replace(',','.').astype(float)
    
    df_final["COLOR"] = df_final['PERC_REALIZADO'].apply(
        lambda x:'#008000' if x >= 100 else '#FFDE21')
    
    return df_final

if __name__ == "__main__":
    
    # print(data_map("obras.csv"))
    
    print("ola")
   