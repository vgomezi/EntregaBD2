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

   # Get the database
   pedidos = mymongo.get_collection('Pedidos')

   #if Cliente.select().where(Cliente.dni == dni_cliente_i).exists():

   if nro_pedido_compuesto_i:
      pedido_simple = {"precio_total": precio_total_i, "estado": estado_i, "fecha": str(fecha_obj_i), "canal_compra": canal_compra_i, "nro_pedido_compuesto": nro_pedido_compuesto_i, "dni_cliente": dni_cliente_i, "nro_pedido_compuesto": nro_pedido_compuesto_i}

      pedidos.insert_one(pedido_simple)
   else:     

      pedido_simple = {"precio_total": precio_total_i, "estado": estado_i, "fecha": str(fecha_obj_i), "canal_compra": canal_compra_i, "nro_pedido_compuesto": nro_pedido_compuesto_i, "dni_cliente": dni_cliente_i}

      pedidos.insert_one(pedido_simple)




if __name__ == '__main__':   

   mymongo = get_database()
   
   alta_pedido_simple_m(12345678,20,'pendiente', date.today(), 'web', 0)


