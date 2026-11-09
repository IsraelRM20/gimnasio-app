import streamlit as st
import json
import os
import random

ARCHIVO_BD = "biblioteca.json"
CARPETA_IMAGENES = "imagenes"
PASSWORD_ADMIN = "47392954-Mm"  # ¡Cámbiala por una segura si quieres!

# --- URL DE LA IMAGEN DE CABECERA ---
URL_IMAGEN_CABECERA = "https://github.com/IsraelRM20/gimnasio-app/blob/main/Zancada%20intensa%20con%20mancuernas.png?raw=true" 

def cargar_bd():
    if not os.path.exists(ARCHIVO_BD):
        return {}
    with open(ARCHIVO_BD, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def guardar_bd(bd):
    with open(ARCHIVO_BD, "w", encoding="utf-8") as f:
        json.dump(bd, f, ensure_ascii=False, indent=4)

def normalizar_ejercicio(nombre):
    palabras = sorted(nombre.lower().strip().split())
    return " ".join(palabras)

# Asegurar carpetas
os.makedirs(CARPETA_IMAGENES, exist_ok=True)

# --- CONFIGURACIÓN DE PÁGINA Y CABECERA PERSONALIZADA ---
st.set_page_config(page_title="Mi Biblioteca de Gimnasio - Motivación", layout="wide")

# Cabecera con imagen y frase
col1, col2 = st.columns([1, 2])
with col1:
    st.image(URL_IMAGEN_CABECERA, width=150)
with col2:
    st.title("🏋️‍♂️ Mi Biblioteca de Gimnasio")
    st.markdown("## Disciplina > Motivación", help="El secreto del éxito.")

st.divider()

tab1, tab2, tab3 = st.tabs(["📋 Ver biblioteca", "🎯 Generar rutina", "➕ Añadir ejercicios"])
bd = cargar_bd()

with tab1:
    st.header("Biblioteca de Ejercicios")
    if not bd:
        st.info("La biblioteca está vacía. Añade ejercicios desde la administración.")
    else:
        for m, ejs in bd.items():
            with st.expander(f"💪 {m} ({len(ejs)})"):
                for e in ejs:
                    if isinstance(e, dict):
                        nombre = e.get("nombre", "")
                        img_path = e.get("imagen", "")
                        st.markdown(f"### {nombre}")
                        if img_path:
                            if img_path.startswith("http") or os.path.exists(img_path):
                                st.image(img_path, width=300)
                            else:
                                st.write("(Imagen no encontrada)")
                    else:
                        st.write(f"- {e}")
                    st.divider()

with tab2:
    st.header("Generar rutina")
    if not bd:
        st.info("Añade ejercicios primero.")
    else:
        sel = st.multiselect("¿Qué entrenas hoy?", list(bd.keys()))
        if sel:
            num = st.slider("Ejercicios por músculo", 1, min(10, len(bd[sel[0]])), 3)
        else:
            num = 3
            
        if st.button("Crear rutina"):
            if sel:
                for m in sel:
                    st.subheader(f"💪 {m}")
                    ej_list = random.sample(bd[m], min(num, len(bd[m])))
                    for i, e in enumerate(ej_list, 1):
                        nombre = e.get("nombre", "") if isinstance(e, dict) else e
                        img_path = e.get("imagen", "") if isinstance(e, dict) else ""
                        st.write(f"**{i}. {nombre}**")
                        if img_path:
                            if img_path.startswith("http") or os.path.exists(img_path):
                                st.image(img_path, width=250)
            else:
                st.warning("Selecciona al menos un músculo.")

with tab3:
    st.header("Añadir ejercicios (Zona Restringida)")
    password = st.text_input("Introduce la contraseña de administrador:", type="password")
    
    if password == PASSWORD_ADMIN:
        st.success("Acceso concedido.")
        musculo = st.text_input("Músculo (ej: Pecho):").strip().capitalize()
        ejercicios_texto = st.text_area("Ejercicios (uno por línea):")
        
        archivo_imagen = st.file_uploader("Sube tu foto generada por IA (opcional):", type=["jpg", "png", "jpeg"])
        
        if st.button("Guardar en la BD"):
            if musculo and ejercicios_texto:
                if musculo not in bd:
                    bd[musculo] = []
                
                ruta_imagen_guardada = ""
                if archivo_imagen is not None:
                    ruta_archivo = os.path.join(CARPETA_IMAGENES, archivo_imagen.name)
                    with open(ruta_archivo, "wb") as f:
                        f.write(archivo_imagen.getbuffer())
                    ruta_imagen_guardada = ruta_archivo

                nuevos = [e.strip() for e in ejercicios_texto.split("\n") if e.strip()]
                agregados = 0
                omitidos = 0
                
                existentes_normalizados = []
                for e in bd[musculo]:
                    nom = e.get("nombre", "") if isinstance(e, dict) else e
                    existentes_normalizados.append(normalizar_ejercicio(nom))
                
                for ej in nuevos:
                    ej_norm = normalizar_ejercicio(ej)
                    if ej_norm not in existentes_normalizados:
                        nuevo_item = {"nombre": ej, "imagen": ruta_imagen_guardada}
                        bd[musculo].append(nuevo_item)
                        existentes_normalizados.append(ej_norm)
                        agregados += 1
                    else:
                        omitidos += 1
                        
                guardar_bd(bd)
                st.success(f"¡Guardado! {agregados} añadidos, {omitidos} omitidos por estar repetidos.")
            else:
                st.warning("Rellena el músculo y los ejercicios.")
    elif password:
        st.error("Contraseña incorrecta.")
    else:
        st.info("Introduce tu contraseña para desbloquear el formulario.")
