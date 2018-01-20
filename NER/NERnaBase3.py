import pt_core_news_sm
import operator
from nltk.tokenize import sent_tokenize

dictEQ = {} #entidade -> quantidade
dictEL = {} #entidade -> label
i = 1
link = ""
titulo = ""
data = ""
noticia = ""
parser = pt_core_news_sm.load()
with open("baseUnica.txt", "r", encoding="utf-8") as docs:
    for linha in docs:
        trx = linha.rstrip()

        if (i == 1):
            link = trx
        elif (i == 2):
            titulo = trx
        elif (i == 3):
            data = trx
        elif (trx == "YippieKiYay"):
            i = 0
            lista_tknzd = sent_tokenize(titulo)
            lista_tknzd += sent_tokenize(noticia)
            #print(lista_tknzd)
            noticia = ""
            for sents in lista_tknzd:
                parsedEx = parser(sents)
                ents = list(parsedEx.ents)

                for entity in ents:
                    aux = (entity.label_, ' '.join(t.orth_ for t in entity))
                    entidade = aux[1]
                    label = aux[0]

                    if dictEQ.get(entidade, 0) == 0:
                        dictEQ[entidade] = 1  # entidade nao estava no dict, adiciona ela
                        dictEL[entidade] = label
                    else:
                        dictEQ[entidade] += 1
        else:
            #baseDados.readline().replace("\n","")
            #noticia += baseDados.readline()
            noticia += trx
        i+=1


import operator
lista = sorted(dictEQ.items(), key=operator.itemgetter(1), reverse=True)

for ele in lista:
    if len(ele[0])== 1:
        lista.remove(ele)

'''
for ele in lista:
    print(ele)
    #print(dictEL[ele[0]],ele[0],str(ele[1]))
'''
with open("SaidaNER.txt","w",encoding="utf-8") as saida:
    for ele in lista:
        saida.write(dictEL[ele[0]]+", ")
        saida.write(ele[0]+", ")
        saida.write(str(ele[1])+"\n")

