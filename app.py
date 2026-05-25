import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ==========================================
# 1. PAGE CONFIG & STYLING
# ==========================================
st.set_page_config(
    page_title="Supply Chain Waste Intelligence",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to mimic the exact layout, deep red headers, and card stylings
st.markdown("""
<style>
    /* Top Bar Styling */
    .header-container {
        text-align: center;
        border-bottom: 2px solid #A8201A;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    .header-title {
        color: #1E293B;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 2px;
    }
    .header-subtitle {
        color: #64748B;
        font-size: 13px;
    }
    
    /* Live Alerts ticker bar */
    .alert-banner {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #EF4444;
        padding: 8px 12px;
        border-radius: 4px;
        margin-bottom: 20px;
        font-size: 13px;
        display: flex;
        align-items: center;
    }
    .alert-tag {
        background-color: #EF4444;
        color: white;
        font-weight: bold;
        padding: 2px 6px;
        border-radius: 3px;
        margin-right: 10px;
        font-size: 11px;
    }

    /* KPI Summary Cards */
    .kpi-card {
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 12px 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .kpi-title {
        color: #64748B;
        font-size: 12px;
        font-weight: 500;
    }
    .kpi-value {
        color: #0F172A;
        font-size: 22px;
        font-weight: 700;
        margin: 4px 0;
    }
    .kpi-delta-pos { color: #10B981; font-size: 12px; font-weight: 600; }
    .kpi-delta-neg { color: #EF4444; font-size: 12px; font-weight: 600; }
    
    /* Insight Cards */
    .insight-card {
        border-radius: 6px;
        padding: 15px;
        height: 100%;
        border: 1px solid #E2E8F0;
    }
    .insight-saving {
        text-align: right;
        font-weight: bold;
        font-size: 18px;
    }
    .insight-label {
        font-size: 11px;
        text-transform: uppercase;
        color: #64748B;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_html=True)

# ==========================================
# 2. HEADER & NAVIGATION TABS
# ==========================================
st.markdown("""
<div class="header-container">
    <div class="header-title">Supply Chain Waste Intelligence</div>
    <div class="header-subtitle">AI-powered waste reduction, inventory optimization & reverse logistics intelligence.</div>
</div>
""", unsafe_html=True)

tabs = st.tabs([
    "📈 Executive Overview", "💧 Waste Leakage", "📦 Inventory Intelligence", 
    "🔄 Returns Intelligence", "🌐 Network Optimization", "🗼 Control Tower", "🔮 What-if Simulation"
])

# All code renders inside the first tab to mimic the dashboard view
with tabs[0]:
    
    # ==========================================
    # 3. INTERACTIVE FILTERS
    # ==========================================
    # Creating layout rows for the dashboard filters
    f1, f2, f3, f4, f5, f6, f7, f8 = st.columns([1.2, 1, 1, 1, 1, 1, 1.5, 0.8])
    
    with f1: time_period = st.selectbox("Time Period", ["May 2024", "Apr 2024", "Mar 2024"])
    with f2: region = st.selectbox("Region", ["All", "North", "South", "East", "West"])
    with f3: country = st.selectbox("Country", ["All", "UK", "US", "Germany"])
    with f4: node_type = st.selectbox("Node Type", ["All", "Depot", "Supplier", "Store"])
    with f5: category = st.selectbox("Category", ["All", "Food (Fresh)", "Electronics", "Home & Living", "Fashion"])
    with f6: store = st.selectbox("Store", ["All Stores", "Manchester Depot", "London Hub"])
    with f7: sku = st.selectbox("SKU / Product", ["All Products", "High-Volume Items", "Perishables"])
    with f8: 
        st.write("") # Spacer
        st.write("")
        clear_filters = st.button("Clear Filters", use_container_width=True)

    # Dynamic Data Adjustments based on filter selections
    multiplier = 1.0
    if category != "All": multiplier *= 0.4
    if region != "All": multiplier *= 0.7

    # ==========================================
    # 4. LIVE ALERTS BANNER
    # ==========================================
    st.markdown(f"""
    <div class="alert-banner">
        <span class="alert-tag">⚡ LIVE ALERTS</span>
        <span style="color:#B45309; font-weight:600; margin-right:5px;">⚠️ MEDIUM</span> Return spike in Electronics category <span style="color:#64748B;">32% increase vs last month</span>
        <span style="color:#CBD5E1; margin: 0 15px;">|</span>
        <span style="color:#B45309; font-weight:600; margin-right:5px;">⚠️ MEDIUM</span> Overstock in Home & Living <span style="color:#64748B;">£5.3M slow moving inventory</span>
        <span style="color:#CBD5E1; margin: 0 15px;">|</span>
        <span style="color:#1D4ED8; font-weight:600; margin-right:5px;">ℹ️ LOW</span> Depot utilization below target <span style="color:#64748B;">Leeds Depot at 62% capacity</span>
    </div>
    """, unsafe_html=True)

    # ==========================================
    # 5. KPI SUMMARY CARDS
    # ==========================================
    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    
    with kpi1:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-title">Total Waste Leakage 🛈</div>
            <div class="kpi-value">£{28.4 * multiplier:.1f}M</div>
            <div class="kpi-delta-neg">▲ +6.7M <span style="color:#64748B; font-weight:normal;">vs Apr</span></div>
        </div>""", unsafe_html=True)
        
    with kpi2:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-title">Waste as % of Revenue 🛈</div>
            <div class="kpi-value">{(2.45 * multiplier if category=="All" else 1.8):.2f}%</div>
            <div class="kpi-delta-neg">▲ +0.16pp <span style="color:#64748B; font-weight:normal;">vs Apr</span></div>
        </div>""", unsafe_html=True)
        
    with kpi3:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-title">Recovery Value 🛈</div>
            <div class="kpi-value">£{12.7 * multiplier:.1f}M</div>
            <div class="kpi-delta-pos">▼ -0.6M <span style="color:#64748B; font-weight:normal;">vs Apr</span></div>
        </div>""", unsafe_html=True)
        
    with kpi4:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-title">Inventory at Risk 🛈</div>
            <div class="kpi-value">£{41.3 * multiplier:.1f}M</div>
            <div class="kpi-delta-neg">▲ +4.1M <span style="color:#64748B; font-weight:normal;">vs Apr</span></div>
        </div>""", unsafe_html=True)
        
    with kpi5:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-title">Return Cycle Time 🛈</div>
            <div class="kpi-value">18.6 Days</div>
            <div class="kpi-delta-pos">▼ -1.9Days <span style="color:#64748B; font-weight:normal;">vs Apr</span></div>
        </div>""", unsafe_html=True)
        
    with kpi6:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-title">Carbon Impact 🛈</div>
            <div class="kpi-value">{8.7 * multiplier:.1f}K tCO₂e</div>
            <div class="kpi-delta-neg">▲ +4.4K <span style="color:#64748B; font-weight:normal;">vs Apr</span></div>
        </div>""", unsafe_html=True)

    st.write("") # Padding

    # ==========================================
    # 6. CHARTS & ANALYTICS WORKSPACE
    # ==========================================
    col_left, col_right = st.columns([4, 6])

    # --- LEFT COLUMN: TREND & TOP CATEGORIES ---
    with col_left:
        # Waste Leakage Trend Line/Area Chart
        st.markdown("### Waste Leakage Trend 🛈")
        months = ['Dec 2023', 'Jan 2024', 'Feb 2024', 'Mar 2024', 'Apr 2024', 'May 2024']
        leakage_vals = [22, 24, 23, 26, 25, 28.4 * multiplier]
        pct_vals = [2.1, 2.3, 2.2, 2.5, 2.4, 2.45]

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=months, y=leakage_vals, name='Waste Leakage (£M)', mode='lines+markers', line=dict(color='#2563EB', width=3)))
        fig_trend.add_trace(go.Scatter(x=months, y=pct_vals, name='Waste as % of Revenue', yaxis='y2', mode='lines', line=dict(color='#64748B', dash='dash')))
        
        fig_trend.update_layout(
            yaxis=dict(title='Waste Leakage (£M)', gridcolor='#F1F5F9'),
            yaxis2=dict(title='As % of Revenue', overlaying='y', side='right'),
            margin=dict(l=40, r=40, t=10, b=10),
            height=240,
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=-0.4, xanchor="center", x=0.5),
            plot_bgcolor='white', paper_bgcolor='white'
        )
        st.plotly_chart(fig_trend, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("<p style='color:#2563EB; font-size:13px; font-weight:600; cursor:pointer;'>View detailed trend →</p>", unsafe_html=True)
        st.write("")

        # Top Waste Categories Horizontal Bar Chart
        st.markdown(f"### Top Waste Categories <span style='font-size:12px; color:#64748B;'>{time_period} | £M</span>", unsafe_html=True)
        cats = ['Fashion', 'Others', 'Home & Li...', 'Electronics', 'Food (Am...)', 'Food (Fresh)'][::-1]
        vals = [2.1, 2.5, 3.2, 4.3, 6.1, 10.2]
        
        # Filter chart data dynamically if a specific category option is picked
        if category != "All":
            cats = [category]
            vals = [10.2 * multiplier]

        fig_cats = go.Figure(go.Bar(x=vals, y=cats, orientation='h', marker_color='#2563EB', text=[f"£{v}M" for v in vals], textposition='outside'))
        fig_cats.update_layout(
            margin=dict(l=10, r=40, t=10, b=10), height=230,
            plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='#F1F5F9')
        )
        st.plotly_chart(fig_cats, use_container_width=True, config={'displayModeBar': False})
        st.markdown("<p style='color:#2563EB; font-size:13px; font-weight:600; cursor:pointer;'>View all categories →</p>", unsafe_html=True)


    # --- RIGHT COLUMN: STAGE BREAKDOWN & AI INSIGHTS ---
    with col_right:
        st.markdown(f"### Supply Chain Waste Breakdown by Stage <span style='font-size:12px; color:#64748B;'>{time_period} | Net Waste vs Recovered (£M)</span>", unsafe_html=True)
        
        stages = ['Suppliers', 'Manufacturing', 'Depots', 'Fulfilment Centres', 'Stores / Dark Stores', 'Returns & Reverse Flow'][::-1]
        net_waste = [20.3, 14.8, 16.5, 5.0, 4.2, 1.2][::-1]
        recovered = [4.1, 3.2, 5.1, 1.2, 2.5, 18.3][::-1]

        fig_stages = go.Figure()
        fig_stages.add_trace(go.Bar(y=stages, x=net_waste, name='Net Waste', orientation='h', marker_color='#1D4ED8'))
        fig_stages.add_trace(go.Bar(y=stages, x=recovered, name='Recovered', orientation='h', marker_color='#10B981'))
        
        fig_stages.update_layout(
            barmode='stack',
            margin=dict(l=10, r=20, t=10, b=10), height=270,
            legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1),
            plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(gridcolor='#F1F5F9')
        )
        st.plotly_chart(fig_stages, use_container_width=True, config={'displayModeBar': False})
        
        # AI Optimization Insights Grid
        st.markdown("### AI Optimization Insights")
        
        r1_c1, r1_c2, r1_c3 = st.columns(3)
        with r1_c1:
            st.markdown("""
            <div class="insight-card" style="background-color: #F0FDF4;">
                <div style="font-weight: 600; color: #166534; font-size:13px;">🟢 Reallocate slow moving stock from Manchester Depot</div>
                <div style="margin-top:20px;">
                    <div class="insight-saving" style="color: #166534;">£1.8M</div>
                    <div class="insight-label">Potential Waste Reduction</div>
                </div>
            </div>
            """, unsafe_html=True)
        with r1_c2:
            st.markdown("""
            <div class="insight-card" style="background-color: #EFF6FF;">
                <div style="font-weight: 600; color: #1E40AF; font-size:13px;">🔵 Reduce return cycle time for Electronics</div>
                <div style="margin-top:20px;">
                    <div class="insight-saving" style="color: #1E40AF;">£2.3M</div>
                    <div class="insight-label">Potential Recovery Improvement</div>
                </div>
            </div>
            """, unsafe_html=True)
        with r1_c3:
            st.markdown("""
            <div class="insight-card" style="background-color: #F0FDF4;">
                <div style="font-weight: 600; color: #166534; font-size:13px;">🟢 Optimize ordering frequency for Fresh category</div>
                <div style="margin-top:20px;">
                    <div class="insight-saving" style="color: #166534;">£1.2M</div>
                    <div class="insight-label">Potential Waste Reduction</div>
                </div>
            </div>
            """, unsafe_html=True)

        st.write("") # Grid row spacer
        
        r2_c1, r2_c2, r2_c3 = st.columns(3)
        with r2_c1:
            st.markdown("""
            <div class="insight-card" style="background-color: #FFFBEB;">
                <div style="font-weight: 600; color: #92400E; font-size:13px;">🟡 Consolidate distribution runs in London</div>
                <div style="margin-top:20px;">
                    <div class="insight-saving" style="color: #92400E;">£0.9M</div>
                    <div class="insight-label">Potential Efficiency Gain</div>
                </div>
            </div>
            """, unsafe_html=True)
        with r2_c2:
            st.markdown("""
            <div class="insight-card" style="background-color: #EFF6FF;">
                <div style="font-weight: 600; color: #1E40AF; font-size:13px;">🔵 Implement dynamic pricing for near-expiry stock</div>
                <div style="margin-top:20px;">
                    <div class="insight-saving" style="color: #1E40AF;">£3.1M</div>
                    <div class="insight-label">Potential Recovery Improvement</div>
                </div>
            </div>
            """, unsafe_html=True)
        with r2_c3:
            st.markdown("""
            <div class="insight-card" style="background-color: #FFFBEB;">
                <div style="font-weight: 600; color: #92400E; font-size:13px;">🟡 Reroute Fashion returns to secondary marketplace</div>
                <div style="margin-top:20px;">
                    <div class="insight-saving" style="color: #92400E;">£0.7M</div>
                    <div class="insight-label">Potential Efficiency Gain</div>
                </div>
            </div>
            """, unsafe_html=True)
            
        st.write("")
        st.markdown("<p style='color:#2563EB; font-size:13px; font-weight:600; cursor:pointer;'>View all recommendations →</p>", unsafe_html=True)