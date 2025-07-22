import requests
from bs4 import BeautifulSoup as bs
import re
import matplotlib.pyplot as plt

def scrapper(url,componentes,producto):
    partes=producto.split()
    pagina=requests.get(url).content
    html=bs(pagina,'html.parser')
    articulos=html.find_all("li",class_=componentes[0])    
    try:
        resultados=[]
        for i in articulos:
            try:
                nombre=i.find("h2",class_=componentes[2]).get_text().lower()
                if re.search(partes[1],nombre):
                    link=i.find("a",class_=componentes[1]).get("href")
                    precio=((str(i.find("span",class_=componentes[3]).get_text()).replace(".","")).replace("$",""))
                    if "," in precio:
                        precio=int(precio.replace(",",""))//100
                    else:
                        precio=int(precio)
                    resultados.append([link,nombre,precio])

                
            except Exception as e:
                print(e)
        
        resultados=ordenar(resultados)    
        return resultados[0][1],resultados[0][2]
        
    except Exception:
        return "the product hasn't been found"

def ordenar(resultados):
    desordenada=True
    while desordenada:
        desordenada=False
        for i in range(0,len(resultados)-1):
            if resultados[i][2]>resultados[i+1][2]:
                aux=resultados[i]
                resultados[i]=resultados[i+1]
                resultados[i+1]=aux
                desordenada=True
    
    return resultados

producto=input("what smartphone do you want to search: ")#li , a , h2, span
urls={f"https://listado.mercadolibre.com.ar/{producto}#":["ui-search-layout__item shops__layout-item","poly-component__title","poly-box","andes-money-amount__fraction"]
      ,f"https://tiendaonline.movistar.com.ar/catalogsearch/result/?q={producto}":["item product product-item","product-link","name","price"]
      ,f"https://tienda.tuenti.com.ar/catalogsearch/result/?q={producto}":["item product product-item","product-link","name","price"]}
""",f"https://www.oscarbarbieri.com/catalogsearch/result/?q={producto}":"a"}"""

lista_productos=[]
lista_precios=[]
for i in urls:
    rf=scrapper(i,urls[i],producto)
    lista_productos.append(rf[0])
    lista_precios.append(rf[1])


print(lista_precios)
# Crear un gráfico de barras
plt.bar(lista_productos, lista_precios)
plt.xlabel('productos')
plt.ylabel('precios')
plt.title('Gráfico de Barras')
plt.show()

