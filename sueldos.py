import streamlit as st
import pandas as pd
import PyPDF2

def pdf_a_texto(pdf_path, start_page=2, end_page=6):
    texto = ''
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            if start_page <= page_num + 1 <= end_page:
                page = reader.pages[page_num]
                texto += page.extract_text()
    return texto

def procesar_pdf(pdf_file):
    if pdf_file is not None:
        texto_extraido = pdf_a_texto(pdf_file)
        
        # Dividir el texto en secciones
        secciones = texto_extraido.split(' - ')
        
        # Crear una lista para almacenar los datos de cada sección
        datos = []
        
        # Procesar cada sección
        for seccion in secciones:
            # Dividir las líneas de la sección
            lineas = seccion.strip().split('\n')
            # Ignorar la primera línea, ya que es el encabezado de la sección
            encabezado = lineas[0]
            # Extraer los nombres de las columnas del encabezado
            columnas = encabezado.split('\t')
            # Procesar las filas de datos
            for linea in lineas[1:]:
                # Dividir la línea en valores separados por tabulaciones
                valores = linea.split('\t')
                # Agregar los valores a la lista de datos
                datos.append(valores)
        
        # Crear un DataFrame a partir de los datos
        df = pd.DataFrame(datos, columns=columnas)
        
        # Separar los datos en la columna '8' en una lista de elementos utilizando "$" como separador
        df['separado'] = df['8'].str.split('$')
        
        # Obtener el máximo número de elementos separados en una fila
        max_elementos = df['separado'].apply(len).max()
        
        # Expandir la lista en columnas individuales
        for i in range(max_elementos):
            df[f'Dato_{i+1}'] = df['separado'].apply(lambda x: x[i] if len(x) > i else None)
        
        # Eliminar la columna original '8' y la columna intermedia 'separado'
        df.drop(columns=['8', 'separado', f'Dato_{max_elementos-1}', f'Dato_{max_elementos}'], inplace=True)
        
        # Renombrar columnas
        df.rename(columns={'Dato_1': 'Concepto', 'Dato_2': 'Importe pesos'}, inplace=True)
        
        # Lista de nombres a filtrar
        nombres_a_filtrar = [
            "00720088007003915204ars",
            "A / - var / 20389871908",
            "00720742007000177128ars",
            "A / - var / 20340458487",
            "A / - var / 20438919717",
            "A / - var / 20300357815"
        ]
        
        # Filtrar las filas que contienen al menos una de las palabras clave
        filtro = df['Concepto'].str.contains('|'.join(nombres_a_filtrar), case=False)
        df = df[filtro]
        
        # Mapeo de nombres
        mappings = {
            "00720088007003915204ars": "Braian Monge",
            "A / - var / 20389871908": "Guillermo Gribaudo",
            "00720742007000177128ars": "Federico Saffores",
            "A / - var / 20340458487": "Cristian Almada",
            "A / - var / 20438919717": "Emilio Borovski",
            "A / - var / 20300357815": "Nicolas Vilariño"
        }
        
        df['Concepto'] = df['Concepto'].replace(mappings)
        
        return df

def sueldos():      
    st.subheader("Cargar archivo PDF:")
    pdf_file = st.file_uploader("Cargar archivo PDF", type=['pdf'])
    
    if pdf_file is not None:
        st.write("Archivo cargado correctamente!")
        st.write(f"Nombre del archivo: {pdf_file.name}")
        
        if st.button("Procesar PDF"):
            df = procesar_pdf(pdf_file)
            st.subheader("Resultados:")
            st.dataframe(df)
            
            # Botón de descarga en Excel
            csv = df.to_csv(index=False)
            st.download_button("Descargar CSV", csv, file_name='sueldos.csv', mime='text/csv')
    else:
        st.warning("Por favor, carga un archivo PDF para comenzar el procesamiento.")



