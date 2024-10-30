import requests
import streamlit as st
import pandas as pd
import time

# Función para cargar los datos
def load_data():
    data = requests.get("https://iph5309hnj.execute-api.us-east-1.amazonaws.com/dev/search-observations").json()
    events = [
        {"event": notice["event"], "id": notice["id"], "observation": notice["observation"], "status": notice["status"], "date": notice["date"], "plate" : notice["plate"]}
        for notice in data["notices"]
    ]
    df = pd.DataFrame(events)
    df.rename(columns={"plate": "Placa", 
                       "observation": "Seguimiento", 
                       "date": "Fecha", 
                       "event": "Aviso", 
                       "status": "Estado"}, inplace=True)

    # Reordenar las columnas según el nuevo nombre
    df = df.reindex(columns=["Placa", "Aviso", "Estado", "Fecha", "Seguimiento"]) 
    #df = df.set_index('Placa', inplace=True)
 

    return df
    
def send_to_api(data, session_id):
    """Send a message to the API and return the messageResponse."""
    url = "https://iph5309hnj.execute-api.us-east-1.amazonaws.com/dev/chat-astra"  # Define the endpoint URL
    payload = {"message": data, "sessionId": session_id}  # Define the payload

    try:
        response = requests.post(url, json=payload)  # Make the POST request
        response.raise_for_status()  # Check for HTTP errors
        return response.json().get("messageResponse", "No messageResponse found")  # Extract messageResponse
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None  # Return None if there's an error
        
st.sidebar.image("https://liferaydev.subocol.com/image/layout_set_logo?img_id=190413&t=1729768369284", use_column_width=True)

st.markdown(
    """
    <style>
 
    .stSidebar, .st-emotion-cache-1gv3huu {
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
    .stTable  {
        font-size: 13px;
        font-weight: 400;
        color: #647281
    }
    
    .stTable .row_heading, .stTable  .blank   {
    border-left: 9px solid #90f0b6;
    border-radius: 8px;
    display:none;
    }
    </style>
    <div class="footer">
        <p>Powered by <b>Subocol</b></p>
    </div>
    """,
    unsafe_allow_html=True
)






    

# Cargar los datos iniciales
if 'df' not in st.session_state:
    st.session_state['df'] = load_data()  # Cargar datos al iniciar la aplicación
    
st.title("Seguimiento a la reparación")
num_columns = len(st.session_state['df'].columns)-1
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
    <span style='font-size: 20px; border-radius: 13px; height: 27px; width: auto; background-color: #ffb92b; color: #FFF; font-size: 16px; font-weight: 700;padding:5px 15px'>
        {num_columns}
    </span>
</p>
""")





st.table(st.session_state['df'])  # Mostrar la tabla

# Botón para recargar los datos
if st.button("Recargar datos"):
    st.session_state['df'] = load_data()  # Recargar los datos
    st.rerun()  # Mostrar la nueva tabla


          
with st.sidebar.popover("Chatea con ASTRA"):
  
    ############################ CHAT ##################################

    # Use the sidebar for chat and add a container for the card
    sidebar = st
    sidebar.header("Chatea con ASTRA 👋")



    # Input box for user messages
    if prompt := sidebar.text_input("Escribe tu mensaje aquí...", key="chat_input"):
        # Add the user's message to the session
        st.session_state.messages.append({"role": "Usuario", "content": prompt})
        # Display user's message immediately in card format
        role_color = "blue"
        sidebar.markdown(
            f"""
            <div style="border: 1px solid {role_color}; padding: 10px; margin-bottom: 5px; border-radius: 5px;">
                <strong style="color: {role_color};">Usuario:</strong>
                <p>{prompt}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

        # Automated response (replace with AI or custom logic)
        session_id = "340f3c1d-d69e-475b-bb31-c1bbbf8ce8b9"
        

        response = send_to_api(prompt, session_id)
        st.session_state.messages.append({"role": "Astra", "content": response})
        role_color = "green"
        sidebar.markdown(
            f"""
            <div style="border: 1px solid {role_color}; padding: 10px; margin-bottom: 5px; border-radius: 5px;">
                <strong style="color: {role_color};">Astra:</strong>
                <p>{response}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    # Define a card layout for displaying messages
    with sidebar.expander("Historial del chat", expanded=False):
        # Initialize session state for storing conversation history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display each message in a "card" format
        for msg in st.session_state.messages:
            role_color = "blue" if msg["role"] == "user" else "green"
            st.markdown(
                f"""
                <div style="border: 1px solid {role_color}; padding: 10px; margin-bottom: 5px; border-radius: 5px;">
                    <strong style="color: {role_color};">{msg["role"].capitalize()}:</strong>
                    <p>{msg["content"]}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )