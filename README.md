#### Web services ESPOL Spider.

##### Setup:

###### - Install dependecies:
	sudo pip2 install tabulate (Python2)
	sudo pip2 install suds	   (Python2)
  	sudo pip3 install tabulate (Python3)
	sudo pip3 install suds-jurko (Python3)


###### - Original Repository:
	https://github.com/juanmisak/wsSpider.git

###### - Run wsSpider:
	cd wsSpider
	chmod +x wsSpider.py
	./wsSpider.py FIRSTNAME LASTNAME YEAR TERM

###### - Run wsHorario:
	cd wsSpider
	chmod +x wsHorario.py
	./wsHorario.py FIRSTNAME LASTNAME

###### - Run wsMateriasDisponibles:
	cd wsSpider
	chmod +x wsMateriasDisponibles.py
	./wsMateriasDisponibles USERNAME
	
###### -Actually wsSpider, wsHorario, wsMateriasDisponibles are in Python 2
