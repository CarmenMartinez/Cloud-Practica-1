# Cloud-Practica-1

Esta practica esta diseñada para hacer una prueba de almacenamiento con python localmente utilizando `sql lite` y después hacer el almacenamiento en dynamo DB

## loadImages.py 
Este archivo se encarga de cargar las imagenes en la base de datos local con las tablas _labesl_ e _images_
Carga un valor determinado de 400 imagenes, las cuales deben ser parte de depiction

## queryImages.py
Se encarga de consultar las imágenes almacenadas localmente, obtiene la URL de cada imagen que corresponda con el label mandado como parámetro y es mostrado en consola

Ejemplo
`python3 queryImages.py africa`
regresará todas las imágenes que esten relacionadas con africa

## dynamoStorage.py
Contiene una logica similar a LoadImages, la diferencia es que seran cargadas en la base de datos de Dynamo utilizando la documentacion para hacer putItem
getItem y cargar las imagenes
