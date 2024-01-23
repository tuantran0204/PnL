import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Function to calculate additional metrics
def calculate_metrics(data, funded_cac_increase, new_customer_increases2024, new_customer_increases2025, new_customer_increases2026, new_customer_increases2027, new_customer_increases2028, active_rate, funding_rate):
    # Assuming 'Year', 'Total Customer', 'Active Rate', 'New Customer', 'Funding Rate',
    # 'ARPU', 'Direct Cost', 'Churn Rate', 'Funded CAC' are columns in your data

    # Convert 'Direct Cost' to numeric
    data['Direct Cost'] = pd.to_numeric(data['Direct Cost'], errors='coerce')

    # Convert 'Total Customer' and 'Active Rate' to numeric if needed
    data['Total Customer'] = pd.to_numeric(data['Total Customer'], errors='coerce')
    data['Active Rate'] = pd.to_numeric(data['Active Rate'], errors='coerce')
    # Convert Active Rate and Funding Rate to percentages
    data['Active Rate'] = data['Active Rate'] * 100
    data['Funding Rate'] = data['Funding Rate'] * 100

    # Apply 
    mask_cac = (data['Year'] >= 2024) & (data['Year'] <= 2028)
    data.loc[mask_cac, 'Funded CAC'] = (data.loc[mask_cac, 'Funded CAC'] * 0) + funded_cac_increase

    mask_cac = (data['Year'] >= 2024) & (data['Year'] <= 2028)
    data.loc[mask_cac, 'Active Rate'] = (data.loc[mask_cac, 'Active Rate'] * 0) + active_rate

    mask_cac = (data['Year'] >= 2024) & (data['Year'] <= 2028)
    data.loc[mask_cac, 'Funding Rate'] = (data.loc[mask_cac, 'Funding Rate'] * 0) + funding_rate

    # Calculate New customer 2024-2028
    mask_cac = (data['Year'] == 2024)
    data.loc[mask_cac, 'New Customer'] = new_customer_increases2024
    mask_cac = (data['Year'] == 2025)
    data.loc[mask_cac, 'New Customer'] = new_customer_increases2025
    mask_cac = (data['Year'] == 2026)
    data.loc[mask_cac, 'New Customer'] = new_customer_increases2026
    mask_cac = (data['Year'] == 2027)
    data.loc[mask_cac, 'New Customer'] = new_customer_increases2027
    mask_cac = (data['Year'] == 2028)
    data.loc[mask_cac, 'New Customer'] = new_customer_increases2028
        
    # Calculate Total customer 2024-2028
    mask_cac = (data['Year'] == 2024)
    data.loc[mask_cac, 'Total Customer'] = (data.loc[mask_cac, 'Total Customer']) + new_customer_increases2024
    mask_cac = (data['Year'] == 2025)
    data.loc[mask_cac, 'Total Customer'] = (data.loc[mask_cac, 'Total Customer']) + new_customer_increases2024+ new_customer_increases2025
    mask_cac = (data['Year'] == 2026)
    data.loc[mask_cac, 'Total Customer'] = (data.loc[mask_cac, 'Total Customer']) + new_customer_increases2024 + new_customer_increases2025 + new_customer_increases2026
    mask_cac = (data['Year'] == 2027)
    data.loc[mask_cac, 'Total Customer'] = (data.loc[mask_cac, 'Total Customer']) + new_customer_increases2024 + new_customer_increases2025 + new_customer_increases2026 + new_customer_increases2027
    mask_cac = (data['Year'] == 2028)
    data.loc[mask_cac, 'Total Customer'] = (data.loc[mask_cac, 'Total Customer']) + new_customer_increases2024 + new_customer_increases2025 + new_customer_increases2026 + new_customer_increases2027 + new_customer_increases2028

    # Calculate active customer and inactive customer for all years
    data['active_customer'] = data['Total Customer'] * (data['Active Rate']/100)

    # Calculate Revenue, GP/Active, total gross profit, LTV, LTV/CAC, Payback
    
    data['Funded Customer'] = (data['active_customer'] * (data['Funding Rate']/100)).round(2)
    
    data['revenue'] = data['ARPU'] * data['active_customer'] / 1000
    data['gp_per_active'] = (data['ARPU'] - data['Direct Cost'])
    data['Gross Profit'] = data['gp_per_active'] * data['active_customer'] / 1000
    data['EBIT'] =  data['Gross Profit'] - ((data['Staff Cost'] +  data['Opex'] + data['Retaining'] + data['Selling Cost']) / 1000000) - (data['Funded CAC'] * data['Funded Customer'] / 1000)
    data['Gross Margin'] = data['Gross Profit'] / data['revenue']  * 100
    data['EBIT Margin'] = data['EBIT'] / data['revenue']  * 100

    data['ltv'] = (data['ARPU'] - data['Direct Cost']) / data['Churn Rate']
    data['ltv_cac_ratio'] = data['ltv'] / data['Funded CAC']
    data['payback'] = data['Funded CAC'] / (data['ARPU'] - data['Direct Cost'])
    data['payback'] = data['payback'].clip(lower=0)

    return data

def create_column_chart(fig, x, y, title):
    # Add trace to the column chart with a different color
    fig.add_trace(go.Bar(x=x, y=y,
                         name=title,
                         marker_color='#563D82',
                         text=y.round(2),
                         textposition='outside'))

    fig.update_layout(title=title)
    fig.update_xaxes(showgrid=False)  # Remove x-axis gridlines
    fig.update_yaxes(showgrid=False)  # Remove y-axis gridlines

# Title of the app
st.title('PnL Simulator')

# Create a sidebar for input
st.sidebar.title("Input Settings")

# Raw Data
# st.sidebar.subheader('Raw Data')
data = pd.read_csv("./data.csv")
# st.sidebar.write(data)

# Check if data is available and then process it
if 'data' in locals() and not data.empty:
    # Input for Funded CAC increase from 5 to 30
    active_rate = st.sidebar.number_input('Active Rate 2024-2028 (Unit: %)', min_value=10, max_value=100, step=1, value=33)
    funding_rate = st.sidebar.number_input('Funded Rate 2024-2028 (Unit: %)', min_value=10, max_value=100, step=1, value=53)
    new_customer_increases2024 = st.sidebar.number_input('New Customer 2024 (Unit: Thousand)', min_value=100, max_value=3000, step=50, value=400)
    new_customer_increases2025 = st.sidebar.number_input('New Customer 2025 (Unit: Thousand)', min_value=100, max_value=3000, step=50, value=400)
    new_customer_increases2026 = st.sidebar.number_input('New Customer 2026 (Unit: Thousand)', min_value=100, max_value=3000, step=50, value=500)
    new_customer_increases2027 = st.sidebar.number_input('New Customer 2027 (Unit: Thousand)', min_value=100, max_value=3000, step=50, value=600)
    new_customer_increases2028 = st.sidebar.number_input('New Customer 2028 (Unit: Thousand)', min_value=100, max_value=3000, step=50, value=700)
    funded_cac_increase = st.sidebar.number_input('Funded CAC 2024-2028 (Unit: $)', min_value=3, max_value=50, step=1, value=10)

    new_customer_increases = [new_customer_increases2024, new_customer_increases2025, new_customer_increases2026, new_customer_increases2027, new_customer_increases2028]

    # Process and calculate additional metrics with user input values
    processed_data = calculate_metrics(data, funded_cac_increase, new_customer_increases2024, new_customer_increases2025, new_customer_increases2026, new_customer_increases2027, new_customer_increases2028, active_rate, funding_rate)

    st.subheader(' Definition:')
    # Additional insights
    st.write("Payback is calculated using the formula of dividing Funded CAC by GP per Active.")

# Visualization
st.subheader(' Metrics Visualization:')

# Checkbox to toggle Customer Base Metrics
show_customer_base_metrics = st.checkbox("Customer Base Metrics")
if show_customer_base_metrics:

    # Column chart for Active Customer by year
    fig_active_customer_chart = go.Figure()
    create_column_chart(fig_active_customer_chart, processed_data['Year'], processed_data['active_customer'], 'Active Customers (Unit: Thousand)')
    st.plotly_chart(fig_active_customer_chart)
    # Column chart for Funded Customer by year
    fig_funded_customer_chart = go.Figure()
    create_column_chart(fig_funded_customer_chart, processed_data['Year'], processed_data['Funded Customer'], 'Funded Customers (Unit: Thousand)')
    st.plotly_chart(fig_funded_customer_chart)

# Checkbox to toggle Financial Metrics
show_financial_metrics = st.checkbox("Financial Metrics")
if show_financial_metrics:
    # Column chart for Revenue vs GP by year
    fig_profitability_column = go.Figure()
    # Add GP
    fig_profitability_column.add_trace(go.Bar(x=processed_data['Year'], y=processed_data['revenue'],
                                               name='Revenue',
                                               marker_color='#2774AE',  
                                               text=processed_data['revenue'].round(2),
                                               textposition='outside'))
    # Add revenue 
    fig_profitability_column.add_trace(go.Bar(x=processed_data['Year'], y=processed_data['Gross Profit'],
                                               name='Gross Profit',
                                               marker_color='#A9A9A9',  # Set color to grey
                                               text=processed_data['Gross Profit'].round(2),
                                               textposition='outside'))
    fig_profitability_column.update_layout(barmode='group', title='Profitability (Unit: Mil $)')
    fig_profitability_column.update_xaxes(showgrid=False)  # Remove x-axis gridlines
    fig_profitability_column.update_yaxes(showgrid=False)  # Remove y-axis gridlines

    st.plotly_chart(fig_profitability_column)

    # Column GM, EBIT margin  by year
    fig_margin_chart = go.Figure()

    # Add GM, EBIT margin 
    fig_margin_chart.add_trace(go.Scatter(x=processed_data['Year'], y=processed_data['Gross Margin'],
                                        mode='lines+text', name='Gross Margin', line=dict(color='#2774AE'),
                                        text=processed_data['Gross Margin'].round(2),
                                        textposition='top left', textfont=dict(color='#2774AE')))
    fig_margin_chart.add_trace(go.Scatter(x=processed_data['Year'], y=processed_data['EBIT Margin'],
                                        mode='lines+text', name='EBIT Margin', line=dict(color='#EB3300'),
                                        text=processed_data['EBIT Margin'].round(2),
                                        textposition='bottom left', textfont=dict(color='#EB3300')))

    fig_margin_chart.update_layout(barmode='group', title='Gross Margin vs EBIT Margin (%)')
    fig_margin_chart.update_xaxes(showgrid=False)  # Remove x-axis gridlines
    fig_margin_chart.update_yaxes(showgrid=False)  # Remove y-axis gridlines

    st.plotly_chart(fig_margin_chart)

    fig_test_chart = go.Figure()
    create_column_chart(fig_test_chart, processed_data['Year'], processed_data['EBIT'], 'EBIT (Unit: Thousand)')
    st.plotly_chart(fig_test_chart)

st.subheader('Thank You')
