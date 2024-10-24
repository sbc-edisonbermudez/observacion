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
    ("Observaciones", "Acerca de", "Contacto", "Ayuda")
)

# Mostrar el logo
logo_url = "https://i1.sndcdn.com/avatars-TUVYyVNGNRk1TF07-p27gng-t500x500.jpg"
st.image(logo_url, width=200)

# Función para cargar los datos
def load_data():
    data = requests.get("https://iph5309hnj.execute-api.us-east-1.amazonaws.com/dev/search-observations").json()
    events = [
        {"event": notice["event"], "id": notice["id"], "observation": notice["observation"], "status": notice["status"]}
        for notice in data["notices"]
    ]
    df = pd.DataFrame(events)
    df.rename(columns={"event": "Aviso", "observation": "Observaciones"}, inplace=True)
    return df

# Estado para controlar si se han cargado los datos
if 'data_loaded' not in st.session_state:
    st.session_state['data_loaded'] = False

# Cargar los datos iniciales
if not st.session_state['data_loaded']:
    df = load_data()
    st.session_state['data_loaded'] = True
    st.session_state['df'] = df

# Mostrar la tabla inicialmente
st.title("Observaciones")
st.table(st.session_state['df'])

# Botón para recargar los datos
if st.button("Recargar datos"):
    df = load_data()  # Recargar los datos
    st.session_state['df'] = df  # Actualizar el estado
    st.table(st.session_state['df'])  # Mostrar la nueva tabla