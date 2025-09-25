-- Script refactorizado para PostgreSQL
-- Definición de tabla para dimensión de fechas

-- Crear tabla DIM_FECHA si no existe
CREATE TABLE IF NOT EXISTS public.DIM_FECHA (
    FechaKey INT NOT NULL PRIMARY KEY,
    Fecha DATE NOT NULL,
    Dia_Semana SMALLINT NOT NULL,
    Nombre_Dia_Semana VARCHAR(20) NOT NULL,
    Dia_Mes SMALLINT NOT NULL,
    Dia_Anio SMALLINT NOT NULL,
    Nombre_Mes VARCHAR(20) NOT NULL,
    Mes_Anio SMALLINT NOT NULL,
    Semana_Anio SMALLINT NOT NULL,
    Anio SMALLINT NOT NULL,
    Bimestre SMALLINT NOT NULL,
    Trimestre SMALLINT NOT NULL,
    Cuatrimestre SMALLINT NOT NULL,
    Semestre SMALLINT NOT NULL,
    Fin_Semana BOOLEAN NOT NULL
);

-- Crear índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_dim_fecha_fecha ON public.DIM_FECHA(Fecha);
CREATE INDEX IF NOT EXISTS idx_dim_fecha_anio ON public.DIM_FECHA(Anio);
CREATE INDEX IF NOT EXISTS idx_dim_fecha_mes ON public.DIM_FECHA(Mes_Anio);

-- Comentarios en la tabla y campos
COMMENT ON TABLE public.DIM_FECHA IS 'Tabla de dimensión de fechas para análisis temporal';
COMMENT ON COLUMN public.DIM_FECHA.FechaKey IS 'Clave primaria en formato YYYYMMDD';
COMMENT ON COLUMN public.DIM_FECHA.Fecha IS 'Fecha en formato DATE';
COMMENT ON COLUMN public.DIM_FECHA.Dia_Semana IS 'Día de la semana (1=Domingo, 7=Sábado)';
COMMENT ON COLUMN public.DIM_FECHA.Fin_Semana IS 'Indica si es fin de semana (TRUE/FALSE)';
