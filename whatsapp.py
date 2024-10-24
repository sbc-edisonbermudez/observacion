import requests
import streamlit as st
import pandas as pd
import streamlit as st


st.markdown(
    """
    <style>
    /* Cambiar color de fondo */
    .main {
        background-color: #f0f2f6;
    }
    /* Cambiar color de fondo de la barra lateral */
    .css-1d391kg {
        background-color: #f4f4f4;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.image("https://liferaydev.subocol.com/image/layout_set_logo?img_id=190413&t=1729768369284", use_column_width=True)
# Título de la aplicación
st.title("Mi Aplicación con Menú Lateral")

# Crear una barra lateral con opciones de menú
menu = st.sidebar.selectbox(
    "Menú",
    ("Inicio", "Acerca de", "Contacto", "Ayuda")
)


# Display the logo from a URL
logo_url = "https://i1.sndcdn.com/avatars-TUVYyVNGNRk1TF07-p27gng-t500x500.jpg"
st.image(logo_url, width=200)  # Adjust width as needed

# Fetch data from the API
data = requests.get("https://iph5309hnj.execute-api.us-east-1.amazonaws.com/dev/search-observations").json()


st.title("Observaciones!")

# Extract only the "event" field from each notice
events = [
    {"event": notice["event"], "id": notice["id"], "observation": notice["observation"], "status": notice["status"]}
    for notice in data["notices"]
]
# Convert the extracted events into a DataFrame
df = pd.DataFrame(events)

# Rename the "event" column to "aviso"
df.rename(columns={"event": "Aviso","observation": "Observaciones",}, inplace=True)


# Display the events in a table
st.table(df)

