from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Databse CSV file
df = pd.read_csv('database.csv')

e_indicators = [
    "climate_change_mitigation", "decarbonisation", "financial_resources_allocated_for_esg",
    "achieved_ghg_emission_reductions", "expected_ghg_emission_reductions", "total_energy_consumption",
    "total_energy_consumption_from_fossil_sources", "total_energy_consumption_from_nuclear_sources",
    "renewable_energy_production", "total_energy_consumption_from_renewable_sources", "scope_1", "scope_2",
    "scope_3", "total_ghg_emissions", "emissions_to_air_by_pollutant", "total_water_consumption",
    "policy_related_to_water_and_marine_resources", "total_waste_generated", "total_amount_of_hazardous_waste"
]

s_indicators = [
    "human_rights_policy_commitments_for_employees", "workplace_accident_prevention_policy",
    "elimination_of_discrimination", "grievance_or_complaints_handling", "mitigate_negative_impacts_on_own_workforce",
    "delivering_positive_impacts_for_own_workforce", "number_of_employees", "number_of_board_members",
    "percentage_of_employees_at_top_management_level", "number_of_work_related_ill_health", 
    "number_of_severe_human_rights_issues", "human_rights_policy_commitments_for_customers_and_end_users"
]

g_indicators = [
    "whistleblowing_protection", "training_within_organisation_on_business_conduct",
    "disclosure_on_corruption_and_bribery", "violation_of_anti_corruption_and_anti_bribery_laws",
    "fines_paid_for_violation_of_anti_corruption_and_anti_bribery_laws", "legal_proceedings_for_late_payments"
]

colors = {
    'E': 'mediumseagreen',
    'S': 'dodgerblue',
    'G': 'orange'
}

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("ESG Indicators Dashboard", className="text-center mt-4"))),
    dbc.Row(dbc.Col(html.Div("Select an Industry:"))),
    dbc.Row(dbc.Col(dcc.Dropdown(
        id='industry-dropdown',
        options=[{'label': i, 'value': i} for i in df['industry'].unique()],
        value=df['industry'].unique()[0],
        style={'marginTop': '20px'}
    ))),
    dbc.Row(dbc.Col(html.Div(id='output-data-upload'))),
    dbc.Row(dbc.Col(html.Div(id='graphs-container')))
])

@app.callback(
    [Output('graphs-container', 'children'),
     Output('output-data-upload', 'children')],
    [Input('industry-dropdown', 'value')]
)
def update_graph(selected_industry):
    industry_data = df[df['industry'] == selected_industry]
    
    esg_columns = industry_data.columns[3:-1]
    
    industry_data['E'] = industry_data[e_indicators].notnull().sum(axis=1)
    industry_data['S'] = industry_data[s_indicators].notnull().sum(axis=1)
    industry_data['G'] = industry_data[g_indicators].notnull().sum(axis=1)
    
    company_totals = industry_data.groupby('company_name').agg(
        E=('E', 'mean'),
        S=('S', 'mean'),
        G=('G', 'mean'),
        years_reported=('year', 'count')
    )
    
    company_totals = company_totals[company_totals['years_reported'] >= 3]
    
    company_totals = company_totals.round(0).astype(int)
    
    company_totals['Total'] = company_totals[['E', 'S', 'G']].sum(axis=1)
    company_totals = company_totals.sort_values(by=['Total', 'E','years_reported'], ascending=[False, False, False])
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, len(company_totals) * 0.3 + 2))  # Adjust the figure size dynamically based on the number of companies
    bar_width = 0.6  # Adjust the bar width to make the bars more compact
    companies = company_totals.index
    
    bars_E = ax.barh(companies, company_totals['E'], color=colors['E'], edgecolor='black', label='Environmental', height=bar_width)
    bars_S = ax.barh(companies, company_totals['S'], left=company_totals['E'], color=colors['S'], edgecolor='black', label='Social', height=bar_width)
    bars_G = ax.barh(companies, company_totals['G'], left=company_totals['E'] + company_totals['S'], color=colors['G'], edgecolor='black', label='Governance', height=bar_width)
    
    ax.set_title(f'Average ESG Indicators Disclosed by Firms ({selected_industry})', pad=20)
    ax.set_xlabel('Average Number of Indicators Disclosed')
    ax.set_ylabel('Firms')
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    ax.invert_yaxis()
    ax.legend()
    
    for bar in bars_E:
        width = bar.get_width()
        label_x_pos = width / 2
        ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'{int(width)}', ha='center', va='center', color='black')

    for bar in bars_S:
        width = bar.get_width()
        label_x_pos = bar.get_x() + width / 2
        ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'{int(width)}', ha='center', va='center', color='black')

    for bar in bars_G:
        width = bar.get_width()
        label_x_pos = bar.get_x() + width / 2
        ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'{int(width)}', ha='center', va='center', color='black')
    
    plt.subplots_adjust(top=0.9)  
    plt.tight_layout(rect=[0, 0, 1, 0.95])  
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode()
    
    # HTML
    table = dbc.Table.from_dataframe(company_totals.reset_index(), striped=True, bordered=True, hover=True)
    
    return html.Img(src=f'data:image/png;base64,{img_base64}'), table

# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
