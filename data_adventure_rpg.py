import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time

# Page configuration
st.set_page_config(
    page_title="Data Adventure RPG",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .achievement-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0.5rem;
        border-radius: 8px;
        color: white;
        margin: 0.5rem 0;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Title and Introduction
st.markdown('<div class="main-header"><h1>🕵️‍♂️ Data Adventure RPG</h1></div>', unsafe_allow_html=True)
st.markdown(
    "Welcome, Data Detective! Embark on a quest to solve the city's data mysteries. "
    "Complete each challenge to unlock the next stage of your adventure."
)

# Initialize session state for game progress
if 'progress' not in st.session_state:
    st.session_state.progress = "character_setup"
if 'achievements' not in st.session_state:
    st.session_state.achievements = []
if 'avatar' not in st.session_state:
    st.session_state.avatar = None
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'specialty' not in st.session_state:
    st.session_state.specialty = ""
if 'case' not in st.session_state:
    st.session_state.case = ""
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'experience' not in st.session_state:
    st.session_state.experience = 0
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'completed_challenges' not in st.session_state:
    st.session_state.completed_challenges = []
if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.now()

# Sidebar navigation and stats
with st.sidebar:
    st.header("🎮 Game Stats")
    
    # Progress bar for level
    st.progress(st.session_state.experience / 100)
    st.metric("Level", st.session_state.level)
    st.metric("Score", st.session_state.score)
    st.metric("Experience", f"{st.session_state.experience}/100")
    
    # Timer
    if st.session_state.progress != "character_setup":
        elapsed_time = datetime.now() - st.session_state.start_time
        st.metric("Time Elapsed", f"{elapsed_time.seconds//60}m {elapsed_time.seconds%60}s")
    
    # Inventory
    if st.session_state.inventory:
        st.header("🎒 Inventory")
        for item in st.session_state.inventory:
            st.write(f"• {item}")
    
    # Achievements
    if st.session_state.achievements:
        st.header("🏆 Achievements")
        for achievement in st.session_state.achievements:
            st.markdown(f'<div class="achievement-card">🏅 {achievement}</div>', unsafe_allow_html=True)
    
    # Avatar display
    if st.session_state.get('avatar'):
        st.image(st.session_state.avatar, caption=f"{st.session_state.name}'s avatar", width=150)

### Character Setup
if st.session_state.progress == "character_setup":
    st.header("👤 Character Setup")
    
    # Create tabs for different setup sections
    tab1, tab2, tab3 = st.tabs(["🎭 Avatar & Identity", "🎯 Skills & Specialty", "🎨 Customization"])
    
    with tab1:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            uploaded_avatar = st.file_uploader("Upload your avatar", type=['png', 'jpg', 'jpeg'])
            if uploaded_avatar is not None:
                st.session_state.avatar = uploaded_avatar
                st.image(st.session_state.avatar, caption="Your Avatar")
        
        with col2:
            st.session_state.name = st.text_input("Enter your detective name", placeholder="Sherlock Data")
            
            # Color picker for theme
            theme_color = st.color_picker("Choose your theme color", "#667eea")
            st.session_state.theme_color = theme_color
            
            # Date picker for birth date
            birth_date = st.date_input("When did you start your data journey?")
            st.session_state.birth_date = birth_date
    
    with tab2:
        st.session_state.specialty = st.selectbox(
            "Choose your specialty",
            ["Data Analyst", "Machine Learning Engineer", "Data Visualization Expert", "Statistical Detective", "Business Intelligence Agent"]
        )
        
        # Skills with sliders
        st.write("Rate your skills (1-10):")
        col1, col2 = st.columns(2)
        
        with col1:
            python_skill = st.slider("Python", 1, 10, 5)
            sql_skill = st.slider("SQL", 1, 10, 5)
            stats_skill = st.slider("Statistics", 1, 10, 5)
        
        with col2:
            ml_skill = st.slider("Machine Learning", 1, 10, 5)
            viz_skill = st.slider("Data Visualization", 1, 10, 5)
            domain_skill = st.slider("Domain Knowledge", 1, 10, 5)
        
        st.session_state.skills = {
            "Python": python_skill,
            "SQL": sql_skill,
            "Statistics": stats_skill,
            "Machine Learning": ml_skill,
            "Data Visualization": viz_skill,
            "Domain Knowledge": domain_skill
        }
        
        # Skills visualization
        skills_df = pd.DataFrame(list(st.session_state.skills.items()), columns=['Skill', 'Level'])
        fig = px.bar(skills_df, x='Skill', y='Level', title="Your Skills Profile")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Preferences
        st.write("Game Preferences:")
        st.session_state.difficulty = st.select_slider(
            "Difficulty Level",
            options=["Easy", "Medium", "Hard", "Expert"],
            value="Medium"
        )
        
        st.session_state.sound_enabled = st.checkbox("Enable sound effects", value=True)
        st.session_state.animations = st.checkbox("Enable animations", value=True)
        
        # Time limit preference
        time_limit = st.radio("Case Time Limit", ["No Limit", "30 minutes", "1 hour", "2 hours"])
        st.session_state.time_limit = time_limit
    
    # Begin adventure button
    if st.button("🚀 Begin Adventure!", type="primary", use_container_width=True):
        if st.session_state.name:
            st.session_state.progress = "case_selection"
            st.session_state.achievements.append("Character created!")
            st.session_state.score += 50
            st.session_state.experience += 20
            st.rerun()
        else:
            st.error("Please enter your detective name!")

### Case Selection
elif st.session_state.progress == "case_selection":
    st.header("📋 Case Selection")
    
    st.write(f"Welcome, **{st.session_state.name}**! Choose your next mystery to solve.")
    
    # Case cards with expandable details
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.expander("🔍 Missing Data Case", expanded=True):
            st.write("**Difficulty:** Easy")
            st.write("**Skills needed:** Data cleaning, basic analysis")
            st.write("**Reward:** 100 XP")
            st.write("A local business has missing sales data. Help them recover and analyze the information.")
            
            if st.button("Take Case", key="case1"):
                st.session_state.case = "Missing Data"
                st.session_state.progress = "data_lab"
                st.session_state.achievements.append(f"Case selected: {st.session_state.case}")
                st.session_state.score += 25
                st.rerun()
    
    with col2:
        with st.expander("📊 Outlier Detective", expanded=True):
            st.write("**Difficulty:** Medium")
            st.write("**Skills needed:** Statistical analysis, visualization")
            st.write("**Reward:** 200 XP")
            st.write("Detect and investigate suspicious patterns in financial data.")
            
            if st.button("Take Case", key="case2"):
                st.session_state.case = "Outlier Detective"
                st.session_state.progress = "data_lab"
                st.session_state.achievements.append(f"Case selected: {st.session_state.case}")
                st.session_state.score += 50
                st.rerun()
    
    with col3:
        with st.expander("📈 Trend Analyzer", expanded=True):
            st.write("**Difficulty:** Hard")
            st.write("**Skills needed:** Time series analysis, forecasting")
            st.write("**Reward:** 300 XP")
            st.write("Analyze market trends and predict future patterns.")
            
            if st.button("Take Case", key="case3"):
                st.session_state.case = "Trend Analyzer"
                st.session_state.progress = "data_lab"
                st.session_state.achievements.append(f"Case selected: {st.session_state.case}")
                st.session_state.score += 75
                st.rerun()
    
    # Back button
    if st.button("⬅️ Back to Setup"):
        st.session_state.progress = "character_setup"
        st.rerun()

### Data Lab
elif st.session_state.progress == "data_lab":
    st.header("🔬 Data Lab")
    
    # Case-specific data generation
    if st.session_state.case == "Missing Data":
        # Generate data with missing values
        np.random.seed(42)
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        sales_data = pd.DataFrame({
            'Date': dates,
            'Sales': np.random.normal(1000, 200, 100),
            'Customers': np.random.poisson(50, 100),
            'Product_ID': np.random.choice(['A', 'B', 'C'], 100)
        })
        
        # Add missing values
        missing_indices = np.random.choice(100, 15, replace=False)
        sales_data.loc[missing_indices, 'Sales'] = np.nan
        sales_data.loc[missing_indices[:5], 'Customers'] = np.nan
        
        df = sales_data
        
    elif st.session_state.case == "Outlier Detective":
        # Generate data with outliers
        np.random.seed(42)
        normal_data = np.random.normal(100, 20, 95)
        outliers = np.random.uniform(200, 300, 5)
        all_values = np.concatenate([normal_data, outliers])
        
        df = pd.DataFrame({
            'Transaction_ID': range(1, 101),
            'Amount': all_values,
            'Category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books'], 100),
            'Customer_Type': np.random.choice(['Regular', 'VIP', 'New'], 100),
            'Hour': np.random.randint(0, 24, 100)
        })
        
    else:  # Trend Analyzer
        # Generate time series data
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=365, freq='D')
        trend = np.linspace(100, 150, 365)
        seasonal = 10 * np.sin(2 * np.pi * np.arange(365) / 365)
        noise = np.random.normal(0, 5, 365)
        
        df = pd.DataFrame({
            'Date': dates,
            'Sales': trend + seasonal + noise,
            'Temperature': np.random.normal(20, 10, 365),
            'Marketing_Spend': np.random.uniform(100, 500, 365),
            'Day_of_Week': dates.dayofweek
        })
    
    st.write(f"**Case:** {st.session_state.case}")
    st.write("Here is your case data. Explore, filter, and visualize to find clues!")
    
    # Create tabs for different analysis tools
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Data Explorer", "🔍 Analysis Tools", "📈 Visualizations", "🎯 Insights"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Raw Data")
            st.dataframe(df, use_container_width=True)
            
            # Data info
            with st.expander("📋 Data Information"):
                buffer = st.empty()
                buffer.dataframe(df.describe())
                
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.write("**Data Types:**")
                    st.write(df.dtypes)
                with col_info2:
                    st.write("**Missing Values:**")
                    st.write(df.isnull().sum())
        
        with col2:
            st.subheader("Filters")
            
            # Dynamic filters based on data
            for col in df.select_dtypes(include=[np.number]).columns:
                if col in df.columns:
                    min_val = float(df[col].min())
                    max_val = float(df[col].min())
                    if not pd.isna(min_val) and not pd.isna(max_val):
                        min_val = float(df[col].min())
                        max_val = float(df[col].max())
                        filter_range = st.slider(f"Filter {col}", min_val, max_val, (min_val, max_val))
                        df = df[(df[col] >= filter_range[0]) & (df[col] <= filter_range[1])]
            
            # Categorical filters
            for col in df.select_dtypes(include=['object']).columns:
                unique_vals = df[col].unique()
                if len(unique_vals) < 20:  # Only show if not too many unique values
                    selected_vals = st.multiselect(f"Filter {col}", unique_vals, default=unique_vals)
                    df = df[df[col].isin(selected_vals)]
    
    with tab2:
        st.subheader("Analysis Tools")
        
        # Missing data analysis
        if df.isnull().sum().sum() > 0:
            with st.expander("🔍 Missing Data Analysis"):
                missing_data = df.isnull().sum()
                missing_pct = (missing_data / len(df)) * 100
                missing_df = pd.DataFrame({
                    'Column': missing_data.index,
                    'Missing_Count': missing_data.values,
                    'Missing_Percentage': missing_pct.values
                })
                st.dataframe(missing_df)
                
                # Missing data visualization
                fig = px.bar(missing_df, x='Column', y='Missing_Percentage', 
                           title="Missing Data Percentage by Column")
                st.plotly_chart(fig, use_container_width=True)
        
        # Outlier detection
        with st.expander("🎯 Outlier Detection"):
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                selected_col = st.selectbox("Select column for outlier analysis", numeric_cols)
                
                if selected_col:
                    Q1 = df[selected_col].quantile(0.25)
                    Q3 = df[selected_col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    outliers = df[(df[selected_col] < lower_bound) | (df[selected_col] > upper_bound)]
                    
                    col_out1, col_out2 = st.columns(2)
                    with col_out1:
                        st.metric("Total Outliers", len(outliers))
                        st.metric("Outlier Percentage", f"{(len(outliers)/len(df)*100):.2f}%")
                    
                    with col_out2:
                        st.metric("Lower Bound", f"{lower_bound:.2f}")
                        st.metric("Upper Bound", f"{upper_bound:.2f}")
                    
                    if len(outliers) > 0:
                        st.write("**Outlier Data:**")
                        st.dataframe(outliers)
        
        # Correlation analysis
        with st.expander("📊 Correlation Analysis"):
            numeric_df = df.select_dtypes(include=[np.number])
            if len(numeric_df.columns) > 1:
                corr_matrix = numeric_df.corr()
                fig = px.imshow(corr_matrix, 
                               title="Correlation Matrix",
                               color_continuous_scale='RdBu')
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Data Visualizations")
        
        # Chart type selection
        chart_type = st.selectbox("Select Chart Type", 
                                 ["Line Chart", "Bar Chart", "Scatter Plot", "Histogram", "Box Plot", "Heatmap"])
        
        if chart_type == "Line Chart":
            if len(df.select_dtypes(include=[np.number]).columns) >= 2:
                x_col = st.selectbox("X-axis", df.select_dtypes(include=[np.number]).columns)
                y_col = st.selectbox("Y-axis", df.select_dtypes(include=[np.number]).columns)
                
                fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Bar Chart":
            if len(df.select_dtypes(include=[np.number]).columns) >= 1:
                x_col = st.selectbox("X-axis (categorical)", df.select_dtypes(include=['object']).columns)
                y_col = st.selectbox("Y-axis (numeric)", df.select_dtypes(include=[np.number]).columns)
                
                fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Scatter Plot":
            if len(df.select_dtypes(include=[np.number]).columns) >= 2:
                x_col = st.selectbox("X-axis", df.select_dtypes(include=[np.number]).columns)
                y_col = st.selectbox("Y-axis", df.select_dtypes(include=[np.number]).columns)
                color_col = st.selectbox("Color by (optional)", ['None'] + list(df.select_dtypes(include=['object']).columns))
                
                if color_col == 'None':
                    fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
                else:
                    fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=f"{y_col} vs {x_col}")
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Histogram":
            if len(df.select_dtypes(include=[np.number]).columns) >= 1:
                col = st.selectbox("Select column", df.select_dtypes(include=[np.number]).columns)
                bins = st.slider("Number of bins", 5, 50, 20)
                
                fig = px.histogram(df, x=col, nbins=bins, title=f"Distribution of {col}")
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Box Plot":
            if len(df.select_dtypes(include=[np.number]).columns) >= 1:
                y_col = st.selectbox("Y-axis", df.select_dtypes(include=[np.number]).columns)
                x_col = st.selectbox("X-axis (optional)", ['None'] + list(df.select_dtypes(include=['object']).columns))
                
                if x_col == 'None':
                    fig = px.box(df, y=y_col, title=f"Box Plot of {y_col}")
                else:
                    fig = px.box(df, x=x_col, y=y_col, title=f"Box Plot of {y_col} by {x_col}")
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Heatmap":
            numeric_df = df.select_dtypes(include=[np.number])
            if len(numeric_df.columns) > 1:
                corr_matrix = numeric_df.corr()
                fig = px.imshow(corr_matrix, 
                               title="Correlation Heatmap",
                               color_continuous_scale='RdBu')
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("🎯 Key Insights")
        
        # Generate insights based on the case
        if st.session_state.case == "Missing Data":
            missing_count = df.isnull().sum().sum()
            st.metric("Total Missing Values", missing_count)
            
            if missing_count > 0:
                st.success("🔍 **Insight:** You found missing data! Consider imputation strategies.")
                st.info("💡 **Tip:** Use forward fill, backward fill, or interpolation for time series data.")
            else:
                st.success("✅ **Insight:** No missing data found! Your data is clean.")
        
        elif st.session_state.case == "Outlier Detective":
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                outlier_counts = {}
                for col in numeric_cols:
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
                    outlier_counts[col] = len(outliers)
                
                max_outliers = max(outlier_counts.values())
                most_outlier_col = max(outlier_counts, key=outlier_counts.get)
                
                st.metric("Most Outliers Found", f"{max_outliers} in {most_outlier_col}")
                st.warning(f"⚠️ **Alert:** {most_outlier_col} has the most outliers. Investigate further!")
        
        else:  # Trend Analyzer
            if 'Sales' in df.columns:
                trend_direction = "increasing" if df['Sales'].iloc[-1] > df['Sales'].iloc[0] else "decreasing"
                st.metric("Trend Direction", trend_direction.title())
                st.info(f"📈 **Trend:** Sales are {trend_direction} over time.")
        
        # General insights
        st.write("**Data Summary:**")
        col_ins1, col_ins2, col_ins3 = st.columns(3)
        with col_ins1:
            st.metric("Total Records", len(df))
        with col_ins2:
            st.metric("Numeric Columns", len(df.select_dtypes(include=[np.number]).columns))
        with col_ins3:
            st.metric("Categorical Columns", len(df.select_dtypes(include=['object']).columns))
    
    # Navigation buttons
    col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 1])
    
    with col_nav1:
        if st.button("⬅️ Back to Cases"):
            st.session_state.progress = "case_selection"
            st.rerun()
    
    with col_nav2:
        if st.button("💾 Save Analysis"):
            # Save current analysis
            analysis_data = {
                'case': st.session_state.case,
                'timestamp': datetime.now().isoformat(),
                'data_shape': df.shape,
                'missing_values': df.isnull().sum().to_dict()
            }
            st.session_state.saved_analyses = st.session_state.get('saved_analyses', [])
            st.session_state.saved_analyses.append(analysis_data)
            st.success("Analysis saved!")
    
    with col_nav3:
        if st.button("🔍 I found a clue!", type="primary"):
            st.session_state.progress = "puzzle_room"
            st.session_state.achievements.append("Clue found in data!")
            st.session_state.score += 100
            st.session_state.experience += 30
            st.rerun()

### Puzzle Room
elif st.session_state.progress == "puzzle_room":
    st.header("🧩 Puzzle Room")
    
    st.write("Time for a riddle! Here's your puzzle:")
    
    # Create tabs for different puzzle types
    puzzle_tab1, puzzle_tab2, puzzle_tab3 = st.tabs(["📝 Text Puzzle", "🔢 Math Challenge", "🎯 Logic Problem"])
    
    with puzzle_tab1:
        st.markdown("**What is the capital of DataLand?**")
        answer = st.text_input("Your answer:", key="text_puzzle")
        
        if st.button("Submit Answer", key="submit_text"):
            if answer.lower() == "datatown":
                st.success("Correct! The mayor thanks you.")
                st.session_state.achievements.append("Text puzzle solved!")
                st.session_state.score += 50
                st.session_state.experience += 20
                st.balloons()
            else:
                st.error("Try again!")
    
    with puzzle_tab2:
        st.markdown("**Math Challenge:** What is the mean of [15, 20, 25, 30, 35]?")
        math_answer = st.number_input("Your answer:", key="math_puzzle")
        
        if st.button("Submit Answer", key="submit_math"):
            if math_answer == 25:
                st.success("Correct! You're a math wizard!")
                st.session_state.achievements.append("Math challenge solved!")
                st.session_state.score += 75
                st.session_state.experience += 25
                st.balloons()
            else:
                st.error("Try again! The correct answer is 25.")
    
    with puzzle_tab3:
        st.markdown("**Logic Problem:** If all data scientists love coffee, and you are a data scientist, do you love coffee?**")
        logic_answer = st.radio("Your answer:", ["Yes", "No", "Maybe"], key="logic_puzzle")
        
        if st.button("Submit Answer", key="submit_logic"):
            if logic_answer == "Yes":
                st.success("Correct! Logical thinking is key in data science!")
                st.session_state.achievements.append("Logic puzzle solved!")
                st.session_state.score += 100
                st.session_state.experience += 30
                st.balloons()
            else:
                st.error("Think about it logically!")
    
    # Progress to next stage
    if st.button("Continue to Report", type="primary"):
        st.session_state.progress = "report_station"
        st.rerun()
    
    if st.button("Give up and return to Data Lab"):
        st.session_state.progress = "data_lab"
        st.rerun()

### Report Station
elif st.session_state.progress == "report_station":
    st.header("📋 Report Station")
    
    st.write("You solved the case—great job! Here's your final report:")
    
    # Create a comprehensive report
    report = f"""
    # Data Adventure RPG Case Report
    
    ## Detective Information
    **Name:** {st.session_state.name}
    **Specialty:** {st.session_state.specialty}
    **Level:** {st.session_state.level}
    **Score:** {st.session_state.score}
    
    ## Case Details
    **Case Type:** {st.session_state.case}
    **Completion Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    **Time Elapsed:** {(datetime.now() - st.session_state.start_time).seconds//60} minutes
    
    ## Achievements Earned
    {chr(10).join([f"- {achievement}" for achievement in st.session_state.achievements])}
    
    ## Skills Demonstrated
    {chr(10).join([f"- {skill}: {level}/10" for skill, level in st.session_state.skills.items()])}
    
    ## Analysis Summary
    - Data exploration completed
    - Visualizations created
    - Insights discovered
    - Puzzle challenges solved
    
    ## Recommendations
    - Continue practicing data analysis
    - Explore more advanced techniques
    - Share findings with the team
    
    **Report Generated by:** Data Adventure RPG System
    """
    
    st.markdown(report)
    
    # Download options
    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        st.download_button(
            label="📄 Download Report (TXT)",
            data=report,
            file_name=f"data_report_{st.session_state.name}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
    
    with col_dl2:
        # Create JSON report
        json_report = {
            "detective": st.session_state.name,
            "specialty": st.session_state.specialty,
            "case": st.session_state.case,
            "score": st.session_state.score,
            "level": st.session_state.level,
            "achievements": st.session_state.achievements,
            "skills": st.session_state.skills,
            "completion_date": datetime.now().isoformat()
        }
        
        st.download_button(
            label="📊 Download Report (JSON)",
            data=json.dumps(json_report, indent=2),
            file_name=f"data_report_{st.session_state.name}_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    # Leaderboard
    st.header("🏆 Leaderboard")
    
    # Add current player to leaderboard
    player_entry = {
        'Name': st.session_state.name,
        'Case': st.session_state.case,
        'Score': st.session_state.score,
        'Level': st.session_state.level,
        'Achievements': len(st.session_state.achievements),
        'Completion_Date': datetime.now().strftime('%Y-%m-%d')
    }
    
    if player_entry not in st.session_state.leaderboard:
        st.session_state.leaderboard.append(player_entry)
    
    # Sort leaderboard by score
    leaderboard_df = pd.DataFrame(st.session_state.leaderboard)
    if not leaderboard_df.empty:
        leaderboard_df = leaderboard_df.sort_values('Score', ascending=False)
        st.dataframe(leaderboard_df, use_container_width=True)
        
        # Leaderboard visualization
        if len(leaderboard_df) > 1:
            fig = px.bar(leaderboard_df.head(10), x='Name', y='Score', 
                        title="Top 10 Detectives by Score")
            st.plotly_chart(fig, use_container_width=True)
    
    # Game completion celebration
    st.success("🎉 Congratulations! You've completed the case!")
    
    # Level up check
    if st.session_state.experience >= 100:
        st.session_state.level += 1
        st.session_state.experience = 0
        st.balloons()
        st.success(f"🎊 Level Up! You are now level {st.session_state.level}!")
    
    # New adventure button
    if st.button("🚀 Start a New Adventure", type="primary", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# Display avatar and achievements (always visible after setup)
if st.session_state.get('avatar'):
    st.sidebar.image(st.session_state.avatar, caption=f"{st.session_state.name}'s avatar")

if st.session_state.get('achievements'):
    st.sidebar.header("🏆 Achievements")
    for ach in st.session_state.achievements:
        st.markdown(f'<div class="achievement-card">🏅 {ach}</div>', unsafe_allow_html=True)
