
El nostre dataset s'anomena **NEWS_YYYYMMDD_HHMMSS.CSV**, i conté una llista de notícies extretes de les webs de diferents periòdics generalistes mitjançant tècniques de WebScraping.

Característiques:
- Fitxer pla CSV amb camps separats per punt i coma (;)
- Codificació UTF-8

Estructura de NEWS_YYYYMMDD_HHMMSS.CSV:
- **id**: identificador del diari
- **news_id**: identificador del diari
- **news_title**: titular notícia
- **news_link**: enllaç a la pàgina web de la notícia
- **news_subtit**: subtitular (o epígraf) de la notícia (opcional).
- **news_title_en**: traducció de la notícia a l'anglés-
- **polarity**: índex de polaritat (índex negatiu/positiu) de la notícia.
- **subjectivity**: index de subjectiviat de la notícia.
- A continuació hi haurà **N columnes** (una per cada diari inclós al fitxer base DIARIS.CSV).
    - Nombre de notícies amb un índex de similitud superior a 60 amb la notícia tractada.
    - Ratio de similitud total de la notícia pel diari tractat.


