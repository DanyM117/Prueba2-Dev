# Prueba2-Dev
Reposritorio para la prueba 2 de DevSecOps

En este repositorio se encuentra el src de la imagen del backend para añadir los registros y conexón a la base de datos.

El resources está añadido en este repositorio por motivos de agilidad en el desarrollo de esta prueba en el repositorio local.

La nueva imagen de docker es: ```https://hub.docker.com/r/danym117/prueba2-dev```

La imagen para la bd es postgres:15

# Instrucciones

Para poder ver la correcta ejecución de esta prueba en OpenShift, hay que hacer una serie de pasos previos.

Primero hay que iniciar sesión en el cluster de openshift con el comando ```oc login```

Una vez hecho eso y recomendablemente creamos un nuevo namespace para la aplicación solo por buenas prácticas, esto con ek comando ```oc new-project prueba2-dev```

Aplicamos el resources con ```oc apply -f resources.yml```

Probablemente debamos asignar la cuenta de servicio del deploy a una política privilegiada por funciones específicas como los volumenes, podemos hacer esto con el comando: ```oc adm policy add-scc-to-user anyuid system:serviceaccount:prueba2-dev:default```

Ya solo esperamos a que los contenedores se creen correctamente y después ingresamos al backend con : ```oc rsh deployment/prueba-especial-deployment -c backend```

Con eso ya deberíamos poder hacer curl a localhost por el 8080 y despues un ```psql -c "SELECT * FROM log;"``` para ver los registros de logins.

Para validar la persistencia podríamos eliminar el pod con ```oc delete pod -l app=prueba-especial```
Esperamos a que el pod vuelva a levantarse y una vez termine podemos ejecutar directamente la consulta ```oc exec -it deployment/prueba-especial-deployment -c database -- psql -U app -d app -c "SELECT * FROM log;"``` y podremos ver que se quedarán guardados los registros previos al delete del pod