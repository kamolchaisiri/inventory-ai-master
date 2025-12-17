import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import plotly.express as px

# 1. Page Configuration (Wide layout, custom icon)
st.set_page_config(
    page_title="Inventory AI Master", 
    layout="wide", 
    page_icon="💎",
    initial_sidebar_state="expanded"
)

# --- CSS Styling for a Premium Look ---
st.markdown("""
<style>
    /* Customize Metrics Cards */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* Header Styling */
    h1, h2, h3 {
        color: #2c3e50;
    }
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# 2. Load Data Function
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('inventory_data.csv')
        return df
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()

# Data Validation
if df.empty:
    st.error("❌ Data not found! Please run 'generate_csv.py' first.")
    st.stop()

# --- SIDEBAR (Control Panel) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2649/2649258.png", width=80)
    st.title("Inventory AI")
    st.caption("Intelligent Stock Management System")
    
    st.divider()
    
    # Filter
    st.subheader("🔍 Filters")
    selected_category = st.selectbox("Category:", ['All'] + list(df['Category'].unique()))
    
    # About
    st.info("💡 **Pro Tip:** Switch tabs to view between 'Clearance Mode' and 'Restock Mode'.")

# Apply Filter
if selected_category != 'All':
    df = df[df['Category'] == selected_category].copy()

# --- AI LOGIC ENGINE ---

# Logic 1: Segmentation (K-Means)
X = df[['Stock_Qty', 'Days_Since_Last_Sale']]
if len(df) > 3:
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['Cluster'] = kmeans.fit_predict(X)
    
    # Identify Dead Stock Cluster (High Days Unsold)
    dead_cluster = df.groupby('Cluster')['Days_Since_Last_Sale'].mean().idxmax()
    df['Status'] = np.where(df['Cluster'] == dead_cluster, "🔴 Dead Stock", 
                   np.where(df['Days_Since_Last_Sale'] < 30, "🟢 Hot Item", "🟡 Slow Moving"))
else:
    df['Status'] = "⚪ Normal"

# Logic 2: Forecasting (Stock Runway)
# Avoid division by zero
df['Days_Until_Stockout'] = (df['Stock_Qty'] / df['Avg_Daily_Sales']).replace([np.inf, -np.inf], 999).fillna(999)

# Logic 3: Restock Alerts
df['Restock_Status'] = np.where(
    df['Days_Until_Stockout'] < df['Lead_Time_Days'], "🚨 Critical Low", 
    np.where(df['Days_Until_Stockout'] < (df['Lead_Time_Days'] * 1.5), "⚠️ Warning", "✅ Healthy")
)

# --- MAIN DASHBOARD UI ---

st.title("💎 Enterprise Inventory Dashboard")
st.markdown("Real-time AI analysis for stock optimization.")

# Top Level KPI
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric("📦 Total SKUs", f"{len(df):,}")
with kpi2:
    dead_count = len(df[df['Status'] == "🔴 Dead Stock"])
    st.metric("🛑 Dead Stock Items", dead_count, delta_color="inverse")
with kpi3:
    critical_count = len(df[df['Restock_Status'] == "🚨 Critical Low"])
    st.metric("⚡ Critical Restock", critical_count, delta="Urgent", delta_color="inverse")
with kpi4:
    total_val = (df['Stock_Qty'] * df['Cost_Price']).sum()
    st.metric("💰 Total Inventory Value", f"${total_val:,.0f}")

st.markdown("---")

# TABS for specific views
tab1, tab2 = st.tabs(["💀 Dead Stock & Clearance", "📉 Forecasting & Restock"])

# ================= TAB 1: DEAD STOCK (With Scatter Plot) =================
with tab1:
    st.subheader("📍 Inventory Health Map")
    
    col_chart, col_list = st.columns([2, 1])
    
    # 1. Scatter Plot (Bubble Chart) - The Highlight
    with col_chart:
        # Color Map
        color_map = {"🔴 Dead Stock": "#FF4B4B", "🟢 Hot Item": "#00CC96", "🟡 Slow Moving": "#FFA15A"}
        
        fig = px.scatter(
            df, 
            x="Days_Since_Last_Sale", 
            y="Stock_Qty", 
            size="Current_Price", # Bubble size = Price impact
            color="Status",
            color_discrete_map=color_map,
            hover_data=['SKU', 'Category', 'Current_Price'],
            title=f"Stock Aging Analysis ({selected_category})",
            labels={"Days_Since_Last_Sale": "Days Unsold", "Stock_Qty": "Stock Level"},
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)

    # 2. Top Dead Stock List
    with col_list:
        st.markdown("#### 🚨 Top Risk Items")
        dead_stock_df = df[df['Status'] == "🔴 Dead Stock"].sort_values('Stock_Qty', ascending=False).head(8)
        
        st.dataframe(
            dead_stock_df[['SKU', 'Stock_Qty', 'Days_Since_Last_Sale']],
            use_container_width=True,
            hide_index=True
        )
    
    # 3. Full Action Table
    st.subheader("📋 Clearance Campaign Candidates")
    display_df = df[df['Status'] == "🔴 Dead Stock"][['SKU', 'Category', 'Stock_Qty', 'Days_Since_Last_Sale', 'Current_Price', 'Status']]
    
    st.dataframe(
        display_df.style.background_gradient(cmap='Reds', subset=['Days_Since_Last_Sale'])
        .format({"Current_Price": "${:.2f}"}),
        use_container_width=True
    )

# ================= TAB 2: FORECASTING =================
with tab2:
    st.subheader("🔮 Demand Forecasting & Replenishment")
    
    critical_stock = df[df['Restock_Status'] != "✅ Healthy"].sort_values('Days_Until_Stockout')
    
    if critical_stock.empty:
        st.success("All stock levels are healthy! No restock needed.")
    else:
        # Forecast Chart
        fig_forecast = px.bar(
            critical_stock.head(10),
            x='Days_Until_Stockout',
            y='SKU',
            orientation='h',
            color='Restock_Status',
            color_discrete_map={"🚨 Critical Low": "#FF4B4B", "⚠️ Warning": "#FFA15A"},
            title="⏳ Stock Runway: Days Left Before Stockout",
            text_auto=True
        )
        fig_forecast.add_vline(x=7, line_dash="dash", line_color="black", annotation_text="Lead Time (7 Days)")
        st.plotly_chart(fig_forecast, use_container_width=True)

        # Restock Table
        st.subheader("🚚 Recommended Order List")
        st.dataframe(
            critical_stock[['SKU', 'Stock_Qty', 'Avg_Daily_Sales', 'Days_Until_Stockout', 'Restock_Status']]
            .style.format({'Avg_Daily_Sales': '{:.1f}', 'Days_Until_Stockout': '{:.1f}'})
            .background_gradient(cmap='OrRd_r', subset=['Days_Until_Stockout']),
            use_container_width=True
        )