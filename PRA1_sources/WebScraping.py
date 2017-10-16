
# coding: utf-8

# In[182]:


from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import csv
import pandas as pd


#from sources.WebScraping_class import WebScraping

class WebScraping_JSON_CSV:

    #Constructor
    def __init__(self, url=None, parser=None):
        self.__url=url
        self.__parser=parser
        if parser=="json":
            self.df = pd.read_json(url)
        else:
            self.df = pd.read_csv(url)

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
    #string: filtre atribut
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

    
def IDESCAT_EMEX_XML (mun_id, wrt):
    
    #Objecte principal a la pàgina pel municipi especificat (mun_id)    
    oIDESCAT = WebScraping_HTML_XML("https://api.idescat.cat/emex/v1/dades.xml?id="+mun_id,"xml",True)
    #oIDESCAT.saveWebdoc("datasets/test.xml")

    oCaps = oIDESCAT.getWebdata("col","all","","")
    for elem in oCaps:
        if elem.get("scheme")=="mun": mun_desc=elem.get_text()
        if elem.get("scheme")=="com": 
            com_id=elem.get("id")
            com_desc=elem.get_text()
    
    #Extracte nivell g (grups d'indicadors)+descendents
    oMun_g = oIDESCAT.getWebdata("g","all","","")
    caps = ['com_id','com_desc','mun_id','mun_desc','g_id','g_desc','t_id','t_desc','t_link','t_r','f_id','f_desc','f_val','f_u']
    lst = []

    if oMun_g == None:
        print("MUNICIPI "+mun_id+" no trobat")
    else:
        #Extracte nivell g (grups d'indicadors)+descendents (taules "t")
        for elem_g in oMun_g:
            g_id = elem_g.get("id")
            g_desc = elem_g.c.get_text()
            oMun_t = (WebScraping_HTML_XML(str(elem_g),"xml",True)).getWebdata("t","all","","")
            #Extracte nivell t (taula indicadors del grup "g")+descendents (indicadors "f")
            for elem_t in oMun_t:
                #ID taula
                t_id = elem_t.get("id")
                #Descripció taula
                t_desc = elem_t.c.get_text()
                #Link pàgina web amb aquesta informació
                t_link = elem_t.l.get_text()
                #Temporalitat
                t_r = elem_t.r.get_text()
                oMun_f = (WebScraping_HTML_XML(str(elem_t),"xml",True)).getWebdata("f","all","","")
                #Extracte nivell f (indicador taula "t", grup "g")+descendents (atributs)
                for elem_f in oMun_f:
                    #ID indicador
                    f_id = elem_f.get("id")
                    #Descripció
                    f_desc = elem_f.c.get_text()
                    #valor(s)
                    f_val = elem_f.v.get_text()
                    #Unitats de mida (no està en tots els casos)
                    try:
                        f_un = elem_f.u.get_text()
                    except AttributeError as e:
                        f_un = ""
                    #Guarda registre
                    csvRow = []
                    csvRow.append(str(com_id))
                    csvRow.append(com_desc)
                    csvRow.append(mun_id)
                    csvRow.append(mun_desc)
                    csvRow.append(g_id)
                    csvRow.append(g_desc)
                    csvRow.append(t_id)
                    csvRow.append(t_desc)
                    csvRow.append(t_link)
                    csvRow.append(t_r)
                    csvRow.append(f_id)
                    csvRow.append(f_desc)
                    csvRow.append(f_val)
                    csvRow.append(f_un)
                    wrt.writerow(csvRow)
                    lst.append([com_id,com_desc,mun_id,mun_desc,g_id,g_desc,t_id,t_desc,t_link,t_r,f_id,f_desc,f_val,f_un])
                del oMun_f
            del oMun_t
        del oMun_g
    del oIDESCAT
    df = pd.DataFrame(lst,columns=caps)
    return df

#Creació fitxer per guardar el dataset
csvFile = open("datasets/IDESCAT_indicadorsMunicipi.csv", "wt", newline="", encoding="iso-8859-1")
writer = csv.writer(csvFile, delimiter=";", quoting=csv.QUOTE_ALL)
df=IDESCAT_EMEX_XML("080193",writer)
csvFile.close()
#Creació fitxer amb Pandas
df.to_csv("datasets/IDESCAT_EMEX_XML_080193_pandas.csv",";")

#Exemple recuperació dades JSON amb Pandas
oJSON = WebScraping_JSON_CSV("https://analisi.transparenciacatalunya.cat/resource/u5vr-ww79.json","json")
oJSON.df.head(5)

##Recollim llista de comarques/municipis
#oCom_Mun = WebScraping_HTML_XML("https://api.idescat.cat/emex/v1/nodes.xml?tipus=com,mun","xml",True)
#oCom = oCom_Mun.getWebdata("v","all","com","scheme")
##Recorregut per Comarca
#for oCom_elem in oCom:
#    com_id = oCom_elem.get("id")
#    com_desc = oCom_elem.contents[0]   
#    oMun = (WebScraping_HTML_XML(str(oCom_elem),"xml",True)).getWebdata("v","all","mun","scheme")
#    #Extracte Municipis per comarca "com_id"
#    for oMun_elem in oMun:
#        mun_id = oMun_elem.get("id")
#        mun_desc = oMun_elem.get_text()
#        #Extracte dades IDESCAT-EMEX
#        print(com_id,com_desc,mun_id,mun_desc)
#        IDESCAT_EMEX_XML(com_id,com_desc,mun_id,mun_desc,writer)
        



