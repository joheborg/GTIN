from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha

retorno = {}

def solve_captcha(site_key, url):
    solver = TwoCaptcha("b3c8b3aae00503ae68ad42754bc6e8f1")
    result = solver.recaptcha(sitekey=site_key, url=url)
    return result['code']

def BuscarGTIN(gtin):
    url = "https://cosmos.bluesoft.com.br/produtos/" + str(gtin)

    # Configurar o WebDriver (Certifique-se de ter o driver do Chrome instalado)
    driver = webdriver.Chrome()
    
    try:
        driver.get(url)
        
        # Coletar a chave do site (site_key) para resolver o CAPTCHA
        site_key = driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
        
        # Resolver o CAPTCHA
        captcha_solution = solve_captcha(site_key, url)
        
        # Injetar a solução do CAPTCHA no campo oculto do formulário
        driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{captcha_solution}";')
        
        # Submeter o formulário (ajuste o seletor conforme necessário)
        submit_button = driver.find_element(By.ID, "submit-button")  # Substitua "submit-button" pelo ID correto do botão
        submit_button.click()
        
        # Esperar a página carregar após o CAPTCHA ser resolvido
        driver.implicitly_wait(10)
        
        # Pegar o conteúdo da página carregada
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        
        # Tratar o retorno com as funções existentes
        return TratarRetorno(soup)

    finally:
        driver.quit()

def ColetarSRCImage(soup):
    product_divimage = soup.find("div", {"class": "picture"})
    if product_divimage != None:
        product_imagea = product_divimage.find("a")
        product_image = product_imagea.find("img")
        return "https://cdn-cosmos.bluesoft.com.br/products/" + ColetarGTINProduto(soup)

def ColetarInformacaoProduto(soup):
    dt_tags = soup.find_all("dt")
    pais_registro = ""
    fabricante = ""
    distribuidores = ""
    marca = ""
    if dt_tags != None:
        for dt in dt_tags:
            if "País de Registro:" in dt.get_text():
                dd = dt.find_next("dd")
                pais_registro = dd.get_text().strip()
            if "Fabricante:" in dt.get_text():
                dd = dt.find_next("dd")
                fabricante = dd.get_text().strip()
            if "Distribuidores:" in dt.get_text():
                dd = dt.find_next("dd")
                distribuidores = dd.get_text().strip()
            if "Marca:" in dt.get_text():
                dd = dt.find_next("dd")
                marca = dd.get_text().strip()
        return {
            "PAISREGISTRO": pais_registro,
            "FABRICANTE": fabricante,
            "DISTRIBUIDORES": distribuidores,
            "MARCA": marca,
        }

def ColetarGTINProduto(soup):
    product_gtin = soup.find("span", {"id": "product_gtin"})
    if product_gtin != None:
        resultadopg = ""
        dentroTag = 0
        for caractere in product_gtin:
            if caractere == "<":
                dentroTag = 1
            if caractere == ">":
                dentroTag = 0
            if dentroTag == 0:
                resultadopg = str(resultadopg) + str(caractere)
        resultadopg = resultadopg.replace('<span id="product_gtin">', "")
        resultadopg = resultadopg.replace("</span>", "")
        return resultadopg

def ColetarDescricaoProduto(soup):
    product_description = soup.find("span", {"id": "product_description"})
    if product_description != None:
        resultadopd = ""
        dentroTag = 0
        for caractere in product_description:
            if caractere == "<":
                dentroTag = 1
            if caractere == ">":
                dentroTag = 0
            if dentroTag == 0:
                resultadopd = str(resultadopd) + str(caractere)
        resultadopd = resultadopd.replace(">", "")
        return resultadopd

def ColetarNCMProduto(soup):
    product_ncm = soup.find("span", {"class": "description"})
    if product_ncm != None:
        resultadoncm = ""
        dentroTag = 0
        if product_ncm == None:
            return {"Erro": "Tente novamente"}
        for dado in product_ncm:
            for caractere in dado:
                if caractere == "<":
                    dentroTag = 1
                if caractere == ">":
                    dentroTag = 0
                if dentroTag == 0:
                    resultadoncm = str(resultadoncm) + str(caractere)
        resultado = ""
        for caractere in resultadoncm:
            if caractere == "<":
                dentroTag = 1
            if caractere == ">":
                dentroTag = 0
            if dentroTag == 0:
                resultado = str(resultado) + str(caractere)
        resultado = resultado.replace(">", "")
        resultado = resultado.replace("\n", "")
        resultadoSplit = resultado.split(" - ")
        codigoNCM = resultadoSplit[0]
        descricaoNCM = resultado.replace(codigoNCM + " - ", "")
        return {"CODIGO": codigoNCM, "DESCRICAO": descricaoNCM, "COMPLETO": resultado}

def ColetarUnidadesComerciaisProduto(soup):
    product_unidadeTable = soup.find("table")
    if product_unidadeTable != None:
        product_unidadeTBody = product_unidadeTable.find("tbody")
        product_unidadeTr = product_unidadeTBody.find("tr")
        product_unidadeTd = product_unidadeTr.find_all("td")
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
