import streamlit as st
from datetime import date
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from PIL import Image as PILImage
import requests

# Configuración de la página
st.set_page_config(
    page_title="Nueva Cotización",
    page_icon="📄",
    layout="wide"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        background-color: #f0ede6;
    }
    h1 {
        color: #1a1a1a;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar el estado de la sesión para los elementos dinámicos
if 'articulos' not in st.session_state:
    st.session_state.articulos = [{'cant': 1, 'cod': '', 'desc': '', 'precio': 0.0, 'impuesto': 'IGV'}]

if 'descuentos' not in st.session_state:
    st.session_state.descuentos = []

if 'envios' not in st.session_state:
    st.session_state.envios = []

if 'ruc_input' not in st.session_state:
    st.session_state.ruc_input = ""

if 'empresa_nombre' not in st.session_state:
    st.session_state.empresa_nombre = ""

if 'empresa_dir' not in st.session_state:
    st.session_state.empresa_dir = ""

# Función para consultar datos básicos de RUC en Perú (API pública o simulación rápida)
def consultar_ruc(ruc):
    # Puedes conectar aquí tu API preferida de RUC o DNI (ej: ApisNet, Facturalo, etc.)
    # Por ahora realizamos una validación estándar y enlace directo de apoyo
    if len(ruc) == 11 and ruc.isdigit():
        # Ejemplo de consulta pública estándar de SUNAT vía enlace web directo
        return True
    return False

# Función para generar el PDF en memoria con soporte para logotipo
def generar_pdf(logo_file, nombre_empresa, num_cot, fecha_cot, cond_pago, dias_pago, vendedor, dir_facturacion, dir_envio, articulos, descuentos, envios, subtotal):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=10
    )
    normal_style = styles['Normal']
    
    # Agregar logotipo al PDF si existe
    if logo_file is not None:
        try:
            logo_img = PILImage.open(logo_file)
            img_buffer = BytesIO()
            logo_img.save(img_buffer, format="PNG")
            img_buffer.seek(0)
            story.append(RLImage(img_buffer, width=100, height=45))
            story.append(Spacer(1, 10))
        except Exception:
            pass

    # Cabecera
    story.append(Paragraph("<b>COTIZACIÓN</b>", title_style))
    story.append(Paragraph(f"<b>Empresa:</b> {nombre_empresa or 'N/A'}", normal_style))
    story.append(Paragraph(f"<b>Nº de Cotización:</b> {num_cot}", normal_style))
    story.append(Paragraph(f"<b>Fecha:</b> {fecha_cot.strftime('%d/%m/%Y')}", normal_style))
    story.append(Paragraph(f"<b>Condiciones de pago:</b> {cond_pago} ({dias_pago} días)", normal_style))
    story.append(Paragraph(f"<b>Vendedor:</b> {vendedor}", normal_style))
    story.append(Spacer(1, 15))
    
    # Direcciones
    story.append(Paragraph(f"<b>Dirección de facturación:</b> {dir_facturacion or 'N/A'}", normal_style))
    story.append(Paragraph(f"<b>Dirección de envío:</b> {dir_envio or 'Igual a la de facturación'}", normal_style))
    story.append(Spacer(1, 15))
    
    # Tabla de Artículos
    data = [["Cant.", "Cód.", "Descripción", "Precio Unit.", "Impuesto", "Total"]]
    for art in articulos:
        tot_fila = art['cant'] * art['precio']
        data.append([
            str(art['cant']),
            art['cod'] or '-',
            art['desc'] or '-',
            f"PEN {art['precio']:.2f}",
            art['impuesto'],
            f"PEN {tot_fila:.2f}"
        ])
        
    for desc in descuentos:
        data.append(["-", "Descuento", desc['desc'], f"-PEN {desc['monto']:.2f}", "-", f"-PEN {desc['monto']:.2f}"])
        
    for env in envios:
        data.append(["-", "Envío", env['desc'], f"PEN {env['monto']:.2f}", "-", f"PEN {env['monto']:.2f}"])
        
    t = Table(data, colWidths=[40, 60, 200, 80, 60, 80])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#736b63')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7f5f0')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d3d3d3')),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph(f"<b>Total a pagar: PEN {subtotal:.2f}</b>", ParagraphStyle('TotalStyle', parent=normal_style, fontSize=14, alignment=2)))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# Título principal y enlace de ayuda superior derecha
col_title, col_help = st.columns([6, 1])
with col_title:
    st.markdown("<h1>Nueva Cotización</h1>", unsafe_allow_html=True)
with col_help:
    st.markdown("<div style='text-align: right; padding-top: 15px;'><a href='#' target='_self'>Ayuda</a></div>", unsafe_allow_html=True)

# Sección superior: Datos de empresa / logotipo y fechas
col_logo, col_empresa, col_vacio, col_datos_izq = st.columns([1.2, 2.2, 0.3, 2.8])

with col_logo:
    uploaded_logo = st.file_uploader("+ Añadir un logotipo", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
    if uploaded_logo is not None:
        st.image(uploaded_logo, width=120, caption="Logotipo cargado")
    
    st.write("")
    cliente = st.selectbox("Cliente:", ["Seleccione cliente...", "Cliente 1", "Cliente 2"], label_visibility="collapsed")
    st.markdown("<p style='margin-top: -30px; font-size: 14px; color: #333;'>Cliente:</p>", unsafe_allow_html=True)

with col_empresa:
    # ── NUEVA SECCIÓN DE BÚSQUEDA RUC Y ENLACE DIRECTO SUNAT ──
    st.markdown("<p style='font-size: 13px; font-weight: bold; margin-bottom: 2px;'>Búsqueda RUC / SUNAT:</p>", unsafe_allow_html=True)
    
    col_r1, col_r2 = st.columns([2, 1])
    with col_r1:
        st.session_state.ruc_input = st.text_input("RUC", value=st.session_state.ruc_input, placeholder="Nº de RUC (11 dígitos)", label_visibility="collapsed")
    with col_r2:
        # Enlace directo a la consulta oficial de SUNAT
        sunat_url = f"https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias?accion=consPorRuc&nrbRuc={st.session_state.ruc_input}" if len(st.session_state.ruc_input) == 11 else "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias"
        st.markdown(f"<a href='{sunat_url}' target='_blank' style='display:inline-block; background-color:#0066cc; color:white; padding:6px 10px; border-radius:4px; text-decoration:none; font-size:12px; text-align:center; width:100%;'>🔍 Ver en SUNAT</a>", unsafe_allow_html=True)

    nombre_empresa = st.text_input("Nombre de la empresa", value=st.session_state.empresa_nombre, placeholder="Nombre de la empresa o Razón Social", label_visibility="collapsed")
    direccion_comercial = st.text_area("Dirección comercial", value=st.session_state.empresa_dir, placeholder="Dirección comercial", height=70, label_visibility="collapsed")

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

# Cabecera de la tabla de artículos
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

# Renderizar filas de artículos dinámicamente
subtotal_general = 0.0

for i, art in enumerate(st.session_state.articulos):
    col_t1, col_t2, col_t3, col_t4, col_t5, col_t6, col_t7 = st.columns([0.8, 1.5, 3.5, 1.5, 1.5, 1.5, 0.4])
    
    with col_t1:
        st.session_state.articulos[i]['cant'] = st.number_input(f"Cant_{i}", value=art['cant'], min_value=1, label_visibility="collapsed")
    with col_t2:
        st.session_state.articulos[i]['cod'] = st.text_input(f"Cod_{i}", value=art['cod'], placeholder="Opcional", label_visibility="collapsed")
    with col_t3:
        st.session_state.articulos[i]['desc'] = st.text_input(f"Desc_{i}", value=art['desc'], placeholder="Descripción", label_visibility="collapsed")
    with col_t4:
        st.session_state.articulos[i]['precio'] = st.number_input(f"Precio_{i}", value=art['precio'], min_value=0.0, format="%.2f", label_visibility="collapsed")
    with col_t5:
        st.session_state.articulos[i]['impuesto'] = st.selectbox(f"Imp_{i}", ["IGV", "Exonerado", "INA"], index=["IGV", "Exonerado", "INA"].index(art['impuesto']), label_visibility="collapsed")
    
    total_fila = st.session_state.articulos[i]['cant'] * st.session_state.articulos[i]['precio']
    subtotal_general += total_fila
    
    with col_t6:
        st.markdown(f"<div style='padding-top: 8px; font-weight: 500;'>PEN {total_fila:.2f}</div>", unsafe_allow_html=True)
    with col_t7:
        if len(st.session_state.articulos) > 1:
            if st.button("❌", key=f"del_art_{i}"):
                st.session_state.articulos.pop(i)
                st.rerun()

for desc in st.session_state.descuentos:
    subtotal_general -= desc['monto']

for env in st.session_state.envios:
    subtotal_general += env['monto']

st.write("")

# Botones inferiores de acción para artículos / descuentos / envíos
col_btn1, col_btn2, col_btn3, col_vacio2 = st.columns([1.5, 1.6, 1.5, 4.4])
with col_btn1:
    if st.button("+ Agregar artículo"):
        st.session_state.articulos.append({'cant': 1, 'cod': '', 'desc': '', 'precio': 0.0, 'impuesto': 'IGV'})
        st.rerun()
with col_btn2:
    if st.button("+ Añadir descuento"):
        st.session_state.descuentos.append({'desc': 'Descuento', 'monto': 0.0})
        st.rerun()
with col_btn3:
    if st.button("+ Añadir envío"):
        st.session_state.envios.append({'desc': 'Envío', 'monto': 0.0})
        st.rerun()

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
    st.markdown(f"""
        <div style="background-color: #f7f5f0; padding: 15px; border-radius: 5px;">
            <div style="display: flex; justify-content: space-between; padding-bottom: 8px; border-bottom: 1px solid #ddd;">
                <span style="font-weight: 500; color: #333;">Subtotal:</span>
                <span style="font-weight: 500; color: #333;">PEN {subtotal_general:.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding-top: 10px;">
                <span style="font-weight: bold; color: #111; font-size: 16px;">Total:</span>
                <span style="font-weight: bold; color: #111; font-size: 16px;">PEN {subtotal_general:.2f}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.write("")

# Botones finales de comentarios, borrado y descarga en PDF
col_com, col_space, col_borrar, col_crear = st.columns([1.5, 2.5, 1.2, 1.5])

with col_com:
    if st.button("💬 Enviar comentarios"):
        st.info("Formulario de comentarios abierto.")

with col_borrar:
    if st.button("Borrar cotización"):
        st.session_state.articulos = [{'cant': 1, 'cod': '', 'desc': '', 'precio': 0.0, 'impuesto': 'IGV'}]
        st.session_state.descuentos = []
        st.session_state.envios = []
        st.session_state.ruc_input = ""
        st.session_state.empresa_nombre = ""
        st.session_state.empresa_dir = ""
        st.rerun()

with col_crear:
    pdf_buffer = generar_pdf(
        uploaded_logo, nombre_empresa, num_cot, fecha_cot, cond_pago, dias_pago, 
        vendedor, dir_facturacion, dir_envio, 
        st.session_state.articulos, st.session_state.descuentos, st.session_state.envios, 
        subtotal_general
    )
    
    st.download_button(
        label="📥 Descargar PDF",
        data=pdf_button if 'pdf_button' in locals() else pdf_buffer,
        file_name=f"Cotizacion_{num_cot}.pdf",
        mime="application/pdf",
        type="primary"
    )
