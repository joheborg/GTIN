from fastapi import FastAPI
from typing import Union
from main import BuscarGTIN
#app = FastAPI()
app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

#codZen = faça um cadastro neste site e envie a chave https://www.zenrows.com/blog/selenium-cloudflare-bypass#what-is-selenium
#iten_id é o gtin do produto que deseja perquisar
#exemplo get http://127.0.0.1:8000/c0c9cd9ef67818b2c18f901f4095a04ad78a9163/7899947313914

@app.get("/{codZen}/{item_id}")
def read_item(codZen: str, item_id: int):
    if codZen == "":
        return {"Erro": "É necessario codigo zenRows"}
    tentativas = 0
    while True:
        resultado = BuscarGTIN(item_id, codZen)
        if "Erro" in resultado:
            tentativas += 1
        if tentativas == 5 and "Erro" in resultado:
            return {"Erro": "Produto não encontrado"}
        if not "Erro" in resultado:
            break
    return resultado
