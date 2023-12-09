from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from enum import Enum
import time

app = FastAPI()

class AtendimentoEnum(str, Enum):
    NORMAL = "N"
    PRIORITARIO = "P"

class Cliente(BaseModel):
    nome: str
    atendimento: AtendimentoEnum
    data_chegada: str

fila = []

@app.get("/fila", response_model=List[Cliente])
def obter_fila():
    return [{"posicao": cliente["posicao"], "nome": cliente["nome"], "atendimento": cliente["atendimento"],
             "data_chegada": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cliente["data_chegada"])),
             "atendido": cliente["atendido"]} for cliente in fila]

@app.get("/fila/{id}", response_model=Cliente)
def obter_cliente_na_posicao(id: int):
    if id >= len(fila):
        raise HTTPException(status_code=404, detail="Cliente não encontrado na posição especificada.")
    cliente = fila[id]
    return {"posicao": cliente["posicao"], "nome": cliente["nome"], "atendimento": cliente["atendimento"],
            "data_chegada": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cliente["data_chegada"])),
            "atendido": cliente["atendido"]}

@app.post("/fila", response_model=Cliente)
def adicionar_cliente(cliente: Cliente):
    if len(cliente.nome) > 20:
        raise HTTPException(status_code=400, detail="O campo 'nome' deve ter no máximo 20 caracteres.")
    novo_cliente = {"posicao": len(fila), "nome": cliente.nome, "atendimento": cliente.atendimento, "data_chegada": time.time(), "atendido": False}
    fila.append(novo_cliente)
    return {"posicao": novo_cliente["posicao"], "nome": novo_cliente["nome"],
            "atendimento": novo_cliente["atendimento"],
            "data_chegada": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(novo_cliente["data_chegada"])),
            "atendido": novo_cliente["atendido"]}

@app.put("/fila")
def atualizar_fila():
    if len(fila) > 0:
        fila.pop(0) 
        for i in range(len(fila)):
            fila[i]["posicao"] = i
    return {"message": "Fila atualizada com sucesso."}

@app.delete("/fila/{id}")
def remover_cliente(id: int):
    if id >= len(fila):
        raise HTTPException(status_code=404, detail="Cliente não encontrado na posição especificada.")
    fila.pop(id)
    for i in range(id, len(fila)):
        fila[i]["posicao"] -= 1
    return {"message": "Cliente removido com sucesso."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
