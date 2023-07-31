# Challenge


## Tecnologías utilizadas y justificación
- Lenguaje: Python
- Framework: Flask. Se decide implementar debido a que es una de las tecnologías utilizadas por la empresa.
- Base de datos: Mysql. Esta base de datos permite manejar de buena manera los datos espaciales, tales como las coordenadas de origen y destino descritas en el enunciado. Además, es de tipo SQL, tal como se solicita en el enunciado.


<hr/>

## Modelo de datos

Para el desarrollo de la solución es utlizada solo la tabla que aparece en la siguiente imagen, debido a que es posible formular el desarrollo de manera adecuada con esta representación.

<img width="102" alt="Captura de pantalla 2023-07-30 225031" src="https://github.com/Taekleee/challenge/assets/44279550/5b8dd000-b03a-4ee8-934a-245546290bc0">

Sin embargo, a modo de mejora se propone generar el siguiente modelo de datos, con el fin de optimizar las consultas mediante el uso de las diversas primary keys. 

## Desarrollo: 
**1. Procesos automatizados para ingerir y almacenar los datos bajo demanda**
  
  **a) Los viajes que son similares en términos de origen, destino y hora del día deben agruparse. Describa
  el enfoque que utilizó para agregar viajes similares.**

  Debido a que el proceso solicitado es para el almacenamiento de datos, es que se decide utilizar índices, ya que estos generan que a medida que se van insertando nuevos    datos, se genere un árbol, lo cual optimiza el tiempo de ejecución de la consulta. 

<hr/>

  **2. Un servicio que es capaz de proporcionar la siguiente funcionalidad:**

  **a. Devuelve el promedio semanal de la cantidad de viajes para un área definida por un bounding box y
la región**

- Para devolver los viajes que se encuentran definidos por un bounding box, se utiliza la consulta SQL 

**b. Informar sobre el estado de la ingesta de datos sin utilizar una solución de polling**


  #### Servicio: 

  
