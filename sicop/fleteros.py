"""Fleteros a monitorear. La empresa/cliente activo es CAFES LA VIRGINIA (id 310).
El token 'prosta' de ProveedorEdit se resuelve dinámicamente desde la grilla por CUIT,
así que acá alcanza con CUIT + nombre + (opcional) contacto del chofer.
"""
EMPRESA_ID = "310"          # CAFES LA VIRGINIA S.A. (contratista principal: TRANSTOTAL SRL)
CONTRATISTA_CUIT = "30708855312"  # TRANSTOTAL SRL

FLETEROS = [
    {"cuit": "20224757000", "nombre": "BARRIONUEVO CESAR CEFERINO", "telefono": None, "email": None},
    {"cuit": "20271494905", "nombre": "COSTANZO MATIAS MANUEL",     "telefono": None, "email": None},
    {"cuit": "20210116460", "nombre": "WEGNER CLAUDIO",             "telefono": None, "email": None},
]
