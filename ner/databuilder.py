import opencorpora
from russian_tagsets import converters


if __name__ == '__main__':
    corpus = opencorpora.CorpusReader("annot.opcorpora.no_ambig.xml")
    i=1
    mark=0
    f = open("corpus2", "w+", encoding="utf-16")
    for i in corpus.iter_documents():
        l=list()
        k=list()
        for q in i.iter_parsed_sents():
            l=list()
            for t in q:
                k=list()
                if ("Name" in t[1][0][1])or ("Surn" in t[1][0][1]) or ("Patr" in t[1][0][1]):
                    if(mark==1):
                        k.append(t[0])
                        k.append(t[1][0][1].split(',')[0])
                        k.append("I-Per")
                    else:
                        k.append(t[0])
                        k.append(t[1][0][1].split(',')[0])
                        k.append("B-Per")
                        mark=1
                elif ("Geox" in t[1][0][1]):
                    if(mark==2):
                        k.append(t[0])
                        k.append(t[1][0][1].split(',')[0])
                        k.append("I-Loc")
                    else:
                        k.append(t[0])
                        k.append(t[1][0][1].split(',')[0])
                        k.append("B-Loc")
                        mark=2
                elif ("Orgn" in t[1][0][1]):
                    if(mark==3):
                        k.append(t[0])
                        k.append(t[1][0][1].split(',')[0])
                        k.append("I-Org")
                    else:
                        k.append(t[0])
                        k.append(t[1][0][1].split(',')[0])
                        k.append("B-Org")
                        mark=3
                elif ("UNKN" in t[1][0][1]):
                    if(mark==1):
                        k.append(t[0])
                        k.append(t[1][0][1].split(',')[0])
                        k.append("I-Per")
                    elif(mark==2):
                        k.append(t[0])
                        k.append(t[1][0][1].split(',')[0])
                        k.append("I-Loc")
                    elif(mark==3):
                        k.append(t[0])
                        k.append(t[1][0][1].split(',')[0])
                        k.append("I-Org")
                    else:
                        k.append(t[0])
                        k.append(t[1][0][1].split(',')[0])
                        k.append("O")
                        mark=0
                else:
                    k.append(t[0])
                    k.append(t[1][0][1].split(',')[0])
                    k.append("O")
                    mark = 0
                l.append(k)
            f.write(str(l)+'\n')
            print(str(l))
