# **Pylpaca — ASCOM Alpaca API framework for Python**

Pylpaca implements ASCOM device interfaces and the ASCOM Alpaca API in Python.  
It exposes astronomy devices through HTTP endpoints using FastAPI.

This project is based on:  
**[https://github.com/T0T4R4/pylpaca](https://github.com/T0T4R4/pylpaca)**

The current version replaces the original Tornado server with FastAPI.

---

## **Supported devices**

Pylpaca provides Python versions of ASCOM interfaces for:

- Dome  
- FilterWheel  
- Telescope  
- Camera  
- CoverCalibrator  

Each device type is exposed through Alpaca‑compatible REST endpoints.

The framework does not register drivers in the Windows ASCOM registry.  
It is intended for Alpaca‑only use.

---

## **Driver structure**

Drivers live under `ASCOMDriver/`.  
Each driver implements one or more ASCOM interfaces.  
Example drivers include:

- `MyDomeDriver`  
- `MyFilterWheelDriver`  
- `MyTelescopeDriverV3`  
- `MyTelescopeDriverV4`

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
      "device_driver": "MyASCOMDomeDriver",
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

### **Dome**

```
GET  /api/v1/dome/0/shutterstatus
PUT  /api/v1/dome/0/openshutter
PUT  /api/v1/dome/0/closeshutter
GET  /api/v1/dome/0/connected
PUT  /api/v1/dome/0/connected?Connected=true
```

### **FilterWheel**

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
Each device type has a dedicated test suite.
