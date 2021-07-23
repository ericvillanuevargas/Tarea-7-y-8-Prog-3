import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class VacunaPrimeraVez(BaseModel):
    Cedula:str
    Nombre:str
    Apellido:str
    Telefono:str
    Fecha_Nacimiento:str
    Zodiaco:str
    Cedula:str
    NombreVacuna:str
    Provincia:str
    Fecha:str

class VacunaSeguimiento(BaseModel):
    Cedula:str
    NombreVacuna:str
    Provincia:str
    Fecha:str


@app.get("/")
def root():
    return {'Sistema': 'ApiVacunaRD'}

@app.get("/api/ConsultarCedula/{cedula}")
def ConsultarCedula(cedula:str):
    Cedul=""
    conexion = sqlite3.connect('BaseDeDatos.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT Cedula FROM Pacientes WHERE Cedula = '"+cedula+"'")
    contenido = cursor.fetchall()
    for i in contenido:
        Cedul = i[0]
    if cedula == Cedul:
        return True
    else:
        return False

@app.post("/api/NuevaVacunacion")
def NuevaVacunacion(a:VacunaPrimeraVez):
    try:
        conexion = sqlite3.connect('BaseDeDatos.db')
        cursor = conexion.cursor()
        DatosPaciente = (a.Cedula,a.Nombre,a.Apellido,a.Telefono,a.Fecha_Nacimiento,a.Zodiaco)
        TablaVacuna = (a.Cedula,a.NombreVacuna,a.Provincia,a.Fecha)
        sql = '''INSERT INTO Pacientes(Cedula,Nombre,Apellido,Telefono,Fecha_Nacimiento,Zodiaco)VALUES(?,?,?,?,?,?)'''
        sql2 = '''INSERT INTO NuevasDosisVacuna(Cedula,NombreVacuna,Provincia,Fecha)VALUES(?,?,?,?)'''
        cursor.execute(sql, DatosPaciente)
        cursor.execute(sql2, TablaVacuna)
        conexion.commit()
        return {"ok":True}
    except:
        return {"ok":False}

@app.post("/api/VacunaSeguimiento")
def VacunaSeguimientos(a:VacunaSeguimiento):
    try:
        conexion = sqlite3.connect('BaseDeDatos.db')
        cursor = conexion.cursor()
        TablaVacuna = (a.Cedula,a.NombreVacuna,a.Provincia,a.Fecha)
        sql2 = '''INSERT INTO NuevasDosisVacuna(Cedula,NombreVacuna,Provincia,Fecha)VALUES(?,?,?,?)'''
        cursor.execute(sql2, TablaVacuna)
        conexion.commit()
        return {"ok":True}
    except:
        return {"ok":False}

@app.delete("/api/EliminarVacunaSeguimiento/{idd}")
def EliminarVacunaSeguimiento(idd:str):
    try:
        conexion = sqlite3.connect('BaseDeDatos.db')
        cursor = conexion.cursor()
        cursor.execute("Delete from NuevasDosisVacuna where IdDosis = '"+idd+"' ")
        conexion.commit()
        return {"ok":True}
    except:
        return {"ok":False}

@app.get("/api/ConsultaDeVacunados")
def ConsultaDeVacunados():
    Datos = []
    conexion = sqlite3.connect('BaseDeDatos.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT U.IdPacientes, U.Cedula,U.Nombre, U.Apellido, U.Telefono,U.Fecha_Nacimiento, U.Zodiaco, count(V.Cedula) As Cantidad FROM Pacientes AS U INNER JOIN NuevasDosisVacuna AS V ON U.Cedula = V.Cedula  GROUP BY U.IdPacientes, U.Cedula,U.Nombre, U.Apellido, U.Telefono,U.Fecha_Nacimiento, U.Zodiaco ')
    contenido = cursor.fetchall()
    conexion.commit()
    for i in contenido:
        Datos.append({"IdUsuario":i[0],"Cedula":i[1],"Nombre": i[2], "Apellido": i[3], "Telefono": i[4],"Fecha_Nacimiento":i[5],"Zodiaco":i[6],"Cantidad":i[7]})
    return Datos

@app.get("/api/ConsultaDeVacunadoUnico/{NombreOApellido}")
def ConsultaDeVacunadoUnico(NombreOApellido:str):
    Datos = []
    idf = 0
    Cedula=""
    Nombre=""
    Apellido=""
    Telefono=""
    Fecha_Nacimiento=""
    Zodiaco=""
    Cantidad=""
    conexion = sqlite3.connect('BaseDeDatos.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT U.*, Count(V.IdDosis) As Cantidad FROM Pacientes AS U INNER JOIN NuevasDosisVacuna AS V ON U.Cedula = V.Cedula WHERE U.Nombre = '"+NombreOApellido+"' or U.Apellido= '"+NombreOApellido+"' GROUP BY U.idPacientes,U.Cedula, U.Nombre, U.Apellido,U.Telefono,U.Fecha_Nacimiento,U.Zodiaco")
    contenido = cursor.fetchall()
    conexion.commit()
    for i in contenido:
        idf = i[0]
        Cedula=i[1]
        Nombre= i[2]
        Apellido= i[3]
        Telefono= i[4]
        Fecha_Nacimiento=i[5]
        Zodiaco=i[6]
        Cantidad=i[7]
    cursor.execute("select IdDosis, NombreVacuna, Provincia,Fecha from NuevasDosisVacuna WHERE Cedula = '"+Cedula+"'")
    contenido2 = cursor.fetchall()
    for i in contenido2:
        Datos.append({"IdDosis": i[0],"NombreVacuna":i[1], "Provincia":i[2], "FechaVacunacion":i[3]})

    return {"idUsuario":idf,"Cedula":Cedula,"Nombre": Nombre, "Apellido": Apellido, "Telefono": Telefono,"Fecha_Nacimiento":Fecha_Nacimiento
                    ,"Zodiaco":Zodiaco,"Cantidad":Cantidad, "DatosVAcunas": Datos}

@app.get("/api/VacunadosPorProvincia/{provincia}")
def VacunadosPorProvincia(provincia:str):
    Datos = []
    conexion = sqlite3.connect('BaseDeDatos.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT U.Cedula,U.Nombre, U.Apellido,U.Telefono,V.NombreVacuna,V.Provincia,V.Fecha,U.IdPacientes FROM Pacientes AS U INNER JOIN NuevasDosisVacuna AS V ON U.Cedula = V.Cedula WHERE V.Provincia = '"+provincia+"' GROUP BY U.Cedula, U.Nombre,U.Apellido,U.Telefono,V.NombreVacuna,V.Provincia,V.Fecha,U.IdPacientes")
    contenido = cursor.fetchall()
    conexion.commit()
    for i in contenido:
        Datos.append({"ok":True,"Cedula":i[0],"Nombre": i[1], "Apellido": i[2], "Telefono": i[3],"NombreVacuna":i[4],
                    "Provincia":i[5],"Fecha_Vacunacion":i[6], "IdUsuario":i[7]})
    if Datos == []:
        return {"ok":False}
    else:
        return Datos

@app.get("/api/VacunadosPorMarcaDeVacuna")
def VacunadosPorMarcaDeVacuna():
    Datos = []
    conexion = sqlite3.connect('BaseDeDatos.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT NombreVacuna, count(IdDosis) as Cantidad from NuevasDosisVacuna WHERE NombreVacuna = NombreVacuna GROUP BY NombreVacuna')
    contenido = cursor.fetchall()
    conexion.commit()
    for i in contenido:
        Datos.append({"ok":True,"NombreVacuna":i[0],"Cantidad":i[1]})
    if Datos == []:
        return {"ok":False}
    else:
        return Datos

@app.get("/api/VacunadosPorZodiaco")
def VacunadosPorZodiaco():
    Datos = []
    conexion = sqlite3.connect('BaseDeDatos.db')
    cursor = conexion.cursor()
    cursor.execute('Select Zodiaco, Count(IdPacientes) as Cantidad from Pacientes where Zodiaco = Zodiaco GROUP BY Zodiaco')
    contenido = cursor.fetchall()
    conexion.commit()
    for i in contenido:
        Datos.append({"ok":True,"Zodiaco":i[0],"Cantidad":i[1]})
    if Datos == []:
        return {"ok":False}
    else:
        return Datos

@app.delete("/api/EliminarRegistroVacunado/{IdUser}")
def EliminarRegistroVacunado(IdUser:str):
    try:
        Cedula = ""
        conexion = sqlite3.connect('BaseDeDatos.db')
        cursor = conexion.cursor()
        cursor.execute("Select Cedula from NuevasDosisVacuna where IdDosis = '"+IdUser+"'")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            Cedula = i[0]
        cursor.execute("Delete from Pacientes where IdPacientes = '"+IdUser+"'")
        cursor.execute("Delete from NuevasDosisVacuna where Cedula = '"+Cedula+"'")
        return {"ok":True}
    except TypeError as e:
        return e

#CRUD PROVINCIAS

#Select All
@app.get("/api/Provincias")
def Provincias():
    try:
        Datos =[]
        conexion = sqlite3.connect('BaseDeDatos.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT IdProvincia, Nombre_Provincia FROM Provincias")
        contenido = cursor.fetchall()
        for i in contenido:
            Datos.append({"ok":True,"IdProvincia":i[0],"NombreProvincia":i[1]})
        if Datos == []:
            return {"ok":False}
        else:
            return Datos
    except TypeError:
        return{"ok":False}
#Create
@app.post("/api/NuevaProvincia/{Nombre}")
def NuevaProvincia(Nombre:str):
    try:
        N = ""
        conexion = sqlite3.connect('BaseDeDatos.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT Nombre_Provincia FROM Provincias WHERE Nombre_Provincia = '"+Nombre+"'")
        contenido = cursor.fetchall()
        for i in contenido:
            N = i[0]
        if Nombre == N:
            return {"ok":False}
        else:
            sql = "INSERT INTO Provincias(Nombre_Provincia)VALUES('"+Nombre+"')"
            cursor.execute(sql)
            conexion.commit()
            return {"ok":True}
    except TypeError:
        return{"ok":False}
#UPDATE
@app.put("/api/ActualizarProvincia/{IdProvincia}/{NuevoNombre}")
def ActualizarProvincia(IdProvincia:str,NuevoNombre:str):
    try:
        conexion = sqlite3.connect('BaseDeDatos.db')
        cursor = conexion.cursor()
        cursor.execute("Update Provincias set Nombre_Provincia = '"+NuevoNombre+"' where IdProvincia = '"+IdProvincia+"'")
        conexion.commit()
        return {"ok":True}
    except:
        return {"ok":False}
#Delete
@app.delete("/api/EliminarProvincia/{IdProvincia}")
def EliminarProvincia(IdProvincia:str):
    try:
        conexion = sqlite3.connect('BaseDeDatos.db')
        cursor = conexion.cursor()
        cursor.execute("Delete from Provincias where IdProvincia = '"+IdProvincia+"'")
        conexion.commit()
        return {"ok":True}
    except:
        return {"ok":False}

#CRUD VacunasExistente

#Select All
@app.get("/api/VacunasExistente")
def VacunasExistente():
    try:
        Datos =[]
        conexion = sqlite3.connect('BaseDeDatos.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT IdVacuna, Nombre_Vacuna FROM VacunasConDisponibilidad")
        contenido = cursor.fetchall()
        for i in contenido:
            Datos.append({"ok":True,"IdVacuna":i[0],"NombreVacuna":i[1]})
        if Datos == []:
            return {"ok":False}
        else:
            return Datos
    except TypeError:
        return{"ok":False}
#Create
@app.post("/api/NuevoNombreVacuna/{Nombre}")
def NuevoNombreVacuna(Nombre:str):
    try:
        N=""
        conexion = sqlite3.connect('BaseDeDatos.db')
        cursor = conexion.cursor()
        sql = "INSERT INTO VacunasConDisponibilidad(Nombre_Vacuna)VALUES('"+Nombre+"')"
        cursor.execute(sql)
        conexion.commit()
        return {"ok":True}
    except:
        return{"ok":False}
#UPDATE
@app.put("/api/ActualizarVacuna/{IdVacuna}/{NuevoNombre}")
def ActualizarVacuna(IdVacuna:str,NuevoNombre:str):
    try:
        conexion = sqlite3.connect('BaseDeDatos.db')
        cursor = conexion.cursor()
        cursor.execute("Update VacunasConDisponibilidad set Nombre_Vacuna = '"+NuevoNombre+"' where IdVacuna = '"+IdVacuna+"'")
        conexion.commit()
        return {"ok":True}
    except:
        return {"ok":True}

#Delete
@app.delete("/api/EliminarVacuna/{IdVacuna}")
def EliminarVacuna(IdVacuna:str):
    try:
        conexion = sqlite3.connect('BaseDeDatos.db')
        cursor = conexion.cursor()
        cursor.execute("Delete from VacunasConDisponibilidad where IdVacuna = '"+IdVacuna+"'")
        conexion.commit()
        return {"ok":True}
    except:
        return {"ok":True}
