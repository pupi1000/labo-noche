# OpenSpec breve - mejora del agente

## Problema
El agente actual no dispone de una herramienta para desglosar y comparar el desempeno de ventas de un producto especifico a traves de las diferentes regiones geograficas (La Paz, Cochabamba, Santa Cruz) en un trimestre dado. Ante una consulta como "¿Cual es el desempeno regional de Killa en Q3?", el agente no puede computar la region lider ni la variacion entre regiones.

## Cambio propuesto
Implementar y registrar la herramienta `comparar_regiones(producto: str, periodo: str = "Q3") -> dict` en `src/tsi_agent/student_extension.py` y exponerla en `src/tsi_agent/tool_registry.py`. La tool:
1. Filtra las ventas del dataset `data/ventas.csv` por trimestre (`periodo`) y nombre de `producto`.
2. Agrupa los ingresos y unidades por `region`.
3. Determina la `region_lider` con mayores ingresos.
4. Calcula la diferencia porcentual entre la region lider y la segunda region (`diferencia_pct_lider_vs_segundo`).
5. Devuelve la lista detallada de filas de evidencia (`filas`) e ingresos por region (`ingresos_por_region`).

## Criterios de aceptacion
- [x] La mejora es visible en la interfaz (timeline y respuesta final al consultar desempeno regional).
- [x] Existe al menos una prueba automatizada en `tests/test_student_extension.py`.
- [x] La traza permite verificar la ejecucion con argumentos y resultado en JSON.
- [x] `ruff check .` pasa sin errores.
- [x] `pytest -q` pasa con todas las pruebas en verde.
- [x] No se agregaron secretos al repositorio.

## Riesgos
- **Riesgo tecnico:** Consultas con nombres de producto inexistentes o periodos invalidos podrian causar errores de indice o agrupaciones vacias si no se validan los parametros. Se mitiga mediante validacion previa de parametros y normalizacion de cadenas.
- **Riesgo de seguridad / datos:** Asegurar que los datos del CSV se traten como fuente analitica sin ejecutar codigo dinamico ni concatenar entradas de usuario directamente en evaluaciones inseguras.

## Evidencia
- Consulta de demostracion: `Compara el desempeno regional de Killa en Q3.`
- Ruta de traza: `logs/` (archivo JSON generado durante la ejecucion en UI/runner).

