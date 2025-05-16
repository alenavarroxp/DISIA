kubectl apply -f mqtt-deployment.yaml
kubectl apply -f influxdb-deployment.yaml
kubectl apply -f telegraf-deployment.yaml
kubectl apply -f grafana-deployment.yaml
kubectl apply -f web-mqtt.yaml

http://localhost:3000/ (Grafana) admin admin
http://localhost:8086/ (InfluxDB) admin admin123
http://localhost:8080/ (Web-MQTT)

