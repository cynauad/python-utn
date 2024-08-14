######################################################################
#
#   Socket para obtener los datos de los observadores implementados
#
######################################################################


La consulta mediante socket está armada para consultar los eventos DEL DIA que registran los
dos observadores implementados. 

Para verlo en funcionamiento:
1- ejecutar la app desde controller.py
2- en la pestaña "Servidor" del menú, hacer click en "Iniciar SRV" (esto inicie el servidor y queda escuchando)
3- Además, seleccionar la base de datos a utilizar (esto genera un registro con fecha de hoy en objeto Observer1
y podrá ser mostrado en el cliente. Si no se activa mostrara que no eventos para mostrar el dia de hoy.)

4- Por otro lado, ejecutar por consola el script "Client.py". Si el servidor está activo debe mostrar un mensaje de bienvenida y opciones para elegir que datos obtener de los observadores.
5- Si en este punto se preciona la opcion 1, deberá imprimir la base de datos seleccionada, si que es se seleccionó en el paso anterior (paso 3). Sino mostrará que "No eventos para mostrar".
6- Asi mismo, si se agrega un Alta o Baja de un evento registrado, se genera el log del dia del Observador2 y podrá consultarse desde el cliente, a traves de la opción 2. De lo contrario, que no hay eventos para mostrar.


