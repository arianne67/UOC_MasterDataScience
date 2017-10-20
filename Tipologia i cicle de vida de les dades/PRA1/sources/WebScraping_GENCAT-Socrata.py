
# coding: utf-8

# In[1]:


import csv
from classes.WebScraping_class import WebScraping_JSON_CSV

#Exemple recuperació dades JSON amb Pandas
#Portal transparència Generalitat, funciona amb l'API Socrata
oJSON = WebScraping_JSON_CSV("https://analisi.transparenciacatalunya.cat/resource/u5vr-ww79.json","json")
oJSON.df.head(5)

