import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Function to calculate additional metrics
def calculate_metrics(data, funded_cac_increase, new_customer_increases2024, new_customer_increases2025, new_customer_increases2026, new_customer_increases2027, new_customer_increases2028):
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

    # Apply Funded CAC increase only for the specified years (2024 to 2028)
    mask_cac = (data['Year'] >= 2024) & (data['Year'] <= 2028)
    data.loc[mask_cac, 'Funded CAC'] = (data.loc[mask_cac, 'Funded CAC'] * 0) + funded_cac_increase

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
    data['revenue'] = data['ARPU'] * data['active_customer'] / 1000
    data['gp_per_active'] = (data['ARPU'] - data['Direct Cost'])
    data['total_gross_profit'] = data['gp_per_active'] * data['active_customer']
    data['ltv'] = (data['ARPU'] - data['Direct Cost']) / data['Churn Rate']
    data['ltv_cac_ratio'] = data['ltv'] / data['Funded CAC']
    data['payback'] = data['Funded CAC'] / (data['ARPU'] - data['Direct Cost'])
    data['payback'] = data['payback'].clip(lower=0)
    data['Funded Customer'] = (data['Total Customer'] * (data['Funding Rate']/100)).round(2)

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
    funded_cac_increase = st.sidebar.number_input('Funded CAC 2024-2028 (Unit: $)', min_value=3, max_value=50, step=1, value=10)
    new_customer_increases2024 = st.sidebar.number_input('New Customer 2024 (Unit: Thousand)', min_value=100, max_value=3000, step=50, value= 400)
    new_customer_increases2025 = st.sidebar.number_input('New Customer 2025 (Unit: Thousand)', min_value=100, max_value=3000, step=50, value= 400)
    new_customer_increases2026 = st.sidebar.number_input('New Customer 2026 (Unit: Thousand)', min_value=100, max_value=3000, step=50, value= 500)
    new_customer_increases2027 = st.sidebar.number_input('New Customer 2027 (Unit: Thousand)', min_value=100, max_value=3000, step=50, value= 600)
    new_customer_increases2028 = st.sidebar.number_input('New Customer 2028 (Unit: Thousand)', min_value=100, max_value=3000, step=50, value= 700)

    new_customer_increases = [new_customer_increases2024, new_customer_increases2025, new_customer_increases2026, new_customer_increases2027, new_customer_increases2028]

    # Process and calculate additional metrics with user input values
    processed_data = calculate_metrics(data, funded_cac_increase, new_customer_increases2024, new_customer_increases2025, new_customer_increases2026, new_customer_increases2027, new_customer_increases2028)

    st.subheader(' Definition:')
    # Additional insights
    st.write("Payback is calculated using the formula of dividing Funded CAC by GP per Active.")

    # Visualization
    st.subheader(' Metrics Visualization:')

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

    # Column chart for New Customer by year
    fig_new_customer_chart = go.Figure()
    create_column_chart(fig_new_customer_chart, processed_data['Year'], processed_data['New Customer'], 'New Customers (Unit: Thousand)')
    st.plotly_chart(fig_new_customer_chart)

    # Column chart for Total Customer by year
    fig_total_customer_chart = go.Figure()
    create_column_chart(fig_total_customer_chart, processed_data['Year'], processed_data['Total Customer'], 'Total Customers (Unit: Thousand)')
    st.plotly_chart(fig_total_customer_chart)

# Column chart for Active Customer by year
fig_active_customer_chart = go.Figure()
create_column_chart(fig_active_customer_chart, processed_data['Year'], processed_data['active_customer'], 'Active Customers (Unit: Thousand)')
st.plotly_chart(fig_active_customer_chart)

# Corrected indentation for the next block
st.subheader('Customer Base (Unit: Thousand Customers)')
customer_base_data = {
    'Year': processed_data['Year'],
    'New Customers': processed_data['New Customer'].round(2),
    'Total Customers': processed_data['Total Customer'].round(2),
    '%Active Rate': processed_data['Active Rate'].round(2),
    'Active Customers': processed_data['active_customer'].round(2),
    '%Funding Rate': processed_data['Funding Rate'].round(2),
    'Funded Customer': processed_data['Funded Customer'].round(2)
}

customer_base_table = pd.DataFrame(customer_base_data)
st.table(customer_base_table)



