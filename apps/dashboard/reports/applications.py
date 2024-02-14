import streamlit as st
import plotly.express as px
import pandas as pd
import requests
from datetime import datetime

bursary_response = requests.get(
    "http://127.0.0.1:8000/dashboard/bursary_applicant_data/"
)
vacancy_response = requests.get("http://127.0.0.1:8000/dashboard/vacancy_data/")


def display():
    st.title("Applications Overview")
    st.write(
        "This page displays applications that were submitted for vacancies and bursaries."
    )
    if bursary_response.status_code == 200 and vacancy_response.status_code == 200:
        bursary_data = bursary_response.json()
        vacancy_data = vacancy_response.json()
        bursary_df = pd.DataFrame(bursary_data)
        vacancy_df = pd.DataFrame(vacancy_data)

        st.write(bursary_data)
        st.write(vacancy_data)

        bursary_gender_fig = px.pie(
            bursary_df,
            color="gender",
            names="gender",
            title="Bursary Gender Distribution",
        )
        vacancy_gender_fig = px.pie(
            vacancy_df,
            color="gender",
            names="gender",
            title="Vacancy Gender Distribution",
        )

        col1, col2 = st.columns(spec=2)

        with col1:
            st.plotly_chart(bursary_gender_fig, use_container_width=100)

        with col2:
            st.plotly_chart(vacancy_gender_fig, use_container_width=100)

        # st.plotly_chart(bursary_gender_fig)

        # Calculate age based on the current year
        current_year = datetime.now().year
        bursary_df['age'] = bursary_df['date_of_birth'].apply(lambda x: current_year - int(x.split('-')[0]) if x and x != 'None' else None)

        bursary_age_fig = px.line(bursary_df, x="bursary", y='age', title='Age Based on Year of Birth and User Type')

        # Show the plot
        st.plotly_chart(bursary_age_fig)

    else:
        st.error(f"Error fetching data. Status code: {bursary_response.status_code}")

    df = pd.DataFrame(bursary_response)
