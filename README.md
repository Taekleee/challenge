# Challenge


## Tecnologías utilizadas y justificación
- Lenguaje: Python
- Framework: Flask. Se decide implementar debido a que es una de las tecnologías utilizadas por la empresa.
- Base de datos: Mysql. Esta base de datos permite manejar de buena manera los datos espaciales, tales como las coordenadas de origen y destino descritas en el enunciado. Además, es de tipo SQL, tal como se solicita en el enunciado. La base de datos se encuentra dentro de un docker para la implementación.


<hr/>

## Modelo de datos

Para el desarrollo de la solución es utlizada solo la tabla que aparece en la siguiente imagen, debido a que es posible formular el desarrollo de manera adecuada con esta representación.

<img width="302" alt="Captura de pantalla 2023-07-30 225031" src="https://github.com/Taekleee/challenge/assets/44279550/be97aa41-9a1f-43e8-9062-ce2ca050b097">



Sin embargo, a modo de mejora se propone generar un modelo de datos, con el fin de optimizar las consultas mediante el uso de las diversas primary keys. 

## Desarrollo: 
**1. Procesos automatizados para ingerir y almacenar los datos bajo demanda**
  
  **a) Los viajes que son similares en términos de origen, destino y hora del día deben agruparse. Describa
  el enfoque que utilizó para agregar viajes similares.**
  #### Consideraciones y supuestos de la implementación: 
  
  - Debido a que el proceso solicitado es para el almacenamiento de datos bajo demanda, es que se genera un método POST con el fin de guardar los valores en la base de datos.
  - Para lograr que los datos se encuentre agrupados dentro de la base de datos, es que se crean índices para ambos valores de localización (origin_coord y destination_coord) y también según la fecha en que se ingresa. Sin embargo, al utilizar la fecha completa no se cumple con lo solicitado, por lo que además, una mejora sería generar nueva columna en el tabla (hour), la cual almacena la hora y permite indexar en base a ese valor.
  - En base a lo anterior, utilizar los índices permite que al momento de realizar los insert, de manera interna la base de datos genere un árbol, lo cual permite optimizar la query de consulta.

  ##### Modo de uso:
  1. URL: http://localhost:5000/insertData
  3. JSON:
     ```
     {
         'region': '',
         'origin_coord': '',
         'destination_coord': '',
         'datetime': '',
         'datasource': ''
     }

  Ejemplo: 
![Captura de pantalla 2023-07-31 223822](https://github.com/Taekleee/challenge/assets/44279550/46015044-8f55-4fad-b3e5-7123e4938472)

Posibles mejoras:
- Validar que los datos ingresados correspondan al tipo de dato solicitado.
- Agregar mensaje de error.
- Mecanismos de autenticación
- Mecanismos de seguridad
- Modelo de datos
- Mejorar la recepción de los datos (que no se debe ingresar POINT(X Y)
  
<hr/>

  **2. Un servicio que es capaz de proporcionar la siguiente funcionalidad:**

  **a. Devuelve el promedio semanal de la cantidad de viajes para un área definida por un bounding box y
la región**

- Para devolver los viajes que se encuentran definidos por un bounding box, se utiliza la consulta SQL que se presenta a continuación:

![Captura de pantalla 2023-07-31 224425](https://github.com/Taekleee/challenge/assets/44279550/a4310274-e804-49bd-8c5e-b16300d290e1)

La consulta lo que realiza es mediante ST_CONTAINS, verificar si el punto de origen y de destino se encuentra dentro de un bounding box. Además,
se valida que la región corresponda a la solicitada por el usuario. Con respecto a la semana, se realiza un GROUP BY según este criterio y se retorna al usuario el
primer y último día de la semana para validar.

Ejemplo: 
![Captura de pantalla 2023-07-31 233302](https://github.com/Taekleee/challenge/assets/44279550/8f2901c1-4e0b-4a3d-99c0-1ecf3b6d2496)

![Captura de pantalla 2023-07-31 233313](https://github.com/Taekleee/challenge/assets/44279550/ba9a40b1-c4fe-44d7-9ee4-9354fb3c1540)


**b. Informar sobre el estado de la ingesta de datos sin utilizar una solución de polling**

  Para informar sobre la ingesta de datos se propone: 
  - Utilizar una solución de weebhook, la cual genera una comunicación desde la API al cliente, con el fin de informar el estado.
  - Para el caso de Python, es posible utilizar websockets, los cuales generan una comunicación via HTML.
  - Por lo tanto, cada vez que se ingrese un dato mediante la consulta descrita en (1), se enviará la comunicación. Sin embargo, al existir muchas consultas esto
    también generará congestión, por lo que una mejora a futuro sería que en base a cierta cantidad de peticiones realizadas, se envíe la información y separar el websocket de la aplicación principal.

Se crea el servidor: 
![Captura de pantalla 2023-07-31 234801](https://github.com/Taekleee/challenge/assets/44279550/1136089c-efd7-4ca8-8b11-9140819650dd)


Función para emitir un mensaje: 

![Captura de pantalla 2023-07-31 234755](https://github.com/Taekleee/challenge/assets/44279550/5a176535-62c4-4f65-a2c0-bee5c0c5c3a2)

Cliente: 

![Captura de pantalla 2023-07-31 234712](https://github.com/Taekleee/challenge/assets/44279550/5ea0b7a2-e519-416d-aec4-ea10be56bde4)

<hr/>

**3. La solución debe ser escalable a 100 millones de entradas. Se recomienda simplificar los datos mediante un
modelo de datos. Agregue pruebas de que la solución es escalable.**

Para probar la solución es utilizado postman. De manera inicial se generan 100 peticiones, lo cual entrega como resultado un promedio de 26ms por petición.

![Captura de pantalla 2023-07-31 235654](https://github.com/Taekleee/challenge/assets/44279550/40121de0-cca3-47ce-b85f-aaca6c00aed2)

Luego se escala la solución a 1.000 peticiones, lo cual genera un aumento en el tiempo de respuesta. 

![Captura de pantalla 2023-08-01 000050](https://github.com/Taekleee/challenge/assets/44279550/aa002917-61c0-4be4-844d-a2e14cf6fb8e)

Debido a lo anterior, se considera que la solución no es escalable, ya que la arquitectura en que se encuentra montada es un entorno local.
Para lograr escalar, una mejora es separar la tabla en un modelo de datos, con el fin de que mediante los índices propios de las tablas, se disminuya el costo computacional de la base de datos. También se podría realizar una refactorización de la query presentada.

Otro punto de mejora es utilizar kubernetes para tener más instancias tanto de la base de datos como del backend, de esta manera no se generarían cuellos de botella, junto con un balanceador de carga.

<hr/>

**4. La solución debe estar escrita en Python usando una base de datos SQL**
 Se cumple con lo solicitado


<hr/>

**5. Incluye contenedores en tu solución y dibuja cómo configuraría la aplicación en GCP**

![Diagrama sin título](https://github.com/Taekleee/challenge/assets/44279550/5ea5fb87-c404-46f6-b246-a1fe4b2d4b42)


- Para el backend se considera un APP Enginee, ya que permite escalar de manera automática.
- Para el websocket se considera un compute enginee debido a que se puede configurar de la manera deseada.
- Para la base de datos se considera el uso de kubernetes, con el fin de escalar de manera horizontal y no generar un cuello de botella en el acceso.
- También se añade un balanceador de carga para distribuir las peticiones a la base de datos.
