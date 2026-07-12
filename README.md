# **Pylpaca — ASCOM Alpaca API framework for Python**

Pylpaca implements ASCOM device interfaces and the ASCOM Alpaca API in Python.  
It exposes astronomy devices through HTTP endpoints using FastAPI.

This project is based on:  
**[https://github.com/T0T4R4/pylpaca](https://github.com/T0T4R4/pylpaca)**

The current version replaces the original Tornado server with FastAPI and adds support for Alpaca device interface versions V2–V4.

---

## **Supported devices**

Pylpaca provides Python implementations of ASCOM interfaces for:

- Camera (V4)  
- CoverCalibrator (V2)  
- Dome (V3)  
- FilterWheel (V2)  
- Focuser (V4)  
- NWaySwitch  
- ObservingConditions (V2)  
- Rotator (V4)  
- Switch (V3)  
- Telescope (V4)  
- Video (V2)

Each device type is exposed through Alpaca‑compatible REST endpoints.

The framework does not register drivers in the Windows ASCOM registry.  
It is intended for Alpaca‑only use.

---

## **Driver structure**

Drivers live under `ASCOMDriver/`.  
Each driver implements one ASCOM interface version.

Example drivers include:

- `MyCameraDriverV4`  
- `MyCoverCalibratorDriver`  
- `MyDomeDriver`  
- `MyFilterWheelDriver`  
- `MyFocuserDriverV4`  
- `MyNWaySwitchDriver`  
- `MyObservingConditionsDriver`  
- `MyRotatorDriverV4`  
- `MySwitchDriver`  
- `MyTelescopeDriverV4`  
- `MyVideoDriver`

Drivers can be extended to control real hardware.

---

## **Configuration**

Devices are defined in `config.json`.

Example:

```json
{
  "drivers": [
    {
      "device_type": "dome",
      "device_number": 0,
      "device_driver": "MyDomeDriver",
      "driver_config": {}
    },
    {
      "device_type": "focuser",
      "device_number": 0,
      "device_driver": "MyFocuserDriverV4",
      "driver_config": {}
    }
  ]
}
```

Each device is exposed under:

```
/api/v1/<device_type>/<device_number>
```

Driver configuration changes can be applied without restarting the server:

```
POST /management/reload
```

Device additions or removals require a restart.

---

## **Installation**

Clone the repository:

```bash
git clone https://github.com/yourname/pylpaca
cd pylpaca
```

Install:

```bash
pip install .
```

Editable install:

```bash
pip install -e .
```

Install test tools:

```bash
pip install .[test]
```

---

## **Running the server**

Start the server:

```bash
python -m pylpaca.server
```

The default port is **11111**.

### **Health check**

```
GET /health
```

---

## **Alpaca Discovery**

Pylpaca includes a UDP discovery server on port 32227, implementing the ASCOM Alpaca Discovery Protocol.  
Unicast and broadcast packets are supported.  
Malformed packets are ignored.

---

## **Environment Configuration**

The server supports environment variables for overriding the default configuration location and bind address.

- `PYLPACA_CONFIG_PATH` — override the path to `config.json`
- `PYLPACA_HOST` — override the server host
- `PYLPACA_PORT` — override the server port
- `PYLPACA_LOG_LEVEL` — set log level

Example:

```bash
PYLPACA_CONFIG_PATH=/path/to/custom-config.json \
PYLPACA_HOST=127.0.0.1 \
PYLPACA_PORT=8123 \
PYLPACA_LOG_LEVEL=DEBUG \
python -m pylpaca.server
```

---

## **API overview**

Below are examples of Alpaca endpoints for each device type.

### **Camera (V4)**

```
PUT  /api/v1/camera/0/connect
PUT  /api/v1/camera/0/disconnect
GET  /api/v1/camera/0/imageready
GET  /api/v1/camera/0/imagearray
PUT  /api/v1/camera/0/startexposure?Duration=1.0&Light=True
PUT  /api/v1/camera/0/abortexposure
```

### **Camera V4 — ImageBytes**

Pylpaca supports Alpaca **ImageBytes** binary transport.

Binary request:

```
GET /api/v1/camera/<n>/imagearray
Accept: application/imagebytes
```

Binary response:

- `content-type: application/imagebytes`
- 32‑byte metadata header
- raw pixel data (Int32, rank 2)

Metadata header layout:

| Field | Type |
|-------|------|
| MetadataVersion | uint32 |
| ErrorNumber | int32 |
| ClientTransactionID | uint32 |
| ServerTransactionID | uint32 |
| DataType | int32 |
| Rank | uint32 |
| Dim1 | uint32 |
| Dim2 | uint32 |

Drivers implementing ImageBytes must provide:

- `GetImageBytes()`  
- `ImageArrayVariant`  
- `CheckConnected()`  

These methods are implementation details and not part of the ASCOM interface.

---

### **CoverCalibrator (V2)**

```
GET  /api/v1/covercalibrator/0/coverstate
PUT  /api/v1/covercalibrator/0/opencover
PUT  /api/v1/covercalibrator/0/closecover
PUT  /api/v1/covercalibrator/0/calibratoron
PUT  /api/v1/covercalibrator/0/calibratoroff
```

### **Dome (V3)**

```
PUT  /api/v1/dome/0/connect
PUT  /api/v1/dome/0/openshutter
PUT  /api/v1/dome/0/closeshutter
GET  /api/v1/dome/0/shutterstatus
```

### **FilterWheel (V2)**

```
GET  /api/v1/filterwheel/0/names
GET  /api/v1/filterwheel/0/position
PUT  /api/v1/filterwheel/0/position?Position=2
```

### **Focuser (V4)**

```
GET  /api/v1/focuser/0/position
PUT  /api/v1/focuser/0/move?value=100
GET  /api/v1/focuser/0/tempcomp
PUT  /api/v1/focuser/0/tempcomp?value=true
```

### **NWaySwitch**

```
GET  /api/v1/nwayswitch/0/getswitch/1
PUT  /api/v1/nwayswitch/0/setswitch/1?state=true
```

### **ObservingConditions (V2)**

```
GET  /api/v1/observingconditions/0/temperature
GET  /api/v1/observingconditions/0/humidity
GET  /api/v1/observingconditions/0/pressure
```

### **Rotator (V4)**

```
GET  /api/v1/rotator/0/position
PUT  /api/v1/rotator/0/moveabsolute?value=90
PUT  /api/v1/rotator/0/sync?value=45
```

### **Switch (V3)**

```
GET  /api/v1/switch/0/getswitch/0
PUT  /api/v1/switch/0/setswitch/0?state=true
```

### **Telescope (V4)**

```
PUT  /api/v1/telescope/0/connect
PUT  /api/v1/telescope/0/slewtocoordinates?RightAscension=...&Declination=...
PUT  /api/v1/telescope/0/abortslew
GET  /api/v1/telescope/0/tracking
PUT  /api/v1/telescope/0/tracking?Tracking=true
```

### **Video (V2)**

```
GET  /api/v1/video/0/lastvideoframe
GET  /api/v1/video/0/supportedintegrationrates
PUT  /api/v1/video/0/integrationrate?value=1
```

### **Management**

```
GET  /management/apiversions
GET  /management/v1/description
GET  /management/v1/configureddevices

POST /management/reload
GET  /management/driver/<device_type>/<device_number>
POST /management/driver/<device_type>/<device_number>/reload
```

---

## **Testing**

Tests use pytest and httpx.  
Test files live under `tests/`.

Each device type has a dedicated test suite.

Discovery tests cover:

- valid packets  
- malformed packets  
- unicode packets  
- oversized packets  
- broadcast and unicast  
- full server integration  
- load testing

Camera tests include:

- JSON ImageArray  
- ImageBytes binary transport  
- metadata header validation  
- dimension block validation  
- payload length  
- ServerTransactionID increments  
- connection requirements

Mock drivers mirror real driver behavior for consistent test coverage.
