
import dash_core_components as dcc
import dash_html_components as html
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import home,diario, mensal


card_content_bar = [
    dbc.CardBody([
                    html.H1("Dashboard de Monitoramento Ambiental no Estado da Bahia", 
                className="text-center text-bold text-dark "),
                dbc.Button("Home ", href="/apps/home", color="success", className="mt-auto text-end"),
                dbc.Button(" Diario ", href="/apps/diario", color="success", className="mt-auto text-end"),
                dbc.Button(" Mensal ", href="/apps/mensal", color="success", className="mt-auto text-end"),
                dbc.Button(" Focos ", href="#", color="success", className="mt-auto text-end"),
                ]),
]

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dbc.Row([html.A(dbc.Card(card_content_bar, color= '#adb9ca'),className="w-100 mb-3")], align="center", style={ 'textAlign': 'center'}),
    ]),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/home':
        return home.layout
    if pathname == '/apps/diario':
        return diario.layout
    if pathname == '/apps/mensal':
        return mensal.layout
    else:
        return home.layout


if __name__ == '__main__':
    app.run_server(debug=True)
