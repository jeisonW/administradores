import base64
import datetime
import pyodbc #modulo para conectar base de datos
from flask_paginate import Pagination, get_page_parameter
from werkzeug.security import generate_password_hash , check_password_hash
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from helper import  *
from flask_mail import Mail, Message
from itsdangerous import SignatureExpired, URLSafeTimedSerializer, BadSignature

app = Flask(__name__)
app.debug = True

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#configuracion mail
app.config["MAIL_DEFAULT_SENDER"] = 'jeiwebst.9@gmail.com'
app.config["MAIL_PASSWORD"] ='bfyqbmzadmixpmds'
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com" or "smtp.office365.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = 'jeiwebst.9@gmail.com'

mail = Mail(app)

s = URLSafeTimedSerializer('Thisisasecret!')

try:##verificar que no haya ningun error al conectarse con la BF
    conexion =  pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=JEISON\SQLEXPRESS;DATABASE=sistemaKD;Trusted_Connection=yes;')
    #conexion =  pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-QUNO8C9;DATABASE=CopiaSystemKD;Trusted_Connection=yes;')
except:
    print("FAIL")

cursor = conexion.cursor()

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        query = "select * from Usuarios where nombre = ?"
        rows = cursor.execute(query, (request.form.get("username")))
        rows = cursor.fetchall()


        #if len(rows) == 0 or not (rows[0][2] ==  request.form.get("password")):
        #    return render_template("login.html" , error_message="Nombre de usuario o contraseña incorrecta")
        if not rows:
            return render_template("login.html" , error_message="Nombre de usuario o contraseña incorrecta")
        if not check_password_hash(rows[0][2] , request.form.get("password")):
            return render_template("login.html" , error_message="Nombre de usuario o contraseña incorrecta")
        else:
            sql = "select estado from Permisos join Usuarios on Permisos.usuario_id = Usuarios.id where usuarios.nombre = ? "
            cursor.execute(sql, (request.form.get("username"),))
            permisos = [row[0] for row in cursor.fetchall()]
            
            if  permisos[0] == 1 :
                session["permisoempleado"] = permisos[0]
            if  permisos[1] == 1:
                session["permisoproveedores"] = permisos[1]
            if permisos[2] == 1:
                session["permisoventa"] = permisos[2]
            if permisos[3] == 1:
                session["permisocompra"] = permisos[3]
            if permisos[4] == 1:
                session["permisodesperfecto"] = permisos[4]
            if permisos[5] == 1:
                session["permisoproducto"] = permisos[5]

            session["user_id"] = rows

            return redirect("/")    

    else : 
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':

        query = "select * from Usuarios where nombre = ?"
        rows = cursor.execute(query, (request.form.get("nombre")))
        rows = cursor.fetchone()

        if rows :
            if len(rows) > 0 :
                session['registro_errado'] = '¡Registro Fallido!'
                return  redirect('/edituser')
            
        query = "select * from Usuarios where correo = ?"
        rows = cursor.execute(query, (request.form.get("correo")))
        rows = cursor.fetchone()
        if rows :
            if len(rows) > 0 :
                session['registro_errado'] = '¡Registro Fallido!'

                return  redirect('/edituser')
            

        sql = "insert into usuarios (nombre,contraseña,correo) VALUES (?,?,?)"
        cursor.execute(sql, ( request.form.get("nombre") , generate_password_hash(request.form.get("contraseña")) , request.form.get("correo")))
        cursor.commit()

        cursor.execute("SELECT MAX(id) FROM Usuarios")
        last_id= cursor.fetchone()[0]


        sql = "INSERT INTO Permisos (usuario_id, nombre, estado) VALUES (?, 'empleados', 0), (?, 'proveedores', 0), (?, 'ventas', 0), (?, 'compras', 0), (?, 'desperfectos', 0), (?, 'productos', 0)"
        cursor.execute(sql , (last_id,last_id,last_id,last_id,last_id,last_id))
        cursor.commit()

        session['mensaje_exitoso'] = '¡Registro exitoso!'


        return redirect('/edituser')
   

@app.route('/search')
def search():
    try:

        resultados_dict = {}
        query = request.args.get("q")
        cursor.execute("SELECT * FROM Usuarios WHERE contraseña = ?", (query,))
        resultados = cursor.fetchall()

        # Convertir resultados a una lista de diccionarios
        resultados_dict = [{'id': row[0], 'nombre': row[1]} for row in resultados]

        # Enviar resultados como JSON
        return jsonify(resultados_dict)
    except Exception as e:
        print('Error en el servidor:', str(e))

        # Enviar un código de estado 500 (Internal Server Error) en caso de error
        return jsonify({'error': 'Error interno del servidor'}), 500

#toda esta ruta es nueva 
@app.route("/edituser" , methods=["GET", "POST"])
def edit():
    if session["user_id"][0][1] != 'admin':
        return redirect("/")
    if request.method == "POST":
        id = request.form.get('user')
        contraseña = request.form.get('contraseña')
        correo = request.form.get('correo')
        if request.form.get('user') == '1':
            sql = "update Usuarios set contraseña = ? , correo = ? where id = ?"
            cursor.execute(sql,  request.form.get('contraseña') ,request.form.get('correo'),  request.form.get('user'))
            cursor.commit()

        else:
            sql = "update Usuarios set contraseña = ? where id = ?"
            cursor.execute(sql,  request.form.get('contraseña') , request.form.get('user'))
            cursor.commit()

        
        return redirect("/edituser")
    else:
        sql = "select * from Usuarios"
        cursor.execute(sql)
        registro = cursor.fetchall()

        registro_errado = session.pop('registro_errado', None)

        mensaje_exitoso = session.pop('mensaje_exitoso', None)
        #if not mensaje_exitoso:
        #    return render_template("edituser.html" , registro = registro )
        
        delete_user = session.pop('delete_user', None)
        #if not delete_user:
        #    return render_template("edituser.html" , registro = registro  )
      
        return render_template("edituser.html" , registro = registro , message = mensaje_exitoso ,deleteuser = delete_user , registro_errado = registro_errado )

@app.route("/eliminaruser" , methods=["GET", "POST" ])
def eliminaruser():
    if session["user_id"][0][1] != 'admin':
        return redirect("/")
    
    sql = "delete from Permisos where usuario_id = ?"
    cursor.execute(sql , request.form.get("idhiddenform") )
    cursor.commit()

    sql = "delete from Usuarios where id = ?"
    print(request.form.get("idhiddenform"))
    cursor.execute(sql , request.form.get("idhiddenform") )
    cursor.commit()
    session['delete_user'] = 'Usuario Inhabilitado!'

    return redirect("/edituser")

@app.route("/empleado" , methods=["GET", "POST"])
@login_required
@permisoempleado_required
def empleado():
    sql = "SELECT * FROM Empleado WHERE ESTADO = 'si'"
    cursor.execute(sql)
    registro = cursor.fetchall()
    empleado = session.pop('delete_empleado', None)
    add_empleado = session.pop('add_empleado', None)

    return render_template("empleado.html" , datos = registro , mensaje = empleado , add_empleado = add_empleado)

@app.route("/addempleado" , methods=["GET", "POST"])
@permisoempleado_required
@login_required
def addempleado():
    
    if request.method == "POST":
        if not request.form.get("correo").endswith('@gmail.com') and not request.form.get("correo").endswith('@hotmail.com'):#validar que es admitido
            return render_template("nuevoproveedor.html" , error = "correo invalido")   
                   
        sql = "insert into Empleado (NombreEmpleado,Correo,Telefono,Dirreccion,salario,ESTADO) VALUES (?,?,?,?,?,'si')"
        cursor.execute(sql , (request.form.get("nombre") , request.form.get("correo") , request.form.get("telefono") , request.form.get("direccion") , request.form.get("salario")))
        conexion.commit() 
        session['add_empleado'] = 'Empleado Registrado!'

        return redirect("/empleado")
 

@app.route("/eliminarempleado" , methods=["GET", "POST" ])
@login_required
@permisoempleado_required
def eliminarempleado():
    id = request.form.get("idhiddenform")
    sql = "update Empleado set ESTADO = 'no' where IDempleado = ?"
    cursor.execute(sql , (id))
    cursor.commit()
    session['delete_empleado'] = 'Empleado Eliminado!'
    return redirect("/empleado")


@app.route("/productos" , methods=["GET" , "POST"])
@login_required
@permisoproducto
def prueba():
        if request.method == 'POST':
            textobuscar = request.form.get('buscar')
            print(textobuscar)
            if textobuscar == '':
                sql = "select * from Producto where ESTADO = 'si'"
                cursor.execute(sql)
                resultados = cursor.fetchall()
            else:
                if textobuscar[0].isalpha():
                    sql = "SELECT * FROM Producto WHERE (NombreProducto LIKE ? OR CodigoProducto LIKE ?) AND ESTADO = 'si'"
                    cursor.execute(sql, ('%' + textobuscar + '%', '%' + textobuscar + '%'))
                    resultados = cursor.fetchall()
                else:
                    sql = "SELECT * FROM Producto WHERE (PrecioProducto = ? OR Stock = ?) AND ESTADO = 'si'"
                    cursor.execute(sql, (textobuscar, textobuscar))
                    resultados = cursor.fetchall()


            #if filtro and textobuscar:
            #    sql = "select * from Producto join Marca on Producto.CodigoProducto = Marca.CodigoProducto where Producto.ESTADO = 'si' and NombreMarca = ? AND NombreProducto like ? "
            #    resultados =cursor.execute(sql , (filtro,textobuscar))
            #    resultados = cursor.fetchall()
            #    print('vvv')


           #esto es solo para que se muestre el filtro 
            rows = "select distinct(NombreMarca) from Producto join Marca on Producto.CodigoProducto = Marca.CodigoProducto"
            cursor.execute(rows)
            filtro = cursor.fetchall()

            # Paginar los resultados
            page = request.args.get(get_page_parameter(), type=int, default=1)
            per_page = 12 # Cambia aquí el número de resultados por página que desees mostrar
            offset = (page - 1) * per_page
            productos_paginados = resultados[offset: offset + per_page]
            text = []
            for row in productos_paginados:
                id = row[0]
                imagens = row[5]
                nombre = row[1]
                precio = row[2]
                stock = row[3]
                if imagens is None:
                    text.append({'id': id , 'imagen': 'https://static.vecteezy.com/system/resources/previews/005/337/799/non_2x/icon-image-not-found-free-vector.jpg', 'nombre':nombre , 'precio':precio , 'stock' : stock})
                else:
                    imagen_base64 = base64.b64encode(imagens).decode('utf-8')
                    text.append({'id': id , 'imagen':    'data:image/png;base64,' + imagen_base64, 'nombre':nombre , 'precio':precio , 'stock' : stock})
            pagination = Pagination(page=page, total=len(resultados), css_framework='bootstrap4', per_page=per_page)
            

            # Renderizar la plantilla con los resultados paginados y la paginación
            return render_template('productos.html', prueba=text, pagination=pagination , filtro= filtro)
        else:
            #para mostrar todos los productos
            sql = "select *  from Producto where ESTADO = 'si'"
            resultados =cursor.execute(sql)
            resultados = cursor.fetchall()
            #esto es solo para que se muestre el filtro 
            rows = "select distinct(NombreMarca) from Producto join Marca on Producto.CodigoProducto = Marca.CodigoProducto"
            cursor.execute(rows)
            filtro = cursor.fetchall()

            # Paginar los resultados
            page = request.args.get(get_page_parameter(), type=int, default=1)
            per_page = 12 # Cambia aquí el número de resultados por página que desees mostrar
            offset = (page - 1) * per_page
            productos_paginados = resultados[offset: offset + per_page]
            text = []
            for row in productos_paginados:
                id = row[0]
                imagens = row[5]
                nombre = row[1]
                precio = row[2]
                stock = row[3]
                if imagens is None:
                    text.append({'id': id , 'imagen': 'https://static.vecteezy.com/system/resources/previews/005/337/799/non_2x/icon-image-not-found-free-vector.jpg', 'nombre':nombre , 'precio':precio , 'stock' : stock})
                else:
                    imagen_base64 = base64.b64encode(imagens).decode('utf-8')
                    text.append({'id': id , 'imagen': 'data:image/png;base64,' + imagen_base64, 'nombre':nombre , 'precio':precio , 'stock' : stock})
            pagination = Pagination(page=page, total=len(resultados), css_framework='bootstrap4', per_page=per_page)

            # Renderizar la plantilla con los resultados paginados y la paginación
            return render_template('productos.html', prueba=text, pagination=pagination , filtro= filtro)

@app.route('/verdetalles_productos/<string:id_product>')
def verdetalles_productos(id_product):
    print(id_product)
    cursor.execute("select * from ColoryTalla where CodigoProducto = ? and Stock > 0", (id_product,))
    detalles = cursor.fetchall()
    print(detalles)
    desgloce = []
    for detalle in detalles:
        detalle_dict = {
            'Talla'	:detalle[2],
            'ColorProducto'	:detalle[3],
            'Stock':detalle[4]

        }
        desgloce.append(detalle_dict)
    print(desgloce)

    return desgloce

@app.route("/compras" , methods=["GET", "POST"])
@login_required
@permisocompra
def compras():
    sql = "select Nombreproveedor ,NombreProducto,CantidadEntrada,PrecioT,FechaEntrada from Proveedor join Proveedor_Producto on Proveedor.IDproveedor = Proveedor_Producto.IDproveedor join Producto on Producto.CodigoProducto = Proveedor_Producto.CodigoProducto WHERE Proveedor_Producto.ESTADO = 'si'"  
    cursor.execute(sql)
    registro = cursor.fetchall()
    return render_template("pp.html" , datos = registro)

@app.route("/ventas" , methods=["GET", "POST"])
@login_required
@permisoventa
def ventas():
    sql = "select NombreProducto , NombreCliente, FechaSalida , CantidadSalida , PrecioProducto from Producto_Cliente join Producto on Producto.CodigoProducto =  Producto_Cliente.CodigoProducto join Cliente on Cliente.IDcliente = Producto_Cliente.IDcliente WHERE Producto_Cliente.ESTADO = 'si' "  
    cursor.execute(sql)
    registro = cursor.fetchall()
    return render_template("pc.html" , datos = registro)

@app.route("/adddesperfecto" , methods=["POST"])
@login_required
@permisodesperfecto
def adddesperfecto():
    if request.method == "POST":
        '''if not request.form.get("codigo") : 
            resultados = productos1()
            return render_template("adddesperfecto.html" , error = "Por favor seleccione un Producto" , datos = resultados)
        '''
        sql = "select Stock from Producto where CodigoProducto = ? "
        cursor.execute(sql, (request.form.get("codigo")))
        resultados = cursor.fetchall()
        resultados = resultados[0][0]
        print(resultados)
        if int(resultados) < int(request.form.get("cantidad")) : 
            session["error_add_desperfecto"] = 'Error'
            return redirect('/verdesperfecto')
            #return render_template("adddesperfecto.html" , error = "No hay suficientes Productos en la tienda" ,  datos = resultados)

        sql = "update  Producto set Stock = ? where CodigoProducto = ?"
        cursor.execute(sql, ( (int(resultados) - int(request.form.get("cantidad"))) , request.form.get("codigo")))
        conexion.commit() 

        sql = "update ColoryTalla set Stock = ? where id = (select MAX(id) from ColoryTalla)"
        values = (int(resultados) - int(request.form.get("cantidad")))
        cursor.execute(sql , (values))
        conexion.commit() 

        sql = "insert into Desperfecto (Descripcion, FechaSalida,Cantidadsalida,CodigoProducto,ESTADO) values (?,?,?,?,'si')"
        cursor.execute(sql, ( request.form.get("descripcion") , request.form.get("fecha"),request.form.get("cantidad") , request.form.get("codigo") ))
        conexion.commit() 
        session["add_desperfecto"] = 'add_desperfecto'
        return redirect('/verdesperfecto')

        #resultados = productos1()
        #return render_template("adddesperfecto.html" , succes = "Registrado Correctamente" , datos = resultados)

 


@app.route("/verventa" , methods=["GET", "POST"])
@login_required
@permisoventa
def verventa():
    sql = "select SUM(de.CantidadVendida) as CantidadVendida , ve.VentaID as ventaid,MAX(ve.FechaVenta) as FechaVenta, max(ve.TotalVenta) as Total_ganancia, max(p.NombreProducto) AS NombreProducto,  MAX(emp.NombreEmpleado) as Nombreempleado from Producto AS p  join Detalleventa as de ON p.CodigoProducto = de.CodigoProducto  join Ventas as ve on ve.VentaID = de.VentaID join empleado as emp on emp.IDempleado = ve.IDempleado GROUP BY ve.VentaID"
    cursor.execute(sql)
    registro = cursor.fetchall()
    return render_template("verventa.html" , datos = registro)    


@app.route("/editarventa" , methods=["GET", "POST" ])
@login_required
@permisoventa
def editarventa():
    sql = "update Producto_Cliente SET FechaSalida = ? , CantidadSalida = ? where CODIGOpc = ?" 
    cursor.execute(sql , ( request.form.get("FechaSalida") , request.form.get("Cantidadsalida") , request.form.get("CODIGOpc") ) )
    cursor.commit()
    return redirect("/verventa")

@app.route("/eliminarventa" , methods=["GET", "POST" ])
@login_required
@permisoventa
def eliminarventa():
    id = request.form.get("idhiddenform")
    sql = "update Producto_Cliente set ESTADO = 'no' where CODIGOpc = ?"
    cursor.execute(sql , (id))
    cursor.commit()
    return redirect("/verventa")

@app.route("/eliminaraba" , methods=["GET", "POST" ])
@login_required
@permisocompra
def eliminaraba():
    id = request.form.get("idhiddenform")
    sql = "update Proveedor_Producto set ESTADO = 'no' where CODIGOpp = ?"
    cursor.execute(sql , (id))
    cursor.commit()
    return redirect("/mostraaba")

@app.route("/proveedores" , methods=["GET", "POST"])
@login_required
@permisoproveedores
def empproveedoresleado():
    
    sql = "SELECT * FROM Proveedor WHERE ESTADO = 'si'"
    cursor.execute(sql)
    registro = cursor.fetchall()
    pro = session.pop('delete_proveedor', None)
    addpro = session.pop('add_proveedor', None)
    

   
    return render_template("proveedor.html" , datos = registro , pro=pro , addpro =addpro)

@app.route("/eliminarproveedor" , methods=["GET", "POST" ])
@login_required
@permisoproveedores
def eliminarproveedor():
    id = request.form.get("idhiddenform")
    sql = "update Proveedor set ESTADO = 'no' where IDproveedor = ?"
    cursor.execute(sql , (id))
    cursor.commit()
    session['delete_proveedor'] = 'Proveedor Eliminado!'
    return redirect("/proveedores")


@app.route("/eliminardesperfecto" , methods=["GET", "POST" ])
@login_required
@permisodesperfecto
def eliminardesperfecto():
    id = request.form.get("idhiddenform")

    consul = "select CodigoProducto, Cantidadsalida from Desperfecto where CodigoSP = ?"
    cursor.execute(consul , (id))
    resultados = cursor.fetchall()

    probando = "update Producto set Stock = Stock + ?  where CodigoProducto = ?"
    cursor.execute(probando , (int(resultados[0][1])) , resultados[0][0])
    cursor.commit()

    sql = "update Desperfecto set ESTADO = 'no' where CodigoSP = ?"
    cursor.execute(sql , (id))
    cursor.commit()
    session['correct_desperfecto'] = 'Eliminado!'

    return redirect("/verdesperfecto")

@app.route("/verdesperfecto" , methods=["GET", "POST"])
@login_required
@permisodesperfecto
def verdesperfecto():
    sql = "select Producto.CodigoProducto as p, NombreProducto , Descripcion , FechaSalida , Cantidadsalida ,	CodigoSP from Producto join Desperfecto on Producto.CodigoProducto = Desperfecto.CodigoProducto where Desperfecto.ESTADO = 'si'"
    cursor.execute(sql)
    registro = cursor.fetchall()
    resultados = productos1()


    error_add_desperfecto = session.pop('error_add_desperfecto', None) 
    add_desperfecto = session.pop('add_desperfecto', None) 
    correct_desperfecto = session.pop('correct_desperfecto', None)


    return render_template("verdesperfecto.html" , datos = registro , productos = resultados , error_add_desperfecto= error_add_desperfecto , add_desperfecto= add_desperfecto , correct_desperfecto =correct_desperfecto) 


@app.route("/agregarproveedor" , methods=["GET", "POST"])
@login_required
@permisoproveedores
def addproveedor():
    if request.method == "POST":
        suma = 0
        if request.form.get("correo") or request.form.get("telefono"):#al menos una forma de comunicarse 
            suma = 1
        if suma == 0 :
            return render_template("nuevoproveedor.html" , error = "registre al menos una forma de comunicarse con el proveedor")
        if request.form.get("correo"):
            if not request.form.get("correo").endswith('@gmail.com') and not request.form.get("correo").endswith('@hotmail.com'):#validar que es admitido
                return render_template("nuevoproveedor.html" , error = "correo invalido")   


        if not request.form.get("Telefono"):
            sql="INSERT INTO dbo.Proveedor(Nombreproveedor,Correo,Dirreccion,ESTADO) VALUES (?,?,?,'si')"
            cursor.execute(sql, (request.form.get("nombre"),  request.form.get("correo"), request.form.get("Dirreccion") ))
            conexion.commit() 
        else:
            sql="INSERT INTO dbo.Proveedor(Nombreproveedor,Correo,Telefono,Dirreccion,ESTADO) VALUES (?,?,?,?,'si')"
            cursor.execute(sql, (request.form.get("nombre"),  request.form.get("correo"),request.form.get("Telefono"), request.form.get("Dirreccion") ))
            conexion.commit() 
        session['add_proveedor'] = 'Proveedor Registrado!'

        return redirect('/proveedores')
    

    else:    
        return render_template("nuevoproveedor.html")
    

@app.route("/editardesperfecto" , methods=["GET", "POST" ])
@login_required
def editardesperfecto():
    
    sql = "select Cantidadsalida from Desperfecto where CodigoSP = ? "
    cursor.execute(sql ,request.form.get("CodigoSP"))
    resultados = cursor.fetchall()
    resultados = resultados[0][0]
    print(request.form.get("productoid"))
    print(resultados)
    if int(resultados) > int(request.form.get("Cantidadsalida")):
        resultados = int(resultados) -  int(request.form.get("Cantidadsalida"))
        sql = "select Stock from Producto Where CodigoProducto = ?"  
        cursor.execute(sql , request.form.get("productoid")) 
        diferencia = cursor.fetchone()
        sql = "update Producto set Stock = ? where CodigoProducto = ?"
        cursor.execute(sql , ( (int(diferencia[0]) + int(resultados) ) , request.form.get("productoid") ))
        cursor.commit()
    else :
        resultados =  int(request.form.get("Cantidadsalida")) - int(resultados)   
        sql = "select Stock from Producto Where CodigoProducto = ?"  
        cursor.execute(sql , request.form.get("productoid")) 
        diferencia = cursor.fetchone()
        sql = "update Producto set Stock = ? where CodigoProducto = ?"
        cursor.execute(sql , ( (int(diferencia[0]) - int(resultados) ) , request.form.get("productoid") ))
        cursor.commit()

    sql = "update Desperfecto set Descripcion = ? , FechaSalida = ? , Cantidadsalida = ? where  CodigoSP = ?"
    cursor.execute(sql ,(request.form.get("Descripcion"),request.form.get("FechaSalida"),request.form.get("Cantidadsalida"),request.form.get("CodigoSP")))
    cursor.commit()

    return redirect("/verdesperfecto")

@app.route("/editProveedor" , methods=["GET", "POST" ])
@login_required
def editProveedor():

    if request.method == "POST":
        id = request.form.get("id")
        nombre = request.form.get("nombre")
        correo = request.form.get("correo")
        telef = request.form.get("Telefono")
        direc = request.form.get("Dirreccion")
        estado = 'si'
        sql = "UPDATE Proveedor SET NombreProveedor = ?, Correo = ?, Telefono = ?, Dirreccion = ?, estado = ? WHERE IDproveedor = ?"
        params = (nombre, correo, telef, direc, estado, id)

        cursor.execute(sql, params)
        cursor.commit()

        return redirect("/proveedores")
    

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")
'''''
@app.route('/data')
def get_data():
    sql = "select top 10 NombreProducto,CantidadSalida from Producto join Producto_Cliente ON Producto.CodigoProducto =  Producto_Cliente.CodigoProducto order by CantidadSalida desc"
    cursor.execute(sql)
    entity_data = cursor.fetchall()

    # Transforma los datos en un formato compatible con Chart.js
    chart_data = {
        'labels': [],
        'data': []
    }
    for data_point in entity_data:
        print(data_point[0])
        chart_data['labels'].append(data_point[0])
        chart_data['data'].append(data_point[1])

    return jsonify(chart_data)
'''''

@app.route("/" , methods=["GET", "POST"])
@login_required
def index():
    
    ''' sql = "select NombreProducto , SUM(CAST(CantidadVendida AS int)) AS TotalSalidas from Producto JOIN DetalleVenta ON Producto.CodigoProducto = DetalleVenta.CodigoProducto GROUP BY NombreProducto ORDER BY TotalSalidas DESC"
    cursor.execute(sql)
    entity_data = cursor.fetchall()

    #Transforma los datos en un formato compatible con Chart.js
    chart_data = {
        'labels': [],
        'data': []
    }
    for data_point in entity_data:
        chart_data['labels'].append(data_point[0])
        chart_data['data'].append(data_point[1])
    '''
    sql = "select TOP 10  NombreProducto ,SUM(CAST(Stock AS int)) AS cantidad from Producto  GROUP BY NombreProducto ORDER BY cantidad DESC"
    cursor.execute(sql)
    entity_data = cursor.fetchall()
    chart2 = {
        'labels': [],
        'data': []
    }
    for data_point in entity_data:
        chart2['labels'].append(data_point[0])
        chart2['data'].append(data_point[1])
    
    sql = '''SELECT TOP 8 p.Nombreproveedor , COUNT(D.CodigoProducto) AS CantidadProductos 
            FROM Proveedor p JOIN Abastecimientos A ON p.IDproveedor = A.IDproveedor 
            join DetalleAbastecimiento D on A.AbastecimientoID = D.AbastecimientoID
            GROUP BY p.Nombreproveedor ORDER BY CantidadProductos DESC'''
    cursor.execute(sql)
    entity_data = cursor.fetchall()

    # Transformar los datos en un formato compatible con Chart.js
    chart3 = {
        'labels': [],
        'data': []
    }
    for data_point in entity_data:
        chart3['labels'].append(data_point[0])
        chart3['data'].append(data_point[1])

    '''data = chart_data , data2 = chart2 , data3 = chart3)'''
    return render_template("futuro.html" , data2 = chart2 , data3 = chart3)
    

@app.route('/obtener_cantidad_disponible/<int:producto_id>')
def obtener_cantidad_disponible(producto_id):
    # Aquí debes realizar la consulta a tu base de datos para obtener la cantidad disponible del producto
    # Reemplaza esta lógica con la forma en que interactúas con tu base de datos
    if producto_id == 1:
        cantidad_disponible = 5
    else:
        cantidad_disponible = 10
        
    # Devolver la cantidad disponible como respuesta JSON
    return jsonify({'cantidad': cantidad_disponible})

@app.route('/permisos', methods=['GET'])
def obtener_permisos():
    if session["user_id"][0][1] != 'admin':
        return redirect("/")
    user_id = request.args.get('id')  
    print(user_id)
    sql = "SELECT Permisos.nombre AS permiso, estado FROM Permisos JOIN Usuarios ON Permisos.usuario_id = Usuarios.id WHERE Usuarios.id = ?"
    cursor.execute(sql, (user_id))
    permisos = cursor.fetchall()
    permisos_list = []
    for permiso in permisos:
        permiso_dict = {
            'permiso': permiso[0],
            'estado': permiso[1]
        }
        permisos_list.append(permiso_dict)
    print(permisos_list)
    return jsonify({'permisos': permisos_list})


@app.route("/editpermisos" , methods=["GET", "POST" ])
def editpermisos():
    if session["user_id"][0][1] != 'admin':
        return redirect("/")

    if request.form.get("permisoempleado") == 'on':
        empleado = 1
    else:
        empleado = 0
    sql = "update Permisos set estado = ? where usuario_id = ? and nombre = 'empleados'"
    cursor.execute(sql , (empleado,request.form.get("id") ))
    cursor.commit()


    if request.form.get("permisodesperfecto") == 'on':
        desperfecto = 1
    else :
        desperfecto = 0

    sql = "update Permisos set estado = ? where usuario_id = ? and nombre = 'desperfectos'"
    cursor.execute(sql , (desperfecto,request.form.get("id") ))
    cursor.commit()


    if request.form.get("permisoproductos") == 'on':
        productos = 1
    else :
        productos = 0
    sql = "update Permisos set estado = ? where usuario_id = ? and nombre = 'productos'"
    cursor.execute(sql , (productos,request.form.get("id") ))
    cursor.commit()

    if request.form.get("permisocompras") == 'on':
        compras = 1
    else :
        compras = 0
    sql = "update Permisos set estado = ? where usuario_id = ? and nombre = 'compras'"
    cursor.execute(sql , (compras,request.form.get("id") ))
    cursor.commit()

    if request.form.get("permisoventas")== 'on':
        ventas = 1
    else :
        ventas = 0
    sql = "update Permisos set estado = ? where usuario_id = ? and nombre = 'ventas'"
    cursor.execute(sql , (ventas,request.form.get("id") ))
    cursor.commit()

    if request.form.get("permisoproveedores") == 'on':
        proveedores = 1
    else :
        proveedores = 0
    sql = "update Permisos set estado = ? where usuario_id = ? and nombre = 'proveedores'"
    cursor.execute(sql , (proveedores,request.form.get("id") ))
    cursor.commit()

    return redirect("/edituser")



@app.route("/editproduct", methods=["POST"])
def editproduct():
    id = request.form.get("idProducto")
    nombre = request.form.get("nombre")
    precio = request.form.get("precio")
    imagen_bytes = ""

    if request.files.get("imagen"):
        imagen = request.files.get("imagen")
        imagen_bytes = imagen.read()

    # Verificar si el nombre del producto ya está registrado
    cursor.execute("SELECT COUNT(*) FROM Producto WHERE NombreProducto = ? AND CodigoProducto != ?", (nombre, id))
    nombre_existente = cursor.fetchone()[0]

    if nombre_existente > 0:
        return jsonify({"error": "El nombre del producto ya está registrado"}), 400

    consult = 'SELECT PrecioProducto FROM Producto WHERE CodigoProducto = ?'
    cursor.execute(consult, (id,))
    resultados = cursor.fetchone()[0]

    if int(resultados) != int(precio):
        sql = '''INSERT INTO HistorialPrecios 
                 (CodigoProducto, FechaCambio, PrecioAnterior, PrecioNuevo) 
                 VALUES (?, ?, ?, ?)'''
        cursor.execute(sql, (id, datetime.date.today(), int(resultados), precio))
        cursor.commit()

    sql = "UPDATE Producto SET NombreProducto = ?, PrecioProducto = ?"
    params = [nombre, precio]

    if imagen_bytes:
        sql += ", foto = ?"
        params.append(pyodbc.Binary(imagen_bytes))

    sql += " WHERE CodigoProducto = ?"
    params.append(id)

    cursor.execute(sql, params)
    cursor.commit()

    return jsonify({"success": "Producto actualizado correctamente"})

@app.route("/verificarDataProduct" , methods=["POST"])
def verificarDataProduct():
    idProducto = request.form.get("id_product")
    nombre = request.form.get("nombreProduct")
    # Verificar si el código ya existe y si el nombre coincide
     # Verificar si el nombre del producto ya existe
    cursor.execute('SELECT COUNT(*) FROM Producto WHERE NombreProducto = ?', (nombre,))
    resultado = cursor.fetchone()[0]

    if resultado == 0:
        # El nombre del producto no existe
        cursor.execute('SELECT COUNT(*) FROM Producto WHERE CodigoProducto = ?', (idProducto,))
        resultado = cursor.fetchone()[0]
        if resultado == 0:
            # El nombre y el código del producto no existen
            return jsonify({"success": "El producto no existe, puede ser añadido."})
        else:
            # El nombre no existe pero el código sí
            return jsonify({"success": "El producto ya existe con otro nombre."})
    else:
        # El nombre del producto existe
        cursor.execute('SELECT COUNT(*) FROM Producto WHERE NombreProducto = ? AND CodigoProducto = ?', (nombre, idProducto))
        resultado = cursor.fetchone()[0]
        if resultado == 0:
            # El nombre existe pero el código no coincide
            cursor.execute('SELECT COUNT(*) FROM Producto WHERE CodigoProducto = ?', (idProducto,))
            resultado = cursor.fetchone()[0]
            if resultado == 0:
                # El nombre existe pero el código no
                return jsonify({"success": "El nombre del producto existe, pero el código no. Puede ser añadido."})
            else:
                # El código existe con otro nombre
                return jsonify({"error": "El código del producto ya existe con otro nombre."})
        else:
            # El nombre y el código coinciden
            return jsonify({"success": "El producto ya existe y el nombre coincide."})


    



 

@app.route("/getproduct/<string:product_id>", methods=["GET"])
def getproduct(product_id):
    cursor.execute("SELECT CodigoProducto, NombreProducto, PrecioProducto, foto FROM Producto WHERE CodigoProducto = ?", (product_id,))
    product = cursor.fetchone()
    if product:
        product_data = {
            "id": product[0],
            "nombre": product[1],
            "precio": product[2],
            "imagen": base64.b64encode(product[3]).decode('utf-8') if product[3] else None
        }
        return jsonify(product_data)
    else:
        return jsonify({"error": "Producto no encontrado"}), 404


@app.route("/agregarproductos" , methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":

        if not request.form.get("codigoproveedor"):
            resultados = productos0()
            lista = proveedor()
            return render_template("pp.html" , error = "Por favor seleccione un Proveedor" , datos = resultados ,proveedor = lista)

        if not request.form.get("codigo") : 
            resultados = productos0()
            lista = proveedor()
            return render_template("pp.html" , error = "Por favor seleccione un Producto" , datos = resultados ,proveedor = lista)
        
        sql="insert into Proveedor_Producto(FechaEntrada,CantidadEntrada,PrecioT, CodigoProducto,IDproveedor , ESTADO) VALUES (?,?,?,?,?,'si')"
        cursor.execute(sql, (request.form.get("fecha") , request.form.get("cantidad"),(int(request.form.get("precio")) * int(request.form.get("cantidad"))) , request.form.get("codigo"),request.form.get("codigoproveedor")  ))
        conexion.commit() 


        sql = "select Stock from Producto where CodigoProducto = ? "
        cursor.execute(sql, (request.form.get("codigo")))
        resultados = cursor.fetchall()
        resultados = resultados[0][0]

        sql =" update  Producto set Stock = ? where CodigoProducto = ?  "
        cursor.execute(sql, ( int(resultados) + int(request.form.get("cantidad")) ,request.form.get("codigo") ))
        conexion.commit() 

        resultados = productos0()
        lista = proveedor()

        return render_template("pp.html" , succes = "Abastecido Correctamente" , datos = resultados , proveedor = lista)

    else:
        lista = proveedor()
        resultados = productos0()
        return render_template("pp.html" , datos = resultados , proveedor = lista)







       
@app.route("/addproduct" , methods=["GET","POST"])
@login_required
@permisoproducto
def addproduct():
    if request.method == "POST":
        try:
            datos_recibidos = request.get_json()  # Obtener los datos JSON de la solicitud
            # Realiza alguna operación con los datos (por ejemplo, guarda en una base de datos)
            # ...
            for row in datos_recibidos:
                
                sql = "SELECT * FROM Producto WHERE CodigoProducto = ? AND NombreProducto = ?"
                cursor.execute(sql, ( row["id_product"] , row["name_producto"]))
                resultados = cursor.fetchone()
                if resultados is None:
                    sql = "INSERT INTO Producto (CodigoProducto, NombreProducto, PrecioProducto , Stock , ESTADO) values (?,? ,?, ? , 'si')"
                    cursor.execute(sql , ( row["id_product"]),row["name_producto"], int(row["precioventa"]),int(row["cantidad_producto"]))
                    cursor.commit()
                else:
                    print('y entonces')
                    sql= "UPDATE Producto set Stock = (stock + ?) where  CodigoProducto = ?"
                    cursor.execute(sql , (int(row["cantidad_producto"]),row["id_product"]))
                    cursor.commit()
                
                sql = "select * from ColoryTalla where (CodigoProducto = ? and Talla = ? and ColorProducto = ?)"
                cursor.execute(sql, ( row["id_product"] , int(row["talla_producto"]),row["color_producto"]))
                resultados = cursor.fetchone()

                if resultados is None:
                    sql = "insert into ColoryTalla (CodigoProducto , Talla , ColorProducto , Stock) values (?,?,?,?)"
                    cursor.execute(sql , (row["id_product"],int(row["talla_producto"]),row["color_producto"],int(row["cantidad_producto"])))
                    cursor.commit()
                else:
                    sql = "update ColoryTalla set Stock = (stock + ?) where (CodigoProducto = ? and Talla = ? and ColorProducto = ? )"
                    cursor.execute(sql , (int(row["cantidad_producto"]),row["id_product"],int(row["talla_producto"]),row["color_producto"],))
                    cursor.commit()
                
                sql = "select * from Abastecimientos where (FechaAbastecimiento = ? and IDproveedor = ?)"
                cursor.execute(sql, ( row["fecha_producto"] , int(row['codigoproveedor'] )))
                resultados = cursor.fetchone()

                if resultados is None:
                    sql="insert into Abastecimientos (IDproveedor , FechaAbastecimiento , TotalCompra) values (?,?,?)"
                    cursor.execute(sql, ( int(row['codigoproveedor'] ),row["fecha_producto"], (int(row['preciocompra']) * int(row["cantidad_producto"]) )  ))                    
                    cursor.commit()

                    
                else:
                    sql='update Abastecimientos set TotalCompra = (TotalCompra + ?) WHERE (FechaAbastecimiento = ? and IDproveedor = ?)'
                    cursor.execute(sql, ( (int(row['preciocompra']) * int(row["cantidad_producto"])) ,row["fecha_producto"], int(row['codigoproveedor']) ) )                  
                    cursor.commit()

                sql = "select AbastecimientoID from Abastecimientos where (FechaAbastecimiento = ? and IDproveedor = ?)"
                cursor.execute(sql, ( row["fecha_producto"] , int(row['codigoproveedor'] )))
                resultados = cursor.fetchone()
                AbastecimientosID = resultados[0]
                print(AbastecimientosID)

                sql = "select * from DetalleAbastecimiento where CodigoProducto = ? and AbastecimientoID = ?"
                values = (row["id_product"],AbastecimientosID)
                cursor.execute(sql , (values))
                resultados = cursor.fetchone()

                if resultados is None:  
                    print("prueba") 
                    sql = """ insert into DetalleAbastecimiento
                                    (CodigoProducto,
                                    AbastecimientoID,
                                    CantidadSuministrada,
                                    PrecioUnitario) values (?,?,?,?)
                                """
                    values = (row["id_product"] , AbastecimientosID , int(row["cantidad_producto"]) , int(row['preciocompra']))
                    cursor.execute(sql , (values))
                    cursor.commit()             

                else:
                    sql = "update DetalleAbastecimiento set CantidadSuministrada = (CantidadSuministrada + ?) where CodigoProducto = ? and AbastecimientoID = ?"
                    values = ( row["cantidad_producto"] , row["id_product"] ,AbastecimientosID )
                    cursor.execute(sql , (values))
                    cursor.commit()
  
                sql = "SELECT * FROM Marca WHERE CodigoProducto = ?"
                cursor.execute(sql, ( row["id_product"] ))
                resultados = cursor.fetchone()
                if resultados is None: 
                    sql = "insert into Marca (NombreMarca , CodigoProducto , ESTADO ) VALUES (?,?,'si')"
                    cursor.execute(sql ,row["marca_producto"]  , row["id_product"] )
                    cursor.commit()

                sql = "SELECT * FROM Categoria WHERE CodigoProducto = ?"
                cursor.execute(sql, ( row["id_product"] ))
                resultados = cursor.fetchone()
                if resultados is None: 
                    sql = "insert into Categoria (NombreCategoria , CodigoProducto , ESTADO ) VALUES (?,?,'si')"
                    cursor.execute(sql ,row["categoria_producto"] , row["id_product"] )
                    cursor.commit()
            
            ''' 'id_product':'505', 
            'imagen_producto': '', 
            'name_producto': 'Literide Clog 3', 
            'talla_producto': '43', 
            'categoria_producto': 'deportivo', 
            'marca_producto': 'nike',
            'color_producto': 'azul con blanco', 
            'preciocompra': '1400', 
            'precioventa': '1800',
            'cantidad_producto': '2',
            'fecha_producto': '2023-10-31',
            'codigoproveedor': '8'} '''


            # Preparar una respuesta en formato JSON
            return jsonify(datos_recibidos)
            

        except Exception as e:
            return jsonify({"error": str(e)})
        
    else:
        return render_template("productonuevo.html" , proveedor = proveedor())


@app.route('/añadir_venta', methods=['POST'])
def recibir_datos_compra():
    datos_compra = request.get_json()
    datos = []
    fecha = datos_compra[0]['fecha']
    empleado = datos_compra[0]['empleado']
    print(empleado)
    print(fecha)
    for row in datos_compra:
        sql = ' update ColoryTalla set Stock = (Stock - ?) where CodigoProducto = ? and ColorProducto = ? and Talla = ?'
        values = (int(row['cantidad']) , row['codigo'] , row['color'], row['talla'])
        cursor.execute(sql , values)
        cursor.commit()

        sql = "update Producto set Stock = (Stock - ?) where CodigoProducto = ?"
        values = (int(row['cantidad'])  , row['codigo'])
        cursor.execute(sql , values)
        cursor.commit()

        sql = "select * from Ventas where IDempleado = ? and Fechaventa = ?"
        values = (empleado , fecha )
        cursor.execute(sql , values)
        resultados = cursor.fetchone() 

        if resultados is None:
            print('y entonces')
            sql = "insert into Ventas (IDempleado , FechaVenta , TotalVenta) values (?, ?,?)"
            values = ( empleado , fecha , (int(row['precio']) *  int(row['cantidad'])) )
            cursor.execute(sql , values)
            cursor.commit()
        else:
            sql = "update Ventas set TotalVenta = (TotalVenta + ?) WHERE IDempleado = ?  and FechaVenta = ?"
            values = ((int(row['precio']) *  int(row['cantidad'])), empleado , fecha)
            cursor.execute(sql , values)
            cursor.commit()
  
        sql = "select VentaID from Ventas where IDempleado = ? and Fechaventa = ?"
        values = ( empleado , fecha )
        cursor.execute(sql , values)
        resultados = cursor.fetchone()
        ventaid =resultados[0] 
        print(ventaid)

        sql = "select * from DetalleVenta where CodigoProducto = ? and VentaID = ?"
        values  = (row['codigo'] , ventaid)
        cursor.execute(sql , values)
        resultados = cursor.fetchone()

        if resultados is None:
            sql = 'insert into DetalleVenta (VentaID ,CodigoProducto , CantidadVendida , PrecioUnitario) VALUES (?,?,?,?)'
            values = (ventaid  ,row['codigo']  , int(row['cantidad']) , int(row['precio']))
            cursor.execute(sql , values)
            cursor.commit()
        else :
            sql = "UPDATE DetalleVenta SET CantidadVendida = (CantidadVendida + ?) WHERE  CodigoProducto = ? AND VentaID = ?"
            values = (int(row['cantidad']) ,row['codigo']  , ventaid )
            cursor.execute(sql , values)
            cursor.commit()
                
        return jsonify({"mensaje": "Datos de compra recibidos con éxito"})


@app.route("/addventa" , methods=["GET"])
@permisoventa
@login_required
def addventa():
    sql = "select  Producto.CodigoProducto as codigo,NombreProducto, PrecioProducto,Talla , ColorProducto,ColoryTalla.Stock as stock from ColoryTalla join Producto on ColoryTalla.CodigoProducto = Producto.CodigoProducto where ColoryTalla.Stock > 0"
    cursor.execute(sql)
    return render_template("addventa.html" ,productos = cursor.fetchall() , empleado = empleado())
    
@app.route("/editarabastecimiento" , methods=["GET", "POST"])
def editarabastecimiento():
    if request.method == "POST":       
        sql = "select CantidadEntrada from Proveedor_Producto where CODIGOpp = ? "
        cursor.execute(sql ,request.form.get("idbastecimiento"))
        resultados = cursor.fetchall()
        resultados = resultados[0][0]
        
        if int(resultados) > int(request.form.get("cantidad")):
            resultados = int(resultados) -  int(request.form.get("cantidad"))
            sql = "select Stock from Producto Where CodigoProducto = ?"  
            cursor.execute(sql , int(request.form.get("idProducto"))) 
            diferencia = cursor.fetchall()
            sql = "update Producto set Stock = ? where CodigoProducto = ?"
            cursor.execute(sql , ( (int(diferencia[0][0]) - int(resultados) ) , int(request.form.get("idProducto") )))
            cursor.commit()
        else :
            resultados =  int(request.form.get("cantidad")) - int(resultados)   
            sql = "select Stock from Producto Where CodigoProducto = ?"  
            cursor.execute(sql , int(request.form.get("idProducto"))) 
            diferencia = cursor.fetchall()
            sql = "update Producto set Stock = ? where CodigoProducto = ?"
            cursor.execute(sql , ( (int(diferencia[0][0]) + int(resultados) ) , int(request.form.get("idProducto") )))
            cursor.commit()

        sql ="update Proveedor_Producto set FechaEntrada = ?,CantidadEntrada = ? , PrecioT = ? where CODIGOpp = ?"
        cursor.execute(sql , request.form.get("fecha") , int(request.form.get("cantidad")) ,request.form.get("gasto") , request.form.get("idbastecimiento")  )
        cursor.commit()

        return redirect("/mostraaba")
    

def empleado():
    sql = "select * from Empleado where ESTADO = 'si'"
    cursor.execute(sql)
    resultados = cursor.fetchall()
    return resultados

@app.route("/reporteempleado" , methods=["GET", "POST"])
def reporteempleado():
    return render_template("reporteempleado.html" , datos = empleado())

@app.route("/reporteventas" , methods=["GET", "POST"])
@login_required
def reporteventas():
    if session["user_id"][0][1] != 'admin':
        return redirect("/")
    sql = "select de.CodigoProducto AS CodigoProducto , de.CantidadVendida as CantidadVendida, de.PrecioUnitario AS PrecioUnitario, ve.FechaVenta as FECHA, emp.NombreEmpleado AS NombreEmpleado,(de.PrecioUnitario*de.CantidadVendida) AS GASTO from DetalleVenta as de  join Ventas as ve on de.VentaID = ve.VentaID join empleado as emp on emp.IDempleado = ve.IDempleado"
    cursor.execute(sql)
    resultados = cursor.fetchall()
    return render_template("reporteventa.html" , datos = resultados)

@app.route("/reportecompras" , methods=["GET", "POST"])
@login_required
def reportecompras():
    if session["user_id"][0][1] != 'admin':
        return redirect("/")
    sql = "select de.CodigoProducto AS CodigoProducto ,de.CantidadSuministrada AS CantidadSuministrada, de.PrecioUnitario AS PrecioUnitario ,aba.FechaAbastecimiento AS FECHA, p.Nombreproveedor AS Nombreproveedor, (de.PrecioUnitario*de.CantidadSuministrada) AS GASTO from DetalleAbastecimiento as de join Abastecimientos AS aba  on aba.AbastecimientoID = de.AbastecimientoID join Proveedor as p on p.IDproveedor = aba.IDproveedor"
    cursor.execute(sql)
    resultados = cursor.fetchall()
    return render_template("reportecompras.html" , datos = resultados)
    

@app.route("/mostraaba" , methods=["GET", "POST"])
@permisocompra
@login_required
def mostraaba():
    if request.method == "POST":
        next
    else:
        
        sql ="SELECT SUM(de.CantidadSuministrada) AS CantidadSuministrada, aba.AbastecimientoID AS id_abas, MAX(aba.FechaAbastecimiento) AS FechaAbastecimiento, MAX(aba.TotalCompra) AS Total_Gasto, MAX(p.NombreProducto) AS NombreProducto, MAX(pro.Nombreproveedor) AS Nombreproveedor FROM Producto AS p JOIN DetalleAbastecimiento AS de ON p.CodigoProducto = de.CodigoProducto JOIN Abastecimientos AS aba ON de.AbastecimientoID = aba.AbastecimientoID JOIN Proveedor AS pro ON aba.IDproveedor = pro.IDproveedor GROUP BY aba.AbastecimientoID;"
       
        resultado = cursor.execute(sql)
        resultado = cursor.fetchall()
        return render_template("mostrarabatecimientos.html" , datos = resultado)
    
@app.route('/ver_detalles/<int:abastecimiento_id>')
def ver_detalles(abastecimiento_id):
    print(abastecimiento_id)
    cursor.execute("SELECT * FROM DetalleAbastecimiento WHERE AbastecimientoID = ?", (abastecimiento_id,))
    detalles = cursor.fetchall()
    print(detalles)
    desgloce = []

    for detalle in detalles:
        detalle_dict = {
            'DetalleAbastecimientoID' : detalle[0],
            'CodigoProducto' : detalle[1], 
            'AbastecimientoID' : detalle[2], 
            'CantidadSuministrada' : detalle[3], 
            'PrecioUnitario' : detalle[4]
        }
        desgloce.append(detalle_dict)
    print(desgloce)

    return desgloce

@app.route('/ver_detalles_compras/<int:ventaid>')
def ver_detalles_compras(ventaid):
    print(ventaid)
    cursor.execute("SELECT * FROM Detalleventa WHERE DetalleVentaID = ?", (ventaid,))
    detalles = cursor.fetchall()
    print(detalles)
    desgloce = []

    for detalle in detalles:
        detalle_dict = {
            'DetalleVenta' : detalle[0],
            'CodigoProducto' : detalle[2], 
            'VentaID' : detalle[2], 
            'cantidadvendida' : detalle[3], 
            'PrecioUnitario' : detalle[4]
        }
        desgloce.append(detalle_dict)
    print(desgloce)

    return desgloce

def productos1():
    sql = "select * from Producto where ESTADO = 'si' and Stock >= '1' "   
    cursor.execute(sql)
    resultados = cursor.fetchall()
    productos = [] 
    for row in resultados:
        id = row[0]
        imagens = row[5]
        nombre = row[1]
        precio = row[2]
        stock = row[3]
        if imagens is None:
            productos.append({'CodigoProducto': id , 'foto': 'https://static.vecteezy.com/system/resources/previews/005/337/799/non_2x/icon-image-not-found-free-vector.jpg', 'NombreProducto':nombre , 'PrecioProducto':precio , 'stock' : stock})
        else:
            imagen_base64 = base64.b64encode(imagens).decode('utf-8')
            productos.append({'CodigoProducto': id , 'foto':    'data:image/png;base64,' + imagen_base64, 'NombreProducto':nombre , 'PrecioProducto':precio , 'stock' : stock})
    
    return productos

def productos0():
    sql = "select * from Producto where ESTADO = 'si' "   
    cursor.execute(sql)
    resultados = cursor.fetchall()
    productos = [] 
    for row in resultados:
        id = row[0]
        imagens = row[7]
        color= row[2]
        talla = row[4]
        nombre = row[1]
        precio = row[3]
        stock = row[5]
        if imagens is None:
            productos.append({'CodigoProducto': id , 'foto': 'https://static.vecteezy.com/system/resources/previews/005/337/799/non_2x/icon-image-not-found-free-vector.jpg', 'ColorProducto':color , 'Talla' : talla , 'NombreProducto':nombre , 'PrecioProducto':precio , 'stock' : stock})
        else:
            imagen_base64 = base64.b64encode(imagens).decode('utf-8')
            productos.append({'CodigoProducto': id , 'foto':    'data:image/png;base64,' + imagen_base64, 'ColorProducto':color , 'Talla' : talla , 'NombreProducto':nombre , 'PrecioProducto':precio , 'stock' : stock})
    
    return productos

def proveedor():
    sql = "select * from Proveedor where ESTADO = 'si'"   
    cursor.execute(sql)
    resultados = cursor.fetchall()
    return resultados
'''''
@app.route('/dataP')
@login_required
def grafproveedor():
    # Consulta SQL para obtener la cantidad de productos suministrados por cada proveedor
    sql = "SELECT TOP 8 p.Nombreproveedor, COUNT(pp.CodigoProducto) AS CantidadProductos FROM Proveedor p JOIN Proveedor_Producto pp ON p.IDproveedor = pp.IDproveedor GROUP BY p.Nombreproveedor ORDER BY CantidadProductos DESC"
    cursor.execute(sql)
    entity_data = cursor.fetchall()

    # Transformar los datos en un formato compatible con Chart.js
    chart_data = {
        'labels': [],
        'data': []
    }
    for data_point in entity_data:
        chart_data['labels'].append(data_point[0])
        chart_data['data'].append(data_point[1])
    print(chart_data)
    return jsonify(chart_data)
'''''

# Ruta que envia el token
@app.route("/recuperaForm", methods=["GET", "POST"])
def recuperaForm():
    if request.method == "POST":
        email = request.form.get("email")
        query1 = "select * from Usuarios where correo = ?"
        rows =cursor.execute(query1, (email))
        rows = cursor.fetchall()
        if not email:
            error='Ingrese un correo'
            return render_template("FormRecupera.html",error=error)
        if len(rows) == 0 or not (rows[0][3] == email):
            error='Ingrese un correo valido'
            return render_template("FormRecupera.html",error=error)
        else:
            token = s.dumps(email, salt='email-confirm')
            mensaje = Message('Cambio de contraseña', sender='KD',recipients=[f"{email}"])
            link = url_for('restablece',token=token, _external=True)
            mensaje.body = 'Da click en el siguiente link para recuperar tu contraseña {}.\nSi no solicitaste el restablecimiento de tu contraseña ignora este mensaje'.format(link)
            enviado = 'Revisa tu correo electrónico.'
            session['enviado'] = enviado
            mail.send(mensaje)
            return redirect(url_for('recuperaForm'))
    enviado = session.pop('enviado', None)
    return render_template("FormRecupera.html", enviado=enviado)

# Ruta para generar el enlace de restablecimiento de contraseña
@app.route("/nuevoPassw/<token>", methods=["GET", "POST"])
def restablece(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=60)
        session["reset_token"] = token  # Almacena el token en la sesión
        session["email"] = email
        session.modified = True 
    except SignatureExpired:
        return '<hI>El link expiró</hl>'

    except BadSignature:
        return '<h1>El link no es válido.</h1>'
    
    return redirect(url_for("Cambio"))
    
# Ruta para el cambio de contrasenia
@app.route("/cambioPassw", methods=["GET", "POST"])
@token_required
def Cambio():
    if request.method == "POST":
        email = session.get("email")  # Obtiene el correo electrónico de la sesión
        contra = request.form.get("nueva-contrasenia")
        confirContra = request.form.get("confirmar-contrasenia")
        if contra and confirContra:
            if contra == confirContra:
                sql = "update Usuarios set contraseña = ? where correo = ?"
                cursor.execute(sql, (generate_password_hash(contra),email))
                cursor.commit()
                session.pop("email", None)  # Elimina el correo electrónico de la sesión
                session.pop("reset_token", None)  # Elimina el token de la sesión
                return render_template("login.html")
            if contra != confirContra:
                error = 'Contraseña no coiciden'
                return render_template("FormNuevoPassw.html",error=error) 
        else:
            error = 'campos vacios'
            return render_template("FormNuevoPassw.html",error=error)                          

    else:
        return render_template("FormNuevoPassw.html") 


@app.route("/editEmpleado" , methods=["GET", "POST" ])
@login_required
@permisoempleado_required
def editEmpleado():

    if request.method == "POST":
        id = request.form.get("id")
        nombre = request.form.get("nombre")
        correo = request.form.get("correo")
        telef = request.form.get("Telefono")
        direc = request.form.get("Dirreccion")
        salario = request.form.get("salario")
        estado = 'si'
        sql = "UPDATE Empleado SET NombreEmpleado = ?, Correo = ?, Telefono = ?, Dirreccion = ?, salario = ?, estado = ? WHERE IDempleado = ?"
        params = (nombre, correo, telef, direc, salario, estado, id)

        cursor.execute(sql, params)
        cursor.commit()

        return redirect("/empleado")
    

#Manual de usuario
@app.route("/usermanual" , methods=["GET", "POST"])
@login_required
def manualUsuario():
    if request.method == "POST":
        pass
    else:
        return render_template("usermanual.html")

@app.route('/descripcionesManual')
@login_required
def descripciones():
    section = request.args.get('data-section', default='')
    print(f"Valor de 'section': {section}")
    # Renderiza la plantilla y pasa el valor de 'section'
    return render_template('manualdescript.html', section=section)


if __name__ == '__main__':
    app.run()




# Endpoint para la búsqueda de productos
@app.route('/buscar_producto', methods=['POST'])
def buscar_producto():

    codigo_producto = request.json['codigo_producto']
    print(codigo_producto)
    if codigo_producto != '':
        
        query = ('''
               SELECT  p.CodigoProducto, p.NombreProducto , p.PrecioProducto 
                , CT.Talla, CT.ColorProducto ,c.NombreCategoria , m.NombreMarca
                FROM Producto AS p 
                JOIN ColoryTalla AS CT ON p.CodigoProducto = CT.CodigoProducto 
                join Categoria as c on p.CodigoProducto = c.CodigoProducto
                join Marca as m on p.CodigoProducto = m.CodigoProducto
                WHERE UPPER(p.CodigoProducto) LIKE ?
        ''')
        params = (f'%{codigo_producto.upper()}%')
        cursor.execute(query, params)
        resultados = cursor.fetchall()


        sugerencias = [{ 'codigo':resultado[0] ,'nombre': resultado[1], 'precio': resultado[2] , 'talla' : resultado[3] , 'color':resultado[4] , 'categoria':resultado[5] , 'marca':resultado[6]} for resultado in resultados]
        # Puedes agregar más detalles según la estructura de tu base de datos

        # Renderizar el resultado como JSON
        print(sugerencias)
        if sugerencias:
            return jsonify(sugerencias)
        else:
            return jsonify({'mensaje': 'No se encontraron resultados.'})
    else:
        return jsonify({'mensaje': 'No se encontraron resultados.'})