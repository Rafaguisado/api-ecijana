from fastapi import FastAPI, Query
import pandas as pd

app = FastAPI(title="API Ecijana del Acero")

EXCEL = "DATOS_ECIJANA_API_READY.xlsx"

def leer_hoja(nombre_hoja):
    df = pd.read_excel(EXCEL, sheet_name=nombre_hoja)
    return df.fillna("").to_dict(orient="records")

@app.get("/")
def inicio():
    return {
        "empresa": "Ecijana del Acero",
        "estado": "API funcionando"
    }

@app.get("/materiales")
def materiales():
    return leer_hoja("api_materiales")

@app.get("/proveedores")
def proveedores():
    return leer_hoja("api_proveedores")

@app.get("/pedidos")
def pedidos():
    return leer_hoja("api_pedidos")

@app.get("/obras")
def obras():
    return leer_hoja("api_obras")

@app.get("/medios-auxiliares")
def medios_auxiliares():
    return leer_hoja("api_medios_auxiliares")

@app.get("/materiales/buscar")
def buscar_material(q: str = Query(..., description="Texto a buscar en materiales")):
    df = pd.read_excel(EXCEL, sheet_name="api_materiales").fillna("")
    resultado = df[df["material"].astype(str).str.contains(q, case=False, na=False)]
    return resultado.to_dict(orient="records")

@app.get("/proveedores/buscar")
def buscar_proveedor(q: str = Query(..., description="Texto a buscar en proveedores")):
    df = pd.read_excel(EXCEL, sheet_name="api_proveedores").fillna("")
    resultado = df[df.astype(str).apply(lambda fila: fila.str.contains(q, case=False, na=False).any(), axis=1)]
    return resultado.to_dict(orient="records")
@app.get("/precio-material")
def precio_material(nombre: str):

    df = pd.read_excel(
        EXCEL,
        sheet_name="api_materiales"
    ).fillna("")

    resultado = df[
        df["material"].astype(str)
        .str.contains(nombre, case=False, na=False)
    ]

    if len(resultado) == 0:
        return {
            "error": "Material no encontrado"
        }

    return resultado[[
        "material",
        "precio_medio",
        "precio_min",
        "precio_max",
        "ultimo_precio",
        "ultimo_proveedor",
        "proveedor_habitual"
    ]].to_dict(orient="records")


@app.get("/proveedor-material")
def proveedor_material(nombre: str):

    df = pd.read_excel(
        EXCEL,
        sheet_name="api_materiales"
    ).fillna("")

    resultado = df[
        df["material"].astype(str)
        .str.contains(nombre, case=False, na=False)
    ]

    if len(resultado) == 0:
        return {
            "error": "Material no encontrado"
        }

    return resultado[[
        "material",
        "ultimo_proveedor",
        "proveedor_habitual"
    ]].to_dict(orient="records")


@app.get("/top-proveedores")
def top_proveedores():

    df = pd.read_excel(
        EXCEL,
        sheet_name="api_proveedores"
    ).fillna("")

    columnas = list(df.columns)

    return {
        "columnas_detectadas": columnas,
        "datos": df.head(20).to_dict(
            orient="records"
        )
    }