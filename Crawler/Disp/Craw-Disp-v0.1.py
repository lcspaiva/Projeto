import os
import re
import requests
import bs4
import time
from urllib.parse import urljoin

dict = {} #dicionario com os links
pasta = "Coleta" #nome da pasta que contera o resultado da coleta, estara no mesmo diretorio do script

#inicializando o dicionario pelo oq temos no arqv dicionario
with open('visitados.txt', 'r') as arqv_visitados:
    for links in arqv_visitados:
        dict[links.rstrip()] = 1 #cada linha eh uma entrada no dict, cada linha sera unica

os.rename("links.txt","b.txt") #aux sera o arquivo q sera processado, e links.txt sera recriado com as noticias unicas
with open("links.txt","w")as arqv:#criando o que sera o arquivo limpo com os links ainda nao visitados
    pass

with open("b.txt","r") as arqv_links:
    for links in arqv_links:
        aux=links.rstrip()#lendo um link do arquivo (linha)
        if(dict.get(aux,0))==0:#o link nao esta no dict, logo ele nao foi visitado
            if(aux==''):
                continue
            else:
                with open("links.txt","a") as arqv:
                    arqv.write(aux+'\n')

#links.txt tera ao final os links que estao no dict, ou seja, ainda nao foram visitados
#b.txt tera o final os links antes de serem comparados com o dict, tera uma copia contendo os links nao visitados ...
# ... e os que ja foram visitados(dict)
os.remove("b.txt")

#entrada dos parametros do site que sera crawleado
nome_site = ""
START_URL = ""
ER = "" #expressao regular para delimitar o dominio do link, delimita a busca somente ao site desejdo
qntd_param = 1 #define a quantidade de paramatros para extrair nas noticias TRIGGER1
#TRIGGER2 define se o crawler percorrera o site por paginas ((DEAD, pq esse progm soh tirara de feed
data_html = "S" #define se precisaremos pegar a data atraves do html, caso sim especificar o nome do campo,
                # caso nao a data esta no proprio link da noticia. TRIGGER3
rel_link = "S" #define se o site utiliza link relativo TRIGGER4

#compilando a expressao regular
er = re.compile(ER)

#setando os parametros, para retirada da noticia (corpo)
if qntd_param == 1:
    param1 = ""
else:
    if qntd_param == 2:
        param1 = ""
        param2 = ""

#especifica se iremos extrair a data do html, caso sim, especifica o nome do campo em questao
if(data_html == "S"):
        param_data = ""

if not os.path.exists(pasta):
    os.mkdir(pasta)

print(nome_site)

#funcao para criar o link, caso a pagina utilize link relativo
#entrada: o link que desejamos testar
#saida: link completo
def is_relativo(link):#se o trigger tiver ativo, retornamos link relativo senao o link retorna da forma que veio
    if rel_link == "S":
        return urljoin(START_URL, link)
    else:
        return link

#dado o PORTAL (pag principal) retorna as classes que contem os links
#Returns an iterator with the a tags with the titles
def get_portal_links(url):
    html = requests.get(url).content
    soup = bs4.BeautifulSoup(html,"html.parser")
    return soup.findAll('a',href=True) #axa todos os campos com links

#dada uma lista com as classes, extrai as informacoes(links)
def extrai_dados(obj):
    return obj.attrs['href']

def extrai_data (sopa):
    for item in sopa.findAll("p", param_data):  # encontra a classe onde esta a data
        data = item.get_text()  # extrai o conteudo da classe, a data em si
        return data

def processa_links():
    pass
