# Función para obtener datos de la API
def obtener_datos():
    # Fetch data from the API
    response = requests.get("https://iph5309hnj.execute-api.us-east-1.amazonaws.com/dev/search-observations")
    data = response.json()
    # Extraer solo los campos relevantes
    events = [
        {"event": notice["event"], "id": notice["id"], "observation": notice["observation"], "status": notice["status"]}
        for notice in data["notices"]
    ]
    # Convertir los datos a un DataFrame
    df = pd.DataFrame(events)
    # Renombrar columnas
    df.rename(columns={"event": "Aviso", "observation": "Observaciones"}, inplace=True)
    return df

# Función para mostrar la tabla de datos
def mostrar_tabla():
    st.title("Observaciones")
    df = obtener_datos()  # Obtener datos
    st.table(df)  # Mostrar tabla con los datos

# Interfaz de la aplicación
def mostrar_interfaz():
    st.sidebar.image("https://liferaydev.subocol.com/image/layout_set_logo?img_id=190413&t=1729768369284", use_column_width=True)

    st.markdown(
        """
        <style>
        /* Cambiar color de fondo */
        .stSidebar {
            background-color: #0D4D64;
        }
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            text-align: center;
            color: #85a4a7;
            margin: 30px auto;
            font-family: 'Montserrat', system-ui !important;
            font-size: 13px !important;
        }
        </style>
        <div class="footer">
            <p>Powered by <b>Subocol</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    menu = st.sidebar.selectbox(
        "",
        ("Inicio", "Observaciones", "Acerca de", "Contacto", "Ayuda")
    )

    # Display the logo from a URL
    logo_url = "https://i1.sndcdn.com/avatars-TUVYyVNGNRk1TF07-p27gng-t500x500.jpg"
    st.image(logo_url, width=200)

# Programa principal
def main():
    mostrar_interfaz()  # Mostrar interfaz básica

    # Mostrar la tabla de datos inicialmente
    mostrar_tabla()

    # Botón para recargar datos
    if st.button("Recargar datos"):
        st.write("Recargando datos...")
        mostrar_tabla()  # Vuelve a cargar y mostrar los datos actualizados

# Ejecutar la aplicación
if __name__ == "__main__":
    main()