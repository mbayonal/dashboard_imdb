# IMDb Rating Classification Dashboard

**Dashboard interactivo para predicción de categoría de rating de películas**

Proyecto MLOps - Grupo 21

## 📋 Descripción

Dashboard web desarrollado con Streamlit que proporciona una interfaz intuitiva para predecir la categoría de rating de películas de IMDb (Poor, Average, Good, Excellent) utilizando el modelo ML desplegado en la API.

## 🎨 Características

- **Interfaz intuitiva**: Formulario simple para ingresar características de películas
- **Visualización en tiempo real**: Resultados con métricas y código de colores
- **Conexión con API**: Integración transparente con el servicio FastAPI
- **Configuración flexible**: URL de API configurable desde el sidebar
- **Métricas del modelo**: Visualización de métricas de desempeño

## 🏗️ Arquitectura

```
.
├── app.py               # Aplicación Streamlit principal
├── requirements.txt     # Dependencias Python
└── .venv/              # Entorno virtual (local)
```

## 🎯 Funcionalidades

### Panel Principal
- **Año de Lanzamiento**: Año de estreno de la película (1900-2030)
- **Duración**: Runtime en minutos (1-500)
- **Número de Votos**: Cantidad de votos recibidos
- **Rating Promedio**: Rating en escala 1-10
- **Categoría de Duración**: Short, Standard, Long, Very Long
- **Popularidad**: Very Low, Low, Medium, High

### Sidebar
- **Configuración de API**: URL del servicio FastAPI
- **Prueba de conexión**: Verificar estado de la API
- **Info del modelo**: Ver métricas y metadata
- **Categorías de Rating**: Documentación de las categorías

### Visualización de Resultados
- **Categoría predicha**: Con emoji indicador
- **Confianza**: Porcentaje de confianza del modelo
- **Modelo usado**: Identificador del algoritmo
- **Métricas del modelo**: Accuracy, F1-score, etc.

## 🚀 Instalación y Uso

### Requisitos Previos
- Python 3.12+
- API REST corriendo en http://localhost:8000 (o configurar otra URL)

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/dashboard_imdb.git
cd dashboard_imdb
```

### 2. Crear entorno virtual e instalar dependencias
```bash
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Ejecutar el dashboard
```bash
# Por defecto en puerto 8501
streamlit run app.py

# Personalizar puerto
streamlit run app.py --server.port 8502
```

### 4. Acceder al dashboard
Abre tu navegador en: http://localhost:8501

## 🔧 Configuración

### Variables de Entorno

```bash
# URL de la API (opcional)
export API_URL=http://localhost:8000
```

### Configuración en la UI

También puedes configurar la URL de la API directamente desde el sidebar de la aplicación.

## 📊 Ejemplo de Uso

1. **Ingresar características de la película**:
   - Año: 2020
   - Duración: 120 minutos
   - Votos: 1000
   - Rating promedio: 7.5
   - Categoría de duración: Standard (90-120m)
   - Popularidad: Low

2. **Click en "Predecir"**

3. **Ver resultados**:
   - Categoría: 🟢 Good
   - Confianza: 98.76%
   - Modelo: logistic_regression

## 🎨 Capturas de Pantalla

### Interfaz Principal
El dashboard muestra un formulario limpio con todos los campos necesarios organizados en tres columnas.

### Resultados
Los resultados se muestran con código de colores:
- 🔴 **Poor**: Rating bajo
- 🟡 **Average**: Rating promedio
- 🟢 **Good**: Buen rating
- 🌟 **Excellent**: Rating excelente

## 🔗 Integración con API

El dashboard se comunica con la API REST mediante requests HTTP:

```python
import requests

# Endpoint de predicción
url = "http://localhost:8000/predict"

# Payload con características
payload = {
    "movies": [{
        "startYear": 2020.0,
        "runtimeMinutes": 120.0,
        "numVotes": 1000.0,
        "averageRating": 7.5,
        "runtime_category": "Standard (90-120m)",
        "popularity": "Low"
    }]
}

# Realizar predicción
response = requests.post(url, json=payload)
result = response.json()
```

## 📦 Dependencias Principales

- `streamlit==1.38.0` - Framework de dashboard
- `requests==2.32.3` - Cliente HTTP
- `pandas==2.2.2` - Manipulación de datos

## 🐳 Docker (Opcional)

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
# Build
docker build -t imdb-rating-dashboard .

# Run
docker run -p 8501:8501 -e API_URL=http://api:8000 imdb-rating-dashboard
```

## 🛠️ Desarrollo

### Estructura del Código

```python
# Configuración de página
st.set_page_config(...)

# Sidebar con configuración
with st.sidebar:
    # Configuración de API
    # Botones de prueba
    # Documentación

# Formulario principal
col1, col2, col3 = st.columns(3)
# Campos de entrada...

# Botón de predicción
if predict_btn:
    # Preparar payload
    # Llamar a API
    # Mostrar resultados
```

## 🧪 Pruebas

### Probar Conexión con API
1. Abrir el dashboard
2. En el sidebar, click en "🔍 Probar Conexión"
3. Verificar el mensaje de éxito

### Probar Predicción
1. Llenar el formulario con datos de prueba
2. Click en "🔮 Predecir"
3. Verificar que se muestren los resultados

## 🚨 Troubleshooting

### Error de Conexión con API
- Verificar que la API esté corriendo: `curl http://localhost:8000/health`
- Revisar la URL configurada en el sidebar
- Verificar que no haya firewalls bloqueando el puerto

### Error al Cargar el Dashboard
- Verificar que todas las dependencias estén instaladas
- Revisar los logs de Streamlit en la consola
- Asegurarse de que el puerto 8501 esté disponible

## 👥 Equipo - Grupo 21

- **Luis Felipe González** - Data Manager/MLOps
- **Daniel Ricardo Marín** - Data Scientist
- **Manuel Alejandro Bayona** - Cloud Engineer
- **Fabián Jiménez** - BI Analyst (Lead Dashboard)

## 📄 Licencia

Este proyecto es parte del curso de MLOps - MIAD Universidad de los Andes.

## 🔗 Repositorios Relacionados

- [Modelo y Pipeline](https://github.com/mbayonal/sentiment_classification_model) - Entrenamiento y DVC
- [API REST](https://github.com/mbayonal/api_imdb) - Servicio de predicción con FastAPI
