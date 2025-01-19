import requests 
from bs4 import BeautifulSoup
import pandas as pd
pd.set_option('display.max_columns', None)

def extraer_datos_wikipedia(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    } #esto es siempre igual, lo habilita para levantar como si fuera un navegador, simular que es un agente

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error en la solicitud: {response.status_code}")
        return None
    
    #parsear la información que nos ha venido en el response a html
    parseo_to_html = BeautifulSoup(response.content, "html.parser") #aqui deberiamos tener todo el contenido del html, aquí ya tendríamos la info
    #print(parseo_to_html)

    #coger la información que nos interesa:
    # Manejar contenido principal de forma segura
    contenido_principal = parseo_to_html.find("div", id="mw-content-text")  #el id mw-content-text siempre existe en wikipedia
    if contenido_principal:
        print('contenido principal encontrado')
    else:
        print("no lo encuentro")
    contenido_texto = contenido_principal.getText() if contenido_principal else "Contenido principal no encontrado."

    #hacer el dataframe buscando los elementos dentro del html
    datos = {
        "titulo": parseo_to_html.find("title").getText() if parseo_to_html.find("title") else "Título no encontrado.",
        "enlaces": [a.getText() for a in parseo_to_html.findAll("a")[:10] if a.getText()],
        "imagenes": [img.get("src") for img in parseo_to_html.findAll("img")[:5] if img.get("src")],
        "principal_content": contenido_texto
    }
    return datos

#llamar a la función para extraer los datos de cada provincia
lista_provincias_andaluzas = ['Almería', 'Jaén', 'Granada', 'Málaga', 'Córdoba', 'Sevilla', 'Cádiz', 'Huelva']
diccionario_contenido_sin_espacio_provincias_andaluzas ={}
for provincia in lista_provincias_andaluzas:
    if provincia == 'Córdoba':
        provincia_1 = extraer_datos_wikipedia(f'https://es.wikipedia.org/wiki/Anexo:Municipios_de_la_provincia_de_{provincia}_(España)')
    else:
        provincia_1 = extraer_datos_wikipedia(f'https://es.wikipedia.org/wiki/Anexo:Municipios_de_la_provincia_de_{provincia}')

    if provincia_1:
        #print("Título de la página:", provincia_1["titulo"])
        #print("Primeros 10 enlaces:", datos_provincia["enlaces"])
        #print("Primeras 5 imágenes:", datos_provincia["imagenes"])
        #print(lista_contenido_principal)
        lista_contenido_principal = provincia_1["principal_content"].split('\n')
        
        lista_provincia_sin_espacio = []
        for elemento_lista in lista_contenido_principal:
            if elemento_lista != '':
                lista_provincia_sin_espacio.append(elemento_lista)
            else:
                lista_provincia_sin_espacio=lista_provincia_sin_espacio
        #print(lista_provincia_sin_espacio)

        diccionario_contenido_sin_espacio_provincias_andaluzas[provincia] = lista_provincia_sin_espacio


#print(diccionario_contenido_sin_espacio_provincias_andaluzas)
#print(len(diccionario_contenido_sin_espacio_provincias_andaluzas))

#Creación DataFrame Málaga
datos_Málaga= diccionario_contenido_sin_espacio_provincias_andaluzas['Málaga']
#print(datos_Málaga)
#print(datos_Málaga.index('Municipios desaparecidos de la provincia de Málaga[editar]'))
lista_detalle_Málaga = datos_Málaga[datos_Málaga.index('Escudo')+1:datos_Málaga.index('Municipios desaparecidos de la provincia de Málaga[editar]')]
#print(lista_detalle_Málaga)
#print(len(lista_detalle_Málaga))

lista_municipios_Málaga = lista_detalle_Málaga[0::3]
lista_poblacion_Málaga = lista_detalle_Málaga[1::3]
lista_superficie_Málaga = lista_detalle_Málaga[2::3]

#print(lista_municipios_Málaga)
#print(lista_poblacion_Málaga)
#print(lista_superficie_Málaga)

diccionario_municipio_Málaga = {'Municipio' : lista_municipios_Málaga, 'Población' : lista_poblacion_Málaga, 'Superficie km2' : lista_superficie_Málaga }
#print(diccionario_municipio_Málaga)

tabla_municipio_Málaga = pd.DataFrame(diccionario_municipio_Málaga)
tabla_municipio_Málaga['Provincia'] = 'Málaga'
print('La información de la Provincia de Málaga es la siguiente:')
print(tabla_municipio_Málaga)

#Creación DataFrame Almería
datos_Almería= diccionario_contenido_sin_espacio_provincias_andaluzas['Almería']
#print(datos_Almería)
lista_detalle_Almería = datos_Almería[datos_Almería.index('Población[1]\u200b (2023)')+1:datos_Almería.index('Referencias[editar]')]
#print(lista_detalle_Almería)
#print(len(lista_detalle_Almería))

lista_municipios_Almería = lista_detalle_Almería[0::2]
lista_poblacion_Almería = lista_detalle_Almería[1::2]
#lista_superficie = lista_detalle_Málaga[2::3]

#print(lista_municipios_Almería)
#print(lista_poblacion_Almería)
#print(lista_superficie)

diccionario_municipio_Almería = {'Municipio' : lista_municipios_Almería, 'Población' : lista_poblacion_Almería, 'Superficie km2' : None}
#print(diccionario_municipio_Almería)

tabla_municipio_Almería = pd.DataFrame(diccionario_municipio_Almería)
tabla_municipio_Almería['Provincia'] = 'Almería'
print('La información de la Provincia de Almeria es la siguiente:')
print(tabla_municipio_Almería)

#Creación DataFrame Jaén
datos_Jaén= diccionario_contenido_sin_espacio_provincias_andaluzas['Jaén']
#print(datos_Jaén)
lista_detalle_Jaén = datos_Jaén[datos_Jaén.index('Bandera')+1:datos_Jaén.index('Notas[editar]')]
#print(lista_detalle_Jaén)
#print(len(lista_detalle_Jaén))

lista_municipios_Jaén = lista_detalle_Jaén[0::6]
lista_poblacion_Jaén = lista_detalle_Jaén[2::6]
lista_superficie_Jaén = lista_detalle_Jaén[1::6]

#print(lista_municipios_Jaén)
#print(lista_poblacion_Jaén)
#print(lista_superficie_Jaén)

diccionario_municipio_Jaén = {'Municipio' : lista_municipios_Jaén, 'Población' : lista_poblacion_Jaén, 'Superficie km2' : lista_superficie_Jaén }
#print(diccionario_municipio_Jaén)

tabla_municipio_Jaén = pd.DataFrame(diccionario_municipio_Jaén)
tabla_municipio_Jaén['Provincia'] = 'Jaén'
print('La información de la Provincia de Jaén es la siguiente:')
print(tabla_municipio_Jaén)

#Creación DataFrame Granada
datos_Granada= diccionario_contenido_sin_espacio_provincias_andaluzas['Granada']
#print(datos_Granada)
lista_detalle_Granada = datos_Granada[datos_Granada.index('Población (2022)[1]\u200b')+1:datos_Granada.index('Véase también[editar]')]
#print(lista_detalle_Granada)
#print(len(lista_detalle_Granada))

lista_municipios_Granada = lista_detalle_Granada[0::2]
lista_poblacion_Granada = lista_detalle_Granada[1::2]
#lista_superficie_Granada = lista_detalle_Granada[2::3]

#print(lista_municipios_Granada)
#print(lista_poblacion_Granada)
#print(lista_superficie_Granada)

diccionario_municipio_Granada = {'Municipio' : lista_municipios_Granada, 'Población' : lista_poblacion_Granada, 'Superficie km2' : None}
#print(diccionario_municipio_Almería)

tabla_municipio_Granada = pd.DataFrame(diccionario_municipio_Granada)
tabla_municipio_Granada['Provincia'] = 'Granada'
print('La información de la Provincia de Granada es la siguiente:')
print(tabla_municipio_Granada)


#Creación DataFrame Córdoba
datos_Córdoba= diccionario_contenido_sin_espacio_provincias_andaluzas['Córdoba']
#print(datos_Córdoba)
lista_detalle_Córdoba = datos_Córdoba[datos_Córdoba.index('Pob. (2018)[2]\u200b')+1:datos_Córdoba.index('Despoblación en la provincia de Córdoba[editar]')]
#print(lista_detalle_Córdoba)
#print(len(lista_detalle_Córdoba))

lista_municipios_Córdoba = lista_detalle_Córdoba[0::5]
lista_poblacion_Córdoba = lista_detalle_Córdoba[1::5]
#lista_superficie_Córdoba = lista_detalle_Córdoba[1::6]

#print(lista_poblacion_Córdoba)
#print(lista_poblacion_Córdoba)
#print(lista_superficie_Córdoba)

diccionario_municipio_Córdoba = {'Municipio' : lista_municipios_Córdoba, 'Población' : lista_poblacion_Córdoba, 'Superficie km2' : None }
#print(diccionario_municipio_Jaén)

tabla_municipio_Córdoba = pd.DataFrame(diccionario_municipio_Córdoba)
tabla_municipio_Córdoba['Provincia'] = 'Córdoba'
print('La información de la Provincia de Córdoba es la siguiente:')
print(tabla_municipio_Córdoba)


#Creación DataFrame Sevilla
datos_Sevilla= diccionario_contenido_sin_espacio_provincias_andaluzas['Sevilla']
#print(datos_Sevilla)
lista_detalle_Sevilla_1= datos_Sevilla[datos_Sevilla.index('Pob.(2017)')+1:datos_Sevilla.index('Palmar de Troya, El')]+datos_Sevilla[datos_Sevilla.index('33,02')+1:datos_Sevilla.index('Total')]
#print(lista_detalle_Sevilla_1)
#print(len(lista_detalle_Sevilla_1))

lista_municipios_Sevilla_1 = lista_detalle_Sevilla_1[0::10]
lista_poblacion_Sevilla_1 = lista_detalle_Sevilla_1[1::10]
lista_superficie_Sevilla_1 = lista_detalle_Sevilla_1[2::10]

#print(lista_municipios_Sevilla_1)
#print(lista_poblacion_Sevilla_1)
#print(lista_superficie_Sevilla_1)

lista_detalle_Sevilla_2= datos_Sevilla[datos_Sevilla.index('Palmar de Troya, El'):datos_Sevilla.index('33,02')+1]
#print(lista_detalle_Sevilla_1)
#print(len(lista_detalle_Sevilla_1))

lista_municipios_Sevilla_2 = lista_detalle_Sevilla_2[0::3]
lista_poblacion_Sevilla_2 = lista_detalle_Sevilla_2[1::3]
lista_superficie_Sevilla_2 = lista_detalle_Sevilla_2[2::3]

#print(lista_municipios_Sevilla_2)
#print(lista_poblacion_Sevilla_2)
#print(lista_superficie_Sevilla_2)

diccionario_municipio_Sevilla = {'Municipio' : lista_municipios_Sevilla_1+lista_municipios_Sevilla_2, 'Población' : lista_poblacion_Sevilla_1+lista_poblacion_Sevilla_2, 'Superficie km2' : lista_superficie_Sevilla_1+lista_superficie_Sevilla_2 }
#print(diccionario_municipio_Sevilla)

tabla_municipio_Sevilla = pd.DataFrame(diccionario_municipio_Sevilla)
tabla_municipio_Sevilla['Provincia'] = 'Sevilla'
print('La información de la Provincia de Sevilla es la siguiente:')
print(tabla_municipio_Sevilla)


#Creación DataFrame Cádiz
datos_Cádiz= diccionario_contenido_sin_espacio_provincias_andaluzas['Cádiz']
#print(datos_Cádiz)
lista_detalle_Cádiz = datos_Cádiz[datos_Cádiz.index('Escudo')+1:datos_Cádiz.index('Véase también[editar]')]
#print(lista_detalle_Cádiz)
#print(len(lista_detalle_Cádiz))

lista_municipios_Cádiz = lista_detalle_Cádiz[0::3]
lista_poblacion_Cádiz = lista_detalle_Cádiz[1::3]
lista_superficie_Cádiz= lista_detalle_Cádiz[2::3]

#print(lista_municipios_Cádiz)
#print(lista_poblacion_Cádiz)
#print(lista_superficie_Cádiz)

diccionario_municipio_Cádiz = {'Municipio' : lista_municipios_Cádiz, 'Población' : lista_poblacion_Cádiz, 'Superficie km2' : lista_superficie_Cádiz }
#print(diccionario_municipio_Cádiz)

tabla_municipio_Cádiz = pd.DataFrame(diccionario_municipio_Cádiz)
tabla_municipio_Cádiz['Provincia'] = 'Cádiz'
print('La información de la Provincia de Cádiz es la siguiente:')
print(tabla_municipio_Cádiz)



#Creación DataFrame Huelva
datos_Huelva= diccionario_contenido_sin_espacio_provincias_andaluzas['Huelva']
#print(datos_Huelva)
lista_detalle_Huelva = datos_Huelva[datos_Huelva.index('Escudo')+1:datos_Huelva.index('Véase también[editar]')]
#print(lista_detalle_Huelva)
#print(len(lista_detalle_Huelva))

lista_municipios_Huelva= lista_detalle_Huelva[0::3]
lista_poblacion_Huelva = lista_detalle_Huelva[1::3]
lista_superficie_Huelva= lista_detalle_Huelva[2::3]

#print(lista_municipios_Huelva)
#print(lista_poblacion_Huelva)
#print(lista_superficie_Huelva)

diccionario_municipio_Huelva = {'Municipio' : lista_municipios_Huelva, 'Población' : lista_poblacion_Huelva, 'Superficie km2' : lista_superficie_Huelva }
#print(diccionario_municipio_Huelva)

tabla_municipio_Huelva = pd.DataFrame(diccionario_municipio_Huelva)
tabla_municipio_Huelva['Provincia'] = 'Huelva'
print('La información de la Provincia de Huelva es la siguiente:')
print(tabla_municipio_Huelva)


#agrupación de todos los DF de las provincias
tabla_total_municipios_andaluces = pd.concat([tabla_municipio_Huelva, tabla_municipio_Almería, tabla_municipio_Cádiz, tabla_municipio_Córdoba, tabla_municipio_Granada, tabla_municipio_Jaén, tabla_municipio_Málaga, tabla_municipio_Sevilla], axis=0)
print(tabla_total_municipios_andaluces)

#print((tabla_total_municipios_andaluces.info()))

#conversión del tipo de dato de las columnas al correcto
tabla_total_municipios_andaluces['Superficie km2'] = tabla_total_municipios_andaluces['Superficie km2'].str.replace(',', '.').astype(float)

print(tabla_total_municipios_andaluces[tabla_total_municipios_andaluces['Población']=='21\xa0581'])

tabla_total_municipios_andaluces['Población'] = tabla_total_municipios_andaluces['Población'].str.replace('\xa0', '')
tabla_total_municipios_andaluces['Población'] = tabla_total_municipios_andaluces['Población'].str.replace(' ', '').astype(float)

#print((tabla_total_municipios_andaluces.info()))

#creación DF agrupado para creación de bignumbers:
df_big_numbers = pd.DataFrame()

df_big_numbers['Total_municipios_provincia']= tabla_total_municipios_andaluces['Provincia'].value_counts()
df_big_numbers['Población_total'] =tabla_total_municipios_andaluces.groupby('Provincia')['Población'].sum()
df_big_numbers['Media_Población_municipio'] =tabla_total_municipios_andaluces.groupby('Provincia')['Población'].mean().round(2)
df_big_numbers['Superficie_total_km2'] = tabla_total_municipios_andaluces.groupby('Provincia')['Superficie km2'].sum()
df_big_numbers['Media_Superficie_km2_municipio'] = tabla_total_municipios_andaluces.groupby('Provincia')['Superficie km2'].mean().round(2)
df_big_numbers['hab/km2'] =df_big_numbers['Población_total']/df_big_numbers['Superficie_total_km2']
print('De modo agregado, podemos obtener los siguientes big numbers')
print(df_big_numbers)

print(f'El municipio con más habitantes es \n {tabla_total_municipios_andaluces.sort_values('Población', ascending=False).head(1).reset_index()}')
print(f'El municipio con menos habitantes \n {tabla_total_municipios_andaluces.sort_values('Población', ascending=True).head(1).reset_index()}')

print(f'El municipio con más km2 de superficie es \n {tabla_total_municipios_andaluces.sort_values('Superficie km2', ascending=False).head(1).reset_index()}')
print(f'El municipio con menos km2 de superficie es \n {tabla_total_municipios_andaluces.sort_values('Superficie km2', ascending=True).head(1).reset_index()}')

