#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IMDb Rating Category Classification Dashboard

Predict movie rating category (Poor, Average, Good, Excellent)
from movie features using ML models.
"""

import os
import requests
import streamlit as st
import pandas as pd

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="IMDb Rating Classifier",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎬 IMDb Rating Category Classifier")
st.caption("Predice la categoría de rating de una película a partir de sus características")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuración")
    api_url = st.text_input("API URL", value=API_URL, help="Endpoint de la API FastAPI")
    
    st.markdown("---")
    
    if st.button("🔍 Probar Conexión", use_container_width=True):
        try:
            r = requests.get(f"{api_url}/health", timeout=5)
            if r.status_code == 200:
                health = r.json()
                if health.get("status") == "healthy":
                    st.success("✅ API funcionando correctamente")
                else:
                    st.warning(f"⚠️ Estado: {health.get('status')}")
            else:
                st.error(f"❌ Error: {r.status_code}")
        except Exception as e:
            st.error(f"❌ Error: {e}")
    
    if st.button("📊 Info del Modelo", use_container_width=True):
        try:
            r = requests.get(f"{api_url}/model-info", timeout=5)
            if r.status_code == 200:
                info = r.json()
                st.json(info)
        except Exception as e:
            st.error(f"Error: {e}")
    
    st.markdown("---")
    st.markdown("### 📋 Categorías de Rating")
    st.markdown("""
    - **Poor**: Rating < 4
    - **Average**: Rating 4-6
    - **Good**: Rating 6-8
    - **Excellent**: Rating > 8
    """)

# Main content
st.subheader("📝 Ingresar Características de la Película")

col1, col2, col3 = st.columns(3)

with col1:
    start_year = st.number_input(
        "Año de Lanzamiento",
        min_value=1900,
        max_value=2030,
        value=2020,
        step=1,
        help="Año en que se estrenó la película"
    )
    
    runtime_minutes = st.number_input(
        "Duración (minutos)",
        min_value=1,
        max_value=500,
        value=120,
        step=1,
        help="Duración de la película en minutos"
    )

with col2:
    num_votes = st.number_input(
        "Número de Votos",
        min_value=0,
        max_value=10000000,
        value=1000,
        step=100,
        help="Cantidad de votos recibidos"
    )
    
    average_rating = st.number_input(
        "Rating Promedio (1-10)",
        min_value=1.0,
        max_value=10.0,
        value=7.5,
        step=0.1,
        help="Rating promedio de la película"
    )

with col3:
    runtime_category = st.selectbox(
        "Categoría de Duración",
        options=[
            "Short (<60m)",
            "Standard (60-90m)",
            "Standard (90-120m)",
            "Long (120-180m)",
            "Very Long (>180m)"
        ],
        index=2,
        help="Categoría basada en la duración"
    )
    
    popularity = st.selectbox(
        "Popularidad",
        options=["Very Low", "Low", "Medium", "High"],
        index=1,
        help="Nivel de popularidad basado en votos"
    )

st.markdown("---")

col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])

with col_btn1:
    predict_btn = st.button("🔮 Predecir", type="primary", use_container_width=True)

with col_btn2:
    clear_btn = st.button("🗑️ Limpiar", use_container_width=True)

if clear_btn:
    st.rerun()

if predict_btn:
    # Prepare payload
    movie_data = {
        "startYear": float(start_year),
        "runtimeMinutes": float(runtime_minutes),
        "numVotes": float(num_votes),
        "averageRating": float(average_rating),
        "runtime_category": runtime_category,
        "popularity": popularity
    }
    
    payload = {"movies": [movie_data]}
    
    with st.spinner("Prediciendo..."):
        try:
            r = requests.post(f"{api_url}/predict", json=payload, timeout=10)
            
            if r.status_code == 200:
                data = r.json()
                prediction = data["predictions"][0]
                
                st.markdown("---")
                st.subheader("📊 Resultado de la Predicción")
                
                col_res1, col_res2, col_res3 = st.columns([1, 1, 1])
                
                with col_res1:
                    rating_cat = prediction["rating_category"]
                    
                    # Color coding
                    color_map = {
                        "Poor": "🔴",
                        "Average": "🟡",
                        "Good": "🟢",
                        "Excellent": "🌟"
                    }
                    
                    icon = color_map.get(rating_cat, "⚪")
                    st.metric(
                        label="Categoría Predicha",
                        value=f"{icon} {rating_cat}"
                    )
                
                with col_res2:
                    if prediction.get("confidence"):
                        conf = prediction["confidence"] * 100
                        st.metric(
                            label="Confianza",
                            value=f"{conf:.2f}%"
                        )
                
                with col_res3:
                    st.metric(
                        label="Modelo Usado",
                        value=data.get("model_name", "N/A")
                    )
                
                # Model metrics
                if data.get("model_metrics"):
                    st.markdown("### 📈 Métricas del Modelo")
                    metrics = data["model_metrics"]
                    
                    metric_cols = st.columns(len(metrics))
                    for i, (key, value) in enumerate(metrics.items()):
                        with metric_cols[i]:
                            st.metric(key.replace("_", " ").title(), f"{value:.4f}")
                
                # Show full response
                with st.expander("🔍 Ver Respuesta Completa"):
                    st.json(data)
                
            else:
                st.error(f"❌ Error de la API ({r.status_code}): {r.text}")
        
        except requests.exceptions.Timeout:
            st.error("⏱️ Timeout: La API no respondió a tiempo")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Error de conexión: No se pudo conectar con la API")
        except Exception as e:
            st.error(f"❌ Error: {e}")

st.markdown("---")

# Footer
col_footer1, col_footer2, col_footer3 = st.columns(3)
with col_footer1:
    st.caption("👥 Grupo 21")
with col_footer2:
    st.caption("🎬 IMDb Rating Classification")
with col_footer3:
    st.caption("🚀 MLOps Project")
