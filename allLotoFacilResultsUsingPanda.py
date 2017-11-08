
# coding: utf-8

# In[2]:

# Import dos módulos
from urllib.request import urlretrieve
import pandas as pd
import zipfile
import os


# In[5]:

# Baixando zip
# url = "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_lotfac.zip"
# urlretrieve(url, "D_lotfac_2.zip")
comando = "wget -N 'http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_lotfac.zip'"
os.system(comando)

# In[6]:

# Extraindo o zip
zFile = zipfile.ZipFile("D_lotfac.zip")
htmlFile = zFile.open(zFile.infolist()[0]).name


# In[7]:

htmlFile


# In[8]:

# Carregando o arquivo html
dfHtml = pd.read_html(htmlFile, header=0)[0]


# In[9]:

dfHtml.head()


# In[10]:

# Subset até a coluna "Bola15"
dfHtml = dfHtml.loc[0:, :"Bola15"]


# In[11]:

dfHtml.head()


# In[12]:

# Apagando linhas "NaN" do dataset
dfHtml = dfHtml.dropna(subset=["Bola1"])


# In[14]:

dfHtml


# In[15]:

# Definindo o index como "Concurso"
dfHtml = dfHtml.set_index("Concurso")


# In[17]:

# Exibindo os primeiro registros
dfHtml


# In[18]:

# Transformando dataset em um arquivo .csv
dfHtml.to_csv("Resultatdos.csv", header=False)

