# 12/06/2026	Describir que hace este programa, que parámetros obtiene de que tipo
#		y que tipo de información da y de que tipo
#		
#		He analizado el programa y parece que obtiene la lista de publicaciones
#		de un contacto específico, la url del contacto y de su actividad se
#		pasa directamente, no la busca via pasos web con selenium, por
#		ejemplo la web que tiene de ejemplo es
#		"https://www.linkedin.com/in/fernandodepablomartin/recent-activity/all/"
#		No lo he ejecutado ni comprobado si funciona

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
import undetected_chromedriver as uc
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

# Pandas para manejo de datos
import pandas as pd
load_dotenv()
URL = 'https://www.linkedin.com/'
#usuario = os.getenv('u_infojobs')
usuario = "jose.zuccoli@yahoo.es"
#clave = os.getenv('c_infojobs')
clave = "Pituti#2021"
empleos = ['programador']

# 2026-06-12 cambio use_subprocess=False, por =True, da errores el False
driver = uc.Chrome(headless=False,use_subprocess=True)

# abre la web
driver.get(URL) # ingresa en la direccion de la URL
# intenta encontrar las cookies y aceptar, si no encuentra impime ya tiene las cookies
try:
    #driver.find_element(By.CSS_SELECTOR, '#a').click()
    driver.find_element(By.CLASS_NAME, "artdeco-global-alert-action__wrapper > *:nth-child(1)").click()
    print('Cookies aceptadas')
except Exception as e:
    print(e)
    print('Ya tienes la cookies')

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

time.sleep(10)

#driver.find_element(By.CLASS_NAME, 'global-nav__primary-link').click()
#mired = driver.find_elements_by_xpath("//*[contains(text(), 'Mi red')]").get_attribute("outerHTML")
#mired = driver.find_element(By.XPATH("//span[contains(text(),'Mi red')]")).get_attribute("outerHTML")
#mired2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Mi red')]")))
#mired2 = driver.find_element(by=By.XPATH, value="//span[contains(text(),'Mi red')]")
#mired2 = driver.find_element(by=By.CSS_SELECTOR, value="[title='Mi red']")
#mired = mired2.get_attribute("outerHTML")
driver.find_element(by=By.CSS_SELECTOR, value="[title='Mi red']").click()

urlFernadoDePablo = "https://www.linkedin.com/in/fernandodepablomartin/recent-activity/all/"
driver.get(urlFernadoDePablo)

publics = driver.find_element(By.CLASS_NAME, 'scaffold-finite-scroll__content > *:nth-child(2) > li')

for public in publics:
    texto = driver.find_element(By.CLASS_NAME, 'feed-shared-inline-show-more-text__see-more-less-toggle').click()
    publics.find_element('div > div > *:nth-child(2) > div > div > div > div > *:nth-child(2) > *:nth-child(2) > div > div > span > span::text ')

    print (texto)

input("Press Enter to continue...")

driver.quit()
fechaactual = str(date.today())
with open(f'{fechaactual}red.html', 'a', encoding="utf-8") as f:
    print (type(lista_ofertas))
    for ofertas in lista_ofertas:
        f.write(f'<p>')
        f.write(f'<div><a href="{ofertas['link_oferta']}">INFOJOBS-{ofertas['titulo']}</a>-{ofertas['publicada']}-{ofertas['empresa']}--{ofertas['ubicacion']}</div>')
        f.write(f'</p>')
f.closed
data= pd.DataFrame(lista_ofertas)
data.to_csv('data2_infojobs.csv', index=False)
data.info()
