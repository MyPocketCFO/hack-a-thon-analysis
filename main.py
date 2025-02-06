import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="FinBot",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to set theme colors and button styles
st.markdown("""
    <style>
    .stApp {
        background-color: white;
    }
    .stButton>button {
        background-color: white !important;
        color: #6bc72e !important;
        border: 2px solid #6bc72e !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background-color: #6bc72e !important;
        color: white !important;
    }
    .stTextInput>div>div>input {
        border-color: #6bc72e;
    }
    .sidebar-content {
        padding-top: 2rem;
    }
    .main-content {
        padding-top: 2rem;
    }
    .stTitle {
        color: #6bc72e;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("main_logo.png", width=600)  # Increased logo size even more
    st.header("Company Information")
    company_name = st.text_input("Enter company name:")
    if company_name:
        st.write(f"Analyzing: {company_name}")
        # Placeholder for company information
        st.write("Company Description:")
        st.write("Industry: Finance")
        st.write("Founded: 2000")
        st.write("Headquarters: New York, USA")

# Main content
st.markdown("<h1 style='color:#6bc72e;'>FinBot</h1>", unsafe_allow_html=True)

# FinBot description
st.write("""
I'm FinBot, your helping hand for in-depth financial analysis. I analyze company financials to identify key trends, risks, and opportunities.
""")

if company_name:
    if st.button("Start Analysis"):
        st.subheader("Financial Analysis Report")
        
        # Placeholder for financial analysis report
        st.write("Detailed financial analysis report goes here.")
        
        # Placeholder for financial data table
        data = {
            'Metric': ['Revenue', 'Net Income', 'Total Assets', 'Total Liabilities'],
            'Value': ['$1,000,000', '$200,000', '$5,000,000', '$2,000,000']
        }
        df = pd.DataFrame(data)
        st.table(df)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Generate Visualizations"):
                st.subheader("Financial Visualizations")
                
                # Placeholder for a sample chart
                fig = go.Figure(data=[go.Bar(x=['Revenue', 'Expenses', 'Profit'], y=[1000, 800, 200])])
                fig.update_layout(title="Financial Overview")
                st.plotly_chart(fig)
        
        with col2:
            if st.button("Edit Information"):
                st.subheader("Edit Company Information")
                st.write("Form for editing company information goes here.")

else:
    st.write("Please enter a company name in the sidebar to begin analysis.")
