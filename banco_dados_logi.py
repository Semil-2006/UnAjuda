from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Banco = declarative_base()


class Usuario(Banco):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Usuario(nome='{self.nome}', email='{self.email}')>"


engine = create_engine('sqlite:///usuarios.db')

Banco.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
