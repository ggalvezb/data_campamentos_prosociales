import pandas as pd
import geopandas as gpd
import numpy as np
from scipy.spatial import cKDTree
from shapely.geometry import Point
import statistics as st


proyectos_sociales=gpd.read_file("C:\\Users\\ggalv\\OneDrive\\Proyectos_Programacion\\geodatos_campamentos\\shapes\\Catastro_Condominios_Sociales\\Catastro_de_Condominios_Sociales_centroides_repro.shp")
establecimientos_educa=gpd.read_file("C:\\Users\\ggalv\\OneDrive\\Proyectos_Programacion\\geodatos_campamentos\\shapes\\establecimientos_edescolar_abr2020\\Establecimientos_EdEscolar_Abr2020.shp")
cuarteles_carabineros=gpd.read_file("C:\\Users\\ggalv\\OneDrive\\Proyectos_Programacion\\geodatos_campamentos\\shapes\\Cuarteles_Carabineros\\CUARTELES.shp")
cuarteles_bomberos=gpd.read_file("C:\\Users\\ggalv\\OneDrive\\Proyectos_Programacion\\geodatos_campamentos\\shapes\\Cuerpos-de-Bomberos\\CUERPOS_DECHILE_repro.shp")
hopitales=gpd.read_file("C:\\Users\\ggalv\\OneDrive\\Proyectos_Programacion\\geodatos_campamentos\\shapes\\Hospitales\\HOSPITALES_SNSS_24102018.shp")
universidades=gpd.read_file("C:\\Users\\ggalv\\OneDrive\\Proyectos_Programacion\\geodatos_campamentos\\shapes\\Instituciones_EdSuperior_Oct2019\\Instituciones_EdSuperior_Oct2019.shp")
jardines_junji=gpd.read_file("C:\\Users\\ggalv\\OneDrive\\Proyectos_Programacion\\geodatos_campamentos\\shapes\\jardines_junji\\JJII_JUNJI_09_2018.shp")

def ckdnearest(gdA, gdB,i):
    nA = np.array(list(gdA.geometry.apply(lambda x: (x.x, x.y))))
    nB = np.array(list(gdB.geometry.apply(lambda x: (x.x, x.y))))
    btree = cKDTree(nB)
    dist, idx = btree.query(nA, k=1)
    if i ==0:
        gdf = pd.concat(
            [gdA.reset_index(drop=True), gdB.loc[idx, gdB.columns == 'NOM_RBD'].reset_index(drop=True),
            pd.Series(dist, name='dist_escuela')], axis=1)
    if i ==1:
        gdf = pd.concat(
            [gdA.reset_index(drop=True), gdB.loc[idx, gdB.columns == 'NOMBRE_DE'].reset_index(drop=True),
            pd.Series(dist, name='dist_comisaria')], axis=1)
    if i ==2:
        gdf = pd.concat(
            [gdA.reset_index(drop=True), gdB.loc[idx, gdB.columns == 'NOMBRE'].reset_index(drop=True),
            pd.Series(dist, name='dist_bomberos')], axis=1)
    if i ==3:
        gdf = pd.concat(
            [gdA.reset_index(drop=True), gdB.loc[idx, gdB.columns == 'SERVIC_SAL'].reset_index(drop=True),
            pd.Series(dist, name='dist_hospital')], axis=1)
    if i ==4:
        gdf = pd.concat(
            [gdA.reset_index(drop=True), gdB.loc[idx, gdB.columns == 'NOMBRE_INS'].reset_index(drop=True),
            pd.Series(dist, name='dist_universidad')], axis=1)
    if i ==5:
        gdf = pd.concat(
            [gdA.reset_index(drop=True), gdB.loc[idx, gdB.columns == 'NOMBRE'].reset_index(drop=True),
            pd.Series(dist, name='dist_jardin')], axis=1)
    return gdf

i=0
for i in range(6):
    if i==0:
        test=ckdnearest(proyectos_sociales, establecimientos_educa,i)
        test["dist_escuela"] = 100000 * test["dist_escuela"]
        test=test.rename(columns={'NOM_RBD': 'Nombre_escuela'})
    if i==1:
        test=ckdnearest(test, cuarteles_carabineros,i)
        test["dist_comisaria"] = 100000 * test["dist_comisaria"]
        test=test.rename(columns={'NOMBRE_DE': 'Nombre_comisaria'})
    if i==2:
        test=ckdnearest(test, cuarteles_bomberos,i)
        test["dist_bomberos"] = 100000 * test["dist_bomberos"]
        test=test.rename(columns={'NOMBRE': 'Nombre_bomberos'})
    if i==3:
        test=ckdnearest(test, hopitales,i)
        test["dist_hospital"] = 100000 * test["dist_hospital"]
        test=test.rename(columns={'SERVIC_SAL': 'Nombre_hospital'})
    if i==4:
        test=ckdnearest(test, universidades,i)
        test["dist_universidad"] = 100000 * test["dist_universidad"]
        test=test.rename(columns={'NOMBRE_INS': 'Nombre_universidad'})
    if i==5:
        test=ckdnearest(test, jardines_junji,i)
        test["dist_jardin"] = 100000 * test["dist_jardin"]
        test=test.rename(columns={'NOMBRE': 'Nombre_jardin'})

test.to_csv('C:\\Users\\ggalv\\OneDrive\\Proyectos_Programacion\\geodatos_campamentos\\proyectos_sociales.csv')



