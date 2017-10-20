
# coding: utf-8

# In[14]:


from classes.WebScraping_class import WebScraping_HTML_XML
import csv
import pandas as pd

#Obtenir dia i hora en format YYYYMMDD_HHMMSS
def getToday():
    from datetime import datetime
    return datetime.now().strftime('%Y%m%d_%H%M%S')

#
# Recull dades d'indicadors de tota mena des de l'IDESCAT
# Mètode: API
#
def IDESCAT_EMEX_XML (mun_id, csv_type):
    
    #Objecte principal a la pàgina pel municipi especificat (mun_id)    
    oIDESCAT = WebScraping_HTML_XML("https://api.idescat.cat/emex/v1/dades.xml?id="+mun_id,"xml",True)
    #oIDESCAT.saveWebdoc("datasets/test.xml")

    if csv_type=="1":
        #Creació fitxer per guardar el dataset (opció-1)
        caps = ['com_id','com_desc','mun_id','mun_desc','g_id','g_desc','t_id','t_desc','t_link','t_r','f_id','f_desc','f_val','f_u']
        csvFile = open("datasets/IDESCAT_EMEX_XML_"+mun_id+".csv", "wt", newline="", encoding="iso-8859-1")
        csvWriter = csv.writer(csvFile, delimiter=";", quoting=csv.QUOTE_ALL)
        csvWriter.writerow(caps)
        lst = []
    else:
        if csv_type=="2":
            #Inicialització llista per guardar el dataset (opció-2)
            caps = ['com_id','com_desc','mun_id','mun_desc','g_id','g_desc','t_id','t_desc','t_link','t_r','f_id','f_desc','f_val','f_u']
            lst = []

    oCaps = oIDESCAT.getWebdata("col","all","","")
    for elem in oCaps:
        if elem.get("scheme")=="mun": mun_desc=elem.get_text()
        if elem.get("scheme")=="com": 
            com_id=elem.get("id")
            com_desc=elem.get_text()
    
    #Extracte nivell g (grups d'indicadors)+descendents
    oMun_g = oIDESCAT.getWebdata("g","all","","")

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
                    #Guarda registre en llista
                    if csv_type=="1" or csv_type=="2":
                        lst.append([com_id,com_desc,mun_id,mun_desc,g_id,g_desc,t_id,t_desc,t_link,t_r,f_id,f_desc,f_val,f_un])
                    else:
                        #Sense opció CSV --> mostrar per pantalla
                        print(com_id,com_desc,mun_id,mun_desc,g_id,g_desc,t_id,t_desc,t_link,t_r,f_id,f_desc,f_val,f_un)
                del oMun_f
            del oMun_t
        del oMun_g
    del oIDESCAT
    
    #Retorna DataFrame Pandas per CSV opció-2
    if csv_type=="1": 
        csvWriter.writerows(lst)
        csvFile.close()
    else:
        if csv_type=="2":
            df = pd.DataFrame(lst,columns=caps)
            df.to_csv("datasets/IDESCAT_EMEX_XML_"+mun_id+"_pandas.csv",";","index:False")
   

sMunicipi = input("Municipi: ")
sCSV = input("(1) CSV Estàndar / (2) Pandas : ")

if (sMunicipi>"" and len(sMunicipi)==6):
    df=IDESCAT_EMEX_XML(sMunicipi,sCSV)

    

#080193

#=======================================================
#Generació de dades per tots els municipis (recorregut)
#Acaba per timeout, segurament per limitacions de l'API
#=======================================================
#
##01. Recollim llista de comarques/municipis
#oCom_Mun = WebScraping_HTML_XML("https://api.idescat.cat/emex/v1/nodes.xml?tipus=com,mun","xml",True)
#oCom = oCom_Mun.getWebdata("v","all","com","scheme")
#
##02. Recorregut per Comarca
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

