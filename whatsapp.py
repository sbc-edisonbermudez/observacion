import requests
import streamlit as st
import pandas as pd
import time

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

# Insertar JavaScript para recargar la página cada 60 segundos
st.markdown(
    """
    <script>
    function reloadPage() {
        setTimeout(function() {
            window.location.reload();
            console.log("Ping")
        }, 5000); // 5000 ms = 5 segundos
    }
    reloadPage();
    </script>
    """,
    unsafe_allow_html=True
)

menu = st.sidebar.selectbox(
    "",
    ("Inicio", "Observaciones", "Acerca de", "Contacto", "Ayuda")
)

# Mostrar el logo
logo_url = "https://i1.sndcdn.com/avatars-TUVYyVNGNRk1TF07-p27gng-t500x500.jpg"
st.image(logo_url, width=200)

# Cargar los datos inicialmente
data = requests.get("https://iph5309hnj.execute-api.us-east-1.amazonaws.com/dev/search-observations").json()

st.title("Observaciones")

# Extraer solo los campos relevantes
events = [
    {"event": notice["event"], "id": notice["id"], "observation": notice["observation"], "status": notice["status"]}
    for notice in data["notices"]
]

# Convertir los datos a un DataFrame
df = pd.DataFrame(events)
# Renombrar columnas
df.rename(columns={"event": "Aviso", "observation": "Observaciones"}, inplace=True)

# Mostrar la tabla inicialmente
st.table(df)

# Botón para recargar los datos
if st.button("Recargar datos"):
    # Volver a cargar los datos cuando se presione el botón
    data = requests.get("https://iph5309hnj.execute-api.us-east-1.amazonaws.com/dev/search-observations").json()
    events = [
        {"event": notice["event"], "id": notice["id"], "observation": notice["observation"], "status": notice["status"]}
        for notice in data["notices"]
    ]
    df = pd.DataFrame(events)
    df.rename(columns={"event": "Aviso", "observation": "Observaciones"}, inplace=True)
    st.table(df)
