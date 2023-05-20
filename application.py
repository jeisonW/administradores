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
    conexion =  pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-F9CVAAQJ\SQLEXPRESS;DATABASE=copiatiendakd;UID=TiendaKD;PWD=1234')
    #Conexion pa mi compu Harvin xd
    #conexion =  pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-QUNO8C9;DATABASE=tiendakdcopia;Trusted_Connection=yes;')
except:
    print("FAIL")

cursor = conexion.cursor()

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        name = request.form.get("usuario")
        password = request.form.get("password")
        #confirmar = request.form.get("confirmar")
        #query = text("SELECT id, password FROM ser WHERE name = :name")
        #rows = db.execute(query, {"name": name}).fetchall()
        #if len(rows) < 1 or not check_password_hash(rows[0][1], password):
        #    return render_template("login.html" , error_msg="Nombre de usuario o contraseña incorrecta")

        if name == admins[0] and password == admins[1]: #and confirmar == password:
            session["user_id"] = 0
        elif name == gerente[0] and password == gerente[1]: #  and confirmar == password:
            session["user_id"] = 1
        else:
            print("usuario invalido")
            return render_template("login.html",error="Credenciales incorrectas")
            
        return redirect("/")
 
    else : 
        return render_template("login.html")


@app.route("/productos" , methods=["GET", "POST"])
@login_required
def prueba():
    sql = "SELECT * FROM Producto WHERE Estado = 'si' " # recomiendo poner order by Stock desc
    cursor.execute(sql)
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
    return render_template("layout.html" )



if __name__ == '__main__':
    app.run()



