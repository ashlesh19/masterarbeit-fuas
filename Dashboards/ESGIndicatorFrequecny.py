# Import required libraries
import pandas as pd
from flask import Flask
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

# Load the CSV file
file_path = 'database.csv'
df = pd.read_csv(file_path)

# Extract the list of companies
companies = df['company'].unique()

# Load the alias CSV file
alias_file_path = 'esg_indicator_aliases.csv'
alias_df = pd.read_csv(alias_file_path)

# Create a dictionary to map indicators to aliases
indicator_to_alias = {alias.lower(): indicator for alias, indicator in zip(alias_df['Alias'], alias_df['indicator'])}

# Define the indicators for each category
e_indicators = [
    "climate_change_mitigation", "decarbonisation", "financial_resources_allocated_for_esg",
    "achieved_ghg_emission_reductions", "expected_ghg_emission_reductions", "total_energy_consumption",
    "total_energy_consumption_from_fossil_sources", "total_energy_consumption_from_nuclear_sources",
    "renewable_energy_production", "total_energy_consumption_from_renewable_sources", "scope_1", "scope_2",
    "scope_3", "total_ghg_emissions", "emissions_to_air_by_pollutant", "emissions_to_water_by_pollutant",
    "emissions_to_soil_by_pollutant", "total_amount_of_substances_of_concern_hazard_class",
    "total_water_consumption", "total_water_recycled_and_reused", "policy_related_to_water_and_marine_resources",
    "total_waste_generated", "total_amount_of_hazardous_waste", "total_amount_of_radioactive_waste"
]

s_indicators = [
    "human_rights_policy_commitments_for_employees", "workplace_accident_prevention_policy",
    "elimination_of_discrimination", "grievance_or_complaints_handling", "mitigate_negative_impacts_on_own_workforce",
    "delivering_positive_impacts_for_own_workforce", "number_of_employees", "number_of_board_members",
    "percentage_of_employees_at_top_management_level", "number_of_employees_under_30", "percentage_of_employees_under_30",
    "number_of_employees_between_30_and_50", "percentage_of_employees_between_30_and_50", "number_of_employees_over_50",
    "percentage_of_employees_over_50", "number_of_fatalities_in_own_workforce", "number_of_work_related_accidents",
    "number_of_work_related_ill_health", "number_incidents_of_discrimination", "number_of_complaints_filed",
    "number_of_severe_human_rights_issues", "amount_of_fines_for_severe_human_rights_issues",
    "human_rights_policy_commitments_for_customers_and_end_users"
]
    
g_indicators = [
    "whistleblowing_protection", "policy_for_animal_welfare", "training_within_organisation_on_business_conduct",
    "disclosure_on_corruption_and_bribery", "violation_of_anti_corruption_and_anti_bribery_laws",
    "fines_paid_for_violation_of_anti_corruption_and_anti_bribery_laws", "financial_political_contributions",
    "legal_proceedings_for_late_payments", "information_regarding_payment_practices"
]

# Combine all indicators
all_indicators = e_indicators + s_indicators + g_indicators

# Filter the indicators to only include those present in the CSV columns
filtered_indicators = [ind for ind in all_indicators if ind in df.columns]

# Initialize the Flask app
server = Flask(__name__)

# Initialize the Dash app
app = dash.Dash(__name__, server=server, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'])

app.layout = html.Div([
    html.Div([
        html.H1("ESG Indicator-Specific Sentence Analysis Dashboard", className="text-center mb-4"),
        
        html.Div([
            html.Label("Select Company:", className="font-weight-bold"),
            dcc.Dropdown(
                id='company-dropdown',
                options=[{'label': company, 'value': company} for company in companies],
                placeholder="Select a company",
                className="mb-3"
            ),
        ], className="form-group"),
        
        html.Div([
            html.Label("Select Indicator Type:", className="font-weight-bold"),
            dcc.Dropdown(
                id='indicator-type-dropdown',
                options=[
                    {'label': 'Top 5 Indicators', 'value': 'top_5'},
                    {'label': 'Top 5 Environmental Indicators', 'value': 'top_5_environmental'},
                    {'label': 'Top 5 Social Indicators', 'value': 'top_5_social'},
                    {'label': 'Top 5 Governance Indicators', 'value': 'top_5_governance'}
                ],
                placeholder="Select indicator type",
                className="mb-3"
            ),
        ], className="form-group"),
        
        html.Div([
            html.Button('Submit', id='submit-button', n_clicks=0, className="btn btn-primary btn-lg btn-block mb-4"),
        ], className="form-group text-center"),
        
        html.Div(id='graph-container', className="mt-4")
    ], className="container")
])

@app.callback(
    Output('graph-container', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('company-dropdown', 'value'),
     State('indicator-type-dropdown', 'value')]
)
def update_graph(n_clicks, selected_company, indicator_type):
    if n_clicks > 0 and selected_company and indicator_type:
        filtered_df = df[df['company'] == selected_company]
        
        if indicator_type == 'top_5':
            indicators = filtered_indicators
        elif indicator_type == 'top_5_environmental':
            indicators = [ind for ind in e_indicators if ind in filtered_indicators]
        elif indicator_type == 'top_5_social':
            indicators = [ind for ind in s_indicators if ind in filtered_indicators]
        elif indicator_type == 'top_5_governance':
            indicators = [ind for ind in g_indicators if ind in filtered_indicators]
        
        indicator_totals = filtered_df[indicators].sum().sort_values(ascending=False)
        top_indicators = indicator_totals.index[:5]

        def get_indicator_with_category(indicator):
            category = ""
            if indicator in e_indicators:
                category = "(E)"
            elif indicator in s_indicators:
                category = "(S)"
            elif indicator in g_indicators:
                category = "(G)"
            
            if indicator_type == 'top_5':
                return f"{indicator_to_alias.get(indicator.lower(), indicator)} {category}"
            else:
                return f"{indicator_to_alias.get(indicator.lower(), indicator)}"
        
        figure = {
            'data': [
                {
                    'x': filtered_df['year'],
                    'y': filtered_df[indicator],
                    'type': 'line',
                    'name': get_indicator_with_category(indicator)  # Use alias and category for legend
                } for indicator in top_indicators
            ],
            'layout': {
                'title': f'{selected_company} ESG Indicators',
                'xaxis': {
                    'title': 'Year',
                    'type': 'category',
                    'categoryorder': 'category ascending'
                },
                'yaxis': {'title': 'ESG Indicator Frequency (Sentence Level)'}
            }
        }
        return dcc.Graph(id='indicator-graph', figure=figure)
    else:
        return html.Div("Please select both a company and an indicator type, then click submit.", className="alert alert-warning")

if __name__ == '__main__':
    app.run_server(debug=True)
