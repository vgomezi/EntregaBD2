

from datetime import date
import datetime 
import peewee


psql_db = peewee.PostgresqlDatabase('dbd2', host='localhost', port=8888,  user='dbd2g2', password='dbd2#G2')
#host='127.0.0.1'

dbms_cursor = psql_db.cursor()


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
    nro_cuenta = peewee.AutoField(column_name= 'nro_cuenta')
    usuario = peewee.CharField(unique = True)
    dni = peewee.ForeignKeyField(Cliente, column_name = 'dni', to_field='dni')
    fecha_creacion = peewee.DateField()

    class Meta():
        database = psql_db
        db_table = 'cuenta'
        schema = 'dbd2g2'
        psql_db.connect

class Tarjeta(peewee.Model):
    tipo= peewee.CharField()
    nro_tarjeta=peewee.BigIntegerField(primary_key=True)
    fecha_vencimiento = peewee.DateField()
    emisor=peewee.CharField()
    nro_cuenta=peewee.ForeignKeyField(Cuenta, column_name = 'nro_cuenta', to_field='nro_cuenta')

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
    nro_aprobacion = peewee.IntegerField(null=True)

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
        print("Se creó el cliente")

    else:
        print ("Error: cliente ya existe")
        return -1

    nro_cuenta_generado = alta_cuenta(dni_cliente, usuario_cuenta)
    if not (Cuenta.select().where(Cuenta.nro_cuenta == nro_cuenta_generado).exists()):
        baja_cliente(dni_cliente)

    return nro_cuenta_generado



def alta_cuenta(dni_cliente, usuario_cuenta):
    
    while Cuenta.select().where(Cuenta.usuario == usuario_cuenta).exists():
        print ("Nombre de usuario ya existe, elija otro: ")
        usuario_cuenta = input("Ingrese otro nombre de usuario: ")

    new_cuenta = Cuenta.create(dni = dni_cliente, usuario = usuario_cuenta, fecha_creacion = date.today()) #nro cuentas no se lo pasamos porque lo autogenera
    new_cuenta.save()
    return new_cuenta.nro_cuenta


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
        return new_pedido_c.id
    else:
        print ("Error: cliente no existe")
    

def actualizar_estado_pedido(id_pedido, estado_pedido):

    if PedidoSimple.select().where(PedidoSimple.id == id_pedido).exists():
        if estado_pedido: #si es true significa que no esta vacio el str
            query = PedidoSimple.update(estado = estado_pedido).where(PedidoSimple.id == id_pedido)
            query.execute()

    else:
        print ("Error: pedido no existe")


def listado_clientes():
    consulta = 'SELECT nombre, apellido, dni, mail, cel , departamento, localidad, calle, cod_postal from CLIENTE'
    dbms_cursor.execute(consulta)
    rows = dbms_cursor.fetchall()
    
    contador = 1
    for i in rows:
        
        print("Cliente", contador, ":", "Nombre:", i[0], "- Apellido: ", i[1], "- DNI: ", i[2], "- Mail: ", i[3], "- Cel: ", i[4],
        "- Departamento: ", i[5], "- Localidad: ", i[6], "- Calle: ", i[7], "- Código Postal: ", i[8],)
        contador = contador + 1



def listado_stock():

    consulta = 'SELECT nombre, precio, stock, cod_prod, qr from PRODUCTO where stock > 0'
    dbms_cursor.execute(consulta)
    rows = dbms_cursor.fetchall()
    
    contador = 1
    for i in rows:
        
        print("Producto", contador, ":", "Nombre:", i[0], "- Precio: ", i[1], "- Stock: ", i[2], "- Código Producto: ", i[3], "- QR: ", i[4])
        contador = contador + 1


def listado_pedidos_en_estado(estado_i):
    consultaPEDIDOS = "SELECT id, precio_total, fecha, canal_compra, dni_cliente, nro_pedido_compuesto FROM pedido_simple WHERE estado = %s"
    dbms_cursor.execute(consultaPEDIDOS,[estado_i])
    rows = dbms_cursor.fetchall()
    
    print('Pedidos Simples \n')
    for i in rows:
        if i[5] is None:
            print("Id:", i[0], "- Costo:", i[1], "- Fecha:", i[2], "- Canal de compra:", i[3], '-DNI del cliente:', i[4], '-No pertenece a ningún pedido compuesto')
        else:
            print("Id:", i[0], "- Costo:", i[1], "- Fecha:", i[2], "- Canal de compra:", i[3], '-DNI del cliente:', i[4], '-Nro de pedido compuesto: ', i[5])

    print('Pedidos Compuestos \n')

    consulta2 = "SELECT id, fecha, canal_compra, dni_cliente FROM pedido_compuesto"
    dbms_cursor.execute(consulta2)
    compuestos = dbms_cursor.fetchall()

    for k in compuestos:
        contador_pendientes =0
        contador_rechazados =0
        costo_total = 0
        estado_compuesto = "ok"

        consulta3 = "SELECT id, estado, precio_total FROM pedido_simple WHERE nro_pedido_compuesto = %s "
        cantidad_total =dbms_cursor.execute(consulta3, [k[0]])
        simples_del_compuesto = dbms_cursor.fetchall()

        ya_imprimio = False

        for i in simples_del_compuesto:
            
            if (i[1] == "pendiente"):
                contador_pendientes = contador_pendientes +1
            elif (i[1] == "rechazado"):
                contador_rechazados = contador_rechazados +1

            costo_total = costo_total + i[2]

        if (contador_pendientes>0 and contador_rechazados ==0):
            estado_compuesto = "pendiente"
        elif (contador_rechazados >0):
            estado_compuesto = "rechazado"
        elif (contador_rechazados == 0 and contador_pendientes == 0):
            #estan aprobados y despachados todos
            estado_compuesto = 'aprobado'

            for j in simples_del_compuesto:
                actualizar_estado_pedido(j[0], "despachado")

            estado_compuesto = 'despachado'
        
        if (estado_compuesto == estado_i):
            print("Id:", k[0], "- Costo:", costo_total, "- Fecha:", k[1], "- Canal de compra:", k[2], "- DNI del cliente:", k[3], '- Estado:', estado_compuesto)
        ''''
elif (contador_rechazados>0 and contador_rechazados<cantidad_total):
            consulta = "SELECT id, from pedido_simple WHERE estado = 'rechazado'" 
            dbms_cursor.execute(consulta)
            rows = dbms_cursor.fetchall()
            
            for i in rows:
                aumentar_stock(i)
                
        

            ped = PedidoSimple.get(PedidoSimple.nro_pedido_compuesto == k[0] and PedidoSimple.estado == "rechazado")
            ped.delete_instance()
            #consulta4 = """DELETE FROM pedido_simple WHERE nro_pedido_compuesto = %s AND estado ='rechazado' ;"""
            #var =dbms_cursor.execute(consulta4, [compuestos[k][0]])
            #repito la consulta luego de que elimine los rechazados
            #print (var)
            contador_pendientes2 = 0
            costo_total2 = 0

            consulta5 = "SELECT id, estado, precio_total FROM pedido_simple WHERE nro_pedido_compuesto = %s "
            dbms_cursor.execute(consulta5, [k[0]])
            simples_del_compuesto2 = dbms_cursor.fetchall()

            for m in simples_del_compuesto2:
                if (m[1] == "pendiente"):
                    contador_pendientes2 = contador_pendientes2 +1

                costo_total2 = costo_total2 + m[2]

            if (contador_pendientes2>0):
                estado_compuesto2 = "pendiente"
            else: #no va a haber rechazados porque los elimine, y si no hay pendientes entonces estan aprobados todos y por lo tanto despachados
                estado_compuesto2 = "aprobado"
                for j in simples_del_compuesto2:
                    actualizar_estado_pedido(j[0], "despachado")
                estado_compuesto2 = "despachado"
            
            if (estado_compuesto == estado_i):
                print("Id:", k[0], "- Costo:", costo_total2, "- Fecha:", k[1], "- Canal de compra:", k[2], "- DNI del cliente:", k[3], '-Estado:', estado_compuesto2)

                ya_imprimio = True
                '''

        


def listado_pedidos_en_estado_con_fechas(estado_i,fecha_inicio_i, fecha_fin_i):
    #muestra los simples en ese rango y los compuestos en ese rango que tengan solo simples en ese rango.

    consultaPEDIDOS = "SELECT id, precio_total, fecha, canal_compra, dni_cliente, nro_pedido_compuesto FROM pedido_simple WHERE estado = %s AND fecha BETWEEN %s AND %s"
    dbms_cursor.execute(consultaPEDIDOS,[estado_i, fecha_inicio_i, fecha_fin_i])
    rows = dbms_cursor.fetchall()
    
    print('Pedidos Simples \n')
    for i in rows:
        if i[5] is None:
            print("Id:", i[0], "- Costo:", i[1], "- Fecha:", i[2], "- Canal de compra:", i[3], '-DNI del cliente:', i[4], '-No pertenece a ningún pedido compuesto')
        else:
            print("Id:", i[0], "- Costo:", i[1], "- Fecha:", i[2], "- Canal de compra:", i[3], '-DNI del cliente:', i[4], '-Nro de pedido compuesto: ', i[5])

    print('Pedidos Compuestos \n')

    consulta2 = "SELECT id, fecha, canal_compra, dni_cliente FROM pedido_compuesto WHERE fecha BETWEEN %s AND %s"
    dbms_cursor.execute(consulta2, [fecha_inicio_i, fecha_fin_i])
    compuestos = dbms_cursor.fetchall()

    for k in compuestos:
        contador_pendientes =0
        contador_rechazados =0
        costo_total = 0
        estado_compuesto = "ok"

        consulta3 = "SELECT id, estado, precio_total, fecha FROM pedido_simple WHERE nro_pedido_compuesto = %s"
        cantidad_total =dbms_cursor.execute(consulta3, [k[0]])
        simples_del_compuesto = dbms_cursor.fetchall()

        ya_imprimio = False
        simple_fuera_de_rango_fechas = False

        for i in simples_del_compuesto:

            if (not(i[3] <= fecha_fin_i and i[3] >= fecha_inicio_i)):
                simple_fuera_de_rango_fechas = True
            
            if (i[1] == "pendiente" and not simple_fuera_de_rango_fechas):
                contador_pendientes = contador_pendientes +1
            elif (i[1] == "rechazado" and not simple_fuera_de_rango_fechas):
                contador_rechazados = contador_rechazados +1
            
            if (not simple_fuera_de_rango_fechas):
                costo_total = costo_total + i[2]
        
        if (not(simple_fuera_de_rango_fechas)):
        
            if (contador_pendientes>0 and contador_rechazados ==0):
                estado_compuesto = "pendiente"
            elif (contador_rechazados == cantidad_total):
                estado_compuesto = "rechazado"
            elif (contador_rechazados>0 and contador_rechazados<cantidad_total):

                consulta = "SELECT id, from pedido_simple WHERE estado = 'rechazado'" 
                dbms_cursor.execute(consulta)
                rows = dbms_cursor.fetchall()
                
                for i in rows:
                    aumentar_stock(i)

                ped = PedidoSimple.get(PedidoSimple.nro_pedido_compuesto == k[0] and PedidoSimple.estado == "rechazado")
                ped.delete_instance()
                #consulta4 = """DELETE FROM pedido_simple WHERE nro_pedido_compuesto = %s AND estado ='rechazado' ;"""
                #var =dbms_cursor.execute(consulta4, [compuestos[k][0]])
                #repito la consulta luego de que elimine los rechazados
                #print (var)
                contador_pendientes2 = 0
                costo_total2 = 0

                consulta5 = "SELECT id, estado, precio_total, fecha FROM pedido_simple WHERE nro_pedido_compuesto = %s AND fecha BETWEEN %s AND %s "
                dbms_cursor.execute(consulta5, [k[0], fecha_inicio_i, fecha_fin_i])
                simples_del_compuesto2 = dbms_cursor.fetchall()

                simple_fuera_de_rango_fechas = False
                for m in simples_del_compuesto2:
                    if (not(m[3] <= fecha_fin_i and m[3] >= fecha_inicio_i)):
                        simple_fuera_de_rango_fechas = True

                    if (m[1] == "pendiente" and not simple_fuera_de_rango_fechas):
                        contador_pendientes2 = contador_pendientes2 +1

                    if (not simple_fuera_de_rango_fechas):
                        costo_total2 = costo_total2 + m[2]

                if (not(simple_fuera_de_rango_fechas)):
                    if (contador_pendientes2>0):
                        estado_compuesto2 = "pendiente"
                    else: #no va a haber rechazados porque los elimine, y si no hay pendientes entonces estan aprobados todos y por lo tanto despachados
                        estado_compuesto2 = "aprobado"
                        for j in simples_del_compuesto2:
                            actualizar_estado_pedido(j[0], "despachado")
                        estado_compuesto2 = "despachado"
                    
                    if (estado_compuesto == estado_i):
                        print("Id:", k[0], "- Costo:", costo_total2, "- Fecha:", k[1], "- Canal de compra:", k[2], "- DNI del cliente:", k[3], '-Estado:', estado_compuesto2)

                        ya_imprimio = True

            elif (contador_rechazados == 0 and contador_pendientes == 0):
                #estan aprobados y despachados todos
                estado_compuesto = 'aprobado'

                for j in simples_del_compuesto:
                    actualizar_estado_pedido(j[0], "despachado")

                estado_compuesto = 'despachado'
            
            if (not ya_imprimio and estado_compuesto == estado_i):
                print("Id:", k[0], "- Costo:", costo_total, "- Fecha:", k[1], "- Canal de compra:", k[2], "- DNI del cliente:", k[3], '- Estado:', estado_compuesto)




def pago_pedido(id_generado, nro_cuenta_i, aprobado_i):

    
    Cobro.create(id_pedido = id_generado, nro_cuenta = nro_cuenta_i, aprobado = aprobado_i)


def disminuir_stock(id_pedido):
     #con el id pedido voy a producto pedido, guardo la cantidad, y con cod_prod voy a producto y stock = stock - cantidad

    consulta_nueva = 'SELECT id_pedido_simple, cantidad, cod_prod FROM producto_pedido WHERE id_pedido_simple = %s '
    dbms_cursor.execute(consulta_nueva, [id_pedido])
    rows = dbms_cursor.fetchall()

    for i in rows:
        cant = i[1]
        codigo_producto = i[2]

        stock_anterior = Producto.get_by_id(codigo_producto).stock

        query = Producto.update(stock = stock_anterior - cant).where(Producto.cod_prod == codigo_producto)
        query.execute()


def aumentar_stock(id_pedido):
     #con el id pedido voy a producto pedido, guardo la cantidad, y con cod_prod voy a producto y stock = stock - cantidad
    consulta_nueva = 'SELECT id_pedido_simple, cantidad, cod_prod FROM producto_pedido WHERE id_pedido_simple = %s '
    dbms_cursor.execute(consulta_nueva, [id_pedido])
    rows = dbms_cursor.fetchall()

    for i in rows:
        cant = i[1]
        codigo_producto = i[2]
        stock_anterior = Producto.get_by_id(codigo_producto).stock

        query = Producto.update(stock = stock_anterior + cant).where(Producto.cod_prod == codigo_producto)
        query.execute()

    #instancia_prod_pedido = ProductoPedido.get(ProductoPedido.id_pedido_simple == id_pedido)
    #cant = instancia_prod_pedido.cantidad
    #codigo_producto = instancia_prod_pedido.cod_prod

    



def pedidos_cliente(dni): 

    if Cliente.select().where(Cliente.dni == dni).exists():
        consulta1 = 'SELECT C.nombre, C.dni, P.id, P.precio_total, P.estado, P.fecha, P.canal_compra, P.nro_pedido_compuesto from PEDIDO_SIMPLE AS P, CLIENTE AS C where C.dni = P.dni_cliente and C.dni = %s'
        dbms_cursor.execute(consulta1, [dni])
        rows = dbms_cursor.fetchall()

        nombre = Cliente.get_by_id(dni).nombre
        doc = Cliente.get_by_id(dni).dni
        print("\n Cliente:", nombre , "DNI:", doc , "\n")
        print("Simples \n")
        

        for i in rows:

            print("- Pedido ID: ", i[2], "- Precio Total: ", i[3], "- Estado Pedido: ", i[4], "- Fecha Pedido: ", i[5], "- Canal de Compra: ", i[6], "- Número de pedido compuesto: ", i[7])

        consulta2 = 'SELECT C.nombre, C.dni, P.id, P.fecha, P.canal_compra from PEDIDO_COMPUESTO AS P, CLIENTE AS C where C.dni = P.dni_cliente and C.dni = %s'
        dbms_cursor.execute(consulta2, [dni])
        rows = dbms_cursor.fetchall()

        print("Compuestos \n")
        
        for i in rows:
            
            print("- Pedido ID: ", i[2], "- Fecha Pedido: ", i[3], "- Canal de Compra: ", i[4])
    else:
        print("Error: el cliente ingresado no existe.")



def listado_pedido_fechas(fecha_inicio, fecha_fin):
    
    consulta1 = 'SELECT id, precio_total, estado, fecha, canal_compra, nro_pedido_compuesto, dni_cliente from PEDIDO_SIMPLE where fecha BETWEEN %s AND %s'
    variable1 = dbms_cursor.execute(consulta1, [fecha_inicio, fecha_fin])
    rows1 = dbms_cursor.fetchall()

    consulta2 = 'SELECT id, fecha, canal_compra, dni_cliente from PEDIDO_COMPUESTO where fecha BETWEEN %s AND %s'
    variable2 = dbms_cursor.execute(consulta2, [fecha_inicio, fecha_fin])
    rows2 = dbms_cursor.fetchall()
    
    print("\n Pedidos con fechas entre: ", fecha_inicio.date(), " y ", fecha_fin.date())


    if variable1 is None and variable2 is None:
        print('Entre las fechas establecidas no existen pedidos')

    else:
        if variable1 is None:
            print('\n No hay pedidos simples')

        else:
            print("Pedidos Simples \n")

            for i in rows1:
                
                print("- Pedido ID: ", i[0], "- Precio Total: ", i[1], 
                "- Estado Pedido: ", i[2], "- Fecha Pedido: ", i[3], "- Canal de Compra: ", i[4], "- Número de pedido compuesto: ", i[5], "- DNI Cliente:" , i[6])

        
        
        if variable2 is None:
            print('No hay pedidos compuestos')

        else:
            print("\n Pedidos Compuestos \n")

            for i in rows2:
                
                print("- Pedido ID: ", i[0], "- Fecha Pedido: ", i[1], "- Canal de Compra: ", i[2], "- DNI Cliente:" , i[3])


    
def menu_principal():

    try:
        menu = int(input ('\n Bienvenido/a: \n Opciones: \n 1. Alta de cliente \n 2. Baja de cliente \n 3. Modificación de cliente \n 4. Ingresar pedido simple \n 5. Ingresar pedido compuesto \n 6. Ingresar producto \n 7. Actualizar estado del cobro de un pedido \n 8. Actualizar estado de un pedido \n 9. Listado de productos en stock  \n 10. Listado de clientes \n 11. Listado de pedidos en un estado dado (opcional: en un rango de fechas) \n 12. Listado de pedidos en rango de fechas \n 13. Listado de pedidos de un cliente \n 14. Salir \n Ingrese una opción: '))
    
    
        if menu == 1:
            menu1()

        elif menu == 2:
            menu2()

        elif menu == 3:
            menu3()

        elif menu == 4:
            menu4()

        elif menu == 5:
            menu5()

        elif menu == 6:
            menu6()

        elif menu == 7:
            menu7()

        elif menu == 8:
            menu8()

        elif menu == 9:
            menu9()

        elif menu == 10:
            menu10()

        elif menu == 11:
            menu11()

        elif menu == 12:
            menu12()

        elif menu == 13:
            menu13()

        elif menu == 14:
            menu14()

        else:
            print('Opción inválida')
    

        

    except:
        print('Error')


def menu1():
    # Alta de cliente

    try:
        dni_cliente = int(input("Ingrese un dni (sin puntos ni guiones): "))
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
        nro_cuenta_generado = alta_cliente(dni_cliente, nombre_cliente, apellido_cliente, mail_cliente, cel_cliente, calle_cliente, nro_puerta_cliente,
        apartamento_cliente, cod_postal_cliente, departamento_cliente, localidad_cliente, usuario_cuenta)

        print("  ")
        
        if nro_cuenta_generado != -1: #si es -1 es que no se creo el cliente pq ya existia
            numero_tarjeta = int(input("Ingrese el numero de la tarjeta: "))
            banco_tarjeta = input("Ingrese el banco de la tarjeta: ")
            tipo_tajeta = input("Ingrese d si el tipo de tarjeta es débito o c si es crédito: ")

            if tipo_tajeta == 'c':
                tipo_tajeta_real = 'crédito'
            elif tipo_tajeta == 'd':
                tipo_tajeta_real = 'débito'
            else:
                int ('mal')

            fecha_vencimiento_t = input('Ingrese la fecha de vencimiento, en formato dd/mm/yyyy: ')
            fecha_vencimiento_tarjeta = datetime.datetime.strptime(fecha_vencimiento_t, '%d/%m/%Y')
            if(fecha_vencimiento_tarjeta.date() > date.today()):
                Tarjeta.create(nro_tarjeta = numero_tarjeta, tipo= tipo_tajeta_real, fecha_vencimiento = fecha_vencimiento_tarjeta, emisor= banco_tarjeta, nro_cuenta = nro_cuenta_generado)
                print("Se creó la tarjeta")
            else:
                print("Tarjeta vencida")

        menu_principal()

    except:
        print("Alguno de los datos es inválido, vuelva a intentarlo")


def menu2():
    # Baja de cliente
    
    try:
        dni_cliente = int(input("Ingrese su dni: "))
        baja_cliente(dni_cliente)

        menu_principal()

    except:
        print("Alguno de los datos es inválido, vuelva a intentarlo")


def menu3():
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

        menu_principal()

    except:
        print("Alguno de los datos es inválido, vuelva a intentarlo")


def menu4():
    # Ingresar pedido simple
    
    #try:
        dni_cliente_i = int(input("Ingrese el dni del cliente que lo realizó: "))
        precio_total_i = float(input("Ingrese el costo total: "))
        estado_i = 'pendiente'
        fecha_i = input("Ingrese la fecha en formato dd/mm/yyyy: ")
        fecha_obj_i = datetime.datetime.strptime(fecha_i, '%d/%m/%Y')
        
        canal_compra_i = input("Ingrese w si el canal de compra es web o m si es móvil: ")

        if canal_compra_i == 'w':
            canal_compra_real = 'web'
        elif canal_compra_i == 'm':
            canal_compra_real = 'móvil'
        else:
            int ('mal')

        nro_pedido_compuesto_i = input("Ingrese el n° de pedido compuesto al que pertenece, si corresponde: ")
        
        if nro_pedido_compuesto_i:
            if PedidoCompuesto.select().where(PedidoCompuesto.id == nro_pedido_compuesto_i).exists():

                var = PedidoCompuesto.get_by_id(nro_pedido_compuesto_i)
                if  var.dni_cliente.dni == dni_cliente_i:
                    
                    cod_prod1 = int(input("Ingrese el codigo de barras del producto pedido: "))
                    cant1 = int(input("Ingrese la cantidad (como máximo 20 unidades): "))

                    if Producto.get_by_id(cod_prod1).stock < cant1:
                        print("Error: la cantidad en stock no es suficiente para realizar el pedido")
                    else:
                        id_generado = alta_pedido_simple(dni_cliente_i,precio_total_i,estado_i,fecha_obj_i, canal_compra_real,nro_pedido_compuesto_i)

                        alta_producto_pedido(id_generado,cod_prod1,cant1)

                        cant_total = cant1

                        while cant_total < 20:
                            respuesta = input("Desea ingresar otro producto? si/no: ")
                            if respuesta == 'si':
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
                            if respuesta == 'no':
                                break
                            
                else:
                    print ("Error: el dni ingresado no coincide con el del pedido compuesto.")
            else:
                print ("Error: el número ingresado de pedido compuesto no existe.")
        else: #no es de un compuesto
            cod_prod1 = int(input("Ingrese el codigo de barras del producto pedido: "))
            cant1 = int(input("Ingrese la cantidad (como máximo 20 unidades): "))

            if Producto.get_by_id(cod_prod1).stock < cant1:
                print("Error: la cantidad en stock no es suficiente para realizar el pedido")
            else:
                id_generado = alta_pedido_simple(dni_cliente_i,precio_total_i,estado_i,fecha_obj_i, canal_compra_i,nro_pedido_compuesto_i)

                alta_producto_pedido(id_generado,cod_prod1,cant1)

                cant_total = cant1

                while cant_total < 20:
                    respuesta = input("Desea ingresar otro producto? si/no: ")
                    if respuesta == 'si':
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
                    if respuesta == 'no':
                        break

        menu_principal()
            
    #except:
    #   print("Alguno de los datos es inválido, vuelva a intentarlo")


def menu5():
    # Ingresar pedido compuesto

    try:
        dni_cliente_i = int(input('Ingrese el dni del cliente que lo realizó: '))
        fecha = input("Ingrese la fecha en formato dd/mm/yyyy: ")
        fecha_obj_i = datetime.datetime.strptime(fecha, '%d/%m/%Y')
        canal_compra_i = input("Ingrese w si el canal de compra es web o m si es móvil: ")

        if canal_compra_i == 'w':
            canal_compra_real = 'web'
        elif canal_compra_i == 'm':
            canal_compra_real = 'móvil'
        else:
            int ('mal')

        id_generado = alta_pedido_compuesto(fecha_obj_i, canal_compra_real, dni_cliente_i)

        id1 = int(input("Ingrese el id del primer pedido simple: "))
        if PedidoSimple.get_by_id(id1) != None :
            query =PedidoSimple.update(nro_pedido_compuesto = id_generado).where(PedidoSimple.id==id1)
            query.execute()
        else:
            print('Error: el id ingresado no existe.')
        
        id2= int(input("Ingrese el id del segundo pedido simple: "))
        if PedidoSimple.get_by_id(id2) != None:
            query =PedidoSimple.update(nro_pedido_compuesto = id_generado).where(PedidoSimple.id==id2)
            query.execute()
        else:
            print('Error: el id ingresado no existe.')

        respuesta = input("Desea agregar otro pedido simple? si/no: ")
        while respuesta == 'si':
            id_nuevo = int(input("Ingrese el id del pedido simple: "))
            if PedidoSimple.get_by_id(id_nuevo) != None:
                query = PedidoSimple.update(nro_pedido_compuesto = id_generado).where(PedidoSimple.id==id_nuevo)
                query.execute()
            else:
                print('Error: el id ingresado no existe.')

            respuesta = input("Desea agregar otro pedido simple? si/no: ")
        
        menu_principal()

    except:
        print("Alguno de los datos es inválido, vuelva a intentarlo")


def menu6():
    # Ingresar producto en stock

    try:
        cod_prod_i = int(input("Ingrese el codigo de barras: "))
        nombre_i = input("Ingrese el nombre: ")
        precio_i = float(input("Ingrese el precio: "))
        stock_i = int(input("Ingrese la cantidad en stock: "))
        qr_i = input("Ingrese el qr: ") #como ingresarian el qr?
        alta_producto(cod_prod_i,nombre_i,precio_i,stock_i,qr_i)
        
        menu_principal()

    except:
        print("Alguno de los datos es inválido, vuelva a intentarlo")


def menu7():
    # Registrar estado del cobro

    try:
        id_pedido_i = input ("Ingrese el id del pedido: ")
        if PedidoSimple.select().where(PedidoSimple.id == id_pedido_i).exists():
            estado_actual = PedidoSimple.select(PedidoSimple.estado).where(PedidoSimple.id == id_pedido_i)
            dni_cliente_i = PedidoSimple.select(PedidoSimple.dni_cliente).where(PedidoSimple.id == id_pedido_i)
            nro_cuenta = Cuenta.get(Cuenta.dni == dni_cliente_i).nro_cuenta
            se_aprobo = input("Indique si el cobro esta aprobado (si/no): ")
            if se_aprobo == 'si':
                if (estado_actual != "aprobado"):
                    pago_pedido(id_pedido_i, nro_cuenta, se_aprobo)
                    query = PedidoSimple.update(estado = 'aprobado').where(PedidoSimple.id == id_pedido_i)
                    query.execute()
                    disminuir_stock(id_pedido_i)
                else:
                    print("El cobro ya se encontraba aprobado.")

            else:
                if (estado_actual != "rechazado"):
                    pago_pedido(id_pedido_i, nro_cuenta, se_aprobo)
                    query = PedidoSimple.update(estado = 'rechazado').where(PedidoSimple.id == id_pedido_i)
                    query.execute()
                    aumentar_stock(id_pedido_i)
                    print("El pago no fue aprobado")
                else: 
                    print( "El cobro ya se encontraba rechazado.")
        else:
            print ("Error: el pedido ingresado no existe")

        menu_principal()

    except:
        print("Alguno de los datos es inválido, vuelva a intentarlo")
    

def menu8():
    # Actualizar estado del pedido
    try:
        id_pedido = input("Ingrese el id del pedido: ")
        opcion = int(input("Elija el estado en el que se encuentra el pedido: \n 1- pendiente \n 2- aprobado \n 3- rechazado \n 4- despachado \n 5- entregado \n"))
        if (opcion == 1):
            actualizar_estado_pedido(id_pedido, "pendiente")
        elif (opcion ==2):
            actualizar_estado_pedido(id_pedido, "aprobado")
        elif (opcion ==3):
            actualizar_estado_pedido(id_pedido, "rechazado")
        elif (opcion ==4):
            actualizar_estado_pedido(id_pedido, "despachado")
        elif (opcion ==5):
            actualizar_estado_pedido(id_pedido, "entregado")
        else:
            print("La opción ingresada no es válida.")

        menu_principal()
        
    except:
        print("Error: alguno de los datos ingresados es inválido, intentelo de nuevo.")


def menu9():
    # Listado de productos en stock

    listado_stock()


def menu10():
    # Listado de clientes

    listado_clientes()
    

def menu11():
    # Listado de pedidos en un estado dado 

    r = input("¿Desea filtrar por rango de fechas? si/no: ")
    if r=="si":
        fecha_inicio = input("Ingrese la fecha inicio en formato dd/mm/yyyy: ")
        fecha_fin = input("Ingrese la fecha fin en formato dd/mm/yyyy: ")

        fecha_inicio_i = datetime.datetime.strptime(fecha_inicio, '%d/%m/%Y')
        fecha_fin_i = datetime.datetime.strptime(fecha_fin, '%d/%m/%Y')
            
        if (fecha_inicio_i >= fecha_fin_i):
            print('Error: Fecha inicio mayor o igual que fecha fin')

        else:
            estado_i = input('Ingrese el estado (pendiente/aprobado/rechazado/despachado/entregado): ')
            
            listado_pedidos_en_estado_con_fechas(estado_i,fecha_inicio_i.date(), fecha_fin_i.date())
    elif r=="no":
        estado_i = input('Ingrese el estado (pendiente/aprobado/rechazado/despachado/entregado): ')
        listado_pedidos_en_estado(estado_i)

    

def menu12():

    # Listado de pedidos en rango de fechas (se muestra cliente, no estado porque es lo mismo que se puede ver en la opcion 11)
    
    fecha_inicio = input("Ingrese la fecha inicio en formato dd/mm/yyyy: ")
    fecha_fin = input("Ingrese la fecha fin en formato dd/mm/yyyy: ")

    fecha_inicio_i = datetime.datetime.strptime(fecha_inicio, '%d/%m/%Y')
    fecha_fin_i = datetime.datetime.strptime(fecha_fin, '%d/%m/%Y')
        
    if (fecha_inicio_i >= fecha_fin_i):
        print('Error: Fecha inicio mayor o igual que fecha fin')

    else:
        listado_pedido_fechas(fecha_inicio = fecha_inicio_i, fecha_fin = fecha_fin_i)

    #no funciona


def menu13():

    # Listado de pedidos de un cliente 

    dni = int(input("Ingrese el dni del cliente para listar sus pedidos: "))
    pedidos_cliente(dni)


def menu14():

    # Salir

    exit()
  


'''
disminuir el stock una vez que se haya entregado el pedido (pq si es confirmado y luego se devuelve 
porque el compuesto se cancela se tendria que aumentar el stock)
'''

    
    
'''''

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

    menu_principal()

'''''