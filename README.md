# energy-mqtt-simulator

A simple Python application that simulates energy consumption / production (based on static data) by sending telemetry to an MQTT broker

### Define environment

Create your `.env` file like `.env.sample`

e.g.

```
MQTT_SERVER='192.168.1.10'
MQTT_PORT=1883
MQTT_KEEP_ALIVE=60
MQTT_USER='username'  # '' if no auth required
MQTT_PASSWORD='password'  # '' if no auth required
MQTT_RECONNECT_DELAY = 5
SCAN_INTERVAL=10
PRODUCTION_CLIENT='energyprod'
PRODUCTION_TOPIC='tele/energyprod'
PRODUCTION_LWT='LWT/energyprod'
```

### Docker Compose example

```yaml
services:

  energy-simulator:
  
    container_name: energy-simulator
    image: ghcr.io/snakuzzo/energy-mqtt-simulator:main
    volumes:
    - "${PWD}:/app/.env"
    environment:
    - "TZ=Europe/Rome"
    network_mode: host 
    restart: unless-stopped
```
