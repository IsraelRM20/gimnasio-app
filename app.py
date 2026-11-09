import streamlit as st
import json
import os
import random

ARCHIVO_BD = "biblioteca.json"
CARPETA_IMAGENES = "imagenes"
PASSWORD_ADMIN = "47392954-Mm"  # Contraseña de administrador

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

os.makedirs(CARPETA_IMAGENES, exist_ok=True)

# Configuración de página limpia y ancha
st.set_page_config(page_title="GymFit - Disciplina > Motivación", layout="wide")

# --- DISEÑO PROFESIONAL CON CSS (Estética oscura, tipografía moderna y banner grande) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    .hero-container {
        text-align: center;
        padding: 10px 0 20px 0;
    }
    
    .hero-title {
        font-weight: 800;
        font-size: 2.8rem;
        letter-spacing: -1px;
        margin-bottom: 5px;
        color: #ffffff;
    }
    
    .hero-subtitle {
        font-weight: 600;
        font-size: 1.3rem;
        color: #00d2ff;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABECERA ESTILO BANNER PROFESIONAL ---
st.markdown('<div class="hero-container">', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Mi Biblioteca de Gimnasio</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Disciplina > Motivación</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Imagen principal centrada y grande ocupando el ancho visual clave
st.image(URL_IMAGEN_CABECERA, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📋 Ver biblioteca", "🎯 Generar rutina", "➕ Añadir ejercicios"])
bd = cargar_bd()

with tab1:
    st.markdown("### Biblioteca de Ejercicios")
    if not bd:
        st.info("La biblioteca está vacía. Añade ejercicios desde la administración.")
    else:
        for m, ejs in bd.items():
            # Sin emojis molestos, limpio y directo con el nombre del músculo en mayúscula elegante
            with st.expander(f"{m.upper()} — ({len(ejs)} ejercicios)"):
                for e in ejs:
                    if isinstance(e, dict):
                        nombre = e.get("nombre", "")
                        img_path = e.get("imagen", "")
                        st.markdown(f"**{nombre}**")
                        if img_path:
                            if img_path.startswith("http") or os.path.exists(img_path):
                                st.image(img_path, width=350)
                            else:
                                st.write("(Imagen no encontrada)")
                    else:
                        st.write(f"- {e}")
                    st.divider()

with tab2:
    st.markdown("### Generador de Rutinas")
    if not bd:
        st.info("Añade ejercicios primero.")
    else:
        sel = st.multiselect("¿Qué grupos musculares entrenas hoy?", list(bd.keys()))
        if sel:
            num = st.slider("Ejercicios por grupo muscular", 1, min(10, len(bd[sel[0]])), 3)
        else:
            num = 3
            
        if st.button("Generar Rutina Óptima"):
            if sel:
                for m in sel:
                    st.markdown(f"#### ⚡ {m.upper()}")
                    ej_list = random.sample(bd[m], min(num, len(bd[m])))
                    for i, e in enumerate(ej_list, 1):
                        nombre = e.get("nombre", "") if isinstance(e, dict) else e
                        img_path = e.get("imagen", "") if isinstance(e, dict) else ""
                        st.write(f"**{i}. {nombre}**")
                        if img_path:
                            if img_path.startswith("http") or os.path.exists(img_path):
                                st.image(img_path, width=300)
            else:
                st.warning("Selecciona al menos un músculo.")

with tab3:
    st.markdown("### Zona de Administración")
    password = st.text_input("Introduce la contraseña de administrador:", type="password")
    
    if password == PASSWORD_ADMIN:
        st.success("Acceso autorizado.")
        musculo = st.text_input("Grupo Muscular (ej: Pecho, Espalda):").strip().capitalize()
        ejercicios_texto = st.text_area("Ejercicios (uno por línea):")
        
        archivo_imagen = st.file_uploader("Sube la imagen del ejercicio (opcional):", type=["jpg", "png", "jpeg"])
        
        if st.button("Guardar en la Base de Datos"):
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
                st.success(f"¡Éxito! {agregados} ejercicios añadidos, {omitidos} omitidos por estar duplicados.")
            else:
                st.warning("Por favor, rellena el grupo muscular y los ejercicios.")
    elif password:
        st.error("Contraseña incorrecta.")
    else:
        st.info("Introduce tu contraseña para desbloquear el panel de administración.")
