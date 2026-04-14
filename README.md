# Validador de CPF

Projeto final da disciplina de Servicos de Software.

Integrantes:

Nome: Felipe Jaenes Marcilio RA: 25.80176-2

Nome: Gabriel Ferreira Fiorotti RA: 16.00595-3

Nome: Lucas Garcia Lopes RA: 25.80183-8

Nome: Mariana Mazzali Stauch RA: 25.80058-2

Nome: Pedro Henrique Reinato Mattia RA: 25.80055-8


Esta aplicacao foi desenvolvida com dois containers Docker:

- `frontend`: interface web em Gradio para entrada do CPF e exibicao do resultado.
- `backend`: API REST em FastAPI responsavel pela validacao do CPF.

## Funcionalidades

- Recebe CPF com ou sem pontuacao.
- Normaliza a entrada para conter apenas digitos.
- Verifica se o CPF possui 11 digitos.
- Rejeita sequencias repetidas, como `111.111.111-11`.
- Calcula os digitos verificadores para informar se o CPF e valido ou invalido.
- Exibe ao usuario o status da validacao, uma mensagem explicativa e o CPF formatado.

## Estrutura do projeto

O projeto principal esta na pasta `passo-a-passo-whisper_p/`.

- `gradio-json/`: frontend
- `backend-json/`: backend
- `compose.yaml`: sobe os dois servicos juntos

## Como executar

```bash
cd passo-a-passo-whisper_p
docker compose up --build
```

Depois disso:

- Frontend: `http://localhost:7860`
- Backend: `http://localhost:8080`
- Documentacao da API: `http://localhost:8080/docs`

## Endpoint principal

`POST /validar-cpf`

Exemplo de requisicao:

```json
{
  "cpf": "529.982.247-25"
}
```

Exemplo de resposta:

```json
{
  "cpf_informado": "529.982.247-25",
  "cpf_normalizado": "52998224725",
  "cpf_formatado": "529.982.247-25",
  "valido": true,
  "mensagem": "CPF valido."
}
```

## Testes

Os testes do backend podem ser executados com:

```bash
cd passo-a-passo-whisper_p/backend-json
python -m unittest discover -s tests
```
