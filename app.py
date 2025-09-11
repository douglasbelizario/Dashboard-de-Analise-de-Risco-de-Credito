import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard de Risco de Crédito",
    page_icon="🪙",
    layout="wide"
)

@st.cache_data
def carregar_dados():
    df = pd.read_csv('dados/credito_alemao_tratado_final.csv', sep=';', decimal=',')
    return df

df = carregar_dados()

st.sidebar.header("Filtros")

proposito_selecionado = st.sidebar.selectbox(
    "Selecione o Propósito do Crédito",
    options=df['Proposito'].unique(),
    index=None, # Faz com que a opção 'placeholder' apareça
    placeholder="Todos"
)

faixa_etaria_selecionada = st.sidebar.selectbox(
    "Selecione a Faixa Etária",
    options=df['Faixa_Etaria'].unique(),
    index=None,
    placeholder="Todos"
)

# Aplicando os filtros ao DataFrame
if proposito_selecionado:
    df = df[df['Proposito'] == proposito_selecionado]

if faixa_etaria_selecionada:
    df = df[df['Faixa_Etaria'] == faixa_etaria_selecionada]  

# Aplicando os filtros ao DataFrame
if proposito_selecionado:
    df = df[df['Proposito'] == proposito_selecionado]

if faixa_etaria_selecionada:
    df = df[df['Faixa_Etaria'] == faixa_etaria_selecionada]


st.title("🪙 Dashboard de Análise de Risco de Crédito")
st.markdown("---")

total_clientes = df.shape[0]
maus_pagadores = df[df['Risco'] == 'Ruim'].shape[0]
taxa_inadimplencia = (maus_pagadores / total_clientes) * 100 if total_clientes > 0 else 0
valor_total_credito = df['Valor_Credito'].sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total de Clientes", f"{total_clientes:,}".replace(",", "."))
with col2:
    st.metric("Taxa de Inadimplência", f"{taxa_inadimplencia:.2f}%")
with col3:
    st.metric("Valor Total Emprestado (DM)", f"{valor_total_credito:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")

col_graf1, col_graf2, col_graf3 = st.columns(3)

with col_graf1:
    # Gráfico1: Risco por Propósito do Crédito
    st.subheader("Risco por Propósito do Crédito")
    fig_proposito = px.histogram(df, 
                                 x='Proposito', 
                                 color='Risco', 
                                 barmode='group',
                                 text_auto=True,
                                 color_discrete_map={'Bom': '#1f77b4', 'Ruim': '#d62728'})
    st.plotly_chart(fig_proposito, use_container_width=True)

with col_graf2:
    # Gráfico2: Proporção de Risco (Pizza)
    st.subheader("Proporção Geral de Risco")
    df_risco = df['Risco'].value_counts().reset_index()
    fig_risco = px.pie(df_risco, 
                       names='Risco', 
                       values='count',
                       color='Risco',
                       color_discrete_map={'Bom': '#1f77b4', 'Ruim': '#d62728'},
                       labels={
                                        "Proposito": "Propósito do cliente",
                                        "count": "Quantidade de Clientes",
                                        "Risco": "Risco de Crédito"
                                    }
                        )
                    

    st.plotly_chart(fig_risco, use_container_width=True)

with col_graf3:    
    # Gráfico3: Total de clientes por faixa etária
    st.subheader("Risco por Faixa Etária")
    fig_faixa_etaria = px.histogram(df,
                              x='Faixa_Etaria',
                              color="Risco",
                              barmode='group',
                              text_auto=True,
                              color_discrete_map={'Bom': '#1f77b4', 'Ruim': '#d62728'},
                              labels={
                                        "Faixa_Etaria": "Faixa Etária",
                                        "count": "Quantidade de Clientes",
                                        "Risco": "Risco de Crédito"   
                                    }
                              ) 
    st.plotly_chart(fig_faixa_etaria, use_container_width=True)                          


