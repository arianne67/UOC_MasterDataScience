# uoc_mstDataSci_tcv_pra1
Tipologia i cicle de vida de les dades - Pràctica 1

L'objectiu d'aquesta pràctica és cobrir les fases de captura i emmagatzematge del cicle de vida de les dades.
A tal efecte, s'ha pensat en el següent cas:

1. Recollir mitjançant tècniques de Web Scraping les notícies de portada de diversos diaris generalistes amb una certa rellevància (descartem regionals o monotemàtics).
2. Les dades es guardaran en un sol arxiu en format CSV.
3. Preparació de dades per la seva anàlisi.
4. Emprar tècniques de business analytics per tal d'elaborar un estudi que permeti:
   - Trobar notíces comunes entre publicacions amb un nivell raonable de similitud mitjançant anàlisi de texts.
   - Un cop trobades, fer un "sentiment analysis" per establir el context positiu/negatiu de la notícia.
   - A continuació es compararan les diferents publicacions per obtenir un rànquing de "neutralitat" en quant al tractament de les notícies.
5. En fases posteriors, es podrien utilitzar dades de població, enquestes del CIS, etc. que permetin classificar les publicacions anteriormentes esmentades segons una certa tendència política, intentar segmentar els lectors, etc.

Creiem que el resultat que aportaria aquesta pràctica seria molt interessant per mesurar la neutralitat dels mitjans de comunicació.

S'han utilitzat les següents eines de suport:
- Extension Google Chrome SelectorGadget
- Extension Google Chrome WebScraper
- Extension Google Chrome WebDeveloper
- Client Github Desktop
- Anaconda + Jupyter Notebook

Tots els fonts inclosos estan programats en Python (Jupyter Notebook), però voldria incloure scripts en R i fer ús de tècniques com SPARQL per recollir dades RDF.

- WebScraping_News.py: script principal. Recopila les notícies des de fonts HTML i les guarda al dataset corresponent.
- WebScraping_IDESCAT.py: script auxiliar que recull indicadors de l'IDESCAT en format XML per possibles anàlisis posteriors.
- WebScraping_GENCAT-Socrata.py: script auxiliar que recull indicadors de GENCAT en format JSON utilitzant l'API Socrata.
- classes/WebScraping_class.py: classe per realitzar Web Scraping.
- datasets/NEWS_YYYYMMDD_HHMMSS.CSV: fitxer CSV que conté la recopilació de notícies.
- datasets/IDESCAT_EMEX_XML_080193.csv: fitxer CSV que conté indicadors d'IDESCAT