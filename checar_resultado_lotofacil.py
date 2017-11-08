import requests
from bs4 import BeautifulSoup
import resultados_lotofacil
import meus_jogos_lotofacil 

url = "http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil"
pagina = requests.get(url)

if (pagina.status_code != 200):
  print("Erro {} ao tentar conectar na URL {}".format(pagina.status_code, url))
else:
  print("Conexao realizada com sucesso!", pagina.status_code)
  
  
html = pagina.text
soup = BeautifulSoup(html, "html.parser")  # html.parser html5lib lxml
#print("Titulo da Pagina: ", soup.title.encode('utf-8'))  # utf-8 latin-1 ascii
samples = soup.find("table", "simple-table")
# print(samples)
titulo = soup.find("div", "title-bar clearfix")

################################################################################
#  R$  4,00 para as apostas com 11 prognósticos certos entre os 15 sorteados;  #
#  R$  8,00 para as apostas com 12 prognósticos certos entre os 15 sorteados;  #
#  R$ 20,00 para as apostas com 13 prognósticos certos entre os 15 sorteados.  #
#                                                                              #
#  Quantidade de números	Valor em R$                                          #
#  15 números                 2,00                                             #
#  16 números                32,00                                             #
#  17 números               272,00                                             #
#  18 números             1.632,00                                             #
#  Atualização do comentario                                                   #
#                                                                              #
################################################################################

def imprimir_content(content, tag):
    rows = []
    for row in content.find_all(tag):
        rows.append(row.text.strip())
    return rows


def resultado_em_inteiro():
    result = imprimir_content(samples, "td")
    for i in range(15):
        result[i] = int(result[i])
    return result

  
#titulo = titulo.text.replace("\n", " ")
#print(titulo.encode('utf-8'))
#print(imprimir_content(titulo, "span"))
#print(imprimir_content(samples, "td"))
print(" ============= ", imprimir_content(titulo, "span")[0], resultado_em_inteiro(), " ============= ")
#print(meus_jogos_lotofacil.carregar_jogos())


def compara_resultado(resultado, jogos, concurso, quantidade_jogos):
    contador = 0
    count = []
    arrumar = []
    cc = concurso[10:]
    if cc.isnumeric():
      cc = int(cc)
    #print(cc)
    for i in range(quantidade_jogos):
        for j in range(15):
            for k in range(15):
                if resultado[j] == jogos[i][k]:
                    contador = contador + 1
        if contador>=11 and cc != (i+1):
          arrumar = jogos[i]
          arrumar.sort()
          print("{}: ".format(concurso), resultado, " Jogo {}: ".format(i+1), arrumar)
          var = "Jogo_" + str(i+1) + ": " + str(contador)
          count.append(var)
        contador = 0
    return count


print(" **** ", compara_resultado(resultado_em_inteiro(), meus_jogos_lotofacil.carregar_jogos(), 
                        imprimir_content(titulo, "span")[0], len(meus_jogos_lotofacil.carregar_jogos()))," **** ")

def ultimos_resultados():
  resultado_especifico = resultados_lotofacil.todos_resultados()
  # print(resultado_especifico[1552])
  string_concurso_atual = imprimir_content(titulo, "span")[0]
  concurso_atual = int(string_concurso_atual[9:13])
  print("Concurso atual: ",concurso_atual)
  for i in range(concurso_atual-15, concurso_atual):
    concurso = "concurso: " + str(i+1)
    print(" >>> ", compara_resultado(resultado_especifico[i], meus_jogos_lotofacil.carregar_jogos(), 
                        concurso, len(meus_jogos_lotofacil.carregar_jogos())), " <<< ")
    

#ultimos_resultados()


def compara_tudo(total):
  rs = resultados_lotofacil.todos_resultados()
  atual = []
  for i in range(total):
    atual = rs[i]
    atual.sort()
    concurso = "Concurso: "+str(i+1)
    resultadoCount = compara_resultado(atual, meus_jogos_lotofacil.carregar_jogos(), concurso, len(meus_jogos_lotofacil.carregar_jogos()))
    if resultadoCount != []:
      print(" >>> compara_tudo <<< ",resultadoCount, " <<>> ")


#compara_tudo(len(resultados_lotofacil.todos_resultados()))


def compara_itself(total):
  rs = resultados_lotofacil.todos_resultados()
  atual = []
  for i in range(total):
    atual = rs[i]
    atual.sort()
    concurso = "Concurso: "+str(i+1)
    resultadoCount = compara_resultado(atual, resultados_lotofacil.todos_resultados(), concurso, len(resultados_lotofacil.todos_resultados()))
    if resultadoCount != []:
      print(" >>> compara_itself <<< ",resultadoCount, " <<>> ")


#compara_itself(len(resultados_lotofacil.todos_resultados()))


def compara_itself2(total):
  rs = meus_jogos_lotofacil.carregar_jogos()
  atual = []
  for i in range(total):
    atual = rs[i]
    atual.sort()
    concurso = "Concurso: "+str(i+1)
    resultadoCount = compara_resultado(atual, meus_jogos_lotofacil.carregar_jogos(), concurso, len(meus_jogos_lotofacil.carregar_jogos()))
    if resultadoCount != []:
      print(" *** compara_itself2 *** ", resultadoCount, " **** ")


#compara_itself2(len(meus_jogos_lotofacil.carregar_jogos()))
