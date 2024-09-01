from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from main import BuscarGTIN
import uvicorn

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def tentar_buscar_gtin(item_id: int, max_tentativas: int = 5):
    for tentativa in range(max_tentativas):
        resultado = BuscarGTIN(item_id)
        if "Erro" not in resultado:
            return resultado
        elif tentativa + 1 == max_tentativas:
            return None
    return None

@app.get("/{item_id}")
def read_item(item_id: int):

    resultado = tentar_buscar_gtin(item_id)
    if resultado is None:
        return Response(content="Produto não encontrado após várias tentativas", status_code=404)

    return resultado

if __name__ == "__main__":
    ip = "0.0.0.0" 
    port = 80
    uvicorn.run(app, host=ip, port=port)
