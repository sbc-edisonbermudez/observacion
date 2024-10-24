import requests
import streamlit as st
import pandas as pd
import streamlit as st

page_bg_img = '''
    <style>
    .reportview-container {
        background: url("Orbikabackground.PNG")
    }
   .sidebar .sidebar-content {
        background: url("Orbikabackground.PNG")
    }
    </style>
'''


st.markdown(page_bg_img, unsafe_allow_html=True)




# Display the logo from a URL
logo_url = "https://i1.sndcdn.com/avatars-TUVYyVNGNRk1TF07-p27gng-t500x500.jpg"
st.image(logo_url, width=200)  # Adjust width as needed

# Fetch data from the API
data = requests.get("https://iph5309hnj.execute-api.us-east-1.amazonaws.com/dev/search-observations").json()


st.title("Observaciones")

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

