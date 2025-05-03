# Despliegue de Servicios en Kubernetes

Para desplegar los servicios necesarios, ejecute los siguientes comandos en el orden indicado:

```bash
kubectl apply -f k8s/volumenes.yaml
kubectl apply -f k8s/entrenador-deployment.yaml
kubectl apply -f k8s/inferidor-deployment.yaml
kubectl apply -f k8s/entrenador-service.yaml
kubectl apply -f k8s/inferidor-service.yaml
kubectl apply -f k8s/gestor.yaml

# Verificar el estado de los recursos desplegados
echo "Verificando los pods desplegados:"
kubectl get pods
echo "Verificando los servicios desplegados:"
kubectl get services
echo "Verificando los volúmenes persistentes:"
kubectl get pvc
echo "Finalizando el despliegue de los servicios."
```

## Crear y Subir Imágenes Docker

En caso de querer crear y subir sus propias imágenes Docker, siga los siguientes pasos:

### Entrenador

```bash
cd entrenador
docker build -t TU_USUARIO_DOCKERHUB/entrenador:latest .
docker push TU_USUARIO_DOCKERHUB/entrenador:latest
```

### Inferidor

```bash
cd ../inferidor
docker build -t TU_USUARIO_DOCKERHUB/inferidor:latest .
docker push TU_USUARIO_DOCKERHUB/inferidor:latest
```

Recuerde modificar los archivos `k8s/entrenador-deployment.yaml` y `k8s/inferidor-deployment.yaml` para que apunten a las imágenes que ha creado.

## Notas Importantes

- Asegúrese de tener configurado un clúster de Kubernetes y que `kubectl` esté correctamente instalado y configurado.
- Los servicios están configurados para usar un `LoadBalancer`. Verifique que su proveedor de Kubernetes soporte este tipo de servicio.
- Se presupone que las imágenes Docker necesarias ya han sido creadas y subidas a Docker Hub.

## Estructura del Dataset

El dataset utilizado en este proyecto está organizado de la siguiente manera:

### `dataset/dataset`

- **`images`**: Contiene las imágenes utilizadas para el entrenamiento y validación del modelo. Los nombres de los archivos sugieren que podrían estar etiquetados o rotados (por ejemplo, `0_10.jpg`, `90_10.jpg`, etc.).
- **`labels/train_data.csv`**: Archivo CSV que contiene las etiquetas asociadas a las imágenes de entrenamiento.

### `dataset/test`

- **`images`**: Contiene imágenes separadas que no se usan durante el entrenamiento. Estas imágenes se utilizan para evaluar el modelo entrenado y medir su rendimiento en datos no vistos.
- **`labels/test_data.csv`**: Archivo CSV que contiene las etiquetas correspondientes a las imágenes de prueba. Sirve para comparar las predicciones del modelo con las etiquetas reales y calcular métricas de evaluación como precisión, recall, F1-score, etc.

## Iniciar la Carga de Datos

El gestor de archivos permite subir datos al sistema de manera sencilla. Para iniciar la carga de datos, siga estos pasos:

1. Asegúrese de que el servicio del gestor de archivos esté desplegado y funcionando correctamente. Puede verificarlo con el siguiente comando:

   ```bash
   kubectl get services
   ```

   Busque el servicio `ip-file-manager-service` y anote la dirección IP o URL asignada.

2. Abra un navegador web y acceda a la URL del servicio. Por ejemplo:

   ```
   http://localhost
   ```

3. En la página principal, encontrará un formulario para subir archivos. Complete los siguientes campos:

   - **Archivos**: Seleccione la carpeta que desea subir.
   - **Destino**: Elija el destino de los archivos. Puede ser `Dataset` o `Modelo`.

4. Haga clic en el botón **Subir** para cargar los archivos al sistema.

   - Debe subir la carpeta `datasets` a `Dataset` y la carpeta `modelobase` a `Modelo`.

5. Una vez completada la carga, puede verificar los archivos subidos accediendo a los enlaces proporcionados en la página principal:

   - Archivos en Dataset: [http://localhost/dataset/](http://localhost/dataset/)
   - Archivos en Modelo: [http://localhost/compartido/](http://localhost/compartido/)


## Endpoints Disponibles

Una vez desplegados, los servicios estarán disponibles en las siguientes rutas:

- Entrenador: [http://localhost:5000/train](http://localhost:5000/train)
- Inferidor: [http://localhost:5001/inferir](http://localhost:5001/inferir)

Puede probar los endpoints utilizando herramientas como `curl` o Postman.

## Ejemplo de Uso con curl

Para probar el endpoint de Inferidor con una solicitud POST, puede usar el siguiente comando:

```bash
curl -X POST http://localhost:5001/inferir -H "Content-Type: application/json" -d "{\"data\": \"valor_de_prueba\"}"
```

Reemplace `valor_de_prueba` con los datos que desee enviar al servicio.

