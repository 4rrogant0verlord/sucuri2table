<p align="center">
  <h2 align="center">Sucuri-2-DataTables</h2>
  <p>
  Script para transferir eventos del Sucuri Web Application Firewall (WAF) hacia Azure Data Tables, en formato JSON.
  </p>
</p>

---

#### Requerimientos:

* [Python3.8+](https://www.python.org/downloads/)

#### Como ejecutar:

Ejecute:

```
python3 -m venv env
```

En Windows, corra:

```
env\Scripts\activate.bat
```

En Unix o MacOS, corra:

```
source env/bin/activate
```

Luego ejecute:

```
pip install -r requirements.txt
```

Finalmente:

```
python3 app.py
```

#### Configuración:

```python
AZURE_ACC_KEY = ...        # Cambiar a la llave de cuenta correspondiente.
AZURE_ACC_NAME = ...       # Cambiar al nombre de cuenta correspondiente.
AZURE_TABLE_NAME = ...     # Cambiar al nombre de tabla correspondiente.
SUCURI_SITES = [
    {
        "secret": "...",   # Añadir tantos API_SECRET como le sea necesario.
        ...
    },
]
```

#### Referencias:

https://waf.sucuri.net/?apidocs
https://docs.microsoft.com/en-us/python/api/overview/azure/data-tables-readme?view=azure-python
https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/tables/azure-data-tables
