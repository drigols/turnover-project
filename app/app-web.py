from pycaret.classification import load_model, predict_model
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import joblib


model = load_model('my_model') # Da um load no nosso modelo com Pycaret.
model_cluster = joblib.load("cluster.joblib") # Da um load no nosso Cluster.
dataset = pd.read_csv("dataset.csv") # Carregar nosso conjunto de dados.

########################## (Streamlit Main content) ##########################

# Define um título para a página.
st.title("Turnover Project")

# Define um subtítulo para a página.
st.markdown("Este é um Data App utilizado para exibir a solução de Machine Learning que tenta prever se um funcionário vai deixar a empresa.")

# Exibe às 100 primeiras amostras do nosso Dataset (DataFrame) no App.
st.dataframe(dataset.head(100))

# Cria uma lógica que implementa cores para o nosso cluster.
kmeans_colors = ['green' if c == 0 else 'red' if c == 1 else 'blue' for c in model_cluster.labels_]

########################## (Streamlit Side content) ##########################

# Define um header para a nossa barra lateral.
st.sidebar.subheader("Defina os atributos do funcionário para predição de turnover")

# [Mapeamento das principais Features (Atributos, Colunas, Variáveis) para o nosso App]
# Nós estamos utilizando a média (mean) porque vai ser ela que vai ser exibida assim que o usuário
# abrir o App. Ou seja, a caixa de entrada já vai iniciar com a média de cada Feature.
# Isso porque nós estamos mapeando um valor para cada caixinha e esse atributo "value" precisa de uma
# entrada inicial (mesmo que seja antes do usuário digitar algo). Outra alternativa seria você não utilizar
# o atributo "value=dataset["x_feature"].mean" e nós teríamos uma caixinha vazia só esperando o usuário digitar algo.
satisfaction = st.sidebar.number_input("satisfaction", value=dataset["satisfaction"].mean())
evaluation = st.sidebar.number_input("evaluation", value=dataset["evaluation"].mean())
averageMonthlyHours = st.sidebar.number_input("averageMonthlyHours", value=dataset["averageMonthlyHours"].mean())
yearsAtCompany = st.sidebar.number_input("yearsAtCompany", value=dataset["yearsAtCompany"].mean())

# Define um botão que ao ser clicado vai classificar (predizer)
# se o funcionário vai continuar ou sair da empresa.
btn_predict = st.sidebar.button("Realizar Classificação")

# Verifica se o botão foi clicado e se (if) for clicado ele vai
# implementar uma classificação que vai dizer se o funcionário
# vai continuar ou sair da empresa.
if btn_predict:

  # Faz um mapeamento entre as entradas do usuário e nosso DataFrame de teste = data_teste.
  data_teste = pd.DataFrame()
  data_teste["satisfaction"] = [satisfaction]
  data_teste["evaluation"] =	[evaluation]    
  data_teste["averageMonthlyHours"] = [averageMonthlyHours]
  data_teste["yearsAtCompany"] = [yearsAtCompany]
    
  # Realiza a predição com a função precit_model() do Pycaret, esse método vai receber:
  # - Nosso modelo (que nós baixamos do Data Lake).
  # - Os dados de teste, que vão ser passados pelo usuário.
  result = predict_model(model, data=data_teste)
    
  # Escreve no App o resultado da predição do nosso modelo baseado nas entradas do usuário.
  st.write(result)

  ########################## (Definição do gráfico/plot) ##########################
  fig = plt.figure(figsize=(10, 6)) # Define o tamando do gráfico
  plt.scatter(
    x = "satisfaction",
    y = "evaluation",
    data = dataset[dataset.turnover==1],
    alpha = 0.25,color = kmeans_colors
  )
  plt.xlabel("Satisfaction")
  plt.ylabel("Evaluation")
  plt.scatter(
    x = model_cluster.cluster_centers_[:,0],
    y = model_cluster.cluster_centers_[:,1],
    color  = "black",
    marker = "X",s=100
  )
  # Exibe no gráfico/plot onde está o valor de entrada pelo usuário.
  # Ou seja, onde nós estamos na predição se comparado com o gráfico.
  plt.scatter(
    x = [satisfaction],
    y = [evaluation],
    color  = "yellow",
    marker = "X",s=300
  )
  plt.title("Grupos de Empregados - Satisfação vs Avaliação.")
  plt.show()
  st.pyplot(fig)
