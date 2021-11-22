<div align="center">
  <h1>DriveTerminal</h1>
  <h4>Esta herramienta esta creada con el fin de poder gestionar google drive atraves de una terminal.</h4>
</div>
<ul>
    <li>Es te script es capaz de descargar y subir archivos, visualizar archivos y carpetas que se encuentren almacenados en google drive.</li>
    <li>Ademas permite crear nuevas carpetas y eleiminar archivos y carpetas.</li>
</ul> 

Requisitos
======
Intalar las librerias de python: 

    pip install tabulate
    pip install PyDrive2
    pip install PyDrive

Uso Google Drive API
======
### Crea un proyecto en https://console.cloud.google.com y habilita la Google Drive API
![](https://i.imgur.com/hmWrrdT.png)

### Añade el correo electronico que usaras luego para logearte al ejecutar el bot
![](https://i.imgur.com/FFM6NaW.png)

### Descarga las credenciales en JSON
![](https://i.imgur.com/KnIT73i.png)

### Renombra el archivo descargado a [client_secret.json]
![](https://i.imgur.com/TaMKGaz.png)

### Ahora con los datos de client_secret.json rellena los datos que faltan en settings.yaml
![](https://i.imgur.com/XEBzLsp.png)
