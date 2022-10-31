

from datetime import date
import datetime 
import peewee


psql_db = peewee.PostgresqlDatabase('dbd2', host='localhost', port=8888,  user='dbd2g2', password='dbd2#G2')
#host='127.0.0.1'

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
    nro_cuenta = peewee.AutoField()
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
    id = peewee.AutoField()
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
    nro_aprobacion = peewee.AutoField()

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
    qr = peewee.BlobField(null=True)

    class Meta():
        database = psql_db
        db_table = 'producto'
        schema = 'dbd2g2'
        psql_db.connect


class ProductoPedido(peewee.Model):
    cod_prod = peewee.ForeignKeyField(Producto, column_name = 'cod_prod', to_field='cod_prod')
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

    new_cuenta = Cuenta.create(dni = dni_cliente, usuario = usuario_cuenta, fecha_creacion = date.today()) #nro cuentas no se lo pasamos porque lo autogenera
    new_cuenta.save()

#modificacion cliente cuenta no

def baja_cliente(dni_cliente):

        if Cliente.select().where(Cliente.dni == dni_cliente).exists():
            cliente = Cliente.get(Cliente.dni == dni_cliente)
            cliente.delete_instance()

        if Cuenta.select().where(Cuenta.dni == dni_cliente).exists():
            cuenta = Cuenta.get(Cuenta.dni == dni_cliente)
            cuenta.delete_instance()

        else:
            print ("Error: cliente no existe")


def modificacion_cliente(dni_cliente, nombre_cliente, apellido_cliente, mail_cliente, cel_cliente, calle_cliente, nro_puerta_cliente, apartamento_cliente, cod_postal_cliente, departamento_cliente, localidad_cliente):

    if Cliente.select().where(Cliente.dni == dni_cliente).exists():
        if nombre_cliente: #si es true significa que no esta vacio el str
            query = Cliente.update(nombre = nombre_cliente).where(Cliente.dni == dni_cliente)
            query.execute()
        if apellido_cliente:
            query = Cliente.update(apellido = apellido_cliente).where(Cliente.dni == dni_cliente)
            query.execute()
        if mail_cliente:
            query = Cliente.update(mail = mail_cliente).where(Cliente.dni == dni_cliente)
            query.execute()
        if cel_cliente:
            query = Cliente.update(cel = int(cel_cliente)).where(Cliente.dni == dni_cliente)
            query.execute()
        if calle_cliente:
            query = Cliente.update(calle = calle_cliente).where(Cliente.dni == dni_cliente)
            query.execute()
        if nro_puerta_cliente:
            query = Cliente.update(nro_puerta = nro_puerta_cliente).where(Cliente.dni == dni_cliente)
            query.execute()
        if apartamento_cliente:
            query = Cliente.update(apartamento = apartamento_cliente).where(Cliente.dni == dni_cliente)
            query.execute()
        if cod_postal_cliente:
            query = Cliente.update(cod_postal = int(cod_postal_cliente)).where(Cliente.dni == dni_cliente)
            query.execute()
        if departamento_cliente:
            query = Cliente.update(departamento = departamento_cliente).where(Cliente.dni == dni_cliente)
            query.execute()
        if localidad_cliente:
            query = Cliente.update(localidad = localidad_cliente).where(Cliente.dni == dni_cliente)
            query.execute()

    else:
        print ("Error: cliente no existe")


def alta_pedido_simple(dni_cliente_i, precio_total_i, estado_i, fecha_obj_i, canal_compra_i, nro_pedido_compuesto_i):

    if Cliente.select().where(Cliente.dni == dni_cliente_i).exists():
        if nro_pedido_compuesto_i:
            new_pedido_s = PedidoSimple.create(precio_total = precio_total_i, estado = estado_i, fecha = fecha_obj_i, canal_compra = canal_compra_i, nro_pedido_compuesto = nro_pedido_compuesto_i, dni_cliente = dni_cliente_i)
            new_pedido_s.save()
            return new_pedido_s.id
        else:
            new_pedido_s = PedidoSimple.create(precio_total = precio_total_i, estado = estado_i, fecha = fecha_obj_i, canal_compra = canal_compra_i, nro_pedido_compuesto = None, dni_cliente = dni_cliente_i)
            new_pedido_s.save()
            return new_pedido_s.id

    else:
        print ("Error: cliente no existe")


def alta_producto(cod_prod_i,nombre_i,precio_i,stock_i,qr_i):

    if qr_i:
        new_producto = Producto.create(cod_prod = cod_prod_i, nombre = nombre_i, precio = precio_i, stock = stock_i, qr = qr_i)
        new_producto.save()
    else:
        new_producto = Producto.create(cod_prod = cod_prod_i, nombre = nombre_i, precio = precio_i, stock = stock_i, qr= None)
        new_producto.save()
    

def alta_producto_pedido(id_generado,cod_prod1,cant1):
    
    new = ProductoPedido.create(id_pedido_simple = id_generado, cod_prod = cod_prod1, cantidad = cant1)
    new.save()


def alta_pedido_compuesto(fecha_obj_i, canal_compra_i, dni_cliente_i):

    if Cliente.select().where(Cliente.dni == dni_cliente_i).exists():
        new_pedido_c = PedidoCompuesto.create(fecha = fecha_obj_i, canal_compra = canal_compra_i, dni_cliente = dni_cliente_i)
        new_pedido_c.save()
    else:
        print ("Error: cliente no existe")
    

def actualizar_estado_pedido(id_pedido, estado_pedido):

    if PedidoSimple.select().where(PedidoSimple.id == id_pedido).exists():
        if estado_pedido: #si es true significa que no esta vacio el str
            query = PedidoSimple.update(estado_i = estado_pedido).where(PedidoSimple.id == id_pedido)
            query.execute()

    else:
        print ("Error: pedido no existe")


def listado_clientes():

    listClientes = []
    for i in Cliente.__sizeof__:
        listClientes.append(Cliente.get(i))
        i = i + 1
    
    print(listClientes)

    #con select recorrer las tuplas de cliente ir guardandolas e imprimir


def pago_pedido(id_generado, nro_cuenta, aprobado):
    
    Cobro.create(id_generado, nro_cuenta, aprobado)

    

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

    menu_principal = int(input ('Bienvenido/a: \n Opciones: \n 1. Alta de cliente \n 2. Baja de cliente \n 3. Modificación de cliente \n 4. Ingresar pedido simple \n 5. Ingresar pedido compuesto \n 6. Ingresar producto en stock \n 7. Actualizar estado del pedido \n 8. Listado pedidos en estado (filtro fechas=?) \n 9. Listado productos en stock \n 10. Listado clientes \n 11. Listado pedidos en rango de fechas \n 12. Listado pedidos de cliente \n 13. Salir \n Ingrese una opción: '))

    if menu_principal == 1:
        # Alta de cliente
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

    elif menu_principal == 2:
        # Baja de cliente
        try:
            dni_cliente = int(input("Ingrese su dni: "))
            baja_cliente(dni_cliente)
            print('sisi')
        except:
            print("Alguno de los datos es inválido, vuelva a intentarlo")

    elif menu_principal == 3:
        # Modificación de cliente
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

    elif menu_principal == 4:
        # Ingresar pedido simple
        try:
            dni_cliente_i = int(input("Ingrese el dni del cliente que lo realizó: "))
            precio_total_i = float(input("Ingrese el costo total: "))
            estado_i = input("Ingrese el estado en el que se encuentra: ")
            fecha = input("Ingrese la fecha en formato dd/mm/yyyy: ")
            fecha_obj_i = datetime.datetime.strptime(fecha, '%d/%m/%Y')
            canal_compra_i = input("Ingrese el canal de compra (movil/web): ")
            nro_pedido_compuesto_i = input("Ingrese el n° de pedido compuesto al que pertenece, si corresponde: ")

            cod_prod1 = int(input("Ingrese el codigo de barras del producto pedido: "))
            cant1 = int(input("Ingrese la cantidad (como máximo 20 unidades): "))

            if Producto.get_by_id(cod_prod1).stock < cant1:
                print("Error: la cantidad en stock no es suficiente para realizar el pedido")
            else:
                id_generado = alta_pedido_simple(dni_cliente_i,precio_total_i,estado_i,fecha_obj_i, canal_compra_i,nro_pedido_compuesto_i)

                alta_producto_pedido(id_generado,cod_prod1,cant1)

                cant_total = cant1

                while cant_total < 20:
                    respuesta = input("Desea ingresar otro producto? s/n: ")
                    if respuesta == 's':
                        cod_prod2 = int(input("Ingrese el codigo del producto pedido: "))
                        cant2 = int(input("Ingrese la cantidad (como máximo 20 unidades): "))

                        if Producto.get_by_id(cod_prod2).stock < cant2:
                            print("Error: la cantidad en stock no es suficiente para realizar el pedido")
                        else:
                            cant_total = cant_total + cant2
                            if cant_total <= 20:
                                alta_producto_pedido(id_generado, cod_prod2,cant2)
                            else:
                                print("Error: la cantidad total de productos no puede superar las 20 unidades")
                    if respuesta == 'n':
                        break
            
            nro_cuenta = int(input("Ingerse el numero de cuenta"))
            aprobado = input("Indique si el pedido esta aprobado s/n: ")
            if aprobado == 's':
                pago_pedido(id_generado, nro_cuenta, aprobado)
            else:
                print("El pago no fue aprobado")
            
            print("ok 4")

        except:
            print("Alguno de los datos es inválido, vuelva a intentarlo")

    elif menu_principal == 5:
        # Ingresar pedido compuesto
        try:
            dni_cliente_i = int(input('Ingrese el dni del cliente que lo realizó: '))
            fecha = input("Ingrese la fecha en formato dd/mm/yyyy: ")
            fecha_obj_i = datetime.datetime.strptime(fecha, '%d/%m/%Y')
            canal_compra_i = input("Ingrese el canal de compra (movil/web): ")
            alta_pedido_compuesto(fecha_obj_i, canal_compra_i, dni_cliente_i)
            print("ok 5")
        except:
            print("Alguno de los datos es inválido, vuelva a intentarlo")

    elif menu_principal == 6:
        # Ingresar producto en stock
        try:
            cod_prod_i = int(input("Ingrese el codigo de barras: "))
            nombre_i = input("Ingrese el nombre: ")
            precio_i = float(input("Ingrese el precio: "))
            stock_i = int(input("Ingrese la cantidad en stock: "))
            qr_i = input("Ingrese el qr: ") #como ingresarian el qr?
            alta_producto(cod_prod_i,nombre_i,precio_i,stock_i,qr_i)
            print("ok 6")
        except:
            print("Alguno de los datos es inválido, vuelva a intentarlo")

    elif menu_principal == 7:
        # Actualizar estado del pedido
        id_pedido = input("Ingrese el id del pedido: ")
        estado_pedido = input("Ingrese el estado en el que se encuentra el pedido: ")
        actualizar_estado_pedido(id_pedido, estado_pedido)
        print("ok 7")

    elif menu_principal == 8:
        # Listado pedidos en estado (filtro fechas=?) 
        print("ok 8")

    elif menu_principal == 9:
        # Listado productos en stock
        print("ok 9")

    elif menu_principal == 10:
        # Listado clientes 
        listado_clientes()
        print("ok 10")

    elif menu_principal == 11:
        # Listado pedidos en rango de fechas
        print("ok 11")

    elif menu_principal == 12:
        # Listado pedidos de cliente
        print("ok 12")

    elif menu_principal == 13:
        # Salir
        print("ok 13")

    else:
        print("La opción ingresada es inválida")
            




    """Crear rutinas que permitan:
− realizar el alta, baja y modificación de clientes 
pronto
− ingresar pedidos simples y compuesto, controlando las restricciones definidas
#al agregar un pedido tmb se agrega una instancia de producto pedido y (no se baja el stock de producto porque se baja cuando se paga)
− ingresar articulos en el stock
− registrar el pago o no de los pedidos (se actualiza el stock del producto segun la letra) dar opcion a registrar otros estados

− Permitir listar
− los pedidos en un estado dato, permitiendo filtro por rango de fechas
− los productos en stock con su disponibilidad
− los clientes mostrando sus atributos
− los pedidos en un rango de fechas, mostrando además el cliente y estado
− los pedidos de un cliente"""