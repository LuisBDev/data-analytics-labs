-- Consultas de validación para la tabla DIM_FECHA en PostgreSQL
-- Ejecutar después de insertar los datos

-- 1. Verificar que la tabla existe
SELECT EXISTS (
    SELECT FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name = 'dim_fecha'
);

-- 2. Contar total de registros
SELECT COUNT(*) as total_registros FROM public.DIM_FECHA;

-- 3. Verificar rango de fechas
SELECT 
    MIN(Fecha) as fecha_minima, 
    MAX(Fecha) as fecha_maxima,
    MAX(Fecha) - MIN(Fecha) as dias_totales
FROM public.DIM_FECHA;

-- 4. Verificar distribución de días de semana
SELECT 
    Nombre_Dia_Semana,
    COUNT(*) as cantidad,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as porcentaje
FROM public.DIM_FECHA 
GROUP BY Dia_Semana, Nombre_Dia_Semana
ORDER BY Dia_Semana;





-- 7. Verificar distribución por años
SELECT 
    Anio,
    COUNT(*) as dias_en_anio,
    MIN(Fecha) as primer_dia,
    MAX(Fecha) as ultimo_dia
FROM public.DIM_FECHA 
GROUP BY Anio
ORDER BY Anio;

-- 8. Verificar que no hay duplicados en FechaKey
SELECT 
    'Duplicados en FechaKey' as validacion,
    COUNT(*) - COUNT(DISTINCT FechaKey) as duplicados
FROM public.DIM_FECHA;

-- 9. Verificar estructura de FechaKey (debe ser YYYYMMDD)
SELECT 
    'FechaKeys con formato incorrecto' as validacion,
    COUNT(*) as registros_incorrectos
FROM public.DIM_FECHA 
WHERE 
    FechaKey::text != TO_CHAR(Fecha, 'YYYYMMDD');

-- 10. Muestra de los primeros 10 registros
SELECT 
    FechaKey,
    Fecha,
    Nombre_Dia_Semana,
    Nombre_Mes,
    Anio,
    Fin_Semana
FROM public.DIM_FECHA 
ORDER BY FechaKey
LIMIT 10;