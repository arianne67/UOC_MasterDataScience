Tots els fonts inclosos estan programats en Python (Jupyter Notebook), però voldria incloure scripts en R i fer ús de tècniques com SPARQL per recollir dades RDF.

- WebScraping_News.py: script principal. Recopila les notícies des de fonts HTML i les guarda al dataset corresponent.
- WebScraping_IDESCAT.py: script auxiliar que recull indicadors de l'IDESCAT en format XML per possibles anàlisis posteriors.
- WebScraping_GENCAT-Socrata.py: script auxiliar que recull indicadors de GENCAT en format JSON utilitzant l'API Socrata.
- classes/WebScraping_class.py: classe per realitzar Web Scraping.
- datasets/NEWS_YYYYMMDD_HHMMSS.CSV: fitxer CSV que conté la recopilació de notícies.
- datasets/IDESCAT_EMEX_XML_080193.csv: fitxer CSV que conté indicadors d'IDESCAT
