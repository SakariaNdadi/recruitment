import streamlit as sl

sl.sidebar.header("Navigation")
import streamlit as st
import company, applications

# Function to display the home page
def home_page():
    st.title("Home Page")
    st.write("Welcome to the home page!")

def company_overview():
    company.display()

def application_overview():
    applications.display()

# Sidebar navigation
selected_page = st.sidebar.radio("", ["Home", "Company", "Applications"])

# Display the selected page
if selected_page == "Home":
    home_page()

elif selected_page == "Company":
    company_overview()

elif selected_page == "Applications":
    application_overview()
