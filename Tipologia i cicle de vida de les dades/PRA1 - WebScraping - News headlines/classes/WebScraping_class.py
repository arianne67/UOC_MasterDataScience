
# coding: utf-8

# In[1]:


from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import pandas as pd

#=======================================================
#Classe per realitzar WebScraping per formats JSON i CSV
#=======================================================
class WebScraping_JSON_CSV:

    #Constructor
    def __init__(self, url=None, parser=None):
        self.__url=url
        self.__parser=parser
        if parser=="json":
            self.df = pd.read_json(url)
        else:
            self.df = pd.read_csv(url)

#=======================================================
#Classe per realitzar WebScraping per formats HTML i XML
#=======================================================
class WebScraping_HTML_XML:
    
    #Constructor
    def __init__(self, url=None, parser="html.parser", openDoc=True):
        self.__url=url
        self.__parser=parser
        self.__contents = None
        self.df = None
        if openDoc:
            self.openWebdoc()
        
    #Set/GET atribut url  
    def set_url(self,url):
        self.__url=url
    def get_url(self):
        return self.__url
    #Set/GET atribut parser  
    def set_parser(self,parser):
        self.__parser=parser
    def get_parser(self):
        return self.__parser
    
    #Mètode per obrir i llegir el recurs URL
    def openWebdoc(self):
        try:
            if self.__url[:4]=="http":
                self.__contents = urlopen(self.__url).read()
            else:
                self.__contents = (self.__url)
        except HTTPError as e:
            return False
        return True

    #Mètode per descarregar el recurs
    def saveWebdoc (self,fic):
        if (len(self.__contents)>0):
            f = open(fic, "wt")
            #print(str(self.__contents))
            f.write(str(self.__contents))
            f.close
            return True
        else:
            return False

    #Mètode per obtenir dades
    #tag: etiqueta HTML/XML
    #scope: recuperar nivell actual("") o actual+descendents ("all")
    #str: filtre atribut
    #strTag: nom atribut
    def getWebdata(self,tag,scope,str,strTag,isRecursive=True):
        try:
            bsObj = BeautifulSoup(self.__contents, self.__parser)
            if scope=="all":
                if str>"":
                    div = bsObj.find_all(tag,{strTag:str},recursive=isRecursive)
                else:
                    div = bsObj.find_all(tag,recursive=isRecursive)
            else:
                if str>"":
                    div = bsObj.find(tag,{strTag:str})
                else:
                    div = bsObj.find(tag)
        except AttributeError as e:
            return None
        return div


