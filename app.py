import streamlit as st
import json
import os
import random

ARCHIVO_BD = "biblioteca.json"

def cargar_bd():
    if not os.path.exists(ARCHIVO_BD):
        return {}
    with open(ARCHIVO_BD, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_bd(bd):
    with open(ARCHIVO_BD, "w", encoding="utf-8") as f:
        json.dump(bd, f, ensure_ascii=False, indent=4)

def normalizar_ejercicio(nombre):
    """Convierte el texto a minúsculas y ordena sus palabras alfabéticamente 
    para que 'pecho plano barra' y 'pecho barra plano' se consideren idénticos."""
    palabras = sorted(nombre.lower().strip().split())
    return " ".join(palabras)

st.title("🏋️‍♂️ Mi Biblioteca de Gimnasio")

tab1, tab2, tab3 = st.tabs(["➕ Añadir", "🎯 Generar", "📋 Ver"])
bd = cargar_bd()

with tab1:
    st.header("Añadir ejercicios")
    musculo = st.text_input("Músculo (ej: Pecho):").strip().capitalize()
    ejercicios = st.text_area("Ejercicios (uno por línea):")
    
    if st.button("Guardar"):
        if musculo and ejercicios:
            if musculo not in bd:
                bd[musculo] = []
            
            nuevos = [e.strip() for e in ejercicios.split("\n") if e.strip()]
            agregados = 0
            omitidos = 0
            
            # Creamos una lista con las versiones normalizadas de los que ya tenemos guardados
            existentes_normalizados = [normalizar_ejercicio(e) for e in bd[musculo]]
            
            for ej in nuevos:
                ej_norm = normalizar_ejercicio(ej)
                if ej_norm not in existentes_normalizados:
                    bd[musculo].append(ej)
                    existentes_normalizados.append(ej_norm)  # Para evitar duplicados dentro del mismo portapapeles
                    agregados += 1
                else:
                    omitidos += 1
                    
            guardar_bd(bd)
            st.success(f"¡Guardado! {agregados} añadidos, {omitidos} omitidos por estar repetidos.")
        else:
            st.warning("Rellena ambos campos.")

with tab2:
    st.header("Generar rutina")
    if not bd:
        st.info("Añade ejercicios primero.")
    else:
        sel = st.multiselect("¿Qué entrenas?", list(bd.keys()))
        num = st.slider("Ejercicios por músculo", 1, 5, 3)
        if st.button("Crear rutina"):
            if sel:
                for m in sel:
                    st.subheader(f"💪 {m}")
                    ej_list = random.sample(bd[m], min(num, len(bd[m])))
                    for i, e in enumerate(ej_list, 1):
                        st.write(f"{i}. {e}")
            else:
                st.warning("Selecciona un músculo.")

with tab3:
    st.header("Biblioteca")
    if not bd:
        st.write("Vacía.")
    else:
        for m, ejs in bd.items():
            with st.expander(f"{m} ({len(ejs)})"):
                for e in ejs:
                    st.write(f"- {e}")