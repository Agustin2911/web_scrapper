import requests
from bs4 import BeautifulSoup as bs

def ordenamiento(lista):
    desordenada=True
    while desordenada:
        desordenada=False
        for i in range(0,len(lista)-1):
            if lista[i][1]>lista[i+1][1]:
                
                aux=lista[i]
                lista[i]=lista[i+1]
                lista[i+1]=aux
                desordenada=True
    return lista

producto=input("ingrese el producto que desea buscar: ")
url=f"https://listado.mercadolibre.com.ar/{producto}"
contenido=requests.get(url).text
datos=bs(contenido,'html.parser')
listado=datos.find_all("li",class_='ui-search-layout__item')

precios=[]
for i in listado:
    precio=i.find("span",class_="andes-money-amount__fraction")
    nombre=i.find("h2",class_="ui-search-item__title")
    link=i.find("a",class_="ui-search-item__group__element ui-search-link__title-card ui-search-link")
    if nombre and precio and link:
        precio_sin_coma=str(precio.get_text(strip=True)).replace(".","")
        print(precio_sin_coma)
        precio=int(precio_sin_coma)
    
        precios.append([nombre.get_text(strip=True),precio,link.get("href")])

precios=ordenamiento(precios)
print(precios)
if not precios:
    print("la busqueda a salido mal , pruebe devuelta")
else:
    for i in precios:
        print(f"producto: {i[0]} precio: {i[1]} el link es: {i[2]}")
        print()

