import uvicorn
from fastapi import FastAPI

from contas_a_pagar_e_receber.routers import contas_a_pagar_e_receber_router

# cria uma variável app com uma instância do FastAPI
app = FastAPI()

@app.get("/")
def oi_eu_sou_dev() -> str:
    return "Oi, eu sou um Dev!"


app.include_router(contas_a_pagar_e_receber_router.router)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)