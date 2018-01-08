from bs4 import BeautifulSoup
import csv
import zipfile
import requests

url = "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_lotfac.zip"
response = requests.get(url, stream=True)

# Extraindo o zip
zFile = zipfile.ZipFile("D_lotfac.zip")
arquivo = zFile.open(zFile.infolist()[0])


soup = BeautifulSoup(arquivo, "html.parser")  # html.parser html5lib lxml
samples = soup.find("table")


def titulo(content, tag):
    """" Separa apenas linha """
    count = 0
    titles = []
    for row in content.find_all(tag):
        count = count + 1
        titles.append(row.text.strip())
        if count > 16:
            break
    return titles


def resultados(content, tag, tag2):
    """" Separa valores de cada coluna isolando em linhas """
    linhas = []
    for row in content.find_all(tag):
        count = 0
        colunas = []
        for row2 in row.find_all(tag2):
            count = count + 1
            if row2.has_attr('rowspan'):
                colunas.append(row2.text.strip())
            else:
                break
            if count > 16:
                break
        if len(colunas) > 1:
            linhas.append(colunas)
    return linhas


def escrever_arquivo():
    file = open("/home/cabox/workspace/lotofacil.csv", 'w')
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    rs = resultados(samples, "tr", "td")
    writer.writerow(titulo(samples, "th"))
    for row in rs:
        writer.writerow(row)
    file.close()


escrever_arquivo()


def ler_arquivo():
    file = open("/home/cabox/workspace/lotofacil.csv", newline='')
    reader = csv.reader(file)
    for row in reader:
        print(row)


ler_arquivo()
