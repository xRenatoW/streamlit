import pandas as pd
import yfinance as yf
import datetime as dt
import streamlit as st

st.set_page_config(page_title='Dashboard Financeiro', layout="wide")

st.title('Dashboard Financeiro')

data_final = dt.datetime.today()
data_inicial = dt.datetime.today() - dt.timedelta(days=365)

with st.container():
    st.header('Insira as informações solicitadas abaixo:')
    col1, col2, col3 = st.columns(3)

    with col1:
        ativo = st.selectbox('Selecione o ativo desejado:', options=['PETR4.SA', 'VALE3.SA', 'MGLU3.SA', 'ITSA4.SA'])

    with col2:
        data_inicial = st.date_input('Selecione a Data Inicial:', data_inicial)
    with col3:
        data_final = st.date_input('Selecione a Data Final:', data_final)

# Retornar dados da API
df = yf.download(ativo, start=data_inicial, end=data_final)

# Criar métricas
ult_atualizacao = df.index.max()  # Data da última atualização
ult_cotacao = round(df.loc[df.index.max(), 'Adj Close'], 2)  # Última cotação encontrada
menor_cotacao = round(df['Adj Close'].min(), 2)
maior_cotacao = round(df['Adj Close'].max(), 2)
primeira_cotacao = round(df.loc[df.index.min(), 'Adj Close'], 2)
delta = round(((ult_cotacao - primeira_cotacao) / primeira_cotacao) * 100, 2)

with st.container():
    with col1:
        st.metric(f"Ultima atualização - {ult_atualizacao}","{:,.2f}".format(ult_cotacao),f"{delta}%")
    with col2:
        st.metric("Menor cotação do periodo","{:,.2f}".format(maior_cotacao))
    with col3:
        st.metric("Maior cotação do periodo", "{:,.2f}".format(maior_cotacao))

# Layout do dashboard
with st.container():
    st.header('Gráfico de Preços:')
    st.area_chart(df[['Adj Close']])
    st.line_chart(df[['Low','Adj Close','High']])



with st.container():
        st.header('Dados Históricos:')
        st.dataframe(df.head(10),1000,400)

with st.container():
    st.header('Métricas:')
    st.write(f"Última Atualização: {ult_atualizacao}")
    st.write(f"Última Cotação: R$ {ult_cotacao}")
    st.write(f"Menor Cotação: R$ {menor_cotacao}")
    st.write(f"Maior Cotação: R$ {maior_cotacao}")
    st.write(f"Primeira Cotação: R$ {primeira_cotacao}")
    st.write(f"Variação: {delta}%")
#
#
#Botão para Download dos Dados em CSV
# st.download_button('Baixar Dados em CSV', df.to_csv(index=False).encode('utf-8'), 'dados_historicos.csv', 'text/csv')
