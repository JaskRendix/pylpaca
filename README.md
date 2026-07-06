# **Pylpaca — ASCOM Alpaca API framework for Python**

Pylpaca is a Python implementation of the [ASCOM](https://ascom-standards.org/) device interfaces and the [ASCOM Alpaca API](https://ascom-standards.org/api).  
It provides a simple way to expose astronomy hardware—such as domes, telescopes, and cameras—through HTTP endpoints.

This project is based on the original work at:  
**[https://github.com/T0T4R4/pylpaca](https://github.com/T0T4R4/pylpaca)**

The current version replaces the original Tornado server with a modern FastAPI implementation.

---

## **Project scope**

Pylpaca supplies:

- Python versions of ASCOM device interfaces  
- A FastAPI server that exposes Alpaca‑compatible REST endpoints  
- A structure for building custom device drivers  
- A working example dome driver (`MyDomeDriver`)  

The framework does not register drivers in the Windows ASCOM registry.  
It is intended for Alpaca‑only use.

---

## **Driver model**

Drivers live under `ASCOMDriver/` and follow the ASCOM interface structure.  
`MyDomeDriver` is a simple example that simulates a dome shutter.  
You can extend it to control real hardware (serial, USB, network, etc.).

---

## **Configuration**

Drivers are defined in `config.json`.  
Each entry describes one device exposed by the Alpaca server.

Example:

```json
{
  "drivers": [
    {
      "device_type": "dome",
      "device_number": 0,
      "device_driver": "MyASCOMDomeDriver",
      "driver_config": {}
    }
  ]
}
```

Changes to this file require a server restart.

---

## **Installation**

### **1. Clone the repository**

```bash
git clone https://github.com/yourname/pylpaca
cd pylpaca
```

### **2. Install the package**

```bash
pip install .
```

### **3. Editable install**

```bash
pip install -e .
```

### **Optional: install test tools**

```bash
pip install .[test]
```

---

## **Running the server**

Start the Alpaca server with:

```bash
python server.py
```

The server listens on port **11111** by default.

---

## **Using the API**

With the example dome driver enabled, the following endpoints are available:

```
GET  /api/v1/dome/0/shutterstatus
PUT  /api/v1/dome/0/openshutter
PUT  /api/v1/dome/0/closeshutter
GET  /api/v1/dome/0/connected
PUT  /api/v1/dome/0/connected?Connected=true
```

Management endpoints:

```
GET /management/apiversions
GET /management/v1/description
GET /management/v1/configureddevices
```
