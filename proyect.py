import requests
import time
from bs4 import BeautifulSoup

#Recurso web con los datos a usar
resource_url = ''

# Petición para descargar el fichero de Internet
response = requests.get(resource_url, time.sleep(10))

# Si la petición se ha ejecutado correctamente (código 200), entonces el contenido HTML de la página se ha podido descargar
if response:
    # Transformamos el HTML plano en un HTML real (estructurado y anidado, con forma de árbol)
    soup = BeautifulSoup(response.text, 'html')
    soup