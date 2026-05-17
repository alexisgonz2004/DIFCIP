-- ================================================
-- DIFCIP - Consultas Analíticas
-- Fase 2 - SQL
-- ================================================

-- 1. Total vendido por vendedor
SELECT vendedor,
       TO_CHAR(SUM(total), 'FM999,999,999.00') AS total_vendido
FROM ventas
WHERE cantidad > 0
GROUP BY vendedor
ORDER BY SUM(total) DESC;

-- 2. Ingresos por categoría
SELECT categoria,
       TO_CHAR(SUM(total), 'FM999,999,999.00') AS total_ingresos,
       COUNT(*) AS cantidad_ventas
FROM ventas
WHERE cantidad > 0
GROUP BY categoria
ORDER BY SUM(total) DESC;

-- 3. Ventas sin NCF (errores fiscales)
SELECT COUNT(*) AS ventas_sin_ncf
FROM ventas
WHERE ncf IS NULL;