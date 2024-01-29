from zenrows import ZenRowsClient
from bs4 import BeautifulSoup

retorno = {}

def BuscarGTIN(gtin, zenRows):
    url = 'https://cosmos.bluesoft.com.br/produtos/' + str(gtin)
    client = ZenRowsClient(str(zenRows))
    response = client.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return TratarRetorno(soup)

def ColetarSRCImage(soup):
    product_divimage = soup.find('div', {"class": 'picture'})
    if product_divimage != None:
        product_imagea = product_divimage.find('a')
        product_image = product_imagea.find('img')
        return "https://cdn-cosmos.bluesoft.com.br/products/" + ColetarGTINProduto(soup)
        # return product_image["src"]

def ColetarInformacaoProduto(soup):
    dt_tags = soup.find_all('dt')
    pais_registro = ""
    fabricante = ""
    distribuidores = ""
    marca = ""
    print(dt_tags)
    if dt_tags != None:
        for dt in dt_tags:
            if "País de Registro:" in dt.get_text():
                dd = dt.find_next('dd')
                pais_registro = dd.get_text().strip()
            if "Fabricante:" in dt.get_text():
                dd = dt.find_next('dd')
                fabricante = dd.get_text().strip()
            if "Distribuidores:" in dt.get_text():
                dd = dt.find_next('dd')
                distribuidores = dd.get_text().strip()
            if "Marca:" in dt.get_text():
                dd = dt.find_next('dd')
                marca = dd.get_text().strip()
        return {"PAISREGISTRO": pais_registro, "FABRICANTE": fabricante, "DISTRIBUIDORES": distribuidores, "MARCA": marca}

def ColetarGTINProduto(soup):
    product_gtin = soup.find('span', {"id": 'product_gtin'})
    if product_gtin != None:
        resultadopg = ""
        dentroTag = 0
        for caractere in product_gtin:
            if caractere == '<':
                dentroTag = 1
            if caractere == '>':
                dentroTag = 0
            if dentroTag == 0:
                resultadopg = (str(resultadopg) + str(caractere))
        resultadopg = resultadopg.replace('<span id="product_gtin">', '')
        resultadopg = resultadopg.replace('</span>', '')
        return resultadopg

def ColetarDescricaoProduto(soup):
    product_description = soup.find('span', {"id": 'product_description'})
    if product_description != None:
        resultadopd = ""
        dentroTag = 0
        for caractere in product_description:
            if caractere == '<':
                dentroTag = 1
            if caractere == '>':
                dentroTag = 0
            if dentroTag == 0:
                resultadopd = (str(resultadopd) + str(caractere))
        resultadopd = resultadopd.replace('>', '')
        return resultadopd

def ColetarNCMProduto(soup):
    product_ncm = soup.find('span', {"class": 'description'})
    if product_ncm != None:
        resultadoncm = ""
        dentroTag = 0
        if product_ncm == None:
            print(product_ncm)
            return {"Erro": "Tente novamente"}
        for dado in product_ncm:
            for caractere in dado:
                if caractere == '<':
                    dentroTag = 1
                if caractere == '>':
                    dentroTag = 0
                if dentroTag == 0:
                    resultadoncm = (str(resultadoncm) + str(caractere))
        resultado = ""
        for caractere in resultadoncm:
            if caractere == '<':
                dentroTag = 1
            if caractere == '>':
                dentroTag = 0
            if dentroTag == 0:
                resultado = (str(resultado) + str(caractere))
        resultado = resultado.replace('>', '')
        resultado = resultado.replace('\n', '')
        resultadoSplit = resultado.split(' - ')
        codigoNCM = resultadoSplit[0]
        descricaoNCM = resultado.replace(codigoNCM + " - ", "")
        return {"CODIGO": codigoNCM,
                "DESCRICAO": descricaoNCM, "COMPLETO": resultado}

def ColetarUnidadesComerciaisProduto(soup):
    product_unidadeTable = soup.find('table')
    if product_unidadeTable != None:
        product_unidadeTBody = product_unidadeTable.find('tbody')
        product_unidadeTr = product_unidadeTBody.find('tr')
        product_unidadeTd = product_unidadeTr.find_all('td')
        valores = []
        for td in product_unidadeTd:
            valor = td.get_text().strip()
            valores.append(valor)
        return {
            "GTIN": valores[0],
            "TIPO": valores[1],
            "EMBALAGEM": valores[2],
            "LASTRO": valores[3],
            "CAMADA": valores[4],
            "COMPRIMENTO": valores[5],
            "ALTURA": valores[6],
            "LARGURA": valores[7],
            "BRUTO": valores[8],
            "LIQUIDO": valores[9],
        }


def TratarRetorno(soup):
    if ColetarDescricaoProduto(soup) == None:
        return {"Erro": "None"}
    retorno["UNIDADESCOMERCIAIS"] = ColetarUnidadesComerciaisProduto(soup)
    retorno["NCM"] = ColetarNCMProduto(soup)
    retorno["NOMEPRODUTO"] = ColetarDescricaoProduto(soup)
    retorno["IMAGEM"] = ColetarSRCImage(soup)
    retorno["GTIN"] = ColetarGTINProduto(soup)
    retorno["INFORMACAO"] = ColetarInformacaoProduto(soup)
    return retorno
