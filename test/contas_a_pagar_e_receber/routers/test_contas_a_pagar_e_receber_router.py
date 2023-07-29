from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_deve_listar_contas_a_pagar_e_receber():
    response = client.get("/contas-a-pagar-e-receber")
    assert response.status_code == 200

    # print(response.json())

    assert response.json() == [
        {'id': 1, 'descricao': 'Aluguel', 'valor': '1000.5', 'tipo': 'PAGAR'},
        {'id': 2, 'descricao': 'Salário', 'valor': '5000', 'tipo': 'RECEBER'}
    ]


def test_deve_criar_conta_a_pagar_e_receber():
    nova_conta = {
        "descricao": "Curso de Python",
        "valor": 333,
        "tipo": "PAGAR"
    }

    nova_conta_copy = nova_conta.copy()
    nova_conta_copy["id"] = 3
    nova_conta_copy["valor"] = '333'

    response = client.post("/contas-a-pagar-e-receber", json=nova_conta)
    assert response.status_code == 201
    # assert response.json() == nova_conta_copy
    assert response.json()["id"] == nova_conta_copy["id"]
    assert response.json()["descricao"] == nova_conta_copy["descricao"]
    assert response.json()["valor"] == nova_conta_copy["valor"]
    assert response.json()["tipo"] == nova_conta_copy["tipo"]
