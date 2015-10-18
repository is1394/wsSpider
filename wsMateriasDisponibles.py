#! /usr/bin/python2
# -*- encoding: utf-8 -*-

from suds.xsd.doctor import ImportDoctor, Import
from suds.client import Client
import sys
import os

class Student():
	def __init__(self,name,lastname,idStudent):
		self.name = name
		self.lastname = lastname
		self.idStudent = idStudent
	
	def __str_(self):
		return " " + self.name + " " + self.lastname

class Subject():
	courses = []
	def __init__(self,code,name): #subject_code, name , course
		self.code = code
		self.name = name

	def setCourses(self,tmp_courses):
		self.courses = tmp_courses

url='http://ws.espol.edu.ec/saac/wsandroid.asmx?WSDL'
imp = Import('http://www.w3.org/2001/XMLSchema')
imp.filter.add('http://tempuri.org/')

doctor = ImportDoctor(imp)
client = Client(url,doctor=doctor)

usrname = sys.argv[1]
usrname  = unicode(usrname,"utf-8")

student = None
subjects = []

if (usrname.isalpha()):
	#return information of the student
	Data = client.service.wsInfoUsuario(usrname)
	try:
		i=Data[1].__getitem__(0).__getitem__(0)
		i_name = i.NOMBRES
		i_lastname = i.APELLIDOS
		try:
			#id matricula
			i_id = i.IDENTIFICACION
			student = Student(i.NOMBRES,i.APELLIDOS,i.IDENTIFICACION)
			print("\n"+ student.name + " " + student.lastname + " Matricula: " + student.idStudent + "\n")
		except:
			print("error bajando matricula\n")
	except:
		print("mas de una persona? o.O\n")
	#return available subjects
	Data2 = client.service.wsMateriasDisponibles(student.idStudent)
	try:
		for i in Data2.diffgram.NewDataSet.MATERIASDISPONIBLES:
			#return  nombre_materia, cod_materia_acad
			s = Subject(i.COD_MATERIA_ACAD,i.NOMBRE_MATERIA)
			subjects.append(s)
	except:
		print("Error mientras bajaba materias\n")

for s in subjects:
	Data3 = client.service.wsBuscarMateria(s.code,1)
	tmp_courses = []
	try:
		for i in Data3.diffgram.NewDataSet.MATERIA:
			tmp_courses.append(i.PARALELO)
		s.setCourses(tmp_courses)
	except:
		tmp = Data3[1].__getitem__(0).__getitem__(0)
		tmp_courses.append(tmp.PARALELO)
		s.setCourses(tmp_courses)
	print s.name
	print s.courses
	#print ("\n")

"""
print("Total de materias: " + str(len(subjects)) + "\n")
i = 1
for sub in subjects:
	print (str(i)+ " " + sub.name)
	i +=1
	print (sub.courses) """
