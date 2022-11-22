from datetime import date
from pymongo import MongoClient


def get_database():
 
#Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb://localhost:27017/"
 
#Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)

   mydatabase = client['mdbg2']
 
# Create the database for our example (we will use the same database throughout the tutorial
   return mydatabase


def alta_pedido_simple_m(dni_cliente_i, precio_total_i, estado_i, fecha_obj_i, canal_compra_i, nro_pedido_compuesto_i):

   pedidos = mymongo.get_collection('Pedidos')

   if nro_pedido_compuesto_i:
      pedido_simple = {"precio_total": precio_total_i, "estado": estado_i, "fecha": str(fecha_obj_i), "canal_compra": canal_compra_i, "nro_pedido_compuesto": nro_pedido_compuesto_i, "dni_cliente": dni_cliente_i}

      pedidos.insert_one(pedido_simple)

      print('se hizo el simple')

   else:     

      pedido_simple = {"precio_total": precio_total_i, "estado": estado_i, "fecha": str(fecha_obj_i), "canal_compra": canal_compra_i,"dni_cliente": dni_cliente_i}

      pedidos.insert_one(pedido_simple)

      print('se hizo el simple')


def alta_pedido_compuesto_m(fecha_obj_i, canal_compra_i, dni_cliente_i):

   pedidos = mymongo.get_collection('Pedidos')

   pedido_compuesto = {"fecha": str(fecha_obj_i), "canal_compra": canal_compra_i, "dni_cliente": dni_cliente_i}

   pedidos.insert_one(pedido_compuesto)

   print('se hizo el compuesto')


def buscar_pedido_simple_id_m(id_buscar):

   pedidos = mymongo.get_collection('Pedidos')

   cursor = pedidos.find(
      {'_id' : id_buscar},
      {'precio_total': 1,
      'estado': 1,
      'fecha': 1,
      'canal_compra': 1,
      'nro_pedido_compuesto':1,
      'dni_cliente': 1}
   )

   for rec in cursor:
      print(rec)
      print(rec['precio_total'])
      print(rec['estado'])
      print(rec['fecha'])
      print(rec["estado"])
      print(rec['canal_compra'])
      print(rec['nro_pedido_compuesto'])
      print(rec['dni_cliente'])

      #no sabmos por qué pero no entra al for




def buscar_pedido_compuesto_id_m(id_buscar):

   pedidos = mymongo.get_collection('Pedidos')

   cursor = pedidos.find(
      {'_id' : id_buscar},
      {'fecha': 1,
      'canal_compra': 1,
      'dni_cliente': 1}
   )

   for rec in cursor:
      print(rec)
      print(rec['fecha'])
      print(rec['canal_compra'])
      print(rec['dni_cliente'])


if __name__ == '__main__':   

   mymongo = get_database()
   
   alta_pedido_simple_m(54967202, 20,'pendiente', date.today(), 'web', None)
   alta_pedido_compuesto_m(date.today(), 'movil', 54967202)