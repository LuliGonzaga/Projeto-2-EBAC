import os
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time
from PIL import Image
from streamlit_pandas_profiling import st_profile_report


sns.set(context='talk', style='ticks')

st.set_page_config(
     page_title="Projeto 2 - Previsão de renda",
     page_icon="https://upload.wikimedia.org/wikipedia/commons/d/dc/MSN_Money_icon.png",
     layout="wide",
)

with st.sidebar:
   image = Image.open('./input/logo_previsao.png')
   st.image(image)

   st.title('Previsão de renda')
   st.caption('Este é um problema de concessão de cartões de crédito, no qual uma instituição financeira deseja estabelecer melhores critérios para a concessão de crédito.')
   st.caption('O objetivo é construir um modelo preditivo para identificar a renda de novos clientes a partir da base de dados do perfil de renda de clientes já existentes.')


st.title('Ciência de Dados: Projeto 2')
st.subheader('Análise exploratória dos dados')
st.caption('''Etapa fundamental no processo de análise de dados que visa entender, resumir e visualizar os principais padrões, características e informações contidas em um conjunto de dados.
          A EDA desempenha um papel crucial na compreensão dos dados antes de aplicar técnicas mais avançadas de modelagem ou análise''')
 
st.markdown('----')

@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv)  # 👈 Download the data
    return df
df = load_data('./input/previsao_de_renda.csv')
df1 = df.drop(['Unnamed: 0', 'data_ref', 'id_cliente', 'tipo_residencia'], axis=1).copy()
df1 = df1.drop_duplicates()
media = df1['tempo_emprego'].mean()
df1['tempo_emprego'] = df1['tempo_emprego'].fillna(media)
df2 = df1[df1['renda'] <= 60000]
df2 = df2[df2['qtd_filhos'] <=4]
df2 = df2[df2['tempo_emprego'] <= 30]
df2 = df2[df2['qt_pessoas_residencia'] <= 6]
df3 = pd.get_dummies(df2, columns=['sexo', 'tipo_renda', 'educacao', 'estado_civil'], drop_first=True).copy()
df3 = df3.drop(['tipo_renda_Bolsista',
               'educacao_Pós graduação', 'educacao_Superior incompleto',
               'estado_civil_Separado', 'estado_civil_Viúvo'], axis=1).copy()
df3['tempo_emprego'] = df3['tempo_emprego'].apply(lambda x: round(x * 2) / 2)
df3.rename(columns={'educacao_Superior completo':'educacao_Superior_completo',
               'tipo_renda_Servidor público':'tipo_renda_Servidor_público'}, inplace=True)
df3 = df3.reset_index(drop=True)

dados = st.radio(
    "Visualizar análise de:",
    ['Dados Brutos', 'Dados Tratados'])

st.subheader(dados,':')


if dados == 'Dados Brutos':

     df

     st.markdown('----')

     st.subheader('Entendimento dos dados:')
     '**Univariadas:** Análise de distribuição das variáveis'

     with st.expander("Ver análise completa"):
          pr = df.profile_report()
          st_profile_report(pr)

     '**Bivariadas:** Análise de comportamento das variáveis em relação a variável renda.'
     st.caption('Selecione o tipo de variável:')

     tab1, tab2, tab3 = st.tabs(['Booleanas', "Categóricas", "Numéricas"])

     with tab1:
          st.subheader("Booleanas")
          fig, axes = plt.subplots(1, 2, figsize=(15, 5), constrained_layout=True)
          sns.pointplot(ax = axes[0], x='posse_de_veiculo', y='renda', data=df)
          sns.pointplot(ax = axes[1], x='posse_de_imovel', y='renda', data=df)
          st.pyplot(fig)

     with tab2:
          st.subheader("Categóricas")
          fig, axes = plt.subplots(2, 2, figsize=(20, 10), constrained_layout=True)
          sns.barplot(ax = axes[0,0], x='tipo_renda', y='renda', data=df)
          sns.barplot(ax = axes[0,1], x='educacao',y='renda', data=df)
          sns.barplot(ax = axes[1,0], x='estado_civil', y='renda', data=df)
          sns.barplot(ax = axes[1,1], x='tipo_residencia',y='renda', data=df)
          st.pyplot(fig)

     with tab3:
          st.subheader("Numéricas")
          fig, axes = plt.subplots(2, 2, figsize=(20, 10), constrained_layout=True)
          sns.lineplot(ax = axes[0,0], x='qtd_filhos', y='renda', data=df)
          sns.lineplot(ax = axes[0,1], x='idade',y='renda', data=df)
          sns.lineplot(ax = axes[1,0], x='tempo_emprego', y='renda', data=df)
          sns.lineplot(ax = axes[1,1], x='qt_pessoas_residencia',y='renda', data=df)
          st.pyplot(fig)



else:

     df3

     st.markdown('----')

     st.subheader('Entendimento dos dados:')
     '**Univariadas:** Análise de distribuição das variáveis'

     with st.expander("Ver análise completa"):
          pr = df3.profile_report(explorative=True, minimal=True)
          st_profile_report(pr)

     '**Bivariadas:** Análise de comportamento das variáveis em relação a variável renda.'
     st.caption('Selecione o tipo de variável:')

     tab1, tab2, tab3 = st.tabs(['Booleanas', "Categóricas", "Numéricas"])

     with tab1:
          st.subheader("Booleanas")
          fig, axes = plt.subplots(1, 2, figsize=(15, 5), constrained_layout=True)
          sns.pointplot(ax = axes[0], x='posse_de_veiculo', y='renda', data=df3)
          sns.pointplot(ax = axes[1], x='posse_de_imovel', y='renda', data=df3)
          st.pyplot(fig)

     with tab2:
          st.subheader("Categóricas")
          fig, axes = plt.subplots(2, 4, figsize=(20, 10), constrained_layout=True)
          sns.barplot(ax = axes[0,0], x='tipo_renda_Empresário', y='renda', data=df3)
          sns.barplot(ax = axes[0,1], x='tipo_renda_Pensionista',y='renda', data=df3)
          sns.barplot(ax = axes[0,2], x='tipo_renda_Servidor_público', y='renda', data=df3)
          sns.barplot(ax = axes[0,3], x='educacao_Secundário',y='renda', data=df3)
          sns.barplot(ax = axes[1,0], x='educacao_Superior_completo',y='renda', data=df3)
          sns.barplot(ax = axes[1,1], x='estado_civil_Solteiro',y='renda', data=df3)
          sns.barplot(ax = axes[1,2], x='estado_civil_União',y='renda', data=df3)
          st.pyplot(fig)

     with tab3:
          st.subheader("Numéricas")
          fig, axes = plt.subplots(2, 2, figsize=(20, 10), constrained_layout=True)
          sns.lineplot(ax = axes[0,0], x='qtd_filhos', y='renda', data=df3)
          sns.lineplot(ax = axes[0,1], x='idade',y='renda', data=df3)
          sns.lineplot(ax = axes[1,0], x='tempo_emprego', y='renda', data=df3)
          sns.lineplot(ax = axes[1,1], x='qt_pessoas_residencia',y='renda', data=df3)
          st.pyplot(fig)