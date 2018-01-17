import os

nome_pastas = []
#nome das pastas que contêm as noticias, como o layout é sempre o mesmo o caminho não muda, bastando termos em mãos o nome do site/pasta
#nome_pastas.append("Agencia PT")
nome_pastas.append("Blog da Maria Fro")

with open("baseUnica.txt","a",encoding="utf-8") as arquivoBaseUnica:
    for s in range(len(nome_pastas)):
        with open(nome_pastas[s]+"/Coleta/"+"nots_"+nome_pastas[s]+".txt","r",encoding='utf-8') as arquivoNoticias:
            for linhas in arquivoNoticias:
                arquivoBaseUnica.write(linhas.rstrip())
                arquivoBaseUnica.write("\n")

