import os
import re
import requests
import bs4
import time
from urllib.parse import urljoin
pular = "N" #faz com que o programa vá direto ao processamento dos arquivos

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
nome_site = "EBC"
START_URL = "http://agenciabrasil.ebc.com.br/ultimas"
ER = "\A(http|https)://agenciabrasil\.ebc\.com\.br/politica/noticia/20(15|16|17).*" #expressao regular para delimitar o dominio do link, delimita a busca somente ao site desejdo
data_html = "S" #define se precisaremos pegar a data atraves do html, caso sim especificar o nome do campo,
                # caso nao a data esta no proprio link da noticia. TRIGGER3
rel_link = "S" #define se o site utiliza link relativo TRIGGER4
pag_ini = 0 #pagina inicial do loop
pag_fim = 5 #pagina final do loop

#compilando a expressao regular
er = re.compile(ER)

#setando os parametros, para retirada da noticia (corpo)


#define o link que sera construido para percorrer as paginas do site (ex: site1/ + pag2 = site1/pag2)
url_base = "http://agenciabrasil.ebc.com.br/ultimas"
url_pag = "?page="

''' todos irao extrair a data do html
#especifica se iremos extrair a data do html, caso sim, especifica o nome do campo em questao
if(data_html == "S"):
        param_data = "date"
'''
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
    return soup.findAll('a', href=True) #axa todos os campos com links

#dada uma lista com as classes, extrai as informacoes(links)
def extrai_dados(obj):
    return obj.attrs['href']

def extrai_data (sopa):
    data = "1"
    for item in sopa.findAll("li","date"):  # encontra a classe onde esta a data
        data = item.get_text()  # extrai o conteudo da classe, a data em si
    if (data is None):
        return "1"
    else:
        return data[:11]

#percorre o arquivo de links, processando-os, extraindo url, html, noticia, data. Em seguida adiciona os links
#presentes nessa pagina (derivadados) ao arquivo de links
def processa_links():
    dataOK = True #flag para a data
    with open('links.txt', 'r') as arqv_links:  #abrindo o arqv de links para processar um de cada vez
        for linha in arqv_links:
            link = linha.rstrip()
            time.sleep(0.50) #pausa para evitar congestionamento e kick pelo provedor
            html = requests.get(link).content  #acessando o link do arqv de links
            soup = bs4.BeautifulSoup(html, "html.parser")#criando o parser para percorrer o html

            data = extrai_data(soup)
            if (data == "1"):
                dataOK = False

            #Checa data
            if (dataOK is False and data_html == "S"): #data esta no html
                    if not (data.find("2017") != -1 or data.find("2016") != -1 or data.find("2015") != -1): #anos permitidos
                        dataOK = False  #noticia nao pode ser processada
                    else:
                        dataOK = True #noticia pode ser processada

            #Escreve HTML
            if (dataOK is True):
                with open(pasta + "/" + 'html_' + nome_site + '.txt', 'a') as arqv_html:  # escrevendo o html no arquivo
                    arqv_html.write(str(html))  # escrevendo CHECAR SE ESTA EXCREVENDO A STR OU EM BYTES !!
                    arqv_html.write("\nYippieKiYay\n")  #separador

            #extracao e escrita dos campos da noticia
            if (dataOK is True):
                noticia = "" #conterá os blocos da noticia
                with open(pasta + "/" + 'nots_' + nome_site + '.txt', 'a', encoding='utf-8') as arqv_nots:
                    arqv_nots.write(link + '\n')  #link da noticia
                    titulo = soup.title.string #titulo da noticia
                    arqv_nots.write(titulo[:len(titulo)-57:]+'\n')   #limpando o titulo
                    arqv_nots.write(data + '\n') #data da noticia
                #conteudo da pagina, a noticia, e a quantidade de parametros pra extrair tal
                    for item in soup.findAll("p"):  #selecionando os blocos com as noticias
                        noticia=(item.get_text()) #extraindo e escrevendo cada bloco no arquivo
                        #pode variar dependendo do site
                        if (noticia.find("Reprodução autorizada mediante indicação da fonte.") != -1): #invalida o bloco que contiver essa frase, pois eh lixo do site
                            continue
                        for linha in item.find_all('a'): #percorre o bloco procurando classes a (links)
                            with open('citados.txt', 'a') as arqv_citados:  #extrai os links citados no corpo na noticia (referencia)
                                test = linha.get('href')
                                if (test is not None):
                                    arqv_citados.write(test + '\n') #escreve o link citado no corpo do texto (link referenciado)
                        #limpando a noticia de termos indesejados !!
                        pat1 = re.compile('Conteúdo exclusivo e gratuito. Cadastre-se')
                        noticia = (re.sub(pat1, '', noticia))

                        #removendo os termos dentro do texto inteiro
                        pat2 = re.compile('Empresa Brasil de Comunicação S/A - EBC')
                        noticia = (re.sub(pat2, '', noticia))
                        arqv_nots.write(noticia)
                    arqv_nots.write("\nYippieKiYay\n") #Separador

            with open('visitados.txt', 'a') as arqv_visitados:  #colocando o link no arqv dict
                arqv_visitados.write(link + '\n')
            dataOK = True #setando o flag

if (pular == "N"):
    #percorrer  por feed as paginas
    for pagina in range(pag_ini, pag_fim):  #intervalo de paginas (feed) a ser percorrido
        posts = get_portal_links(url_base + url_pag + str(pagina) + "/")  #chamaremos as paginas, e tiraremos os links
        print(pagina)
        dado = []
        for post in posts:  #preenchendo a lista com os links
            post_data = extrai_dados(post)  #extraindo os links
            dado.append(post_data)  #colocando apenas os links na lista

        for link in dado:  #percorrendo os links na lista
            link = is_relativo(link)  #testando se o link e link relativo
            if (dict.get(link, 0) == 0):  #se o link nao estiver no dic add ele e continua (sendo ele processado dps ou nao)
                dict[link] = 1  #o link vai pro dict, mas so vai pro arquivo dps de ser processado
                objval = re.match(er, link)
                if (objval is not None):  # testando se o link eh apto a processar
                    with open("links.txt", "a") as arqv:
                        arqv.write(link + "\n")  # colocando o link apto (passou pela ER) no arqv de links a serem processados
                else:  #nao passou pela ER, mas vai pro arqv dict pra nao voltarmos nele
                    with open("visitados.txt", "a") as arqv_dict:
                        arqv_dict.write(link + "\n")


#a primeira parte tem a funcao de extrair as paginas para coleta, aqui sera a chamada a funcao que processa, extrai o conteudo
#e preenche os arquivos etc.
print("processando...")
processa_links()#se os starters forem rapidos executa naturalmente, se eles demorarem a iniciar a coleta, podemos pular
#direto para o processamento
print("Done")




