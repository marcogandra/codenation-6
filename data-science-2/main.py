#!/usr/bin/env python
# coding: utf-8

# # Desafio 4
# 
# Neste desafio, vamos praticar um pouco sobre testes de hipóteses. Utilizaremos o _data set_ [2016 Olympics in Rio de Janeiro](https://www.kaggle.com/rio2016/olympic-games/), que contém dados sobre os atletas das Olimpíadas de 2016 no Rio de Janeiro.
# 
# Esse _data set_ conta com informações gerais sobre 11538 atletas como nome, nacionalidade, altura, peso e esporte praticado. Estaremos especialmente interessados nas variáveis numéricas altura (`height`) e peso (`weight`). As análises feitas aqui são parte de uma Análise Exploratória de Dados (EDA).
# 
# > Obs.: Por favor, não modifique o nome das funções de resposta.

# ## _Setup_ geral

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sct
import seaborn as sns
import statsmodels.api as sm


# In[3]:


#%matplotlib inline

from IPython.core.pylabtools import figsize


figsize(12, 8)

sns.set()


# In[4]:


athletes = pd.read_csv("athletes.csv")


# In[5]:


def get_sample(df, col_name, n=100, seed=42):
    """Get a sample from a column of a dataframe.
    
    It drops any numpy.nan entries before sampling. The sampling
    is performed without replacement.
    
    Example of numpydoc for those who haven't seen yet.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Source dataframe.
    col_name : str
        Name of the column to be sampled.
    n : int
        Sample size. Default is 100.
    seed : int
        Random seed. Default is 42.
    
    Returns
    -------
    pandas.Series
        Sample of size n from dataframe's column.
    """
    np.random.seed(seed)
    
    random_idx = np.random.choice(df[col_name].dropna().index, size=n, replace=False)
    
    return df.loc[random_idx, col_name]


# ## Inicia sua análise a partir daqui

# In[ ]:





# In[6]:


# Sua análise começa aqui.
amostra_height = get_sample(athletes, 'height',3000)
alpha = 0.05
test, p_value = sct.jarque_bera(amostra_height)
print(p_value)
if p_value > alpha:
    print('TRUE')
else:
    print('FALSE')


# In[7]:


amostra_weight = get_sample(athletes, 'weight',3000)
alpha = .05
log_amostra_weight = np.log(amostra_weight)
test, p_value = sct.normaltest(log_amostra_weight)
print(p_value)
if p_value > alpha:
    print('TRUE')
else:
    print('FALSE')


# In[ ]:





# ## Questão 1
# 
# Considerando uma amostra de tamanho 3000 da coluna `height` obtida com a função `get_sample()`, execute o teste de normalidade de Shapiro-Wilk com a função `scipy.stats.shapiro()`. Podemos afirmar que as alturas são normalmente distribuídas com base nesse teste (ao nível de significância de 5%)? Responda com um boolean (`True` ou `False`).

# In[8]:


def q1():
    amostra_height = get_sample(athletes, 'height',3000)
    alpha = .05
    test, p_value = sct.shapiro(amostra_height)
    return bool(p_value > alpha)


# In[9]:


q1()


# __Para refletir__:
# 
# * Plote o histograma dessa variável (com, por exemplo, `bins=25`). A forma do gráfico e o resultado do teste são condizentes? Por que?
# * Plote o qq-plot para essa variável e a analise.
# * Existe algum nível de significância razoável que nos dê outro resultado no teste? (Não faça isso na prática. Isso é chamado _p-value hacking_, e não é legal).

# ## Questão 2
# 
# Repita o mesmo procedimento acima, mas agora utilizando o teste de normalidade de Jarque-Bera através da função `scipy.stats.jarque_bera()`. Agora podemos afirmar que as alturas são normalmente distribuídas (ao nível de significância de 5%)? Responda com um boolean (`True` ou `False`).

# In[10]:


def q2():
    amostra_height = get_sample(athletes, 'height',3000)
    alpha = .05
    test, p_value = sct.jarque_bera(amostra_height)
    return bool(p_value > alpha)


# In[11]:


q2()


# __Para refletir__:
# 
# * Esse resultado faz sentido?

# ## Questão 3
# 
# Considerando agora uma amostra de tamanho 3000 da coluna `weight` obtida com a função `get_sample()`. Faça o teste de normalidade de D'Agostino-Pearson utilizando a função `scipy.stats.normaltest()`. Podemos afirmar que os pesos vêm de uma distribuição normal ao nível de significância de 5%? Responda com um boolean (`True` ou `False`).

# In[12]:


def q3():
    amostra_height = get_sample(athletes, 'height',3000)
    alpha = .05
    test, p_value = sct.normaltest(amostra_height)
    return bool(p_value > alpha)


# In[13]:


q3()


# __Para refletir__:
# 
# * Plote o histograma dessa variável (com, por exemplo, `bins=25`). A forma do gráfico e o resultado do teste são condizentes? Por que?
# * Um _box plot_ também poderia ajudar a entender a resposta.

# ## Questão 4
# 
# Realize uma transformação logarítmica em na amostra de `weight` da questão 3 e repita o mesmo procedimento. Podemos afirmar a normalidade da variável transformada ao nível de significância de 5%? Responda com um boolean (`True` ou `False`).

# In[14]:


def q4():
    amostra_weight = get_sample(athletes, 'weight',3000)
    alpha = .05
    log_amostra_weight = np.log(amostra_weight)
    test, p_value = sct.normaltest(log_amostra_weight)
    return bool(p_value > alpha)


# In[15]:


q4()


# __Para refletir__:
# 
# * Plote o histograma dessa variável (com, por exemplo, `bins=25`). A forma do gráfico e o resultado do teste são condizentes? Por que?
# * Você esperava um resultado diferente agora?

# > __Para as questão 5 6 e 7 a seguir considere todos testes efetuados ao nível de significância de 5%__.

# ## Questão 5
# 
# Obtenha todos atletas brasileiros, norte-americanos e canadenses em `DataFrame`s chamados `bra`, `usa` e `can`,respectivamente. Realize um teste de hipóteses para comparação das médias das alturas (`height`) para amostras independentes e variâncias diferentes com a função `scipy.stats.ttest_ind()` entre `bra` e `usa`. Podemos afirmar que as médias são estatisticamente iguais? Responda com um boolean (`True` ou `False`).

# In[16]:


athletes_bra = athletes[['nationality', 'height']].loc[athletes['nationality'] == 'BRA']
athletes_usa = athletes[['nationality', 'height']].loc[athletes['nationality'] == 'USA']
athletes_can = athletes[['nationality', 'height']].loc[athletes['nationality'] == 'CAN']
print(athletes_bra.shape[0])
print(athletes_usa.shape[0])
print(athletes_can.shape[0])
print(athletes.shape[0])


# In[24]:


def q5():
    alpha = .05
    test, p_value = sct.ttest_ind(athletes_bra['height'], athletes_usa['height'], equal_var = False, nan_policy='omit')
    return bool(p_value > alpha)


# In[25]:


q5()


# ## Questão 6
# 
# Repita o procedimento da questão 5, mas agora entre as alturas de `bra` e `can`. Podemos afimar agora que as médias são estatisticamente iguais? Reponda com um boolean (`True` ou `False`).

# In[26]:


def q6():
    alpha = .05
    test, p_value = sct.ttest_ind(athletes_bra['height'], athletes_can['height'], equal_var = False, nan_policy='omit')
    return bool(p_value > alpha)


# In[27]:


q6()


# ## Questão 7
# 
# Repita o procedimento da questão 6, mas agora entre as alturas de `usa` e `can`. Qual o valor do p-valor retornado? Responda como um único escalar arredondado para oito casas decimais.

# In[32]:


def q7():
    alpha = .05
    test, p_value = sct.ttest_ind(athletes_usa['height'], athletes_can['height'], equal_var = False, nan_policy='omit')
    return float(np.around(p_value,8))


# In[33]:


q7()


# __Para refletir__:
# 
# * O resultado faz sentido?
# * Você consegue interpretar esse p-valor?
# * Você consegue chegar a esse valor de p-valor a partir da variável de estatística?
