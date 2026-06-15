# 12/06/2026	Describir que hace este programa, que parámetros obtiene de que tipo
#		y que tipo de información da y de que tipo
#		
#		Obtenemos información de 1 empleo de Linkedin,
#		pasamos la web en un archivo 2026-06-15listaEmpleos.txt
#               con 1 url por línea. Se leen y se guardan en varios archivos json
#               1 archivo json por empleo
#
#               Por ejempleo una web sería
#		https://www.linkedin.com/jobs/view/4411194255/?eBP=CwEAAAGesYMZ-sySkH2Gk3Vkbyj4MRqyhiEpH-UO3uDrPoW8rSLoxonVZ-0ayxHy4s5_n1m5t614HryxBHchpT48OriMLLFMoc9anCaV8dHxMXx-5S_RwsyWbVGRqX3mLHcibNZBzWl6ph59bh0QW3w_WA-q31WWZy1RhwiiL-QImLABVWL0SKRrOwPzxNNl9STsqtKFHy7u-emRcs3W3xxZINj2VW2zK3aiQhf-VbfSBcH1rZ1jNvH9b42o01hUlDaKWwNprlk3jnIja2ULP6StT0hAZLpbYkGrFkg6ekG0MZ9FdbhW0xNEYv0HyGM0Z4y7itE_KOBZqo8kQZGfMCKaUIKLZDltR4qNUC0aFoFaX8_gntsOEYfppgBRehaP9XdaYgiOjqKsZvGetR1VzIo1XV9s6hgtmPXoilCumwotfKQHApV1AcL8000UwtNtHGj6MZVIuFUVVm6cWVsVn-kovag5ef9GJ7h9BBqpNf_-FfimTQ&trk=flagship3_search_srp_jobs&refId=ffPcEjIy85l4abAnOH77Dg%3D%3D&trackingId=gyX3zz66CgffFbPJeHvlRA%3D%3D
#		que en 12/06/2026 tiene la siguiente información que queremos obtener:
#
#		Ayesa Digital
#		Ingeniero/a de Ciberseguridad L2 
#		Guipúzcoa, País Vasco / Euskadi, España
#		Personas con las que puedes hablar. Conoce al equipo de contratación
#		Gema B. - 3er
#		Talent Acquisition Specialist en Ayesa Digital
#		Acerca del empleo
#		¿Qué vas a hacer?
#
#		Atender los escalados de nivel 1 (L1) dentro de los servicios del SOC.
#		Formar y dotar al equipo L1 de las herramientas y conocimientos necesarios para mejorar su eficacia.
#		¿Qué buscamos?
#
#		Experiencia previa como analista de ciberseguridad, ingeniero/a de seguridad o SOC L2.
#		Conocimientos en SIEM (QRadar, Splunk, Microsoft Sentinel u otros).
#
#               Guardamos titulo del Empleo, Hace cuanto tiempo se publicó ( por ejemplo Hace 1 mes )
#               y el texto del Empleo con nueva lineas,
#               Lo guardamos en un archivo .json tipo 2026-06-15-17-29-00nombreEmpleo.json
#               con el siguiente formato:
#               {
#                 "tituloEmpleo": "Programador",
#                 "tiempoPublicacion": "Hace 1 mes",
#                 "textoEmpleo": "Programador Informático"
#               }

# Módulos de Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import selenium.webdriver.common.keys as Keys
from datetime import date

#empproj08_03: grabo con formato json para mezclar ofertas con el resto
#               formato reducido en 1 linea

# Otros módulos

# 2026-06-12-11-19-00 desinstale undetected_webdriver por problemas de versión con Selenium
#import undetected_chromedriver as uc

import os
from dotenv import load_dotenv
import time
import random
from bs4 import BeautifulSoup as bs
import requests as req
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from zenrows import ZenRowsClient
from datetime import datetime
import json
import re
import sys

# nos autenticamos en linkedin y una vez allí vamos a la url

# Pandas para manejo de datos
import pandas as pd
load_dotenv()
URL = 'https://www.linkedin.com/'
#usuario = os.getenv('u_infojobs')
usuario = "jose.zuccoli@yahoo.es"
#clave = os.getenv('c_infojobs')
clave = "Pituti#2021"

# 2026-06-12-11-17-00 cambios por error de versiones entre selenium y undetected_webdriver
# driver = uc.Chrome(headless=False,use_subprocess=True)
driver = webdriver.Chrome()

# abre la web
driver.get(URL) # ingresa en la direccion de la URL

# intenta encontrar las cookies y aceptar, si no encuentra impime ya tiene las cookies
try:
    driver.find_element(By.CLASS_NAME, "artdeco-global-alert-action__wrapper > *:nth-child(1)").click()
    print('Cookies aceptadas')
except Exception as e:
    print(e)
    print('Ya tienes la cookies')

print('Esperamos......')
time.sleep(5)

#hacer click en acceso a candidatos
driver.find_element(By.CLASS_NAME, 'sign-in-form__sign-in-cta').click()

# Esperar hasta que el boton exista o sea clickable
cuadro_usuario= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#username')))
# ingresar letra a letra usuario y clave
for letra in usuario:
    cuadro_usuario.send_keys(letra)
    time.sleep(random.uniform(0.3,0.75))
cuadro_clave= driver.find_element(By.CSS_SELECTOR, '#password')
for num in clave:
    cuadro_clave.send_keys(num)
    time.sleep(random.uniform(0.3,0.75))
cuadro_usuario.submit()
lista_ofertas= []

# Por si intenta enviar un codigo por correo
# debemos esperar recibirlo y ponerlo, por
# ello esperamos 100 segundos
print('Esperamos 5 segundos recibir código por correo......')
time.sleep(5)

# Despues de verificar con código de correo electrónico
# Volvemos a aceptar cookies
cookiesAceptar = driver.find_element(By.XPATH, "//button[@data-testid='global-alerts-actions-0']/span/span")

print ("Vemos si es Aceptar: ",cookiesAceptar.text)

# El elemento no se puede hacer click con click()
driver.execute_script("arguments[0].click();", cookiesAceptar )
time.sleep(5)
print ("Click en Aceptar para cookies por 2da vez...")

# leo url de 2026-06-15listaEmpleos.txt , 1 línea por URL
# buscamos la web de empleo por defecto
# urlEmpleo = "https://www.linkedin.com/jobs/view/4411194255/?eBP=CwEAAAGesYMZ-sySkH2Gk3Vkbyj4MRqyhiEpH-UO3uDrPoW8rSLoxonVZ-0ayxHy4s5_n1m5t614HryxBHchpT48OriMLLFMoc9anCaV8dHxMXx-5S_RwsyWbVGRqX3mLHcibNZBzWl6ph59bh0QW3w_WA-q31WWZy1RhwiiL-QImLABVWL0SKRrOwPzxNNl9STsqtKFHy7u-emRcs3W3xxZINj2VW2zK3aiQhf-VbfSBcH1rZ1jNvH9b42o01hUlDaKWwNprlk3jnIja2ULP6StT0hAZLpbYkGrFkg6ekG0MZ9FdbhW0xNEYv0HyGM0Z4y7itE_KOBZqo8kQZGfMCKaUIKLZDltR4qNUC0aFoFaX8_gntsOEYfppgBRehaP9XdaYgiOjqKsZvGetR1VzIo1XV9s6hgtmPXoilCumwotfKQHApV1AcL8000UwtNtHGj6MZVIuFUVVm6cWVsVn-kovag5ef9GJ7h9BBqpNf_-FfimTQ&trk=flagship3_search_srp_jobs&refId=ffPcEjIy85l4abAnOH77Dg%3D%3D&trackingId=gyX3zz66CgffFbPJeHvlRA%3D%3D"
hoy = datetime.today().strftime("%Y-%m-%d")

# Existe el archivo?
if not (os.path.exists(f"{hoy}textoEmpleos.txt")):
    driver.quit()
    sys.exit (f"No existe {hoy}textoEmpleos.txt")

file = open (f"{hoy}textoEmpleos.txt", "r")
for line in file:
    urlEmpleo = line.strip()

    driver.get(urlEmpleo)
    time.sleep(5)

    titulo = driver.find_element(By.XPATH, "//section[@aria-label='Contenido principal']/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/p").text

    titulo = titulo.strip()
    print ("titulo", titulo)

    nombreArchivo = titulo
    nombreArchivo = nombreArchivo.strip()
    nombreArchivo = ''.join(word.capitalize() for word in nombreArchivo.split())
    nombreArchivo = re.sub(r'[^a-zA-Z0-9]', '', nombreArchivo)
    nombreArchivo = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + nombreArchivo + ".json"

    tiempoPublicacion = driver.find_element(By.XPATH, "//section[@aria-label='Contenido principal']/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/p/span[4]").get_attribute('innerHTML')[:50]
    print ("tiempoPublicacion", tiempoPublicacion)

    textoEmpleo = driver.find_element(By.XPATH, "//div[@data-sdui-component='com.linkedin.sdui.generated.jobseeker.dsl.impl.aboutTheJob']/div[1]/div[1]/div[1]/div[1]/p[1]/span[1]").get_attribute('outerHTML')

    # Para que beautifullsoup coga las lineas nuevas \n, debemos reemplazar
    # <p> </p> con "\n" y asimismo <br> con "\n"
    # Asi tendremos un texto con nuevas lineas

    soup = bs(textoEmpleo, 'html.parser')  # 👉️ Parsing
    el = soup.find("span") # 👉️ Find <div> TAG
    textoEmpleo2 = el.get_text() # 👉️ Get text of the <div>

    textoEmpleo = textoEmpleo.replace("\n", "\\n")
    jsontext = json.loads('{ \"tituloEmpleo\": \"' + titulo + '\", \"tiempoPublicacion\": \"' + tiempoPublicacion.strip()  + '\", \"textoEmpleo\": \"' + textoEmpleo2  + '\" }')

    # Pulsar sobre 
    botonMasEmpleo = driver.find_element(By.XPATH, "//div[@data-sdui-component='com.linkedin.sdui.generated.jobseeker.dsl.impl.aboutTheJob']/div[1]/div[1]/div[1]/div[1]/p[1]/span[1]/button/span/span/span[2]")
    #  span/button/span/span/span[2] texto " más"

    driver.execute_script("arguments[0].click();", botonMasEmpleo )
    time.sleep(5)
    #print ("Click en Aceptar para cookies por 2da vez...")

    textoEmpleo = driver.find_element(By.XPATH, "//div[@data-sdui-component='com.linkedin.sdui.generated.jobseeker.dsl.impl.aboutTheJob']/div[1]/div[1]/div[1]/div[1]/p[1]/span[1]").get_attribute('outerHTML')

    soup = bs(textoEmpleo, 'html.parser')  # 👉️ Parsing
    el = soup.find("span") # 👉️ Find <div> TAG
    textoEmpleo2 = el.get_text() # 👉️ Get text of the <div>

    print ("texto Empleo2\n", textoEmpleo2)

    #driver.quit()

    print (f"Escribimos en archivo {nombreArchivo}....")
    json_str = json.dumps(jsontext, indent = 4)
    with open(f'{nombreArchivo}', 'w') as f:
        f.write(json_str)
    f.closed

file.close()
