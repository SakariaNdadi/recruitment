import streamlit as st
import plotly.express as px
import pandas as pd
import requests
from datetime import datetime

response = requests.get("http://127.0.0.1:8000/dashboard/profile_data/")


def display():
    st.title("Company Overview")

    if response.status_code == 200:
        profile_data = response.json()

        # Convert JSON data to DataFrame
        df = pd.DataFrame(profile_data)

        # Create different graphs based on user_type
        user_types = df["user_type"].unique()

        st.subheader(f"Graphs for Users in the organization")
        gender_fig = px.bar(
            df,
            x="user_type",
            color="gender",
            barmode="overlay",
            title="Gender Distribution",
        )
        population_group_fig = px.bar(
            df,
            x="user_type",
            color="population_group",
            barmode="group",
            title="Population Groups",
        )
        col1, col2 = st.columns(spec=2)

        with col1:
            st.plotly_chart(gender_fig, use_container_width=100)

        with col2:
            st.plotly_chart(population_group_fig, use_container_width=100)

        nationality_fig = px.scatter(df, y="nationality", x="user_type")
        st.plotly_chart(nationality_fig)

        # Calculate age based on the current year
        current_year = datetime.now().year
        df['age'] = df['date_of_birth'].apply(lambda x: current_year - int(x.split('-')[0]) if x and x != 'None' else None)

        age_fig = px.line(df, x="position", y='age', title='Age Based on Year of Birth and User Type')

        # Show the plot
        st.plotly_chart(age_fig)

    else:
        st.error(f"Error fetching data. Status code: {response.status_code}")
