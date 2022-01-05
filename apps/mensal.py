
#Monthly page
#written by Alisson Santiago

#import all libraries
import pandas as pd
import plotly.express as px
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import os
import pathlib
from app import app




# app config
app.config.external_stylesheets = [dbc.themes.SLATE]

#PATHs where the data is.
PATH = pathlib.Path(__file__).parent
clima_PATH = PATH.joinpath("../dados").resolve()
mensal_PATH = PATH.joinpath("../dados/mensal").resolve()
diario_PATH = PATH.joinpath("../dados/diario").resolve()

#Climatology data
climatology = pd.DataFrame(pd.read_csv(clima_PATH.joinpath("climatologia2.csv")))

list_year = sorted(os.listdir(mensal_PATH))
number_files_year = len(list_year)
year_options = [{'label': i.rstrip(".csv") , 'value': i.rstrip(".csv")} for i in list_year]

month_list = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

dir_diario = diario_PATH.joinpath(year_options[-1]['value'])
list_diario_2 = os.listdir(dir_diario)
number_files_diario = len(list_diario_2)
month_options2 = [{'label': i.rstrip(".csv") , 'value': i.rstrip(".csv")} for i in month_list[:number_files_diario]]

rain = pd.DataFrame(pd.read_csv(diario_PATH.joinpath(year_options[-1]['value'] + '/' + month_options2[-1]['value'] + '.csv')))

#Dictionaries for options
date_options2 = [{ 'label': i, 'value': i} for i in rain.columns[8:]]
city_climatology = [{'label':i, 'value':i} for i in sorted(climatology['nome_codigo'].unique())]
graph_type = [{'label': 'Barras', 'value': 'Bar'},
            {'label': 'Linhas', 'value': 'Scatter'}]
research_type = [{'label': 'Por Ano', 'value': 'Ano'},
            {'label': 'Por Estação', 'value': 'Estação'}]

# Dash layout
layout = html.Div([
    # Data Stores
    dcc.Store(id='memory', storage_type='local'),
    dcc.Store(id='memory_anual', storage_type='local'),
            # Titles
    dbc.Row([
            dbc.Col(html.H1(children='Analise de Precipitação Mensal no Estado da Bahia', style={ 'textAlign': 'center', 'color': 'white'}, 
            className="mb-1"))
            ]),
    dbc.Row([html.H1(' ', style={"margin-top": "10px"})
            ]),
            #Dropdowns years and stations
    dbc.Row([
            dbc.Col(dcc.Graph(id='estacoes-maps'), width={"size": 6 ,"offset": 1}, md=4),
            dbc.Col([html.H6('Ano: ', style={ "margin-top": "10px"}),
                    dcc.Dropdown(id = 'year_dropdown', options = year_options, value = year_options[-1]['value'], 
                                persistence=True,persistence_type='memory',style={'width': '60%', 'margin-left':'10px'}),
                    html.H6('Precipitação Observada: ', style={ "margin-top": "30px"}),
                    dcc.Dropdown(id = 'stations_dropdown', value=['Salvador (Ondina) - 83229'], multi=True,
                                persistence=True,persistence_type='memory',style={'width': '100%', 'margin-left':'10px'}),        
                            ],width={"size": 3, 'align': 'center'}),
            #Dropdowns climatology Stations and Graph Type
            dbc.Col([
                html.H6('Climatologias(INMET):  ', style={ "margin-top": "10px"}),
                dcc.Dropdown(id = 'clima_dropdown', options = city_climatology, value='(Clima)Salvador - 83229', 
                            persistence=True, persistence_type='memory',style={'width': '80%', 'margin-left':'10px'}),
                html.H6('Tipo de Gráfico: ', style={ "margin-top": "30px"}),
                dcc.RadioItems(id = 'graph_type',options = graph_type, value='Scatter', labelStyle={'display': 'inline-block', 'margin-left':'30px', 'margin-top':'10px'})
                    ], width={"size": 4, 'align': 'center'},)
            ]),
    dbc.Row([
        dbc.Col(html.H6(children= 'Última atualização: ' + date_options2[-2]['value'].replace('_','/'), style={ 'textAlign': 'end'}), 
                        width={"size": 11 ,"offset": 0}),
            ]),
            #Graph1
    dbc.Row([
        dbc.Col(html.H5(id= 'graph1_title', className="text-center", style={ 'textAlign': 'center', 'color': 'white', 'margin-top': '0px'}),
                className="mt-4")
            ]),
    dcc.Graph(id='situation_graph_by_period', style={'margin-left':'70px', 'margin-right':'70px'}),
        #Data Table
    dbc.Row([
        dbc.Col(html.H5('Tabela de Dados(mm)', style={ 'textAlign': 'center', 'color': 'white'}),
                className="mt-5")
            ],justify='center'),
    dbc.Row([
        dbc.Col(html.Div(id='table1'),style={ 'textAlign': 'center'}, width={"size": 11})
            ], justify='center'),
        #anomaly table
    dbc.Row([
        dbc.Col(html.H5('Anomalia de Precipitação(mm)', style={ 'textAlign': 'center', 'color': 'white'}),
                )
            ],justify='center'),
    dbc.Row([
        dbc.Col(html.Div(id='table2'),style={ 'textAlign': 'center'}, width={"size": 11})
            ], justify='center'),
    dbc.Row(html.H1('----------------------------------------------------------------------------', style={ 'textAlign': 'center', "margin-top": "20px"}), justify='center'),
    #Data from every year
    dbc.Row([
        dbc.Col(html.H1(children='Analise de Precipitação Anual no Estado da Bahia', style={ 'textAlign': 'center', 'color': 'white'}, 
            className="mb-1"))
            ]),
    dbc.Row([html.H1(' ')
            ]),
    # Dropdowns stations and years
    dbc.Row([
        dbc.Col([
            html.H5('Escolha a Estação: '),
            dcc.Dropdown(id = 'stations_dropdown_anual',value='Salvador (Ondina) - 83229', 
                        persistence=True, persistence_type='memory', style={'width': '70%', 'margin-left':'30px'}),
            html.H1(' '),
            html.H5('Ano: ' ),
            dcc.Dropdown(id = 'year_dropdown_anual', options = year_options, multi=True, value = [i.rstrip(".csv") for i in list_year][::-1], 
                        persistence=True, persistence_type='memory', style={'width': '70%', 'margin-left':'30px'}),
            html.H1(' '),
                ], width={"size": 5, "offset": 1} ),
    #Dropdown climatology Stations
        dbc.Col([
            html.H1(' '),
            html.H5('Climatologias(INMET):  '),
            dcc.Dropdown(id = 'clima_dropdown_anual', options = city_climatology, value=['(Clima)Salvador - 83229'], multi=True, 
                        persistence=True, persistence_type='memory', style={'width': '70%', 'margin-left':'30px'}),

                ], width={"size": 4, "offset": 1} ),
            ]),
    dbc.Row([
        dbc.Col(html.H5(id= 'graph2_title', className="text-center"),
                className="mt-4")
                ]),
    dcc.Graph(id='situation_graph_by_year', style={'margin-left':'70px', 'margin-right':'70px'}),
    html.H6("Developed by Alisson Santiago - alisson.santiago123@gmail.com", style={ 'textAlign': 'center', "margin-top": "30px"}),
])


#Callbacks and Functions

#Update store memory
@app.callback(
    Output('memory', 'data'),
    Input('year_dropdown', 'value')
)
def update_store(ano):
    df = pd.DataFrame(pd.read_csv(mensal_PATH.joinpath(ano + ".csv")))
    tabdict = dict(df)
    return tabdict

#Update graph title1
@app.callback(
    Output('graph1_title', 'children'),
    Input('year_dropdown', 'value')
)
def update_titles(year):
    graph1_title = 'Gráfico de Precipitação -' + year + '- X Climatologia(INMET)'
    return graph1_title

#Update dropdowns - stations and yearly stations
@app.callback(
    Output('stations_dropdown', 'options'),
    Output('stations_dropdown_anual', 'options'),
    Input('memory', 'data')
)
def update_stations(df6):
    tabela = pd.DataFrame.from_dict(df6)
    city_options = [{'label':i, 'value':i} for i in sorted(tabela["estacao"].unique())]
    return city_options, city_options

#Update Graph1
@app.callback(
    Output('situation_graph_by_period', 'figure'),
    [Input('stations_dropdown', 'value'),
    Input('clima_dropdown', 'value'),
    Input('graph_type', 'value'),
    Input('memory', 'data')])

def update_graph1(stations_value,clima_value,graph_type, df):
    df_graph1 = pd.DataFrame.from_dict(df)
    df_graph1 = df_graph1.set_index('estacao')

    df_clima2 = climatology.set_index('nome_codigo')

    #colors = ['#05a0ff', '#ffbab1','#8cffab', '#f8f85c','#cb7bf9', '#00cbe5','#ff73dc', '#ffa860', '#b88459', '#8e3378']
    #colors2 = ['#080808','#a7a7a7','#bea672', '#91c4c4', '#636771']
    if graph_type == 'Bar':
        trace_1 = []
        t_1 = 0
        for i in stations_value:
            if df_graph1.loc[df_graph1.index.isin([i])].shape[0] == 0:
                continue
            df1 = df_graph1[df_graph1.index == i].iloc[:,5:].T
            trace_1.append(go.Bar(name=i, x=df1.index, y=df1[i], text=i))
            t_1+=1

        j = clima_value
        df2 = df_clima2[df_clima2.index == j].iloc[:,7:-2].T
        trace_1.append(go.Scatter(name=j, x=df2.index, y=df2[j], line={'dash': 'dash'}, line_color = '#080808', text = j))

        data = trace_1
    meses = [ 'Janeiro','Favereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
    if graph_type == 'Scatter':
        trace_1 = []
        t_1 = 0
        for i in stations_value:
            if df_graph1.loc[df_graph1.index.isin([i])].shape[0] == 0:
                continue
            df1 = df_graph1[df_graph1.index == i].iloc[:,5:].T
            trace_1.append(go.Scatter(name=i, x=meses, y=df1[i], text=i))
            t_1+=1

        
        j = clima_value
        df2 = df_clima2[df_clima2.index == j].iloc[:,7:-2].T
        trace_1.append(go.Scatter(name=j, x=meses, y=df2[j], line={'dash': 'dash'}, line_color = '#080808', text = j))
        

        data = trace_1

    layout = go.Layout(
        yaxis={'title': "Precipitação (mm)"},
        barmode='stack',
        height=300,
        paper_bgcolor = 'rgba(255, 255, 255,0.1)',
        plot_bgcolor = 'rgba(255, 255, 255,0)',
        template='simple_white',
        font_color="rgba(224, 224, 224,1)",
        margin=dict(t=20)
    )
    return  {'data': data, 'layout': layout}

#Update table1
@app.callback(
    Output('table1','children'),
    [Input('stations_dropdown', 'value'),
    Input('clima_dropdown', 'value'),
    Input('memory', 'data')]
)
def update_table1(dropdown1,dropdown2,df5):
    df = pd.DataFrame.from_dict(df5)
    tab_total = df.loc[df['estacao'].isin(dropdown1)]

    filtered_table = pd.concat([tab_total.iloc[:,0:2],tab_total.iloc[:,6:]], axis=1)
    filtered_table.rename(columns={'municipio': 'Município', 'estacao': 'Estação'}, inplace=True)


    df_clima_table = climatology
    tab_filt_clima = df_clima_table.loc[df_clima_table['nome_codigo'].isin([dropdown2])]
    
    filtered_clima = pd.concat([tab_filt_clima.loc[:,['municipio','nome_codigo']],tab_filt_clima.iloc[:,8:-2]], axis=1)
    filtered_clima.rename(columns={'municipio': 'Município', 'nome_codigo': 'Estação'}, inplace=True)

    tabela_final = pd.concat([filtered_table,filtered_clima])
    
    table1 = dbc.Table.from_dataframe(tabela_final, striped=True, bordered=True, hover=True, size = 'sm')
    return table1

#Update table2
@app.callback(
    Output('table2','children'),
    [Input('stations_dropdown', 'value'),
    Input('clima_dropdown', 'value'),
    Input('memory', 'data')]
)

def update_table2(stations_obs,station_clima,df7):
    anual = pd.DataFrame.from_dict(df7)

    stations = stations_obs

    anual = anual.loc[anual['estacao'].isin(stations)]

    anomalia = pd.DataFrame()

    for i in anual.iloc[:,6:].columns:
        select1 = anual.set_index('estacao')
        select2 = climatology[climatology['nome_codigo'] == station_clima]
        valor1 = select2[i].apply(lambda x: select1[i] - x)
        anomalia[i] = valor1.iloc[0].round(1)
    anomalia['Estação']=select1.index
    anomalia['Município'] = select1['municipio']
    anomalia = pd.concat([anomalia.iloc[:,[-1,-2]], anomalia.iloc[:,0:-2]], axis=1)

    table2 = dbc.Table.from_dataframe(anomalia, striped=True, bordered=True, hover=True, size = 'sm')

    return table2


#Update store memory2
@app.callback(
    Output('memory_anual', 'data'),
    Input('stations_dropdown_anual', 'value')
)

def update_memory_anual(station_anual):
    
    data = pd.DataFrame()
    list_year_anual = [i.rstrip(".csv") for i in list_year]

    for i in list_year_anual:
        df_test2 = pd.DataFrame(pd.read_csv(mensal_PATH.joinpath( i + ".csv")))
        if df_test2.loc[df_test2['estacao'].isin([station_anual])].shape[0] == 0:
            continue
        test_tab = df_test2.loc[df_test2['estacao'].isin([station_anual])]
        test_tab = test_tab.assign(Ano = i)
        data[i] = test_tab.iloc[0,6:-1]
    data_dict = dict(data)
    return data_dict

#Update stations map
@app.callback(
    Output('estacoes-maps', 'figure'),
    Input('memory', 'data'),
)

def update_map1(df4):

    df_map1 = pd.DataFrame.from_dict(df4)
    df_clima2 = climatology

    df_map1['Tipo'] = 'Observada'
    df_clima2['Tipo'] = 'Climatologia'

    df_filtro1 = df_map1[['estacao','municipio', 'latitude', 'longitude', 'Tipo']]
    df_filtro2 = df_clima2[['nome_codigo','municipio', 'latitude', 'longitude', 'Tipo']]

    df_filtro2.columns = ['estacao','municipio', 'latitude', 'longitude','Tipo']

    df_filtrado = pd.concat([df_filtro1,df_filtro2])

    points = px.scatter_mapbox(df_filtrado, lat="latitude", lon="longitude", color='Tipo', zoom=4.3 , text= 'municipio', 
                                hover_name = 'estacao', width=400, height=300, center=dict(lat=-13.20,lon=-41.75))


    figure_1 = go.Figure(data = points)
    figure_1.update_traces(mode="markers")
    figure_1.update_layout(legend=dict(
    yanchor="top",
    y=1.0,
    xanchor="left",
    x=0.01
))
    #figure_1.update_traces(marker_symbol="circle", marker_colorscale= 'Bluered', marker_size = 9)
    figure_1.update_layout(mapbox_style="open-street-map")
    figure_1.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor='rgba(0,0,0,0)', font_color="black")

    return figure_1

#Update yearly dropdown options
@app.callback(
    Output('year_dropdown_anual', 'options'),
    Input('memory_anual', 'data')
)

def update_dropdownyearsanual(df3):
    data_year3 = pd.DataFrame.from_dict(df3)
    options_year_anual = [{'label': i, 'value': i} for i in data_year3.columns]

    return options_year_anual

#Update graph2 
@app.callback(
    Output('situation_graph_by_year', 'figure'),
    Input('stations_dropdown_anual', 'value'),
    Input('year_dropdown_anual', 'value'),
    Input('clima_dropdown_anual', 'value'),
    Input( 'memory_anual', 'data')
)
def update_graph2(station,years, stations_clima, df):
    df1 = pd.DataFrame.from_dict(df)
    
    df_clima2 = climatology.set_index('nome_codigo')
    
    colors = ['#05a0ff', '#ffbab1','#8cffab', '#f8f85c','#cb7bf9', '#00cbe5','#ff73dc', '#ffa860', '#b88459', '#8e3378']
    colors2 = ['#080808','#a7a7a7','#bea672', '#91c4c4', '#636771'] 

    trace_1 = []

    t_1 = 0
    for i in years:
        if i not in df1.columns:
            continue
        trace_1.append(go.Scatter(name=i, x=month_list, y=df1[i]))
        t_1+=1

    t_2=0
    for j in stations_clima:
        df2 = df_clima2[df_clima2.index == j].iloc[:,7:-1].T
        trace_1.append(go.Scatter(name=j, x=df2.index, y=df2[j], line={'dash': 'dash'}, line_color = colors2[t_2]))
        t_2+=1
    data = trace_1
    
    layout = go.Layout(
        yaxis={'title': "Precipitação (mm)"},
        barmode='stack',
        paper_bgcolor = 'rgba(255, 255, 255,0.1)',
        plot_bgcolor = 'rgba(255, 255, 255,0)',
        template='simple_white',
        font_color="rgba(224, 224, 224,1)",
        margin=dict(t=20)
    )

    return  {'data': data, 'layout': layout}


