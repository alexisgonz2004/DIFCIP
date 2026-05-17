# kpis.py
# Fase 3 — Limpieza y KPIs
# DIFCIP

import pandas as pd

# ── 1. Cargar el dataset ───────────────────────────────────────────────────
df = pd.read_csv("../data/raw/ventas_2024.csv")

print("=== ANTES DE LIMPIAR ===")
print(f"Total filas: {len(df)}")
print(f"Cantidades negativas: {(df['cantidad'] < 0).sum()}")
print(f"NCF nulos: {df['ncf'].isna().sum()}")

# ── 2. Limpiar errores ─────────────────────────────────────────────────────
df_limpio = df[df['cantidad'] > 0].copy()
df_limpio = df_limpio.dropna(subset=['ncf'])

print("\n=== DESPUÉS DE LIMPIAR ===")
print(f"Total filas: {len(df_limpio)}")

# ── 3. KPIs ───────────────────────────────────────────────────────────────
total_ventas     = df_limpio['total'].sum()
ticket_promedio  = df_limpio['total'].mean()
total_itbis      = df_limpio['itbis'].sum()
mes_top          = df_limpio.groupby('fecha')['total'].sum().idxmax()

print("\n=== KPIs ===")
print(f"Total ventas:    RD$ {total_ventas:,.2f}")
print(f"Ticket promedio: RD$ {ticket_promedio:,.2f}")
print(f"Total ITBIS:     RD$ {total_itbis:,.2f}")
print(f"Día top:         {mes_top}")

# ── 4. Guardar dataset limpio ──────────────────────────────────────────────
df_limpio.to_csv("../data/processed/ventas_limpio.csv", index=False, encoding="utf-8-sig")
print("\n✅ Dataset limpio guardado.")