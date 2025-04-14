# Import required libraries
import dash                 # For building web applications
import pandas as pd         # For data manipulation and analysis
import plotly.express as px # For data visualization

from dash.dependencies import Input, Output # For building web applications
from dash import html                       # For building web applications
from dash import dcc                        # For building web applications


# Read the airline data into pandas data frame
spacex_df   = pd.read_csv("C:\\Users\\scott\\OneDrive\\Documentos\\Data Science\\DS_C9\\spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=
                      [html.H1(
                          'SpaceX Launch Records Dashboard',
                            style={
                                'textAlign': 'center',
                                    'color': (0,0,0),
                                'font-size': 40
                            }),

             # Add a dropdown list to enable Launch Site selection
             dcc.Dropdown(id='site-dropdown',
                          options=[
                                {'label': 'All Sites',    'value': 'All'},
                                {'label': 'CCAFS LC-40',  'value': 'CCAFS LC-40'},
                                {'label': 'VAFB SLC-4E',  'value': 'VAFB SLC-4E'},
                                {'label': 'KSC LC-39A',   'value': 'KSC LC-39A'},
                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                 ],
                          value='All',
                          placeholder='Select a Launch Site Here',
                          style={'color': (0,0,0)},
                          searchable=True
                                            ),
              html.Br(), 

              # Add a pie chart to show the total successful launches count for all sites
              html.Div(dcc.Graph(id='success-pie-chart')),
              html.Br(),

              html.P("Payload range (Kg):"),
              dcc.RangeSlider(id    = 'payload-slider', # Add a slider to select payload range
                              min   =  min_payload, 
                              max   =  max_payload, 
                              step  =  1000,
                              marks =  {
                                            0:  '0',
                                          500:  '500',
                                         2500:  '2500',
                                         5000:  '5000',
                                         7500:  '7500',
                                        10000: '10000'},
                              value = [min_payload, max_payload]),
               html.Br(),

                                # Add a scatter chart to show the correlation between payload and launch success
               html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id       = 'success-pie-chart', 
                     component_property = 'figure'),

              Input(component_id       = 'site-dropdown', 
                    component_property = 'value'))

# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
def get_pie_chart(entered_site):
    filtered_df = spacex_df

    if entered_site == 'All':
        fig = px.pie(filtered_df, 
                     values = 'Launch Outcome', 
                     names  = 'Launch Site', 
                     title  = 'Total Success Launches By Site')
        return fig

    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df = filtered_df.groupby(['Launch Site', 'Launch Outcome']).size().reset_index(name='Launch Outcome count')
        fig = px.pie(filtered_df, 
                     values = 'Launch Outcome count', 
                     names  = 'Launch Outcome', 
                     title  = 'Total Success Launches for site ' + entered_site)

        return fig

# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id       = 'success-payload-scatter-chart', 
           component_property = 'figure'),

    [Input(component_id       = 'site-dropdown', 
           component_property = 'value'),

     Input(component_id       = 'payload-slider', 
           component_property = 'value')]
)
def get_scatter_chart(entered_site, payload_mass):

    # Rename the class column to Launch Outcome
    spacex_df.rename(columns = {'class': 'Launch Outcome'}, inplace=True)
    
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_mass[0]) & 
        (spacex_df['Payload Mass (kg)'] <= payload_mass[1])
    ]
    if entered_site == 'All':
        fig = px.scatter(filtered_df, 
                         x = 'Payload Mass (kg)', 
                         y = 'Launch Outcome', 
                         color = 'Booster Version Category')
    
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, 
                         x = 'Payload Mass (kg)', 
                         y = 'Launch Outcome', 
                         color = 'Booster Version Category')
    return fig



# Run the app
if __name__ == '__main__':
    app.run_server()