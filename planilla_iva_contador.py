import os
import re
import pdfplumber
from openpyxl import Workbook
import streamlit as st
from io import BytesIO
import pandas as pd

def pdf_a_texto(pdf_path):
    texto = ''
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()
            texto += texto_pagina + '\n'
    return texto

def extraer_datos(texto):
    fecha_emision = re.search(r'Fecha de Emisión:\s*(\d{2}/\d{2}/\d{4})', texto)
    punto_venta = re.search(r'Punto de Venta:\s*(\d+)', texto)
    comp_numero = re.search(r'Comp\. Nro:\s*(\d+)', texto)
    razon_social = re.search(r'Razón Social:(?! Virtual Sense)([^\n]+)(?= Fecha)', texto)    
    cuit = re.search(r'CUIT:\s*(?!30716843285)(\d+)', texto)
    iva = re.search(r'Condición frente al IVA:\s*([^\n]+?)(?= Fecha)', texto)
    subtotal = re.search(r'Subtotal:\s*\$\s*([\d,.]+)', texto)
    importe_total = re.search(r'Importe Total:\s*\$\s*([\d,.]+)', texto)

    punto_venta = punto_venta.group(1) if punto_venta else ""
    comp_numero = comp_numero.group(1) if comp_numero else ""
    razon_social = razon_social.group(1).strip() if razon_social else ""
    fecha_emision = fecha_emision.group(1) if fecha_emision else ""
    cuit = cuit.group(1) if cuit else ""
    iva = iva.group(1).strip() if iva else ""
    subtotal = subtotal.group(1).replace(",", "") if subtotal else ""
    importe_total = importe_total.group(1).replace(",", "") if importe_total else ""

    return punto_venta, comp_numero, razon_social, fecha_emision, cuit, iva, subtotal, importe_total

def planilla_iva_contador():
    st.write("Seleccione los archivos PDF de facturas para procesar y extraer datos.")

    uploaded_files = st.file_uploader("Sube tus archivos PDF", accept_multiple_files=True, type=["pdf"])
    if st.button("Procesar archivos PDF"):
        if uploaded_files:
            procesar_pdfs(uploaded_files)
        else:
            st.error("Por favor, suba al menos un archivo PDF.")

def procesar_pdfs(uploaded_files):
    # Crear una lista para almacenar los datos
    datos_facturas = []

    for uploaded_file in uploaded_files:
        # Obtener el texto del PDF
        texto_leido = pdf_a_texto(uploaded_file)
        
        # Extraer los datos de la factura del texto
        datos = extraer_datos(texto_leido)
        
        # Agregar los datos a la lista
        datos_facturas.append(datos)

    # Crear un DataFrame de pandas
    df = pd.DataFrame(datos_facturas, columns=["Fecha de emision", "Punto de Venta", "Comp. Nro", "Razón Social", "CUIT", "Condición frente al IVA", "Subtotal", "Importe Total"])

    # Mostrar el DataFrame en la aplicación
    st.write(df)

    # Convertir el DataFrame a un archivo Excel en memoria
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos Facturas')
    excel_buffer.seek(0)

    # Botón para descargar el archivo Excel
    st.download_button(
        label="Descargar Excel",
        data=excel_buffer,
        file_name="datos_facturas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
