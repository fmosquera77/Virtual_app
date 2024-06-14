import streamlit as st
from gestion_usuarios import gestion_usuarios
from facturas_cobradas import facturas_cobradas
from sueldos import sueldos
from planilla_cuenta_bancaria import planilla_cuenta_bancaria
from planilla_tarjeta import planilla_tarjeta
from planilla_iva_contador import planilla_iva_contador

def main():
    st.title("Administración Virtual")

    menu = ["Inicio", "Gestión de Usuarios", "Facturas cobradas", "Sueldos", "Planilla Cuenta Bancaria", "Planilla Tarjeta", "Planilla IVA Contador"]
    choice = st.sidebar.selectbox("Menú", menu)

    if choice == "Inicio":
        st.subheader("Inicio")
        st.write("Bienvenido a la aplicación de Administración Virtual.")
        st.write("Selecciona una opción del menú desplegable a la izquierda para empezar.")

    elif choice == "Gestión de Usuarios":
        st.subheader("Gestión de Usuarios")
        gestion_usuarios()

    elif choice == "Facturas cobradas":
        st.subheader("Facturas cobradas")
        facturas_cobradas()

    elif choice == "Sueldos":
        st.subheader("Sueldos")
        sueldos()

    elif choice == "Planilla Cuenta Bancaria":
        st.subheader("Planilla Cuenta Bancaria")
        planilla_cuenta_bancaria()

    elif choice == "Planilla Tarjeta":
        st.subheader("Planilla Tarjeta")
        planilla_tarjeta()

    elif choice == "Planilla IVA Contador":
        st.subheader("Planilla IVA Contador")
        planilla_iva_contador()

if __name__ == '__main__':
    main()
