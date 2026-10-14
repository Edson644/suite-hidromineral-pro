"""
Interfaz de Usuario y Generador Avanzado - Módulo 10: Informe Gerencial PDF de Alta Gama y Multipestaña Excel
Suite Hidromineral Pro
"""

import streamlit as st
import pandas as pd
import io
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.title("Módulo 10: Generador de Informes y Memorias de Cálculo")

st.markdown("""
Este módulo centraliza la emisión de documentación oficial. Genera un **Informe Gerencial PDF de Alta Gama** 
(con diseño visual atractivo, sin marcas de texto plano y optimizado para ocupar toda la hoja) y una **Memoria de Cálculo Multipestaña en Excel**.
""")

st.divider()

os.makedirs("reportes_generados/pdf", exist_ok=True)
os.makedirs("reportes_generados/excel", exist_ok=True)

# Sección 1: Generador de Informe Gerencial PDF de Alta Gama
st.subheader("1. Generación de Informe Gerencial Ejecutivo (PDF de Alta Gama)")
st.markdown("Crea un reporte visualmente atractivo, estructurado y optimizado para directorio y gerencia.")

if st.button("📄 Generar y Guardar Informe PDF Gerencial Visual"):
    try:
        filename_pdf = "reportes_generados/pdf/Informe_Gerencial_Alta_Gama.pdf"
        # Márgenes compactos para aprovechar toda la hoja verticalmente
        doc = SimpleDocTemplate(filename_pdf, pagesize=letter, rightMargin=25, leftMargin=25, topMargin=25, bottomMargin=25)
        story = []
        
        styles = getSampleStyleSheet()
        titulo_estilo = ParagraphStyle('TituloPDF', parent=styles['Heading1'], fontSize=15, textColor=colors.HexColor('#1b4f72'), spaceAfter=2, alignment=1)
        sub_estilo = ParagraphStyle('SubPDF', parent=styles['Heading2'], fontSize=10, textColor=colors.HexColor('#566573'), spaceAfter=6, alignment=1)
        seccion_estilo = ParagraphStyle('SecPDF', parent=styles['Heading2'], fontSize=11, textColor=colors.HexColor('#1b4f72'), spaceBefore=6, spaceAfter=4)
        normal_estilo = ParagraphStyle('NormalPDF', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#333333'), leading=11)

        # Encabezado Ejecutivo Visual
        story.append(Paragraph("<b>SUITE HIDROMINERAL PRO — REPORTE GERENCIAL DE OPERACIONES</b>", titulo_estilo))
        story.append(Paragraph("Evaluación Integral de Procesos, Confiabilidad y Rentabilidad Minera", sub_estilo))
        story.append(Spacer(1, 4))

        # 1. Tabla de Desempeño por Área
        story.append(Paragraph("<b>1. Desempeño Operacional por Circuito de Planta</b>", seccion_estilo))
        data_areas = [
            ["Área / Circuito", "Parámetro Monitoreado", "Valor Actual", "Meta / Diseño", "Estado"],
            ["M1 Chancado", "Tonelaje Tratado", "2.330 t/h", "2.500 t/h", "Óptimo"],
            ["M2 Aglomeración", "Humedad en Tambor", "7,50 %", "7,0 - 8,0 %", "Conforme"],
            ["M3 Lixiviación", "Recuperación Acumulada", "82,00 %", "80,00 %", "Excelente"],
            ["M4 SX", "Eficiencia Extracción", "96,50 %", "95,00 %", "Conforme"],
            ["M5 EW", "Producción Cátodos Grado A", "346,0 t/día", "340,0 t/día", "Sobrecumplido"],
            ["M8 Finanzas", "VAN del Proyecto (10 Años)", "$393,7 MM USD", "$350 MM USD", "Altamente Rentable"]
        ]
        
        t_areas = Table(data_areas, colWidths=[100, 150, 95, 95, 120])
        t_areas.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1b4f72')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 3),
            ('TOPPADDING', (0,0), (-1,0), 3),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8f9f9')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bdc3c7')),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ]))
        story.append(t_areas)
        story.append(Spacer(1, 6))

        # 2. Gráfico Ejecutivo Integrado
        story.append(Paragraph("<b>2. Indicadores de Eficiencia Operacional por Circuito (%)</b>", seccion_estilo))
        
        d = Drawing(540, 115)
        bc = VerticalBarChart()
        bc.x = 35
        bc.y = 12
        bc.height = 90
        bc.width = 485
        bc.data = [[93.2, 94.0, 82.0, 96.5, 92.0, 98.5]]
        bc.categoryAxis.categoryNames = ['Chancado', 'Aglomeración', 'Lixiviación', 'SX', 'EW', 'Finanzas']
        bc.categoryAxis.labels.fontSize = 7.5
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = 100
        bc.valueAxis.valueStep = 25
        bc.valueAxis.labels.fontSize = 7.5
        bc.bars[0].fillColor = colors.HexColor('#1b4f72')
        d.add(bc)
        story.append(d)
        story.append(Spacer(1, 6))

        # 3. Nueva Tabla de Indicadores Financieros y Productivos Globales (Para ocupar toda la hoja)
        story.append(Paragraph("<b>3. Consolidado Financiero y Productivo Anual</b>", seccion_estilo))
        data_kpis = [
            ["Indicador Macroeconómico / Planta", "Proyección Anual", "Parámetro Financiero", "Valor Comercial"],
            ["Producción Anual de Cátodos", "126.300 t/año", "Precio de Venta Cobre", "4,15 USD/lb"],
            ["Costo Operacional Global (OPEX)", "1,85 USD/lb", "Tasa Descuento (WACC)", "8,5 %"],
            ["EBITDA Operacional Estimado", "$564,2 MM USD", "TIR del Proyecto", "15,0 %"]
        ]
        t_kpis = Table(data_kpis, colWidths=[150, 120, 150, 140])
        t_kpis.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#283747')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 3),
            ('TOPPADDING', (0,0), (-1,0), 3),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#ebedef')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bdc3c7')),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ]))
        story.append(t_kpis)
        story.append(Spacer(1, 6))

        # 4. Conclusiones Limpias y Numeradas (Sin asteriscos)
        story.append(Paragraph("<b>4. Conclusiones y Recomendaciones Estratégicas</b>", seccion_estilo))
        texto_conclusiones = (
            "1. <b>Estabilidad Operacional:</b> El complejo hidrometalúrgico opera de manera sólida, destacando el cumplimiento "
            "riguroso en la producción de cátodos de alta pureza (Grado A) en la sección de Electroobtención.<br/>"
            "2. <b>Oportunidad de Mejora:</b> Se recomienda intensificar los controles de compactación y canales preferenciales "
            "en las pilas de lixiviación (M3) para asegurar que la cinética de extracción mantenga una tendencia superior a la proyectada.<br/>"
            "3. <b>Viabilidad Financiera:</b> Los indicadores económicos del Módulo 8 confirman la absoluta robustez del proyecto, "
            "arrojando un VAN de $393,7 millones de dólares y un retorno sumamente favorable para la inversión corporativa."
        )
        story.append(Paragraph(texto_conclusiones, normal_estilo))
        
        doc.build(story)
        st.success("¡Informe PDF Gerencial de Alta Gama generado con éxito en `reportes_generados/pdf/`!")
        
        with open(filename_pdf, "rb") as f:
            st.download_button("⬇️ Descargar Informe PDF Gerencial Visual", f.read(), "Informe_Gerencial_Alta_Gama.pdf", "application/pdf")
    except Exception as e:
        st.error(f"Error generando el PDF visual: {e}")

st.divider()

# Sección 2: Generador de Memoria de Cálculo Multipestaña en Excel
st.subheader("2. Generación de Memoria de Cálculo Multipestaña (Excel con Fórmulas Linkeadas)")
st.markdown("Genera el libro maestro en Excel con pestañas dedicadas por cada módulo y datos interconectados.")

if st.button("📊 Generar y Guardar Memoria de Cálculo Multipestaña"):
    try:
        filename_excel = "reportes_generados/excel/Memoria_de_Calculo_Multipestana.xlsx"
        wb = Workbook()
        
        font_titulo = Font(name="Arial", size=12, bold=True, color="FFFFFF")
        fill_titulo = PatternFill(start_color="1B4F72", end_color="1B4F72", fill_type="solid")
        font_header = Font(name="Arial", size=10, bold=True, color="FFFFFF")
        fill_header = PatternFill(start_color="283747", end_color="283747", fill_type="solid")
        font_normal = Font(name="Arial", size=9.5)
        borde_fino = Border(left=Side(style='thin', color='BDC3C7'), right=Side(style='thin', color='BDC3C7'), top=Side(style='thin', color='BDC3C7'), bottom=Side(style='thin', color='BDC3C7'))

        # Hoja 1: Datos de Entrada
        ws_in = wb.active
        ws_in.title = "Datos de Entrada"
        ws_in.merge_cells("A1:D1")
        ws_in["A1"] = "PARÁMETROS MAESTROS DE DISEÑO Y OPERACIÓN"
        ws_in["A1"].font = font_titulo
        ws_in["A1"].fill = fill_titulo
        ws_in["A1"].alignment = Alignment(horizontal="center", vertical="center")
        ws_in.row_dimensions[1].height = 25

        headers_in = ["Parámetro / Variable", "Símbolo", "Valor", "Unidad"]
        for col_idx, h in enumerate(headers_in, 1):
            c = ws_in.cell(row=3, column=col_idx, value=h)
            c.font = font_header
            c.fill = fill_header
            c.alignment = Alignment(horizontal="center", vertical="center")

        datos_entrada = [
            ("Tonelaje de Alimentación a Planta", "M_alim", 2330.0, "t/h"),
            ("Ley de Cabeza de Cobre Total", "Cu_t", 0.85, "%"),
            ("Recuperación en Lixiviación", "Rec_lix", 82.0, "%"),
            ("Eficiencia de Extracción SX", "Eff_sx", 96.5, "%"),
            ("Eficiencia de Corriente EW", "Eff_ew", 92.0, "%"),
            ("Precio de Venta del Cobre", "Pre_Cu", 4.15, "USD/lb"),
            ("Costo Operacional Total (OPEX)", "OPEX", 1.85, "USD/lb")
        ]

        for r_idx, fila in enumerate(datos_entrada, 4):
            for c_idx, val in enumerate(fila, 1):
                cell = ws_in.cell(row=r_idx, column=c_idx, value=val)
                cell.font = font_normal
                cell.border = borde_fino
                if c_idx == 3:
                    cell.number_format = '#,##0.00'
                    cell.alignment = Alignment(horizontal="right")
                else:
                    cell.alignment = Alignment(horizontal="left" if c_idx == 1 else "center")

        ws_in.column_dimensions['A'].width = 38
        ws_in.column_dimensions['B'].width = 15
        ws_in.column_dimensions['C'].width = 15
        ws_in.column_dimensions['D'].width = 15

        # Hojas de Módulos (M1 a M5 y M8)
        modulos = [
            ("M1 Chancado", "MÓDULO 1: CIRCUITO DE CHANCADO", [("Tonelaje Horario", "M_chanc", "='Datos de Entrada'!C4", "t/h"), ("Disponibilidad", "Disp", 90.0, "%")]),
            ("M2 Aglomeración", "MÓDULO 2: AGLOMERACIÓN", [("Mineral Alimentado", "M_ag", "='M1 Chancado'!C4", "t/h"), ("Dosificación Ácido", "Acido", 16.0, "kg/t")]),
            ("M3 Lixiviación", "MÓDULO 3: PILAS DE LIXIVIACIÓN", [("Mineral Pila", "M_pila", "='Datos de Entrada'!C4", "t/h"), ("Ley Cabeza", "Cu", "='Datos de Entrada'!C5", "%"), ("Recuperación", "Rec", "='Datos de Entrada'!C6", "%")]),
            ("M4-M5 SX y EW", "MÓDULO 4 Y 5: SX Y EW", [("Fino PLS", "Fino", "='M3 Lixiviación'!C6", "t/h"), ("Prod Diaria", "Prod", "=(C4*24)*(0.85/100)*(0.82)", "t/día")]),
            ("M8 Finanzas", "MÓDULO 8: FINANZAS", [("Producción Anual", "Prod_anual", "='M4-M5 SX y EW'!C5 * 365", "t/año"), ("VAN Proyecto", "VAN", 393748568, "USD")])
        ]

        for nombre_hoja, titulo_hoja, filas in modulos:
            ws = wb.create_sheet(title=nombre_hoja)
            ws.merge_cells("A1:D1")
            ws["A1"] = titulo_hoja
            ws["A1"].font = font_titulo
            ws["A1"].fill = fill_titulo
            ws["A1"].alignment = Alignment(horizontal="center", vertical="center")

            for c_i, h in enumerate(["Variable Operacional", "Símbolo", "Valor / Fórmula", "Unidad"], 1):
                c = ws.cell(row=3, column=c_i, value=h)
                c.font = font_header
                c.fill = fill_header
                c.alignment = Alignment(horizontal="center", vertical="center")

            for r_i, fila in enumerate(filas, 4):
                for c_i, val in enumerate(fila, 1):
                    cell = ws.cell(row=r_i, column=c_i, value=val)
                    cell.font = font_normal
                    cell.border = borde_fino
                    if c_i == 3:
                        cell.alignment = Alignment(horizontal="right")
                        if str(val).startswith("="):
                            cell.number_format = '#,##0.00'
                        elif isinstance(val, (int, float)) and val > 1000:
                            cell.number_format = '$#,##0'

            ws.column_dimensions['A'].width = 35
            ws.column_dimensions['B'].width = 15
            ws.column_dimensions['C'].width = 20
            ws.column_dimensions['D'].width = 15

        wb.save(filename_excel)
        st.success("¡Memoria de Cálculo Multipestaña generada con éxito en `reportes_generados/excel/`!")
        
        with open(filename_excel, "rb") as f:
            st.download_button("⬇️ Descargar Memoria Multipestaña Excel", f.read(), "Memoria_de_Calculo_Multipestana.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        st.error(f"Error generando el Excel: {e}")
