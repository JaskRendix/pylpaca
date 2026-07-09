# **Pylpaca — ASCOM Alpaca API framework for Python**

Pylpaca implements ASCOM device interfaces and the ASCOM Alpaca API in Python.  
It exposes astronomy devices through HTTP endpoints using FastAPI.

This project is based on:  
**[https://github.com/T0T4R4/pylpaca](https://github.com/T0T4R4/pylpaca)**

The current version replaces the original Tornado server with FastAPI and adds full support for modern Alpaca device interface versions (V2–V4).

---

## **Supported devices**

Pylpaca provides Python implementations of ASCOM interfaces for:

- Dome (V3)  
- FilterWheel (V2)  
- Telescope (V4)  
- Camera (V4)  
- CoverCalibrator (V2)
- Video (V2)

Each device type is exposed through Alpaca‑compatible REST endpoints.

The framework does not register drivers in the Windows ASCOM registry.  
It is intended for Alpaca‑only use.

---

## **Driver structure**

Drivers live under `ASCOMDriver/`.  
Each driver implements one or more ASCOM interfaces.

Example drivers include:

- `MyDomeDriver` (IDomeV3)  
- `MyFilterWheelDriver` (IFilterWheelV2)  
- `MyTelescopeDriverV4` (ITelescopeV4)  
- `MyCameraDriverV4` (ICameraV4)  
- `MyCoverCalibratorDriver` (ICoverCalibratorV2)
- `MyVideoDriver` (IVideoV2)

Drivers can be extended to control real hardware.

---

## **Configuration**

Devices are defined in `config.json`.  
Each entry describes one Alpaca‑exposed device.

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
      "device_type": "filterwheel",
      "device_number": 0,
      "device_driver": "MyFilterWheelDriver",
      "driver_config": {}
    }
  ]
}
```

Each device is exposed under:

```
/api/v1/<device_type>/<device_number>
```

Changes to this file require a server restart.

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

---

## **API overview**

### **Dome (V3)**

```
PUT  /api/v1/dome/0/connect
PUT  /api/v1/dome/0/disconnect
GET  /api/v1/dome/0/connecting
GET  /api/v1/dome/0/devicestate

GET  /api/v1/dome/0/shutterstatus
PUT  /api/v1/dome/0/openshutter
PUT  /api/v1/dome/0/closeshutter

GET  /api/v1/dome/0/connected
PUT  /api/v1/dome/0/connected?Connected=true
```

### **FilterWheel (V2)**

```
GET  /api/v1/filterwheel/0/focusoffsets
GET  /api/v1/filterwheel/0/names
GET  /api/v1/filterwheel/0/position
PUT  /api/v1/filterwheel/0/position?Position=2

GET  /api/v1/filterwheel/0/connected
PUT  /api/v1/filterwheel/0/connected?Connected=true

PUT  /api/v1/filterwheel/0/connect
PUT  /api/v1/filterwheel/0/disconnect
GET  /api/v1/filterwheel/0/connecting
GET  /api/v1/filterwheel/0/devicestate
```

### **Telescope (V4)**

```
PUT  /api/v1/telescope/0/connect
PUT  /api/v1/telescope/0/disconnect
GET  /api/v1/telescope/0/connecting
GET  /api/v1/telescope/0/devicestate

GET  /api/v1/telescope/0/rightascension
GET  /api/v1/telescope/0/declination
GET  /api/v1/telescope/0/siderealtime
GET  /api/v1/telescope/0/utcdate

PUT  /api/v1/telescope/0/slewtocoordinates?RightAscension=...&Declination=...
PUT  /api/v1/telescope/0/abortslew

GET  /api/v1/telescope/0/tracking
PUT  /api/v1/telescope/0/tracking?Tracking=true

GET  /api/v1/telescope/0/trackingrate
PUT  /api/v1/telescope/0/trackingrate?TrackingRate=0
```

### **Camera (V4)**

```
PUT  /api/v1/camera/0/connect
PUT  /api/v1/camera/0/disconnect
GET  /api/v1/camera/0/connecting
GET  /api/v1/camera/0/devicestate

PUT  /api/v1/camera/0/startexposure?Duration=1.0&Light=True
PUT  /api/v1/camera/0/stopexposure
PUT  /api/v1/camera/0/abort

GET  /api/v1/camera/0/imageready
GET  /api/v1/camera/0/imagearray

PUT  /api/v1/camera/0/binx?BinX=2
PUT  /api/v1/camera/0/biny?BinY=2
PUT  /api/v1/camera/0/numx?NumX=1000
PUT  /api/v1/camera/0/numy?NumY=1000
PUT  /api/v1/camera/0/startx?StartX=0
PUT  /api/v1/camera/0/starty?StartY=0

PUT  /api/v1/camera/0/cooleron
PUT  /api/v1/camera/0/ccdtemperature?CCDTemperature=-10
PUT  /api/v1/camera/0/gain?Gain=100
PUT  /api/v1/camera/0/offset?Offset=10
PUT  /api/v1/camera/0/readoutmode?ReadoutMode=0
```

### **Video (V2)**

```
GET  /api/v1/video/0/connected
PUT  /api/v1/video/0/connected?value=true

GET  /api/v1/video/0/description
GET  /api/v1/video/0/driverinfo
GET  /api/v1/video/0/driverversion
GET  /api/v1/video/0/interfaceversion
GET  /api/v1/video/0/name

GET  /api/v1/video/0/supportedactions
PUT  /api/v1/video/0/action/<ActionName>

GET  /api/v1/video/0/videocapturedevicename
GET  /api/v1/video/0/exposuremax
GET  /api/v1/video/0/exposuremin
GET  /api/v1/video/0/framerate

GET  /api/v1/video/0/supportedintegrationrates
GET  /api/v1/video/0/integrationrate
PUT  /api/v1/video/0/integrationrate?value=<index>

GET  /api/v1/video/0/lastvideoframe

GET  /api/v1/video/0/sensorname
GET  /api/v1/video/0/sensortype
```

### **CoverCalibrator (V2)**

```
PUT  /api/v1/covercalibrator/0/connect
PUT  /api/v1/covercalibrator/0/disconnect
GET  /api/v1/covercalibrator/0/connecting
GET  /api/v1/covercalibrator/0/devicestate

GET  /api/v1/covercalibrator/0/coverstate
PUT  /api/v1/covercalibrator/0/opencover
PUT  /api/v1/covercalibrator/0/closecover
PUT  /api/v1/covercalibrator/0/haltcover

GET  /api/v1/covercalibrator/0/calibratorstate
GET  /api/v1/covercalibrator/0/brightness
GET  /api/v1/covercalibrator/0/maxbrightness
PUT  /api/v1/covercalibrator/0/calibratoron
PUT  /api/v1/covercalibrator/0/calibratoroff
```

### **Management**

```
GET /management/apiversions
GET /management/v1/description
GET /management/v1/configureddevices
```

---

## **Testing**

Tests use pytest and httpx.  
Test files live under `tests/`.  
Each device type has a dedicated test suite, including:

- DomeV3  
- TelescopeV4  
- CameraV4  
- FilterWheelV2  
- CoverCalibratorV2  
- Management API  
- Driver instantiation  
- Error handling

The test suite validates both driver behavior and Alpaca REST API compliance.
