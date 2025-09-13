# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 19:49:16 2025

@author: Fabio
"""

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR')

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk


def ajustar_milhar(valor):
    
    if isinstance(valor, int) == True:
        valor_ajustado = locale.format_string("%d", valor, grouping=True)
        
    elif isinstance(valor, float) == True:
        valor_ajustado = locale.format_string("%.2f", valor, grouping=True)
        
    return str(valor_ajustado)

@st.cache_resource
def plotly_genderchart():
    try:
        # Carrega os dados da API do IBGE
        df = pd.DataFrame(dpg.ibge_data())
    except:
        message1 = st.title("Erro!")
        message2 = st.write("Não foi possível conectar a API do IBGE")
        return message1, message2
    
    # df["Value"] = df["Value"].apply(ajustar_milhar)    
    
    df["hover_data"] = df["Value"].apply(ajustar_milhar)
    
    df = df.sort_values(by = "Value", ascending=True)
    
    filt = ["Category", "Value"]

    # Renomeia colunas para exibição
    df_show = df[filt].rename(columns={
        "Category": "Gênero",
        "hover_data": "Pessoas por Gênero"
    })
    
    with st.container(border=True):
    
        with st.expander("📋Tabela de Dados"):    
            st.dataframe(df_show, hide_index=True)
    
        # Define cores personalizadas
        color_map = {
            "👩🏿Feminino": "lightpink",
            "🧔Masculino": "lightblue",
            "👨‍👩‍👧‍👦Total": "lightgray"
        }
    
        # Cria gráfico de barras com Plotly
        fig = px.bar(
            df,
            x="Category",
            y="Value",
            color="Category",
            text="hover_data",  # <- Aqui está o segredo!
            color_discrete_map=color_map,
            labels={"Category": "Gênero", "hover_data": "Pessoas por Gênero"},
            title="Pessoas por Gênero",
            hover_data={"Category": True, "hover_data": True, "Value": False}
        )
        
        # Atualizar posição dos rótulos
        fig.update_traces(
            # text=df_show["Pessoas por Gênero"],  # Adiciona os valores como texto
            textposition="outside",
            textfont=dict(color="black", size=14),  # Define cor e tamanho do texto
            # hoverinfo="label+value",
            marker=dict(line=dict(color="black", width=1))
            )
    
        fig.update_layout(
            xaxis_title="Gênero",
            yaxis_title="Pessoas por Gênero",
            showlegend=False,
            legend_title_text=None,
            separators=",.",
            xaxis=dict(
                title_font=dict(size=16, color="black"),
                tickfont=dict(size=14, color="black")
            ),
            yaxis=dict(
                title_font=dict(size=16, color="black"),
                tickfont=dict(size=14, color="black"),
                range=[0, df["Value"].max() * 1.1]
            ),        
        )
    
        st.plotly_chart(fig)
        return st.caption("Fonte: IBGE, censo 2022")

def pop_etaria():

    # Título do dashboard
    st.title("📊 População por Faixa Etária – São José dos Campos")
    
    # Dados populacionais
    dados = {
        "Faixa Etária": ["0 a 14 anos", "15 a 29 anos", "30 a 64 anos", "65 anos ou mais"],
        "2010": [137245, 168655, 285169, 38852],
        "2022": [128855, 144730, 342965, 80504]
    }
    
    df = pd.DataFrame(dados)
    
    # Gráfico de barras comparativo
    fig, ax = plt.subplots()
    bar_width = 0.35
    x = range(len(df))
    
    ax.bar(x, df["2010"], width=bar_width, label="2010", color="#6fa8dc")
    ax.bar([i + bar_width for i in x], df["2022"], width=bar_width, label="2022", color="#f6b26b")
    
    # Configurações do gráfico
    ax.set_xticks([i + bar_width / 2 for i in x])
    ax.set_xticklabels(df["Faixa Etária"])
    ax.set_ylabel("População")
    ax.set_title("Comparativo por Faixa Etária")
    ax.legend()
    
    # Exibir no Streamlit
    st.pyplot(fig)
    
    # Tabela de dados
    st.subheader("📋 Tabela de Dados")
    st.dataframe(df, hide_index = True)
    
def pop_etaria_2():   
    # Dados populacionais
    dados = {
        "Faixa Etária": ["0 a 14 anos", "15 a 29 anos", "30 a 64 anos", "65 anos ou mais"],
        "2010": [137245, 168655, 285169, 38852],
        "2022": [128855, 144730, 342965, 80504]
    }
    
    df = pd.DataFrame(dados)
    
    # Transformar para formato longo (long format) para facilitar o Plotly
    df_long = df.melt(id_vars="Faixa Etária", var_name="Ano", value_name="População")
    
    # Gráfico interativo com Plotly
    fig = px.bar(
        df_long,
        x="Faixa Etária",
        y="População",
        color="Ano",
        barmode="group",
        text="População",
        hover_name="Faixa Etária",
        hover_data={"Ano": True, "População": True},
        color_discrete_map={"2010": "#6fa8dc", "2022": "#f6b26b"}
    )
        
    # Atualizar posição dos rótulos
    fig.update_traces(
        textposition="outside",
        textfont=dict(color="black", size=14),
        marker=dict(
        line=dict(color="black", width=1)
    )

        )
    
    fig.update_layout(
        title="Evolução da participação percentual dos grupos etários na população",
        xaxis_title="Faixa Etária",
        yaxis_title="População",
        legend_title="Ano",
        bargap=0.2,
        xaxis=dict(
            title_font=dict(size=16, color="black"),
            tickfont=dict(size=14, color="black")
        ),
        yaxis=dict(
            title_font=dict(size=16, color="black"),
            tickfont=dict(size=14, color="black"),
            range=[0, df["2022"].max() * 1.1]
        ),        
        # 🔧 Outros ajustes visuais
        uniformtext_minsize=10,
        uniformtext_mode='hide'
    
        )
    
    with st.container(border=True):
    
        # Título do dashboard
        # st.title("📊 População por Faixa Etária – São José dos Campos")
        
        with st.expander("📋 Tabela de Dados"):
            st.dataframe(df, hide_index= True)
        
        # Exibir no Streamlit
        st.plotly_chart(fig, use_container_width=True)   

def pop_urb_rural():    
    # Dados populacionais
    dados = {
        "Tipo de Área": ["🌇 Urbana", "🌄 Rural"],
        "População": [681842, 15212]
    }
    
    df = pd.DataFrame(dados)
    
    df_formatado = df.copy()
    
    # df_formatado["População"] = df_formatado["População"].apply(ajustar_milhar)
    
    # Gráfico de pizza com rotação para destacar a área rural à esquerda
    fig = px.pie(
        df_formatado,
        names="Tipo de Área",
        values="População",
        color="Tipo de Área",
        color_discrete_map={
            "🌇 Urbana": "#6fa8dc",
            "🌄 Rural": "#93c47d"
        },
        hole=0.4        
    )
    
    # Ajustes visuais e interatividade
    fig.update_traces(
        textinfo="label+percent+value",
        # texttemplate='%{percent:.2f}%',
        textposition='outside',  # 👈 rótulos fora do donut!
        # textfont_size=16,
        textfont=dict(color="black", size=16),
        pull=[0, 0.1],  # destaque leve na área rural
        marker=dict(line=dict(color="#000000", width=1)),
        showlegend=False,
        insidetextorientation='tangential',
        hoverinfo="label+value+percent",
        rotation=120 # gira o gráfico para posicionar a área rural à esquerda
    )
    
    fig.update_layout(
        title="📊 Proporção Populacional por Tipo de Área",
        title_x=0,  # centraliza o título
        title_y=0.95,  # afasta o título do gráfico
        height=500,   # aumenta a altura
        separators=",.",
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="right",
            x=1.1,
            font=dict(size=14)
        ),
        # margin=dict(t=60, b=20, l=20, r=120),
        margin=dict(t=100, b=70, l=50, r=50),
        uniformtext_minsize=10,
        uniformtext_mode='show',
    )
    
    with st.container(border= True):
        
        # Título do dashboard
        # st.title("🏙️ População Urbana vs Rural – São José dos Campos")
    
        # Tabela de dados
        with st. expander("📋 Tabela de Dados"):
            st.dataframe(df_formatado, hide_index = True)
        
        # Exibir no Streamlit
        st.plotly_chart(fig, use_container_width=True)

def domicilios():    
    # Dados oficiais
    dados = {
        "Tipo de Área": ["🌆 Urbanos", 
                         "🌄 Rurais",
                         "🛖 Improvisados",
                         "🏫👶 Coletivos",
                         "🏚️ Particulares - Não Ocupados",
                         "🏠 Particulare - Ocupados"
                         ],
        "Domicílios": [272406, 
                       9808,
                       59,
                       283,
                       33978,
                       247894
                       ]
    }
    
    df = pd.DataFrame(dados)
    
    df_formatado = df.copy()
    
    df_show = df_formatado.sort_values(by="Domicílios", ascending=True)
    
    # 🎯 Gráfico interativo tipo donut
    fig = px.pie(
        df_formatado,
        names="Tipo de Área",
        values="Domicílios",
        color="Tipo de Área",
        hole=0.4,
        color_discrete_map={
            "🌆 Urbanos": "#D3D3D3",
            "🌄 Rurais": "#E76F51",
            "🛖 Improvisados": "#F4A261",
            "🏫👶 Coletivos": "#A8DADC",
            "🏚️ Particulares - Não Ocupados": "#B5838D",
            "🏠 Particulare - Ocupados": "#2A9D8F"
        }
    )
    
    fig.update_traces(
        textinfo="label+value",
        textposition='outside',  # 👈 rótulos fora do donut!
        textfont=dict(color="black", size=16),
        # textfont_size=16,
        rotation=110,  # gira o gráfico para destacar a área rural à esquerda
        pull=[0, 0.1],  # destaque leve na área rural
        insidetextorientation='tangential',
        marker=dict(line=dict(color="black", width=1)),
        hoverinfo="label+percent+value",
        showlegend= False
    )
    
    fig.update_layout(
        title="📊 Proporção de Domicílios por Tipo",
        title_x=0,  # centraliza o título
        title_y=0.95,  # afasta o título do gráfico
        height=500,   # aumenta a altura
        separators=",.",
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="right",
            x=1.1,
            font=dict(size=14)
        ),
        margin=dict(t=105, b=70, l=85, r=20)
    )
    
    with st.container(border = True):    
        # Título da seção
        # st.title("🏠 Domicílios – São José dos Campos")
        
        # 🔽 Tabela dentro do expander
        with st.expander("📋 Tabela de dados"):                   
            st.dataframe(df_show, use_container_width=True, hide_index=True)
        
        # Exibir gráfico
        st.plotly_chart(fig, use_container_width=True)
        
        # Texto explicativo
        # st.markdown("📌 Cada domicílio possui, em média, **2,8 moradores**.")
        
        st.badge("Cada domicílio possui, em média, **2,8 moradores**.",
                 icon= "📌",
                 color = "green"
                 )
        
        # 🔗 Fonte oficial
        st.markdown("🔗 Fonte: [Prefeitura Municipal de São José dos Campos – Dados da Cidade](https://www.sjc.sp.gov.br/servicos/governanca/populacao/)")

def piramide_etaria():
    with st.container(border=True):
        # Título
        # st.title("👶🏽👵🏿 Pirâmide Etária – São José dos Campos (Censo 2022)")
        
        st.badge("Você pode filtrar a pirâmide por faixa etária",
                 icon = "❗",
                 color = "red"
                 )
        
        # Dados por grupo quinquenal
        dados = {
            "Grupo Etário": [
                "0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39",
                "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74",
                "75-79", "80-84", "85-89", "90-94", "95-99", "100+"
            ],
            "Homens": [
                20442, 22933, 22335, 22726, 25154, 24915, 26157, 27734, 28317,
                23336, 21040, 18869, 16576, 13642, 9947, 5990, 3124, 1385, 581, 144, 12
            ],
            "Mulheres": [
                19545, 22027, 21573, 21643, 24652, 25640, 27780, 29870, 31141,
                25827, 23437, 22468, 20413, 16600, 12226, 7828, 4727, 2659, 1219, 347, 73
            ]
        }
        
        df = pd.DataFrame(dados)
        
        # Lista de faixas etárias disponíveis
        faixas_etarias = df["Grupo Etário"].tolist()
        
        # 2) Inicializa a seleção completa uma única vez
        if "faixa_selecionada" not in st.session_state:
            st.session_state.faixa_selecionada = faixas_etarias
        
        # 3) Botão para resetar seleção
        if st.button("🔄 Restaurar seleção de faixas etárias"):
            st.session_state.faixa_selecionada = faixas_etarias
        
        # 4) multiselect sempre visível, usa 'key' e SEM default
        faixa_selecionada = st.multiselect(
            "👨‍👩‍👧‍👦 Selecione as faixas etárias que deseja visualizar:",
            options=faixas_etarias,
            key="faixa_selecionada"  # vincula widget a st.session_state["faixa_selecionada"]
        )
        
        # 5) Agora use st.session_state.faixa_selecionada para filtrar o df
        df_filtrado = df[df["Grupo Etário"].isin(st.session_state.faixa_selecionada)]
        
        # Inverter valores dos homens para aparecerem à esquerda
        df_filtrado["Homens"] = df_filtrado["Homens"] * -1
        
        # remove a virgula dos milhares, ajusta para padrão BR
        df_milhar_ajustado = df_filtrado.copy()
        
        df_milhar_ajustado["Homens"] = df_milhar_ajustado["Homens"].abs()
        
        df_milhar_ajustado["Homens"] = df_milhar_ajustado["Homens"].apply(ajustar_milhar)
        
        df_milhar_ajustado["Mulheres"] = df_milhar_ajustado["Mulheres"].apply(ajustar_milhar)
        
        # Estatísticas resumidas
        total_homens = df_filtrado["Homens"].abs().sum()
        total_mulheres = df_filtrado["Mulheres"].sum()
        total_geral = total_homens + total_mulheres
                
        # Gráfico interativo
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=df_filtrado["Grupo Etário"],
            x=df_filtrado["Homens"],
            name="👨 Homens",
            orientation='h',
            marker_color="#B0E0E6",
            customdata=df_milhar_ajustado["Homens"],  # 👈 valores positivos para o tooltip
            hovertemplate="Homens: %{customdata:,}<extra></extra>",       
            marker=dict(line=dict(color="black", width=1))
        ))
        
        fig.add_trace(go.Bar(
            y=df_filtrado["Grupo Etário"],
            x=df_filtrado["Mulheres"],
            name="👩 Mulheres",
            orientation='h',
            marker_color="#FADADD",
            customdata=df_milhar_ajustado["Mulheres"],
            hovertemplate="Mulheres: %{customdata:,}<extra></extra>",
            marker=dict(line=dict(color="black", width=1))
        ))
        
        # Layout refinado
        fig.update_layout(
            barmode='overlay',
            title="📊 Distribuição da População por Sexo e Grupos Etários",
            xaxis=dict(title="População", tickvals=[-30000, -15000, 0, 15000, 30000],
                       ticktext=["30.000", "15.000", "0", "15.000", "30.000"],
                       title_font=dict(size=16, color="black"),
                       tickfont=dict(size=14, color="black")                       
                       ),
            yaxis=dict(title="Grupo Etário", 
                       autorange="reversed",
                       title_font=dict(size=16, color="black"),
                       tickfont=dict(size=14, color="black")                       
                       ),
            
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5,
                font=dict(size=14)
            ),
            height=700,
            margin=dict(t=80, b=60, l=60, r=60)
        )
        
        # Exibir gráfico
        st.plotly_chart(fig, use_container_width=True)
        
        with st.container(border = True):
            st.markdown("### 📌 Estatísticas Resumidas")
            st.markdown(
                f"- 👨 Total de homens nas faixas selecionadas: **{total_homens:,}**".replace(",", "."))
            st.markdown(
                f"- 👩 Total de mulheres nas faixas selecionadas: **{total_mulheres:,}**".replace(",", "."))
            st.markdown(
                f"- 👨‍👩‍👧‍👦 População total nas faixas selecionadas: **{total_geral:,}**".replace(",", "."))
        
        # Fonte
        st.markdown("🔗 Fonte: [Prefeitura Municipal de São José dos Campos – População](https://www.sjc.sp.gov.br/servicos/governanca/populacao/)")

def pop_região():    
    
    # 7) Dados oficiais da prefeitura
    dados_regiao = {
        "Região": ["Centro", 
                   "Leste", 
                   "Norte", 
                   "Oeste", 
                   "São Francisco Xavier", 
                   "Sudeste", 
                   "Sul", 
                   "Rural"
                   ],
        
        "População": [72401, 
                      181463, 
                      61940, 
                      64482, 
                      1443, 
                      62541, 
                      237572, 
                      15212
                      ]
        }
    
    df_regiao = pd.DataFrame(dados_regiao)    
    
    # 9) Gráfico de barras horizontal interativo
    fig = px.bar(
        df_regiao,
        x="População",
        y="Região",
        orientation="h",
        category_orders={"Região": df_regiao.sort_values("População")["Região"].tolist()},
        text="População",
        color="Região",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    
    # 10) Ajustes de traços: borda nas barras e posição do texto
    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        textfont=dict(color="black", size=14),
        marker_line_color="black",
        marker_line_width=1,
        cliponaxis=False,   # 👈 permite que o texto extrapole sem ser cortado
        hovertemplate="População: %{x:,.0f}<extra></extra>"
    )
    
    # 11.1) Linhas de grade para facilitar leitura
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="lightgray",
        zeroline=False
    )
    fig.update_yaxes(
        showgrid=False
    )

    
    # 11) Layout com separadores corretos e margens ajustadas
    fig.update_layout(
        title="📊 População por Região",
        xaxis=dict(title="População",
                   title_font=dict(size=16, color="black"),
                   tickfont=dict(size=14, color="black")
                   ),
        yaxis=dict(title="Região", 
                   autorange="reversed",
                   title_font=dict(size=16, color="black"),
                   tickfont=dict(size=14, color="black")
                   ),
        separators=",.",
        margin=dict(t=80, b=50, l=100, r=200),
        height=600,
        showlegend=False
    )
    
    with st.container(border=True):        
        # 6) Subtítulo
        # st.subheader("🗺️ População por Região")
        
        # 8) Tabela dentro do expander (sem índice)
        with st.expander("📋 Tabela de dados"):
            df_display = df_regiao.reset_index(drop=True)
            st.dataframe(df_display, 
                         use_container_width=True,
                         hide_index= True
                         )
        
        # 12) Renderiza o gráfico
        st.plotly_chart(fig, use_container_width=True)
        
        # 13) Fonte oficial
        st.markdown(
            "🔗 Fonte: [Prefeitura Municipal de São José dos Campos – População](https://www.sjc.sp.gov.br/servicos/governanca/populacao/)"
        )

def pop_região_map():

    # Dados de população e domicílios por região de São José dos Campos (Censo 2022)
    data = {
        "Região": [
            "Centro", "Leste", "Norte", "Oeste", "São Francisco Xavier",
            "Sudeste", "Sul", "Rural"
        ],
        "População": [
            72401, 181463, 61940, 64482, 1443, 62541, 237572, 15212
        ],
        "Domicílios": [
            34663, 70536, 24193, 26913, 754, 23410, 91937, 9808
        ],
        # Coordenadas aproximadas de cada região
        "Latitude": [
            -23.1896, -23.1860, -23.1610, -23.2020, -22.9142,
            -23.2170, -23.2430, -23.2700
        ],
        "Longitude": [
            -45.8840, -45.8510, -45.8800, -45.9150, -45.9594,
            -45.8700, -45.8900, -45.9500
        ]
    }    
        # Criar DataFrame
    df = pd.DataFrame(data)
    
    with st.container(border = True):

    # Título do aplicativo
        st.markdown("_**Mapa interativo**_")
        
        # Seletor de métrica
        metrica = st.selectbox("Selecione a métrica para visualização:", 
                               ["População", "Domicílios"])
    
        # Exibir tabela de dados
        st.badge("Você pode manipular e interagir com o mapa",
                 icon="🔎",
                 color= "green")
        # st.dataframe(df)
    
        # Criar o mapa com Pydeck
        layer = pdk.Layer(
        "ColumnLayer",
        data=df,
        get_position=["Longitude", "Latitude"],
        get_elevation=f"{metrica} / 100",    
        elevation_scale=4,
        radius=700,
        get_fill_color="[255 - Domicílios / 500, Domicílios / 500, 100, 160]", # 160 = ~63% opacidade
        pickable=True,
        auto_highlight=True
        )
    
    
    
        # Configuração da visualização do mapa
        view_state = pdk.ViewState(
        latitude=-23.2,
        longitude=-45.9,
        zoom=10,
        pitch=45,  # Inclinação para efeito 3D
        bearing=0
        )
        
        #ajusta o df para o tooltip usar separador de milhar padrão BR
        df["População"] = str(df["População"].apply(ajustar_milhar))
        df["Domicílios"] = str(df["Domicílios"].apply(ajustar_milhar))
        
        # df.rename(columns={"População": "Populacao", "Domicílios": "Domicilios"}, inplace=True)
    
    
        # Renderizar o mapa
        st.pydeck_chart(pdk.Deck(
            map_style="light",
            layers=[layer],
            initial_view_state=view_state,
            tooltip={
                "html": "<b>{Região}</b><br>População: {População}<br>Domicílios: {Domicílios}", 
                "style": {
                    "backgroundColor": "rgba(195, 195, 195, 0.85)",  # branco com 85% opacidade
                    "color": "black",
                    "borderRadius": "8px",  # cantos arredondados
                    "padding": "10px",
                    "boxShadow": "0px 0px 10px rgba(0, 0, 0, 0.2)"  # sombra leve
        }
    }
    
        ))
        
        st.markdown("""
        ### 🔍 Legenda
        
        - **Altura da coluna**: representa a quantidade de habitantes ou domicílios, conforme a métrica selecionada.
        - **Cor da coluna**: quanto mais verde, maior o número de habitantes ou domicílios.
        """)

def setor_socio():
    with st.container(border= True):
        # st.subheader("🏘️ População por Setores Socioeconômicos")
    
        # 3) Cria DataFrame
        df_setores = pd.read_csv("setor_socio.csv",encoding='latin-1', sep=";")
        
        # Lista de setores disponíveis
        setores_disponiveis = df_setores["Setor socioeconômico/área"].tolist()
        
        # Inicializa o estado da seleção
        if "setores_selecionados" not in st.session_state:
            st.session_state.setores_selecionados = setores_disponiveis
        
        # Botão de reset
        if st.button("🔄 Resetar seleção de setores"):
            st.session_state.setores_selecionados = setores_disponiveis
        
        # Caixa de seleção sempre visível
        setores_selecionados = st.multiselect(
            "🏘️ Selecione os setores que deseja visualizar:",
            options=setores_disponiveis,
            key="setores_selecionados"
        )
        
        # Botão para alternar entre gráfico de barras e gráfico de pizza
        tipo_grafico = st.radio(
            "📊 Escolha o tipo de gráfico:",
            options=["Barras", "Pizza"],
            horizontal=True
        )
    
    
        # Filtra o DataFrame com base na seleção
        df_filtrado = df_setores[df_setores["Setor socioeconômico/área"].isin(st.session_state.setores_selecionados)]
        
        df_filtrado = df_filtrado.sort_values(by= "População (2022)", ascending= True)
        # 4) Tabela sem índice
        with st.expander("📋 Tabela de dados"):
            st.dataframe(df_filtrado.reset_index(drop=True), 
                         hide_index= True,
                         use_container_width=True)
        
        # Cria o gráfico com base na escolha
        if tipo_grafico == "Barras":
            fig = px.bar(
                df_filtrado,
                x="População (2022)",
                y="Setor socioeconômico/área",
                orientation="h",
                text="População (2022)",
                color="Setor socioeconômico/área",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
        
            fig.update_traces(
                texttemplate="%{text:,}",
                textposition="outside",
                textfont=dict(color="black", size=14),
                marker_line_color="black",
                marker_line_width=1,
                cliponaxis=False,
                hovertemplate="População: %{x:,.0f}<extra></extra>"
            )
        
            fig.update_xaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor="lightgray",
                zeroline=False,
                tickfont=dict(size=14, family="Arial, sans-serif", color="black"),
                title_font=dict(size=16, family="Arial, sans-serif", color="black")
            )
            fig.update_yaxes(
                showgrid=False,
                tickfont=dict(size=14, family="Arial, sans-serif", color="black"),
                title_font=dict(size=16, family="Arial, sans-serif", color="black")
            )
        
            fig.update_layout(
                title="📊 Total de População por Setores Socioeconômicos",
                xaxis=dict(title="População", color= "black"),
                yaxis=dict(title="Setor", autorange="reversed", color="black"),
                separators=",.",
                margin=dict(t=80, b=50, l=250, r=150),
                height=800,
                showlegend=False
            )
        
        else:  # Gráfico de Pizza
            fig = px.pie(
                df_filtrado,
                names="Setor socioeconômico/área",
                values="População (2022)",
                color="Setor socioeconômico/área",
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.4
            )
        
            fig.update_traces(
                textinfo="label+percent",
                hovertemplate="%{label}: %{value:,.0f} habitantes<extra></extra>",
                marker=dict(line=dict(color="black", width=1))
            )
        
            fig.update_layout(
                title="🥧 Distribuição da População por Setores Socioeconômicos",
                separators=",.",
                height=600,
                font=dict(size=14, family="Arial, sans-serif"),
                margin=dict(t=100, b=100, l=50, r=50),
                showlegend=False
            )
        
        # Exibe o gráfico
        st.plotly_chart(fig, use_container_width=True)
        
        # 10) Fonte oficial
        st.markdown(
            "🔗 Fonte: [Prefeitura Municipal de São José dos Campos – População](https://www.sjc.sp.gov.br/servicos/governanca/populacao/)"
        )

def pop_região_pizza():
    with st.container(border=True):
        # 1) Carrega os dados do arquivo
        df = pd.read_csv("pop_socio.csv", encoding='latin-1', sep=";")
        
        # 2) Agrupa por região somando a população
        df_agrupado = df.groupby("Região", as_index=False)["População"].sum()
                
        # 4) Gráfico de pizza
        fig = px.pie(
            df_agrupado,
            names="Região",
            values="População",
            color="Região",
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        
        # 5) Ajustes visuais
        fig.update_traces(
            textinfo="label+percent+value",
            hovertemplate="%{label}: %{value:,.0f} habitantes<extra></extra>",
            marker=dict(line=dict(color="black", width=1))
        )
        
        # 6) Layout com legenda visível e fontes legíveis
        fig.update_layout(
            title="🥧 Distribuição da População por Região",
            separators=",.",
            height=800,
            font=dict(size=14, family="Arial, sans-serif"),
            margin=dict(t=80, b=50, l=50, r=250),
            showlegend=False,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.05,
                font=dict(size=13)
            )
        )
        # 3) Tabela sem índice
        with st.expander("📋 Ver população total por região"):
            st.dataframe(df_agrupado.reset_index(drop=True), 
                         hide_index=True,
                         use_container_width=True)        
        # 7) Exibe o gráfico
        st.plotly_chart(fig, use_container_width=True)
        
        # 8) Fonte oficial
        st.markdown(
            "🔗 Fonte: [Prefeitura Municipal de São José dos Campos – População](https://www.sjc.sp.gov.br/servicos/governanca/populacao/)"
        )

def pop_socio_2():
    with st.container(border= True):    
        # Carrega os dados
        df = pd.read_csv("pop_socio.csv",encoding='latin-1', sep=";")
        
        # Lista de regiões únicas
        regioes_disponiveis = df["Região"].dropna().unique().tolist()
        
        # Filtro de seleção de região
        regiao_selecionada = st.selectbox(
            "🗺️ Selecione uma região para visualizar os subsetores:",
            options=regioes_disponiveis
        )
        
        # Filtra os subsetores da região escolhida
        df_subsetores = df[df["Região"] == regiao_selecionada]
        
        # Ordena os subsetores por população (do maior para o menor)
        df_subsetores = df_subsetores.sort_values(by="População", ascending=False)
        
        # Gráfico de barras por subsetores da região selecionada
        fig = px.bar(
            df_subsetores,
            x="População",
            y="Susbsetor \x96 Nome",
            orientation="h",
            text="População",
            color="Susbsetor \x96 Nome",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_traces(
            texttemplate="%{text:,}",
            textposition="outside",
            textfont=dict(color="black", size=14),
            marker_line_color="black",
            marker_line_width=1,
            cliponaxis=False,
            hovertemplate="%{y}: %{x:,.0f} habitantes<extra></extra>"
        )
        
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor="lightgray",
            zeroline=False,
            tickfont=dict(size=14, family="Arial, sans-serif", color="black"),
            title_font=dict(size=16, family="Arial, sans-serif", color="black")
        )
        fig.update_yaxes(
            showgrid=False,
            tickfont=dict(size=14, family="Arial, sans-serif", color="black"),
            title_font=dict(size=16, family="Arial, sans-serif", color="black")
        )
        
        fig.update_layout(
            title=f"📊 População por Subsetores – Região {regiao_selecionada}",
            separators=",.",
            height=900,
            margin=dict(t=80, b=50, l=250, r=150),
            showlegend=False
        )
        
        with st.expander("📋 Ver tabela de subsetores da região selecionada"):
            st.dataframe(df_subsetores[["Susbsetor \x96 Nome", "População"]].reset_index(drop=True), 
                         use_container_width=True,
                         hide_index = True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        

if __name__ == "__main__":
    
    #configura a página.
    st.set_page_config(page_title="Dados SJC",
                       page_icon="📊")

    # Exibe automaticamente ao carregar
    st.toast("📢 Por gentileza, não se esqueça de responder ao formulário de pesquisa. Obrigado.", icon="🔔")
    
    # Estado para controlar visibilidade
    if "show_popup" not in st.session_state:
        st.session_state.show_popup = True
    
    def fechar_popup():
        st.session_state.show_popup = False
    
    # Simula um popup visual
    if st.session_state.show_popup:
        st.markdown(
            """
            <div style='
                background-color: #fff3cd;
                padding: 20px;
                border-radius: 10px;
                border: 1px solid #ffeeba;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                font-size: 16px;
                color: #856404;
                animation: fadeIn 0.5s ease-in-out;
            '>
                <strong>📢 Atenção:</strong>Por gentileza, não se esqueça de responder ao formulário de pesquisa. Obrigado!<br>
                </div>
            """,
            unsafe_allow_html=True
        )
        st.button("Fechar mensagem", on_click=fechar_popup)

    
    #cabeçalho
    st.title("Informações Populacionais")
    st.title("Município de São José dos Campos")
    
    with st.container(border= True):
        st.markdown("Os dados de população exibidos nesta página consideram as informações do Censo Demográfico 2022, realizado pelo IBGE, que divulga anualmente estimativas de população total para todo o município, porém não prevê o detalhamento da estimativa para regiões da cidade ou características específicas da população.")
   
    #apenas para espaçar as seções
    st.write("")
    st.write("")
    st.write("")
    
    
    ###########################################################################
    #seção população totoal e por genero    
    st.subheader("**População Total e divisão por Gênero 👪🏾**")
    st.badge("Você expandir ou contrair as seções para facilitar a visualização da página.",
             icon = "🔥",
             color = "red"
             )
    with st.expander("**População Total e divisão por Gênero**", 
                     expanded= True,
                     icon= ":material/diversity_3:"):       
        plotly_genderchart()
    
    st.divider()
    
    ###########################################################################
    #seção população urbana e rural
    st.subheader("**População Urbana e Rural 👨‍⚖️👩🏽‍🌾**")
    
    with st.expander("**População Urbana e Rural**", 
                     expanded= False,
                     icon= ":material/sword_rose:"):       
        pop_urb_rural()
        
    st.divider()
    
    ###########################################################################
    #seção domicilios por tipo
    st.subheader("**Total de domícilios por tipo 🏘️**")
    
    with st.expander("**Total de domícilios por tipo**", 
                     expanded= False,
                     icon= ":material/house:"):       
        domicilios()
        
    st.divider()
    
    ###########################################################################
    #Evolução da participação percentual dos grupos etários na população
    st.subheader("**Evolução da participação dos grupos etários na população 👶🏿👴**")
    
    with st.expander("**Evolução da participação dos grupos etários na população**", 
                     expanded= False,
                     icon= ":material/elderly:"):       
        pop_etaria_2()
        
    st.divider()
    
    ###########################################################################
    #Piramide Etária por sexo e faixas quinquenais
    st.subheader("**Piramide Etária por sexo e faixas quinquenais 👶🏼👵🏿**")
    
    with st.expander("**Piramide Etária por sexo e faixas quinquenais**", 
                     expanded= False,
                     icon= ":material/add_triangle:"):       
        piramide_etaria()
        
    st.divider()
    
    ###########################################################################
    #População por região
    st.subheader("**População por região 👩‍👩‍👧‍👦 🗺️**")
    
    with st.expander("**População por região**", 
                     expanded= False,
                     icon= ":material/map_search:"):
        
        pop_região()    
        
        pop_região_map()
        
    st.divider()
    
    ###########################################################################
    #População por setores socioeconomicos
    st.subheader("**População por setores socioeconômicos 🙋‍♂️🙋🏽‍♀️📍**")
    
    with st.expander("**População por setores socioeconômicos**", 
                     expanded= False,
                     icon= ":material/location_on:"):
        
        setor_socio()
        
    st.divider()
    
    ###########################################################################
    #População por subsetores socioeconomicos
    st.subheader("**População por subsetores socioeconômicos 🙋🏽‍♀️🙋‍♂️📍**")
    
    with st.expander("**População por setores socioeconômicos**", 
                     expanded= False,
                     icon= ":material/share_location:"):
        
        pop_socio_2()
        
    # st.divider()
       
    
    
    
    
      
    
        
    
        
    
    
    
    
    
    
    # st.set_page_config(page_title="Dashboard Populacional – SJC", layout="wide")
    # st.title("📊 Dashboard Populacional – São José dos Campos")
    
    # # Tabs temáticas
    # tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([
    #     "Pirâmide Etária",
    #     "Faixa Etária (Comparativo)",
    #     "Urbano vs Rural",
    #     "Domicílios",
    #     "Regiões",
    #     "Mapa por Região",
    #     "Resumo por Região",
    #     "Subsetores",
    #     "Setores Socioeconômicos",
    #     "Escolaridade",
    #     "Sobre"
    # ])
    
    # with tab1:
    #     piramide_etaria()
    
    # with tab2:
    #     pop_etaria_2()
    
    # with tab3:
    #     pop_urb_rural()
    
    # with tab4:
    #     domicilios()
    
    # with tab5:
    #     pop_região()
    
    # with tab6:
    #     pop_região_map()
    
    # with tab7:
    #     pop_socio()
    
    # with tab8:
    #     pop_socio_2()
    
    # with tab9:
    #     setor_socio()
    
    # with tab10:
    #     st.markdown("📚 Em breve: distribuição por escolaridade")
    
    # with tab11:
    #     st.markdown("""
    #     ### 👋 Sobre o Projeto
    
    #     Este painel foi desenvolvido por Viviane com o objetivo de tornar os dados populacionais de São José dos Campos mais acessíveis, visuais e interativos.  
    #     Ele utiliza dados oficiais do Censo 2022 e da Prefeitura Municipal, combinando gráficos refinados, filtros inteligentes e visualizações geoespaciais.
    
    #     ---
    #     🔗 [Fonte oficial dos dados](https://www.sjc.sp.gov.br/servicos/governanca/populacao/)  
    #     🛠️ Desenvolvido com Python, Streamlit, Plotly e Pydeck  
    #     📅 Última atualização: setembro de 2025
    #     """)
    
    # st.title("📊 Panorama Populacional – São José dos Campos")

    # col1, col2 = st.columns(2)
    
    # with col1:
    #     piramide_etaria()
    
    # with col2:
    #     pop_etaria_2()
        
    # st.markdown("## 🏘️ População e Domicílios")

    # col3, col4 = st.columns(2)
    
    # with col3:
    #     pop_urb_rural()
    
    # with col4:
    #     domicilios()
        
    # st.markdown("## 🗺️ Distribuição por Região")

    # col5, col6 = st.columns([1, 1.2])
    
    # with col5:
    #     pop_região()
    
    # with col6:
    #     pop_região_map()
        
    # st.markdown("## 🧩 Setores Socioeconômicos e Subsetores")

    # col7, col8 = st.columns(2)
    
    # with col7:
    #     setor_socio()
    
    # with col8:
    #     pop_socio_2()
        
    # st.markdown("## 🥧 Resumo por Região")

    # pop_socio()
    
    # st.markdown("## 📚 Escolaridade")

    # st.info("Em breve: distribuição por escolaridade com dados do Censo 2022.")
    
    # st.markdown("---")
    # st.markdown("""
    # 🔗 [Fonte oficial dos dados](https://www.sjc.sp.gov.br/servicos/governanca/populacao/)  
    # 🛠️ Desenvolvido por Viviane com Python, Streamlit, Plotly e Pydeck  
    # 📅 Última atualização: setembro de 2025
    # """)
    
    # # Configuração da página
    # st.set_page_config(page_title="Dashboard Populacional – SJC", layout="wide")
    # st.title("📊 Dashboard Populacional – São José dos Campos")
    
    # # Seções com expansores
    # with st.expander("👥 Pirâmide Etária"):
    #     piramide_etaria()
    
    # with st.expander("📊 Comparativo por Faixa Etária (2010 vs 2022)"):
    #     pop_etaria_2()
    
    # with st.expander("🌆 População Urbana vs Rural"):
    #     pop_urb_rural()
    
    # with st.expander("🏠 Domicílios por Tipo de Área"):
    #     domicilios()
    
    # with st.expander("📍 População por Região"):
    #     pop_região()
    
    # with st.expander("🗺️ Mapa 3D por Região"):
    #     pop_região_map()
    
    # with st.expander("🥧 Distribuição da População por Região"):
    #     pop_socio()
    
    # with st.expander("📌 População por Subsetores"):
    #     pop_socio_2()
    
    # with st.expander("🏘️ População por Setores Socioeconômicos"):
    #     setor_socio()
    
    # with st.expander("📚 Escolaridade (em breve)"):
    #     st.info("Em breve: distribuição por escolaridade com dados do Censo 2022.")
    
    # # Rodapé
    # st.markdown("---")
    # st.markdown("""
    # 🔗 [Fonte oficial dos dados](https://www.sjc.sp.gov.br/servicos/governanca/populacao/)  
    # 🛠️ Desenvolvido por Viviane com Python, Streamlit, Plotly e Pydeck  
    # 📅 Última atualização: setembro de 2025
    # """)
