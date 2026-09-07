import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set page configuration (must be first Streamlit command)
st.set_page_config(
    page_title="EDA Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title
st.title("📊 Exploratory Data Analysis Dashboard")
st.markdown("---")

# Sidebar for controls
st.sidebar.header("📁 Data Upload")
uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV file",
    type=['csv'],
    help="Upload a CSV file to analyze"
)

# Initialize session state for data
if 'data' not in st.session_state:
    st.session_state.data = None

# Check if file is uploaded
if uploaded_file is not None:
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        st.session_state.data = df
        
        # Display success message
        st.sidebar.success(f"✅ File loaded: {uploaded_file.name}")
        
    except Exception as e:
        st.sidebar.error(f"❌ Error loading file: {str(e)}")
        st.session_state.data = None
else:
    # Load default titanic dataset if available
    st.sidebar.info("ℹ️ No file uploaded. You can upload a CSV file or use the demo below.")
    
    # Create a sample dataset for demonstration
    if st.sidebar.button("Load Demo Dataset"):
        # Create sample titanic-like data
        np.random.seed(42)
        demo_data = {
            'PassengerId': range(1, 101),
            'Survived': np.random.choice([0, 1], 100, p=[0.6, 0.4]),
            'Pclass': np.random.choice([1, 2, 3], 100, p=[0.24, 0.21, 0.55]),
            'Name': [f'Passenger {i}' for i in range(1, 101)],
            'Sex': np.random.choice(['male', 'female'], 100),
            'Age': np.random.randint(1, 80, 100),
            'SibSp': np.random.choice([0, 1, 2], 100),
            'Parch': np.random.choice([0, 1, 2], 100),
            'Ticket': [f'Ticket_{i}' for i in range(1, 101)],
            'Fare': np.random.uniform(10, 500, 100).round(2),
            'Cabin': np.random.choice(['A', 'B', 'C', None], 100),
            'Embarked': np.random.choice(['S', 'C', 'Q'], 100)
        }
        st.session_state.data = pd.DataFrame(demo_data)
        st.sidebar.success("✅ Demo dataset loaded!")

# Main content area
if st.session_state.data is not None:
    df = st.session_state.data
    
    # Top section: Dataset preview and metadata
    st.header("📋 Dataset Overview")
    
    # Create two columns for metadata
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dataset Dimensions")
        st.write(f"**Rows:** {df.shape[0]}")
        st.write(f"**Columns:** {df.shape[1]}")
        
        st.subheader("Column Data Types")
        dtype_df = pd.DataFrame({
            'Column': df.dtypes.index,
            'Data Type': df.dtypes.values.astype(str)
        })
        st.dataframe(dtype_df, width='stretch')
    
    with col2:
        st.subheader("Missing Values")
        missing_df = pd.DataFrame({
            'Column': df.columns,
            'Missing Count': df.isnull().sum(),
            'Missing %': (df.isnull().sum() / len(df) * 100).round(2)
        })
        st.dataframe(missing_df, width='stretch')
        
        # Statistical summary for numerical columns
        st.subheader("Statistical Summary (Numerical)")
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 0:
            stats_df = df[numerical_cols].agg(['mean', 'median', 'min', 'max']).round(2)
            st.dataframe(stats_df, width='stretch')
        else:
            st.info("No numerical columns found")
    
    st.markdown("---")
    
    # Dataset Preview
    st.subheader("📄 Dataset Preview (First 5 Rows)")
    st.dataframe(df.head(), width='stretch')
    
    st.markdown("---")
    
    # Bottom section: Visualization
    st.header("📈 Data Visualization")
    
    # Sidebar for column selection
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Analysis Controls")
    
    # Column selection dropdown
    selected_column = st.sidebar.selectbox(
        "Select Column for Analysis",
        options=df.columns,
        help="Choose a column to visualize"
    )
    
    # Automated attribute typing
    def detect_column_type(column_data):
        """Detect if column is numerical or categorical"""
        if pd.api.types.is_numeric_dtype(column_data):
            # Check if it's actually categorical (few unique values)
            if column_data.nunique() < 10:
                return "categorical"
            return "numerical"
        else:
            return "categorical"
    
    column_type = detect_column_type(df[selected_column])
    
    # Display column info
    st.sidebar.info(f"**Column Type:** {column_type.capitalize()}")
    
    # Create visualization area
    st.subheader(f"Visualization: {selected_column}")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if column_type == "numerical":
        # Histogram for numerical data
        ax.hist(df[selected_column].dropna(), bins=20, edgecolor='black', alpha=0.7)
        ax.set_xlabel(selected_column, fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title(f'Distribution of {selected_column}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add statistics
        stats_text = f"Mean: {df[selected_column].mean():.2f}  |  Median: {df[selected_column].median():.2f}"
        ax.text(0.98, 0.95, stats_text, transform=ax.transAxes,
                fontsize=10, verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
    else:
        # Bar chart for categorical data
        value_counts = df[selected_column].value_counts()
        
        # Create bar chart
        bars = ax.bar(range(len(value_counts)), value_counts.values, 
                      edgecolor='black', alpha=0.7)
        
        # Add percentage labels
        total = len(df[selected_column].dropna())
        for i, (bar, count) in enumerate(zip(bars, value_counts.values)):
            percentage = (count / total) * 100
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                   f'{count}\n({percentage:.1f}%)',
                   ha='center', va='bottom', fontsize=9)
        
        ax.set_xticks(range(len(value_counts)))
        ax.set_xticklabels(value_counts.index, rotation=45, ha='right')
        ax.set_xlabel(selected_column, fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title(f'Frequency Distribution of {selected_column}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Additional statistics
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Column Statistics")
        if column_type == "numerical":
            stats = {
                'Mean': df[selected_column].mean(),
                'Median': df[selected_column].median(),
                'Std Dev': df[selected_column].std(),
                'Min': df[selected_column].min(),
                'Max': df[selected_column].max()
            }
        else:
            stats = {
                'Unique Values': df[selected_column].nunique(),
                'Mode': df[selected_column].mode().iloc[0] if len(df[selected_column].mode()) > 0 else 'N/A',
                'Most Frequent Count': df[selected_column].value_counts().iloc[0]
            }
        
        for key, value in stats.items():
            if column_type == "numerical" and isinstance(value, (int, float)):
                st.write(f"**{key}:** {value:.2f}")
            else:
                st.write(f"**{key}:** {value}")
    
    with col2:
        st.subheader("💡 Quick Insights")
        if column_type == "numerical":
            st.write(f"• Column has {df[selected_column].isnull().sum()} missing values")
            st.write(f"• Distribution appears {'normal' if abs(df[selected_column].skew()) < 0.5 else 'skewed'}")
            st.write(f"• Range: {df[selected_column].max() - df[selected_column].min():.2f}")
        else:
            top_category = df[selected_column].value_counts().index[0]
            top_percentage = (df[selected_column].value_counts().iloc[0] / len(df) * 100)
            st.write(f"• Most common: {top_category}")
            st.write(f"• Represents {top_percentage:.1f}% of data")
            st.write(f"• Number of categories: {df[selected_column].nunique()}")

else:
    # Display instructions when no data is loaded
    st.info("👈 **Please upload a CSV file using the sidebar or load the demo dataset to begin analysis**")
    
    # Show example of what the app does
    st.markdown("""
    ### Features:
    - 📁 **Upload CSV files** for instant analysis
    - 📊 **View dataset metadata** including dimensions, types, and missing values
    - 📈 **Interactive visualizations** for both numerical and categorical data
    - 🔍 **Automated column type detection** and appropriate chart generation
    
    ### How to use:
    1. Upload a CSV file or load the demo dataset
    2. Select a column to analyze from the sidebar
    3. View the automatic visualization and statistics
    """)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | EDA Dashboard v1.0")