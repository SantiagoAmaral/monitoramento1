
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

import base64
import pathlib
from app import app


# Cards of home page
card_content_diario = [
    dbc.CardBody(
        [
            html.H4("Precipitação Diária", className="text-dark text-center"),
            html.P(
                "Dados de Chuva Diária",
                className="text-dark text-center",),
    ]),
]

card_content_mensal = [
    dbc.CardBody(
        [
            html.H4("Precipitação Mensal e Anual", className="text-dark text-center"),
            html.P(
                "Analises de Chuva Mensal e Anual",
                className="text-dark text-center",)
    ]),
]

card_content_focos = [
    dbc.CardBody(
        [
            html.H4("Focos de Calor", className="text-dark text-center"),
            html.P(
                "(em construção)",
                className="text-dark text-center",),
    ]),
]


# Layout
layout = html.Div([
    dbc.Row([
        dbc.Col(html.H1('Monitoramento', style={ 'textAlign': 'center',"margin-top": "50px"}))
    ]),
    dbc.Row(html.H1(' ', style={"margin-top": "50px"})),
    dbc.Row([
        dbc.Col(html.A(dbc.Card(card_content_diario, color= '#adb9ca'), href="/apps/diario"), width={"size": 3}),
        dbc.Col(html.A(dbc.Card(card_content_mensal, color= '#d9d9d9'), href="/apps/mensal"), width={"size": 3}),
        dbc.Col(html.A(dbc.Card(card_content_focos, color= '#fbe5d6'), href="#"), width={"size": 3}) 
    ], justify="center"),
    dbc.Row(html.H1(' ', style={"margin-top": "10px"})),
    dbc.Row([html.H6('Fonte de dados: ', style={ 'textAlign': 'center',"margin-top": "50px"})], justify='center'),
    dbc.Row([html.A('INEMA - Instituto do Meio Ambiente e Recursos Hídricos - SEIA MONITORAMENTO', href = 'http://monitoramento.seia.ba.gov.br/', target = '_blank')], justify='center'),
    dbc.Row([html.A('DIRAM/COCEP - Coordenação de Estudos de Clima e Projetos Especiais', href = 'http://www.inema.ba.gov.br/monitoramento/indice-precipitacao/', target = '_blank')], justify='center'),
    dbc.Row([html.A('CEMADEN - Centro Nacional de Monitoramento e Alertas de Desastres Naturais', href = 'http://www2.cemaden.gov.br/mapainterativo/#', target = '_blank')], justify='center'),
    dbc.Row([html.A('INMET - Instituto Nacional de Meteorologia',href = 'https://portal.inmet.gov.br/', target = '_blank')], justify='center'),
    dbc.Row([html.A('ANA - Agência Nacional de Águas',href = 'https://www.snirh.gov.br/hidroweb/apresentacao', target = '_blank'),
    ], justify='center'),
    html.H6("Developed by Alisson Santiago - alisson.santiago123@gmail.com", style={ 'textAlign': 'center', "margin-top": "40px"}),
    html.A('Linkedin: Alisson Santiago Amaral',href = 'https://www.linkedin.com/in/alisson-santiago-amaral-3a75b566/', target = '_blank'), justify='center')
])
