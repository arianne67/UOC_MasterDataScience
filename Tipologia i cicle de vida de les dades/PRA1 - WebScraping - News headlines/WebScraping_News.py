
# coding: utf-8

from classes.WebScraping_class import WebScraping_HTML_XML
import pandas as pd

from textblob import TextBlob
from fuzzywuzzy import fuzz
from googletrans import Translator

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
    
    #--------------------------------------------------------------------------
    # Mètode per obrir i llegir el recurs URL
    #--------------------------------------------------------------------------
    # tag_art: etiqueta HTML on es troba l'article (habitualment <article>)
    # tag_flt: atribut de "tag_art" on es fa el filtre
    # str_atr: text per filtrar l'atribut "tag_flt"
    # tag_cont: etiqueta HTML on hi ha text+link de l'article 
    # str_cont: text per filtrar l'etiqueta "tag_cont" 
    # tag_sum: etiqueta on -opcionalment- podem trobar sumari/epígraf d'article
    #--------------------------------------------------------------------------
    # Retorn: llista contening els articles
    #--------------------------------------------------------------------------
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
            except:
                n_tit_l = ""
                n_tit_t = ""
                n_sum = ""                
            # Si les notícies no venen originalment en anglés, traduïr
            # Utilitzem la llibreria "googletrans"
            if (n_tit_l>"" and n_tit_t>"" and self.__lng!="en"):
                tit_t_en = oTrans.translate(n_tit_t, src=self.__lng, dest='en').text
                self.__articles.append([self.__id,n_tit_t,n_tit_l,n_sum,tit_t_en])
        return self.__articles


#Obtenir dia i hora en format YYYYMMDD_HHMMSS
def getToday():
    from datetime import datetime
    return datetime.now().strftime('%Y%m%d_%H%M%S')


caps = ["news_id","news_title","news_link","news_subtit","news_title_en", \
    "polarity","subjectivity"]
lstCSV = []

#
# Recuperem continguts de l'arxiu CSV "diaris.csv" que conté les dades base de l'estudi:
# - id: identificador del diari a tractar (ej: LV -> La Vanguardia)
# - nom: del diari
# - url: del diari digital
# - lng: idioma del diari
# - tag: etiqueta utilitzada per guardar els articles
# - tag_attr: atribut per filtrar article (opcional)
# - tag_attr_str: contingut atribut "tag_attr"
# - tag_cont: etiqueta on es guarda el texte de la notícia (opcional)
# - tag_cont_str: contingut atribut "tag_cont"
# - tag_sum: etiqueta on es guarda el sumari de la notícia (opcional)
# - n_lectors: nombre de lectors diaris (2016, AIMC)
#
df_diaris=pd.read_csv("diaris.csv",sep=";",header=0,na_values=0,keep_default_na=False)
news = df_diaris["id"].values.tolist()
caps.extend(news)

#
# Procés de WebScraping
# L'objecte "oDiari" emmagatzema les dades recuperades (HTML)
#
for d in df_diaris.values.tolist():
    oDiari = Newspaper(d[0],d[1],d[2],d[3])
    lst = oDiari.get_articles(d[4], d[5], d[6], d[7], d[8], d[9])
    print(d[1], len(lst))
    lstCSV = lstCSV + lst
    
print("Sentiment & Similitud")
#
# Recorregut de totes les notícies per associar indicadors:
# - Sentiment: ús de llibreria "TextBlob"
# - Similitud: ús de la llibreria "fuzzywuzzy"
#
for r1 in lstCSV:
    
    # Afegim columnes per guardar polaritat i subjectivitat
    r1.extend(["",""])
    
    # Afegim columnes per guardar similitud [i,j] on:
    # i = nombre de notícies al diari "n" amb un grau de similitud > 60%
    # j = ratio (%) de similitud de la notícia respecte al diari "n"
    for n in news:
        r1.extend([[0,0]])
    try:
        b = TextBlob(r1[4])
        r1[5] = round(b.sentiment.polarity,4)
        r1[6] = round(b.sentiment.subjectivity,4)
    except:
        r1[5] = "-"
        r1[6] = "-"
    for r2 in [r for r in lstCSV if r[0]!=r1[0]]:
        ratio = fuzz.token_set_ratio(r1[4],r2[4])
        if ratio>60:
            r1[7+news.index(r2[0])][0] = r1[7+news.index(r2[0])][0]+1
            r1[7+news.index(r2[0])][1] = r1[7+news.index(r2[0])][1]+ratio
    for i in range(0,7):
       if r1[7+i][0]>0: r1[7+i][1] = round(r1[7+i][1]/r1[7+i][0])

# Guardem la llista en una estructura DataFrame (llibreria "pandas")
df = pd.DataFrame(lstCSV,columns=caps)
# Guardem la llista en un fitxer CSV (dataset resultat)
df.to_csv("datasets/NEWS_"+getToday()+".csv",sep=";",index=False,decimal=",")

