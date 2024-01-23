import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Function to calculate additional metrics
def calculate_metrics(data, funded_cac_increase, new_customer_increase_2024, new_customer_increase_2025, new_customer_increase_2026, new_customer_increase_2027, new_customer_increase_2028):
    # Assuming 'Year', 'Total Customer', 'Active Rate', 'New Customer', 'Funding Rate',
    # 'ARPU', 'Direct Cost', 'Churn Rate', 'Funded CAC' are columns in your data

    # Convert 'Direct Cost' to numeric
    data['Direct Cost'] = pd.to_numeric(data['Direct Cost'], errors='coerce')

    # Convert 'Total Customer' and 'Active Rate' to numeric if needed
    data['Total Customer'] = pd.to_numeric(data['Total Customer'], errors='coerce')
    data['Active Rate'] = pd.to_numeric(data['Active Rate'], errors='coerce')

    # Calculate active customer and inactive customer for all years
    data['active_customer'] = data['Total Customer'] * data['Active Rate']
    data['inactive_customer'] = data['Total Customer'] - data['active_customer']

    # Apply Funded CAC increase only for the specified years (2024 to 2028)
    mask = (data['Year'] >= 2024) & (data['Year'] <= 2028)
    data.loc[mask, 'Funded CAC'] = (data.loc[mask, 'Funded CAC'] * 0) + funded_cac_increase

    # Calculate GP/Active, total gross profit, LTV, LTV/CAC, Payback
    data['gp_per_active'] = (data['ARPU'] - data['Direct Cost'])
    data['total_gross_profit'] = data['gp_per_active'] * data['active_customer']
    data['ltv'] = (data['ARPU'] - data['Direct Cost']) / data['Churn Rate']
    data['ltv_cac_ratio'] = data['ltv'] / data['Funded CAC']
    data['payback'] = data['Funded CAC'] / (data['ARPU'] - data['Direct Cost'])
    data['payback'] = data['payback'].clip(lower=0)

    # Calculate New Customer and Total Customer for each year
    for year in range(2024, 2029):
        new_customer_column = f'New Customer {year}'
        total_customer_column = f'Total Customer {year}'

        # Assuming you have declared these variables somewhere
        new_customer_increase_value = globals()[f'new_customer_increase_{year}']

        mask = (data['Year'] == year)
        data.loc[mask, new_customer_column] = (data.loc[mask, new_customer_column] * 0) + new_customer_increase_value

        data.loc[mask, total_customer_column] = data.loc[mask, 'Total Customer'] + data.loc[mask, new_customer_column]

    # Calculate Revenue
    data['revenue'] = data['ARPU'] * data['active_customer'] / 1000

    return data

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
    new_customer_increase_2024 = st.sidebar.number_input('New Customer 2024 (Unit: Thousand)', min_value=100, max_value=3000, step=1, value=400)
    new_customer_increase_2025 = st.sidebar.number_input('New Customer 2025 (Unit: Thousand)', min_value=100, max_value=3000, step=1, value=400)
    new_customer_increase_2026 = st.sidebar.number_input('New Customer 2026 (Unit: Thousand)', min_value=100, max_value=3000, step=1, value=500)
    new_customer_increase_2027 = st.sidebar.number_input('New Customer 2027 (Unit: Thousand)', min_value=100, max_value=3000, step=1, value=600)
    new_customer_increase_2028 = st.sidebar.number_input('New Customer 2028 (Unit: Thousand)', min_value=100, max_value=3000, step=1, value=700)
    funded_cac_increase = st.sidebar.number_input('Funded CAC 2024-2028 (Unit: $)', min_value=3, max_value=50, step=1, value=10)

    # Process and calculate additional metrics with user input values
    processed_data = calculate_metrics(data, funded_cac_increase, new_customer_increase_2024, new_customer_increase_2025, new_customer_increase_2026, new_customer_increase_2027, new_customer_increase_2028)

    st.subheader(' Definition:')
    # Additional insights
    st.write("Payback is calculated using the formula of dividing Funded CAC by GP per Active.")
    
    # Visualization
    st.subheader(' Metrics Visualization:')

    # Column chart for Revenue by year
    fig_revenue_chart = go.Figure()

    # Add Revenue to the column chart with a different color
    fig_revenue_chart.add_trace(go.Bar(x=processed_data['Year'], y=processed_data['revenue'],
                                      name='Revenue',
                                      marker_color='#563D82',  
                                      text=processed_data['revenue'].round(2),
                                      textposition='outside'))
    
    fig_revenue_chart.update_layout(title='Revenue (Unit: Mil $)')

    fig_revenue_chart.update_xaxes(showgrid=False)  # Remove x-axis gridlines
    fig_revenue_chart.update_yaxes(showgrid=False)  # Remove y-axis gridlines

    st.plotly_chart(fig_revenue_chart)

    # Column chart for New Customer by year
    fig_new_customer_chart = go.Figure()

    # Add New Customer to the column chart with a different color
    fig_new_customer_chart.add_trace(go.Bar(x=processed_data['Year'], y=processed_data['New Customer'],
                                      name='New Customer',
                                      marker_color='#563D82',  
                                      text=processed_data['New Customer'].round(2),
                                      textposition='outside'))
    
    fig_new_customer_chart.update_layout(title='New Customers (Unit: Thousand)')

    fig_new_customer_chart.update_xaxes(showgrid=False)  # Remove x-axis gridlines
    fig_new_customer_chart.update_yaxes(showgrid=False)  # Remove y-axis gridlines

    st.plotly_chart(fig_new_customer_chart)

     # Column chart for Total Customer by year
    fig_total_customer_chart = go.Figure()

     # Add total Customer to the column chart with a different color
    fig_total_customer_chart.add_trace(go.Bar(x=processed_data['Year'], y=processed_data['Total Customer'],
                                      name='Total Customer',
                                      marker_color='#563D82',  
                                      text=processed_data['Total Customer'].round(2),
                                      textposition='outside'))
    
    fig_total_customer_chart.update_layout(title='Total Customers (Unit: Thousand)')

    fig_total_customer_chart.update_xaxes(showgrid=False)  # Remove x-axis gridlines
    fig_total_customer_chart.update_yaxes(showgrid=False)  # Remove y-axis gridlines

    st.plotly_chart(fig_total_customer_chart)

    # Column chart for Active Customer by year
    fig_active_customer_chart = go.Figure()

     # Add total Customer to the column chart with a different color
    fig_active_customer_chart.add_trace(go.Bar(x=processed_data['Year'], y=processed_data['active_customer'],
                                      name='Active Customers',
                                      marker_color='#563D82',  
                                      text=processed_data['active_customer'].round(2),
                                      textposition='outside'))
    
    fig_active_customer_chart.update_layout(title='Active Customers (Unit: Thousand)')

    fig_active_customer_chart.update_xaxes(showgrid=False)  # Remove x-axis gridlines
    fig_active_customer_chart.update_yaxes(showgrid=False)  # Remove y-axis gridlines

    st.plotly_chart(fig_active_customer_chart)

    st.title('Thank You')
