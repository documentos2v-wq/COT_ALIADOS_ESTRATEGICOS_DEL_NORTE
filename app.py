from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import streamlit as st
import tempfile
import os

st.set_page_config(page_title="Generador de Cotizaciones B2G", layout="centered")

st.title("📄 Generador de Cotizaciones - Formato Aliados / B2G")
st.markdown("Complete los campos a continuación para generar y descargar la cotización formal en PDF.")

with st.form("cotizacion_form"):
    st.subheader("1. Datos del Emisor / Proveedor")
    col1, col2 = st.columns(2)
    with col1:
        empresa_nombre = st.text_input("Nombre de la Empresa", value="NEWTECH HOSPI S.A.C.")
        empresa_ruc = st.text_input("RUC del Proveedor", value="20604321272")
        empresa_correo = st.text_input("Correo Electrónico", value="ventas@hospitechperu.com")
    with col2:
        empresa_celular = st.text_input("Celular / Teléfono", value="934007166")
        empresa_dir = st.text_input("Dirección Fiscal", value="BARRIO XIV SECT. G GR. 1 PPNP MZ. O LT. 8 / VENTANILLA - CALLAO")
        representante = st.text_input("Representante Legal", value="MARLON BECERRA HERNANDEZ - GERENTE GENERAL")

    st.subheader("2. Datos del Cliente y Documento")
    col3, col4 = st.columns(2)
    with col3:
        nro_coti = st.text_input("Código de Cotización", value="COTI NT HOSPI-000970-2026")
        cliente_nombre = st.text_input("Cliente / Entidad", value="RED INTEGRADA DE SALUD PACIFICO NORTE")
        referencia = st.text_input("Referencia", value="PEDIDO DE COMPRA")
    with col4:
        fecha_emision = st.text_input("Fecha de Emisión", value="Lima, 15 de mayo del 2026")
        vendedor = st.text_input("Asesor / Venta", value="YOSELIN ACERO")
        celular_vendedor = st.text_input("Celular de Contacto Venta", value="924367556 / 981622589")

    st.subheader("3. Detalle del Producto / Servicio (Ítem)")
    item_desc = st.text_area("Descripción Técnica del Ítem", value="CAJA DE BIOSEGURIDAD DE 3L CON DISPOSITIVO\nMARCA: DESLAB\nPROCEDENCIA: NACIONAL\nESPECIFICACIONES TÉCNICAS:\nTapa de seguridad: Dispositivo de plástico con tapa hermética...\nMaterial: Cartón microcorrugado trilaminado 575 g/m2")
    col5, col6, col7 = st.columns(3)
    with col5:
        cantidad = st.number_input("Cantidad", value=6000, step=1)
    with col6:
        p_unit = st.number_input("Precio Unitario (S/)", value=5.12, format="%.2f")
    with col7:
        unidad_medida = st.text_input("Unidad", value="UND")

    st.subheader("4. Condiciones Comerciales")
    col8, col9 = st.columns(2)
    with col8:
        tiempo_entrega = st.text_input("Tiempo de Entrega", value="10 DÍAS CALENDARIOS")
        forma_pago = st.text_input("Forma de Pago", value="Abono en cuenta interbancaria (CCI) crédito comercial")
    with col9:
        garantia = st.text_input("Garantía", value="12 meses a partir de la fecha de entrega")
        validez_oferta = st.text_input("Validez de Oferta", value="10 días calendarios o hasta agotar stock")

    st.subheader("5. Datos Bancarios")
    banco_1 = st.text_area("Cuentas Bancarias (Texto o detalle)", value="BBVA CTA. CTE. SOLES: 0011 01110100059448 | CCI: 011 111 000100059448 29\nBCP CTA. CTE. SOLES: 192 2661210 0 08 | CCI: 002 192 002661210008 36")

    submitted = st.form_submit_button("Generar Cotización en PDF")

if submitted:
    subtotal = cantidad * p_unit
    igv = subtotal * 0.18
    total = subtotal # Si los precios ya incluyen IGV según el formato original

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf_path = tmp_file.name

    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()

    # Estilos personalizados
    header_style = ParagraphStyle('HeaderStyle', parent=styles['Normal'], fontSize=9, leading=11, textColor=colors.HexColor("#333333"))
    title_style = ParagraphStyle('TitleStyle', parent=styles['Normal'], fontSize=11, leading=14, fontName="Helvetica-Bold", textColor=colors.HexColor("#A81C1C"))
    normal_style = ParagraphStyle('NormalStyle', parent=styles['Normal'], fontSize=8.5, leading=11)
    bold_style = ParagraphStyle('BoldStyle', parent=styles['Normal'], fontSize=8.5, leading=11, fontName="Helvetica-Bold")

    # Encabezado Empresa
    header_data = [
        [Paragraph(f"<b>{empresa_nombre}</b><br/>RUC: {empresa_ruc}<br/>{empresa_dir}<br/>Email: {empresa_correo} | Tel: {empresa_celular}", header_style),
         Paragraph(f"<b>{nro_coti}</b><br/><br/><b>Fecha:</b> {fecha_emision}", title_style)]
    ]
    t_header = Table(header_data, colWidths=[360, 180])
    t_header.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_header)
    story.append(Spacer(1, 10))

    # Datos Cliente
    client_data = [
        [Paragraph(f"<b>CLIENTE:</b> {cliente_nombre}", normal_style), Paragraph(f"<b>VENTA:</b> {vendedor}", normal_style)],
        [Paragraph(f"<b>REFERENCIA:</b> {referencia}", normal_style), Paragraph(f"<b>CELULAR:</b> {celular_vendedor}", normal_style)]
    ]
    t_client = Table(client_data, colWidths=[360, 180])
    t_client.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#EFEFEF")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_client)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Nos dirigimos a ustedes a fin de saludarlos y remitir la presente cotización por lo siguiente:", normal_style))
    story.append(Spacer(1, 8))

    # Tabla de Ítems
    table_items = [
        ["ITEM", "DESCRIPCIÓN", "CANT", "UND", "P. UNIT", "P. TOTAL"],
        ["01", Paragraph(item_desc.replace('\n', '<br/>'), normal_style), f"{cantidad}", f"{unidad_medida}", f"S/{p_unit:,.2f}", f"S/{subtotal:,.2f}"]
    ]
    t_items = Table(table_items, colWidths=[35, 275, 45, 35, 55, 95])
    t_items.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#A81C1C")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8.5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (1,1), (1,1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_items)

    # Total row
    total_data = [
        ["", "", "", "", "MONTO TOTAL:", f"S/{subtotal:,.2f}"]
    ]
    t_total = Table(total_data, colWidths=[35, 275, 45, 35, 55, 95])
    t_total.setStyle(TableStyle([
        ('BACKGROUND', (4,0), (5,0), colors.HexColor("#F2F2F2")),
        ('FONTNAME', (4,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('ALIGN', (4,0), (4,0), 'RIGHT'),
        ('ALIGN', (5,0), (5,0), 'CENTER'),
        ('GRID', (4,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_total)
    story.append(Spacer(1, 10))

    # Condiciones de Venta
    cond_data = [
        [Paragraph("<b>CONDICIONES DE VENTA:</b>", bold_style), Paragraph("", normal_style)],
        [Paragraph("<b>Precio</b>", bold_style), Paragraph("Los precios están dados en SOLES, incluyen el IGV.", normal_style)],
        [Paragraph("<b>Tiempo de entrega</b>", bold_style), Paragraph(f"{tiempo_entrega} contabilizado a partir del día siguiente de suscrito el contrato.", normal_style)],
        [Paragraph("<b>Forma de pago</b>", bold_style), Paragraph(f"{forma_pago}", normal_style)],
        [Paragraph("<b>Garantía</b>", bold_style), Paragraph(f"{garantia} y exclusivamente contra defectos de diseño o fabricación.", normal_style)],
        [Paragraph("<b>Validez de oferta</b>", bold_style), Paragraph(f"{validez_oferta}", normal_style)],
    ]
    t_cond = Table(cond_data, colWidths=[120, 420])
    t_cond.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#EFEFEF")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_cond)
    story.append(Spacer(1, 8))

    # Notas y Cuentas Bancarias
    notas_text = """<b>Notas Importantes:</b><br/>
    1. Nuestra oferta está propensa a una nueva cotización en caso de modificaciones de las características técnicas o cantidades.<br/>
    2. Considerar la revisión de esta cotización a detalle, quien haga sus veces para dar la conformidad y se genere la orden de compra.<br/>
    3. Para proceder con la adquisición del bien, es necesario generar una orden de compra que nos permita formalizar y validar la operación.<br/>
    4. Antes de proceder a notificar la orden de compra, por favor comunicarse telefónicamente para verificar la disponibilidad de los productos.<br/><br/>
    <b>CUENTAS BANCARIAS:</b><br/>
    {banco_text}
    """.format(banco_text=banco_1.replace('\n', '<br/>'))

    story.append(Paragraph(notas_text, normal_style))
    story.append(Spacer(1, 15))

    # Firma
    firma_data = [
        [Paragraph(f"<b>{representante}</b><br/>REPRESENTANTE LEGAL<br/>{empresa_nombre}<br/>RUC: {empresa_ruc}", ParagraphStyle('Firma', parent=normal_style, alignment=1))]
    ]
    t_firma = Table(firma_data, colWidths=[200])
    t_firma.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 20),
    ]))
    # Centrar tabla de firma
    story.append(Table([["", t_firma, ""]], colWidths=[170, 200, 170]))

    doc.build(story)

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    st.success("¡Cotización generada exitosamente!")
    st.download_button(
        label="📥 Descargar Cotización en PDF",
        data=pdf_bytes,
        file_name=f"{nro_coti}.pdf",
        mime="application/pdf"
    )
