## Requisitos previos

Para ejecutar los ejercicios se necesita:

- Un proyecto de **Microsoft Foundry** con un agente creado.
- Un entorno Linux, como **GitHub Codespaces**.
- **Python** y el gestor de dependencias **uv**.
- **Azure Developer CLI (`azd`)**, para autenticar los scripts que utilizan `AzureDeveloperCliCredential`.
- Permisos de acceso al proyecto de Foundry.

Para las evaluaciones continuas, la identidad administrada del proyecto debe tener los permisos necesarios sobre Foundry, Application Insights y Log Analytics.

## Preparación del entorno

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd AMAIA-Agent-evaluation
```

### 2. Instalar uv

Si no está instalado:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Comprobar la instalación:

```bash
uv --version
```

### 3. Instalar las dependencias de Python

```bash
uv sync
```

Este comando crea el entorno virtual `.venv` e instala las dependencias definidas en `pyproject.toml` y `uv.lock`.

### 4. Activar el entorno virtual

En Linux o GitHub Codespaces:

```bash
source .venv/bin/activate
```

Para comprobar que está activo, el nombre del entorno aparecerá al principio de la terminal.

Para desactivarlo:

```bash
deactivate
```

**Nota:** activar el entorno virtual es opcional si se ejecutan los scripts mediante `uv run`, ya que `uv` utiliza automáticamente el entorno del proyecto.


### 6. Instalar Azure Developer CLI (azd)

En Linux:

```bash
curl -fsSL https://aka.ms/install-azd.sh | bash
```

Comprobar:

```bash
azd version
```

### 7. Iniciar sesión en Azure


Autenticarse con Azure Developer CLI:

```bash
azd auth login --use-device-code
```


### 8. Configurar las variables de entorno

Crear un archivo `.env` en la raíz del repositorio.

Configurar el endpoint del proyecto Foundry, el nombre del agente, los identificadores de Azure y las demás variables utilizadas por los scripts.

El archivo `.env` debe estar incluido en `.gitignore` para evitar publicar información de configuración privada.


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