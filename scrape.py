#!/usr/bin/env python
# -*- encoding: Latin-1 -*-

import urllib
import urllib2
import re
from random import randrange
import time
from decimal import Decimal
from bs4 import BeautifulSoup

import sys  
reload(sys)  
sys.setdefaultencoding('iso-8859-1')

PortalesList = [
    'http://www.laestokada.cl/foro/index.php/rss/forums/2-anuncios-de-chicas-escorts-hasta-30lks/',
    'http://www.laestokada.cl/foro/index.php/rss/forums/3-anuncios-de-chicas-escorts-sobre-35lks/',
    'http://www.laestokada.cl/foro/index.php/forum/335-anuncios-de-chicas-escorts-sobre-50lks/',
    'http://www.planetaescort.cl/_js/ajax/cargar_portadas.php?vip=1',
    'http://www.planetaescort.cl/_js/ajax/cargar_portadas.php?premium=1',
    'http://www.planetaescort.cl/_js/ajax/cargar_portadas.php?gold=1',
    'http://www.sexo.cl/?id=996&bTodas=1',
    'http://www.relaxchile.cl/destacadas_vip',
    'http://www.relaxchile.cl/destacadas_top',
    'http://www.relaxchile.cl/destacadas',
    'http://miprivado.cl/',
    'http://infiernohot.cl/',
    #'http://www.elsilencio.cl/',
    #'http://www.laestocada.cl/content.php',
    #'http://miescort.cl/',
    #'http://ponelo.cl/premium/'
    ]

sql = ''
row = ''
anchorLenLista = []
ubicacionLenLista = []
serviciosLenLista = []
adicionalesLenLista = []
iTime = 1500
fTime = 3000
sTime = 153

try :
    for urls in PortalesList :
        #htmlfile = urllib.urlopen(urls)
        #html = htmlfile.read()
        request = urllib2.Request(urls)
        request.add_header('User-Agent', 'Mozilla/5.0')
        opener = urllib2.build_opener()
        html = opener.open(request).read()
        html = html.replace('&aacute;','á').replace('&eacute;','é').replace('&iacute;','í').replace('&oacute;','ó').replace('&uacute;','ú')
        html = html.replace('&Aacute;','Á').replace('&Eacute;','É').replace('&Iacute;','Í').replace('&Oacute;','Ó').replace('&Uacute;','Ú')
        html = html.replace('&ntilde;','ñ').replace('&Ntilde;','Ñ')
    
        # La EstoKada Scraper:
        if len (re.findall(r'laestokada', urls)) :
            if len (re.findall('<rss version="2.0">', html)) :
                html = html.decode('iso-8859-1').replace('&#160;',' ').replace('&nbsp;',' ')
                # Getting Data Escort from LEK 30K & 40K Pages :
                EscortDataBlocks = html.split('</ttl>')[1].split('</item>')
                row = ''
                for EscortData in EscortDataBlocks :
                    if not re.findall(r'<item>', EscortData) : break
                
                    sql = sql + 'INSERT INTO escortssantiago(Escort,Edad,Tarifa,Telefono,Estatura,Busto,Cintura,Culo,Hasta_Dia,Inicio,Termino,Lugar,Servicios,Adicionales) VALUES ('
        
        			# Getting Escort Name (one or two words):
                    if len (re.findall(r'<title>', EscortData)) :
                        nombre = EscortData.split('<title>')[1].split('</title>')[0]
                        print '\n======================== Escort LEK Inicia ===================\n', 'Nombre :', nombre
        
        			# Getting Link of Escort Page:
                    enlace = 'http://www.laestokada.cl/foro/'
                    if len (re.findall(r'<link>', EscortData)) :
                        enlace = EscortData.split('<link>')[1].split('</link>')[0]
                    anchor = '<a href="' + enlace + '" target="_blank">' + nombre + '</a>'
                    anchorLenLista += [len(anchor)]
                    sql = sql + '\'' + anchor + '\''
                    row = anchor
                
        			# Getting Escort Age:
                    edad = 'null'
                    if len(re.findall(r'[Ee]dad\W*\d+', EscortData)) :
                        edad = re.findall(r'[Ee]dad\W*(\d+)', EscortData)[0]
                    sql = sql + ',' + edad
                    row = row + ',' + edad
                
        			# Getting Escort Rate:
                    tarifa = 'null'
                    if len (re.findall(r'[Vv][Aa][Ll][Oo][Rr]', EscortData)) :
                        if len (re.findall(r'\W*\$\W*\d+\.\d+', EscortData)) :
                            tarifa = re.findall(r'\W*\$\W*(\d+\.\d+)', EscortData)[0]
                    tarifa = tarifa.replace('.','')
                    sql = sql + ',' + tarifa
                    row = row + ',' + tarifa
            
        			# Getting Escort Phone Number: 
                    telefono = 'null'
                    if len (re.findall(r'\+569\W*\d{8}', EscortData)) :
                        telefono = re.findall(r'\+569\W*(\d{8})', EscortData)[0]
                    elif len (re.findall(r'[0-9]{8}', EscortData)) :
                        telefono = re.findall(r'([0-9]{8})', EscortData)[0]
                    sql = sql + ',' + telefono
                    row = row + ',' + telefono
            
        			# Getting Escort Height: 
                    estatura = 'null'
                    EscortDataNoDot = EscortData.replace('.','') # Getting rid of dot char
                    EscortDataNoDotNoComma = EscortDataNoDot.replace(',','') # Getting rid of comma char
                    if len (re.findall(r'\>\W*?[Ee]statura\W*?\:?\W*?(\d\d\d)\W*?\<[\/b]', EscortDataNoDotNoComma)) :
                        estatura = re.findall(r'\>\W*?[Ee]statura\W*?\:?\W*?(\d\d\d)\W*?\<[\/b]', EscortDataNoDotNoComma)[0]
                    sql = sql + ',' + estatura
                    row = row + ',' + estatura
            
        			# Breasts, Waist and Hips of our Escort:
                    pechos = 'null'
                    cintura = 'null'
                    caderas = 'null'
                    if len (re.findall(r'Medidas\W+\d+\-\d+\-\d+', EscortData)) :
                        pechos = re.findall(r'Medidas\W+(\d+)\-\d+\-\d+', EscortData)[0]
                        cintura = re.findall(r'Medidas\W+\d+\-(\d+)\-\d+', EscortData)[0]
                        caderas = re.findall(r'Medidas\W+\d+\-\d+\-(\d+)', EscortData)[0]
                    elif len (re.findall(r'[Mm]edidas\s*\:\s*\d+\W*\d+\W*\d+', EscortData)) :
                        pechos = re.findall(r'[Mm]edidas\s*\:\s*(\d+)\W*\d+\W*\d+', EscortData)[0]
                        cintura = re.findall(r'[Mm]edidas\s*\:\s*\d+\W*(\d+)\W*\d+', EscortData)[0]
                        caderas = re.findall(r'[Mm]edidas\s*\:\s*\d+\W*\d+\W*(\d+)', EscortData)[0]            
                    elif len (re.findall(r'[Mm]edidas\s*\:\s*\&\#160\;\d+\W+\d+\W+\d+', EscortData)) :
                        pechos = re.findall(r'[Mm]edidas\s*\:\s*\&\#160\;(\d+)\W+\d+\W+\d+', EscortData)[0]
                        cintura = re.findall(r'[Mm]edidas\s*\:\s*\&\#160\;\d+\W+(\d+)\W+\d+', EscortData)[0]
                        caderas = re.findall(r'[Mm]edidas\s*\:\s*\&\#160\;\d+\W+\d+\W+(\d+)', EscortData)[0] 
                    elif len (re.findall(r'[Mm]edidas\s*\:\s*\d+\s*\&\#8211\;\W+\d+\W+\d+', EscortData)) :
                        pechos = re.findall(r'[Mm]edidas\s*\:\s*(\d+)\s*\&\#8211\;\W+\d+\W+\d+', EscortData)[0]
                        cintura = re.findall(r'[Mm]edidas\s*\:\s*\d+\s*\&\#8211\;\W+(\d+)\W+\d+', EscortData)[0]
                        caderas = re.findall(r'[Mm]edidas\s*\:\s*\d+\s*\&\#8211\;\W+\d+\W+(\d+)', EscortData)[0]
                    sql = sql + ',' + pechos + ',' + cintura + ',' + caderas
                    row = row + ',' + pechos + ',' + cintura + ',' + caderas
            
        			# Days of Escorting: 
                    hastaDia = ''
                    if len (re.findall(r'[Vv]ierne[Ss]', EscortData)) : hastaDia = 'Vi'
                    elif len (re.findall(r'[Vv]iernes?', EscortData)) : hastaDia = 'Vi'
                    elif len (re.findall(r'[Ss]\&\#225\;bados?', EscortData)) : hastaDia = 'Sa'
                    elif len (re.findall(r'[Ss]abados?', EscortData)) : hastaDia = 'Sa'
                    elif len (re.findall(r'[Dd]omingo', EscortData)) : hastaDia = 'Do'
                    elif len (re.findall(r'[Ff]ull\s[Tt]ime', EscortData)) : hastaDia = 'Do'
                    sql = sql + ',\'' + hastaDia + '\'' 
                    row = row + ',' + hastaDia
                
        			# Hours of Escorting:
                    inicio = ''
                    termino = ''
                    if len (re.findall(r'\d\d\:\d\d\s[aA]\s\d\d\:\d\d\W+\w*?', EscortData)) :
                        inicio = re.findall(r'(\d\d\:\d\d)\s[aA]\s\d\d\:\d\d\W+\w*?', EscortData)[0]
                        termino = re.findall(r'\d\d\:\d\d\s[aA]\s(\d\d\:\d\d)\W+\w*?',  EscortData)[0]
                    elif len (re.findall(r'desde\slas\s\d\d\:\d\d\W+\w*', EscortData)) :
                        inicio = re.findall(r'desde las (\d\d\:\d\d)\W+\w*', EscortData)[0]
                        termino = '06:00'
                    elif len (re.findall(r'[Ff]ull\s[Tt]ime', EscortData)) :
                        inicio = '00:00'
                        termino = '23:59'
                    elif (len (re.findall(r'\d\d\:\d\d', EscortData)) > 1) :
                        inicio = re.findall(r'\d\d\:\d\d', EscortData)[0]
                        termino = re.findall(r'\d\d\:\d\d', EscortData)[1]
                    elif (len (re.findall(r'\d\d\:\d\d', EscortData)) == 1) :
                        inicio = re.findall(r'\d\d\:\d\d', EscortData)[0]
                        termino = ''
                    sql = sql + ',\'' + inicio + '\',\'' + termino + '\'' 
                    row = row + ',' + inicio + ',' + termino
        
        			# Escort Location:
                    EscortData = EscortData.replace(',','')
                    ubicacion = ''
                    if len (re.findall(r'Ubicaci', EscortData)) :
                        ubicacion = EscortData.split('Ubicaci')[1].split('<')[0]
                        print 'Ubicacion split < :..............\n', ubicacion, '\n.........................\n'
                        if len (re.findall(r'\:', ubicacion)) :
                            ubicacion = ubicacion.split(':')[1]
                            print 'Ubicacion split (:) :..................\n', ubicacion, '\n.............................\n'
                        if len (re.findall(r'\&', ubicacion)) :
                            ubicacion = ubicacion.split('&')[0]
                    ubicacion = ubicacion.replace('\n','')
                    print 'Ubicacion Final:', ubicacion
                    
                    ubicacionLenLista += [len(ubicacion)]
                    sql = sql + ',\'' + ubicacion + '\''
                    row = row + ',' + ubicacion
        
        			# Kind of Escort Servicing:   
                    servicios = ''
                    if len (re.findall(r'[Ss]ervicios\W+[Nn]ormales[<\W+]', EscortData)) : servicios = 'Normales'
                    elif len (re.findall(r'[Ss]ervicios\W+[Cc]ompletos[<\W+]', EscortData)) : servicios = 'Completos'
                    serviciosLenLista += [len(servicios)]
                    sql = sql + ',\'' + servicios + '\''
                    row = row + ',' + servicios
            
        			# Service Included:
                    EscortDataNoComma = EscortData.replace(',','') # Getting rid of comma char
                    EscortDataNoCommaNoSlash = EscortDataNoComma.replace('/','') # Getting rid of slash char
                    incluye = ''
                    if len (re.findall(r'[Ss]ervicios', EscortDataNoCommaNoSlash)) :
                        if len (re.findall(r'[Cc]ontactos?\W+[Ii]limitados?', EscortData)) : 
                            incluye = 'Contactos Ilimitados'
                        if len (re.findall(r'[Bb]esos?\W+[Dd]e\W+[Pp]ololas?', EscortData)) :
                            incluye = incluye + ' ' + 'Besos de Polola'
                        if len (re.findall(r'[Aa]mericana', EscortData)) :
                            incluye = incluye + ' ' + 'Americana'
                        if len (re.findall(r'[Aa]nal', EscortData)) :
                            incluye = incluye + ' ' + 'Anal'
                        if len (re.findall(r'[Gg]reco', EscortData)) :
                            incluye = incluye + ' ' + 'Greco'
                        if len (re.findall(r'[Bb]eso\W+[Nn]egro', EscortData)) :
                            incluye = incluye + ' ' + 'Beso Negro'
                    adicionalesLenLista += [len(incluye)]
                    sql = sql + ',\'' + incluye + '\');\n'
                    row = row + ',' + incluye
                    print row
        			
        # End of Loop for LEK 30K & 40K Pages ...........................
        
            elif len (re.findall('<!DOCTYPE html>', html)) :
                # Getting Escort Data from LEK 50K pages : ...................
                EscortDataBlocks = (((html.split('<!-- BEGIN TOPICS -->'))[1].split('</table>'))[0]).split('col_f_content')
                
                i = 1 # BECAUSE : "list indices must be integers, not str".
                for items in EscortDataBlocks :
                    row = ''
                    if (len(EscortDataBlocks) < i+1) : break
                    else : EscortData = EscortDataBlocks[i]
                    if not re.findall(r'<h4>', EscortData) : break
                
                    print '\n\n===================== Escort LEK 50K Inicia ========================='
                    sql = sql + 'INSERT INTO escortssantiago(Escort,Edad,Tarifa,Telefono,Estatura,Busto,Cintura,Culo,Hasta_Dia,Inicio,Termino,Lugar,Servicios,Adicionales) VALUES ('
        
        			# URL of Escort Page:
                    enlace = 'http://www.laestokada.cl/foro/'
                    if len (re.findall(r'\<a\sitemprop\=\"url\"\sid\=\"tid\-link\-\d+\"\shref\=\"http\:\/\/www\.laestokada\.cl\/foro\/index\.php\/topic\/\d+\-\w+\/\"\stitle\=', EscortData)) :
                        enlace = re.findall(r'\<a\sitemprop\=\"url\"\sid\=\"tid\-link\-\d+\"\shref\=\"(http\:\/\/www\.laestokada\.cl\/foro\/index\.php\/topic\/\d+\-\w+\/)\"\stitle\=', EscortData)[0]
                    elif len (re.findall(r'\<a\sitemprop\=\"url\"\sid\=\"tid\-link\-\d+\"\shref\=\"http\:\/\/www\.laestokada\.cl\/foro\/index\.php\/topic\/\d+\-\w+\-\w+\/\"\stitle\=', EscortData)) :
                        enlace = re.findall(r'\<a\sitemprop\=\"url\"\sid\=\"tid\-link\-\d+\"\shref\=\"(http\:\/\/www\.laestokada\.cl\/foro\/index\.php\/topic\/\d+\-\w+\-\w+\/)\"\stitle\=', EscortData)[0]
        
                    htmlfile = urllib.urlopen(enlace)
                    html = htmlfile.read()
                    
                    Escort50KData = (((html.split('<meta name="description"'))[1]).split('">'))[0]
                    
        			# Escort Name (one or two words):
                    nombre = 'Escort LEK'
                    if len (re.findall(r'ipsType\_pagetitle', html)) :
                        nombre = html.split('<h1 itemprop="name" class=\'ipsType_pagetitle\'>')[1].split('</h1>')[0]
                        #print 'Nombre :', nombre
                        
                    anchor = '<a href="' + enlace + '" target="_blank">' + nombre + '</a>'
                    #print 'Largo de Anchor:', str(len(anchor))
                    anchorLenLista += [len(anchor)]
                    sql = sql + '\'' + anchor + '\''
                    row = anchor
                    
                    # Age of the Escort:
                    edad = 'null'
                    if len(re.findall(r'[Ee]dad\W*?\:\W*?(\d\d)\W*?[Aa]\&\#241\;os\<[\/b]', html)) :
                        edad = re.findall(r'[Ee]dad\W*?\:\W*?(\d\d)\W*?[Aa]\&\#241\;os\<[\/b]', html)[0]
                    elif len(re.findall(r'[Ee]dad\W+\d+', html)) :
                        edad = re.findall(r'[Ee]dad\W+(\d+)', html)[0]
                    else : Edad = ''
                    sql = sql + ',' + edad
                    row = row + ',' + edad
                    
                    # Rate or Price of Escort Services:
                    tarifa = 'null'
                    if len (re.findall(r'\;\"\>VALOR\W?\$\W?(\d\d\d?\.\d\d\d)\W*?', html)) :
                        tarifa = re.findall(r'\;\"\>VALOR\W?\$\W?(\d\d\d?\.\d\d\d)\W*?', html)[0]
                    elif len (re.findall(r'\W*?\$\W*?(\d\d\d?\.\d\d\d)\W*?', html)) : 
                        tarifa = re.findall(r'\W*?\$\W*?(\d\d\d?\.\d\d\d)\W*?', html)[0]
                    elif len (re.findall(r'\d\d\d?\.\d\d\d\.\-\W*?', html)) : 
                        tarifa = re.findall(r'(\d\d\d?\.\d\d\d)\.\-\W*?', html)[0]
                    elif len (re.findall(r'[Vv][Aa][Ll][Oo][Rr]\W*\d+\.\d+', html)) :
                        tarifa = re.findall('[Vv][Aa][Ll][Oo][Rr]\W*(\d+\.\d+)', html)
                    tarifa = tarifa.replace('.','')
                    sql = sql + ',' + tarifa
                    row = row + ',' + tarifa
                    
                    # Phone Number of the Escort: 
                    telefono = 'null'
                    if len (re.findall(r'569-?\W*([0-9]{8})', html)) :
                        telefono = re.findall(r'569-?\W*([0-9]{8})', html)[0]
                    elif len (re.findall(r'569\&\#160\;[0-9]{8}\n\&\#160\;', html)) :
                        telefono = re.findall(r'569\&\#160\;([0-9]{8})\n\&\#160\;', html)[0]
                    elif len (re.findall(r'[0-9]{8}', html)) :
                        telefono = re.findall(r'([0-9]{8})', html)[0]
                    sql = sql + ',' + telefono
                    row = row + ',' + telefono
                        
                    # Height of the Escort: 
                    estatura = 'null'
                    if len (re.findall(r'[Ee]statura\W*\d\.\d\d', html)) :
                        estatura = re.findall(r'[Ee]statura\W*(\d\.\d\d)', html)[0]
                    if len (re.findall(r'[Ee]statura\W+\d\W+\d+', html)):
                        estatura = re.findall(r'[Ee]statura\W+(\d\W+\d+)', html)[0]
                    estatura = estatura.replace('.','').replace(',','')
                    if ( len(estatura) == 2 ):
                        estatura = str( int(estatura)*10)
                    print 'Estatura:', estatura
                    sql = sql + ',' + estatura
                    row = row + ',' + estatura
                    
                    # Breasts, Waist and Hips of our Escort:
                    pechos = 'null'
                    cintura = 'null'
                    caderas = 'null'
                    if len (re.findall(r'[Mm]edidas\W*\d+\W*\d+\W*\d+', html)) :
                        pechos = re.findall(r'[Mm]edidas\W*(\d+)\W*\d+\W*\d+', html)
                        cintura = re.findall(r'[Mm]edidas\W*\d+\W*(\d+)\W*\d+', html)
                        caderas = re.findall(r'[Mm]edidas\W*\d+\W*\d+\W*(\d+)', html)
                    if len (re.findall(r'Medidas\W+\d+\-\d+\-\d+', html)) :
                        pechos = re.findall(r'Medidas\W+(\d+)\-\d+\-\d+', html)[0]
                        cintura = re.findall(r'Medidas\W+\d+\-(\d+)\-\d+', html)[0]
                        caderas = re.findall(r'Medidas\W+\d+\-\d+\-(\d+)', html)[0]
                    elif len (re.findall(r'[Mm]edidas\s*\:\s*\d+\W*\d+\W*\d+[\n\W*]', html)) :
                        pechos = re.findall(r'[Mm]edidas\s*\:\s*(\d+)\W*\d+\W*\d+[\n\W*]', html)[0]
                        cintura = re.findall(r'[Mm]edidas\s*\:\s*\d+\W*(\d+)\W*\d+[\n\W*]', html)[0]
                        caderas = re.findall(r'[Mm]edidas\s*\:\s*\d+\W*\d+\W*(\d+)[\n\W*]', html)[0]
                    elif len (re.findall(r'[Mm]edidas\s*\:\s*\&\#160\;\d+\W+\d+\W+\d+[\n|W*]', html)) :
                        pechos = re.findall(r'[Mm]edidas\s*\:\s*\&\#160\;(\d+)\W+\d+\W+\d+[\n|W*]', html)[0]
                        cintura = re.findall(r'[Mm]edidas\s*\:\s*\&\#160\;\d+\W+(\d+)\W+\d+[\n|W*]', html)[0]
                        caderas = re.findall(r'[Mm]edidas\s*\:\s*\&\#160\;\d+\W+\d+\W+(\d+)[\n|W*]', html)[0]
                    elif len (re.findall(r'[Mm]edidas\s*\:\s*\d+\s*\&\#8211\;\W+\d+\W+\d+[\n|\W*]', html)) :
                        pechos = re.findall(r'[Mm]edidas\s*\:\s*(\d+)\s*\&\#8211\;\W+\d+\W+\d+[\n|\W*]', html)[0]
                        cintura = re.findall(r'[Mm]edidas\s*\:\s*\d+\s*\&\#8211\;\W+(\d+)\W+\d+[\n|\W*]', html)[0]
                        caderas = re.findall(r'[Mm]edidas\s*\:\s*\d+\s*\&\#8211\;\W+\d+\W+(\d+)[\n|\W*]', html)[0]
                    print 'Pechos:', pechos
                    print 'Cintura:', cintura
                    print 'Caderas:', caderas
                    sql = sql + ',' + pechos + ',' + cintura + ',' + caderas
                    row = row + ',' + pechos + ',' + cintura + ',' + caderas
                
                    # Days of Escorting:  
                    hastaDia = ''
                    if len (re.findall(r'[Vv]ierne[Ss]', html)) : hastaDia = 'Vi'
                    elif len (re.findall(r'[Vv]iernes?', html)) : hastaDia = 'Vi'
                    elif len (re.findall(r'[Ss]\&\#225\;bados?', html)) : hastaDia = 'Sa'
                    elif len (re.findall(r'[Ss]abados?', html)) : hastaDia = 'Sa'
                    elif len (re.findall(r'[Ss]\W+bados?', html)) : hastaDia = 'Sa'
                    elif len (re.findall(r'[Dd]omingo', html)) : hastaDia = 'Do'
                    elif len (re.findall(r'[Ff]ull\s[Tt]ime', html)) : hastaDia = 'Do'
                    sql = sql + ',\'' + hastaDia + '\''
                    row = row + ',' + hastaDia
                
                    # Hours of Escorting:  
                    inicio = ''
                    termino = ''
                    if len (re.findall(r'\d\d\:\d\d\s[aA]\s\d\d\:\d\d\W+\w*?', html)) :
                    	inicio = re.findall(r'(\d\d\:\d\d)\s[aA]\s\d\d\:\d\d\W+\w*?', html)[0]
                    	termino = re.findall(r'\d\d\:\d\d\s[aA]\s(\d\d\:\d\d)\W+\w*?',  html)[0]
                    elif len (re.findall(r'desde\slas\s\d\d\:\d\d\W+\w*', html)) :
                    	inicio = re.findall(r'desde las (\d\d\:\d\d)\W+\w*', html)[0]
                    	termino = '06:00'
                    elif len (re.findall(r'[Ff]ull\s[Tt]ime', html)) :
                    	inicio = '00:00'
                    	termino = '23:59'
                    elif (len (re.findall(r'\d\d\:\d\d', html)) > 1) :
                    	inicio = re.findall(r'\d\d\:\d\d', html)[0]
                    	termino = re.findall(r'\d\d\:\d\d', html)[1]
                    elif (len (re.findall(r'\d\d\:\d\d', html)) == 1) :
                    	inicio = re.findall(r'\d\d\:\d\d', html)[0]
                    	termino = ''
                    sql = sql + ',\'' + inicio + '\',\'' + termino + '\''
                    row = row + ',' + inicio + ',' + termino
                
                    # Location of the Escort:
                    ubicacion = ''
                    if len (re.findall(r'Ubicacion\s\:', html)) :
                        ubicacion = html.split('Ubicacion :')[1]
                        if len (re.findall(r'Disponibilidad', ubicacion)) :
                            ubicacion = ubicacion.split('Disponibilidad')[0]
                        if len (re.findall(r'Servicios', ubicacion)) :
                            ubicacion = ubicacion.split('Servicios')[0]
                    elif len (re.findall(r'Ubicaci\&\#243\;n:', html)) :
                        ubicacion = html.split('Ubicaci&#243;n:')[1]
                        if len (re.findall(r'Disponibilidad', ubicacion)) :
                            ubicacion = ubicacion.split('Disponibilidad')[0]
                        if len (re.findall(r'Servicios', ubicacion)) :
                            ubicacion = ubicacion.split('Servicios')[0]
                    elif len (re.findall(r'Ubicaci\&\#243\;n\s:', html)) :
                        ubicacion = html.split('Ubicaci&#243;n :')[1]
                        if len (re.findall(r'Disponibilidad', ubicacion)) :
                            ubicacion = ubicacion.split('Disponibilidad')[0]
                        if len (re.findall(r'Servicios', ubicacion)) :
                            ubicacion = ubicacion.split('Servicios')[0]
                    if len (re.findall(r'\n', ubicacion)) :
                        ubicacion = ubicacion.split('\n')[0]
                    print 'Ubicacion :', ubicacion
                    ubicacionLenLista += [len(ubicacion)]
                    sql = sql + ',\'' + ubicacion + '\''
                    row = row + ',' + ubicacion
                
                    # Service of the Escort:
                    servicios = 'Normales'
                    adicionales = ''
                    if len (re.findall(r'Servicios\s\:', html)) :
                        adicionales = html.split('Servicios :')[1].split('&#160;')[0]
                        if len (re.findall(r'[Cc]ompletos', adicionales)) :
                            servicios = 'Completos'
                        if len (re.findall(r'Disponibilidad', adicionales)) :
                            adicionales = adicionales.split('Disponibilidad')[0]
                        if len (re.findall(r'Ubicacion', adicionales)) :
                            adicionales = adicionales.split('Ubicacion')[0]
                        if len (re.findall(r'\.', adicionales)) :
                            adicionales = adicionales.split('.')[0]
                        adicionales = adicionales.replace('\n','').replace(',','.').replace('m&#225;s','y')
                        print 'Adicionales:', adicionales
    
                    serviciosLenLista += [len(servicios)]
                    adicionalesLenLista += [len(adicionales)]
                    sql = sql + ',\'' + servicios + '\',\'' + adicionales + '\');\n'
                    row = row + ',' + servicios + ',' + adicionales
                    
                    # RESULTS :
                    print row
                    time.sleep(Decimal(Decimal(randrange(iTime,fTime,sTime)) / Decimal(1000)))
                    i+=1

        # El Silencio Scraper:
        elif len (re.findall(r'elsilencio', urls)) :
            request = urllib2.Request(urls)
            request.add_header('User-Agent', 'Mozilla/5.0')
            opener = urllib2.build_opener()
            html = opener.open(request).read()
            
            if len (re.findall('chicas', html)) :
                String101 = (html.split('<div class="_body_widget_publicaciones" data-chicas="TODAS">'))[1]
                String102 = (String101.split('<div style="display:none" class="_body_widget_publicaciones" data-chicas="VIP"></div>'))[0]
                EscortDataBlocks = String102.split('<a target="_blank"')
            
                for EscortData in EscortDataBlocks :
                    row = ''
                    enlace = ''
            
                    if len (re.findall('href\=\"http:\/\/www\.elsilencio\.cl\/\?load\=publicacion\&id\=\d+', EscortData)) :
                        sql = sql + 'INSERT INTO escortssantiago(Escort,Edad,Tarifa,Telefono,Estatura,Busto,Cintura,Culo,Hasta_Dia,Inicio,Termino,Lugar,Servicios,Adicionales) VALUES ('
                        enlace = re.findall('href\=\"(http:\/\/www\.elsilencio\.cl\/\?load\=publicacion\&id\=\d+)', EscortData)[0]
                        print '\n\n================= INICIA Escort El Silencio ==========================\n'
                        print 'Enlace : ', enlace
                        
                        request = urllib2.Request(enlace)
                        request.add_header('User-Agent', 'Mozilla/5.0')
                        opener = urllib2.build_opener()
                        EscortPage = opener.open(request).read()
                        EscortPage = str(BeautifulSoup(EscortPage, from_encoding='iso-8859-1'))
    
                        #print 'EscortPage...........................\n', EscortPage, '\n...................................\n'
            
                        # Getting Escort Name (one or two words):
                        nombre = 'Escort ElSilencio'
                        if len (re.findall(r'<span class="_div_nombrepublicacion_fono_nombre">', EscortPage)) :
                            nombreBlock = EscortPage.split('<span class="_div_nombrepublicacion_fono_nombre">')[1]
                            if len (re.findall(r'\<\/span\>', nombreBlock)) :
                                nombreBlock = nombreBlock.split('</span>')[0]
                                if len (re.findall(r'\,', nombreBlock)) :
                                    nombreBlock = nombreBlock.split(',')[0]
                                nombre = nombreBlock.replace('\n','').replace('\t','')
                        print 'Nombre : ', nombre
                            
                        # Anchor Link:
                        anchorLenLista += [len('\'<a href="' + enlace + '" target="_blank">' + nombre + '</a>\'')]
                        #print 'Largo String Achor:', str(len('\'<a href="' + enlace + '" target="_blank">' + nombre + '</a>\''))
                        sql = sql + '\'<a href="' + enlace + '" target="_blank">' + nombre + '</a>\''
                        row = row + '<a href="' + enlace + '" target="_blank">' + nombre + '</a>'
                        
                        # Getting the Escort Data Splits:
                        ListaDatos = EscortPage.split('<span class="_publicacion_contenido_detalle_lista_titulo">')

            			# Getting Escort Age:
                        edad = 'null'
                        if len(re.findall(r'Edad', EscortPage)) :
                            edadBlock = EscortPage.split('Edad')[1].split('</li>')[0]
                            if len(re.findall(r'\d\d', edadBlock)) :
                                edad = re.findall(r'\d\d', edadBlock)[0]
                        print 'Edad : ', edad
                        sql = sql + ',' + edad
                        row = row + ',' + edad
                        
                        # Escort Rate or Value Services:
                        tarifa = 'null'
                        if len (re.findall(r'Tarifa', EscortPage)) :
                            tarifaBlock = EscortPage.split('Tarifa')[1]
                            if len (re.findall(r'</li>', tarifaBlock)) :
                                tarifaBlock = tarifaBlock.split('</li>')[0]
                                #print 'Block de Tarifa:.......................\n', tarifaBlock, '\n.....................\n'
                                if len (re.findall(r'\d+\.\d+', tarifaBlock)) :
                                    tarifa = re.findall(r'\d+\.\d+', tarifaBlock)[0]
                        print 'Tarifa :', tarifa
                        tarifa = tarifa.replace('.','')
                        sql = sql + ',' + tarifa
                        row = row + ',' + tarifa            
                        
                        # Telephone to contact the Escort:
                        telefono = 'null'
                        if len (re.findall('\<div\sclass\W*\_imagen\_icono\_telefono\W*div\W*569\s\d+\s\d+\W*span\>', EscortPage)) :
                            telefono = re.findall('\<div\sclass\W*\_imagen\_icono\_telefono\W*div\W*569\s(\d+\s\d+)\W*span\>', EscortPage)[0]
                            telefono = telefono.replace(' ','')
                        #print 'Telefono :', telefono
                        sql = sql + ',' + telefono
                        row = row + ',' + telefono
            
            			# Getting Escort Height: 
                        estatura = 'null'
                        EscortDataNoDot = EscortData.replace('.','') # Getting rid of dot char
                        if len (re.findall(r'\<span\sclass\=\"\_publicacion\_contenido\_detalle\_lista\_desc\"\>\n\t*\d\.\d+\.*\W*metros\t*\<\/span\>', ListaDatos[3])) :
                            estatura = re.findall(r'\<span\sclass\=\"\_publicacion\_contenido\_detalle\_lista\_desc\"\>\n\t*(\d\.\d+)\.*\W*metros\t*\<\/span\>', ListaDatos[3])[0]
                            estatura = estatura.replace('.','')
                            if ( len(str(estatura)) == 2) :
                                estatura = str((int(estatura)) * 10)
                            #print 'Estatura :', estatura
                        sql = sql + ',' + estatura
                        row = row + ',' + estatura            
                        
            			# Breasts, Waist and Hips of our Escort:
                        pechos = 'null'
                        cintura = 'null'
                        caderas = 'null'
                        if len (re.findall(r'\<span\sclass\=\"\_publicacion\_contenido\_detalle\_lista\_desc\"\>\n\t*\d+\W+\d+\W+\d+\t*\<\/span\>', ListaDatos[4])) :
                            pechos = re.findall(r'\<span\sclass\=\"\_publicacion\_contenido\_detalle\_lista\_desc\"\>\n\t*(\d+)\W+\d+\W+\d+\t*\<\/span\>', ListaDatos[4])[0]
                            cintura = re.findall(r'\<span\sclass\=\"\_publicacion\_contenido\_detalle\_lista\_desc\"\>\n\t*\d+\W+(\d+)\W+\d+\t*\<\/span\>', ListaDatos[4])[0]
                            caderas = re.findall(r'\<span\sclass\=\"\_publicacion\_contenido\_detalle\_lista\_desc\"\>\n\t*\d+\W+\d+\W+(\d+)\t*\<\/span\>', ListaDatos[4])[0]
                            #print 'Pechos :', pechos
                            #print 'Cintura :', cintura
                            #print 'Caderas :', caderas
                       
                        sql = sql + ',' + pechos + ',' + cintura + ',' + caderas
                        row = row + ',' + pechos + ',' + cintura + ',' + caderas
                        
                        # Escort Schedule (Days & Hours):
                        hastaDia = ''
                        inicio = ''
                        termino = ''
                        if len (re.findall('\<div\sclass\=\"calendario\"\>', EscortPage)) :
                            String801 = ((EscortPage.split('<div class="calendario">'))[1].split('<!--**** fin de datos 3 ****-->'))[0]
                            Lista801 = String801.split('<div class="dia">')
                            j = 7
                            for dias in Lista801 :
                                if not len (re.findall('\<div\sclass\=\"dia\_titulo\"\>', Lista801[j])) : break
                                if len (re.findall('close\.png', Lista801[j])) :
                                    j -= 1
                                else :
                                    hastaDia = re.findall('\<div\sclass\=\"dia\_titulo\"\>(\w*)\<\/div\>', Lista801[j])[0]
                                    inicio = re.findall('\<div\sclass\=\"dia\_horario\"\>\W*ul\W*li\W*(\d+\:\d+)\W*li\W*\W*li\W*a\W*li\W*li\W*\d+\:\d+\W*li\W*ul\>', Lista801[j])[0]
                                    termino = re.findall('\<div\sclass\=\"dia\_horario\"\>\W*ul\W*li\W*\d+\:\d+\W*li\W*\W*li\W*a\W*li\W*li\W*(\d+\:\d+)\W*li\W*ul\>', Lista801[j])[0]
                        sql = sql + ',\'' + hastaDia + '\',\'' + inicio + '\',\'' + termino + '\''
                        row = row + ',' + hastaDia + ',' + inicio + ',' + termino
                        
            			# Escort Location:
                        ubicacion = ''
                        #if len (re.findall(r'\<span\s*class\=\"\_publicacion\_contenido\_detalle\_lista\_desc\"\>\n\t*', ListaDatos[18])) :
                        if len (re.findall(r'Ubicaci', EscortPage)) :
                            ubicacion = EscortPage.split('Ubicaci')[1].split('</li>')[0].split('<span class="_publicacion_contenido_detalle_lista_desc">')[1].split('</span>')[0]
                            #ubicacion = ((ListaDatos[18].split('<span class="_publicacion_contenido_detalle_lista_desc">'))[1].split('</span>'))[0]
                            ubicacion = ubicacion.replace('\t','').replace('\n','')
                        #print 'Lugar :', ubicacion
            
                        # Escort Location Aditional Data:
                        ubicacionAdicional = ''
                        if len(re.findall(r'Atenci', EscortPage)) :
                            ubicacionAdicional = EscortPage.split('Atenci')[1]
                            if len (re.findall(r'</li>', ubicacionAdicional)) :
                                ubicacionAdicional = ubicacionAdicional.split('</li>')[0]
                                if len (re.findall(r'<span class=\"_publicacion_contenido_detalle_lista_desc3\">', ubicacionAdicional)) :
                                    ubicacionAdicional = ubicacionAdicional.split('<span class=\"_publicacion_contenido_detalle_lista_desc3\">')[1]
                                    if len (re.findall(r'</span>', ubicacionAdicional)) :
                                        ubicacionAdicional = ubicacionAdicional.split('</span>')[0]
                                        ubicacionAdicional = ubicacionAdicional.replace('\t','').replace('\n','').replace(',','.')
                                        ubicacion = ubicacion + '. ' + ubicacionAdicional
                        #print 'Ubicacion Adicional :', ubicacionAdicional
                        print 'Lugar FINAL:', ubicacion
                            
                        sql = sql + ',\'' + ubicacion + '\''
                        ubicacionLenLista += [len(ubicacion)]
                        #print 'Largo String Ubicacion:', str(len(ubicacion))
                        row = row + ',' + ubicacion
                        
                        # Standard Services of the Escort:
                        servicios = 'Normales'
                        incluidos = ''
                        adicionales = ''
                        if len (re.findall(r'popup\_incluidas', EscortPage)) :
                            serviciosBlock = EscortPage.split('popup_incluidas')[1]
                            if len (re.findall(r'fin\sde\sdatos\s2', serviciosBlock)) :
                                serviciosBlock = serviciosBlock.split('<!-- fin de datos 2-->')[0]
                                if len (re.findall(r'[Aa]nal', serviciosBlock)) :
                                    servicios = 'Completos'
                        print 'Servicios:', servicios
                        #if len (re.findall('\<div class\=\"\_publicacion\_contenido\_detalle\_datos3\"\>', EscortPage)) :
                            #String501 = ((EscortPage.split('<div class="_publicacion_contenido_detalle_datos3">'))[1].split('<!-- fin de datos 2-->'))[0]
                            #if len (re.findall('[Aa]nal', (String501.split('incluidas'))[1])) :
                                #servicios = 'Completos'
                        if len(re.findall(r'popup\_incluidas',EscortPage)) :
                            if len(re.findall(r'\<\/ul\>',EscortPage)) :
                                incluidos = EscortPage.split('popup_incluidas')[1].split('</ul>')[0]
                                incluidos = incluidos.replace('" style="left: 269px; top: 323px;">','')
                                incluidos = incluidos.replace('<ul style="list-style-type:square;float:left;padding:5px 5px 5px 25px;margin:0px">','')
                                incluidos = incluidos.replace('<li style="width:140px">','').replace('</li>','. ').replace('" style="">','').replace('\n','')
                                #print 'Servicios Incluidos :', incluidos
                        if len(re.findall(r'popup\_adicionales',EscortPage)) :
                            if len(re.findall(r'\<\/ul\>',EscortPage)) :
                                adicionales = EscortPage.split('popup_adicionales')[1].split('</ul>')[0]
                                adicionales = adicionales.replace('<ul style="list-style-type:square;float:left;padding:5px 5px 5px 25px;margin:0px">','')
                                adicionales = adicionales.replace('<li style="width:140px;">','').replace('</li>','. ').replace('">','').replace('\n','')
                                #print 'Servicios Adicionales:', adicionales
                                
                        #print 'Servicios :', servicios
                        serviciosLenLista += [len(servicios)]
                        
                        #print 'Largo String Adicionales:', str(len(incluidos + '. ' + adicionales))
                        print 'Servicios Incluidos y Adicionales :', incluidos + '. ' + adicionales
                        adicionalesLenLista += [len(incluidos + '. ' + adicionales)]
                        row = row + ',' + servicios + ',' + incluidos + '. ' + adicionales
                        sql = sql + ',\'' + servicios + '\',\'' + incluidos + '. ' + adicionales + '\');\n'
            
                        #print row.decode('iso-8859-1'), '\n ===============================================\n\n'
                        time.sleep(Decimal(Decimal(randrange(iTime,fTime,sTime)) / Decimal(1000)))
    
            
        # Relax Chile Scraper:
        elif len (re.findall(r'relaxchile', urls)) :
            # Detecting Start Point of Escort Data List:
            if len (re.findall('Destacadas\<\/title\>', html)) :
                EscortDataList = html.split('Destacadas</title>')[1].split('</ul>')[0].split('</li>')
            elif len (re.findall('Destacadas\sTop\<\/title\>', html)) :
                EscortDataList = html.split('Destacadas Top</title>')[1].split('</ul>')[0].split('</li>')
            elif len (re.findall('Destacadas\sVip\<\/title\>', html)) :
                EscortDataList = html.split('Destacadas Vip</title>')[1].split('</ul>')[0].split('</li>')
        
            i = 0
            for items in EscortDataList :
                #if (i==2) : break
        
                # Name of Escort:
                nombre = 'Escort Relax'
                if len(re.findall('\<img\salt\=\"\w+\"\ssrc\=\"', items)) :
                    nombre = re.findall('\<img\salt\=\"(\w+)\"\ssrc\=\"', items)[0]
                if len(re.findall('\<img\salt\=\"\w+\W+\w+\"\ssrc\=\"', items)) :
                    nombre = re.findall('\<img\salt\=\"(\w+\W+\w+)\"\ssrc\=\"', items)[0]
            
                # URLs of Escort:        
                enlace = 'http://www.relaxchile.cl/'
                if len(re.findall('href\=\'\/escort\/\d+\'', items)) :
                    enlace = 'http://www.relaxchile.cl' + re.findall('href\=\'(\/escort\/\d+)\'', items)[0] + '+&cd=4&hl=es-419&ct=clnk&gl=cl'
                anchor = '<a href="' + enlace + '" target="_blank">' + nombre + '</a>'
        
                row = anchor
            
                # Preps of Escort Data Page
                escortPage = urllib.urlopen(enlace)
                htmlEscortPage = escortPage.read()
                if len (re.findall('descripcion', htmlEscortPage)) :
                    EscortData = htmlEscortPage.split('descripcion')[1].split('imagenes')[0]
                else : break

                sql = sql + 'INSERT INTO escortssantiago(Escort,Edad,Tarifa,Telefono,Estatura,Busto,Cintura,Culo,Hasta_Dia,Inicio,Termino,Lugar,Servicios,Adicionales) VALUES ('
                sql = sql + '\'' + anchor + '\''
                anchorLenLista += [len(anchor)]
                print 'Largo String Anchor:', str(len(anchor))
                
                # Age of the Escort:
                edad = 'null'
                if len(re.findall('\<td\>\nEdad\:\n\d\d\s+años\n\<\/td\>', EscortData)) :
                    edad = re.findall('\<td\>\nEdad\:\n(\d\d)\s+años\n\<\/td\>', EscortData)[0]
                if len(re.findall('\<td\>\nEdad\:\n\s\d\d\s\w+\n\<\/td\>', EscortData)) :
                    edad = re.findall('\<td\>\nEdad\:\n\s(\d\d)\s\w+\n\<\/td\>', EscortData)[0]
                sql = sql + ',' + edad
                row = row + ',' + edad
                
                # Rate or Price or Escort Services:
                tarifa = 'null'
                if len (re.findall('\<p\sclass\=\'valor\-original\'\>\$\d\d\d?\.\d\d\d\<\/p\>', EscortData)) :
                    tarifa = re.findall('\<p\sclass\=\'valor\-original\'\>\$(\d\d\d?\.\d\d\d)\<\/p\>', EscortData)[0]
                elif len (re.findall('\<p\sid\=\'valor\'\>\nvalor\:\n\$\d\d\d?\.\d\d\d\n\<span\>', EscortData)) :
                    tarifa = re.findall('\<p\sid\=\'valor\'\>\nvalor\:\n\$(\d\d\d?\.\d\d\d)\n\<span\>', EscortData)[0]
                elif len (re.findall('\<p\sid\=\'valor\'\>\nvalor\:\na\sconsultar\n\<\/p\>', EscortData)) :
                    tarifa = 'null'
                tarifa = tarifa.replace('.','')
                sql = sql + ',' + tarifa
                row = row + ',' + tarifa
                
                # Cell Phone of Escort:
                telefono = 'null'
                if len (re.findall('\<label\>fono\:\<\/label\>\n\<span\>\d\s\d\d\d\s\d\d\d\d\<\/span\>', EscortData)) :
                    telefono = re.findall('\<label\>fono\:\<\/label\>\n\<span\>(\d\s\d\d\d\s\d\d\d\d)\<\/span\>', EscortData)[0]
                elif len (re.findall('\<span\>\+569\s\d\s\d\d\d\s\d\d\d\d\<\/span\>', EscortData)) :
                    telefono = re.findall('\<span\>\+569\s(\d\s\d\d\d\s\d\d\d\d)\<\/span\>', EscortData)[0]
                elif len (re.findall('\<span\>\s\d\s\d\d\d\d\s\d\d\d\<\/span\>', EscortData)) :
                    telefono = re.findall('\<span\>\s(\d\s\d\d\d\d\s\d\d\d)\<\/span\>', EscortData)[0]
                elif len (re.findall('0056\s*\d\s*\d\s*\d\d\d\s*\d\d\d\d', EscortData)) :
                    telefono = re.findall('0056\s*\d\s*(\d\s*\d\d\d\s*\d\d\d\d)', EscortData)[0]
                elif len (re.findall('0056\s9\s\d\s\d\d\d\d\s\d\d\d', EscortData)) :
                    telefono = re.findall('0056\s9\s(\d\s\d\d\d\d\s\d\d\d)', EscortData)[0]
                elif len (re.findall('fono:', EscortData)) :
                    telefono = EscortData.split('fono:')[1].split('</span>')[0]
                    telefono = telefono.replace('</label>','').replace('\n','').replace('<span>','')
                telefono = telefono.replace(' ','') # Getting rid of space char.
                sql = sql + ',' + telefono
                row = row + ',' + telefono
                    
                # Height of the Escort:
                estatura = 'null'
                if len (re.findall('\<td\>\nAltura\:\n\d\.\d\d\sMts\.\n\<\/td\>', EscortData)) :
                    estatura = re.findall('\<td\>\nAltura\:\n(\d\.\d\d)\sMts\.\n\<\/td\>', EscortData)[0]
                    estatura = estatura.replace('.','') # Getting rid of dot char.
                sql = sql + ',' + estatura
                row = row + ',' + estatura
                
                # Breasts, Waist and Hips of our Escort:
                pechos = 'null'
                cintura = 'null'
                caderas = 'null'
                if len (re.findall('\<td\>\nMedidas\:\n\d\d\d?\-\d\d\d?\-\d\d\d?\n\<\/td\>', EscortData)) :
                    pechos = re.findall('\<td\>\nMedidas\:\n(\d\d\d?)\-\d\d\d?\-\d\d\d?\n\<\/td\>', EscortData)[0]
                    cintura = re.findall('\<td\>\nMedidas\:\n\d\d\d?\-(\d\d\d?)\-\d\d\d?\n\<\/td\>', EscortData)[0]
                    caderas = re.findall('\<td\>\nMedidas\:\n\d\d\d?\-\d\d\d?\-(\d\d\d?)\n\<\/td\>', EscortData)[0]
                sql = sql + ',' + pechos + ',' + cintura + ',' + caderas
                row = row + ',' + pechos + ',' + cintura + ',' + caderas
             
                # Days & Hours of Escorting:
                hastaDia = 'Viernes'
                inicio = ''
                termino = ''
                Lista30 = EscortData.split('horario-atencion')
                String30 = Lista30[1]
                Lista31 = String30.split('</div>')
                DaysAndLocation = Lista31[0]
                if len (re.findall('\<p\>\nHorario\:De\s\w+\sa\s\w+\sdesde\slas\s\d\d\:\d\d\sa\s\d\d\:\d\d\shrs\n\<\/p\>', DaysAndLocation)) :
                    hastaDia = re.findall('\<p\>\nHorario\:De\s\w+\sa\s(\w+)\sdesde\slas\s\d\d\:\d\d\sa\s\d\d\:\d\d\shrs\n\<\/p\>', DaysAndLocation)[0]
                    inicio = re.findall('\<p\>\nHorario\:De\s\w+\sa\s\w+\sdesde\slas\s(\d\d\:\d\d)\sa\s\d\d\:\d\d\shrs\n\<\/p\>', DaysAndLocation)[0]
                    termino = re.findall('\<p\>\nHorario\:De\s\w+\sa\s\w+\sdesde\slas\s\d\d\:\d\d\sa\s(\d\d\:\d\d)\shrs\n\<\/p\>', DaysAndLocation)[0]
                elif len (re.findall('\d\d\:\d\d\sa\s\d\d\:\d\d', DaysAndLocation)) :
                    inicio = re.findall('(\d\d\:\d\d)\sa\s\d\d\:\d\d', DaysAndLocation)[0]
                    termino = re.findall('\d\d\:\d\d\sa\s(\d\d\:\d\d)', DaysAndLocation)[0]
                elif len (re.findall('\<p\>\nHorario\:\nFull\sTime\n\<\/p\>', DaysAndLocation)) :
                    hastaDia = 'Do'
                    inicio = '00:00'
                    termino = '23:59'
                sql = sql + ',\'' + hastaDia + '\',\'' + inicio + '\',\'' + termino + '\''
                row = row + ',' + hastaDia + ',' + inicio + ',' + termino
            
                # Location of the Escort:
                ubicacion = DaysAndLocation.split('Atención:')[1].replace('\n','').replace('\'','').replace('\>','').replace('<p>',' ').replace('</p>','').replace(',','')
                sql = sql + ',\'' + ubicacion + '\''
                ubicacionLenLista += [len(ubicacion)]
                print 'Largo String Ubicacion:', str(len(ubicacion))
                row = row + ',' + ubicacion
                
                # Standard Services of the Escort :
                servicios = ''
                if len (re.findall('<span\W*class\W*dorado\W*\nServicios:\n\W*span\W*\n\w+', EscortData)) :
                    servicios = re.findall('<span\W*class\W*dorado\W*\nServicios:\n\W*span\W*\n(\w+)', EscortData)[0]
                serviciosLenLista += [len(servicios)]
                print 'Largo String Servicios:', str(len(servicios))
                print 'Servicios:', servicios
                sql = sql + ',\'' + servicios + '\''
                row = row + ',' + servicios
            
                # Additional Services of the Escort:
                adicionales = ''
                if len (re.findall('Servicios\:', EscortData)) :
                    String51 = EscortData.split('Servicios:')[1].split('</div>')[0].replace('\n','').replace('</span>','').replace('</p>','')
                    String51 = String51.replace(',','.')
                    if ( len (String51.split('.',1)) == 2 ) :
                        adicionales = String51.split('.',1)[1]
        
                print 'Adicionales:', adicionales
                adicionalesLenLista += [len(adicionales)]
                print 'Largo String Adicionales:', str(len(adicionales))
                sql = sql + ',\'' + adicionales + '\');\n'
                row = row + ',' + adicionales
        
                print row
                time.sleep(Decimal(Decimal(randrange(iTime,fTime,sTime)) / Decimal(1000)))
            
                # Indice de Control:
                i+=1            
          
        # Sexo Scraper :
        elif len (re.findall(r'sexo', urls)) :
            htmlfile = urllib.urlopen(urls)
            html = htmlfile.read()
            UlsBlocks = html.split('<ul>')
            SecondPortion = UlsBlocks[1]
            Blocks = SecondPortion.split('</ul>')
            MainBlock = Blocks[0]
            EscortDataBlocks = MainBlock.split('</li>')
            
            print 'Total de Escorts Publicadas en sexo.cl :', len(EscortDataBlocks)
            
            i = 0 # Control Loop Index
            for items in EscortDataBlocks :
                #if (i==20) : break # Going Out of the Loop
                EscortData = EscortDataBlocks[i]
                if not re.findall(r'divCategRes', EscortData) : break
                row = ''
                sql = sql + 'INSERT INTO escortssantiago(Escort,Edad,Tarifa,Telefono,Estatura,Busto,Cintura,Culo,Hasta_Dia,Inicio,Termino,Lugar,Servicios,Adicionales) VALUES ('
                
                #print '\n', 'Escort Data Block : ...................', '\n', EscortDataBlocks[i], '......................', '\n'
                nombre = ''
                if len (re.findall('text\-decoration\:none\;\"\>', EscortDataBlocks[i])) :
                    nombre = ((EscortDataBlocks[i].split('text-decoration:none;">'))[1].split('</a>'))[0]
                    nombre = str(BeautifulSoup(nombre, from_encoding='iso-8859-1'))
                    nombre = nombre.replace('<html><body><p>','')
                    nombre = nombre.replace('</p></body></html>','')
            
                # URL of Escort Page:
                enlace = 'Falla'
                if len(re.findall(r'href\=\"\/\?id\=\d+\&\id\_Ficha\=\d+\&utm', EscortData)) :
                    enlace = 'http://www.sexo.cl' + re.findall(r'href\=\"(\/\?id\=\d+\&\id\_Ficha\=\d+)\&utm', EscortData)[0]
                sql = sql + '\'<a href="' + enlace + '" target="_blank">' + nombre +'</a>\''
                row = '<a href="' + enlace + '" target="_blank">' + nombre +'</a>'
                anchorLenLista += [len(row)]
                print 'Largo String Anchor:', str(len(row))
                
                # Data from Escort Page
                htmlfile = urllib.urlopen(enlace)
                html = htmlfile.read()
                if len(re.findall(r'\<table\sid\=\"DatosFicha\"', html)) :
                    EscortPageBlockOne = html.split('<table id="DatosFicha"')
                    EscortPageSecondHalf = EscortPageBlockOne[1]
                    EscortPageMain = EscortPageSecondHalf.split('<div class="FichaFavoritas">')
                    EscortPage = EscortPageMain[0]
                else :
                    print 'No detecta DatosFicha en linea 851....'
                    break
                
                # Age of Escort:
                edad = 'null'
                if len(re.findall('\<span\sid\=\"FichaAcomp\_nacionalidad\"\>\<\/span\>\sde\s\<b\>(\d\d)\sa', EscortPage)) :
                    edad = re.findall('\<span\sid\=\"FichaAcomp\_nacionalidad\"\>\<\/span\>\sde\s\<b\>(\d\d)\sa', EscortPage)[0]
                sql = sql + ',' + edad
                row = row + ',' + edad
                
                # Rate or Price of Escort Services:
                tarifa = 'null'
                if len(re.findall('\<b\>Valor\:\s\$\d\d\d?\.\d\d\d\<\/b\>', EscortPage)) :
                    tarifa = re.findall('\<b\>Valor\:\s\$(\d\d\d?\.\d\d\d)\<\/b\>', EscortPage)[0]
                tarifa = tarifa.replace('.','')
                sql = sql + ',' + tarifa
                row = row + ',' + tarifa
                
                # Cel Phone of Escort:
                telefono = 'null'
                if len(re.findall('\<script\>fFormatoFonos\(\'\d\d\.\s\d\d\d\s\d\d\d\d\<br\>\d\d\.\s\d\d\d\s\d\d\d\d\'\)\<\/script\>', EscortPage)) :
                    telefono = re.findall('\<script\>fFormatoFonos\(\'\d(\d\.\s\d\d\d\s\d\d\d\d)\<br\>\d\d\.\s\d\d\d\s\d\d\d\d\'\)\<\/script\>', EscortPage)[0]
                elif len(re.findall('\<script\>fFormatoFonos\(\'\d\d\.\s\d\d\d\s\d\d\d\d\<br\>\'\)\<\/script\>\<\/div\>', EscortPage)) :
                    telefono = re.findall('\<script\>fFormatoFonos\(\'\d(\d\.\s\d\d\d\s\d\d\d\d)\<br\>\'\)\<\/script\>\<\/div\>', EscortPage)[0]
                telefono = telefono.replace('.','') # No Dot Char.
                telefono = telefono.replace(' ','') # No Space Char.
                sql = sql + ',' + telefono
                row = row + ',' + telefono
                
                # Height of Escort:
                estatura = 'null'
                if len(re.findall('\<b\>\d\.\d\d\<\/b\>\smts\sde\sestatura', EscortPage)) :
                    estatura = re.findall('\<b\>(\d\.\d\d)\<\/b\>\smts\sde\sestatura', EscortPage)[0]
                elif len(re.findall('\-\sEstatura\:\s\d[\.\,]\d\d\s\-', html)) :
                    estatura = re.findall('\-\sEstatura\:\s(\d[\.\,]\d\d)\s\-', html)[0]
                estatura = estatura.replace('.','') # No Dot Char.
                estatura = estatura.replace(',','') # No Comma Char.
                sql = sql + ',' + estatura
                row = row + ',' + estatura
                
                # Breasts, Waist and Hips of our Escort:
                pechos = 'null'
                cintura = 'null'
                caderas = 'null'
                if len(re.findall('\<br\>Sus\smedidas\sson\s\<b\>\d\d\,\s\d\d\,\s\d\d\<\/b\>', EscortPage)) :
                    pechos = re.findall('\<br\>Sus\smedidas\sson\s\<b\>(\d\d)\,\s\d\d\,\s\d\d\<\/b\>', EscortPage)[0]
                    cintura = re.findall('\<br\>Sus\smedidas\sson\s\<b\>\d\d\,\s(\d\d)\,\s\d\d\<\/b\>', EscortPage)[0]
                    caderas = re.findall('\<br\>Sus\smedidas\sson\s\<b\>\d\d\,\s\d\d\,\s(\d\d)\<\/b\>', EscortPage)[0]
                elif len(re.findall('\-\sMedidas\:\s\d\d\d?\,\s\d\d\d?\,\s\d\d\d?', html)) :
                    pechos = re.findall('\-\sMedidas\:\s(\d\d\d?)\,\s\d\d\d?\,\s\d\d\d?', html)[0]
                    cintura = re.findall('\-\sMedidas\:\s\d\d\d?\,\s(\d\d\d?)\,\s\d\d\d?', html)[0]
                    caderas = re.findall('\-\sMedidas\:\s\d\d\d?\,\s\d\d\d?\,\s(\d\d\d?)', html)[0]
                sql = sql + ',' + pechos + ',' + cintura + ',' + caderas
                row = row + ',' + pechos + ',' + cintura + ',' + caderas
                
                # Days & Hours of Escorting:
                hastaDia = 'Vi'
                inicio = ''
                termino = ''
                # Preps:
                if len (re.findall('\<div\sstyle\=\"margin\-top\:10px\;\"\>', EscortPage)) :
                    List10 = EscortPage.split('<div style=\"margin-top:10px;\">')
                    dayshours = List10[5].replace('</div> ', '')
                    # Finding Days & Hours:
                    if len (re.findall('Full Time', dayshours)) :
                        hastaDia = 'Do'
                        inicio = '00:00'
                        termino = '24:00'
                    elif len (re.findall('\d\d\:\d\d\sa\s\d\d\:\d\d', dayshours)) :
                        hastaDia = 'Vi'
                        inicio = re.findall('(\d\d\:\d\d)\sa\s\d\d\:\d\d', dayshours)[0]
                        termino = re.findall('\d\d\:\d\d\sa\s(\d\d\:\d\d)', dayshours)[0]
                    elif len (re.findall('\d+\.\d+\sa\s\d+\.\d+', dayshours)) :
                        hastaDia = 'Vi'
                        inicio = re.findall('(\d+)\.\d+\sa\s\d+\.\d+', dayshours)[0] + ':' + re.findall('\d+\.(\d+)\sa\s\d+\.\d+', dayshours)[0]
                        termino = re.findall('\d+\.\d+\sa\s(\d+)\.\d+', dayshours)[0] + ':' + re.findall('\d+\.\d+\sa\s\d+\.(\d+)', dayshours)[0]
                    elif len (re.findall('\d\d\sa\s\d\d', dayshours)) :
                        hastaDia = 'Vi'
                        inicio = re.findall('(\d\d)\sa\s\d\d', dayshours)[0] + ':00'
                        termino = re.findall('\d\d\sa\s(\d\d)', dayshours)[0] + ':00'
                    elif len (re.findall('\d\d\sa\slas\s\d\d', dayshours)) :
                        hastaDia = 'Vi'
                        inicio = re.findall('(\d\d)\sa\slas\s\d\d', dayshours)[0] + ':00'
                        termino = re.findall('\d\d\sa\slas\s(\d\d)', dayshours)[0] + ':00'
                sql = sql + ',\'' + hastaDia + '\',\'' + inicio + '\',\'' + termino + '\''
                row = row + ',' + hastaDia + ',' + inicio + ',' + termino  
                
                # Location of the Escort:
                ubicacion = ''
                if len (re.findall('\<div\sstyle\=\"margin\-top\:10px\;\"\>', EscortPage)) :
                    List10 = EscortPage.split('<div style=\"margin-top:10px;\">')
                    ubicacion = List10[4].replace('</div>', '')
                    ubicacion = ubicacion.replace('<br/>',' ')
                    ubicacion = ubicacion.replace('.','')
                    ubicacion = ubicacion.replace('<b>','')
                    ubicacion = ubicacion.replace('Estoy en ','')
                    ubicacion = ubicacion.replace('Estoy','')
                    ubicacion = ubicacion.replace(',','')
                    ubicacion = ubicacion.replace('</b>','')
                    ubicacion = ubicacion.replace('<br>',' ')
                    ubicacion = ubicacion.replace('\n','')
                    ubicacion = ubicacion.replace('\r','')
                    ubicacion = str(BeautifulSoup(ubicacion, from_encoding='iso-8859-1'))
                    ubicacion = ubicacion.replace('<html><body><p>','')
                    ubicacion = ubicacion.replace('</p></body></html>','')
                sql = sql + ',\'' + ubicacion + '\''
                row = row + ',' + ubicacion
                ubicacionLenLista += [len(ubicacion)]
                print 'Largo String Ubicacion:', str(len(ubicacion))
                
                # Service of the Escort:
                servicios = 'Normales'
                sql = sql + ',\'' + servicios + '\''
                row = row + ',' + servicios
                serviciosLenLista += [len(servicios)]
                # Service Included:
                adicionales = ''
                # Preps :
                if len (re.findall('Servicios\:', EscortPageBlockOne[0])) :
                    List20 = EscortPageBlockOne[0].split('Servicios: ')
                    List21 = List20[1].split('\">')
                    String20 = List21[0]
                    adicionales = String20.replace(',','')
                    adicionales = adicionales.replace('Idiomas:','')
                    adicionales = adicionales.replace('-','')
                    adicionales = str(BeautifulSoup(adicionales, from_encoding='iso-8859-1'))
                    adicionales = adicionales.replace('<html><body><p>','')
                    adicionales = adicionales.replace('</p></body></html>','')
                sql = sql + ',\'' + adicionales + '\');\n'
                row = row + ',' + adicionales
                adicionalesLenLista += [len(adicionales)]
                print 'Largo String Adicionales:', str(len(adicionales))
                
                print row
                i+=1
                time.sleep(Decimal(Decimal(randrange(iTime,fTime,sTime)) / Decimal(1000)))
    
            
        # La EstoCada Scraper:
        elif len (re.findall(r'laestocada', urls)) :
            if len (re.findall('Chicas Black', html)) :
                EscortDataBlocks = ((((html.split('Chicas Black'))[1]).split('Chicas Recomendadas'))[0]).split('</a>')
                for EscortData in EscortDataBlocks :
                    row = ''
                    enlace = ''
                    if len (re.findall('\/upload\_files\/utilidades\/views\/ficha\.php\?id\=\d+', EscortData)) :
                        if (re.findall('\/upload\_files\/utilidades\/views\/ficha\.php\?id\=(\d+)', EscortData)[0] != '850') : # Getting Rid of Banner Ad
                            enlace = 'http://www.laestocada.cl' + re.findall('\/upload\_files\/utilidades\/views\/ficha\.php\?id\=\d+', EscortData)[0]
                            #print 'Enlace : ', enlace
                            
                            sql = sql + 'INSERT INTO escortssantiago(Escort,Edad,Tarifa,Telefono,Estatura,Busto,Cintura,Culo,Hasta_Dia,Inicio,Termino,Lugar,Servicios,Adicionales) VALUES ('
            
                            # Escort Page opening & reading:
                            request = urllib2.Request(enlace)
                            request.add_header('User-Agent', 'Mozilla/5.0')
                            opener = urllib2.build_opener()
                            EscortPage = opener.open(request).read()
                            #EscortPage = EscortPage.decode('iso-8859-1')
                            print '\n==================== Escort LaEstoCada Inicia ======================\n\n'
                            print 'Enlace : ', enlace
                            
                            # Escort Data Splitting:
                            if len (re.findall('LaEstocada.cl</title>', EscortPage)) :
                                EscortDataList = EscortPage.split('</tr>')
                
                            # Getting Escort Name (any words size):
                            nombre = 'Escort LaEstoCada'
                            if len (re.findall(r'TitFicha', EscortDataList[2])) :
                                nombre = ((EscortPage.split('<td class="TitFicha"><div align="center">'))[1].split('</div>'))[0]
    
                            anchor = '<a href="' + enlace + '" target="_blank">' + nombre + '</a>'
                            anchorLenLista += [len(anchor)]
                            #print 'Nombre:', nombre
                            #print 'Largo String Anchor:', str(len(anchor))
                            sql = sql + '\'' + anchor + '\''
                            row = row + '<a href="' + enlace + '" target="_blank">' + nombre + '</a>'
                            
            			    # Age of the Escort:
                            edad = 'null'
                            if len(re.findall(r'Edad\:', EscortPage)) :
                                edad = EscortPage.split('Edad:')[1].split('</td>')[1]
                                #print 'Edad After split </td>:', edad
                                if len (re.findall(r'\<td\sclass\=\"RespPop\"\>', edad)) :
                                    edad = edad.split('<td class="RespPop">')[1].split(' ')[0]
                            #print 'Edad:', edad
                                #edad = re.findall(r'\<td\swidth=\"80\"\sclass\=\"textosPop\"\>Edad\:\<\/td\>\W*td\sclass\=\"RespPop\"\>(\d+)', EscortDataList[4])[0]
                            #print 'Edad : ', edad
                            sql = sql + ',' + edad
                            row = row + ',' + edad
                            
                            # Escort Rate or Value Services:
                            tarifa = 'null'
                            if len(re.findall(r'Valor\sNormal\:', EscortPage)) :
                                #print 'Tarifa After IF Valor Normal:'
                                tarifa = EscortPage.split('Valor Normal:')[1].split('</tr>')[0].split('$')[1]
                                #print 'Tarifa After Valor Normal split ............:', tarifa
                                tarifa = tarifa.replace('</td>','').replace('\n','').replace('\t','').replace(' ','')
                            elif len(re.findall(r'Valor\sPreferencial\:', EscortPage)) :
                                tarifa = EscortPage.split('Valor Preferencial:')[1].split('</tr>')[0].split('$')[1]
                                tarifa = tarifa.replace('</td>','').replace('\n','').replace('\t','').replace(' ','')
                            tarifa = tarifa.replace('.','')
                            if not len (re.findall(r'\d+', tarifa)) :
                                tarifa = 'null'
                            #print 'Tarifa:', tarifa
                            #print 'Tarifa :', tarifa
                            sql = sql + ',' + tarifa
                            row = row + ',' + tarifa
                            
                            # Telephone to contact the Escort:
                            telefono = 'null'
                            if len (re.findall(r'fono\"\>', EscortPage)) :
                                telefonoBlock = EscortPage.split('fono\">')[1].split('</td>')[0]
                                print 'Telefono Block:\n..............................\n', telefonoBlock, '\n.............................\n'
                                if len (re.findall(r'\W*56\W*9\W*\d+\W*\d+', telefonoBlock)) :
                                    telefono = re.findall(r'\W*56\W*9\W*(\d+\W*\d+)', telefonoBlock)[0]
                                elif len (re.findall(r'\d\W*\d{7}', telefonoBlock)) :
                                    telefono = re.findall(r'\d\W*\d{7}', telefonoBlock)[0]
                                elif len (re.findall(r'\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d', telefonoBlock)) :
                                    telefono = re.findall(r'\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d', telefonoBlock)[0]
                                telefono = telefono.replace(' ','').replace('-','').replace('+','')
                                
                            #if len (re.findall('\<td\sclass\=\"fono\"\>', EscortPage)) :
                                #telefono = ((EscortPage.split('<td class="fono">'))[1].split('</td>'))[0]
                                
                            print 'Telefono :', telefono, '\n-----------------------\n'
                            sql = sql + ',' + telefono
                            row = row + ',' + telefono
                            
                			# Getting Escort Height: 
                            estatura = 'null'
                            if len (re.findall('Estatura', EscortPage)) :
                                estatura = ((EscortPage.split('Estatura'))[1].split('</td>'))[1]
                                if len (re.findall(r'\<td\sclass\=\"RespPop\"\>', estatura)) :
                                    estatura = ((estatura.split('<td class="RespPop">'))[1].split(' mt'))[0] 
                            estatura = estatura.replace('.','').replace(',','')
                            if ( len(str(estatura)) == 2) :
                                estatura = str((int(estatura)) * 10)
                            #print 'Estatura :', estatura
                            sql = sql + ',' + estatura
                            row = row + ',' + estatura 
                        
                			# Breasts, Waist and Hips of our Escort:
                            pechos = 'null'
                            cintura = 'null'
                            caderas = 'null'
                            for items in EscortDataList :
                                if len (re.findall('Medidas', items)) :
                                    if len (re.findall(r'\<td\sclass\=\"RespPop\"\>', items)) :
                                        medidasList = items.split('<td class="RespPop">')
                                        medidas = (medidasList[1].split('</td>'))[0]
                                        medidas = medidas.replace('\n','')
                                        medidas = medidas.replace('\t','')
                                        #print 'Medidas :', medidas
                                        if len (re.findall(r'\d+\-\d+\-\d+', medidas)) :
                                            pechos = re.findall(r'(\d+)\-\d+\-\d+', medidas)[0]
                                            cintura = re.findall(r'\d+\-(\d+)\-\d+', medidas)[0]
                                            caderas = re.findall(r'\d+\-\d+\-(\d+)', medidas)[0]
                                        elif len (re.findall(r'\d+\W+\d+\W+\d+', medidas)) :
                                            pechos = re.findall(r'(\d+)\W+\d+\W+\d+', medidas)[0]
                                            cintura = re.findall(r'\d+\W+(\d+)\W+\d+', medidas)[0]
                                            caderas = re.findall(r'\d+\W+\d+\W+(\d+)', medidas)[0]
                            #print 'Pechos :', pechos
                            #print 'Cintura :', cintura
                            #print 'Caderas :', caderas
                            sql = sql + ',' + pechos + ',' + cintura + ',' + caderas
                            row = row + ',' + pechos + ',' + cintura + ',' + caderas
                            
                            # Escort Schedule (Days & Hours):
                            hastaDia = 'Vi'
                            inicio = ''
                            termino = ''
                            for items in EscortDataList :
                                if len (re.findall('Disponible', items)) :
                                    horariosList = items.split('<td class="RespPop">')
                                    horarios = horariosList[1].decode('iso-8859-1')
                                    #print 'horariosList[1]:', horariosList[1]
                                    if len (re.findall('[Ff]ull?\W*[Tt]ime', horarios)) :
                                        hastaDia = 'Do'
                                        inicio = '00:00'
                                        termino = '24:00'
                                    elif len (re.findall('\w+\sa\s\w+\sde\s\d+\sa\s\d+', horarios)) :
                                        hastaDia = re.findall('\w+\sa\s(\w+)\sde\s\d+\sa\s\d+', horarios)[0]
                                        inicio = re.findall('\w+\sa\s\w+\sde\s(\d+)\sa\s\d+',horarios)[0] + ':00'
                                        termino = re.findall('\w+\sa\s\w+\sde\s\d+\sa\s(\d+)',horarios)[0] + ':00'
                                    elif len (re.findall('\w+\W+a\W+\w+\W+\d+\W+a\W+\d+', horarios)) :
                                        hastaDia = re.findall('\w+\W+a\W+(\w+)\W+\d+\W+a\W+\d+', horarios)[0]
                                        inicio = re.findall('\w+\W+a\W+\w+\W+(\d+)\W+a\W+\d+', horarios)[0] + ':00'
                                        termino = re.findall('\w+\W+a\W+\w+\W+\d+\W+a\W+(\d+)', horarios)[0] + ':00'
                                    elif len (re.findall('\d+\W+\d+\W+[ap]m\W+\d+\W+\d+\W+', horarios)) :
                                        inicio = re.findall('(\d+\W+\d+)\W+[ap]m\W+\d+\W+\d+\W+', horarios)[0]
                                        termino = re.findall('\d+\W+\d+\W+[ap]m\W+(\d+\W+\d+)\W+', horarios)[0]
                                    elif len (re.findall('\w+\sa\s', horarios)):
                                        if len (re.findall(r'\sde\s\d+\sa\s\d+', horarios)) :
                                            hastaDiaList1 = horarios.split('\sde\s\d+\sa\s\d+')
                                            #print 'hastaDiaList1: ....................\n', hastaDiaList1, '\n........................'
                                            hastaDiaList2 = hastaDiaList1[0].split('\w+\sa\s')
                                            #print 'hastaDiaList2: ....................\n', hastaDiaList2, '\n........................'
                                            hastaDia = hastaDiaList2[0]#.decode('iso-8859-1')
                                        if len (re.findall(r'\sde\s(\d+)\sa\s\d+', horarios)) :
                                            inicio = re.findall('\sde\s(\d+)\sa\s\d+', horarios)[0] + ':00'
                                            termino = re.findall('\sde\s\d+\sa\s(\d+)', horarios)[0] + ':00'
                            #print 'Hasta Dia :', hastaDia
                            #print 'Inicio :', inicio
                            #print 'Termino :', termino
                            sql = sql + ',\'' + hastaDia + '\',\'' + inicio + '\',\'' + termino + '\''
                            row = row + ',' + hastaDia + ',' + inicio + ',' + termino
                            
                            # Preps for Location:
                            if len (re.findall(r'height\=\"350', EscortPage)) :
                                EscortItemsList = EscortPage.split('height="350')[1].split('class="Comentario"')[0].split('</tr>')
                                        
                			# Escort Location:
                            ubicacion = ''
                            lugar = ''
                            for partes in EscortItemsList :
                                if len (re.findall('Ubicaci', partes)) :
                                    ubicacion = (partes.split('<td class="RespPop">')[1]).split('</td>')[0]
                            #print 'Ubicacion :', ubicacion
                            for partes in EscortItemsList :
                                if len (re.findall('Atenci', partes)) :
                                    #print 'Lugar Atenci : ....................\n', partes, '\n...............................\n'
                                    lugar = partes.split('<td class="RespPop">')[1].split('</td>')[0]
                                    lugar = lugar.replace(',','.')
                            #print 'Lugar :', lugar
                            ubicacionLenLista += [len(ubicacion + '. ' + lugar)]
                            #print 'Largo String Lugar:', str(len(ubicacion + '. ' + lugar))
                            sql = sql + ',\'' + ubicacion + '. ' + lugar + '\''
                            row = row + ',' + ubicacion + '. ' + lugar
                            
                            # Standard Services of the Escort:  
                            servicios = ''
                            for items in EscortDataList :
                                if len (re.findall('Servicios:', items)) :
                                    servicios = (items.split('<td class="RespPop">')[1]).split('<div>')[0]
                                    servicios = servicios.replace('\n','')
                                    servicios = servicios.replace('\t','')
                                    servicios = servicios.replace(' ','')
                                    #print 'Servicios :', servicios
                            serviciosLenLista += [len(servicios)]
                            #print 'Largo String Servicios:', str(len(servicios))
                            sql = sql + ',\'' + servicios + '\''
                            row = row + ',' + servicios
                            
                            # Additional Services of the Escort:  
                            adicionales = ''
                            for items in EscortDataList :
                                if len (re.findall('trans_box2', items)) :
                                    #print 'items.split(trans_box2)[1] :.....................', items.split('trans_box2')[1], '\n.....................\n'
                                    adicionalesBlock = items.split('trans_box2')[1]
                                    if len (re.findall('<div id=\w*>\w*\W*?\w*?\W*?\w*?\<\/div\>', adicionalesBlock)) :
                                        adicionalesList = re.findall('<div id=\w*>(\w*\W*?\w*?\W*?\w*?)\<\/div\>', adicionalesBlock)
                                        for cadaAdicional in adicionalesList :
                                            adicionales += cadaAdicional + '. '
                                        #print 'Adicionales :', adicionales
                            adicionalesLenLista += [len(adicionales)]
                            #print 'Largo String Adicionales:', str(len(adicionales))
                            sql = sql + ',\'' + adicionales + '\');\n'
                            row = row + ',' + adicionales
            
                            #print row #, '\n==============================================\n\n'
                            time.sleep(Decimal(Decimal(randrange(iTime,fTime,sTime)) / Decimal(1000)))
    
            
        # Mi Privado Scraper:
        elif len (re.findall(r'miprivado', urls)) :
            if len (re.findall('\:\:\/escort\/', html)) :
                EscortURLsList = html.split('form-select')[1].split('</select>')[0].split('::')
                for url in EscortURLsList :
                    if ( len (re.findall('\/escort\/\d+\/', url))) :
                        # Example: http://miprivado.cl/node/811/lightbox/ 
                        EscortURL = 'http://miprivado.cl/node/' + re.findall('\/escort\/(\d+)\/', url)[0] + '/lightbox/'
                        #print 'Escort Page: ', EscortURL
                        print '\n========================= Inicia Escort MiPrivado ==========================='
                        
                        # Escort Page Data Preps:
                        request = urllib2.Request(EscortURL)
                        request.add_header('User-Agent', 'Mozilla/5.0')
                        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)
                        try:
                            EscortPage = opener.open(request).read()
                            sql = sql + 'INSERT INTO escortssantiago(Escort,Edad,Tarifa,Telefono,Estatura,Busto,Cintura,Culo,Hasta_Dia,Inicio,Termino,Lugar,Servicios,Adicionales) VALUES ('
                            # Name of the Escort:
                            nombre = ''
                            if len (re.findall('nombre\-ficha', EscortPage)) :
                                nombre = EscortPage.split('nombre-ficha">')[1].split('</div>')[0].replace('\n', '')
                            print 'Nombre :', nombre
                            anchor = '<a href="' + EscortURL + '" target="_blank">' + nombre + '</a>'
                            print 'Escort URL:', EscortURL
                            anchorLenLista += [len('<a href="' + EscortURL + '" target="_blank">' + nombre + '</a>')]
                            #print 'Largo String Anchor:', str(len('<a href="' + EscortURL + '" target="_blank">' + nombre + '</a>'))
                            sql = sql + '\'' + anchor + '\''
                            row = '<a href="' + EscortURL + '" target="_blank">' + nombre + '</a>'
                            
                            # Age of the Escort:
                            edad = 'null'
                            if len (re.findall('Edad\:', EscortPage)) :
                                edad = re.findall('\d\d', EscortPage.split('Edad:</span> ')[1].split('</div>')[0])[0]
                            print 'Edad :', edad
                            sql = sql + ',' + edad
                            row = row + ',' + edad
                            
                            # Rate & Price of the Escort Services:
                            tarifa = 'null'
                            if len (re.findall('Consultar', EscortPage)) :
                                tarifa = 'null'
                            elif len (re.findall('valor\-ficha', EscortPage)) :
                                tarifa = EscortPage.split('valor-ficha"><span class="label-ficha">Valor</span> $')[1].split('</div>')[0]
                                if len (re.findall('\<a\sclass\=', tarifa)) :
                                    tarifa = tarifa.split('<a class=')[0]
                            tarifa = tarifa.replace(' ','').replace('.','')
                            if not len (re.findall(r'\d+', tarifa)) :
                                tarifa = 'null'
                            print 'Tarifa :', tarifa
                            sql = sql + ',' + tarifa
                            row = row + ',' + tarifa
                            
                            # Phone Number of the Escort:
                            telefono = 'null'
                            if len (re.findall('telefono\-ficha', EscortPage)) :
                                telefonoString101 = EscortPage.split('telefono-ficha"><span class="label-ficha">Tel')[1]
                                telefono = telefonoString101.split('</div>')[0].split('</span>')[1].replace(' ','')
                            print 'Telefono :', telefono
                            sql = sql + ',' + telefono
                            row = row + ',' + telefono
                            
                            # Height of the Escort:
                            estatura = 'null'
                            if len (re.findall('estatura\-ficha', EscortPage)) :
                                estaturaString101 = EscortPage.split('Estatura:')[1]
                                estaturaString102 = estaturaString101.split('</div>')[0]
                                estatura = re.findall('\d+\.\d+', estaturaString102)[0].replace('.', '')
                                if (len(estatura) == 2) : estatura = str(int(estatura)*10)
                            print 'Estatura :', estatura
                            sql = sql + ',' + estatura
                            row = row + ',' + estatura
                            
                            # Breasts, Waist and Hips of our Escort:
                            pechos = 'null'
                            cintura = 'null'
                            caderas = 'null'
                            if len (re.findall('Medidas\:', EscortPage)) :
                                medidas = EscortPage.split('Medidas:</span> ')[1].split('</div>')[0]
                                print 'Medidas :', medidas
                                if len (re.findall('\W*\d+\W*\d+\W*\d+', medidas)) :
                                    pechos = re.findall('\W*(\d+)\W*\d+\W*\d+', medidas)[0]
                                    cintura = re.findall('\W*\d+\W*(\d+)\W*\d+', medidas)[0]
                                    caderas = re.findall('\W*\d+\W*\d+\W*(\d+)', medidas)[0]
                            print 'Pechos :', pechos
                            print 'Cintura :', cintura
                            print 'Caderas :', caderas
                            sql = sql + ',' + pechos + ',' + cintura + ',' + caderas
                            row = row + ',' + pechos + ',' + cintura + ',' + caderas
                            
                            # Escort Schedule (Days & Hours):
                            hastaDia = 'Vi'
                            inicio = ''
                            termino = ''
                            if len (re.findall('horario\-ficha', EscortPage)) :
                                horarios = EscortPage.split('Horario:</span> ')[1].split('</div>')[0]
                                print 'Horarios :', horarios
                                if len (re.findall('[Ff]ull\s[Tt]ime', horarios)) :
                                    #print 'Block 1'
                                    hastaDia = 'Do'
                                    inicio = '00:00'
                                    termino = '24:00'
                                    if len (re.findall('bado', horarios)) :
                                        #print 'Block 2'
                                        hastaDia = 'Sa'
                                        inicio = '00:00'
                                        termino = '24:00'
                                        
                                elif len (re.findall('\d+\:\d+\sa\s\d+\:\d+', horarios)) :
                                    #print 'Block 3'
                                    hastaDia = 'Vi'
                                    inicio = re.findall('(\d+\:\d+)\sa\s\d+\:\d+', horarios)[0]
                                    #print 'Inicio :', inicio
                                    termino = re.findall('\d+\:\d+\sa\s(\d+\:\d+)', horarios)[0]
                                    #print 'Termino :', termino
                                    
                                elif len (re.findall('\d+\:\d+\sa\s\d+\:[Hh][Rr][Ss]', horarios)) :
                                    #print 'Block 4'
                                    inicio = re.findall('(\d+\:\d+)\sa\s\d+\:[Hh][Rr][Ss]', horarios)[0]
                                    #print 'Inicio :', inicio
                                    termino = re.findall('\d+\:\d+\sa\s(\d+)\:[Hh][Rr][Ss]', horarios)[0] + ':00'
                                    #print 'Termino :', termino
                                    if len (re.findall('abado', horarios)) : 
                                        #print 'Block 4'
                                        hastaDia = 'Sa'
                                elif len (re.findall('[Vv]iernes', horarios)) :
                                    #print 'Block 5'
                                    hastaDia = 'Vi'
                                elif len (re.findall('\d+\:\d+\w+\sa\s\d+\:\d+', horarios)) :
                                    #print 'Block 6'
                                    inicio = re.findall('(\d+\:\d+)\w+\sa\s\d+\:\d+', horarios)[0]
                                    termino = re.findall('\d+\:\d+\w+\sa\s(\d+\:\d+)', horarios)[0]
                                    if len (re.findall('bado', horarios)) :
                                        #print 'Block 7'
                                        hastaDia = 'Sa'
                                    if len (re.findall('[Dd]omingo', horarios)) :
                                        #print 'Block 8'
                                        hastaDia = 'Do'
                            print 'Hasta Dia:', hastaDia
                            print 'Inicio :', inicio
                            print 'Termino :', termino
                            sql = sql + ',\'' + hastaDia + '\',\'' + inicio + '\',\'' + termino + '\''
                            row = row + ',' + hastaDia + ',' + inicio + ',' + termino
                            
                            # Escort Location:
                            ubicacion = ''
                            lugar = ''
                            if len (re.findall('Sector\:', EscortPage)) :
                                ubicacion = EscortPage.split('Sector:</span> ')[1].split('</div>')[0]
                            print 'Ubicacion :', ubicacion
                            if len (re.findall('Atención\:', EscortPage)) :
                                lugar = EscortPage.split('Atención:</span> ')[1].split('</div>')[0].replace(',', '.')
                            print 'Lugar :', lugar
                            ubicacionLenLista += [len(ubicacion + '. ' + lugar)]
                            print 'Largo String Lugar:', str(len(ubicacion + '. ' + lugar))
                            sql = sql + ',\'' + ubicacion + '. ' + lugar + '\''
                            row = row + ',' + ubicacion + '. ' + lugar
                            
                            # Standard Services of the Escort:
                            servicios = ''
                            adicionales = ''
                            if len (re.findall('Servicios\:', EscortPage)) :
                                servicios = EscortPage.split('Servicios:</span> ')[1].split('<a class="')[0].replace('\n','')
                            print 'Servicios :', servicios
                            serviciosLenLista += [len(servicios)]
                            print 'Largo String Servicios', str(len(servicios))
                            sql = sql + ',\'' + servicios + '\''
                            row = row + ',' + servicios
                            
                            # Additional Services of the Escort:
                            adicionales = ''
                            if len (re.findall('sevicios\-ficha', EscortPage)) :
                                adicionalesList = EscortPage.split('sevicios-ficha')[1].split('</li>')
                                for adicionalesItem in adicionalesList :
                                    #print 'adicionalesItem : ------------------------\n', adicionalesItem, '\n---------------------'
                                    if len (re.findall('first', adicionalesItem)) :
                                        adicionales += adicionalesItem.split('<li class="first">')[1] + '. '
                                        #print 'Block 10 :', adicionalesItem.split('<li class="first">')[1]
                                    elif len (re.findall('\<li\>', adicionalesItem)) :
                                        adicionales += adicionalesItem.split('<li>')[1] + '. '
                                        #print 'Block 11 :', adicionalesItem.split('<li>')[1]
                                    elif len (re.findall('last', adicionalesItem)) :
                                        adicionales += adicionalesItem.split('<li class="last">')[1] + '.'
                                        #print 'Block 12 :', adicionalesItem.split('<li class="last">')[1]
                                        break
                            print 'Adicionales :', adicionales
                            adicionalesLenLista += [len(adicionales)]
                            print 'Largo String Adicionales:', str(len(adicionales))
                            sql = sql + ',\'' + adicionales + '\');\n'
                            row = row + ',' + adicionales
            
                            print row
                            time.sleep(Decimal(Decimal(randrange(iTime,fTime,sTime)) / Decimal(1000)))
                        
                        except:
                            print 'Error al tratar de abrir URL :', url, '!!!\n==============================\n\n'

        # Planeta Escort Scraper:
        elif len (re.findall(r'planetaescort', urls)) :
            if len (re.findall(r'\{\"id\"\:', html)) :
                # Getting Data Escort from Category Pages :
                EscortDataBlocks = html.split('{"id":')
                #print 'EscortDataBlocks[1]', EscortDataBlocks[1]
                for EscortData in EscortDataBlocks :
                    if len(re.findall(r'nombre', EscortData)) :
                        row = ''
                        sql = sql + 'INSERT INTO escortssantiago(Escort,Edad,Tarifa,Telefono,Estatura,Busto,Cintura,Culo,Hasta_Dia,Inicio,Termino,Lugar,Servicios,Adicionales) VALUES ('
                        # Escort Name:
                        nombre = EscortData.split('"nombre":"')[1].split('","')[0]
                        #print 'Nombre :', nombre
                        
                        # Escort URL:
                        escortURL = 'http://www.planetaescort.cl/ie/_html/ficha.php?fichaID=' + EscortData.split(',"nombre":"')[0]
                        anchor = '<a href="http://www.planetaescort.cl/ie/_html/ficha.php?fichaID=' + EscortData.split(',"nombre":"')[0] + '" target="_blank">' + nombre + '</a>'
                        anchorLenLista += [len(anchor)]
                        print 'Largo String Anchor:......', len(anchor)
                        #print 'Escort URL: ', escortURL
                        #print 'Enlace :', anchor
                        sql = sql + '\'' + anchor + '\''
                        row = row + anchor
                        
                        # Escort Page preps:
                        htmlfile = urllib.urlopen(escortURL)
                        EscortPage = htmlfile.read()
                        EscortPage = EscortPage.replace('&aacute;','á').replace('&eacute;','é').replace('&iacute;','í').replace('&oacute;','ó').replace('&uacute;','ú')
                        EscortPage = EscortPage.replace('&Aacute;','Á').replace('&Eacute;','É').replace('&Iacute;','Í').replace('&Oacute;','Ó').replace('&Uacute;','Ú')
                        EscortPage = EscortPage.replace('&ntilde;','ñ').replace('&Ntilde;','Ñ')
        
                        # Age of the Escort:
                        edad = 'null'
                        if len (re.findall(r'edad\"\:\"', EscortData)) :
                            edad = EscortData.split('edad":"')[1].split('","')[0]
                        print 'Edad :', edad
                        sql = sql + ',' + edad
                        row = row + ',' + edad
                        
                        # Rate & Price of the Escort Services:
                        valor = EscortData.split('valor":"')[1].split('","')[0]
                        valor = str(int(valor)/1000) + '.000'
                        valor = valor.replace('.','')
                        if not len (re.findall(r'', valor)) :
                            valor = 'null'
                        #print 'Tarifa :', valor
                        sql = sql + ',' + valor
                        row = row + ',' + valor
                        
                        # Phone Contact of the Escort:
                        telefono = 'null'
                        if len (re.findall(r'contacto\"\:\"', EscortData)) :
                            telefono = EscortData.split('contacto":"')[1].split('","')[0].replace(' ','')
                        print 'Telefono :', telefono
                        sql = sql + ',' + telefono
                        row = row + ',' + telefono
                        
                        # Height of the Escort:
                        estatura = 'null'
                        if len (re.findall(r'estatura\"\:\"', EscortData)) :
                            estatura = EscortData.split('estatura":"')[1].split('","')[0]
                        print 'Estatura :', estatura
                        sql = sql + ',' + estatura
                        row = row + ',' + estatura
                        
                        # Breasts, Waist and Hips of our Escort:
                        pechos = 'null'
                        cintura = 'null'
                        caderas = 'null'
                        if len (re.findall(r'Medidas\:', EscortPage)) :
                            medidas = EscortPage.split('Medidas:')[1].split('</dl>')[0]
                            medidas = medidas.replace('</dt>','').replace('<dd>','').replace('\n','').replace('\t','').replace('</dd>','')
                            if len (re.findall(r'\d+\W*\d+\W*\d+', medidas)) :
                                pechos = re.findall(r'(\d+)\W*\d+\W*\d+', medidas)[0]
                                cintura = re.findall(r'\d+\W*(\d+)\W*\d+', medidas)[0]
                                caderas = re.findall(r'\d+\W*\d+\W*(\d+)', medidas)[0]
                        print 'Medidas :', medidas
                        print 'Pechos :', pechos
                        print 'Cintura :', cintura
                        print 'Caderas :', caderas
                        sql = sql + ',' + pechos + ',' + cintura + ',' + caderas
                        row = row + ',' + pechos + ',' + cintura + ',' + caderas
                        
                        # Days & Hours of Escort Schedule:
                        hastaDia = 'Vi'
                        inicio = ''
                        termino = ''
                        if len (re.findall(r'movimiento', EscortPage)) :
                            horario = EscortPage.split('<span id="movimiento">')[1].split('</span>')[0]
                            horario = horario.replace('\n','').replace('\t','')
                            #print 'Horario :', horario
                            if len (re.findall(r'[Pp]art\s[Tt]ime', horario)) :
                                hastaDia = 'Vi'
                                if len (re.findall(r'\d+\:\d+', horario)) :
                                    inicio = re.findall(r'\d+\:\d+', horario)[0]
                                    termino = re.findall(r'\d+\:\d+', horario)[1]
                            elif len (re.findall(r'[Ff]ull [Tt]ime', horario)) :
                                hastaDia = 'Do'
                                inicio = '00:00'
                                termino = '24:00'
                            elif len (re.findall(r'Sabado', horario)) :
                                hastaDia = 'Sa'
                            elif len(re.findall(r'\d+\:\d+', horario)) :
                                hastaDia = 'Vi'
                                inicio = re.findall(r'\d+\:\d+', horario)[0]
                                termino = re.findall(r'\d+\:\d+', horario)[1]
                        #print 'Hasta Dia :', hastaDia
                        #print 'Inicio :', inicio
                        #print 'Termino :', termino
                        sql = sql + ',\'' + hastaDia + '\',\'' + inicio + '\',\'' + termino + '\''
                        row = row + ',\'' + hastaDia + '\',\'' + inicio + '\',\'' + termino + '\''
                        
                        # Escort Location:
                        ubicacion = ''
                        if len (re.findall(r'Sector\:', EscortPage)) :
                            ubicacion = EscortPage.split('Sector:')[1].split('</dd>')[0]
                            ubicacion = ubicacion.replace('\n', '').replace('\t', '').replace('</dt>','').replace('<dd>','')
        
                        #print 'Ubicacion :', ubicacion
        
                        # Space of the Escort:
                        lugar = ''
                        if len (re.findall(r'Atenci', EscortPage)) :
                            lugar = EscortPage.split('Atenci')[1].split('</dd>')[0].split('<dd>')[1]
                            lugar = lugar.replace('\n','').replace('\t','').replace(',','.')
                        #print 'Lugar :', lugar
                        sql = sql + ',\'' + ubicacion + '. ' + lugar + '\''
                        print 'Largo String Ubicacion:...', str(len(ubicacion)+len(lugar))
                        ubicacionLenLista += [2+len(ubicacion)+len(lugar)]
                        row = row + ',\'' + ubicacion + '. ' + lugar + '\''    
                            
                        # Standard Services of the Escort:
                        servicios = ''
                        if len (re.findall(r'servicios\_ficha', EscortData)) :
                            servicios = EscortData.split('servicios_ficha":"')[1].split('","')[0].replace('(','').replace(')','').replace(',','.')
                        serviciosLenLista += [len(servicios)]
                        print 'Largo String Servicios:...', str(len(servicios))
                        #print 'Servicios :', servicios
                        
                        # Additional Services of the Escort:
                        adicionales = ''
                        if len (re.findall(r'detalle\-corner', EscortPage)) :
                            adicionales = EscortPage.split('detalle-corner')[1].split('</div>')[1]
                            adicionales = adicionales.replace('\n','').replace('\t','').replace('<br />','. ').replace('(','').replace(')','').replace(',','.')
                            adicionalesLenLista += [len(adicionales)]
                            print 'Largo String Adicionales:', str(len(adicionales))
        
                        #print 'Adicionales :', adicionales
                        sql = sql + ',\'' + servicios + '\',\'' + adicionales + '\');\n'
                        row = row + ',\'' + servicios + '\',\'' + adicionales + '\');'
                        time.sleep(Decimal(Decimal(randrange(iTime,fTime,sTime)) / Decimal(1000)))
                        print row + '\n------------------------------------\n'
       
        # Infierno Hot Scraper:                
        if len (re.findall(r'infiernohot', urls)) :
            if len (re.findall(r'Escort\sDestacadas', html)) :
                EscortDataBlocks = html.split('Escort Destacadas')[1].split('<h3><a href="')
                for block in EscortDataBlocks :
                    escortData = block.split('</h3>')[0]
                    #print 'Escort Data:', escortData
                    if len (re.findall(r'\/escort\-', escortData)) :
                        #print 'Escort Data:', escortData
                        escortURL = 'http://infiernohot.cl' + escortData.split('">')[0]
                        print 'Escort URL:', escortURL
                        nombre = escortData.split('">')[1].split('</a>')[0]
                        enlace = '<a href="' + escortURL + '" target="_blank">' + nombre + '</a>'
                        #print 'Enlace:', enlace
                        anchorLenLista += [len(enlace)]
                        #print 'Nombre:', nombre
                        
                        # Escort Page preps:
                        htmlfile = urllib.urlopen(escortURL)
                        EscortPage = htmlfile.read()
                        EscortPage = EscortPage.replace('&aacute;','á').replace('&eacute;','é').replace('&iacute;','í').replace('&oacute;','ó').replace('&uacute;','ú')
                        EscortPage = EscortPage.replace('&Aacute;','Á').replace('&Eacute;','É').replace('&Iacute;','Í').replace('&Oacute;','Ó').replace('&Uacute;','Ú')
                        EscortPage = EscortPage.replace('&ntilde;','ñ').replace('&Ntilde;','Ñ')
                        
                        sql = sql + 'INSERT INTO escortssantiago(Escort,Edad,Tarifa,Telefono,Estatura,Busto,Cintura,Culo,Hasta_Dia,Inicio,Termino,Lugar,Servicios,Adicionales) VALUES ('
                        sql = sql + '\'' + enlace + '\''
                        
                        edad = 'null'
                        if len (re.findall(r'EDAD\:\<\/span\>', EscortPage)) :
                            edad = EscortPage.split('EDAD:</span>')[1].split('</span>')[0].split('<span class="product-field-display">')[1]
                            if len (re.findall(r'\d\d', edad)) :
                                edad = re.findall(r'(\d\d)', edad)[0]
                            else : edad = 'null'
                        #print 'Edad:', edad
                        sql = sql + ',' + edad
                            
                        tarifa = ''
                        if len (re.findall(r'Precio\:', EscortPage)) :
                            tarifa = EscortPage.split('Precio:')[1].split('$')[1].split('</span>')[0]
                        tarifa = tarifa.replace('.','')
                        if not len (re.findall(r'\d+', tarifa)) :
                            tarifa = 'null'
                        sql = sql + ',' + tarifa
                        #print 'Tarifa:', tarifa
                        
                        telefono = 'null'
                        if len (re.findall(r'Contacto\W+\d+\W*\d+', EscortPage)) :
                            telefono = re.findall(r'Contacto\W+(\d+\W*\d+)', EscortPage)[0]
                            telefono = telefono.replace(' ','')
                        elif len (re.findall(r'Contactos\W+\d+\W*\d+', EscortPage)) :
                            telefono = re.findall(r'Contactos\W+(\d+\W*\d+)', EscortPage)[0]
                            telefono = telefono.replace(' ','')
                        elif len (re.findall(r'\:\s\d{4}\s\d{4}', EscortPage)) :
                            telefono = re.findall(r'\:\s(\d{4}\s\d{4})', EscortPage)[0]
                            telefono = telefono.replace(' ','')
                            
                        sql = sql + ',' + telefono
                        #print 'Telefono:', telefono
                        
                        estatura = 'null'
                        if len (re.findall(r'ESTATURA\:', EscortPage)) :
                            estatura = EscortPage.split('ESTATURA:')[1].split('mts.')[0].split('<span class="product-field-display">')[1]
                            estatura = estatura.replace('.','').replace(',','')
                            if len (estatura) == 2 :
                                estatura = str(int(estatura) * 10)
                        sql = sql + ',' + estatura
                        #print 'Estatura:', estatura
                        
                        medidas = 'null'
                        pechos = 'null'
                        cintura = 'null'
                        caderas = 'null'
                        if len (re.findall(r'MEDIDAS\:', EscortPage)) :
                            medidas = EscortPage.split('MEDIDAS:')[1].split('<span class="product-field-desc">')[0].split('<span class="product-field-display">')[1].split('</span>')[0]
                            if len (re.findall(r'\d+\W+\d+\W+\d+', medidas)) :
                                pechos = re.findall(r'(\d+)\W+\d+\W+\d+', medidas)[0]
                                cintura = re.findall(r'\d+\W+(\d+)\W+\d+', medidas)[0]
                                caderas = re.findall(r'\d+\W+\d+\W+(\d+)', medidas)[0]
                        sql = sql + ',' + pechos + ',' + cintura + ',' + caderas 
                        #print 'Medidas:', medidas
                        #print 'Pechos:', pechos
                        #print 'Cintura:', cintura
                        #print 'Caderas:', caderas
                        
                        horario = ''
                        inicio = '15:00'
                        termino = '18:00'
                        hastaDia = 'Vi'
                        if len (re.findall(r'HORARIO\:', EscortPage)) :
                            horario = EscortPage.split('HORARIO:')[1].split('<span class="product-field-desc">')[0].split('<span class="product-field-display">')[1].split('</span>')[0]
                        print 'Horario:', horario, '\n----------------------------\n'
                        if len (re.findall(r'Full', horario)) :
                            hastaDia = 'Do'
                            inicio = '00:00'
                            termino = '24:00'
                        elif len (re.findall(r'Part', horario)) :
                            hastaDia = 'Vi'
                            inicio = '14:00'
                            terminio = '18:00'
                        if len (re.findall(r'\d\d?\W*am', horario)) :
                            inicio = re.findall(r'(\d\d?)\W*am', horario)[0] + ':00'
                        if len (re.findall(r'\d\d?\W*pm', horario)) :
                            termino = str(int(re.findall(r'(\d\d?)\W*pm', horario)[0]) + 12) + ':00'
                        if len (re.findall(r'\d+\W*a\W*\d+', horario)) :
                            inicio = re.findall(r'(\d+)\W*a\W*\d+', horario)[0] + ':00'
                            termino = re.findall(r'\d+\W*a\W*(\d+)', horario)[0] + ':00'
                        #print 'Hasta Dia:', hastaDia
                        #print 'Inicio:', inicio
                        #print 'Termino', termino
                        sql = sql + ',\'' + hastaDia + '\',\'' + inicio + '\',\'' + termino + '\''
                        
                        sector = ''
                        habitacion = ''
                        lugar = ''
                        if len (re.findall(r'SECTOR\:', EscortPage)) :
                            sector = EscortPage.split('SECTOR:')[1].split('<span class="product-field-desc">')[0].split('<span class="product-field-display">')[1].split('</span>')[0]
                        #print 'Sector:', sector
                        if len (re.findall(r'ATENCION:', EscortPage)) :
                            habitacion = EscortPage.split('ATENCION:')[1].split('<span class="product-field-desc">')[0].split('<span class="product-field-display">')[1].split('</span>')[0]
                        #print 'Habitacion:', habitacion
                        lugar = (sector + '. ' + habitacion).replace(',','.')
                        ubicacionLenLista += [len(lugar)]
                        sql = sql + ',\'' + lugar + '\''
                        #print 'Lugar:', lugar
                        
                        servicios = 'Normales'
                        adicionales = ''
                        if len (re.findall(r'SERVICIOS\:', EscortPage)) :
                            adicionales = EscortPage.split('SERVICIOS:')[1].split('<span class="product-field-desc">')[0].split('<span class="product-field-display">')[1].split('</span>')[0]
                            adicionales = adicionales.replace(',','.')
                            if len (re.findall(r'Normales', adicionales)) :
                                servicios = 'Normales'
                            elif len (re.findall(r'Completos', adicionales)) :
                                servicios = 'Completos'
                        sql = sql + ',\'' + servicios + '\',\'' + adicionales + '\');\n'
                        serviciosLenLista += [len(servicios)]
                        adicionalesLenLista += [len(adicionales)]
                        #print 'Adicionales', adicionales
                        #print 'Servicios:', servicios, '\n----------------------------\n'
    
                        time.sleep(Decimal(Decimal(randrange(iTime,fTime,sTime)) / Decimal(1000)))
                        
        # MiEscort.CL Scraper:                
        if len (re.findall(r'miescort', urls)) :
            if len (re.findall(r'Seleccione\.\.\.\<\/option\>', html)) :
                EscortDataBlocks = html.split('Seleccione...</option>')[1].split('</select>')[0].split('</option>')
                print 'EscortDataBlocks: ', EscortDataBlocks
                for block in EscortDataBlocks :
                    if len (re.findall(r'option\svalue', block)) :
                        escortURL = 'http://miescort.cl/?' + re.findall(r'\d+', block)[0]
                        print 'Escort URL:', escortURL
                        nombre = block.split('>')[1]
                        print 'Nombre:', nombre
                        enlace = '<a href="' + escortURL + '" target="_blank">' + nombre + '</a>'
                        anchorLenLista += [len(enlace)]
                        print 'Enlace:', enlace
                        

                        # Escort Page preps:
                        htmlfile = urllib.urlopen(escortURL)
                        EscortPage = htmlfile.read()
                        EscortPage = EscortPage.replace('&aacute;','á').replace('&eacute;','é').replace('&iacute;','í').replace('&oacute;','ó').replace('&uacute;','ú')
                        EscortPage = EscortPage.replace('&Aacute;','Á').replace('&Eacute;','É').replace('&Iacute;','Í').replace('&Oacute;','Ó').replace('&Uacute;','Ú')
                        EscortPage = EscortPage.replace('&ntilde;','ñ').replace('&Ntilde;','Ñ')
                        
                        sql = sql + 'INSERT INTO escortssantiago(Escort,Edad,Tarifa,Telefono,Estatura,Busto,Cintura,Culo,Hasta_Dia,Inicio,Termino,Lugar,Servicios,Adicionales) VALUES ('
                        sql = sql + '\'' + enlace + '\''
                        
                        
                        # Age of the Escort:
                        edad = 'null'
                        if len (re.findall(r'lblFieldEdad', EscortPage)) :
                            edad = EscortPage.split('lblFieldEdad')[1].split('</span>')[0]
                            edad = re.findall(r'\d+', edad)[0]
                            sql = sql + ',' + edad
                            print 'Edad:', edad
                            
                        # Price of the Escort's Services:
                        tarifa = 'null'
                        if len (re.findall(r'lblFieldValor', EscortPage)) :
                            tarifa = EscortPage.split('lblFieldValor')[1].split('</span>')[0]
                            tarifa = re.findall(r'\d+\.\d+', tarifa)[0].replace('.','')
                            sql = sql + ',' + tarifa
                            print 'Tarifa:', tarifa
                            
                        # Telephone of the Escort:
                        telefono = 'null'
                        if len (re.findall(r'lblField', EscortPage)) :
                            telefono = EscortPage.split('lblFieldFono')[1].split('</span>')[0]
                            telefono = re.findall(r'\d+', telefono)[0]
                            sql = sql + ',' + telefono
                            print 'Telefono:', telefono
                            
                        # Height of the Escort:
                        estatura = 'null'
                        if len (re.findall(r'lblFieldEstatura', EscortPage)) :
                            estatura = EscortPage.split('lblFieldEstatura')[1].split('</span>')[0]
                            estatura = re.findall(r'\d+\W\d+', estatura)[0].replace(',','').replace('.','')
                            sql = sql + ',' + estatura
                            print 'Estatura:', estatura
                            
                        # Measurements of the Escort:
                        medidas = ''                        
                        busto = 'null'
                        cintura = 'null'
                        caderas = 'null'
                        if len (re.findall(r'lblFieldMedidas', EscortPage)) :
                            medidas = EscortPage.split('lblFieldMedidas')[1].split('</span>')[0]
                            if len (re.findall(r'\d+\W\d+\W\d+', medidas)) :
                                medidas = re.findall(r'\d+\W\d+\W\d+', medidas)[0]
                                busto = re.findall(r'(\d+)\W\d+\W\d+', medidas)[0]
                                cintura = re.findall(r'\d+\W(\d+)\W\d+', medidas)[0]
                                caderas = re.findall(r'\d+\W\d+\W(\d+)', medidas)[0]
                        sql = sql + ',' + busto + ',' + cintura + ',' + caderas
                        print 'Medidas:', medidas,'\n','Busto:', busto, '\n', 'Cintura:', cintura, '\n', 'Caderas:', caderas
                        
                        horario = ''
                        inicio = '15:00'
                        termino = '18:00'
                        hastaDia = 'Vi'
                        if len (re.findall(r'lblFieldHorario', EscortPage)) :
                            horario = EscortPage.split('lblFieldHorario')[1].split('</span>')[0].split('>')[1]
                            if len (re.findall(r'Full\sTime', horario)) :
                                inicio = '00:00'
                                termino = '24:00'
                                hastaDia = 'Do'
                            elif len (re.findall(r'lblFieldHorarioComentario', EscortPage)) :
                                horario = horario + '. ' +  EscortPage.split('lblFieldHorarioComentario')[1].split('</span>')[0].split('>')[1]
                                if len (re.findall(r'[Ba][Aa]', horario)) :
                                    hastaDia = 'Sa'
                                if len (re.findall(r'\d\d\:\d\d', horario)) :
                                    inicio = re.findall(r'\d\d\:\d\d', horario)[0]
                                    if len (re.findall(r'\d\d\:\d\d', horario)) == 2 :
                                        termino = re.findall(r'\d\d\:\d\d', horario)[1]
                                elif len (re.findall(r'\d\d', horario)) :
                                    inicio = re.findall(r'\d\d', horario)[0] + ':00'
                                    if len (re.findall(r'\d\d', horario)) == 2 :
                                        termino = re.findall(r'\d\d', horario)[1] + ':00'
                        sql = sql + ',\'' + inicio + '\',\'' + termino + '\',\'' + hastaDia + '\''
                        print 'Horario:', horario
                        print 'Inicio:', inicio
                        print 'Termino:', termino
                        print 'Hasta Dia:', hastaDia
                        
                        lugar = ''
                        habitacion = ''
                        if len (re.findall(r'lblFieldSector', EscortPage)) :
                            lugar = EscortPage.split('lblFieldSector')[1].split('</span>')[0].split('>')[1]
                        if len (re.findall(r'lblTituloAtencion', EscortPage)) :
                            habitacionLista = EscortPage.split('lblTituloAtencion')[1].split('<div style="float:none;">')[0]
                            habitacionLista = habitacionLista.split('</span>')
                            for habitacionItem in habitacionLista :
                                if len (re.findall(r'FichaField', habitacionItem)) :
                                    habitacion = habitacion + habitacionItem.split('FichaField">')[1] + '. '
                            #print 'Lista de Habitaciones:', habitacion
                        lugar = lugar + '. ' + habitacion
                        ubicacionLenLista += [len(lugar)]
                        sql = sql + ',\'' + lugar + '\''
                        print 'Lugar:', lugar
                        
                        servicios = 'Normales'
                        adicionales = ''
                        serviciosBlock = ''
                        if len (re.findall(r'lblTituloTipoServicio', EscortPage)) :
                            serviciosLista = EscortPage.split('lblTituloTipoServicio')[1].split('<div style="float:none;">')[0].split('</span>')
                            for serviciosItem in serviciosLista :
                                if len(re.findall(r'FichaField', serviciosItem)) :
                                    serviciosBlock = serviciosBlock + serviciosItem.split('FichaField">')[1] + '. '
                                    if len(re.findall(r'Incluye\sColita', serviciosBlock)) :
                                        servicios = 'Completos'
                        serviciosLenLista += [len(servicios)]
                        sql = sql + ',\'' + servicios + '\''
                        print 'Servicios Normales o Completos:', serviciosBlock                
                        print 'Servicios:', servicios
                        
                        adicionales = ''
                        if len (re.findall(r'Americana', serviciosBlock)) :
                            adicionales = 'Americana. '
                        if len (re.findall(r'Colita', serviciosBlock)) :
                            adicionales = adicionales + 'Sexo Anal. '
                        if len (re.findall(r'lblTituloServicios', EscortPage)) :
                            adicionalesLista = EscortPage.split('lblTituloServicios')[1].split('<div style="float:none;">')[0].split('</span>')
                            for adicionalesItem in adicionalesLista :
                                if len (re.findall(r'FichaField', adicionalesItem)) :
                                    adicionales = adicionales + adicionalesItem.split('FichaField">')[1] + '. '
                        adicionalesLenLista += [len(adicionales)]
                        sql = sql + ',\'' + adicionales + '\');\n'
                        print 'Adicionales:', adicionales, '\n================================\n'
                        

                        time.sleep(Decimal(Decimal(randrange(iTime,fTime,sTime)) / Decimal(1000)))
                        
        # Ponelo Premium Scraper:                
        if len (re.findall(r'ponelo', urls)) :
            print 'Inicia Ponelo Premium'
            if len (re.findall(r'Avisos\sPremium', html)) :
                print 'Avisos Premium Detectado'
                EscortDataBlocks = html.split('Avisos Premium')[1]
                #print 'EscortDataBlocks: \n-----------------\n', EscortDataBlocks, '\n---------------------------\n\n'
                if len (re.findall(r'width\=\"5\"', EscortDataBlocks)) :
                    print 'Detecta : width=\"5\"'
                    EscortDataBlocks = EscortDataBlocks.split('width=\"5\"')[0]
                    if len (re.findall(r'\<\!\-\-\s\<tr\>', EscortDataBlocks)) :
                        print 'Detecta: <!-- <tr>'
                        EscortDataBlocks = EscortDataBlocks.split('<!-- <tr>')
                        #print '\n-------------------------------\n'.join(EscortDataBlocks)
                        
                        for eachBlock in EscortDataBlocks :
                            if len (re.findall(r'\<i\>', eachBlock)) :
                                nombre = eachBlock.split('<i>')[1].split('</i>')[0]
                                print '---------------------------------------\nInicia Escort Premium Ponelo \nNombre: ', nombre
                                escortURLarea = eachBlock.split('</i>')[1]
                                if len (re.findall(r'clasificados\/detail\.php\?id\=\d+', escortURLarea)) :
                                    escortURL = 'http://ponelo.cl/' + re.findall(r'clasificados\/detail\.php\?id\=\d+', escortURLarea)[0]
                                    print 'Escort URL:', escortURL
                                    enlace = '<a href="' + escortURL + '" target="_blank">' + nombre + '</a>'
                                    anchorLenLista += [len(enlace)]
                                    
                                    # Escort Page Begins...
                                    # Escort Page preps:
                                    htmlfile = urllib.urlopen(escortURL)
                                    EscortPage = htmlfile.read()
                                    EscortPage = EscortPage.replace('&aacute;','á').replace('&eacute;','é').replace('&iacute;','í').replace('&oacute;','ó').replace('&uacute;','ú')
                                    EscortPage = EscortPage.replace('&Aacute;','Á').replace('&Eacute;','É').replace('&Iacute;','Í').replace('&Oacute;','Ó').replace('&Uacute;','Ú')
                                    EscortPage = EscortPage.replace('&ntilde;','ñ').replace('&Ntilde;','Ñ')
                                    
                                    sql = sql + 'INSERT INTO escortssantiago(Escort,Edad,Tarifa,Telefono,Estatura,Busto,Cintura,Culo,Hasta_Dia,Inicio,Termino,Lugar,Servicios,Adicionales) VALUES ('
                                    sql = sql + '\'' + enlace + '\''
                                    
                                    # Age of the Escort:
                                    edad = 'null'
                                    if (len(re.findall(r'size\=\"3\"', EscortPage)) == 2) :
                                        edadArea = EscortPage.split('size=\"3\"')[2].split('</b>')[0]
                                        #print 'Edad Area:.......................\n', edadArea, '\n.............................\n'
                                        if len (re.findall(r'\d\d', edadArea)) :
                                            edad = re.findall(r'\d\d', edadArea)[0]
                                    print 'Edad:', edad
                                    sql = sql + ',' + edad
                                    
                                    # Price of the Escort's Services:
                                    tarifa = 'null'
                                    if len (re.findall(r'Valor\spor\s1\sHora', EscortPage)) :
                                        tarifaArea = EscortPage.split('Valor por 1 Hora')[1].split('</tr>')[0]
                                        if len (re.findall(r'\$\d+\.\d+', tarifaArea)) :
                                            tarifa = re.findall(r'\$(\d+\.\d+)', tarifaArea)[0].replace('.','')
                                    print 'Tarifa:', tarifa
                                    sql = sql + ',' + tarifa
                                    
                                    # Telephone of the Escort:
                                    telefono = 'null'
                                    if len (re.findall(r'Telefono', EscortPage)) :
                                        telefono = EscortPage.split('Telefono')[1].split('</tr>')[0].split('negro2\">')[1].split('</td>')[0]
                                        telefono = telefono.replace('-','')
                                    print 'Telefono:', telefono
                                    sql = sql + ',' + telefono
                                    
                                    # Height of the Escort:
                                    estatura = 'null'
                                    if len (re.findall(r'Estatura', EscortPage)) :
                                        estaturaArea = EscortPage.split('Estatura')[1].split('</td>')[0]
                                        if len (re.findall(r'\d\.\d\d', estaturaArea)) :
                                            estatura = re.findall(r'\d\.\d\d', estaturaArea)[0].replace('.','')
                                    print 'Estatura:', estatura
                                    
                                    
                                    
                                    time.sleep(Decimal(Decimal(randrange(iTime,fTime,sTime)) / Decimal(1000)))

finally :
    # SQL Final Printing:
    
    a01 = 'DROP TABLE escortssantiago;\n'
    a02 = 'CREATE TABLE escortssantiago(\n'
    a03 = '  Escort VARCHAR('+ str(max(anchorLenLista)) + ') NOT NULL PRIMARY KEY\n'
    a04 = ', Edad INTEGER(2)\n'
    a05 = ', Tarifa INTEGER(7)\n'
    a06 = ', Telefono INTEGER(11)\n'
    a07 = ', Estatura INTEGER(3)\n'
    a08 = ', Busto INTEGER(3)\n'
    a09 = ', Cintura INTEGER(2)\n'
    a10 = ', Culo INTEGER(3)\n'
    a11 = ', Hasta_Dia VARCHAR(7)\n'
    a12 = ', Inicio VARCHAR(5)\n'
    a13 = ', Termino VARCHAR(5)\n'
    a14 = ', Lugar VARCHAR(' + str(max(ubicacionLenLista)) + ')\n'
    a15 = ', Servicios VARCHAR(' + str(max(serviciosLenLista)) + ')\n'
    a16 = ', Adicionales VARCHAR(' + str(max(adicionalesLenLista)) + ')\n'
    a17 = ');\n'
    
    print '\n'+a01+a02+a03+a04+a05+a06+a07+a08+a09+a10+a11+a12+a13+a14+a15+a16+a17 + sql
    
