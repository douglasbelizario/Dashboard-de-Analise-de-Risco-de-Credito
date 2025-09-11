import streamlit as st
import pandas as pd
import plotly.express as px

#st.set_page_config() para configurar o título da aba, o ícone e o layout.
# "wide" aproveita melhor o espaço em telas maiores.
st.set_page_config(
    page_title="Dashboard de Risco de Crédito",
    page_icon="🪙",
    layout="wide"
)



#@st.cache_data para que o Streamlit não precise recarregar os dados
# toda vez que o usuário interage com um filtro. Ele guarda os dados em cache (Necessário ser uma função).
@st.cache_data
def carregar_dados():
    df = pd.read_csv('dados/credito_alemao_tratado_final.csv', sep=';', decimal=',')
    return df


df_original = carregar_dados()

st.sidebar.header("Filtros Interativos")

proposito_selecionado = st.sidebar.selectbox(
    "Selecione o Propósito do Crédito",
    options=['Todos'] + sorted(df_original['Proposito'].unique()),
    index=0 # 'Todos' será a opção padrão
)

faixa_etaria_selecionada = st.sidebar.selectbox(
    "Selecione a Faixa Etária",
    options=['Todos'] + sorted(df_original['Faixa_Etaria'].unique()),
    index=0
)

# Criei uma cópia filtrada para usar no dashboard.
# Isso evita problemas e torna o código mais claro.
df_filtrado = df_original.copy()

if proposito_selecionado and proposito_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Proposito'] == proposito_selecionado]

if faixa_etaria_selecionada and faixa_etaria_selecionada != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Faixa_Etaria'] == faixa_etaria_selecionada]


st.sidebar.markdown("---")
st.sidebar.markdown("Feito por **Douglas Belizario**")
st.sidebar.markdown("Conecte-se comigo:")
st.sidebar.markdown("➡️ [Meu LinkedIn](https://www.linkedin.com/in/douglassbelizario/)")
st.sidebar.markdown("➡️ [Meu GitHub](https://github.com/douglasbelizario)")    

#LAYOUT PRINCIPAL DO DASHBOARD

# Título do Dashboard
st.title("🪙 Dashboard de Análise de Risco de Crédito")
st.markdown("Use os filtros na barra lateral para explorar os dados.")
st.markdown("---")

# Calculo as métricas com base no DataFrame JÁ FILTRADO.
total_clientes = df_filtrado.shape[0]
maus_pagadores = df_filtrado[df_filtrado['Risco'] == 'Ruim'].shape[0]
taxa_inadimplencia = (maus_pagadores / total_clientes) * 100 if total_clientes > 0 else 0
valor_total_credito = df_filtrado['Valor_Credito'].sum()

# Uso colunas para organizar as métricas lado a lado.
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total de Clientes", f"{total_clientes:,}".replace(",", "."))
with col2:
    st.metric("Taxa de Inadimplência", f"{taxa_inadimplencia:.2f}%")
with col3:
    valor_formatado_br = f"{valor_total_credito:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    st.metric("Valor Total Emprestado (Marco alemão)", f"{valor_formatado_br} DM")

st.markdown("---")

#GRÁFICOS
# Um layout com duas colunas e um gráfico de largura total abaixo
# costuma ser mais agradável visualmente do que três colunas apertadas.
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    # Gráfico 1: Risco por Faixa Etária
    st.subheader("Risco por Faixa Etária")
    fig_faixa_etaria = px.histogram(
        df_filtrado,
        x='Faixa_Etaria',
        color="Risco",
        barmode='group',
        text_auto=True,
        title="Contagem de Clientes por Faixa Etária e Risco",
        color_discrete_map={'Bom': '#1f77b4', 'Ruim': '#d62728'},
        labels={"Faixa_Etaria": "Faixa Etária", "count": "Quantidade de Clientes", "Risco": "Risco"}
    )
    st.plotly_chart(fig_faixa_etaria, use_container_width=True)

with col_graf2:
    # Gráfico 2: Proporção de Risco (Pizza)
    st.subheader("Proporção Geral de Risco")
    df_risco = df_filtrado['Risco'].value_counts().reset_index()
    fig_risco = px.pie(
        df_risco,
        names='Risco',
        values='count',
        title="Proporção de Clientes Bons vs. Ruins",
        color='Risco',
        color_discrete_map={'Bom': '#1f77b4', 'Ruim': '#d62728'}
    )
    st.plotly_chart(fig_risco, use_container_width=True)

# Gráfico 3 ocupando a largura total para melhor visualização
st.subheader("Risco por Propósito do Crédito")
fig_proposito = px.histogram(
    df_filtrado,
    x='Proposito',
    color='Risco',
    barmode='group',
    text_auto=True,
    title="Contagem de Clientes por Propósito do Crédito e Risco",
    color_discrete_map={'Bom': '#1f77b4', 'Ruim': '#d62728'},
    labels={"Proposito": "Propósito do Crédito", "count": "Quantidade de Clientes", "Risco": "Risco"}
)

fig_proposito.update_layout(xaxis={'categoryorder': 'total descending'})
st.plotly_chart(fig_proposito, use_container_width=True)
