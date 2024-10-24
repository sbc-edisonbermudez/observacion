import requests
import streamlit as st
import pandas as pd
import streamlit as st


original_title = '<h1 style="font-family: serif; color:white; font-size: 20px;">Streamlit CSS Styling✨ </h1>'
st.markdown(original_title, unsafe_allow_html=True)


# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)

st.text_input("", placeholder="Streamlit CSS ")

input_style = """
<style>
input[type="text"] {
    background-color: transparent;
    color: #a19eae;  // This changes the text color inside the input box
}
div[data-baseweb="base-input"] {
    background-color: transparent !important;
}
[data-testid="stAppViewContainer"] {
    background-color: transparent !important;
}
</style>
"""
st.markdown(input_style, unsafe_allow_html=True)



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

