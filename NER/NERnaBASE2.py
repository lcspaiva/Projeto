import pt_core_news_sm
import operator

dictEQ = {} #entidade -> quantidade
dictEL = {} #entidade -> label

parser = pt_core_news_sm.load()
with open("baseUnica.txt", "r", encoding="utf-8") as docs:
    for linha in docs:
        trx = linha.rstrip()
        parsedEx = parser(trx)
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

import operator
lista = sorted(dictEQ.items(), key=operator.itemgetter(1), reverse=True)
print("-------------- entidades ---------------")

for ele in lista:
    print(dictEL[ele[0]],ele[0],str(ele[1]))

with open("SaidaNER.txt","w",encoding="utf-8") as saida:
    for ele in lista:
        saida.write(dictEL[ele[0]]+", ")
        saida.write(ele[0]+", ")
        saida.write(str(ele[1])+"\n")

