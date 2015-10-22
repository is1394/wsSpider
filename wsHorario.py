#! /usr/bin/python2
# -*- encoding: utf-8 -*-

from suds.xsd.doctor import ImportDoctor, Import
from suds.client import Client
from tabulate import tabulate
import sys
import os

class Student():
    def __init__(self, name, lastname, idStudent):
        self.name = name
        self.lastname = lastname
        self.idStudent = idStudent

    def __str__(self):
        return " " + self.name + " " + self.lastname

class Subject():
    def __init__(self,code,name,course): #subject_code, name , course
        self.code = code
        self.name = name
        self.course = course

    def __str__(self):
        return (self.code + " " + self.name + "\n")

class Schedule():
    def __init__(self,name,start,end,day,cours,bloq):
        self.name = name
        self.day = day
        self.start=start.lstrip("PT")
        self.end=end.lstrip("PT")
        self.course=cours
        self.bloq = bloq

    def __str__(self):
        return ("MATERIA: " + self.name + "\n" + "DIA: " + self.day + "\n" + "BLOQUE: " + self.bloq + "\n" + "AULA: " + self.course + "\n" + "HORA INICIO: " + self.start + "\n" + "HORA FIN: " + self.end + "\n")

url = 'http://ws.espol.edu.ec/saac/wsandroid.asmx?WSDL'
imp = Import('http://www.w3.org/2001/XMLSchema') # the schema to import.
imp.filter.add('http://tempuri.org/')

doctor = ImportDoctor(imp)
client = Client(url, doctor=doctor)
subjects = []
recorded_subjs = []
subjsTabulate = []
students = []
name = sys.argv[1]
lastname = sys.argv[2]
name = unicode(name,"utf-8")
lastname = unicode(lastname,"utf-8")

if (name.isalpha() and lastname.isalpha()):
    #Return student's information
    Data = client.service.wsConsultarPersonaPorNombres(name,lastname)
    try:
        i = Data[1].__getitem__(0).__getitem__(0)
        i_name = i.NOMBRES
        i_lastname = i.APELLIDOS
        try:
            i_code = i.CODESTUDIANTE
            s=Student(i.NOMBRES, i.APELLIDOS, i.CODESTUDIANTE)
            print("\n"+s.name + " " + s.lastname + " " + s.idStudent  + "\n")
            COD_ESTUDIANTE = s.idStudent
        except:
            print("Esta persona no tiene matricula o.O " + i.NOMBRES + " " + i.APELLIDOS)
    except:
        for i in Data.diffgram.NewDataSet.DATOSPERSONA:
            i_name = i.NOMBRES
            i_lastname = i.APELLIDOS
            try:
                i_code = i.CODESTUDIANTE
                students.append(Student(i.NOMBRES, i.APELLIDOS, i.CODESTUDIANTE))
            except:
                #CASOS DE PERSONAS SIN MATRICULA CRISTIAN PEÑAFIEL MANUEL SUAREZ
                print ("\nEsta persona no tiene matricula: " + i.NOMBRES + " " + i.APELLIDOS)

        cont=1
        print ("\n\n")
        for i in students:
            print (str(cont) + " " + i.name + " " + i.lastname + " " + i.idStudent +"\n" )
            cont+=1

        op=input("Ingrese el numero de la persona a consultar: ")
        #return COD_ESTUDIANTE
        COD_ESTUDIANTE = students[int(op)-1].idStudent

    #return MATERIASREGISTRADAS
    gradesMat = client.service.wsMateriasRegistradas(COD_ESTUDIANTE)
    try:
        for i in gradesMat.diffgram.NewDataSet.MATERIASREGISTRADAS:
            subjects.append(Subject(i.COD_MATERIA_ACAD, i.NOMBRE, i.PARALELO))

    except:
        data= gradesMat[1].__getitem__(0).__getitem__(0)
        sub = Subject(data.COD_MATERIA_ACAD,data.NOMBRE,data.PARALELO)
        subjects.append(sub)


    for subject in subjects:
        #Return HORARIOCLASES
        data2= client.service.wsHorarioClases(subject.code,subject.course)
        try:
            for i in data2.diffgram.NewDataSet.HORARIOCLASES:
                sub =[]
                sub.append(i.NOMBRE)
                sub.append(i.HORAINICIO.lstrip("PT"))
                sub.append(i.HORAFIN.lstrip("PT"))
                sub.append(i.NOMBREDIA)
                sub.append(i.AULA)
                sub.append(i.BLOQUE)
                subjsTabulate.append(sub)
                #recorded_subjs.append(Schedule(i.NOMBRE,i.HORAINICIO,i.HORAFIN,i.NOMBREDIA,i.AULA,i.BLOQUE))
        except:
            sub = []
            sub.append(data2[1].__getitem__(0).__getitem__(0).NOMBRE)
            sub.append(data2[1].__getitem__(0).__getitem__(0).HORAINICIO.lstrip("PT"))
            sub.append(data2[1].__getitem__(0).__getitem__(0).HORAFIN.lstrip("PT"))
            sub.append(data2[1].__getitem__(0).__getitem__(0).NOMBREDIA)
            sub.append(data2[1].__getitem__(0).__getitem__(0).AULA)
            sub.append(data2[1].__getitem__(0).__getitem__(0).BLOQUE)
            subjsTabulate.append(sub)



    print ("\n\n")
    #for sub in recorded_subjs:
    #    print ("MATERIA: " + sub.name + "\n" + "DIA: " + sub.day + "\n" + "BLOQUE: " + sub.bloq + "\n" + "AULA: " + sub.course + "\n" + "HORA INICIO: " + sub.start + "\n" + "HORA FIN: " + sub.end + "\n")
    print (tabulate(subjsTabulate, headers=["MATERIA ","DIA ","BLOQUE ","AULA ","HORA INICIO ","HORA FIN "],tablefmt="fancy_grid"))
else:
    print("Invalido")
