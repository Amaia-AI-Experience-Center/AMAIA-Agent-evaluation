# Evaluación de agentes de IA con Microsoft Foundry

Repositorio de ejemplos prácticos para evaluar la **calidad y la seguridad de agentes de inteligencia artificial** mediante Microsoft Foundry y Python.

Se incluyen dos ejercicios independientes:

1. **Evaluaciones continuas y monitorización:** seguimiento automático de la calidad de las respuestas de un agente.
2. **Red Teaming automatizado:** pruebas adversarias para detectar posibles debilidades de seguridad.

## Requisitos previos

- Un proyecto de Microsoft Foundry con un agente creado.
- Python y el gestor de dependencias [uv](https://docs.astral.sh/uv/).
- Azure CLI (`az`) y Azure Developer CLI (`azd`).
- Acceso al proyecto de Foundry y permisos para utilizar los recursos de evaluación.
- Para las evaluaciones continuas, acceso de lectura de la identidad administrada del proyecto a Application Insights y Log Analytics, además del rol **Foundry User** sobre Foundry.
- Para crear alertas, permisos para gestionar los recursos correspondientes de Azure Monitor.

## Preparación del entorno

Clonar el repositorio y acceder a su carpeta:

```bash
git clone <URL_DEL_REPOSITORIO>
cd AMAIA-Agent-evaluation
```

Instalar las dependencias:

```bash
uv sync
```

Iniciar sesión en Azure desde la terminal:

```bash
az login --use-device-code
azd auth login --use-device-code
```

Crear un archivo `.env` en la raíz del proyecto y configurar las variables utilizadas por los scripts, incluyendo el endpoint del proyecto Foundry y los identificadores de los recursos correspondientes.

El archivo `.env` es local y no debe subirse al repositorio.

## Ejercicio 1. Evaluaciones continuas y alertas

### Objetivo

Automatizar la evaluación de las respuestas de un agente para detectar posibles problemas de calidad, comportamiento o seguridad a lo largo del tiempo.

### ¿Cómo funciona?

El ejercicio utiliza las capacidades de evaluación de Microsoft Foundry para definir evaluadores y configurar evaluaciones periódicas a partir de las trazas del agente.

Se utilizan métricas relacionadas con aspectos como:

- Relevancia de las respuestas.
- Cumplimiento de la tarea.
- Resolución de la intención del usuario.
- Seguridad del contenido.

Los resultados pueden utilizarse para supervisar el comportamiento del agente y detectar degradaciones.

### Ejecutar la evaluación

```bash
uv run scripts/continuous_eval.py
```

El script configura la evaluación y su programación en Foundry.

### Configurar alertas con Azure Monitor

```bash
uv run scripts/continuous_eval_alert.py
```

Este segundo script configura la monitorización de los resultados mediante Azure Monitor, permitiendo generar alertas cuando se cumplen determinadas condiciones.

Las alertas dependen de que existan resultados de evaluación disponibles en los recursos de monitorización.

## Ejercicio 2. Red Teaming automatizado

### Objetivo

Comprobar cómo se comporta un agente cuando recibe entradas diseñadas para manipularlo, eludir sus instrucciones o provocar respuestas no deseadas.

A diferencia de una evaluación de calidad convencional, el Red Teaming busca identificar **posibles fallos de seguridad y resistencia frente a ataques adversarios**.

### ¿Cómo funciona?

El ejercicio utiliza Red Teaming automatizado de Microsoft Foundry para generar y ejecutar pruebas contra un agente existente.

Se prueban diferentes técnicas de ataque:

- **Baseline:** peticiones adversarias directas.
- **Flip:** reformulaciones de los ataques.
- **Base64:** contenido codificado para comprobar la resistencia del agente a intentos de evasión.

El sistema recoge las respuestas del agente y genera valoraciones automáticas para facilitar su análisis.

### Ejecutar el ejercicio

```bash
uv run scripts/red_team.py
```

El script inicia una evaluación de Red Teaming y permite consultar los identificadores de la evaluación y de su ejecución en Foundry.

### Interpretar los resultados

Los resultados permiten revisar las pruebas realizadas, las respuestas del agente y las valoraciones emitidas por los evaluadores.

Es importante analizar tanto las etiquetas **pass/fail** como las explicaciones y respuestas individuales. Una etiqueta automática no debe interpretarse por sí sola como una vulnerabilidad confirmada.

Los casos sospechosos deben revisarse antes de sacar conclusiones o proponer cambios en el agente.

## Estructura del proyecto

| Archivo | Descripción |
|---|---|
| `scripts/continuous_eval.py` | Configuración de evaluaciones continuas |
| `scripts/continuous_eval_alert.py` | Configuración de alertas en Azure Monitor |
| `scripts/red_team.py` | Ejecución de pruebas de Red Teaming |
| `pyproject.toml` | Configuración y dependencias del proyecto |
| `uv.lock` | Versiones bloqueadas de las dependencias |
| `.python-version` | Versión de Python utilizada |

## Consideraciones

Los ejercicios están pensados para entornos de desarrollo y pruebas con recursos de Azure configurados previamente.

Las evaluaciones pueden consumir recursos y generar costes asociados a los servicios de Azure utilizados.

No deben incluirse credenciales, datos personales ni información sensible en el repositorio o en los resultados compartidos.