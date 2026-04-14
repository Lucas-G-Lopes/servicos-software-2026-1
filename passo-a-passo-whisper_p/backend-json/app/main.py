from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="Validador de CPF",
    description="API REST para validar os digitos verificadores de um CPF.",
)


class CPFRequest(BaseModel):
    cpf: str


class CPFResponse(BaseModel):
    cpf_informado: str
    cpf_normalizado: str
    cpf_formatado: str | None
    valido: bool
    mensagem: str


def somente_digitos(valor: str) -> str:
    return "".join(filter(str.isdigit, valor))


def formatar_cpf(cpf: str) -> str:
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def calcular_digito(cpf_parcial: str) -> int:
    peso_inicial = len(cpf_parcial) + 1
    soma = sum(int(digito) * (peso_inicial - indice) for indice, digito in enumerate(cpf_parcial))
    resto = soma % 11
    return 0 if resto < 2 else 11 - resto


def validar_cpf(cpf: str) -> bool:
    cpf = somente_digitos(cpf)

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    primeiro_digito = calcular_digito(cpf[:9])
    segundo_digito = calcular_digito(cpf[:9] + str(primeiro_digito))
    return cpf[-2:] == f"{primeiro_digito}{segundo_digito}"


@app.get("/")
def healthcheck() -> dict[str, str]:
    return {"status": "ok", "servico": "validador-cpf"}


@app.post("/validar-cpf", response_model=CPFResponse)
def validar_cpf_endpoint(payload: CPFRequest) -> CPFResponse:
    cpf_normalizado = somente_digitos(payload.cpf)
    cpf_valido = validar_cpf(payload.cpf)

    if len(cpf_normalizado) != 11:
        mensagem = "CPF invalido: informe exatamente 11 digitos."
        cpf_formatado = None
    elif cpf_normalizado == cpf_normalizado[:1] * 11:
        mensagem = "CPF invalido: sequencias repetidas nao sao aceitas."
        cpf_formatado = formatar_cpf(cpf_normalizado)
    elif cpf_valido:
        mensagem = "CPF valido."
        cpf_formatado = formatar_cpf(cpf_normalizado)
    else:
        mensagem = "CPF invalido: digitos verificadores nao conferem."
        cpf_formatado = formatar_cpf(cpf_normalizado)

    return CPFResponse(
        cpf_informado=payload.cpf,
        cpf_normalizado=cpf_normalizado,
        cpf_formatado=cpf_formatado,
        valido=cpf_valido,
        mensagem=mensagem,
    )
