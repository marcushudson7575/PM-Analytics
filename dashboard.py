"""
PM Analytics Dashboard - Streamlit
Displays private markets fund data from the FastAPI backend.
"""
import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List

# API Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

# Page configuration
st.set_page_config(
    page_title="PM Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .banner-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 2.5rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 10px 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .banner-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .banner-subtitle {
        font-size: 1.5rem;
        color: #94a3b8;
        margin: 0.5rem 0 0 0;
        font-weight: 300;
    }
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f9fafb;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=60)
def fetch_dashboard_data() -> Dict:
    """Fetch dashboard KPIs from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/dashboard")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching dashboard data: {e}")
        return {}


@st.cache_data(ttl=60)
def fetch_aum_by_strategy() -> Dict:
    """Fetch AUM distribution by strategy"""
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/aum-by-strategy")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching AUM data: {e}")
        return {}


@st.cache_data(ttl=60)
def fetch_funds(page: int = 1, page_size: int = 50, strategy: str = None) -> Dict:
    """Fetch funds list"""
    try:
        params = {"page": page, "page_size": page_size}
        if strategy:
            params["strategy"] = strategy

        response = requests.get(f"{API_BASE_URL}/funds", params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching funds: {e}")
        return {}


@st.cache_data(ttl=60)
def fetch_vintage_year_data() -> Dict:
    """Fetch vintage year distribution"""
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/vintage-year-distribution")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching vintage year data: {e}")
        return {}


def format_currency(value: float) -> str:
    """Format value as currency in billions"""
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.1f}B"
    elif value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    else:
        return f"${value:,.0f}"


def main():
    # Professional Banner Header
    st.markdown("""
        <div class="banner-header">
            <h1 class="banner-title">📊 Private Markets</h1>
            <p class="banner-subtitle">Analytics Software</p>
        </div>
    """, unsafe_allow_html=True)

    # Fetch data
    dashboard_data = fetch_dashboard_data()
    aum_data = fetch_aum_by_strategy()

    if not dashboard_data:
        st.error("Unable to load dashboard data. Make sure the FastAPI server is running at http://localhost:8000")
        return

    # KPI Cards
    st.markdown("### 📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Funds",
            value=dashboard_data.get('total_funds', 0),
            help="Number of funds in database with ≥95% confidence"
        )

    with col2:
        total_aum = dashboard_data.get('total_aum_usd', 0)
        st.metric(
            label="Total AUM",
            value=format_currency(total_aum),
            help="Total Assets Under Management across all funds"
        )

    with col3:
        avg_size = dashboard_data.get('avg_fund_size_usd', 0)
        st.metric(
            label="Avg Fund Size",
            value=format_currency(avg_size),
            help="Average fund size across all strategies"
        )

    with col4:
        data_quality = dashboard_data.get('data_quality_pct', 0)
        st.metric(
            label="Data Quality",
            value=f"{data_quality}%",
            help="Percentage of funds with high confidence scores"
        )

    st.divider()

    # Charts Row 1
    st.markdown("### 📊 Asset Allocation")
    col1, col2 = st.columns(2)

    with col1:
        # AUM by Strategy Pie Chart
        if aum_data and 'chart_data' in aum_data:
            df_aum = pd.DataFrame(aum_data['chart_data'])

            fig_pie = px.pie(
                df_aum,
                values='aum_usd',
                names='strategy',
                title='AUM Distribution by Strategy',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>AUM: $%{value:,.0f}<br>%{percent}<extra></extra>'
            )
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Fund Count by Strategy Bar Chart
        if aum_data and 'chart_data' in aum_data:
            df_aum = pd.DataFrame(aum_data['chart_data'])

            fig_bar = px.bar(
                df_aum,
                x='strategy',
                y='fund_count',
                title='Number of Funds by Strategy',
                color='strategy',
                color_discrete_sequence=px.colors.qualitative.Set3,
                text='fund_count'
            )
            fig_bar.update_traces(textposition='outside')
            fig_bar.update_layout(
                height=400,
                showlegend=False,
                xaxis_title="Strategy",
                yaxis_title="Number of Funds"
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    # Vintage Year Chart
    st.markdown("### 📅 Vintage Year Analysis")
    vintage_data = fetch_vintage_year_data()

    if vintage_data and 'chart_data' in vintage_data:
        df_vintage = pd.DataFrame(vintage_data['chart_data'])

        fig_vintage = go.Figure()

        # Bar chart for fund count
        fig_vintage.add_trace(go.Bar(
            x=df_vintage['year'],
            y=df_vintage['fund_count'],
            name='Fund Count',
            marker_color='lightblue',
            yaxis='y',
            text=df_vintage['fund_count'],
            textposition='outside'
        ))

        # Line chart for AUM
        fig_vintage.add_trace(go.Scatter(
            x=df_vintage['year'],
            y=df_vintage['total_aum_usd'] / 1_000_000_000,  # Convert to billions
            name='Total AUM ($B)',
            marker_color='darkblue',
            yaxis='y2',
            mode='lines+markers'
        ))

        fig_vintage.update_layout(
            title='Funds by Vintage Year',
            xaxis=dict(title='Vintage Year'),
            yaxis=dict(title='Number of Funds', side='left'),
            yaxis2=dict(title='Total AUM ($B)', overlaying='y', side='right'),
            height=400,
            hovermode='x unified'
        )

        st.plotly_chart(fig_vintage, use_container_width=True)

    st.divider()

    # Funds Table
    st.markdown("### 📋 Fund Database")

    # Filter options
    col1, col2 = st.columns([1, 3])

    with col1:
        # Strategy filter
        strategies = ["All"] + sorted(list(set([item['strategy'] for item in aum_data.get('chart_data', [])])))
        selected_strategy = st.selectbox("Filter by Strategy", strategies)

    # Fetch funds
    strategy_filter = None if selected_strategy == "All" else selected_strategy
    funds_data = fetch_funds(strategy=strategy_filter)

    if funds_data and 'funds' in funds_data:
        funds = funds_data['funds']

        # Convert to DataFrame
        df_funds = pd.DataFrame([
            {
                'Name': f['name'],
                'Strategy': f['strategy'],
                'Vintage Year': f['vintage_year'],
                'Geography': f['geography'],
                'Fund Size': format_currency(float(f['fund_size_usd'])) if f.get('fund_size_usd') else 'N/A',
                'Confidence': f"{float(f['data_confidence_score']) * 100:.0f}%",
                'Source': f['data_source']
            }
            for f in funds
        ])

        st.dataframe(
            df_funds,
            use_container_width=True,
            hide_index=True,
            height=400
        )

        st.caption(f"Showing {len(funds)} of {funds_data.get('total', 0)} total funds")
    else:
        st.info("No funds data available")

    # Footer
    st.divider()
    st.markdown("""
        <div style='text-align: center; color: #6b7280; padding: 2rem 0;'>
            <p><strong>PM Analytics</strong> - Private Markets Data Platform</p>
            <p style='font-size: 0.9rem;'>Data sourced from authoritative regulatory filings and public disclosures</p>
            <p style='font-size: 0.85rem;'>Only displaying funds with ≥95% confidence scores</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
