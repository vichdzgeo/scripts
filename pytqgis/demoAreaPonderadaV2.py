from qgis.analysis import * 
from os.path import join
from PyQt4.QtCore import *
from os.path import join
from datetime import datetime, date, time, timedelta
import calendar
from os import listdir
import os

def contarch():
    path = "C:/swat/demo/PET/1950"
    cont = 0
    for root, dirs, files in os.walk(path):
        for name in files:
            extension = os.path.splitext(name)
            if extension[1] == '.tif':
                cont=cont + 1
    return cont

##**** Archivos de origen *****##
bandas = QgsVectorLayer("C:/swat/demo/origen/swat_EB_insct.shp","bandas","ogr")
bandaspixel=QgsVectorLayer("C:/swat/demo/origen/swat_EB_insct_id_pixe_area.shp","bandaspixel","ogr")
crs=bandas.crs()
##**************************##

##Copiar vectores en carpetas
clon_bandas = QgsVectorFileWriter.writeAsVectorFormat(bandas,"C:/swat/demo/PET/1950/swat_EB_insct_1950.shp",'utf-8',crs,"ESRI Shapefile")
clon_bandaspixel = QgsVectorFileWriter.writeAsVectorFormat(bandaspixel,"C:/swat/demo/PET/1950/swat_EB_insct_id_pixe_area_1950.shp",'utf-8',crs,"ESRI Shapefile")
####

max = contarch()
min = 0
fecha=date(1950,01,01)

bandaspixel = QgsVectorLayer("C:/swat/demo/PET/1950/swat_EB_insct_id_pixe_area_1950.shp","bandaspixel","ogr")
while min < max:
        fecha_a=fecha +timedelta(days=min)
        fe=fecha_a.strftime("%Y%m%d")
        p_folder="C:/swat/demo/PET/1950/PET_%s_Liv_06_UTM.tif"%fe
        zoneStat= QgsZonalStatistics(bandaspixel,p_folder,fe,1,QgsZonalStatistics.Mean)
        zoneStat.calculateStatistics(None)
        print p_folder
        min= min+1
        
print "finalizo el proceso"
## integrando las areas ponderadas al shape de bandas

bandas_year = QgsVectorLayer("C:/swat/demo/PET/1950/swat_EB_insct_1950.shp","bandas","ogr")
bandas_id="id_uni"
bandaspixel_id="id_uni"
#resamplingFields="PET"
max2 = contarch()
min2 = 0
fecha2=date(1950,01,01)

print "creando campos en shape de bandas"
while min2 < max2:
        fecha_a2=fecha2 +timedelta(days=min2)
        fec=fecha_a2.strftime("%Y%m%d")
        bandas_year.dataProvider().addAttributes([QgsField(fec,QVariant.Double)])
        
        min2= min2+1
        
print "finalizo el proceso de creacion de campos"

##***Asignacion de areas****##

bandas_year.startEditing()
    
for poligono in bandas_year.getFeatures():
    print("procesando el poligono",poligono[bandas_id],":")
    max3=contarch()
    min3=0
    bandas_id="id_uni"
    bandaspixel_id="id_uni"
    fecha3=date(1950,01,01)
    while min3 < max3:
        fecha_cont=fecha3 +timedelta(days=min3)
        fe_txt=fecha_cont.strftime("%Y%m%d")
        precip =fe_txt+"me"
        areap=0.0
        for bpix in bandaspixel.getFeatures():
            if(int(bpix[bandaspixel_id])==int(poligono[bandas_id])):
                areap+=((bpix["area_pix"]/bpix["inst_a"])*float(bpix[precip]))
            poligono[fe_txt]=areap
            bandas_year.updateFeature(poligono)
        min3= min3+1    
    bandas_year.commitChanges()
    

print "finalizo el proceso"

#bandas.startEditing()
#for poligono in bandas.getFeatures():
#    
#    print ("procesando el poligono", poligono[bandas_id], ":")
#    new_field_value = 0.0
#    for bit in bandaspixel.getFeatures():
#        if (int(bit[bandaspixel_id]) == int(poligono[bandas_id])):
#            new_field_value += ((bit["area_pix"]/bit["inst_a"])*float(bit["precmean"]))                
#        poligono["PET"] = new_field_value
#        bandas.updateFeature(poligono)
#        
#    
#bandas.commitChanges()