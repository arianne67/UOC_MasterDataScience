
# coding: utf-8

# In[69]:


from classes.WebScraping_class import WebScraping_HTML_XML
import csv
import pandas as pd

#=======================================================
#Classe per realitzar WebScraping per formats JSON i CSV
#=======================================================
class Newspaper:

    #Constructor
    def __init__(self, id, nom, url, pag=""):
        self.__id = id
        self.__nom=nom
        self.__url=url
        self.__pag=pag
        if url>"": self.__oWP = WebScraping_HTML_XML(url+pag,"html.parser",True)
        self.__articles = []

    #Set/GET atribut id  
    def set_nom(self,id):
        self.__id = id
    def get_nom(self):
        return self.__id
    #Set/GET atribut url  
    def set_nom(self,url):
        self.__url=url
    def get_nom(self):
        return self.__url
    #Set/GET atribut url  
    def set_url(self,url):
        self.__url=url
    def get_url(self):
        return self.__url
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
        for elem in oArt:
            try:
                if tag_cont>"":
                    n_tit_t = elem.find(tag_cont).a.get_text()
                    n_tit_l = elem.find(tag_cont).a.get("href").strip()
                else:
                    if tag_art=="a":
                        n_tit_t = elem.get_text()
                        n_tit_l = elem.get("href").strip()
                    else:
                        n_tit_t = elem.a.get_text()
                        n_tit_l = elem.a.get("href").strip()
                if "http" not in n_tit_l: n_tit_l=self.__url+n_tit_l
                n_sum = ""
                if tag_sum>"" and elem.find(tag_sum): n_sum = elem.find(tag_sum).get_text().strip()
                n_rel = ""
            except:
                n_tit_l = ""
                n_tit_t = ""
                n_sum = ""
                n_rel = ""

            if (n_tit_l>"" and n_tit_t>""):
                self.__articles.append([self.__id,n_tit_t,n_tit_l,n_sum,n_rel])
        return self.__articles


#Obtenir dia i hora en format YYYYMMDD_HHMMSS
def getToday():
    from datetime import datetime
    return datetime.now().strftime('%Y%m%d_%H%M%S')


lstCSV = []

oEP = Newspaper("EP","EL PERIÓDICO","http://www.elperiodico.com/es/")
lst = oEP.get_articles("article", "", "", "h2", "", "p")
print("EL PERIÓDICO", len(lst))
lstCSV = lstCSV + lst

oLV = Newspaper("LV","LA VANGUARDIA","http://www.lavanguardia.com/")
lst = oLV.get_articles("article", "", "", "h1", "", "")
print("LA VANGUARDIA:", len(lst))
lstCSV = lstCSV + lst

o20m = Newspaper("20M","20 MINUTOS","http://www.20minutos.es/")
lst = o20m.get_articles("h2", "", "", "", "", "")
print("20 MINUTOS:", len(lst))
lstCSV = lstCSV + lst

oPA = Newspaper("PA","EL PAÍS","https://elpais.com/")
lst = oPA.get_articles("article", "", "", "h2", "","p")
print("EL PAÍS:", len(lst))
lstCSV = lstCSV + lst

oEM = Newspaper("EM","EL MUNDO","http://www.elmundo.es/")
lst = oEM.get_articles("article", "", "", "h3", "", "p")
print("EL MUNDO:", len(lst))
lstCSV = lstCSV + lst

oLR = Newspaper("LR","LA RAZÓN","http://www.larazon.es/")
lst = oLR.get_articles("article", "", "", "h2", "", "p")
print("LA RAZÓN:", len(lst))
lstCSV = lstCSV + lst

oABC = Newspaper("ABC","ABC","http://www.abc.es/")
lst = oABC.get_articles("article", "", "", "h1", "", "p")
print("ABC:", len(lst))
lstCSV = lstCSV + lst

df = pd.DataFrame(lstCSV,columns=["news_id","news_title","news_link","news_subtit","news_rel"])
df.to_csv("datasets/NEWS_"+getToday()+".csv",";","index:False")


