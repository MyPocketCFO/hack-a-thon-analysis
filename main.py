import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
from financial_analysis import generate_market_report_perplexity, analyze_company_standing, calculate_averages_using_ai, generate_visualizations


# Set page config
st.set_page_config(page_title="FinBot", page_icon="/Users/mehak/Documents/GitHub/hack-a-thon-analysis/images/logo.png", layout="wide")

# Define colors
primary_color = "#6bc72e"
text_color = "#333333"

# Custom CSS to remove any red and force green styling
st.markdown(f"""
    <style>
    /* Global Styles */
    .stApp {{
        background-color: #ffffff;
        font-family: 'Arial', sans-serif;
    }}
    .stSidebar {{
        background-color: {primary_color};
        padding: 20px;
    }}
    .stSidebar h3, .stSidebar h4, .stSidebar .highlight {{
        color: white;
        font-size: 1.2em;
        font-weight: bold;
    }}
    .stSidebar p {{
        color: {text_color};
    }}

    /* Button Styles */
    .stButton > button {{
        background-color: white;
        color: {primary_color};
        border: 2px solid {primary_color};
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }}
    .stButton > button:hover, .stButton > button:focus, .stButton > button:active {{
        background-color: {primary_color} !important;
        color: white !important;
        border: 2px solid {primary_color} !important;
        outline: none !important;
        box-shadow: none !important;
    }}

    /* Input Fields without green borders */
    input, textarea, select {{
        border: 1px solid #cccccc !important;
        border-radius: 5px;
        padding: 5px;
        background-color: white !important;
        color: {text_color} !important;
    }}

    /* Remove focus shadow */
    input:focus, textarea:focus, select:focus {{
        outline: none !important;
        box-shadow: none !important;
    }}

    /* Expander Styles */
    .stExpander {{
        border: 1px solid #d3d3d3;
    }}
    .stExpander:hover, .stExpander:focus, details[open] summary {{
        border-color: {primary_color} !important;
        color: {primary_color} !important;
        outline: none !important;
    }}
    details summary:hover {{
        color: {primary_color} !important;
    }}

    /* Navigation Tabs with single green underline */
    .stTabs [data-baseweb="tab"] {{
        height: 45px;
        background-color: #fefefd;
        border-radius: 8px 8px 0px 0px;
        font-weight: bold;
        padding: 12px;
        color: {text_color} !important;
        border-bottom: none;
    }}
    
    /* Active tab: Force single green underline */
    .stTabs [aria-selected="true"] {{
        color: {primary_color} !important;
        border-bottom: 3px solid {primary_color} !important;
    }}

    /* Ensure no red focus outline or shadow */
    *:focus, *:active, *:hover {{
        outline: none !important;
        box-shadow: none !important;
    }}

    /* Override any remaining red borders */
    [data-baseweb="tab-highlight"] {{
        background-color: transparent !important;
    }}

    /* Green headings */
    h1, h2, h3 {{
        color: {primary_color} !important;
    }}

    /* FinBot image alignment */
    .finbot-image {{
        display: flex;
        justify-content: flex-end;
        align-items: flex-end;
        height: 100%;
    }}

    /* White text for sidebar title */
    .sidebar-title {{
        color: white !important;
    }}

    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'company_name' not in st.session_state:
    st.session_state.company_name = ""
if 'market_report' not in st.session_state:
    st.session_state.market_report = ""
if 'show_prompt' not in st.session_state:
    st.session_state.show_prompt = False

# Load images
main_logo = Image.open("/Users/mehak/Documents/GitHub/hack-a-thon-analysis/images/main_logo.png")
overview_image = Image.open("/Users/mehak/Documents/GitHub/hack-a-thon-analysis/images/overview.jpeg")
finbot_image = Image.open("/Users/mehak/Documents/GitHub/hack-a-thon-analysis/images/finbot.jpg")

# Sidebar with branding and description
with st.sidebar:
    st.image(main_logo, use_container_width=True)
    st.markdown("""
        <h3 class="sidebar-title">mypocketCFO: Your Financial Companion</h3>
        
        mypocketCFO is an innovative financial management tool designed to empower small businesses and entrepreneurs. Our AI-driven platform provides real-time financial insights, predictive analytics, and personalized recommendations to help you make informed decisions and drive growth.
        
        <h4>Key features:</h4>
        
        - Automated bookkeeping and financial reporting
        - Cash flow forecasting and budget optimization
        - Customized financial advice and strategy planning
        - Integration with popular accounting software
        
        <p class="highlight">Let mypocketCFO be your trusted financial partner on your journey to success!</p>
    """, unsafe_allow_html=True)

# Tabs for navigation
tab1, tab2 = st.tabs(["Overview", "Analysis"])

with tab1:
    st.header("Overview", help="Company overview and market insights")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Company Information")
        st.write("Enter the company name")
        company_name = st.text_input("Company Name", value=st.session_state.company_name, key="company_name_input", label_visibility="collapsed")
        if st.button("Enter"):
            if not company_name:
                st.session_state.show_prompt = True
                st.session_state.company_name = ""
                st.session_state.market_report = ""
            else:
                st.session_state.company_name = company_name
                st.session_state.market_report = generate_market_report_perplexity(company_name)
                st.session_state.show_prompt = False
        
        if st.session_state.show_prompt:
            st.markdown('<p class="prompt-box">Please enter a company name</p>', unsafe_allow_html=True)
    
    with col2:
        st.image(overview_image, use_container_width=True)
    
    if st.session_state.market_report:
        st.subheader("Market Report")
        st.markdown(f'<p class="market-insights">{st.session_state.market_report}</p>', unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header("FinBot", help="AI-powered financial analysis")
        st.write("**FinBot provides a deep dive into financial performance, identifying key trends and risks.**")
        start_analysis = st.button("Start Analysis")
    
    with col2:
        st.markdown('<div class="finbot-image">', unsafe_allow_html=True)
        st.image(finbot_image, width=500)  # Adjust the width as needed
        st.markdown('</div>', unsafe_allow_html=True)
    
    if start_analysis:
        if not st.session_state.company_name:
            st.markdown('<p class="prompt-box">Enter a company name in Overview first.</p>', unsafe_allow_html=True)
        elif not st.session_state.market_report:
            st.markdown('<p class="prompt-box">Generate the market report in Overview first.</p>', unsafe_allow_html=True)
        else:
            # Perform analysis
            company_1_statement = 'data/original_data.csv'
            with open(company_1_statement, 'r') as f:
                company_1_statement_content = f.read()
            
            file_paths_companies_2_to_9 = [
                'data/synthetic_data_4.csv',
                'data/synthetic_data_5.csv',
                'data/synthetic_data_6.csv',
            ]
            documents_companies_2_to_9 = [open(file, 'r').read() for file in file_paths_companies_2_to_9]
            
            industry_averages = calculate_averages_using_ai(documents_companies_2_to_9, st.session_state.company_name)
            company_standing = analyze_company_standing(company_1_statement_content, industry_averages, st.session_state.market_report, st.session_state.company_name)
            
            with st.expander("Financial Metrics"):
                st.markdown(company_standing, unsafe_allow_html=True)
            
            with st.expander("Visualizations"):
                figures = generate_visualizations()
                for fig in figures:
                    st.pyplot(fig)
            
            with st.expander("Edit Information"):
                edit_info = st.text_area("Changes", label_visibility="collapsed")
                if st.button("Submit Changes"):
                    st.success("Changes submitted successfully!")
