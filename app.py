from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import streamlit as st
import tempfile
import os

# Configuración de la página
st.set_page_config(
    page_title="Generador de Cotizaciones - HospiTech",
    page_icon="📄",
    layout="wide"
)

# Estilo visual moderno para Streamlit
st.markdown("""
    <style>
    .main-header {
        font-size: 24px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #A81C1C;
        color: white;
        font-weight: bold;
        width: 100%;
        border-radius: 8px;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #801313;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📋 Generador Profesional de Cotizaciones - B2G</p>', unsafe_allow_html=True)
st.markdown("Rellena los datos en las pestañas a continuación para generar tu cotización formal lista para descargar en PDF.")

with st.form("cotizacion_form"):
    tab1, tab2, tab3, tab4 = st.tabs(["🏢 1. Encabezado y Cliente", "📦 2. Ítems y Precios", "📝 3. Condiciones y Notas", "🏦 4. Bancos y Firmas"])

    with tab1:
        st.subheader("Información del Documento y Cliente")
        col1, col2 = st.columns(2)
        with col1:
            nro_coti = st.text_input("Código de Cotización", placeholder="Ej. COTI NT HOSPI-000970-2026")
            cliente_nombre = st.text_input("Cliente / Entidad Pública", placeholder="Ej. RED INTEGRADA DE SALUD PACIFICO NORTE")
            referencia = st.text_input("Referencia", placeholder="Ej. PEDIDO DE COMPRA")
        with col2:
            fecha_emision = st.text_input("Fecha de Emisión", placeholder="Ej. Lima, 15 de mayo del 2026")
            vendedor = st.text_input("Asesor Comercial (Venta)", placeholder="Ej. YOSELIN ACERO")
            celular_vendedor = st.text_input("Celular de Contacto", placeholder="Ej. 924367556 / 981622589")

    with tab2:
        st.subheader("Detalle de Productos o Servicios")
        st.markdown("Puedes agregar los ítems que requieras para tu cotización:")

        # Sistema dinámico de ítems usando session_state dentro de Streamlit form
        if 'num_items' not in st.session_state:
            st.session_state.num_items = 1

        # Botones para agregar o quitar filas de ítems de forma interactiva
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.form_submit_button("➕ Agregar otro ítem"):
                st.session_state.num_items += 1
        with col_btn2:
            if st.session_state.num_items > 1:
                if st.form_submit_button("➖ Quitar último ítem"):
                    st.session_state.num_items -= 1

        items_data = []
        for i in range(st.session_state.num_items):
            st.markdown(f"--- **Ítem {i+1}**")
            desc = st.text_area(f"Descripción Técnica - Ítems {i+1}", placeholder="Ej. CAJA DE BIOSEGURIDAD...", key=f"desc_{i}", height=90)
            c_col1, c_col2, c_col3 = st.columns(3)
            with c_col1:
                cant = st.number_input(f"Cantidad {i+1}", min_value=1.0, value=1.0, step=1.0, key=f"cant_{i}")
            with c_col2:
                p_u = st.number_input(f"Precio Unitario (S/) {i+1}", min_value=0.0, value=0.0, format="%.2f", key=f"p_u_{i}")
            with c_col3:
                und = st.text_input(f"Unidad {i+1}", value="UND", key=f"und_{i}")
            
            items_data.append({"desc": desc, "cant": cant, "p_u": p_u, "und": und})

    with tab3:
        st.subheader("Condiciones Comerciales y Notas")
        col6, col7 = st.columns(2)
        with col6:
            tiempo_entrega = st.text_input("Tiempo de Entrega", value="10 DÍAS CALENDARIOS contabilizado a partir del día siguiente de suscrito el contrato.")
            forma_pago = st.text_input("Forma de Pago", value="abono en cuenta interbancaria (CCI) crédito comercial")
        with col7:
            garantia = st.text_input("Garantía", value="(12) meses a partir de la fecha de entrega y exclusivamente contra defectos de diseño o fabricación.")
            validez_oferta = st.text_input("Validez de Oferta", value="10 días calendarios o hasta agotar stock.")

        st.markdown("---")
        nota_1 = st.text_input("Nota 1", value="Nuestra oferta está propensa a una nueva cotización en caso de modificaciones de las características técnicas o cantidades.")
        nota_2 = st.text_input("Nota 2", value="Considerar la revisión de esta cotización a detalle, quien haga sus veces para dar la conformidad y se genere la orden de compra.")
        nota_3 = st.text_input("Nota 3", value="Para proceder con la adquisición del bien, es necesario generar una orden de compra que nos permita formalizar y validar la operación.")
        nota_4 = st.text_input("Nota 4", value="Antes de proceder a notificar la orden de compra, por favor comunicarse telefónicamente para verificar la disponibilidad de los productos.")

    with tab4:
        st.subheader("Cuentas Bancarias y Representante Legal")
        banco_bbva_cta = st.text_input("CTA. CTE. SOLES BBVA", value="0011 01110100059448")
        banco_bbva_cci = st.text_input("CCI SOLES BBVA", value="011 111 000100059448 29")
        banco_bcp_cta = st.text_input("CTA. CTE. SOLES BCP", value="192 2661210 0 08")
        banco_bcp_cci = st.text_input("CCI SOLES BCP", value="002 192 002661210008 36")
        
        col8, col9 = st.columns(2)
        with col8:
            telefonos_contacto = st.text_input("Teléfono de Contacto Pie", value="934115891")
            ruc_empresa = st.text_input("RUC Empresa", value="20604321272")
        with col9:
            representante = st.text_input("Representante Legal", value="MARLON BECERRA HERNANDEZ")
            cargo_representante = st.text_input("Cargo", value="GERENTE GENERAL")

        pie_garantia_texto = st.text_input("Texto de pie de página", value="NEWTECH HOSPI S.A.C. garantiza la validez de sus propuestas comerciales solo si son emitidas desde nuestras cuentas autorizadas: ventas@hospitechperu.com / nthospi@gmail.com.")

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🚀 Generar y Descargar Cotización en PDF")

if submitted:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf_path = tmp_file.name

    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    styles = getSampleStyleSheet()

    header_left_style = ParagraphStyle('HeaderLeft', parent=styles['Normal'], fontSize=8.5, leading=11, textColor=colors.HexColor("#333333"))
    header_right_style = ParagraphStyle('HeaderRight', parent=styles['Normal'], fontSize=11, leading=14, fontName="Helvetica-Bold", textColor=colors.HexColor("#A81C1C"), alignment=2)
    normal_style = ParagraphStyle('NormalStyle', parent=styles['Normal'], fontSize=8.5, leading=11)
    bold_style = ParagraphStyle('BoldStyle', parent=styles['Normal'], fontSize=8.5, leading=11, fontName="Helvetica-Bold")
    table_header_style = ParagraphStyle('TableHead', parent=styles['Normal'], fontSize=8.5, leading=11, fontName="Helvetica-Bold", textColor=colors.white, alignment=1)

    # Membrete Superior
    empresa_info = f"<b>NEWTECH HOSPI S.A.C.</b><br/>RUC: {ruc_empresa}<br/>VENTANILLA - CALLAO<br/>Email: ventas@hospitechperu.com / nthospi@gmail.com"
    doc_info = f"<b>{nro_coti}</b><br/><br/>{fecha_emision}"

    t_top = Table([[Paragraph(empresa_info, header_left_style), Paragraph(doc_info, header_right_style)]], colWidths=[330, 222])
    t_top.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_top)
    story.append(Spacer(1, 5))

    # Datos del Cliente
    client_data = [
        [Paragraph(f"<b>CLIENTE:</b> {cliente_nombre}", normal_style), Paragraph(f"<b>VENTA:</b> {vendedor}", normal_style)],
        [Paragraph(f"<b>REFERENCIA:</b> {referencia}", normal_style), Paragraph(f"<b>CELULAR:</b> {celular_vendedor}", normal_style)]
    ]
    t_client = Table(client_data, colWidths=[360, 192])
    t_client.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#999999")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_client)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Nos dirigimos a ustedes a fin de saludarlos y remitir la presente cotización por lo siguiente:", normal_style))
    story.append(Spacer(1, 6))

    # Tabla de Ítems Dinámica
    table_items = [
        [Paragraph("ITEM", table_header_style), Paragraph("DESCRIPCIÓN", table_header_style), Paragraph("CANT", table_header_style), Paragraph("UND", table_header_style), Paragraph("P. UNIT", table_header_style), Paragraph("P. TOTAL", table_header_style)]
    ]

    monto_total_general = 0.0
    for idx, item in enumerate(items_data):
        subtotal_item = item["cant"] * item["p_u"]
        monto_total_general += subtotal_item
        nro_item_str = f"{idx+1:02d}"
        desc_para = Paragraph(item["desc"].replace('\n', '<br/>'), normal_style)
        table_items.append([nro_item_str, desc_para, f"{int(item['cant']) if item['cant'].is_integer() else item['cant']}", item["und"], f"S/{item['p_u']:,.2f}", f"S/{subtotal_item:,.2f}"])

    t_items = Table(table_items, colWidths=[35, 302, 45, 35, 55, 80])
    
    # Estilo dinámico para los ítems según la cantidad de filas
    ts = [
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A2B4C")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (1,1), (1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#999999")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]
    t_items.setStyle(TableStyle(ts))
    story.append(t_items)

    # Monto Total General
    total_data = [
        ["", "", "", "", "MONTO TOTAL:", f"S/{monto_total_general:,.2f}"]
    ]
    t_total = Table(total_data, colWidths=[35, 302, 45, 35, 55, 80])
    t_total.setStyle(TableStyle([
        ('BACKGROUND', (4,0), (5,0), colors.HexColor("#EFEFEF")),
        ('FONTNAME', (4,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('ALIGN', (4,0), (4,0), 'RIGHT'),
        ('ALIGN', (5,0), (5,0), 'CENTER'),
        ('GRID', (4,0), (-1,-1), 0.5, colors.HexColor("#999999")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_total)
    story.append(Spacer(1, 8))

    # Condiciones de Venta
    cond_data = [
        [Paragraph("<b>CONDICIONES DE VENTA:</b>", bold_style), Paragraph("", normal_style)],
        [Paragraph("Precio", bold_style), Paragraph(": Los precios están dados en SOLES, incluyen el IGV.", normal_style)],
        [Paragraph("Tiempo de entrega", bold_style), Paragraph(f": {tiempo_entrega}", normal_style)],
        [Paragraph("Forma de pago", bold_style), Paragraph(f": {forma_pago}", normal_style)],
        [Paragraph("Garantía", bold_style), Paragraph(f": {garantia}", normal_style)],
        [Paragraph("Validez de oferta", bold_style), Paragraph(f": {validez_oferta}", normal_style)],
        [Paragraph("Nota 1", bold_style), Paragraph(f": {nota_1}", normal_style)],
        [Paragraph("Nota 2", bold_style), Paragraph(f": {nota_2}", normal_style)],
        [Paragraph("Nota 3", bold_style), Paragraph(f": {nota_3}", normal_style)],
        [Paragraph("NOTA 4", bold_style), Paragraph(f": {nota_4}", normal_style)],
    ]
    t_cond = Table(cond_data, colWidths=[100, 452])
    t_cond.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#EFEFEF")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_cond)
    story.append(Spacer(1, 8))

    # Cuentas Bancarias y Firmas
    banco_text = f"""
    <b>CTA. CORRIENTE SOLES BBVA:</b> {banco_bbva_cta}<br/>
    <b>CODIGO. CCI. SOLES BBVA:</b> {banco_bbva_cci}<br/>
    <b>CTA. CORRIENTE SOLES BCP:</b> {banco_bcp_cta}<br/>
    <b>CODIGO. CCI. SOLES BCP:</b> {banco_bcp_cci}<br/>
    <b>TELÉFONO:</b> {telefonos_contacto} | <b>R.U.C.:</b> {ruc_empresa}
    """
    
    firma_text = f"""
    <b>NEWTECH HOSPI S.A.C.</b><br/>
    <b>R.U.C. {ruc_empresa}</b><br/><br/>
    <b>{representante}</b><br/>
    <b>{cargo_representante}</b>
    """

    footer_data = [
        [Paragraph(banco_text, normal_style), Paragraph(firma_text, ParagraphStyle('Firma', parent=normal_style, alignment=1))]
    ]
    t_footer = Table(footer_data, colWidths=[330, 222])
    t_footer.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_footer)
    story.append(Spacer(1, 8))

    # Pie de página final
    pie_text = f"<font size=7 color='#666666'><i>{pie_garantia_texto}</i></font>"
    story.append(Paragraph(pie_text, ParagraphStyle('Pie', parent=normal_style, alignment=1)))

    doc.build(story)

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    st.success("¡Cotización generada exitosamente!")
    st.download_button(
        label="📥 Descargar Cotización Oficial en PDF",
        data=pdf_bytes,
        file_name=f"{nro_coti if nro_coti else 'COTIZACION'}.pdf",
        mime="application/pdf"
    )
