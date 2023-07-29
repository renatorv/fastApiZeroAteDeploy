from decimal import Decimal
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/contas-a-pagar-e-receber")


class ContaPagarReceberResponse(BaseModel):
    id: int
    description: str
    valor: Decimal
    tipo: str  # PAGAR, RECEBER


class ContaPagarReceberRequest(BaseModel):
    description: str
    valor: Decimal
    tipo: str  # PAGAR, RECEBER


@router.get("", response_model=List[ContaPagarReceberResponse])
def listar_contas():
    return [
        ContaPagarReceberResponse(
            id=1,
            description="Aluguel",
            valor=1000.50,
            tipo="PAGAR"
        ),
        ContaPagarReceberResponse(
            id=2,
            description="Salário",
            valor=5000,
            tipo="RECEBER"
        ),
    ]


@router.post("", response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta: ContaPagarReceberRequest):
    return ContaPagarReceberResponse(
        id=3,
        description=conta.description,
        valor=conta.valor,
        tipo=conta.tipo
    )
