# app.py
import streamlit as st
from views.economic import show_mobility_ladder
from views.affordability import show_affordability_analysis

def get_page_config():
    return {
        "page_title": "College Mobility Analysis",
        "page_icon": "📚",
        "layout": "wide"
    }

def show_home():
    st.title("College Mobility Analysis Dashboard")
    
    st.markdown("""
    ### About This Dashboard
    
    This interactive dashboard explores the relationship between college affordability and economic mobility in U.S. higher education. Using data from [Opportunity Insights](https://opportunityinsights.org/), we analyze how different types of colleges contribute to intergenerational economic mobility.
    
    ### Key Metrics
    - **Economic Mobility**: The probability of moving from the bottom income quintile to the top quintile
    - **Bottom Quintile Share**: Percentage of students from the bottom 20% of the income distribution
    - **Affordability**: Both sticker price and net price (after financial aid) in 2013
    
    ### Available Analyses
    
    #### 1. Mobility vs Affordability
    - **Four Year Colleges**: Analyze mobility rates and affordability across different types of four-year institutions (Elite, Selective, etc.)
    - **Two Year Colleges**: Compare mobility outcomes between public and for-profit two-year institutions
    
    #### 2. Economic Mobility
    - **Mobility Ladder**: Visualize the probability distribution of children's income quintiles given parents from the bottom quintile
    
    ### How to Use This Dashboard
    
    1. **Select an Analysis**:
       - Use the sidebar to choose between "Mobility vs Affordability" and "Economic Mobility"
       - Select specific analyses like "Four Year Colleges" or "Mobility Ladder"
    
    2. **Interact with Filters**:
       - Filter by institution groups (e.g., Elite, Selective Public)
       - Adjust minimum thresholds for mobility rates and bottom quintile shares
       - Use the quadrant analysis to identify high-performing institutions
    
    3. **Explore the Data**:
       - Hover over data points in plots for detailed information
       - Sort tables by clicking column headers
       - Use the institution list to find specific colleges
    
    ### Data Sources
    This analysis uses data from the Mobility Report Cards: The Role of Colleges in Intergenerational Mobility (Chetty, Friedman, Saez, Turner, and Yagan, 2017).
    """)

def main():
    st.set_page_config(**get_page_config())
    
    level_1 = st.sidebar.selectbox(
        "Select Category",
        ["Home", "Mobility vs Affordability", "Economic Mobility"]
    )
    
    if level_1 == "Home":
        show_home()
        return
    
    pages = {
        "Economic Mobility": ["Mobility Ladder", "Documentation"],
        "Mobility vs Affordability": ["Four Year Colleges", "Two Year Colleges", "Documentation"]
    }
    
    selected_page = st.sidebar.selectbox(
        "Select Analysis",
        pages[level_1]
    )
    
    if level_1 == "Economic Mobility":
        if selected_page == "Mobility Ladder":
            show_mobility_ladder()
        else:
            st.info("This analysis is currently under development.")
    elif level_1 == "Mobility vs Affordability":
        if selected_page == "Four Year Colleges":
            show_affordability_analysis(iclevel=4)
        elif selected_page == "Two Year Colleges":
            show_affordability_analysis(iclevel=2)
    else:
        st.info("This analysis is currently under development.")

if __name__ == "__main__":
    main()
