from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from shared.database import Base
from shared.dependecies import get_db

client = TestClient(app)

# Para rodar os teste sem quebar o banco de dados produção.
SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_some_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def overrride_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = overrride_get_db


def test_deve_listar_contas_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post("/contas-a-pagar-e-receber", json={'descricao': 'Aluguel', 'valor': '1000.5', 'tipo': 'PAGAR'})
    client.post("/contas-a-pagar-e-receber", json={'descricao': 'Salário', 'valor': '5000', 'tipo': 'RECEBER'})

    response = client.get("/contas-a-pagar-e-receber")

    assert response.status_code == 200

    print(response.json())

    assert response.json() == [
        {'id': 1, 'descricao': 'Aluguel', 'valor': '1000.5000000000', 'tipo': 'PAGAR'},
        {'id': 2, 'descricao': 'Salário', 'valor': '5000.0000000000', 'tipo': 'RECEBER'}
    ]


def test_deve_criar_conta_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    nova_conta = {
        "descricao": "Curso de Python2",
        "valor": 333,
        "tipo": "PAGAR"
    }

    nova_conta_copy = nova_conta.copy()
    nova_conta_copy["id"] = 1
    nova_conta_copy["valor"] = '333.0000000000'

    response = client.post("/contas-a-pagar-e-receber", json=nova_conta)
    assert response.status_code == 201
    # assert response.json() == nova_conta_copy
    assert response.json()["id"] == nova_conta_copy["id"]
    assert response.json()["descricao"] == nova_conta_copy["descricao"]
    assert response.json()["valor"] == nova_conta_copy["valor"]
    assert response.json()["tipo"] == nova_conta_copy["tipo"]


def test_deve_retornar_erro_quando_exceder_descricao():
    response = client.post('/contas-a-pagar-e-receber', json={
        "descricao": "Curso de Python2 jakdjfakjfak kja fkajf k jakfdjakfjakjfakjfakjfkasjfjasdkjfaksjfdlka",
        "valor": 333,
        "tipo": "PAGAR"
    })

    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ["body", "descricao"]


def test_deve_retornar_erro_quando_descricao_for_menor_que_tres():
    response = client.post('/contas-a-pagar-e-receber', json={
        "descricao": "Py",
        "valor": 333,
        "tipo": "PAGAR"
    })

    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ["body", "descricao"]


def test_deve_retornar_erro_quando_valor_for_zero_ou_menor():
    response = client.post('/contas-a-pagar-e-receber', json={
        "descricao": "Curso de Python2",
        "valor": -1,
        "tipo": "PAGAR"
    })

    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ["body", "valor"]


def test_deve_retornar_erro_quando_tipo_forem_invalidos():
    response = client.post('/contas-a-pagar-e-receber', json={
        "descricao": "Curso de Python2",
        "valor": 33,
        "tipo": "PAGAR1"
    })

    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ["body", "tipo"]


def test_deve_atualizar_conta_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/contas-a-pagar-e-receber", json={
        "descricao": "Curso de Python2",
        "valor": 333,
        "tipo": "PAGAR"
    })

    id_da_conta_a_pagar_e_receber = response.json()['id']

    response_put = client.put(f"/contas-a-pagar-e-receber/{id_da_conta_a_pagar_e_receber}", json={
        "descricao": "Curso de Python2",
        "valor": 111,
        "tipo": "PAGAR"
    })

    assert response_put.status_code == 200
    assert response_put.json()["valor"] == "111.0000000000"


def test_deve_remover_conta_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/contas-a-pagar-e-receber", json={
        "descricao": "Curso de Python2",
        "valor": 333,
        "tipo": "PAGAR"
    })

    id_da_conta_a_pagar_e_receber = response.json()['id']

    response_delete = client.delete(f"/contas-a-pagar-e-receber/{id_da_conta_a_pagar_e_receber}")

    assert response_delete.status_code == 204


# def test_deve_pegar_por_id():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#
#     response = client.post("/contas-a-pagar-e-receber", json={
#         "descricao": "Curso de Python2",
#         "valor": 333,
#         "tipo": "PAGAR"
#     })
#
#     id_da_conta_a_pagar_e_receber = response.json()['id']
#
#     response_get = client.put(f"/contas-a-pagar-e-receber/{id_da_conta_a_pagar_e_receber}")
#
#     assert response_get.status_code == 422
#     assert response_get.json()["valor"] == "333.0000000000"
#     assert response_get.json()["tipo"] == "PAGAR"
#     assert response_get.json()["descricao"] == "Curso de Python2"
