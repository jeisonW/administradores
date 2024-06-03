CREATE DATABASE TIENDAKD;

USE TIENDAKD;

CREATE TABLE Proveedor(IDproveedor int IDENTITY(1,1) PRIMARY KEY, 
						Nombreproveedor VARCHAR(100) NOT NULL,
					    Correo NVARCHAR (50), Telefono NUMERIC(8) ,
					    Dirreccion NVARCHAR (100) , ESTADO VARCHAR(2) not null );

CREATE TABLE Usuarios (
  id int IDENTITY(1,1) PRIMARY KEY, 
  nombre VARCHAR(50),
  contraseña VARCHAR(20)
  ,correo  VARCHAR(100)
);

insert into Usuarios (nombre,contraseña,correo) values ('admin' , '12345', 'jeisonawebster@gmail.com') 

CREATE TABLE Empleado(IDempleado int IDENTITY(1,1) PRIMARY KEY,
					  NombreEmpleado VARCHAR(100) , 
					  Correo NVARCHAR (50), Telefono NUMERIC(8) ,Dirreccion NVARCHAR (50) , salario NVARCHAR(50) NOT NULL,
					  horas_t NVARCHAR(50), ESTADO VARCHAR(2) not null);

CREATE TABLE Cliente(IDcliente int IDENTITY(1,1) PRIMARY KEY,
					NombreCliente VARCHAR(100) , IDempleado int ,ESTADO VARCHAR(2)not null,
					CONSTRAINT FK_cliente FOREIGN KEY (IDempleado) REFERENCES Empleado(IDempleado));

CREATE TABLE Producto(CodigoProducto int IDENTITY(1,1) PRIMARY KEY, NombreProducto VARCHAR(50) NOT NULL ,
				    ColorProducto VARCHAR(20), PrecioProducto NUMERIC(20) ,
					Talla NUMERIC(5) ,Stock NVARCHAR(30) , ESTADO VARCHAR(2) not null , foto varbinary(max));

CREATE TABLE Desperfecto(CodigoSP int IDENTITY(1,1) PRIMARY KEY, Descripcion VARCHAR(50)  NOT NULL , 
						 FechaSalida  NVARCHAR(15) NOT NULL ,Cantidadsalida NUMERIC(20)  NOT NULL , CodigoProducto int , ESTADO VARCHAR(2) not null ,
						 CONSTRAINT FK_desperfecto FOREIGN KEY (CodigoProducto) REFERENCES Producto(CodigoProducto));

CREATE TABLE Categoria(CodigoCategoria int IDENTITY(1,1) PRIMARY KEY, NombreCategoria NVARCHAR(30), CodigoProducto int ,ESTADO VARCHAR(2) not null ,
					   CONSTRAINT FK_Categoria FOREIGN KEY (CodigoProducto) REFERENCES Producto(CodigoProducto));

CREATE TABLE Marca(CodigoMarca int IDENTITY(1,1) PRIMARY KEY, NombreMarca NVARCHAR(30), CodigoProducto int,  ESTADO VARCHAR(2) not null,
					   CONSTRAINT FK_Marca FOREIGN KEY (CodigoProducto) REFERENCES Producto(CodigoProducto));

CREATE TABLE Proveedor_Producto(CODIGOpp int IDENTITY(1,1) PRIMARY KEY ,FechaEntrada  NVARCHAR(15), CantidadEntrada NVARCHAR(30),PrecioT NUMERIC(20) , CodigoProducto int ,IDproveedor int , ESTADO VARCHAR(2) not null ,
								CONSTRAINT FK_Proveedor FOREIGN KEY (IDproveedor) REFERENCES Proveedor(IDproveedor),
								CONSTRAINT FK_PRODUCT FOREIGN KEY (CodigoProducto) REFERENCES Producto(CodigoProducto));

CREATE TABLE Producto_Cliente(CODIGOpc  int IDENTITY(1,1) PRIMARY KEY ,FechaSalida  NVARCHAR(15), CantidadSalida NVARCHAR(30) NOT NULL, CodigoProducto int, IDcliente int , ESTADO VARCHAR(2) not null,
							  CONSTRAINT FK_ClienteP FOREIGN KEY (IDcliente) REFERENCES Cliente(IDcliente),
							  CONSTRAINT FK_Producto FOREIGN KEY (CodigoProducto) REFERENCES Producto(CodigoProducto));

insert into Empleado(NombreEmpleado,Correo,Telefono,Dirreccion,salario,horas_t,Estado) VALUES
					('Jose Eduardo Perez Garcias','Joseeduardo21@gmail.com','77281547','Parque Dario, 1/2 cuadra arriba','5,000','5','si'),
					('Jennifer Margarita Rodriguez Lopez','JenniRodrguez561@gmail.com','7777147','Plaza Inter, 1 cuadra al Sur, 1 cuadra al Oeste','5,500','6','si'),
					('Carlos Emilio Flores Garcias','CarlosEmilio23@gmail.com','87381647','Del Reloj, 1 cuadra abajo','2,000','3','si'),
					('Maria Fernanda Gutierrez Mena','MariferGutierrez@gmail.com','77281111','Km 19 Carretera a Ticuantepe','7,000','8','si'),
					('Luisa Emilia Acu�a Pereira' , 'Pereiraacu?a23@gmail.com','88481547','Sem?foros del Zumen, 50 varas al Sur','7,000','8','si'),
					('ashly Massiel Arauz Rodriguez','massielRodrigues24@gmail.com','7281667','Sem?foros del Zumen, 20 varas al Sur','7,000','8','si'),
					('Jorge Carlos avenda�o Garcias','Avenda?oGarcia.J@gmail.com','83283547','Barrio San Judas, Los Cocos, 3 cuadras abajo','5,000','5','si'),
					('Jose Eduardo Beneditt Ayala','BenedittJos26@gmail.com','77584154','Barrio San Judas, Los Cocos, 5 cuadras arriba','7,000','6','si'),
					('Josue Danilo Ortiz Duran','DaniloOrtiz@gmail.com','77282940','Contiguo a Escuela Salvador Mendieta','2,000','3','si'),
					('kenia Isallana Mondragon Mena','KeniaMondragon@gmail.com','87302057','ciudad sandino zona 8 frente al parque','2,000','3','si');

insert into Cliente(NombreCliente ,Correo, Telefono , Dirreccion,IDempleado,ESTADO)
		   values('Maria Jose Flores Mesa','MariaMesa@gmail.com','87348817','ciudad sandino del pali 1/2 abajo','3','si')
				,('karla Patricia Perez Martinez','KPerez38@gmail.com','87208520','barrio la reynaga de la gasolinera puma 200 mts al oeste','1','si')
				,('Fabiola Sofia Mesa Guzman','Guzmanfabi07@gmail.com','85348811','barrio santana','6','si')
				,('Daniel Eduardo Solis Perez','Solisduardo78@gmail.com','77340217','rotonda el periodista 2 cuadras al sur','1','si')
				,('Oscar Isaac Larios estrada','OLariosEstrada@gmail.com','87772020','del antiguo velez pais media 1/2 arriba','5','si')
				,('Pablo Javier Hernandez Orozco','H.O.pablo68@gmail.com','85330402','Rotonda El G?eg?ense, 2 cuadras arriba','3','si')
				,('Maria Concepcion Torrez Sandoval','MariaConcepciontorrez@gmail.com','87348817','Plaza Inter, 1 cuadra al Sur, 1 cuadra al Oeste','2','si')
				,('maria Jose Gutierrez Mesa','mariaG384@gmail.com','77183617','Sem?foros del Zumen, 50 varas al Sur','4','si')
				,('Luis Enrique Millon Gutierrez','luisMillon23@gmail.com','87888817','Pista Juan Pablo II, contiguo a Union Fenosa','1','si')
				,('Jason Alexander Flores Gonzalez','GonzalesAxel@gmail.com','85541201','De la Subasta 10 vrs al lago, frente a Caf? Soluble','1','si')
				,('Jennifer Alexa Tiffer Torrez','AlexaTiffer02@gmail.com','87348817','De donde fue el cine Cabrera 1 cuadra al Norte','1','si')
				,('Imara Sofia flores Mesa','Sofiamesa30@gmail.com','83202034','Costado oeste del parque central','1','si')
				,('Karla Daniela Gonzales Celedon','GonzalesCeledon56@gmail.com','74444447','Barrio San Judas, Los Cocos, 3 cuadras arriba','6','si')
				,('Isallana Ester Carrion Lopez','CarrionIsa@gmail.com','87355798','Frente a Iglesie Santa Ana','8','si')
				,('Olga Sofia Medal Lara','Laramedalsofi@gmail.com','81127676','Contiguo a Escuela Salvador Mendieta','9','si')
				,('Kenia Ibet Ayala Guzman','GuzmanKenia54@gmail.com','86262817','Entrada a reparto Cailagua, 20 varas al Sur','3','si')
				,('Scarleth veronica Lara Mena','SLaraMena44@gmail.com','87348817','Puente Le?n 2 cuadras abajo','5','si')
				,('Maria Rosario flores Celedon','Rosaceledon21@gmail.com','74748817','De la Parroquia, 3 1/2 cuadras al Sur','6','si')
				,('Katherine Johana beneditt Romero','Katbeneditt@gmail.com','79148817','Rotonda El G?eg?ense, 1 cuadras arriba','6','si')
				,('Eliezer Ezequiel Castillo Lopez','ezequielCastillo.L23@gmail.com','87348817','Cl?nica Santa Mar?a, 1 cuadra al Sur, 20 varas abajo','3','si')

INSERT INTO   Producto(NombreProducto  , ColorProducto  , PrecioProducto  , Talla ,Stock,ESTADO ) 
VALUES					('Air jordan V','Negro', 1200, 40,'0','si'),
						('Air jordan V','Negro', 1200, 42,'3','si'),
						('Air jordan VIII','Blanco', 1200, 39,'5','si'),
						('Air jordan VIII' ,'Negro', 1200, 41,'15','si'),
						('Air jordan retro IV','Negro', 900, 37,'12','si'),
						('Air jordan retro IV','Blanco', 900, 36,'7','si'),
						('Air jordan I','Rojo', 1200, 42,'15','si'),
						('Air jordan I','Azul', 900, 36,'45','si'),
						('Air jordan I','Gris', 900, 38,'17','si'),
						('Chuck Taylor All Star Classic','Blanco', 1390, 40,'18','si'),
						('Chuck Taylor All Star Classic','Negro', 1390, 41,'5','si'),
						('Chuck Taylor All Star Classic','Blanco', 1390, 43,'11','si'),
						('Chuck 70 Vintage Canvas','Blanco', 1100, 42,'3','si'),
						('Chuck 70 Vintage Canvas','Blanco', 1100, 41,'5','si'),
						('Chuck 70 Vintage Canvas','Blanco', 990, 36,'2','si'),
						('Chuck 70 Vintage Canvas','Blanco', 1100, 44,'12','si'),
						('Doble Plataforma Bratz Premium Berry','Vinil piel', 2200, 40,'3','si'),
						('Doble Plataforma Bratz Premium Berry','Vinil piel', 2200, 41,'1','si'),
						('Doble Plataforma Bratz Premium Berry','Vinil piel', 2200, 44,'2','si'),
						('Doble Plataforma Bratz Premium Berry','Vinil piel', 2200, 42,'3','si'),
						('Plataforma Modelo Elevate','Negro', 2500, 41,'5','si'),
						('Plataforma Modelo Elevate','Rojo', 2500, 40,'10','si'),
						('Sam Edelman Felicia Ballet Flat','Negro', 200, 41,'6','si'),
						('Sam Edelman Felicia Ballet Flat','Negro', 200, 43,'7','si'),
						('Air force one','Blanco',990, 42,'10','si'),
						('Air force one','Blanco',990, 43,'6','si'),
						('Literide Clog','Rojo con negro',1100, 40,'24','si'),
						('Literide Clog','Rojo con negro',1100, 41,'25','si');

INSERT INTO Proveedor
   ( Nombreproveedor ,
	Correo, 
	Telefono,
	Dirreccion,ESTADO)
  VALUES  
		('Maritza Noemi Molina Orellana','Noemi110@gmail.com',88125692,'Barrio San Judas, de la pulperia el gordo 2 cuadras al sur' , 'si'),
		('Luis Fernando Pereira Roda','PereiraFern45@gmail.com',85103300,'Anexo Las Brisas, Colegio Bautista 1 cuadras al este','si'),
		('Ernestina Graciela Leon Gonzalez','Gracielaleon@hotmail.com',78359120,'Anexo La Primavera','si'),
		('Pablo Roberto Perez Lozano','PerezRobertoPabl@hotmail.com',22639825,'Batahola Sur','si'),
		('Fredy Xavier Enriquez Godoy','Fredy.Enrique12@gmail.com',71496325,'Colonia M?ntica','si'),
		('Flavio Rodolfo Garcia Bercian','FlavGarc123@gmail.com',22356912,'Linda Vista Sur','si'),
		('Rosa Miriam Perez','PerezGarcRosa@hotmail.com',80126345,'Los Martinez','si'),
		('Hugo Alberto Vasquez Sandoval','Sandoval.Hugo77@hotmail.com',70569812,'Reparto Espa�a','si'),
		('Patricia Eugeni Velez Zambrano','Eugen23zambrano@gmail.com',55628910,'San Jos? Boer','si'),
		('Rafael Oswaldo Cruz Arias','oswaldoRafa8@gmail.com',88126394,'Batahola Sur','si'),
		('Heydi Tatiana Perez Barrios','heydiperez@hotmail.com',52143089,'La Primavera','si'),
		('Fernando David Acosta Duque','duque_fernado8@hotmail.com',55628910,'Jardines de Managua','si'),
		('Arelis Lisseth Flores Rivas','rivasAreli22@gmail.com',77635810,'Reparto Rubenia','si'),
		('Daniel Jose Mendoza Guerrero','joseMendz@hotmail.com',20156930,'Sur Villa Venezuela','si'),
		('Teresa Alejandra Chavez Mora','teresa_mora34@gmail.com',55320153,'Urbanizaci?n Progresiva villa libertad','si'),
		('Oscar Gabriel Garcia Romero','garcia2romero@gmail.com',25637812,'Reparto Villa Flor','si'),
		('Veronica Aleksandra Ramirez Callejo','verocallejo987@gmail.com',86521022,'Residencial Las Mercedes','si'),
		('Mario Javier Acu�a Rivas','mario_rivas2@hotmail.com',56321496,'Villa libertad','si'),
		('Martha Lucia Herrera Nicaragua','lucHerrera@gmail.com',88512365,'Villa Japon','si'),
		('Maria Elena Lopez Rodriguez','LMaria@gmail.com',22523018,'Monse?or Lezcano','si');


INSERT INTO Proveedor_Producto(FechaEntrada , CantidadEntrada,PrecioT , CodigoProducto,IDproveedor, ESTADO) VALUES 
								('2022-1-24','7',7000,'1','1','si'),
								('2022-3-12','3',3000,'2','1','si'),
								('2021-12-12','15',15000,'4','11','si'),
								('2022-1-24','5',5000,'3','4','si'),
								('2022-1-24','12',12000,'5','3','si'),
								('2022-1-24','3',3000,'6','5','si'),
								('2021-2-24','4',4000,'6','3','si'),
								('2022-1-24','15',15000,'7','9','si'),
								('2021-11-13','30',30000,'8','4','si'),
								('2022-1-24','15',15000,'8','5','si'),
								('2022-4-24','17',17000,'9','6','si'),
								('2021-10-12','18',18000,'10','19','si'),
								('2020-5-4','5',6000,'11','17','si'),
								('2020-8-4','11',13200,'12','16','si'),
								('2022-3-17','3',2700,'13','14','si'),
								('2020-5-4','5',4500,'14','11','si'),
								('2020-7-4','2',1600,'15','12','si'),
								('2022-5-14','12',10800,'16','19','si'),
								('2021-10-22','3',4800,'17','8','si'),
								('2022-12-6','1',160,'18','17','si'),
								('2020-5-4','2',3000,'19','4','si'),
								('2022-8-22','3',4500,'20','17','si'),
								('2022-6-27','5',10000,'21','12','si'),
								('2020-5-4','10',20000,'22','7','si'),
								('2022-3-16','6',300,'23','15','si'),
								('2020-5-4','7',350,'24','12','si'),
								('2022-12-10','10',8000,'25','10','si'),
								('2022-11-25','6',4800,'26','6','si'),
								('2020-5-4','24',21600,'27','12','si'),
								('2022-5-4','25',22500,'28','17','si');

INSERT INTO Producto_Cliente(FechaSalida, CantidadSalida , CodigoProducto , IDcliente ,ESTADO) VALUES
							('2022-11-6','2','1','1','si'),
							('2022-4-5','1','12','5','si'),
							('2022-1-4','5','28','9','si'),
							('2022-7-11','7','27','4','si'),
							('2022-9-23','2','6','10','si'),
							('2022-10-18','1','9','9','si');

INSERT INTO Desperfecto
	(Descripcion, 
	 FechaSalida,
	 Cantidadsalida, 
	 CodigoProducto,ESTADO)

VALUES
		('Sin cordones','2022-10-15','1','1','si'),
		('Par perdido','2022-06-05','2','2','si'),
		('Etiquetas desprendidas','2022-02-08','4','27','si'),
		('Botas con cremallera da?ada','2022-06-20','1','17','si'),
		('Error de fabrica talla incorrecta','2022-08-26','2','25','si'),
		('Despegado','2022-05-06','2','23','si'),
		('Sin cordones','2022-08-10','1','3','si'),
		('Forro interior da?ado','2022-07-20','3','14','si'); 
		
INSERT INTO Categoria(NombreCategoria , CodigoProducto, ESTADO) VALUES 
						('Deportivo','1','si'),
						('Deportivo','2','si'),
						('Deportivo','3','si'),
						('Deportivo','4','si'),
						('Deportivo','5','si'),
						('Deportivo','6','si'),
						('Deportivo','7','si'),
						('Deportivo','8','si'),
						('Deportivo','9','si'),
						('Zapatos casual','10','si'),
						('Zapatos casual','11','si'),
						('Zapatos casual','12','si'),
						('Zapatos casual','13','si'),
						('Zapatos casual','14','si'),
						('Zapatos casual','15','si'),
						('Zapatos casual','16','si'),
						('Botas','17','si'),
						('Botas','18','si'),
						('Botas','19','si'),
						('Botas','20','si'),
						('Sandalias Plataforma','21','si'),
						('Sandalias Plataforma','22','si'),
						('Zapatos casual','23','si'),
						('Zapatos casual','24','si'),
						('Deportivo','25','si'),
						('Deportivo','26','si'),
						('Sandalias','27','si'),
						('Sandalias','28','si');

INSERT INTO Marca( NombreMarca , CodigoProducto ,ESTADO) VALUES 
						('Nike','1','si'),
						('Nike','2','si'),
						('Nike','3','si'),
						('Nike','4','si'),
						('Nike','5','si'),
						('Nike','6','si'),
						('Nike','7','si'),
						('Nike','8','si'),
						('Nike','9','si'),
						('Converse','10','si'),
						('Converse','11','si'),
						('Converse','12','si'),
						('Converse','13','si'),
						('Converse','14','si'),
						('Converse','15','si'),
						('Converse','16','si'),
					    ('Berry','17','si'),
						('Berry','18','si'),
						('Berry','19','si'),
						('Berry','20','si'),
                        ('Bamboo','21','si'),
						('Bamboo','22','si'),
						('Flats','23','si'),
						('Flats','24','si'),
						('Nike','25','si'),
						('Nike','26','si'),
						('Crocs','27','si'),
						('Crocs','28','si');