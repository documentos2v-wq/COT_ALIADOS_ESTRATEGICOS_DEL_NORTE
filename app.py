import streamlit as st
from datetime import date
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

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

# Función para generar el PDF en memoria
def generar_pdf(nombre_empresa, num_cot, fecha_cot, cond_pago, dias_pago, vendedor, dir_facturacion, dir_envio, articulos, descuentos, envios, subtotal):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=15
    )
    normal_style = styles['Normal']
    
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
    
    # Totales
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
    st.markdown("""
        <div style="border: 2px dashed #b0b0b0; padding: 30px 10px; text-align: center; color: #777777; border-radius: 4px; background-color: #faf8f5; height: 130px; display: flex; align-items: center; justify-content: center;">
            + Añadir un logotipo
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    cliente = st.selectbox("Cliente:", ["Seleccione cliente...", "Cliente 1", "Cliente 2"], label_visibility="collapsed")
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

# Renderizar descuentos y envíos en el cálculo
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
