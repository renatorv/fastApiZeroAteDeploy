import uvicorn
from fastapi import FastAPI

from contas_a_pagar_e_receber.routers import contas_a_pagar_e_receber_router
from shared.exceptions import NotFound
from shared.exceptions_handler import not_found_exception_handler

'''
    Essas 3 linhas são responsáveis por recriar o bd a cada compilação.
'''
# from contas_a_pagar_e_receber.models.contas_a_pagar_receber_model import ContaPagarReceber
#
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)

# cria uma variável app com uma instância do FastAPI
app = FastAPI()


@app.get("/")
def oi_eu_sou_dev() -> str:
    return "Oi, eu sou um Dev!"


app.include_router(contas_a_pagar_e_receber_router.router)
app.add_exception_handler(NotFound, not_found_exception_handler)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)
