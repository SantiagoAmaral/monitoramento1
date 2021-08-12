# Imports
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

#Themes of Dashboard
app.config.external_stylesheets = [dbc.themes.FLATLY]


#Directory where data is
PATH = pathlib.Path(__file__).parent
diario_PATH = PATH.joinpath("../dados/diario").resolve()
tabela_PATH = PATH.joinpath("../dados/diario/2021").resolve()
mensal_PATH = PATH.joinpath("../dados/mensal").resolve()


dir_year = diario_PATH
list_year = sorted(os.listdir(dir_year))
number_files_year = len(list_year)

ano_options = [{'label': i.rstrip(".csv") , 'value': i.rstrip(".csv")} for i in list_year]

month_list = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

dir23 = diario_PATH.joinpath(ano_options[-1]['value'])
list23 = os.listdir(dir23)
number_files23 = len(list23)
month_options = [{'label': i.rstrip(".csv") , 'value': i.rstrip(".csv")} for i in month_list[:number_files23]]

tabela = pd.DataFrame(pd.read_csv(diario_PATH.joinpath(ano_options[-1]['value'] + '/' + month_options[-1]['value'] + '.csv')))
tab1 = tabela.iloc[:,:8]
tab2 = tabela.iloc[:,8:].round(1)

tabela = pd.concat([tab1,tab2], axis=1)

tabela2 = pd.DataFrame(tabela)

municipio_options = [{'label':i, 'value':i} for i in tabela["municipio"].unique()]


region_options = [{'label':i, 'value':i} for i in tabela["regiao"].unique()]
date_options = [{ 'label': i, 'value': i} for i in tabela.columns[8:]]

#px.set_mapbox_access_token(open(".mapbox_token").read())

contagem_estacoes = tabela.groupby('regiao')['nome_estacao'].agg({'count'})
contagem_estacoes = pd.DataFrame(contagem_estacoes).reset_index()
contagem_total = contagem_estacoes['count'].sum()

layout = html.Div([
    dcc.Store(id='memory1', storage_type='local'),
    dcc.Store(id='memory_diario', storage_type= 'local'),
    dbc.Row([ 
            dbc.Col(html.H1(id = 'main_title', style={ 'textAlign': 'center', 'color': 'white'}), align='center')]),
    html.P([
        html.A('SEIA Monitoramento',
        href = 'http://monitoramento.seia.ba.gov.br/',
        target = '_blank')], style={ 'textAlign': 'center'}),
    dbc.Row([
        dbc.Col(dcc.Graph(id='estacoes-graph'), width={"size": 5 ,"offset": 1}, md=4),
        dbc.Col([html.H5(id = 'dia_dados', style={ 'textAlign': 'center'}),
            html.H5('Quantidade de Estações'),
            html.Div(id = 'tabela-contagem'),
            html.H6(id = 'total-estações')
        ], width="auto", style={ 'textAlign': 'center', }),
        dbc.Col(dcc.Graph(id ='density-graph'), width={"size": 5 ,"offset": 0}, md=4)
    ], justify="start"),
    dbc.Row([
        dbc.Col(html.H6(children= 'Última atualização: ' + date_options[-2]['value'].replace('_','/'), style={ 'textAlign': 'center'}), 
                        width={"size": 12 ,"offset": 0}),
            ]),
        html.H5(id = 'graph_title', style={ 'textAlign': 'center', 'color': 'white', "margin-top": "20px"}),
    dbc.Row([
        dbc.Col([
            html.H6('Ano: ' ),
            dcc.Dropdown(id = 'Ano_dropdown', options = ano_options, value = ano_options[-1]['value'],
                        persistence=True, persistence_type='memory', style={'margin-bottom':'20px'}),
            html.H6('Mês: ' ),
            dcc.Dropdown(id = 'month_dropdown', options = month_options, value = month_options[-1]['value'],
                        persistence=True, persistence_type='memory', style={'margin-bottom':'20px'}),
            html.H6('Selecione o dia ou Total'),
            dcc.Dropdown(id = 'date_dropdown', options=date_options, value=date_options[-1]['value'],
                        persistence=True, persistence_type='memory', style={'margin-bottom':'20px'}),
            html.H6('Regiões Climáticas: '),
            dcc.Dropdown(id = 'regiao_dropdown', options = region_options, value= 'Recôncavo',
                        persistence=True, persistence_type='memory', style={'margin-bottom':'20px'})
            ],width={"size": 1.5, "offset": 1}),
        dbc.Col(dcc.Graph(id = 'municipio-graph'), width={"size": 9 }),
    ], justify="start"),
    html.H5(id = 'table_title', style={ 'textAlign': 'center', 'color': 'white', "margin-top": "20px"}),
    #dash_table.DataTable(
        #id='dados-info',
        #columns=[{'name': col, 'id': col} for col in tabela.columns]),
    dbc.Row([
        dbc.Col(html.Div(id ='dados-info1'), width={"size": 4, "offset": 0}),
        dbc.Col(html.Div(id ='dados-info2'), width={"size": 4, "offset": 0}),
        dbc.Col(html.Div(id ='dados-info3'), width={"size": 4, "offset": 0})
        ], justify="center"),
    dbc.Row(html.H5(id = 'graph_title_2', style={ 'textAlign': 'center', 'color': 'white', "margin-top": "30px"}), justify='center'),
    dbc.Row([
        dbc.Col([
            html.H6('Ano: ' ),
            dcc.Dropdown(id = 'Ano_dropdown_diario', options = ano_options, value = ano_options[-1]['value'],
                        persistence=True, persistence_type='memory', style={'width': '100%', 'margin-bottom':'20px'}),
            html.H6('Mês: ' ),
            dcc.Dropdown(id = 'month_dropdown_diario', options = month_options, value = month_options[-1]['value'],
                        persistence=True, persistence_type='memory', style={'width': '100%', 'margin-bottom':'20px'}),
            html.H6('Estação'),
            dcc.Dropdown(id = 'station_dropdown_diario', value="Salvador (Ondina) - 83229",
                        persistence=True, persistence_type='memory', style={'width': '100%', 'margin-bottom':'10px'}),
            ],width={"size": 2, "offset": 1}),
        dbc.Col(dcc.Graph(id = 'municipio-graph_2'), width={"size": 9 }),
        ], justify='center'),
    html.H6("Developed by Alisson Santiago - alisson.santiago123@gmail.com", style={ 'textAlign': 'center'})
])

@app.callback(
    Output('memory1', 'data'),
    Output('month_dropdown', 'options'),
    Input('month_dropdown', 'value'),
    Input('Ano_dropdown', 'value')
)

def update_store(month1, ano):
    df = pd.DataFrame(pd.read_csv(diario_PATH.joinpath(ano + "/" + month1 + ".csv")))
    dir = diario_PATH.joinpath(ano)
    tab1 = df.iloc[:,:8]
    tab2 = df.iloc[:,8:].round(1)

    df = pd.concat([tab1,tab2], axis=1)
    tabdict = dict(df)

    list = os.listdir(dir)
    number_files = len(list)

    month_list = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    month_options = [{'label': i.rstrip(".csv") , 'value': i.rstrip(".csv")} for i in month_list[:number_files]]

    return tabdict, month_options



@app.callback(
    Output( 'main_title', 'children'),
    Output('graph_title', 'children'),
    Output('table_title', 'children'),
    Input('month_dropdown', 'value'),
    Input('date_dropdown', 'value'),
    Input('Ano_dropdown', 'value'),

)

def update_titles(Month,date,ano):
    month_df = pd.DataFrame(month_options)
    main_title = 'Precipitação Diária no Estado da Bahia - ' + month_df[month_df['value']==Month].label + " - " + ano
    graph_title = 'Gráfico de Precipitação por Região Climática - ' + month_df[month_df['value']==Month].label + ' - ' + date.replace('_','/')
    table_title = 'Tabela de Dados de Precipitação(mm) - ' + month_df[month_df['value']==Month].label + ' - ' + date.replace('_','/')

    return main_title, graph_title, table_title

@app.callback(
    Output('regiao_dropdown', 'options'),
    Output('regiao_dropdown', 'value'),
    Output('date_dropdown', 'options'),
    Output('date_dropdown', 'value'),
    Input('memory1', 'data')
)

def update_options(df):
    df_new = pd.DataFrame.from_dict(df)

    region_options = [{'label':i, 'value':i} for i in df_new["regiao"].unique()]
    region_value = 'Recôncavo'
    date_options = [{ 'label': i, 'value': i} for i in df_new.columns[8:]]
    date_value = date_options[-1]['value']
    return region_options, region_value, date_options, date_value

@app.callback(
    Output('tabela-contagem', 'children'),
    Output('total-estações', 'children'),
    Input('date_dropdown', 'value'),
    Input('memory1', 'data')
)

def update_contagem_table(select_date, df):
    tabela = pd.DataFrame.from_dict(df)
    contagem_estacoes = tabela.groupby('regiao')[select_date].agg({'count'})
    contagem_estacoes = pd.DataFrame(contagem_estacoes).reset_index()
    contagem_total = contagem_estacoes['count'].sum()
    contagem_estacoes.rename(columns={'regiao': 'Região', 'count': 'Total'}, inplace=True)

    table1 = dbc.Table.from_dataframe(contagem_estacoes, striped=True, bordered=True, hover=True, size = 'sm')

    return table1, f'Total de estações: {str(contagem_total)}'


@app.callback(
    Output('municipio-graph', 'figure'),
    Output('dia_dados', 'children'),
    Input('regiao_dropdown', 'value'),
    Input('date_dropdown', 'value'),
    Input('memory1', 'data')
)

def update_graph (selected_regiao, selected_date, df):
    tabela = pd.DataFrame.from_dict(df)
    filtered_erro = tabela[tabela['regiao']==selected_regiao]
    filtered_erro = filtered_erro[selected_date].sum()

    if filtered_erro == 0:
        filtered_tabela_erro = tabela[tabela['regiao']==selected_regiao]
        bar_fig_erro = px.bar(x = list(filtered_tabela_erro["municipio"] + " - " + filtered_tabela_erro["codigo"]), y = list(filtered_tabela_erro[selected_date]))
        return bar_fig_erro, f'Precipitação {selected_date.replace("_","/")}'
    else:
        filtered_tabela = tabela[tabela['regiao']==selected_regiao]
        filtered_tabela = filtered_tabela[filtered_tabela[selected_date] > 0]
        filtered_tabela = filtered_tabela.sort_values(selected_date, ascending=False)
        bar_fig = px.bar(x = (filtered_tabela["municipio"] + " - " + filtered_tabela["codigo"]), y = filtered_tabela[selected_date], hover_name=filtered_tabela['nome_estacao'], text=list(filtered_tabela[selected_date]),
                    opacity=0.7, template= 'simple_white')
        bar_fig.layout.xaxis.title = 'Estações'
        bar_fig.layout.yaxis.title = 'Total de Precipitação(mm)'
        bar_fig.update_layout(
    margin=dict(l=50, r=50, t=30, b=30),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor='rgba(0,0,0,0)', font_color="gray",
)
        return bar_fig, f'Precipitação {selected_date.replace("_","/")}'

@app.callback(
    Output('dados-info1', 'children'),
    Output('dados-info2', 'children'),
    Output('dados-info3', 'children'),
    Input('regiao_dropdown', 'value'),
    Input('date_dropdown', 'value'),
    Input('memory1', 'data')
)

def update_table (selected_regiao, selected_date, df):
    tabela = pd.DataFrame.from_dict(df)

    tab1 = tabela.iloc[:,:8]
    tab2 = tabela.iloc[:,8:].round(1)

    tabela = pd.concat([tab1,tab2], axis=1)

    filtered_tabela = tabela[tabela['regiao']==selected_regiao]

    filtered_tabela = filtered_tabela[filtered_tabela[selected_date] > 0]

    filtered_tabela[selected_date] = filtered_tabela[selected_date]
    filtered_tabela = filtered_tabela[['estacao',selected_date]]
    filtered_tabela = filtered_tabela.sort_values(selected_date, ascending=False)
    filtered_tabela[selected_date] = filtered_tabela[selected_date]

    filtered_tabela.rename(columns= {'estacao': 'Nome da Estação', selected_date: selected_date.replace('_','/')}, inplace=True)


    total_col = int(filtered_tabela['Nome da Estação'].count())
    cont = int(total_col/3)
    parte1 = filtered_tabela.iloc[:cont+1]
    parte2 = filtered_tabela.iloc[cont+1:(total_col - cont)]
    parte3 = filtered_tabela.iloc[(total_col - cont):]

    table1 = dbc.Table.from_dataframe(parte1, striped=True, bordered=True, hover=True, size = 'sm')
    table2 = dbc.Table.from_dataframe(parte2, striped=True, bordered=True, hover=True, size = 'sm')
    table3 = dbc.Table.from_dataframe(parte3, striped=True, bordered=True, hover=True, size = 'sm')

    return table1, table2, table3

@app.callback(
    Output('estacoes-graph', 'figure'),
    Output('density-graph', 'figure'),
    Input('date_dropdown', 'value'),
    Input('memory1', 'data')
)

def update_maps(date,df):
    tabela = pd.DataFrame.from_dict(df)
    table_map = tabela
    sequential1 = ['#e0fefc', '#befefe','#73f1fd', '#11d4ff','#21b5fb', '#3698fd', '#4975f9', '#5c56f4', '#4e37e7', '#4217d6', '#390cc7', '#3300b8']

    colors_m2 = ['#05a0ff', '#ffbab1','#8cffab', '#f8f85c','#cb7bf9', '#00cbe5','#ff73dc', '#ffa860']
    density = px.density_mapbox(table_map, lat="latitude", lon="longitude", z = date, radius=20 , zoom=4.5, height=400,
                                color_continuous_scale= sequential1, range_color=[0,150], opacity=0.8, center=dict(lat=-12.91,lon=-41.68))

    points = px.scatter_mapbox(table_map, lat="latitude", lon="longitude", zoom=4.5 ,color= 'regiao', text= 'municipio', hover_name='codigo',
                                hover_data=["municipio", "nome_estacao"], height=400, color_discrete_sequence=px.colors.qualitative.Antique,
                                center=dict(lat=-13.21,lon=-40.10))

    figure_1 = go.Figure(data = points)
    figure_1.update_layout()
    figure_1.update_traces(marker_symbol="circle", marker_size = 9, mode="markers")
    figure_1.update_layout(mapbox_style="open-street-map", legend=dict(yanchor="bottom",
                                                                        y=0.01,
                                                                        xanchor="right",
                                                                        x=1.0), )
    figure_1.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor='rgba(0,0,0,0)', font_color="gray")

    figure_2 = go.Figure(data=density)
    figure_2.update_layout(mapbox_style="open-street-map")
    figure_2.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor='rgba(0,0,0,0)',font_color="gray")

    return figure_1, figure_2

@app.callback(
    Output('memory_diario', 'data'),
    Output('month_dropdown_diario', 'options'),
    Output('station_dropdown_diario', 'options'),
    Input('month_dropdown_diario', 'value'),
    Input('Ano_dropdown_diario', 'value')
)

def update_store2(month_diario, ano_diario):
    df = pd.DataFrame(pd.read_csv(diario_PATH.joinpath(ano_diario + "/" + month_diario + ".csv")))
    dir = diario_PATH.joinpath(ano_diario)
    tab1 = df.iloc[:,:8]
    tab2 = df.iloc[:,8:].round(1)

    df = pd.concat([tab1,tab2], axis=1)
    tabdict2 = dict(df)

    list = os.listdir(dir)
    number_files = len(list)

    month_list = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    month_options2 = [{'label': i.rstrip(".csv") , 'value': i.rstrip(".csv")} for i in month_list[:number_files]]

    stations_diario = [{'label': i , 'value': i} for i in df['estacao']]
    return tabdict2, month_options2, stations_diario

@app.callback(
    Output('municipio-graph_2', 'figure'),
    Output('graph_title_2', 'children'),
    Input('memory_diario', 'data'),
    Input('station_dropdown_diario', 'value'),
    Input('month_dropdown_diario', 'value'),
    Input('Ano_dropdown_diario', 'value')
)

def update_graph_diario(memory_df, station_value, month_name,year_name):
    i = station_value
    graph_title_2 = 'Gráfico de Precipitação por Estação - ' + month_name +'/' + year_name + ' - ' +  station_value
    df_diario = pd.DataFrame.from_dict(memory_df)

    df_diario1 = df_diario.set_index('estacao')
    df_diario2 = df_diario1[df_diario1.index == i].iloc[:,7:-1].T


    fig_Bar_2 = px.bar(x=df_diario2.index, y=df_diario2[i], opacity=0.7,
                        text=list(df_diario2[i]), template='simple_white')
    fig_Bar_2.update_layout(
        yaxis={'title': "Precipitação (mm)"},
        paper_bgcolor = "rgba(0,0,0,0)",
        plot_bgcolor = 'rgba(0,0,0,0)',
        font_color="gray",
        margin=dict(l=50, r=50, t=30, b=30)
    )


    return fig_Bar_2, graph_title_2