import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

# Load the CSV file
file_path = 'database.csv'
df = pd.read_csv(file_path)
plt.switch_backend('Agg')

# List of ESG indicators
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

# Filter the indicators to include only those that exist in the dataset
e_indicators = [col for col in e_indicators if col in df.columns]
s_indicators = [col for col in s_indicators if col in df.columns]
g_indicators = [col for col in g_indicators if col in df.columns]

# Fill NaN values with 0
df[e_indicators] = df[e_indicators].fillna(0)
df[s_indicators] = df[s_indicators].fillna(0)
df[g_indicators] = df[g_indicators].fillna(0)

# Helper function to create heatmaps
def generate_heatmap(data, title, yaxis_label=True):
    plt.figure(figsize=(10, 7))  # Rescaled image size
    sns.heatmap(data.set_index('industry').T, annot=True, cmap="YlGnBu", cbar=True, linewidths=.5)
    plt.title(title, fontsize=16)
    plt.xlabel("Industry", fontsize=12)
    plt.ylabel("Indicators" if yaxis_label else "", fontsize=12)  # Control y-axis label

    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels to avoid cutting off
    plt.yticks(rotation=0)  # Ensure y-axis labels are horizontal
    plt.tight_layout()  # Automatically adjust plot to ensure nothing is cut off

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return image_base64

def generate_difference_heatmap(data1, data2, title):
    # Ensure that both datasets contain the same industries
    all_industries = set(data1['industry']).union(set(data2['industry']))

    # Add missing industries with zero values in data1
    for industry in all_industries:
        if industry not in data1['industry'].values:
            missing_row = pd.DataFrame([[industry] + [0] * (data1.shape[1] - 1)], columns=data1.columns)
            data1 = pd.concat([data1, missing_row], ignore_index=True)

    # Add missing industries with zero values in data2
    for industry in all_industries:
        if industry not in data2['industry'].values:
            missing_row = pd.DataFrame([[industry] + [0] * (data2.shape[1] - 1)], columns=data2.columns)
            data2 = pd.concat([data2, missing_row], ignore_index=True)

    # Ensure that the data is sorted by industry to align rows correctly
    data1 = data1.sort_values('industry').reset_index(drop=True)
    data2 = data2.sort_values('industry').reset_index(drop=True)

    # Calculate the difference
    diff_data = data2.set_index('industry') - data1.set_index('industry')

    plt.figure(figsize=(10, 7))
    sns.heatmap(diff_data.T, annot=True, cmap="coolwarm", cbar=True, linewidths=.5, vmin=-1, vmax=1)
    plt.title(title, fontsize=16)
    plt.xlabel("Industry", fontsize=12)
    plt.ylabel("Indicators", fontsize=12)

    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return image_base64

# Initialize Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'])

# Generate list of years for dropdown
years = sorted(df['year'].unique())

app.layout = html.Div([
    html.Div([
        html.H1("ESG Heatmap Dashboard", className="text-center mb-4"),
        
        html.Div([
            html.Label("Select Year 1:", className="font-weight-bold"),
            dcc.Dropdown(
                id='year1-dropdown',
                options=[{'label': str(year), 'value': year} for year in years],
                value=years[0],
                className="mb-4"
            ),
        ], className="form-group"),
        
        html.Div([
            html.Label("Select Year 2:", className="font-weight-bold"),
            dcc.Dropdown(
                id='year2-dropdown',
                options=[{'label': str(year), 'value': year} for year in years],
                value=years[1] if len(years) > 1 else years[0],
                className="mb-4"
            ),
        ], className="form-group"),
        
        html.Div([
            html.Label("Select ESG Category:", className="font-weight-bold"),
            dcc.Dropdown(
                id='category-dropdown',
                options=[
                    {'label': 'Environmental Indicators', 'value': 'environmental'},
                    {'label': 'Social Indicators', 'value': 'social'},
                    {'label': 'Governance Indicators', 'value': 'governance'}
                ],
                value='environmental',
                className="mb-4"
            ),
        ], className="form-group"),
        
        html.Div([
            html.Button('Submit', id='submit-button', n_clicks=0, className="btn btn-primary btn-lg btn-block mb-4"),
        ], className="form-group text-center"),
        
        html.Div([
            html.Div([
                html.Img(id='heatmap1-image', style={'width': '45%', 'display': 'inline-block'}),
                html.Img(id='heatmap2-image', style={'width': '45%', 'display': 'inline-block', 'margin-left': '10px'}),
            ], className="text-center"),
        ]),
        
        html.Div([
            html.H3("Difference Heatmap", className="text-center mt-4"),
            html.Img(id='difference-heatmap-image', style={'width': '80%', 'height': 'auto'})
        ], className="text-center mt-4")
    ], className="container")
])

@app.callback(
    [Output('heatmap1-image', 'src'),
     Output('heatmap2-image', 'src'),
     Output('difference-heatmap-image', 'src')],
    [Input('submit-button', 'n_clicks')],
    [State('year1-dropdown', 'value'), State('year2-dropdown', 'value'), State('category-dropdown', 'value')]
)
def update_heatmaps(n_clicks, selected_year1, selected_year2, category):
    if n_clicks > 0:  # Only generate heatmap after clicking submit
        # Filter data by selected years
        df_year1 = df[df['year'] == selected_year1]
        df_year2 = df[df['year'] == selected_year2]
        
        industry_prevalence_e1 = df_year1.groupby('industry')[e_indicators].apply(lambda x: (x > 0).mean()).reset_index()
        industry_prevalence_s1 = df_year1.groupby('industry')[s_indicators].apply(lambda x: (x > 0).mean()).reset_index()
        industry_prevalence_g1 = df_year1.groupby('industry')[g_indicators].apply(lambda x: (x > 0).mean()).reset_index()

        industry_prevalence_e2 = df_year2.groupby('industry')[e_indicators].apply(lambda x: (x > 0).mean()).reset_index()
        industry_prevalence_s2 = df_year2.groupby('industry')[s_indicators].apply(lambda x: (x > 0).mean()).reset_index()
        industry_prevalence_g2 = df_year2.groupby('industry')[g_indicators].apply(lambda x: (x > 0).mean()).reset_index()

        if category == 'environmental':
            heatmap1 = generate_heatmap(industry_prevalence_e1, f"Year {selected_year1} - Environmental ESG Indicators by Industry", yaxis_label=True)
            heatmap2 = generate_heatmap(industry_prevalence_e2, f"Year {selected_year2} - Environmental ESG Indicators by Industry", yaxis_label=False)
            difference_heatmap = generate_difference_heatmap(industry_prevalence_e1, industry_prevalence_e2, "Difference in Environmental ESG Indicators by Industry")
        elif category == 'social':
            heatmap1 = generate_heatmap(industry_prevalence_s1, f"Year {selected_year1} - Social ESG Indicators by Industry", yaxis_label=True)
            heatmap2 = generate_heatmap(industry_prevalence_s2, f"Year {selected_year2} - Social ESG Indicators by Industry", yaxis_label=False)
            difference_heatmap = generate_difference_heatmap(industry_prevalence_s1, industry_prevalence_s2, "Difference in Social ESG Indicators by Industry")
        elif category == 'governance':
            heatmap1 = generate_heatmap(industry_prevalence_g1, f"Year {selected_year1} - Governance ESG Indicators by Industry", yaxis_label=True)
            heatmap2 = generate_heatmap(industry_prevalence_g2, f"Year {selected_year2} - Governance ESG Indicators by Industry", yaxis_label=False)
            difference_heatmap = generate_difference_heatmap(industry_prevalence_g1, industry_prevalence_g2, "Difference in Governance ESG Indicators by Industry")
        
        return f"data:image/png;base64,{heatmap1}", f"data:image/png;base64,{heatmap2}", f"data:image/png;base64,{difference_heatmap}"
    return None, None, None  # Don't display an image before the button is clicked

if __name__ == '__main__':
    app.run_server(debug=True)

