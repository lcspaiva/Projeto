from operator import itemgetter
#tira as noticias do arquivo de modo ordenado, em blocos (noticias individuais)

import datetime
def date_key(a):
    a = datetime.datetime.strptime(a, '%d/%m/%Y\n').date()
    return a

link = ""
titulo = ""
data = ""
i = 1
noticia = ""
tam = 0
datas = []
aux = ()
with open("teste.txt", "r") as baseDados:
    for linha in baseDados:
        #print(len(linha))
        #print("linha:" + linha)
        if(i == 1):
            link = linha
        elif(i == 2):
            titulo = linha
        elif(i == 3):
            print(tam)
            data = linha
            x = str(date_key(data))
            aux = (x,tam)
        elif(linha == "YippieKiYay\n" or linha == "YippieKiYay"):
            datas.append(aux)
            i=0
            #print(tam) #em ql pos a not começa
            #print(linha)
            tam = tam + len(link)+len(titulo)+len(data)+len(noticia)+len(linha)
            #tam = 0
            noticia = ""
        else:
            noticia += linha
        i = i + 1
print(datas)
datas.sort(key=itemgetter(0))
#print(datas)

link = ""
titulo = ""
data = ""
i = 1
noticia = ""
with open("teste.txt","r") as docs:
    docs.seek(38)
    x = docs.read(38)
    print(x)
'''
    for linha in docs:
        #print(linha[:len(linha)-1])
        if (i == 1):
            link = linha
        elif (i == 2):
            titulo = linha
        elif (i == 3):
            data = linha
        elif (linha == "YippieKiYay\n" or linha == "YippieKiYay"):
            i = 0
            with open("saida.txt","w") as saida:
                saida.write(link)
                saida.write(titulo)
                saida.write(data)
                saida.write(noticia)
                saida.write(linha)
                break
        else:
            noticia += linha
        i = i + 1
'''
