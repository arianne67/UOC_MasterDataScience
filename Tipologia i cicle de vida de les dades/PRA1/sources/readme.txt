De moment, tots els fonts inclosos estan programats en Python, per� voldria incloure scripts en R i fer �s de t�cniques com SPARQL per recollir dades RDF.

/WebScraping_News.py: script principal. Recopila les not�cies des de fonts HTML i les guarda al dataset corresponent.
/WebScraping_IDESCAT.py: script auxiliar que recull indicadors de l'IDESCAT en format XML per possibles an�lisis posteriors.
/WebScraping_GENCAT-Socrata.py: script auxiliar que recull indicadors de GENCAT en format JSON utilitzant l'API Socrata.
classes/WebScraping_class.py: classe per realitzar Web Scraping.
/datasets/NEWS_YYYYMMDD_HHMMSS.CSV: fitxer CSV que cont� la recopilaci� de not�cies.
