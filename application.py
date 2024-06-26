import base64
import pyodbc
import requests
from flask_paginate import Pagination, get_page_parameter
from urllib.parse import unquote
from werkzeug.security import generate_password_hash , check_password_hash
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_session import Session
from helper import  login_required

admins = ['KD' , '1234']
gerente = ['kd' , '1234']

app = Flask(__name__)
app.debug = True

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

try:##verificar que no haya ningun error al conectarse con la BF
    #conexion =  pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-F9CVAAQJ\SQLEXPRESS;DATABASE=copiatiendakd;UID=TiendaKD;PWD=1234')
    conexion =  pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-LNI0PI4;DATABASE=copiatienda01-06;UID=Nayareth;PWD=0212')

    #Conexion pa mi compu Harvin xd
    #conexion =  pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-QUNO8C9;DATABASE=copiatienda01-06;Trusted_Connection=yes;')
except:
    print("FAIL")

cursor = conexion.cursor()

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        nombre = request.form.get("usuario")
        password = request.form.get("password")

        query = "select * from Usuarios where nombre = ?"
        rows =cursor.execute(query, (nombre))
        rows = cursor.fetchall()

        if len(rows) == 0 or not (rows[0][2] == password):
            print("prueba")
            return render_template("login.html" , error="Nombre de usuario o contraseña incorrecta")

            #if query and password: #and confirmar == password:
        
        else:
        
            session["user_id"] = rows
            print(session["user_id"][0][1])
            return redirect("/")    


        #elif nombre == gerente[0] and password == gerente[1]: #  and confirmar == password:
            #session["user_id"] = 1
        #else:
        #    print("usuario invalido")
        #    return render_template("login.html",error="Credenciales incorrectas")
            
    else : 
        return render_template("login.html")


@app.route("/productos" , methods=["GET", "POST"])
@login_required
def prueba():

    search = request.args.get("buscar")
    print(search)
    if search is None or search is '':
        print("mensaje")
        sql = "SELECT * FROM Producto WHERE Estado = 'si' " # recomiendo poner order by Stock desc
        cursor.execute(sql)
        resultados = cursor.fetchall()
    else:

        cadena_sin_espacios = search.replace(' ', '')

        if cadena_sin_espacios.isalpha():
            sql = "select *  from Producto where ESTADO = 'si' and NombreProducto like ? "
            resultados =cursor.execute(sql, ("%" + search +"%" ))
            resultados = cursor.fetchall()
        else:
            sql = "select *  from Producto where ESTADO = 'si' and  CodigoProducto = ? "
            resultados =cursor.execute(sql, (search))
            resultados = cursor.fetchall()


    # Paginar los resultados
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 12 # Cambia aquí el número de resultados por página que desees mostrar
    offset = (page - 1) * per_page
    productos_paginados = resultados[offset: offset + per_page]
    text = []
    for row in productos_paginados:
        id = row[0]
        imagens = row[7]
        color= row[2]
        talla = row[4]
        nombre = row[1]
        precio = row[3]
        stock = row[5]
        if imagens is None:
            text.append({'id': id , 'imagen':'None', 'color':color , 'talla' : talla , 'nombre':nombre , 'precio':precio , 'stock' : stock})
        else:
            imagen_base64 = base64.b64encode(imagens).decode('utf-8')
            text.append({'id': id , 'imagen':imagen_base64, 'color':color , 'talla' : talla , 'nombre':nombre , 'precio':precio , 'stock' : stock})
    pagination = Pagination(page=page, total=len(resultados), css_framework='bootstrap4', per_page=per_page)

    # Renderizar la plantilla con los resultados paginados y la paginación
    return render_template('productos.html', prueba=text, pagination=pagination)

@app.route("/compras" , methods=["GET", "POST"])
@login_required
def compras():
    sql = "select Nombreproveedor ,NombreProducto,CantidadEntrada,PrecioT,FechaEntrada from Proveedor join Proveedor_Producto on Proveedor.IDproveedor = Proveedor_Producto.IDproveedor join Producto on Producto.CodigoProducto = Proveedor_Producto.CodigoProducto WHERE Proveedor_Producto.ESTADO = 'si'"  
    cursor.execute(sql)
    registro = cursor.fetchall()
    return render_template("pp.html" , datos = registro)

@app.route("/ventas" , methods=["GET", "POST"])
@login_required
def ventas():
    sql = "select NombreProducto , NombreCliente, FechaSalida , CantidadSalida , PrecioProducto from Producto_Cliente join Producto on Producto.CodigoProducto =  Producto_Cliente.CodigoProducto join Cliente on Cliente.IDcliente = Producto_Cliente.IDcliente WHERE Producto_Cliente.ESTADO = 'si' "  
    cursor.execute(sql)
    registro = cursor.fetchall()
    return render_template("pc.html" , datos = registro)

@app.route("/empleado" , methods=["GET", "POST"])
@login_required
def empleado():
    opcion_seleccionada =  request.args.get('opcion') 
    sql = "SELECT * FROM {} WHERE ESTADO = 'si'".format(opcion_seleccionada)
    cursor.execute(sql)
    registro = cursor.fetchall()
    print(opcion_seleccionada)
    if opcion_seleccionada == "Empleado":
        return render_template("empleado.html" , datos = registro)
    elif opcion_seleccionada == "Proveedor":
        return render_template("proveedor.html" , datos = registro)
    elif opcion_seleccionada == "Producto":
        return render_template("productos.html" , datos = registro)
    else:
        return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")

@app.route("/" , methods=["GET", "POST"])
@login_required
def index():
    return render_template("futuro.html" )

#toda esta ruta es nueva 
@app.route("/edituser" , methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        name = 0
    else:
        sql = "select * from Usuarios"
        cursor.execute(sql)
        registro = cursor.fetchall()
        return render_template("edituser.html" , registro = registro)

if __name__ == '__main__':
    app.run()



