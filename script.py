
import pyodbc
from werkzeug.security import generate_password_hash , check_password_hash

try:##verificar que no haya ningun error al conectarse con la BF
    conexion =  pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-F9CVAAQJ\SQLEXPRESS;DATABASE=CopiaSystemKD;UID=TiendaKD;PWD=1234')
    #conexion =  pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-QUNO8C9;DATABASE=CopiaSystemKD;Trusted_Connection=yes;')
except:
    print("FAIL")

cursor = conexion.cursor()
sql = "insert into Usuarios (nombre , contraseña , correo) values ('admin' , ? , 'jeison@gmail.com')"
cursor.execute(sql  , generate_password_hash('12345'))
cursor.commit()





