from sqlalchemy import Integer, String, Column, Numeric

from shared.database import Base


class ContaPagarReceber(Base):
    __tablename__ = 'conta_pagar_receber'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(30))
    valor = Column(Numeric)
    tipo = Column(String(30))


#
# https://www.youtube.com/watch?v=1n9pidw3XO0
# 17:20