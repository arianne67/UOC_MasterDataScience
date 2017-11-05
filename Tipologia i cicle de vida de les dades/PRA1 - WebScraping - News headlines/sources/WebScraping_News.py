
# coding: utf-8

# In[1]:


from classes.WebScraping_class import WebScraping_HTML_XML
#import csv
import pandas as pd

from textblob import TextBlob, Word, Blobber
#from textblob.classifiers import NaiveBayesClassifier
#from textblob.taggers import NLTKTagger
#import nltk

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from googletrans import Translator

#import indicoio
#indicoio.config.api_key = "7a4879025797243e81860392cdc7e4ff"

#=======================================================
#Classe per realitzar WebScraping per formats JSON i CSV
#=======================================================
class Newspaper:

    #Constructor
    def __init__(self, id, nom, url, lng, pag=""):
        self.__id = id
        self.__nom=nom
        self.__url=url
        self.__lng=lng
        self.__pag=pag
        if url>"": self.__oWP = WebScraping_HTML_XML(url+pag,"html.parser",True)
        self.__articles = []

    #Set/GET atribut id  
    def set_nom(self,id):
        self.__id = id
    def get_nom(self):
        return self.__id
    #Set/GET atribut url  
    def set_url(self,url):
        self.__url=url
    def get_url(self):
        return self.__url
    #Set/GET atribut lng  
    def set_lng(self,lng):
        self.__lng=lng
    def get_lng(self):
        return self.__lng
   
    #Set/GET atribut parser  
    def set_oWP(self):
        self.__oWP = WebScraping_HTML_XML(self.__url+self.__pag,"html.parser",True)
    def get_parser(self):
        return self.__oWP
    
    #Mètode per obrir i llegir el recurs URL
    #tag_art: etiqueta HTML on es troba l'article (habitualment <article>)
    #tag_flt: atribut de "tag_art" on es fa el filtre
    #str_atr: text per filtrar l'atribut "tag_flt"
    #tag_cont: etiqueta HTML on hi ha text+link de l'article 
    #str_cont: text per filtrar l'etiqueta "tag_cont" 
    #tag_sum: etiqueta HTML on -opcionalment- podem trobar sumari/epígraf d'article
    #
    def get_articles(self, tag_art, tag_flt, str_flt, tag_cont, str_cont, tag_sum=""):
        oArt = self.__oWP.getWebdata(tag_art,"all",str_flt,tag_flt)
        oTrans = Translator()
        for elem in oArt:
            try:
                if tag_cont>"":
                    n_tit_t = elem.find(tag_cont).a.get_text().strip('\r\n\t ')
                    n_tit_l = elem.find(tag_cont).a.get("href").strip()
                else:
                    if tag_art=="a":
                        n_tit_t = elem.get_text().strip('\r\n\t ')
                        n_tit_l = elem.get("href").strip()
                    else:
                        n_tit_t = elem.a.get_text().strip('\r\n\t ')
                        n_tit_l = elem.a.get("href").strip()
                if "http" not in n_tit_l: n_tit_l=self.__url+n_tit_l
                n_sum = ""
                if tag_sum>"" and elem.find(tag_sum): 
                    n_sum = elem.find(tag_sum).get_text().strip('\r\n\t ')
                #n_rel = ""
            except:
                n_tit_l = ""
                n_tit_t = ""
                n_sum = ""
                #n_rel = ""

            if (n_tit_l>"" and n_tit_t>""):
                tit_t_en = oTrans.translate(n_tit_t, src=self.__lng, dest='en').text
                self.__articles.append([self.__id,n_tit_t,n_tit_l,n_sum,tit_t_en])
        return self.__articles


#Obtenir dia i hora en format YYYYMMDD_HHMMSS
def getToday():
    from datetime import datetime
    return datetime.now().strftime('%Y%m%d_%H%M%S')

news = ["EP", "LV", "20M", "PA", "EM", "LR", "ABC", "ARA", "PAV"]
caps = ["news_id","news_title","news_link","news_subtit","news_title_en", \
    "polarity","subjectivity","EP","LV","20M","PA","EM","LR","ABC","ARA","PAV"]

lstCSV = []

oEP = Newspaper("EP","EL PERIÓDICO","http://www.elperiodico.com/es/","es")
lst = oEP.get_articles("article", "", "", "h2", "", "p")
print("EL PERIÓDICO", len(lst))
lstCSV = lstCSV + lst

oLV = Newspaper("LV","LA VANGUARDIA","http://www.lavanguardia.com/","es")
lst = oLV.get_articles("article", "", "", "h1", "", "")
print("LA VANGUARDIA:", len(lst))
lstCSV = lstCSV + lst

o20m = Newspaper("20M","20 MINUTOS","http://www.20minutos.es/","es")
lst = o20m.get_articles("h2", "", "", "", "", "")
print("20 MINUTOS:", len(lst))
lstCSV = lstCSV + lst

oPA = Newspaper("PA","EL PAÍS","https://elpais.com/","es")
lst = oPA.get_articles("article", "", "", "h2", "","p")
print("EL PAÍS:", len(lst))
lstCSV = lstCSV + lst

oEM = Newspaper("EM","EL MUNDO","http://www.elmundo.es/","es")
lst = oEM.get_articles("article", "", "", "h3", "", "p")
print("EL MUNDO:", len(lst))
lstCSV = lstCSV + lst

oLR = Newspaper("LR","LA RAZÓN","http://www.larazon.es/","es")
lst = oLR.get_articles("article", "", "", "h2", "", "p")
print("LA RAZÓN:", len(lst))
lstCSV = lstCSV + lst

oABC = Newspaper("ABC","ABC","http://www.abc.es/","es")
lst = oABC.get_articles("article", "", "", "h1", "", "p")
print("ABC:", len(lst))
lstCSV = lstCSV + lst

oARA = Newspaper("ARA","ARA.CAT","https://www.ara.cat/","ca")
lst = oARA.get_articles("h2", "", "", "", "", "p")
print("ARA.CAT:", len(lst))
lstCSV = lstCSV + lst

oPAV = Newspaper("PAV","PUNT AVUI","http://www.elpuntavui.cat/barcelona.html","ca")
lst = oPAV.get_articles("div", "class", "article", "", "", "p")
print("PUNT AVUI:", len(lst))
lstCSV = lstCSV + lst

print("Sentiment & Similitud")
#lstCSV = lstCSV[0:50]

for r1 in lstCSV:
    r1.extend(["-","-",[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]])
    try:
        #b = (TextBlob(r1[1])).translate(to="en")
        #r1[5] = b.title()
        b = TextBlob(r1[4])
        r1[5] = round(b.sentiment.polarity,4)
        r1[6] = round(b.sentiment.subjectivity,4)
    except:
        r1[5] = "-"
    for r2 in [r for r in lstCSV if r[0]!=r1[0]]:
        ratio = fuzz.token_set_ratio(r1[4],r2[4])
        if ratio>60:
            r1[7+news.index(r2[0])][0] = r1[7+news.index(r2[0])][0]+1
            r1[7+news.index(r2[0])][1] = r1[7+news.index(r2[0])][1]+ratio
    for i in range(0,7):
       if r1[7+i][0]>0: r1[7+i][2] = round(r1[7+i][1]/r1[7+i][0])

df = pd.DataFrame(lstCSV,columns=caps)
df.to_csv("datasets/NEWS_"+getToday()+".csv",";","index=False")


