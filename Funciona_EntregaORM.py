
from datetime import date
import datetime 
import peewee


psql_db = peewee.PostgresqlDatabase('dbd2', host='localhost', port=8888,  user='dbd2g2', password='dbd2#G2')
#host='127.0.0.1'

nro_cuentas = 1

class Cliente(peewee.Model):
    dni = peewee.IntegerField(primary_key= True)
    nombre = peewee.CharField()
    apellido = peewee.CharField()
    mail = peewee.CharField()
    cel = peewee.IntegerField()
    calle = peewee.CharField()
    nro_puerta = peewee.CharField()
    apartamento = peewee.CharField()
    cod_postal = peewee.IntegerField()
    departamento = peewee.CharField()
    localidad = peewee.CharField()
    
    class Meta():
        database = psql_db
        db_table = 'cliente'
        schema = 'dbd2g2'
        psql_db.connect

class Cuenta(peewee.Model):
    nro_cuenta = peewee.IntegerField(primary_key=True)
    usuario = peewee.CharField(unique = True)
    dni = peewee.ForeignKeyField(Cliente, column_name = 'dni', to_field='dni')
    fecha_creacion = peewee.DateField()

    class Meta():
        database = psql_db
        db_table = 'cuenta'
        schema = 'dbd2g2'
        psql_db.connect

class Tarjeta(peewee.Model):
    numero=peewee.IntegerField(primary_key=True)
    banco=peewee.CharField()
    tipo=peewee.CharField()

    class Meta():
        database = psql_db
        db_table = 'tarjeta'
        schema = 'dbd2g2'
        psql_db.connect


class PedidoCompuesto(peewee.Model):
    id = peewee.IntegerField(primary_key=True)
    fecha = peewee.DateField()
    canal_compra = peewee.CharField()
    dni_cliente = peewee.ForeignKeyField(Cliente, column_name= 'dni_cliente', to_field='dni')

    class Meta():
        database = psql_db
        db_table = 'pedido_compuesto'
        schema = 'dbd2g2'
        psql_db.connect

class PedidoSimple(peewee.Model):
    id = peewee.AutoField()
    precio_total = peewee.FloatField()
    estado = peewee.CharField()
    fecha = peewee.DateField()
    canal_compra = peewee.CharField()
    nro_pedido_compuesto = peewee.ForeignKeyField(PedidoCompuesto, column_name = 'nro_pedido_compuesto', to_field='id', null=True)
    dni_cliente = peewee.ForeignKeyField(Cliente, column_name = 'dni_cliente', to_field='dni')

    class Meta():
        database = psql_db
        db_table = 'pedido_simple'
        schema = 'dbd2g2'
        psql_db.connect

class Cobro(peewee.Model):
    id_pedido = peewee.ForeignKeyField(PedidoSimple, column_name = 'id_pedido', to_field='id', primary_key=True)
    nro_cuenta = peewee.ForeignKeyField(Cuenta, column_name = 'nro_cuenta', to_field='nro_cuenta')
    aprobado = peewee.CharField()
    nro_aprobacion = peewee.IntegerField()

    class Meta():
        database = psql_db
        db_table = 'cobro'
        schema = 'dbd2g2'
        psql_db.connect


class Producto(peewee.Model):
    cod_prod = peewee.IntegerField(primary_key=True)
    nombre = peewee.CharField()
    precio = peewee.FloatField()
    stock = peewee.IntegerField()
    qr = peewee.BlobField()

    class Meta():
        database = psql_db
        db_table = 'producto'
        schema = 'dbd2g2'
        psql_db.connect

class ProductoPedido(peewee.Model):
    cod_producto = peewee.ForeignKeyField(Producto, column_name = 'cod_producto', to_field='cod_prod')
    id_pedido_simple = peewee.ForeignKeyField(PedidoSimple, column_name = 'id_pedido_simple', to_field='id')
    cantidad = peewee.IntegerField()

    class Meta:
        database = psql_db
        db_table = 'producto_pedido'
        schema = 'dbd2g2'
        psql_db.connect
        primary_key = peewee.CompositeKey('cod_prod','id_pedido_simple')


def alta_cliente(dni_cliente, nombre_cliente, apellido_cliente, mail_cliente, cel_cliente, calle_cliente, nro_puerta_cliente,
    apartamento_cliente, cod_postal_cliente, departamento_cliente, localidad_cliente, usuario_cuenta):
    
    if not Cliente.select().where(Cliente.dni == dni_cliente).exists():
        
        new_cliente = Cliente.create(dni = dni_cliente, nombre = nombre_cliente, apellido = apellido_cliente, mail = mail_cliente, cel = cel_cliente, calle = calle_cliente, 
        nro_puerta = nro_puerta_cliente, apartamento = apartamento_cliente, cod_postal = cod_postal_cliente, departamento = departamento_cliente, localidad = localidad_cliente)
        new_cliente.save()

    else:
        print ("Error: cliente ya existe")

    alta_cuenta(dni_cliente, usuario_cuenta)



def alta_cuenta(dni_cliente, usuario_cuenta):
    
    while Cuenta.select().where(Cuenta.usuario == usuario_cuenta).exists():
        print ("Nombre de usuario ya existe, elija otro: ")
        usuario_cuenta = input("Ingrese otro nombre de usuario: ")

    global nro_cuentas
    new_cuenta = Cuenta.create(dni = dni_cliente, nro_cuenta = nro_cuentas, usuario = usuario_cuenta, fecha_creacion = date.today())
    new_cuenta.save()
    nro_cuentas = nro_cuentas + 1

    
#modificacion cliente cuenta no

def baja_cliente(dni_cliente):

        if Cliente.select().where(Cliente.dni == dni_cliente).exists():
            cliente = Cliente.get(Cliente.dni == dni_cliente)
            cliente.delete_instance()


        else:
            print ("Error: cliente no existe")

        #hacer que se borre la cuenta tmb

def modificacion_cliente(dni_cliente, nombre_cliente, apellido_cliente, mail_cliente, cel_cliente, calle_cliente, nro_puerta_cliente, apartamento_cliente, cod_postal_cliente, departamento_cliente, localidad_cliente):

    if Cliente.select().where(Cliente.dni == dni_cliente).exists():
        if nombre_cliente: #si es true significa que no esta vacio el str
            query = Cliente.update(nombre = nombre_cliente).where(Cliente.dni == dni_cliente)
            query.execute()
        if apellido_cliente:
            query = Cliente.update(apellido = apellido_cliente).where(Cliente.dni == dni_cliente)
            query.execute()
        if mail_cliente:
            query =Cliente.update(mail = mail_cliente).where(Cliente.dni == dni_cliente)
            query.execute()
        if cel_cliente:
            query =Cliente.update(cel = int(cel_cliente)).where(Cliente.dni == dni_cliente)
            query.execute()
        if calle_cliente:
            query =Cliente.update(calle = calle_cliente).where(Cliente.dni == dni_cliente)
            query.execute()
        if nro_puerta_cliente:
            query =Cliente.update(nro_puerta = nro_puerta_cliente).where(Cliente.dni == dni_cliente)
            query.execute()
        if apartamento_cliente:
            query =Cliente.update(apartamento = apartamento_cliente).where(Cliente.dni == dni_cliente)
            query.execute()
        if cod_postal_cliente:
            query =Cliente.update(cod_postal = int(cod_postal_cliente)).where(Cliente.dni == dni_cliente)
            query.execute()
        if departamento_cliente:
            query =Cliente.update(departamento = departamento_cliente).where(Cliente.dni == dni_cliente)
            query.execute()
        if localidad_cliente:
            query =Cliente.update(localidad = localidad_cliente).where(Cliente.dni == dni_cliente)
            query.execute()

    else:
        print ("Error: cliente no existe")

def alta_pedido_simple(dni_cliente_i,precio_total_i,estado_i,fecha_obj_i, canal_compra_i,nro_pedido_compuesto_i):
    if Cliente.select().where(Cliente.dni == dni_cliente_i).exists():
        if nro_pedido_compuesto_i:
            new_pedido_s = PedidoSimple.create(precio_total = precio_total_i, estado = estado_i, fecha = fecha_obj_i, canal_compra = canal_compra_i, nro_pedido_compuesto = nro_pedido_compuesto_i, dni_cliente = dni_cliente_i)
            new_pedido_s.save()
        else:
            new_pedido_s = PedidoSimple.create(precio_total = precio_total_i, estado = estado_i, fecha = fecha_obj_i, canal_compra = canal_compra_i, nro_pedido_compuesto = None, dni_cliente = dni_cliente_i)
            new_pedido_s.save()


    else:
        print ("Error: cliente no existe")

    
'''
def baja_cliente_numero(numero):
    cliente=Cliente.get(Cliente.numero==numero)
    cliente.delete_instance()

def baja_cliente_nombre(nombre):
    cliente=Cliente.get(Cliente.nombre==nombre)
    cliente.delete_instance()

def baja_cliente_direccion(direccion):
    cliente=Cliente.get(Cliente.direccion==direccion)
    cliente.delete_instance()

def baja_cliente_telefono(telefono):
    cliente=Cliente.get(Cliente.telefono==telefono)
    cliente.delete_instance()

def baja_cliente_email(email):
    cliente=Cliente.get(Cliente.email==email)
    cliente.delete_instance()

def modificar_cliente_numero(numero,nuevo_numero,nuevo_nombre,nueva_direccion,nuevo_telefono,nuevo_email):
    qry=Cliente.update(numero=nuevo_numero,nombre=nuevo_nombre,direccion=nueva_direccion,telefono=nuevo_telefono,email=nuevo_email).where(Cliente.numero==numero)
    qry.execute()

def modificar_cliente_nombre(nombre,nuevo_numero,nuevo_nombre,nueva_direccion,nuevo_telefono,nuevo_email):
    qry=Cliente.update(numero=nuevo_numero,nombre=nuevo_nombre,direccion=nueva_direccion,telefono=nuevo_telefono,email=nuevo_email).where(Cliente.nombre==nombre)
    qry.execute()

def modificar_cliente_telefono(telefono,nuevo_numero,nuevo_nombre,nueva_direccion,nuevo_telefono,nuevo_email):
    qry=Cliente.update(numero=nuevo_numero,nombre=nuevo_nombre,direccion=nueva_direccion,telefono=nuevo_telefono,email=nuevo_email).where(Cliente.telefono==telefono)
    qry.execute()

def modificar_cliente_direccion(direccion,nuevo_numero,nuevo_nombre,nueva_direccion,nuevo_telefono,nuevo_email):
    qry=Cliente.update(numero=nuevo_numero,nombre=nuevo_nombre,direccion=nueva_direccion,telefono=nuevo_telefono,email=nuevo_email).where(Cliente.direccion==direccion)
    qry.execute()

def modificar_cliente_email(email,nuevo_numero,nuevo_nombre,nueva_direccion,nuevo_telefono,nuevo_email):
    qry=Cliente.update(numero=nuevo_numero,nombre=nuevo_nombre,direccion=nueva_direccion,telefono=nuevo_telefono,email=nuevo_email).where(Cliente.email==email)
    qry.execute()
'''

#def ingresar_pedido_simple(numero_pedido,numero_cuenta,numero_pago):


if __name__ == '__main__':

    if not Cliente.table_exists():
        Cliente.create_table()
        
    if not Cuenta.table_exists():
        Cuenta.create_table()

    if not Tarjeta.table_exists():
        Tarjeta.create_table()

    if not Cobro.table_exists():
        Cobro.create_table()

    if not PedidoSimple.table_exists():
        PedidoSimple.create_table()

    if not PedidoCompuesto.table_exists():
        PedidoCompuesto.create_table()

    if not Producto.table_exists():
        Producto.create_table()

    menu_principal = int(input ('Bienvenido/a: \n Opciones: \n 1. Alta de cliente \n 2. Baja de cliente \n 3. Modificación de cliente \n 4. Ingresar pedido simple \n 5. Ingresar pedido compuesto \n 6. Ingresar producto en stock \n 7. Registrar estado de pedido \n 8. Listado pedidos en estado (filtro fechas=?) \n 9. Listado productos en stock \n 10. Listado clientes \n 11. Listado pedidos en rango de fechas \n 12. Listado pedidos de cliente \n 13. Salir \n Ingrese una opción: '))

    if (menu_principal == 1):
        try:
            dni_cliente = int(input("Ingrese un dni: "))
            nombre_cliente = input("Ingrese un nombre: ")
            apellido_cliente = input("Ingrese un apellido: ")
            mail_cliente = input("Ingrese un mail: ")
            cel_cliente = int(input("Ingrese un celular: "))
            calle_cliente = input("Ingrese una calle: ")
            nro_puerta_cliente = input("Ingrese un numero de puerta, si lo tiene: ")
            apartamento_cliente = input("Si no es casa, ingrese apartamento: ")
            cod_postal_cliente = int(input("Ingrese un codigo postal: "))
            departamento_cliente = input("Ingrese un departamento: ")
            localidad_cliente = input("Ingrese una localidad: ")
            usuario_cuenta = input("Ingrese un nombre de usuario: ")
            alta_cliente(dni_cliente, nombre_cliente, apellido_cliente, mail_cliente, cel_cliente, calle_cliente, nro_puerta_cliente,
            apartamento_cliente, cod_postal_cliente, departamento_cliente, localidad_cliente, usuario_cuenta)
            print ('si')
        except:
            print("Alguno de los datos es inválido, vuelva a intentarlo")

    elif (menu_principal == 2):
        try:
            dni_cliente = int(input("Ingrese su dni: "))
            baja_cliente(dni_cliente)
            print('sisi')
        except:
            print("Alguno de los datos es inválido, vuelva a intentarlo")

    elif menu_principal==3:
        try:
            dni_cliente = int(input("Ingrese su dni: "))
            print ("Ingrese solo los datos que desea modificar: ")
            nombre_cliente = input("Nombre: ")
            apellido_cliente = input("Apellido: ")
            mail_cliente = input("Mail: ")
            cel_cliente = input("Celular: ")
            calle_cliente = input("Calle: ")
            nro_puerta_cliente = input("Numero de puerta: ")
            apartamento_cliente = input("Apartamento: ")
            cod_postal_cliente = input("Codigo postal: ")
            departamento_cliente = input("Departamento: ")
            localidad_cliente = input("Localidad: ")
            modificacion_cliente(dni_cliente, nombre_cliente, apellido_cliente, mail_cliente, cel_cliente, calle_cliente, nro_puerta_cliente, apartamento_cliente, cod_postal_cliente, departamento_cliente, localidad_cliente)
            print("ok 3")
        except:
            print("Alguno de los datos es inválido, vuelva a intentarlo")

    elif menu_principal==4:
        #try:
            dni_cliente_i = int(input("Ingrese el dni del cliente que lo realizó: "))
            precio_total_i = float(input("Ingrese el costo total: "))
            estado_i = input("Ingrese el estado en el que se encuentra: ")
            fecha = input("Ingrese la fecha en formato dd/mm/yyyy: ")
            fecha_obj_i = datetime.datetime.strptime(fecha, '%d/%m/%Y')
            canal_compra_i = input("Ingrese el canal de compra (movil/web): ")
            nro_pedido_compuesto_i = input("Ingrese el n° de pedido compuesto al que pertenece, si corresponde: ")
            alta_pedido_simple(dni_cliente_i,precio_total_i,estado_i,fecha_obj_i, canal_compra_i,nro_pedido_compuesto_i)
            print("ok 4")
        #except:
        #    print("Alguno de los datos es inválido, vuelva a intentarlo")


    else:
            pass
            



    #alta_cliente(12345678,'Agustina','Rivera 1234','094995507','agustina@mail.com')

    #modificar_cliente(12345678,87654321,'Belén','Av Italia 4321','095108089','belen@mail.com')

    #baja_cliente(87654321)

    """Crear rutinas que permitan:
− realizar el alta, baja y modificación de clientes 
pronto, solo falta error al crear cuenta
− ingresar pedidos simples y compuesto, controlando las restricciones definidas
− ingresar articulos en el stock
− registrar el pago o no de los pedidos

− Permitir listar
− los pedidos en un estado dato, permitiendo filtro por rango de fechas
− los productos en stock con su disponibilidad
− los clientes mostrando sus atributos
− los pedidos en un rango de fechas, mostrando además el cliente y estado
− los pedidos de un cliente"""