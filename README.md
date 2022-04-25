# Selenium-Stuff

Requisitos

- Python3 instalado (en Windows se descarga desde la tienda Micrpsoft)
- Instalar Selenium y el wendrive ejecutando
  - pip install selenium
  - pip install webdriver_manager


Editar el script con un editor y modificar las variables requeridas:
- USER, PASSWORD: no requieren de explicación
- FIRST_DAY, LAST_DAY: el día de comienzo y el final. Si hay festivos entre medias (aparte de Sábados y Domingos) esos días no se actualizarán (dará un error) pero el programa no aborta, así que se puede poner un año entero si se quiere
- STARTING_HOUR, VARIANCE: la hora de comienzo y la variación aleatoria en minutos. Ejemplo si la hora de comienzo son “09:00” y VARIANCE son 60, el programa generará hora aleatorias de entrada entre las 08:30 y las 09:30. Así queda más realista 😊
- EXTRA_TIME: el tiempo de la comida o no computable
-	LOCAL_HOLIDAYS, VARIABLE_HOLIDAYS para ajustar los festivos en cada año/region

