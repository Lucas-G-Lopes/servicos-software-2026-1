import os
import shutil
import whisper 
from typing import Optional, Union
from fastapi import FastAPI
from fastapi import File, UploadFile

import json
from pydantic import BaseModel

app=FastAPI()

print ("Carregando modelo de IA (Whisper)...")
model = whisper.load_model("base")
print("Modelo carregado!")

@app.get("/")
def diz_ola():
    return { "Olá" : "Mundo" }


@app.post("/transcrever")
async def transcrever_audio(file: UploadFile = File(...)):
    caminho_temp = f"temp_{file.filename}"
    with open(caminho_temp, "wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

    try:
        resultado = model.transcribe(caminho_temp, language="pt")
        texto = resultado["text"].strip()
    finally:
        if os.path.exists(caminho_temp):
            os.remove(caminho_temp)
    return { "texto" : texto }

def validar_cpf(cpf: str) -> bool:
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))
    
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    # Calcula primeiro dígito
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    dig1 = 0 if resto < 2 else 11 - resto
    
    if dig1 != int(cpf[9]):
        return False
    
    # Calcula segundo dígito
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    dig2 = 0 if resto < 2 else 11 - resto
    
    return dig2 == int(cpf[10])
