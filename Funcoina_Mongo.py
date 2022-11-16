from datetime import date
from pymongo import MongoClient

from Funciona_EntregaORM import Cliente

client = MongoClient('localhost', 27017)

mydatabase = client.mdbg2



def insertPedido(numPedido):
   myPedido = {"numero": numPedido}
   mycollection = mydatabase.Pedidos
   mycollection.insert_many([myPedido])

insertPedido(432)
insertPedido(2)