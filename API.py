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

@app.get("/{codZen}/{item_id}")
def read_item(codZen: str, item_id: int):
    if codZen == "":
        return Response(content="É necessário código zenRows", status_code=400)
    tentativas = 0
    while True:
        resultado = BuscarGTIN(item_id, codZen)
        if "Erro" in resultado:
            tentativas += 1
        if tentativas == 5 and "Erro" in resultado:
            return Response(content="Produto não encontrado", status_code=404)
        if not "Erro" in resultado:
            break
    return resultado

if __name__ == "__main__":
    ip = "127.0.0.1" 
    port = 80
    uvicorn.run(app, host=ip, port=port)
