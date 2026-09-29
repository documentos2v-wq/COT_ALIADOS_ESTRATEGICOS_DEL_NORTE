from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import streamlit as st
import tempfile
import os

st.set_page_config(page_title="Generador de Cotizaciones B2G", layout="centered")

st.title("📄 Generador de Cotizaciones - Formato HospiTech (B2G)")
st.markdown("Complete la información para generar la cotización idéntica al formato original.")

with st.form("cotizacion_form"):
    st.subheader("1. Datos del Documento y Cliente")
    col1, col2 = st.columns(2)
    with col1:
        nro_coti = st.text_input("Código de Cotización", value="COTI NT HOSPI-000970-2026")
        cliente_nombre = st.text_input("Cliente / Entidad", value="RED INTEGRADA DE SALUD PACIFICO NORTE")
        referencia = st.text_input("Referencia", value="PEDIDO DE COMPRA")
    with col2:
        fecha_emision = st.text_input("Fecha de Emisión", value="Lima, 15 de mayo del 2026")
        vendedor = st.text_input("Asesor / Venta", value="YOSELIN ACERO")
        celular_vendedor = st.text_input("Celular de Contacto Venta", value="924367556 / 981622589")

    st.subheader("2. Detalle del Producto / Ítem")
    item_desc = st.text_area("Descripción Técnica del Ítem", value="CAJA DE BIOSEGURIDAD DE 3L CON DISPOSITIVO\nMARCA: DESLAB\nPROCEDENCIA: NACIONAL\nESPECIFICACIONES TÉCNICAS:\n• Tapa de seguridad: Dispositivo de plástico con tapa hermética que evita aerosoles\n• Material: Cartón microcorrugado trilaminado 575 g/m2\nDIMENSIONES:\n• Espesor: 2 mm | Altura: 19 cm | Ancho: 15 cm | Largo: 11 cm")
    col3, col4, col5 = st.columns(3)
    with col3:
        cantidad = st.number_input("Cantidad", value=6000, step=1)
    with col4:
        p_unit = st.number_input("Precio Unitario (S/)", value=5.12, format="%.2f")
    with col5:
        unidad_medida = st.text_input("Unidad", value="UND")

    st.subheader("3. Condiciones Comerciales")
    col6, col7 = st.columns(2)
    with col6:
        tiempo_entrega = st.text_input("Tiempo de Entrega", value="10 DÍAS CALENDARIOS contabilizado a partir del día siguiente de suscrito el contrato.")
        forma_pago = st.text_input("Forma de Pago", value="Abono en cuenta interbancaria (CCI) crédito comercial")
    with col7:
        garantia = st.text_input("Garantía", value="(12) meses a partir de la fecha de entrega y exclusivamente contra defectos de diseño o fabricación.")
        validez_oferta = st.text_input("Validez de Oferta", value="10 días calendarios o hasta agotar stock.")

    submitted = st.form_submit_button("Generar Cotización en PDF")

if submitted:
    subtotal = cantidad * p_unit

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf_path = tmp_file.name

    # Márgenes reducidos para aprovechar el formato de dos columnas idéntico al original
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    story = []
    styles = getSampleStyleSheet()

    # Estilos tipográficos precisos
    sidebar_style = ParagraphStyle('Sidebar', parent=styles['Normal'], fontSize=7.5, leading=9, textColor=colors.HexColor("#333333"))
    header_right_style = ParagraphStyle('HeaderRight', parent=styles['Normal'], fontSize=9, leading=12, alignment=2)
    title_coti_style = ParagraphStyle('TitleCoti', parent=styles['Normal'], fontSize=11, leading=14, fontName="Helvetica-Bold", textColor=colors.HexColor("#A81C1C"), alignment=2)
    normal_style = ParagraphStyle('NormalStyle', parent=styles['Normal'], fontSize=8, leading=10)
    bold_style = ParagraphStyle('BoldStyle', parent=styles['Normal'], fontSize=8, leading=10, fontName="Helvetica-Bold")
    table_header_style = ParagraphStyle('TableHead', parent=styles['Normal'], fontSize=8, leading=10, fontName="Helvetica-Bold", textColor=colors.white, alignment=1)

    # ----------------------------------------------------
    # COLUMNA IZQUIERDA (Sidebar) vs COLUMNA DERECHA (Encabezado)
    # ----------------------------------------------------
    sidebar_content = """
    <b>PRACTICAS DE ALMACEN</b><br/>
    <b>BPA</b><br/>
    <b>GPS</b><br/>
    <b>HDD PRACTICE STORAGE</b><br/><br/>
    <b>RUC 20604321272</b><br/>
    NEWTECH HOSPI SAC<br/><br/>
    ventas@hospitechperu.com<br/>
    nthospi@gmail.com<br/>
    Hospitechperu.com<br/>
    934007166<br/><br/>
    <b>DROGUERIA</b><br/>
    <b>HospiTech</b><br/>
    NUEVA TECNOLOGIA MEDICA Perú<br/><br/>
    BARRIO XIV SECT. G GR. 1<br/>
    PPNP MZ. O LT. 8 /<br/>
    VENTANILLA - CALLAO<br/><br/>
    <b>SIGUENOS:</b> f / 📷
    """

    header_right_content = f"""
    <b>{nro_coti}</b><br/><br/>
    Lima, 15 de mayo del 2026
    """

    top_table_data = [
        [Paragraph(sidebar_content, sidebar_style), Paragraph(header_right_content, title_coti_style)]
    ]
    
    # Anchos calculados en base a hoja Letter (Ancho total ~572 puntos disponibles)
    t_top = Table(top_table_data, colWidths=[140, 432])
    t_top.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEAFTER', (0,0), (0,0), 1, colors.HexColor("#A81C1C")),
        ('RIGHTPADDING', (0,0), (0,0), 10),
        ('LEFTPADDING', (1,0), (1,0), 15),
    ]))
    story.append(t_top)
    story.append(Spacer(1, 10))

    # Datos de Cliente y Venta
    client_data = [
        [Paragraph(f"<b>CLIENTE:</b> {cliente_nombre}", normal_style), Paragraph(f"<b>VENTA:</b> {vendedor}", normal_style)],
        [Paragraph(f"<b>REFERENCIA:</b> {referencia}", normal_style), Paragraph(f"<b>CELULAR:</b> {celular_vendedor}", normal_style)]
    ]
    t_client = Table(client_data, colWidths=[372, 200])
    t_client.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#999999")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_client)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Nos dirigimos a ustedes a fin de saludarlos y remitir la presente cotización por lo siguiente:", normal_style))
    story.append(Spacer(1, 4))

    # Tabla de Ítems principal
    table_items = [
        [Paragraph("ITEM", table_header_style), Paragraph("DESCRIPCIÓN", table_header_style), Paragraph("CANT", table_header_style), Paragraph("UND", table_header_style), Paragraph("P. UNIT", table_header_style), Paragraph("P. TOTAL", table_header_style)],
        ["01", Paragraph(item_desc.replace('\n', '<br/>'), normal_style), f"{cantidad}", f"{unidad_medida}", f"S/{p_unit:,.2f}", f"S/{subtotal:,.2f}"]
    ]
    t_items = Table(table_items, colWidths=[30, 312, 45, 35, 55, 95])
    t_items.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A2B4C")), # Azul institucional o rojo oscuro original
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (1,1), (1,1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#999999")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_items)

    # Monto Total
    total_data = [
        ["", "", "", "", "MONTO TOTAL:", f"S/{subtotal:,.2f}"]
    ]
    t_total = Table(total_data, colWidths=[30, 312, 45, 35, 55, 95])
    t_total.setStyle(TableStyle([
        ('BACKGROUND', (4,0), (5,0), colors.HexColor("#EFEFEF")),
        ('FONTNAME', (4,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (4,0), (4,0), 'RIGHT'),
        ('ALIGN', (5,0), (5,0), 'CENTER'),
        ('GRID', (4,0), (-1,-1), 0.5, colors.HexColor("#999999")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_total)
    story.append(Spacer(1, 6))

    # Condiciones de Venta (Formato con dos puntos alineados)
    cond_data = [
        [Paragraph("<b>CONDICIONES DE VENTA:</b>", bold_style), Paragraph("", normal_style)],
        [Paragraph("Precio", bold_style), Paragraph(": Los precios están dados en SOLES, incluyen el IGV.", normal_style)],
        [Paragraph("Tiempo de entrega", bold_style), Paragraph(f": {tiempo_entrega}", normal_style)],
        [Paragraph("Forma de pago", bold_style), Paragraph(f": {forma_pago}", normal_style)],
        [Paragraph("Garantía", bold_style), Paragraph(f": {garantia}", normal_style)],
        [Paragraph("Validez de oferta", bold_style), Paragraph(f": {validez_oferta}", normal_style)],
        [Paragraph("Nota 1", bold_style), Paragraph(": Nuestra oferta está propensa a una nueva cotización en caso de modificaciones técnicas o cantidades.", normal_style)],
        [Paragraph("Nota 2", bold_style), Paragraph(": Considerar la revisión de esta cotización a detalle para dar conformidad y generar la orden de compra.", normal_style)],
        [Paragraph("Nota 3", bold_style), Paragraph(": Para proceder con la adquisición del bien, es necesario generar una orden de compra que formalice la operación.", normal_style)],
        [Paragraph("NOTA 4", bold_style), Paragraph(": Antes de notificar la orden de compra, comunicarse telefónicamente para verificar disponibilidad.", normal_style)],
    ]
    t_cond = Table(cond_data, colWidths=[110, 462])
    t_cond.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#EFEFEF")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_cond)
    story.append(Spacer(1, 6))

    # Cuentas Bancarias y Firmas
    banco_text = """
    <b>CTA. CORRIENTE SOLES BBVA BANCO CONTINENTAL:</b> 0011 01110100059448<br/>
    <b>CODIGO. CCI. SOLES BBVA:</b> 011 111 000100059448 29<br/>
    <b>CTA. CORRIENTE SOLES BCP:</b> 192 2661210 0 08<br/>
    <b>CODIGO. CCI. SOLES BCP:</b> 002 192 002661210008 36<br/>
    <b>TELÉFONO:</b> 934115891 | <b>R.U.C.:</b> 20604321272
    """
    
    firma_text = """
    <b>NEWTECH HOSPI S.A.C.</b><br/><br/><br/>
    <b>MARLON BECERRA HERNANDEZ</b><br/>
    <b>GERENTE GENERAL</b>
    """

    footer_data = [
        [Paragraph(banco_text, normal_style), Paragraph(firma_text, ParagraphStyle('Firma', parent=normal_style, alignment=1))]
    ]
    t_footer = Table(footer_data, colWidths=[330, 242])
    t_footer.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_footer)

    doc.build(story)

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    st.success("¡Cotización generada con el diseño exacto!")
    st.download_button(
        label="📥 Descargar Cotización PDF",
        data=pdf_bytes,
        file_name=f"{nro_coti}.pdf",
        mime="application/pdf"
    )
