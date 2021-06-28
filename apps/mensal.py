import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import base64
import os
import pathlib
from app import app




# meta_tags are required for the app layout to be mobile responsive


PATH = pathlib.Path(__file__).parent
clima_PATH = PATH.joinpath("../dados").resolve()
mensal_PATH = PATH.joinpath("../dados/mensal").resolve()
diario_PATH = PATH.joinpath("../dados/diario").resolve()


climatology = pd.DataFrame(pd.read_csv(clima_PATH.joinpath("Climatologia2.csv")))



rain_PATH = PATH.joinpath("../dados/diario/2021").resolve()
rain = pd.read_csv(rain_PATH.joinpath("junho.csv"))



dir = PATH.joinpath("../dados/mensal").resolve()


list = os.listdir(dir) # dir is your directory path
number_files = len(list)

dir_year = mensal_PATH
list_year = os.listdir(dir_year)
number_files_year = len(list_year)
year_options = [{'label': i.rstrip(".csv") , 'value': i.rstrip(".csv")} for i in list_year]


month_list = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

city_options = [{'label':i, 'value':i} for i in rain["municipio"].unique()]

city_climatology = [{'label':i, 'value':i} for i in sorted(climatology['nome_codigo'].unique())]

stations_options = rain[rain['municipio']=='Salvador']
stations_options = [{'label':i, 'value':i} for i in stations_options['estacao']]

graph_type = [{'label': 'Barras', 'value': 'Bar'},
            {'label': 'linhas', 'value': 'Scatter'}]

img_PATH = PATH.joinpath("../img").resolve()
image_filename1 = img_PATH.joinpath('logo_santiago.png')
encoded_image1 = base64.b64encode(open(image_filename1, 'rb').read())

layout = html.Div([
    dcc.Store(id='memory', storage_type='local'),
    dcc.Store(id='memory_anual', storage_type='local'),
    dbc.Row([ 
            dbc.Col(html.H1(children='Analise de Precipitação no Estado da Bahia', style={ 'textAlign': 'center'}, 
            className="mb-1"))
            ]),
    dbc.Row([html.H1(' ')]),
    dbc.Row([
            dbc.Col(dbc.Card(html.H2("Precipitação Mensal", className="text-center text-bold text-dark "), body=True, color="#c8c8c8"), 
            className="mb-1")
        ]),
    dbc.Row([
        dbc.Col([
            html.H4('Estações: ', style={ 'textAlign': 'center'}),
            html.H5('Ano: ' ),
            dcc.Dropdown(id = 'year_dropdown', options = year_options, value = year_options[-1]['value']),
            html.H1(' '),
            html.H5('Estações: '),
            dcc.Dropdown(id = 'stations_dropdown', options = city_options, value=['Salvador (J. Zoológico) - A401'], multi=True, style={'width': '70%', 'margin-left':'30px'}),
            html.H1(' ')
            ]),
        dbc.Col([
            html.H4('Climatologias(INMET): ', style={ 'textAlign': 'center'}),
            html.H1(' '),
            html.H5('Município: '),
            dcc.Dropdown(id = 'clima_dropdown', options = city_climatology, value=['(Clima)Salvador - 83229'], multi=True, style={'width': '70%', 'margin-left':'30px'}),
            html.H1(' '),
            html.H5('Tipo de Gráfico'),
            dcc.RadioItems(id = 'graph_type',options = graph_type, value='Scatter', labelStyle={'display': 'inline-block'})
            ])
    ]),
    dbc.Row([
        dbc.Col(html.H5(id= 'graph1_title', className="text-center"),
                className="mt-4")]),
    dcc.Graph(id='situation_graph_by_period'),
    dbc.Row([
        dbc.Col(html.H5('Tabela de Dados', className="text-center"),
                className="mt-5")
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='table1'))
    ]),
    dbc.Row(html.H1(' ')),
    dbc.Row([
        dbc.Col(dbc.Card(html.H3("Precipitação Anual", className="text-center text-bold text-dark "), body=True, color="#c8c8c8"), 
            className="mb-6")
    ]),
    dbc.Row([html.H1(' ')]),
    dbc.Row([
        dbc.Col([
            html.H4('Estações: ', style={ 'textAlign': 'center'}),
            html.H5('Escolha a Estação: '),
            dcc.Dropdown(id = 'stations_dropdown_anual', options = stations_options ,value='Salvador (J. Zoológico) - A401', style={'width': '70%', 'margin-left':'30px'}),
            html.H1(' '),
            html.H5('Ano: ' ),
            dcc.Dropdown(id = 'year_dropdown_anual', options = year_options, multi=True, value = [i.rstrip(".csv") for i in list_year][::-1]),
            html.H1(' '),
            ]),
        dbc.Col([
            html.H4('Climatologias(INMET): ', style={ 'textAlign': 'center'}),
            html.H1(' '),
            html.H5('Município: '),
            dcc.Dropdown(id = 'clima_dropdown_anual', options = city_climatology, value=['(Clima)Salvador - 83229'], multi=True, style={'width': '70%', 'margin-left':'30px'}),
            html.H1(' '),
            html.H5('Tipo de Gráfico'),
            ]),
    ]),
    dbc.Row([
        dbc.Col(html.H5(id= 'graph2_title', className="text-center"),
                className="mt-4")]),
    dcc.Graph(id='situation_graph_by_year'),
    dbc.Row(dbc.Col([html.Img(src='data:image/png;base64,{}'.format(encoded_image1.decode()), height=90)],style={ 'textAlign': 'center'})),
    html.H6("Developed by Alisson Santiago - alisson.santiago123@gmail.com", style={ 'textAlign': 'center'}),
])

@app.callback(
    Output('memory', 'data'),
    Input('year_dropdown', 'value')
)
def update_store(ano):

    df = pd.DataFrame(pd.read_csv(mensal_PATH.joinpath(ano + ".csv")))
    tabdict = dict(df)
    return tabdict

@app.callback(
    Output('graph1_title', 'children'),
    Input('year_dropdown', 'value')
)
def update_titles(year):
    graph1_title = 'Gráfico de Precipitação -' + year + '- X Climatologia(INMET)'
    return graph1_title

@app.callback(
    Output('stations_dropdown', 'options'),
    Output('stations_dropdown_anual', 'options'),
    Input('memory', 'data')
)
def update_stations(df):
    tabela = pd.DataFrame.from_dict(df)
    city_options = [{'label':i, 'value':i} for i in sorted(tabela["estacao"].unique())]
    return city_options, city_options

@app.callback(
    Output('situation_graph_by_period', 'figure'),
    [Input('stations_dropdown', 'value'),
    Input('clima_dropdown', 'value'),
    Input('graph_type', 'value'),
    Input('memory', 'data')])

def update_graph1(stations_value,clima_value,graph_type, df):
    

    df = pd.DataFrame.from_dict(df)
    df.set_index('estacao', inplace=True)

    df_clima = climatology.set_index('nome_codigo')

    colors = ['#05a0ff', '#ffbab1','#8cffab', '#f8f85c','#cb7bf9', '#00cbe5','#ff73dc', '#ffa860', '#b88459', '#8e3378']
    colors2 = ['#080808','#a7a7a7','#bea672', '#91c4c4', '#636771']

    if graph_type == 'Bar':
        trace_1 = []
        t_1 = 0
        for i in stations_value:
            df1 = df[df.index == i].iloc[:,5:].T
            trace_1.append(go.Bar(name=i, x=df1.index, y=df1[i]))
            t_1+=1

        t_2=0
        for j in clima_value:
            df2 = df_clima[df_clima.index == j].iloc[:,5:-1].T
            trace_1.append(go.Scatter(name=j, x=df2.index, y=df2[j], line={'dash': 'dash'}, line_color = colors2[t_2]))
            t_2+=1
        data = trace_1

    if graph_type == 'Scatter':
        trace_1 = []
        t_1 = 0
        for i in stations_value:
            df1 = df[df.index == i].iloc[:,5:].T
            trace_1.append(go.Scatter(name=i, x=df1.index, y=df1[i]))
            t_1+=1

        t_2=0
        for j in clima_value:
            df2 = df_clima[df_clima.index == j].iloc[:,5:-1].T
            trace_1.append(go.Scatter(name=j, x=df2.index, y=df2[j], line={'dash': 'dash'}, line_color = colors2[t_2]))
            t_2+=1
        data = trace_1

    layout = go.Layout(
        yaxis={'title': "Precipitação (mm)"},
        barmode='stack',
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor = 'rgba(0,0,0,0)',
        template="seaborn",
        margin=dict(t=20)
    )

    return  {'data': data, 'layout': layout}

@app.callback(
    Output('table1','children'),
    [Input('stations_dropdown', 'value'),
    Input('clima_dropdown', 'value'),
    Input('memory', 'data')]
)
def update_table1(dropdown1,dropdown2,df):
    df = pd.DataFrame.from_dict(df)
    tab_total = df.loc[df['estacao'].isin(dropdown1)]

    filtered_table = pd.concat([tab_total.iloc[:,0:2],tab_total.iloc[:,6:]], axis=1)
    filtered_table.rename(columns={'municipio': 'Município', 'estacao': 'Estação'}, inplace=True)

    df_clima = climatology
    tab_filt_clima = df_clima.loc[df_clima['nome_codigo'].isin(dropdown2)]
    
    filtered_clima = pd.concat([tab_filt_clima.loc[:,['municipio','nome_codigo']],tab_filt_clima.iloc[:,6:-1]], axis=1)
    filtered_clima.rename(columns={'municipio': 'Município', 'nome_codigo': 'Estação'}, inplace=True)

    tabela_final = pd.concat([filtered_table,filtered_clima])
    table1 = dbc.Table.from_dataframe(tabela_final, striped=True, bordered=True, hover=True, size = 'sm')
    return table1

@app.callback(
    Output('memory_anual', 'data'),
    [Input('stations_dropdown_anual', 'value'),
    Input('year_dropdown_anual', 'value')]
)

def update_memory_anual(station,years):
    data = pd.DataFrame()

    for i in years[::-1]:
        df_test2 = pd.DataFrame(pd.read_csv(mensal_PATH.joinpath(i + ".csv")))
        test_tab = df_test2.loc[df_test2['estacao'].isin([station])]
        test_tab = test_tab.assign(Ano = i)
        data[i] = test_tab.iloc[0,6:-1]
    data = dict(data)
    return data


@app.callback(
    Output('situation_graph_by_year', 'figure'),
    Input('stations_dropdown_anual', 'value'),
    Input('year_dropdown_anual', 'value'),
    Input('clima_dropdown_anual', 'value'),
    Input( 'memory_anual', 'data')
)
def update_graph2(station,years, stations_clima, df):
    df1 = pd.DataFrame.from_dict(df)
    
    df_clima = climatology.set_index('nome_codigo')
    
    colors = ['#05a0ff', '#ffbab1','#8cffab', '#f8f85c','#cb7bf9', '#00cbe5','#ff73dc', '#ffa860', '#b88459', '#8e3378']
    colors2 = ['#080808','#a7a7a7','#bea672', '#91c4c4', '#636771'] 

    trace_1 = []

    t_1 = 0
    for i in years:
        trace_1.append(go.Scatter(name=i, x=month_list, y=df1[i]))
        t_1+=1

    t_2=0
    for j in stations_clima:
        df2 = df_clima[df_clima.index == j].iloc[:,5:-1].T
        trace_1.append(go.Scatter(name=j, x=df2.index, y=df2[j], line={'dash': 'dash'}, line_color = colors2[t_2]))
        t_2+=1
    data = trace_1
    
    layout = go.Layout(
            yaxis={'title': "Precipitação (mm)"},
            barmode='stack',
            paper_bgcolor = 'rgba(0,0,0,0)',
            plot_bgcolor = 'rgba(0,0,0,0)',
            template="seaborn",
            margin=dict(t=20)
        )

    return  {'data': data, 'layout': layout}


