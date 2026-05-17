# generar_dataset.py
# Fase 1 — Generación del Dataset de Ventas DIFCIP

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

random.seed(42)
np.random.seed(42)

CLIENTES = [
    "Supermercados Nacional", "Grupo Rica", "Corripio Import",
    "Ferretería Americana", "Distribuidora Rojas", "Inversiones Pérez SRL",
    "Colmado El Vecino", "Farmacia Carol", "Tienda La Promesa",
    "Empresa Constructora Báez", "Comercial Hernández", "Grupo Ramos",
    "Import & Export Martínez", "Distribuidora Flores", "El Emporio del Sur"
]

VENDEDORES = [
    "Carlos Méndez", "Ana Rodríguez", "Pedro Fernández",
    "María Santos", "José García", "Luisa Peralta"
]

REGIONES = ["Santo Domingo", "Santiago", "La Romana", "San Pedro de Macorís",
            "Puerto Plata", "La Vega", "Higüey", "Barahona"]


PRODUCTOS = {
    "Arroz Premium 50lb":        {"precio": 2850, "categoria": "Alimentos"},
    "Aceite de Cocina 1gl":      {"precio": 980,  "categoria": "Alimentos"},
    "Azúcar Refinada 100lb":     {"precio": 4200, "categoria": "Alimentos"},
    "Cemento Portland (saco)":   {"precio": 590,  "categoria": "Construcción"},
    "Varilla 3/8 (quintal)":     {"precio": 3800, "categoria": "Construcción"},
    "Pintura Latex Galón":       {"precio": 1450, "categoria": "Ferretería"},
    "Cable #12 (rollo 100m)":    {"precio": 3200, "categoria": "Ferretería"},
    "Detergente Industrial 5gl": {"precio": 1750, "categoria": "Limpieza"},
    "Papel Higiénico x48":       {"precio": 1100, "categoria": "Limpieza"},
    "Agua Mineral x24":          {"precio": 420,  "categoria": "Bebidas"},
    "Jugo Tropical x12":         {"precio": 680,  "categoria": "Bebidas"},
    "Cerveza Presidente x24":    {"precio": 1200, "categoria": "Bebidas"},
}

def generar_ncf(tipo="B01", numero=1):
    return f"{tipo}-{str(numero).zfill(8)}"

def generar_ventas(n=500):
    fecha_inicio = datetime(2024, 1, 1)
    fecha_fin    = datetime(2024, 6, 30)
    dias_rango   = (fecha_fin - fecha_inicio).days
    registros    = []

    for i in range(1, n + 1):
        producto_nombre = random.choice(list(PRODUCTOS.keys()))
        producto_info   = PRODUCTOS[producto_nombre]
        cantidad        = random.randint(1, 50)
        precio_unitario = producto_info["precio"]
        subtotal        = round(cantidad * precio_unitario, 2)

        tiene_itbis = random.random() > 0.2
        itbis       = round(subtotal * 0.18, 2) if tiene_itbis else 0
        total       = round(subtotal + itbis, 2)

        fecha    = fecha_inicio + timedelta(days=random.randint(0, dias_rango))
        tipo_ncf = "B01" if random.random() > 0.3 else "B02"
        ncf      = generar_ncf(tipo_ncf, i)

        if random.random() < 0.05:
            cantidad = -cantidad
        if random.random() < 0.05:
            ncf = None

        registros.append({
            "id_venta":        i,
            "fecha":           fecha.strftime("%Y-%m-%d"),
            "cliente":         random.choice(CLIENTES),
            "vendedor":        random.choice(VENDEDORES),
            "region":          random.choice(REGIONES),
            "producto":        producto_nombre,
            "categoria":       producto_info["categoria"],
            "cantidad":        cantidad,
            "precio_unitario": precio_unitario,
            "subtotal":        subtotal,
            "itbis":           itbis,
            "total":           total,
            "ncf":             ncf,
            "tipo_ncf":        tipo_ncf,
        })

    return pd.DataFrame(registros)
if __name__ == "__main__":
    os.makedirs("../data/raw", exist_ok=True)

    df   = generar_ventas(500)
    ruta = "../data/raw/ventas_2024.csv"
    df.to_csv(ruta, index=False, encoding="utf-8-sig")

    print(f"✅ Dataset generado: {ruta}")
    print(f"   Filas:    {len(df)}")
    print(f"   Columnas: {list(df.columns)}")
    print(f"\n📋 Primeras 3 filas:")
    print(df.head(3).to_string())
    print(f"\n⚠️  Errores intencionales introducidos:")
    print(f"   NCF nulos:           {df['ncf'].isna().sum()}")
    print(f"   Cantidades negativas: {(df['cantidad'] < 0).sum()}")