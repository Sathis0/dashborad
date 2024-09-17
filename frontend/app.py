import streamlit as st
import requests
import plotly.graph_objects as go
import json

# Streamlit interface
st.title("Natural Language Query Interface")

# Input box for user to enter queries
query = st.text_input("Ask a question about the data (e.g., 'Show commit statistics'):")

# Process the query when the user clicks the button
if st.button('Submit'):
    if query:
        # Send the query to the FastAPI backend
        response = requests.post("http://127.0.0.1:8000/query", json={"question": query})

        # Check if the response contains a graph
        if response.status_code == 200:
            result = response.json()

            if "graph" in result:
                # Load the Plotly graph from JSON
                fig = go.Figure(json.loads(result["graph"]))
                st.plotly_chart(fig)
            else:
                st.write(result.get("message", "No relevant data found."))

    else:
        st.write("Please enter a query.")
