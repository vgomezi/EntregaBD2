from datetime import date
from pymongo import MongoClient

from Funciona_EntregaORM import Cliente


def get_database():
 
#    # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb://localhost:27017/"
 
#    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)

   mydatabase = client['mdbg2']
 
#    # Create the database for our example (we will use the same database throughout the tutorial
   return mydatabase

def alta_pedido_simple_m(dni_cliente_i, precio_total_i, estado_i, fecha_obj_i, canal_compra_i, nro_pedido_compuesto_i):

   print("hola1")
   # Get the database
   pedidos = mymongo.get_collection('Pedidos')
  
   print(pedidos)

   #if Cliente.select().where(Cliente.dni == dni_cliente_i).exists():

   item = {"precio_total": precio_total_i, "estado": estado_i, "fecha": str(fecha_obj_i), "canal_compra": canal_compra_i, "nro_pedido_compuesto": nro_pedido_compuesto_i, "dni_cliente": dni_cliente_i}

   print("itemmmm") 

   print(item)

   #mycollection.insert_one(item)

   pedidos.insert_one(item)
   print("hola2")
   
   '''''
   if nro_pedido_compuesto_i :
      pass
   else:
      print("hola")
     
      item = {"precio_total" : precio_total_i, "estado" : estado_i, "fecha" : fecha_obj_i, "canal_compra" : canal_compra_i, "nro_pedido_compuesto" : None, "dni_cliente" : dni_cliente_i }

      pedidos.insert_one(item)
   '''''


# This is added so that many files can reuse the function get_database()
if __name__ == '__main__':   

   mymongo = get_database()
   print("hola0")
   alta_pedido_simple_m(12345678,20,'pendiente', date.today(), 'web', 0)

#alta_pedido_simple_m(42, 547, "Hecho", 5748, 98765, 274) 

    #else:
    #    print ("Error: cliente no existe")

#def insertPedido(numPedido):
#   myPedido = {"numero": numPedido}
#   mycollection = mydatabase.Pedidos
#   mycollection.insert_many([myPedido])

#insertPedido(432)
#insertPedido(2)
   
