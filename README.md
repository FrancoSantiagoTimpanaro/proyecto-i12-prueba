#clonar el repo
#en la carpeta postgres crear una carpeta vacía llamada data en el mismo nivel donde esta la carpeta init-scripts
#hacer docker compose up --build -d desde la carpeta del proyecto
#hacer docker exec -it backend_i12 bash (para que haya un tabla users)
#hacer flask db upgrade (para que hay una tabla users)
#navegar a http://localhost:5000/ o http://localhost para ver si se conecta con flask/proxy
#probar endpoints /health o /users
