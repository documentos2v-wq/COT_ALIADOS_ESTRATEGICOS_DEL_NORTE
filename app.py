import streamlit as st
from datetime import date

# Configuración de la página
st.set_page_config(
    page_title="Nueva Cotización",
    page_icon="📄",
    layout="wide"
)

# Estilos CSS personalizados para replicar la apariencia visual de la imagen
st.markdown("""
    <style>
    .main {
        background-color: #f0ede6;
    }
    h1 {
        color: #1a1a1a;
        font-weight: 700;
    }
    .stButton>button {
        background-color: #0066cc;
        color: white;
        border-radius: 4px;
    }
    .create-btn>button {
        background-color: #00aa00 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal y enlace de ayuda superior derecha
col_title, col_help = st.columns([6, 1])
with col_title:
    st.markdown("<h1>Nueva Cotización</h1>", unsafe_allow_html=True)
with col_help:
    st.markdown("<div style='text-align: right; padding-top: 15px;'><a href='#' target='_self'>Ayuda</a></div>", unsafe_allow_html=True)

# Sección superior: Datos de empresa / logotipo y fechas
col_logo, col_empresa, col_vacio, col_datos_izq = st.columns([1.2, 2.2, 0.3, 2.8])

with col_logo:
    st.markdown("""
        <div style="border: 2px dashed #b0b0b0; padding: 30px 10px; text-align: center; color: #777777; border-radius: 4px; background-color: #faf8f5; height: 130px; display: flex; align-items: center; justify-content: center;">
            + Añadir un logotipo
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    cliente = st.selectbox("Cliente:", ["Seleccione cliente...", "Cliente 1", "Cliente 2"], label_visibility="collapsed")
    # Para alinear la etiqueta visualmente como en la imagen
    st.markdown("<p style='margin-top: -30px; font-size: 14px; color: #333;'>Cliente:</p>", unsafe_allow_html=True)

with col_empresa:
    nombre_empresa = st.text_input("Nombre de la empresa", placeholder="Nombre de la empresa", label_visibility="collapsed")
    direccion_comercial = st.text_area("Dirección comercial", placeholder="Dirección comercial", height=85, label_visibility="collapsed")

with col_datos_izq:
    col_d1, col_d2 = st.columns([1, 1.3])
    with col_d1:
        st.markdown("<p style='margin-top: 8px;'>Fecha:</p>", unsafe_allow_html=True)
        st.markdown("<p style='margin-top: 16px;'>Nº de Cotización:</p>", unsafe_allow_html=True)
        st.markdown("<p style='margin-top: 16px;'>Condiciones de pago:</p>", unsafe_allow_html=True)
        st.markdown("<p style='margin-top: 16px;'>Vendedor:</p>", unsafe_allow_html=True)
    with col_d2:
        fecha_cot = st.date_input("Fecha", value=date(2026, 10, 30), label_visibility="collapsed")
        num_cot = st.text_input("Nº de Cotización", value="10001", label_visibility="collapsed")
        
        col_cp1, col_cp2 = st.columns([1.3, 1])
        with col_cp1:
            cond_pago = st.selectbox("Condiciones de pago", ["Pago en días", "Contado", "Crédito"], label_visibility="collapsed")
        with col_cp2:
            dias_pago = st.number_input("Días", value=30, label_visibility="collapsed")
            
        vendedor = st.selectbox("Vendedor", ["Opcional", "Vendedor 1", "Vendedor 2"], label_visibility="collapsed")

# Sección de direcciones de facturación y envío
col_fact, col_env = st.columns(2)
with col_fact:
    st.text("Dirección de facturación:")
    dir_facturacion = st.text_area("Dirección de facturación", placeholder="", height=70, label_visibility="collapsed")

with col_env:
    st.text("Dirección de envío:")
    dir_envio = st.text_area("Dirección de envío", placeholder="Déjelo en blanco si es igual que la dirección de facturación.", height=70, label_visibility="collapsed")

st.write("---")

# Cabecera de la tabla de artículos (Estilo barra marrón oscura)
st.markdown("""
    <div style="background-color: #736b63; padding: 10px; color: white; font-weight: bold; display: flex; justify-content: space-between; border-radius: 4px 4px 0 0; font-size: 14px;">
        <span style="flex: 0.8;">Cant. ▾</span>
        <span style="flex: 1.5;">Cód. artículo ▾</span>
        <span style="flex: 3.5;">Descripción ▾</span>
        <span style="flex: 1.5;">Precio unit... ▾</span>
        <span style="flex: 1.5;">Impuesto ▾</span>
        <span style="flex: 1.5;">Total ▾</span>
    </div>
""", unsafe_allow_html=True)

# Fila interactiva de artículos
col_t1, col_t2, col_t3, col_t4, col_t5, col_t6, col_t7 = st.columns([0.8, 1.5, 3.5, 1.5, 1.5, 1.5, 0.4])

with col_t1:
    cantidad = st.number_input("Cant.", value=1, min_value=1, label_visibility="collapsed")
with col_t2:
    cod_articulo = st.text_input("Cód.", value="", placeholder="Opcional", label_visibility="collapsed")
with col_t3:
    descripcion = st.text_input("Desc", value="", placeholder="Descripción", label_visibility="collapsed")
with col_t4:
    precio_unit = st.text_input("Precio", value="PEN 0.00", label_visibility="collapsed")
with col_t5:
    impuesto = st.selectbox("Impuesto", ["IGV", "Exonerado", "INA"], label_visibility="collapsed")
with col_t6:
    total_fila = st.text_input("Total", value="PEN 0.00", label_visibility="collapsed")
with col_t7:
    st.markdown("<div style='padding-top: 8px; font-size: 18px; cursor: pointer;'>❌</div>", unsafe_allow_html=True)

st.write("")

# Botones inferiores de acción para artículos / descuentos / envíos
col_btn1, col_btn2, col_btn3, col_vacio2 = st.columns([1.5, 1.6, 1.5, 4.4])
with col_btn1:
    if st.button("+ Agregar artículo"):
        pass
with col_btn2:
    if st.button("+ Añadir descuento"):
        pass
with col_btn3:
    if st.button("+ Añadir envío"):
        pass

st.write("")

# Pestañas de notas y sección de totales a la derecha
col_notas, col_totales = st.columns([1.2, 1])

with col_notas:
    tab_pub, tab_priv, tab_pie = st.tabs(["Nota pública", "Nota privada", "Nota al pie"])
    with tab_pub:
        nota_pub = st.text_area("Nota pública", placeholder="", height=90, label_visibility="collapsed")
    with tab_priv:
        nota_priv = st.text_area("Nota privada", placeholder="", height=90, label_visibility="collapsed")
    with tab_pie:
        nota_pie = st.text_area("Nota al pie", placeholder="", height=90, label_visibility="collapsed")

with col_totales:
    st.markdown("""
        <div style="background-color: #f7f5f0; padding: 15px; border-radius: 5px;">
            <div style="display: flex; justify-content: space-between; padding-bottom: 8px; border-bottom: 1px solid #ddd;">
                <span style="font-weight: 500; color: #333;">Subtotal:</span>
                <span style="font-weight: 500; color: #333;">PEN 0.00</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding-top: 10px;">
                <span style="font-weight: bold; color: #111; font-size: 16px;">Total:</span>
                <span style="font-weight: bold; color: #111; font-size: 16px;">PEN 0.00</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.write("")

# Botones finales de comentarios y creación de cotización
col_com, col_space, col_borrar, col_crear = st.columns([1.5, 2.5, 1.2, 1.5])

with col_com:
    st.button("💬 Enviar comentarios")

with col_borrar:
    st.button("Borrar cotización")

with col_crear:
    st.button("Crear Cotización ▾", type="primary")
