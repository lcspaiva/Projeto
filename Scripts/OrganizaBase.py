

link = ""
titulo = ""
data = ""
i = 1
noticia = ""
with open("doc1.txt", "r") as baseDados:
    for linha in baseDados:
        aux = linha.rstrip()
        #print(aux)
        if (i == 1):
            link = aux
        elif (i == 2):
            titulo = aux
        elif (i == 3):
            data = aux
        elif(aux == "YippieKiYay"):
            i=0
            print(link)
            print(titulo)
            print(data)
            print(noticia)
            print("**************************************************")
            print("**************************************************")
            noticia = ""
        else:
            #baseDados.readline().replace("\n","")
            #noticia += baseDados.readline()
            noticia += aux
        i+=1

