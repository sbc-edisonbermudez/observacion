import requests
import streamlit as st
import pandas as pd
import streamlit as st
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

# Display the logo from a URL
logo_url = "https://i1.sndcdn.com/avatars-TUVYyVNGNRk1TF07-p27gng-t500x500.jpg"
st.image(logo_url, width=200)  # Adjust width as needed



# Definir el intervalo de recarga en segundos
reload_interval = 5  # Cambia este valor al número de segundos deseado

# Inicializar el temporizador si no está en el estado de sesión
if 'last_updated' not in st.session_state:
    st.session_state.last_updated = time.time()

# Obtener datos de la API
def fetch_data():
    data = requests.get("https://iph5309hnj.execute-api.us-east-1.amazonaws.com/dev/search-observations").json()
    events = [
        {"event": notice["event"], "id": notice["id"], "observation": notice["observation"], "status": notice["status"]}
        for notice in data["notices"]
    ]
    df = pd.DataFrame(events)
    df.rename(columns={"event": "Aviso", "observation": "Observaciones"}, inplace=True)
    return df

# Verificar si ha pasado el intervalo de recarga
elapsed_time = time.time() - st.session_state.last_updated
if elapsed_time > reload_interval:
    # Actualizar la tabla de datos
    st.session_state.df = fetch_data()
    st.session_state.last_updated = time.time()

# Mostrar título y tabla
st.title("Observaciones")
if 'df' in st.session_state:
    st.table(st.session_state.df)

# Mostrar el tiempo restante hasta la próxima actualización
remaining_time = reload_interval - (time.time() - st.session_state.last_updated)
st.write(f"Actualizando en {int(remaining_time)} segundos...")