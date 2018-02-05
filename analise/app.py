import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from datetime import datetime

app = dash.Dash(__name__)

server = app.server

df = pd.read_csv('https://docs.google.com/spreadsheets/d/' +
                 '1PKcStpSL_JBKOsUbwWbo5LF8i6MRvEReATAYJj0esqI' +
                 '/export?gid=401459338&format=csv')

df.Produto_Final_Data = df.Produto_Final_Data.apply(lambda x: str(x).split(';')[0])


agency_options = [{'label': agency, 'value': agency}
                  for agency in set(df['Agência'])]

type_year_options = [{'label': 'Por ano', 'value': 'Por ano'},
                     {'label': 'Por mandato presidencial', 'value': 'Por mandato presidencial'},
                     {'label': 'Por mandato diretor-presidente da agência', 'value': 'Por mandato diretor-presidente da agência'}]

type_part_options = [{'label': 'Todos', 'value': 'Todos'},
                     {'label': 'Presencial', 'value': 'PP'},
                     {'label': 'Não presencial', 'value': 'PNP'},
                     {'label': 'Presencial e não presencial', 'value': 'PP e PNP'}]

colors_palette = ['#5977e3', '#7b9ff9', '#9ebeff', '#c0d4f5', '#dddcdc', '#f2cbb7', '#f7ac8e', '#ee8468', '#d65244']

objective_options = []
subject_options = []

aux_instru_part = {'PP': 'Presencial', 'PNP': 'Não presencial', 'PP e PNP': 'Presencial e não presencial'}

colors = {'text_H1': '#292735',
          'text_n': '#565656'}

app.layout = html.Div(children=[
html.Div([
    html.Div(
        [
            html.H2(
                'Regulação em números',
                style = {'text-align': 'center',
                         'color': colors['text_H1'],
                         },
            ),
            html.H6('Mecanismo de participação', style = {'text-align': 'center', 'color': colors['text_n']}),
        ],
        className='row'
    ),
    html.Hr(style={'margin': '20', 'margin-bottom': '5'}),

    html.Div([
        html.Div([
            html.Div([

                html.P('Escolha uma agência reguladora:'),

                dcc.Dropdown(
                    id='agency_options',
                    options=agency_options,
                    value='ANA',
                        ),],
                className='three columns offset-by-one', style ={'float': 'left', 'color': colors['text_H1']},
                ),

            html.Div([
                html.P('Escolha um instrumento de participação:'),

                dcc.Dropdown(
                    id='type_part_options',
                    options=type_part_options,
                    value='Todos',
                ),],
                className='three columns offset-by-one', style ={'float': 'left', 'color': colors['text_H1']},
                ),

            html.Div([
                html.P('Escolha o período temporal:'),

                dcc.Dropdown(
                    id='type_year_options',
                    options=type_year_options,
                    value='Por ano',
                ),],
            className='three columns offset-by-one', style ={'float': 'left', 'color': colors['text_H1']},
            ),
        ],
        className='ten columns offset-by-one', style={'margin-top': '20'},
        ),
    ]),

    html.Div([
          html.H6('',
                   id='num_mecanism',
                   style={'text-align': 'center', 'color': colors['text_H1'], 'margin-top': '60'},
                   ),
    ], className = 'six columns offset-by-three'),

    html.Div([
        html.P('Percentual do número de audiências por ano em relação ao total de todos os anos.', style={'text-align': 'center'}),

        dcc.Graph(id='contribution_time'),
            ], className = 'ten columns offset-by-one', style = {'margin-top': '35'},
        ),

    html.Div([
        html.P('Percentual de audiências por ano e objetivo da participação.',
               style={'text-align': 'center'}),

        dcc.Graph(id='object_time'),
        ],className = 'ten columns offset-by-one', style={'margin-top': '35'}
    ),

    html.Div([
        html.P('Percentual de audiências por ano e tema da audiência.',
               style={'text-align': 'center'}),

        dcc.Graph(id='subject_time'),
        ], className = 'ten columns offset-by-one', style={'margin-top': '35'}
    ),

    html.Div([

    html.Hr(style={'margin': '0', 'margin-bottom': '0'}),

    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Média do tempo da preparação para a audiência, em dias.',
               style={'text-align': 'center'}),

        dcc.Graph(id='mean_time_preparation')
            ],
                className = 'ten columns offset-by-one', style={'margin-top': '35'}),
    html.Div([
        html.P('Média do tempo da preparação para a audiência por objetivo da participação, em dias.',
               style={'text-align': 'center'}),

        dcc.Graph(id='mean_time_preparation_table_obj')
    ],
        className='ten columns offset-by-one', style={'margin-top': '35'}),
    html.Div([
        html.P('Média do tempo da preparação para a audiência por tema da audiência, em dias.',
               style={'text-align': 'center'}),

        dcc.Graph(id='mean_time_preparation_table_subject')
    ],
        className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Média do tempo de preparação por grupo de número de contribuinte.',
               style={'text-align': 'center'}),

        dcc.Graph(id='mean_time_contribution')
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.Hr(style={'margin': '0', 'margin-bottom': '0'}),

    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Média do tempo da disponibilização do relatório após a última data de contribuição, em dias.',
               style={'text-align': 'center'}),

        dcc.Graph(id='mean_time_answer')
        ],
            className = 'ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Média do tempo da disponibilização do relatório após a última data de contribuição por objetivo, em dias.',
               style={'text-align': 'center'}),

        dcc.Graph(id='mean_time_answer_table_obj')
    ],
        className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Média do tempo da disponibilização do relatório após a última data de contribuição por tema, em dias.',
            style={'text-align': 'center'}),

        dcc.Graph(id='mean_time_answer_table_subject')
    ],
        className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.Hr(style={'margin': '0', 'margin-bottom': '0'}),

    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Média do tempo da disponibilização do relatório após a convocação, em dias.',
               style={'text-align': 'center'}),

        dcc.Graph(id='mean_time_type1')
        ],
            className = 'ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        dcc.Graph(id='mean_time_type1_table_obj')
    ],
        className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        dcc.Graph(id='mean_time_type1_table_subject')
    ],
        className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.Hr(style={'margin': '0', 'margin-bottom': '0'}),

    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
            dcc.Graph(id='mean_time_type2')
        ],
            className = 'ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        dcc.Graph(id='mean_time_type2_table_obj')
    ],
        className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        dcc.Graph(id='mean_time_type2_table_subject')
    ],
        className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.Hr(style={'margin': '0', 'margin-bottom': '0'}),

    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
            dcc.Graph(id = 'mean_contribution')
        ], className = 'ten columns offset-by-one', style={'margin-top': '35'}),
    html.Div([
        dcc.Graph(id = 'table_obj')
    ], className = 'ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        dcc.Graph(id='table_subject')
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.Hr(style={'margin': '0', 'margin-bottom': '0'}),

    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

], className='ten columns offset-by-one', style = {'background-color': '#bbbbbb'}),
], className='twelve columns', style = {'background-color': '#eeeeee'})

def filter_dataframe(df, agency, int_part):
    if int_part == 'Todos':
        dff = df[df['Agência'] == agency]
        return dff
    else:
        dff = df[df['Agência'] == agency]
        dff = dff[dff['Instrumento_de_Participacao'] == int_part]
        return dff

def filter_dataframe_objective_subject(df, agency, int_part, objective, subject):
    dff = filter_dataframe(df, agency, int_part)
    if objective == "Todos" and subject == "Todos":
        return dff

    elif objective != "Todos" and subject == "Todos":
        return dff[dff["Objetivo_participacao"] == objective]

    elif objective == "Todos" and subject != "Todos":
        return dff[dff["Indexacao_Tema"] == subject]

    else:
        dff = dff[dff["Objetivo_participacao"] == objective]
        dff = dff[dff["Indexacao_Tema"] == subject]
        return dff

@app.callback(Output('num_mecanism', 'children'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value')])

def update_num_mecanism(agency_value, int_part_value):

    dff = filter_dataframe(df, agency_value, int_part_value)

    if dff.shape[0] > 0:
        if int_part_value == 'Todos':

            return "Para a agência {}, temos registro dos mecanismos de participação começando no ano {} " \
                   "e terminando em {}, totalizando {} registros, com {} ainda em andamento.".format(agency_value,
                                                                                                    np.min(dff.Ano),
                                                                                                    np.max(dff.Ano),
                                                                                                    dff.shape[0],
                                                                                                    dff[dff.Situacao == "Em andamento"].shape[0])

        else:
            return "Com essa combinação de filtros, para a agência {}, temos registro dos mecanismos de participação começando no ano {} " \
                   "e terminando em {}, totalizando {} registros, que foram feitos de forma {}, com {} ainda em andamento.".format(agency_value,
                                                                                                                                  np.min(dff.Ano),
                                                                                                                                  np.max(dff.Ano),
                                                                                                                                  dff.shape[0],
                                                                                                                                  aux_instru_part[int_part_value].lower(),
                                                                                                                                  dff[dff.Situacao == "Em andamento"].shape[0])
    else:
        return "Não temos registros, sobre a {}, com essas combinações de filtros".format(agency_value)

'''

@app.callback(Output('objective_options', 'options'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value')])
def update_slider(agency_value, int_part_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    aux = [{'label': i, 'value': i} for i in set(dff['Objetivo_participacao'])]
    aux.insert(0, {'label': 'Todos', 'value': 'Todos'})
    return aux

@app.callback(Output('subject_options', 'options'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value')])
def update_slider(agency_value, int_part_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    aux = [{'label': i, 'value': i} for i in set(dff['Indexacao_Tema'])]
    aux.insert(0, {'label': 'Todos', 'value': 'Todos'})
    return aux

'''

def colors_palettes_function(df, agency_options, columns):

    df = df[df['Agência']==agency_options]

    aux = list(df[columns].drop_duplicates().sort_values())

    c = 0
    aux_colors = {}
    for i in aux:
        aux_colors.update({i: colors_palette[c]})
        c += 1

    return aux_colors

@app.callback(Output('contribution_time', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value')])
def make_contribution_time_figure(agency_value, int_part_value, year_options_value):

    dff = filter_dataframe(df, agency_value, int_part_value)

    a = [str(i) + '%' for i in np.round((dff.groupby('Ano').count()['Agência'].values/dff.shape[0])*100,1)]

    traces = []
    trace = dict(
        type='bar',
        x = [str(i) for i in dff.groupby('Ano').count()['Agência'].index],
        y = (dff.groupby('Ano').count()['Agência'].values/dff.shape[0])*100,
        text=a,
        textposition = 'auto',
        marker = dict(
            color = '#5498A5'
        ),

    )

    traces.append(trace)

    layout = dict(
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=120
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        zoom=7,
        titlefont = dict(
          size = 21,
            color = 'rgb(0,0,0)',
        ),
        font = dict(
            color = 'rgb(0,0,0)'
        ),
        yaxis = dict (
            showgrid = False,
            showticklabels = False,
        )
       )

    figure = dict(data=traces, layout = layout)
    return figure

@app.callback(Output('object_time', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),])
def make_object_time_figure(agency_value, int_part_value, year_options_value):
    dfff = filter_dataframe(df, agency_value, int_part_value)

    aux_ano = list(dfff.Ano.drop_duplicates().sort_values())
    aux_ano = ['Ano '+str(i) for i in aux_ano]
    aux_ano.append('Geral')

    aux_objetivo = list(dfff.Objetivo_participacao.drop_duplicates().sort_values())

    traces = []

    aux_colors = colors_palettes_function(df,agency_value,'Objetivo_participacao')

    for j in aux_objetivo:

        y = []

        for i in aux_ano:

            if i == 'Geral':
                aux = (dfff.Objetivo_participacao[dfff.Objetivo_participacao == j].count() / dfff.Objetivo_participacao.count()) * 100
                y.append(aux)

            else:
                aux = (dfff.Objetivo_participacao[dfff.Objetivo_participacao == j][dfff.Ano == int(i.split()[1])].count() / dfff.Objetivo_participacao[dfff.Ano == int(i.split()[1])].count()) * 100
                y.append(aux)

        a = [str(i) + '%' for i in np.round(y, 1)]

        trace = dict(
            type='bar',
            x=aux_ano,
            y=y,
            text=a,
            textposition = 'auto',
            name=j,
            marker = dict(
            color=aux_colors[j]
                )
        )

        traces.append(trace)

    layout = dict(
        barmode='stack',
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=45
        ),
        hovermode="closest",
        zoom=7,
        titlefont = dict(
          size = 21,
            color = 'rgb(0,0,0)',
        ),
        font = dict(
            color = 'rgb(0,0,0)'
        ),
        showlegend=True,
        legend=dict(
            orientation='h',
            x=0.5,
            xanchor='center'

        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
        )

    )

    figure = dict(data=traces, layout=layout)
    return figure

@app.callback(Output('subject_time', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),])
def make_subject_time_figure(agency_value, int_part_value, year_options_value):
    dfff = filter_dataframe(df, agency_value, int_part_value)

    aux_ano = list(dfff.Ano.drop_duplicates().sort_values())
    aux_ano = ['Ano '+str(i) for i in aux_ano]
    aux_ano.append('Geral')

    aux_tema = list(dfff.Indexacao_Tema.drop_duplicates().sort_values())

    aux_colors = colors_palettes_function(df, agency_value, 'Indexacao_Tema')

    traces = []

    for j in aux_tema:

        y = []

        for i in aux_ano:

            if i == 'Geral':
                aux = (dfff.Indexacao_Tema[dfff.Indexacao_Tema == j].count() / dfff.Indexacao_Tema.count()) * 100
                y.append(aux)

            else:
                aux = (dfff.Indexacao_Tema[dfff.Indexacao_Tema == j][dfff.Ano == int(i.split()[1])].count() / dfff.Indexacao_Tema[dfff.Ano == int(i.split()[1])].count()) * 100
                y.append(aux)

        a = [str(i)+'%' for i in np.round(y, 1)]

        trace = dict(
            type='bar',
            x=aux_ano,
            y=y,
            name=j,
            text = a,
            textposition = 'auto',
            marker = dict(
            color=aux_colors[j]
                )
        )

        traces.append(trace)

    layout = dict(
        barmode='stack',
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=45
        ),
        hovermode="closest",
        zoom=7,
        titlefont = dict(
          size = 21,
            color = 'rgb(0,0,0)',
        ),
        font = dict(
            color = 'rgb(0,0,0)'
        ),
        showlegend=True,
        legend=dict(
            orientation='h',
            x=0.5,
            xanchor='center'
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
        )

    )

    figure = dict(data=traces, layout=layout)
    return figure

def data_calculo(df, var1, var2):

    time_day = []

    for i in df.index:

        if df.loc[i,var1]  != 'N/D' and df.loc[i,var1]  != 'N/D' and type(df.loc[i,var1]) == str:
            if df.loc[i,var2]  != 'N/D' and df.loc[i,var2]  != 'N/D' and type(df.loc[i,var2]) == str:
                if len(df.loc[i, var1].split('/')[0]) == 4:
                    aux_var1 = datetime.strptime(df.loc[i, var1], '%Y/%m/%d')
                else:
                    aux_var1 = datetime.strptime(df.loc[i, var1], '%d/%m/%Y')
                if len(df.loc[i, var2].split('/')[0]) == 4:
                    aux_var2 = datetime.strptime(df.loc[i, var2], '%Y/%m/%d')
                else:
                    aux_var2 = datetime.strptime(df.loc[i, var2], '%d/%m/%Y')

                aux = aux_var2 - aux_var1
                aux = aux.days
                time_day.append(aux)
            else:
                time_day.append(df.loc[i,var2])
        else:
            time_day.append(df.loc[i,var1])

    return time_day

@app.callback(Output('mean_time_preparation', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              ])
def make_object_time_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Contribuicao_data_final')

    y = []
    x = []
    y2 = []
    x2 = []
    for i in dff.Ano.drop_duplicates().sort_values():
        y.append(np.mean([i for i in dff[dff.Ano == i].time_days if type(i) != str]))
        x.append(str(i))

        y2.append(np.mean([i for i in dff.time_days if type(i) != str]))
        x2.append(str(i))

    traces = []
    trace = dict(
        type='Scatter',
        x = x,
        y = y,
        name = 'Média por ano'
        )

    trace2 = dict(
        x=x2,
        y=y2,
        mode='lines',
        type='Scatter',
        name='Média geral',
    )

    traces.append(trace)
    traces.append(trace2)

    layout = dict(
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=120
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        zoom=7,
        xaxis = dict(showgrid = False),
        yaxis = dict(showgrid=False)
    )
    figure = dict(data=traces, layout = layout)
    return figure

@app.callback(Output('mean_time_answer', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
             ])
def make_object_time_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = dff[dff.Situacao == 'Encerrada']

    dff['time_days'] = data_calculo(dff, 'Contribuicao_data_final', 'Relatorio_data')

    y = []
    x = []
    y2 = []
    x2 = []
    for i in dff.Ano.drop_duplicates().sort_values():
        y.append(np.mean([i for i in dff[dff.Ano == i].time_days if type(i) != str]))
        x.append(str(i))

        y2.append(np.mean([i for i in dff.time_days if type(i) != str ]))
        x2.append(str(i))

    traces = []
    trace = dict(
        type='Scatter',
        x = x,
        y = y,
        name = 'Média por ano'
        )

    trace2 = dict(
        x=x2,
        y=y2,
        mode='lines',
        type='Scatter',
        name='Média geral',
    )

    traces.append(trace)
    traces.append(trace2)

    layout = dict(
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=120
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        zoom=7,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)

    )
    figure = dict(data=traces, layout = layout)
    return figure

@app.callback(Output('mean_time_type1', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              ])
def make_object_time_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = dff[dff.Situacao == 'Encerrada']

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Relatorio_data')

    y = []
    x = []
    y2 = []
    x2 = []
    for i in dff.Ano.drop_duplicates().sort_values():
        y.append(np.mean([i for i in dff[dff.Ano == i].time_days if type(i) != str]))
        x.append(str(i))

        y2.append(np.mean([i for i in dff.time_days if type(i) != str ]))
        x2.append(str(i))

    traces = []
    trace = dict(
        type='Scatter',
        x = x,
        y = y,
        name = 'Média por ano'
        )

    trace2 = dict(
        x=x2,
        y=y2,
        mode='lines',
        type='Scatter',
        name='Média geral',
    )

    traces.append(trace)
    traces.append(trace2)

    layout = dict(
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=120
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        title="Média do tempo da disponibilização do relatório após a convocação, em dias.",
        zoom=7,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)

    )
    figure = dict(data=traces, layout = layout)
    return figure

@app.callback(Output('mean_time_type2', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              ])
def make_object_time_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = dff[dff.Situacao == 'Encerrada']

    dff.Produto_Final_Data[dff.Produto_Final_Data == '2016'] = 'N/C'

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i,'Produto_Final_Data'])]

    dff = dff.loc[aux,:]

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i, 'Convocacao_Data'])]

    dff = dff.loc[aux, :]

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Produto_Final_Data')

    y = []
    x = []
    y2 = []
    x2 = []
    for i in dff.Ano.drop_duplicates().sort_values():
        y.append(np.mean([i for i in dff[dff.Ano == i].time_days if type(i) != str]))
        x.append(str(i))

        y2.append(np.mean([i for i in dff.time_days if type(i) != str ]))
        x2.append(str(i))

    traces = []
    trace = dict(
        type='Scatter',
        x = x,
        y = y,
        name = 'Média por ano'
        )

    trace2 = dict(
        x=x2,
        y=y2,
        mode='lines',
        type='Scatter',
        name='Média geral',
    )

    traces.append(trace)
    traces.append(trace2)

    layout = dict(
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=120
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        title="Média do tempo da disponibilização do produto final após a convocação, em dias.",
        zoom=7,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)

    )
    figure = dict(data=traces, layout = layout)
    return figure


@app.callback(Output('mean_contribution', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              ])
def make_object_time_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = dff[dff.Situacao == 'Encerrada']

    y = []
    x = []
    y2 = []
    x2 = []
    for i in dff.Ano.drop_duplicates().sort_values():
        y.append(np.mean([float(j) for j in dff.Quantos_participaram[dff.Ano == i] if 'N' not in str(j).upper()]))
        x.append(str(i))

        y2.append(np.mean([float(j) for j in dff.Quantos_participaram if 'N' not in str(j).upper()]))
        x2.append(str(i))

    traces = []
    trace = dict(
        type='Scatter',
        x = x,
        y = y,
        name = 'Média por ano'
        )

    trace2 = dict(
        x=x2,
        y=y2,
        mode='lines',
        type='Scatter',
        name='Média geral',
    )

    traces.append(trace)
    traces.append(trace2)

    layout = dict(
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=120
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        title="Média do número de contribuintes que participaram de audiências",
        zoom=7,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)

    )
    figure = dict(data=traces, layout = layout)
    return figure

@app.callback(Output('table_obj', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              ])
def make_object_table_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = dff[dff.Situacao == 'Encerrada']

    aux = [i for i in dff.index if 'N' not in dff.loc[i,'Quantos_participaram']]
    dff = dff.loc[aux,:]
    dff.Quantos_participaram = dff.Quantos_participaram.apply(lambda x: float(x))

    table = dff.pivot_table(values='Quantos_participaram', index=['Ano'], columns=['Objetivo_participacao'], aggfunc=agg_table_mean, fill_value = '', dropna = False)

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    table = table[names_table]

    names_table = ['<b>'+i+'</b>' for i in names_table]

    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    aux_color = []

    for i in table.Ano:
        if i%2 != 0:
            aux_color.append(rowOddColor)
        else:
            aux_color.append(rowEvenColor)

    traces = []

    trace = dict(
        type = 'table',
        header = dict(
            values = names_table,
            line = dict(color = '#506784'),
            fill = dict(color = 'grey'),
            align = 'center',
            font = dict(color = 'white', size = 10)
        ),
        cells = dict(
           values = table.values.T,
            fill = dict(
                color=[aux_color]
                ),
            )
        )

    traces.append(trace)

    layout = dict(
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=120
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        title="Média do número de contribuintes que participaram de audiências por objetivo",
        zoom=7,
    )

    figure = dict(data=traces, layout = layout)
    return figure

def agg_table_mean(x):
    x = np.nanmean(x)
    x = np.round(x, 1)
    return x

@app.callback(Output('table_subject', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              ])
def make_subject_table_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = dff[dff.Situacao == 'Encerrada']

    aux = [i for i in dff.index if 'N' not in dff.loc[i,'Quantos_participaram']]
    dff = dff.loc[aux,:]
    dff.Quantos_participaram = dff.Quantos_participaram.apply(lambda x: float(x))

    table = dff.pivot_table(values='Quantos_participaram', index=['Ano'], columns=['Indexacao_Tema'], aggfunc=agg_table_mean, fill_value = '', dropna = False)

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    table = table[names_table]

    names_table = ['<b>'+i+'</b>' for i in names_table]


    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    aux_color = []

    for i in table.Ano:
        if i%2 != 0:
            aux_color.append(rowOddColor)
        else:
            aux_color.append(rowEvenColor)


    traces = []

    trace = dict(
        type = 'table',
        header = dict(
            values = names_table,
            line = dict(color = '#506784'),
            fill = dict(color = 'grey'),
            align = 'center',
            font = dict(color = 'white', size = 10)
        ),
        cells = dict(
           values = table.values.T,
            fill = dict(
                color=[aux_color]
                ),
            )
        )
    traces.append(trace)

    layout = dict(
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=120
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        title="Média do número de contribuintes que participaram de audiências por tema",
        zoom=7,
    )

    figure = dict(data=traces, layout = layout)
    return figure

@app.callback(Output('mean_time_preparation_table_obj', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              ])
def make_object_table_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Contribuicao_data_final')

    table = dff.pivot_table(values='time_days', index=['Ano'], columns=['Objetivo_participacao'], aggfunc=agg_table_mean, fill_value = '', dropna = False)

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    table = table[names_table]

    names_table = ['<b>'+i+'</b>' for i in names_table]

    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    aux_color = []

    for i in table.Ano:
        if i%2 != 0:
            aux_color.append(rowOddColor)
        else:
            aux_color.append(rowEvenColor)

    traces = []

    trace = dict(
        type = 'table',
        header = dict(
            values = names_table,
            line = dict(color = '#506784'),
            fill = dict(color = 'grey'),
            align = 'center',
            font = dict(color = 'white', size = 10)
        ),
        cells = dict(
           values = table.values.T,
            fill = dict(
                color=[aux_color]
                ),
            )
        )

    traces.append(trace)

    layout = dict(
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=120
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        zoom=7,
    )

    figure = dict(data=traces, layout = layout)
    return figure


@app.callback(Output('mean_time_preparation_table_subject', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              ])
def make_subject_table_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Contribuicao_data_final')

    table = dff.pivot_table(values='time_days', index=['Ano'], columns=['Indexacao_Tema'], aggfunc=agg_table_mean, fill_value = '', dropna = False)

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    table = table[names_table]

    names_table = ['<b>'+i+'</b>' for i in names_table]

    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    aux_color = []

    for i in table.Ano:
        if i%2 != 0:
            aux_color.append(rowOddColor)
        else:
            aux_color.append(rowEvenColor)


    traces = []

    trace = dict(
        type = 'table',
        header = dict(
            values = names_table,
            line = dict(color = '#506784'),
            fill = dict(color = 'grey'),
            align = 'center',
            font = dict(color = 'white', size = 10)
        ),
        cells = dict(
           values = table.values.T,
            fill = dict(
                color=[aux_color]
                ),
            )
        )
    traces.append(trace)

    layout = dict(
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=120
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        zoom=7,
    )

    figure = dict(data=traces, layout = layout)
    return figure

@app.callback(Output('mean_time_answer_table_obj', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              ])
def make_object_table_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = dff[dff.Situacao == 'Encerrada']

    dff['time_days'] = data_calculo(dff, 'Contribuicao_data_final', 'Relatorio_data')

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i, 'time_days'])]
    dff = dff.loc[aux, :]
    dff.time_days = dff.time_days.apply(lambda x: float(x))

    table = dff.pivot_table(values='time_days', index=['Ano'], columns=['Objetivo_participacao'], aggfunc=agg_table_mean, fill_value = '', dropna = False)

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    table = table[names_table]

    names_table = ['<b>'+i+'</b>' for i in names_table]

    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    aux_color = []

    for i in table.Ano:
        if i%2 != 0:
            aux_color.append(rowOddColor)
        else:
            aux_color.append(rowEvenColor)

    traces = []

    trace = dict(
        type = 'table',
        header = dict(
            values = names_table,
            line = dict(color = '#506784'),
            fill = dict(color = 'grey'),
            align = 'center',
            font = dict(color = 'white', size = 10)
        ),
        cells = dict(
           values = table.values.T,
            fill = dict(
                color=[aux_color]
                ),
            )
        )

    traces.append(trace)

    layout = dict(
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=120
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        zoom=7,
    )

    figure = dict(data=traces, layout = layout)
    return figure


@app.callback(Output('mean_time_answer_table_subject', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              ])
def make_subject_table_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = dff[dff.Situacao == 'Encerrada']

    dff['time_days'] = data_calculo(dff, 'Contribuicao_data_final', 'Relatorio_data')

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i, 'time_days'])]
    dff = dff.loc[aux, :]
    dff.time_days = dff.time_days.apply(lambda x: float(x))

    table = dff.pivot_table(values='time_days', index=['Ano'], columns=['Indexacao_Tema'], aggfunc=agg_table_mean, fill_value = '', dropna = False)

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    table = table[names_table]

    names_table = ['<b>'+i+'</b>' for i in names_table]

    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    aux_color = []

    for i in table.Ano:
        if i%2 != 0:
            aux_color.append(rowOddColor)
        else:
            aux_color.append(rowEvenColor)


    traces = []

    trace = dict(
        type = 'table',
        header = dict(
            values = names_table,
            line = dict(color = '#506784'),
            fill = dict(color = 'grey'),
            align = 'center',
            font = dict(color = 'white', size = 10)
        ),
        cells = dict(
           values = table.values.T,
            fill = dict(
                color=[aux_color]
                ),
            )
        )
    traces.append(trace)

    layout = dict(
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=120
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        zoom=7,
    )

    figure = dict(data=traces, layout = layout)
    return figure


@app.callback(Output('mean_time_type1_table_obj', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              ])
def make_object_table_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = dff[dff.Situacao == 'Encerrada']

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Relatorio_data')

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i, 'time_days'])]
    dff = dff.loc[aux, :]
    dff.time_days = dff.time_days.apply(lambda x: float(x))

    table = dff.pivot_table(values='time_days', index=['Ano'], columns=['Objetivo_participacao'], aggfunc=agg_table_mean, fill_value = '', dropna = False)

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    table = table[names_table]

    names_table = ['<b>'+i+'</b>' for i in names_table]

    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    aux_color = []

    for i in table.Ano:
        if i%2 != 0:
            aux_color.append(rowOddColor)
        else:
            aux_color.append(rowEvenColor)

    traces = []

    trace = dict(
        type = 'table',
        header = dict(
            values = names_table,
            line = dict(color = '#506784'),
            fill = dict(color = 'grey'),
            align = 'center',
            font = dict(color = 'white', size = 10)
        ),
        cells = dict(
           values = table.values.T,
            fill = dict(
                color=[aux_color]
                ),
            )
        )

    traces.append(trace)

    layout = dict(
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=120
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        title="Média do tempo da disponibilização do relatório após a data de convocação por objetivo, em dias.",
        zoom=7,
    )

    figure = dict(data=traces, layout = layout)
    return figure

@app.callback(Output('mean_time_type1_table_subject', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              ])
def make_subject_table_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = dff[dff.Situacao == 'Encerrada']

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Relatorio_data')

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i, 'time_days'])]
    dff = dff.loc[aux, :]
    dff.time_days = dff.time_days.apply(lambda x: float(x))

    table = dff.pivot_table(values='time_days', index=['Ano'], columns=['Indexacao_Tema'], aggfunc=agg_table_mean, fill_value = '', dropna = False)

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    table = table[names_table]

    names_table = ['<b>'+i+'</b>' for i in names_table]

    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    aux_color = []

    for i in table.Ano:
        if i%2 != 0:
            aux_color.append(rowOddColor)
        else:
            aux_color.append(rowEvenColor)


    traces = []

    trace = dict(
        type = 'table',
        header = dict(
            values = names_table,
            line = dict(color = '#506784'),
            fill = dict(color = 'grey'),
            align = 'center',
            font = dict(color = 'white', size = 10)
        ),
        cells = dict(
           values = table.values.T,
            fill = dict(
                color=[aux_color]
                ),
            )
        )
    traces.append(trace)

    layout = dict(
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=120
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        title="Média do tempo da disponibilização do relatório após a data de convocação por tema, em dias.",
        zoom=7,
    )

    figure = dict(data=traces, layout = layout)
    return figure


@app.callback(Output('mean_time_type2_table_obj', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              ])
def make_object_table_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = dff[dff.Situacao == 'Encerrada']

    dff.Produto_Final_Data[dff.Produto_Final_Data == '2016'] = 'N/C'

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i,'Produto_Final_Data'])]

    dff = dff.loc[aux,:]

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i, 'Convocacao_Data'])]

    dff = dff.loc[aux, :]

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Produto_Final_Data')

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i, 'time_days'])]
    dff = dff.loc[aux, :]
    dff.time_days = dff.time_days.apply(lambda x: float(x))

    table = dff.pivot_table(values='time_days', index=['Ano'], columns=['Objetivo_participacao'], aggfunc=agg_table_mean, fill_value = '', dropna = False)

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    table = table[names_table]

    names_table = ['<b>'+i+'</b>' for i in names_table]

    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    aux_color = []

    for i in table.Ano:
        if i%2 != 0:
            aux_color.append(rowOddColor)
        else:
            aux_color.append(rowEvenColor)

    traces = []

    trace = dict(
        type = 'table',
        header = dict(
            values = names_table,
            line = dict(color = '#506784'),
            fill = dict(color = 'grey'),
            align = 'center',
            font = dict(color = 'white', size = 10)
        ),
        cells = dict(
           values = table.values.T,
            fill = dict(
                color=[aux_color]
                ),
            )
        )

    traces.append(trace)

    layout = dict(
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=120
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        title="Média do tempo da disponibilização do produto final após a data de convocação por objetivo, em dias.",
        zoom=7,
    )

    figure = dict(data=traces, layout = layout)
    return figure

@app.callback(Output('mean_time_type2_table_subject', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              ])
def make_subject_table_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = dff[dff.Situacao == 'Encerrada']

    dff.Produto_Final_Data[dff.Produto_Final_Data == '2016'] = 'N/C'

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i,'Produto_Final_Data'])]

    dff = dff.loc[aux,:]

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i, 'Convocacao_Data'])]

    dff = dff.loc[aux, :]

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Produto_Final_Data')

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i, 'time_days'])]
    dff = dff.loc[aux, :]
    dff.time_days = dff.time_days.apply(lambda x: float(x))

    table = dff.pivot_table(values='time_days', index=['Ano'], columns=['Indexacao_Tema'], aggfunc=agg_table_mean, fill_value = '', dropna = False)

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    table = table[names_table]

    names_table = ['<b>'+i+'</b>' for i in names_table]

    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    aux_color = []

    for i in table.Ano:
        if i%2 != 0:
            aux_color.append(rowOddColor)
        else:
            aux_color.append(rowEvenColor)


    traces = []

    trace = dict(
        type = 'table',
        header = dict(
            values = names_table,
            line = dict(color = '#506784'),
            fill = dict(color = 'grey'),
            align = 'center',
            font = dict(color = 'white', size = 10)
        ),
        cells = dict(
           values = table.values.T,
            fill = dict(
                color=[aux_color]
                ),
            )
        )
    traces.append(trace)

    layout = dict(
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=120
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        title="Média do tempo da disponibilização do produto final após a data de convocação por tema, em dias.",
        zoom=7,
    )

    figure = dict(data=traces, layout = layout)
    return figure

@app.callback(Output('mean_time_contribution', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),])
def make_subject_table_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = dff[dff.Situacao == 'Encerrada']

    aux = [float(i) for i in dff.index if 'N' not in str(dff.loc[i, 'Quantos_participaram']).upper()]

    dff = dff.loc[aux, :]

    dff.Quantos_participaram = dff.Quantos_participaram.apply(lambda x: float(x))

    q100 = dff.Quantos_participaram.quantile(1)

    q75 = dff.Quantos_participaram.quantile(0.75)

    q50 = dff.Quantos_participaram.quantile(0.5)

    q25 = dff.Quantos_participaram.quantile(0.25)

    dff['group'] = '0 |- {}'.format(q25)
    dff.group[dff.Quantos_participaram >= q25] = '{} |- {}'.format(q25,q50)
    dff.group[dff.Quantos_participaram >= q50] = '{} |- {}'.format(q50, q75)
    dff.group[dff.Quantos_participaram >= q75] = '{} |- {}'.format(q75, q100)

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Contribuicao_data_final')

    table = dff.pivot_table(values='time_days', index='Ano', columns='group', aggfunc=agg_table_mean,
                            fill_value='', dropna=False)

    names_table = ['Ano']
    names_table.extend(['0 |- {}'.format(q25), '{} |- {}'.format(q25,q50),
                        '{} |- {}'.format(q50, q75), '{} |- {}'.format(q75, q100)])

    table['Ano'] = table.index

    table = table[names_table]

    names_table = ['<b>' + i + '</b>' for i in names_table]

    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    aux_color = []

    for i in table.Ano:
        if i % 2 != 0:
            aux_color.append(rowOddColor)
        else:
            aux_color.append(rowEvenColor)

    traces = []

    trace = dict(
        type='table',
        header=dict(
            values=names_table,
            line=dict(color='#506784'),
            fill=dict(color='grey'),
            align='center',
            font=dict(color='white', size=10)
        ),
        cells=dict(
            values=table.values.T,
            fill=dict(
                color=[aux_color]
            ),
        )
    )
    traces.append(trace)

    layout = dict(
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=120
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        zoom=7,
    )

    figure = dict(data=traces, layout=layout)
    return figure

#app.css.append_css({"external_url": "https://codepen.io/JoaoCarabetta/pen/RjzpPB.css"})

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                #"https://cdn.rawgit.com/plotly/dash-app-stylesheets/5047eb29e4afe01b45b27b1d2f7deda2a942311a/goldman-sachs-report.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
               "https://cdn.rawgit.com/plotly/dash-app-stylesheets/a3401de132a6d0b652ba11548736b1d1e80aa10d/dash-goldman-sachs-report-js.js"]

for js in external_js:
    app.scripts.append_script({"external_url": js})

if __name__ == '__main__':
    app.run_server(debug=True)