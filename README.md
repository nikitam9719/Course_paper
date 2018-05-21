# diplom

Нужно скачать: дамп dbPedia https://drive.google.com/file/d/18OaFbzUT0kjVRTcgS8Dp9SY7t_nzUPao/view?usp=sharing и закинуть его в dbpediaparser
дамп opencorpora https://drive.google.com/file/d/1gq_EqHCSj_ZW-mA55RWCmbCFkDJFqvBh/view?usp=sharing в ner
поставить dbpediaEnquirerPy на место папки с тем же именем.
Две папки dbpediaparser и ner.
В dbpediaparser есть parser.py, она создаёт из дампа dbpedia файл csv, вида: имя сущности/тип сущности
В ner:
Databuilder-строит из дампа опенкорпоры данные. Предложение-список троек [слово, часть речи, тип сущности в опенкорпоре]
Alg, alg+dic, alg+wiki+checker-собственно чистые алгоритмы, алгоритм со словарём и со словарём+чекером
