kubectl apply -f components.yaml
kubectl apply -f mqtt-deployment.yaml
kubectl apply -f influxdb-deployment.yaml
kubectl apply -f telegraf-deployment.yaml
kubectl apply -f grafana-deployment.yaml
kubectl apply -f metrics-client.yaml

http://localhost:3000/ (Grafana) admin admin
http://localhost:8086/ (InfluxDB) admin admin123
http://localhost:8080/ (Web-MQTT)

Para visionar todas las graficas es necesario lanzar todos los pods tanto de hito 4 como de hito 5.

Despues subir los datos al hito 4 (modelo y dataset) y automaticamente se mostraran la version del modelo y la distribucion de los datos

web-mqtt.yaml es un sistema sencillo para probar el envio de datos a MQTT, no es necesario para el hito 5.
