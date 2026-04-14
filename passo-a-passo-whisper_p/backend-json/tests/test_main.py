import sys
from pathlib import Path
from unittest import TestCase

from fastapi.testclient import TestClient


BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app.main import app, validar_cpf  # noqa: E402


class CPFValidationTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_validar_cpf_valido(self) -> None:
        self.assertTrue(validar_cpf("529.982.247-25"))

    def test_validar_cpf_invalido(self) -> None:
        self.assertFalse(validar_cpf("529.982.247-24"))

    def test_endpoint_retorna_cpf_valido(self) -> None:
        response = self.client.post("/validar-cpf", json={"cpf": "529.982.247-25"})
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["valido"])
        self.assertEqual(data["mensagem"], "CPF valido.")

    def test_endpoint_rejeita_sequencia_repetida(self) -> None:
        response = self.client.post("/validar-cpf", json={"cpf": "111.111.111-11"})
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(data["valido"])
        self.assertEqual(data["mensagem"], "CPF invalido: sequencias repetidas nao sao aceitas.")
