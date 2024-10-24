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
    df.rename(columns={"plate": "Placa", 
                       "observation": "Nota", 
                       "date": "Fecha", 
                       "event": "Aviso", 
                       "status": "Estado"}, inplace=True)

    # Reordenar las columnas según el nuevo nombre
    df = df.reindex(columns=["Placa", "Aviso", "Estado", "Fecha", "Nota"]) 
    
    return df

# Cargar los datos iniciales
if 'df' not in st.session_state:
    st.session_state['df'] = load_data()  # Cargar datos al iniciar la aplicación
    



st.title("Observaciones")
st.html(f"""
<p>
    <span style='font-family: "Roboto"; font-size: 20px; color: #025a7a; font-weight: 500;'>
        Taller: 
    </span>
    <span style='font-family: "font-family: 'Roboto';
    font-size: 17px;
    font-weight: 500;
    color: #1e80a2;
        '>
        TOBON AUTOS
    </span>
</p>
""")
st.html(f"""
<p>
    <span style='font-family: "Roboto"; font-size: 20px; color: #025a7a; font-weight: 500;'>
        Total Avisos: 
    </span>
    <span style='font-size: 20px; border-radius: 13px; height: 27px; width: auto; background-color: #ffb92b; color: #FFF; font-size: 16px; font-weight: 700;padding:5px'>
        {num_columns}
    </span>
</p>
""")

st.table(st.session_state['df'])  # Mostrar la tabla
num_columns = len(st.session_state['df'].columns)-1





# Botón para recargar los datos
if st.button("Recargar datos"):
    st.session_state['df'] = load_data()  # Recargar los datos
    st.rerun()  # Mostrar la nueva tabla

