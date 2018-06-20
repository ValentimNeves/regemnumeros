import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
from datetime import datetime

app = dash.Dash(__name__)

server = app.server

df = pd.read_csv(
    'https://docs.google.com/spreadsheets/d/'
     + '1IOvUGadhTcyLYtKY9yriImylhRgHNt6mQH-JcHf-3tU'
     + '/export?gid=0&format=csv', index_col=0)

df.Produto_Final_Data = df.Produto_Final_Data.apply(lambda x: str(x).split(';')[0])

agency_options = [{'label': agency, 'value': agency} for agency in set(df['Agência'])]

type_year_options = [{'label': 'Por ano', 'value': 'Por ano'},
                     {'label': 'Por mandato presidencial', 'value': 'Por mandato presidencial'},
                     {'label': 'Por mandato diretor-presidente da agência', 'value': 'Por mandato diretor-presidente da agência'}]

type_part_options = [{'label': 'Todos', 'value': 'Todos'},
                     {'label': 'Presencial', 'value': 'PP'},
                     {'label': 'Não presencial', 'value': 'PNP'},
                     {'label': 'Presencial e não presencial', 'value': 'PP e PNP'}]

colors_palette = ['#e69f09', '#56b4e9', '#009e73', '#f0e442',
                  '#0072b2', '#d55e00', '#cc79a7', '#cccccc',
                  '#515151']

objective_options = []
subject_options = []

aux_instru_part = {'PP': 'Presencial', 'PNP': 'Não presencial',
                   'PP e PNP': 'Presencial e não presencial'}

colors = {'text_H1': '#292735',
          'text_n': '#565656'}

app.layout = \
html.Div([
    html.Div([
            html.H2('Regulação em números',
                    style = {'text-align': 'center', 'color': colors['text_H1']}),
            html.H6('Mecanismo de participação',
                    style = {'text-align': 'center', 'color': colors['text_n']}),
        ],className='row'),

    html.Hr(style={'margin': '20', 'margin-bottom': '5'}),

    html.Div([
        html.Div([
            html.Div([
                html.P('Agência:'),
                dcc.Dropdown(
                    id='agency_options',
                    options=agency_options,
                    value='ANA',
                )
            ], className='one columns offset-by-one', style ={'float': 'left', 'color': colors['text_H1']},),

            html.Div([
                html.P('Instrumento de participação:'),
                dcc.Dropdown(
                    id='type_part_options',
                    options=type_part_options,
                    value='Todos',
                )
            ], className='two columns offset-by-one', style ={'float': 'left', 'color': colors['text_H1']},),

            html.Div([
                html.P('Objetivo do mecanismo:'),
                dcc.Dropdown(
                    id='objective_options',
                    options=objective_options,
                    value='Todos',
                )
            ], className='two columns offset-by-one', style ={'float': 'left', 'color': colors['text_H1']},),

            html.Div([
                html.P('Tema do mecanismo:'),
                dcc.Dropdown(
                    id='subject_options',
                    options=subject_options,
                    value='Todos',
                ),
            ], className='two columns offset-by-one', style={'float': 'left', 'color': colors['text_H1']},),
        ], className='row', style={'margin-top': '20'},),
    ]),

    html.Div([
        html.H6('',
                id='num_mecanism',
                style={'text-align': 'center', 'color': colors['text_H1'], 'margin-top': '60'},
                ),
    ], className = 'six columns offset-by-three'),

    html.Div([
        html.P('Percentual do número de audiências por ano em relação ao total de todos os anos.',
               style={'text-align': 'center'}
        ),
        dcc.Graph(id='contribution_time'),
    ], className = 'ten columns offset-by-one', style = {'margin-top': '35'}),

    html.Div([
        html.P('Número bruto de mecanismos de participação por ano.',
               style={'text-align': 'center'}
        ),
        dcc.Graph(id='table_contribution_number'),
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Percentual de informações não disponíveis, dos mecanismos realizados, por ano.',
               style={'text-align': 'center'}
        ),
        dcc.Graph(id='contribution_time_N/D'),
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Percentual de audiências por ano e objetivo da participação.',
               style={'text-align': 'center'}
        ),
        dcc.Graph(id='object_time'),
    ], className = 'ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Percentual de audiências por ano e tema da audiência.',
               style={'text-align': 'center'}
        ),
        dcc.Graph(id='subject_time'),
    ], className = 'ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Número bruto de mecanismos de participação por tema e ano.',
               style={'text-align': 'center'}
        ),
        dcc.Graph(id='table_contribution_number_subject'),
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.Hr(style={'margin': '0', 'margin-bottom': '0'}),
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Média do tempo da preparação para a audiência, em dias.',
               style={'text-align': 'center'}
        ),
        dcc.Graph(id='mean_time_preparation')
    ], className = 'ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Média do tempo da preparação para a audiência por objetivo da participação, em dias.',
               style={'text-align': 'center'}
        ),
        dcc.Graph(id='mean_time_preparation_table_obj')
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Média do tempo da preparação para a audiência por tema da audiência, em dias.',
               style={'text-align': 'center'}
        ),
        dcc.Graph(id='mean_time_preparation_table_subject')
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

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
               style={'text-align': 'center'}
        ),
        dcc.Graph(id='mean_time_answer')
    ], className = 'ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Média do tempo da disponibilização do relatório após a última data de contribuição por objetivo, em dias.',
               style={'text-align': 'center'}
        ),
        dcc.Graph(id='mean_time_answer_table_obj')
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

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
        html.P('Média do tempo da disponibilização do relatório após a convocação por objetivo das audiências ou consultas públicas, em dias.',
               style={'text-align': 'center'}),

        dcc.Graph(id='mean_time_type1_table_obj')
    ],
        className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Média do tempo da disponibilização do relatório após a convocação por tema das audiências ou consultas públicas, em dias.',
               style={'text-align': 'center'}
        ),
        dcc.Graph(id='mean_time_type1_table_subject')
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.Hr(style={'margin': '0', 'margin-bottom': '0'}),
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P("Média do tempo da disponibilização do produto final após a convocação, em dias.",
               style={'text-align': 'center'}
        ),
        dcc.Graph(id='mean_time_type2')
    ], className = 'ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P("Média do tempo da disponibilização do produto final após a convocação por objetivo das audiências ou consultas públicas, em dias.",
               style={'text-align': 'center'}
        ),
        dcc.Graph(id='mean_time_type2_table_obj')
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P("Média do tempo da disponibilização do produto final após a convocação por tema das audiências ou consultas públicas, em dias.",
               style={'text-align': 'center'}
        ),
        dcc.Graph(id='mean_time_type2_table_subject')
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.Hr(style={'margin': '0', 'margin-bottom': '0'}),
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Comparação entre a média do tempo da disponibilização do relatório e a média do tempo da disponibilização do protudo final, em dias.',
               style={'text-align': 'center'}
        ),
        dcc.Graph(id='mean_time_type1_versus_mean_time_type2')
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.Hr(style={'margin': '0', 'margin-bottom': '0'}),
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P("Média do número de contribuintes que participaram de audiências ou consultas.",
               style={'text-align': 'center'}
        ),
        dcc.Graph(id = 'mean_contribution')
    ], className = 'ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P("Média do número de contribuintes que participaram de audiências ou consultas por objetivo",
               style={'text-align': 'center'}
        ),
        dcc.Graph(id = 'table_obj')
    ], className = 'ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P("Média do número de contribuintes que participaram de audiências ou consultas por tema",
               style={'text-align': 'center'}
               ),
        dcc.Graph(id='table_subject')
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.Hr(style={'margin': '0', 'margin-bottom': '0'}),
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Futura implementação: Escolha o período temporal:'),
        dcc.Dropdown(
            id='type_year_options',
            options=type_year_options,
            value='Por ano',
        ),
    ], className='three columns offset-by-one', style={'float': 'left', 'color': colors['text_H1']}),

], className='twelve columns', style = {'background-color': '#dddddd'})

def filter_dataframe(df, agency, int_part):
    """
    Recebe o banco de dados e retorna o  banco filtrado.

    Argumentos:
    -------
    agency (str): nome da agência
    int_part (str): instrumento de participação

    Return
    -------
    dff: Dataframe
    """
    if int_part == 'Todos':
        dff = df[df['Agência'] == agency]
        return dff
    else:
        dff = df[df['Agência'] == agency]
        dff = dff[dff['Instrumento_de_Participacao'] == int_part]
        return dff

def filter_dataframe_objective_subject(dff, objective, subject):
    """
    Recebe o banco de dados e retorna o banco filtrado.

    Argumentos:
    -------
    objective (str): objetivo do mecanismo de participção
    subject (str): tema do mecanismo de participação

    Return
    -------
    dff: Dataframe
    """

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

@app.callback(Output('objective_options', 'options'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('subject_options', 'value')])
def update_num_mecanism(agency_value, int_part_value, subject):
    """
    Recebe as opções selecionadas nos filtros dos gráficos e retorna uma nova lista com as opções filtradas do objetivo.

    Argumentos:
    -------
    agency_options (str): nome da agência
    int_part_value (str): instrumento de participação
    subject (str): tema do mecanismo de participação

    Return
    -------
    objective_options: List
    """

    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, 'Todos', subject)

    if 'N/D' in dff['Objetivo_participacao'].values:
        dff = dff[dff['Objetivo_participacao'] != 'N/D']

    objective_options = list(dff['Objetivo_participacao'].sort_values().unique())
    objective_options.insert(0, 'Todos')

    objective_options = [{'label': opt, 'value': opt} for opt in objective_options]

    return objective_options

@app.callback(Output('subject_options', 'options'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),])
def update_num_mecanism(agency_value, int_part_value, objective):
    """
    Recebe as opções selecionadas nos filtros dos gráficos e retorna uma nova lista com os opções filtradas dos temas.

    Argumentos:
    -------
    agency_options (str): nome da agência
    int_part_value (str): instrumento de participação
    objective (str): objetivo do mecanismo de participação

    Return
    -------
    subjective_options: List
    """

    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, 'Todos')

    if 'N/D' in dff['Indexacao_Tema'].values:
        dff = dff[dff['Indexacao_Tema'] != 'N/D']

    dff = sep_delimitador(dff, ';', 'Indexacao_Tema')

    subject_options = list(dff['Indexacao_Tema'].sort_values().unique())
    subject_options.insert(0, 'Todos')

    subject_options = [{'label': opt, 'value': opt} for opt in subject_options]

    return subject_options

@app.callback(Output('num_mecanism', 'children'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'),])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    """
    Cria um texto interativo com os filtros.

    Argumentos:
    -------
    agency_options (str): nome da agência
    int_part_value (str): instrumento de participação
    subject (str): tema do mecanismo de participação
    objective (str): objetivo do mecanismo de participação

    Return
    -------
    string
    """

    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)

    if dff.shape[0] > 0:
        if int_part_value == 'Todos':

            return "Para a agência {}, temos registro dos mecanismos de participação " \
                   "começando no ano {} e terminando em {}, totalizando {} " \
                   "registros, com {} ainda em andamento.".format(agency_value,
                                                                  np.min(dff.Ano),
                                                                  np.max(dff.Ano),
                                                                  dff.shape[0],
                                                                  dff[dff.Situacao == "Em andamento"].shape[0])

        else:
            return "Com essa combinação de filtros, para a agência {}, temos registro dos " \
                   "mecanismos de participação começando no ano {} e terminando em {}, " \
                   "totalizando {} registros, que foram feitos de forma {}, com {} " \
                   "ainda em andamento.".format(agency_value,
                                                np.min(dff.Ano),
                                                np.max(dff.Ano),
                                                dff.shape[0],
                                                aux_instru_part[int_part_value].lower(),
                                                dff[dff.Situacao == "Em andamento"].shape[0])
    else:
        return "Não temos registros, sobre a {}, com essas combinações de filtros".format(agency_value)

def colors_palettes_function(df, agency_value, columns):
    """
    Recebe o banco de dados e uma coluna dele, mais o filtro de agência, e retorna um dicionário.
    Com as keys sendo os valores únicos da coluna e os values a informação da cor

    Argumentos:
    -------
    df (dataframe): base de dados
    agenccy_value (str): nome da âgencia
    columns (str): nome de alguma coluna do base de dados

    Return
    -------
    aux_colors: Dictionary
    """

    df = df[df['Agência'] == agency_value]

    if 'N/D' in df[columns].values:
        df = df[df[columns] != 'N/D']

    multiplos_temas = False

    for i in df[columns]:
        if ';' in i:
            multiplos_temas = True
            break

    if multiplos_temas == True:
        lista_valores = list(df[columns].drop_duplicates().sort_values())

        aux = []
        [aux.extend(i.split(';')) for i in lista_valores]

        lista_valores_unicos = [i.strip() for i in aux]
        lista_valores_unicos = list(np.unique(lista_valores_unicos))

        c = 0
        aux_colors = {}
        for i in lista_valores_unicos:
            aux_colors.update({i: colors_palette[c]})
            c += 1

        return aux_colors

    else:
        lista_valores_unicos = list(df[columns].drop_duplicates().sort_values())

        c = 0
        aux_colors = {}
        for i in lista_valores_unicos:
            aux_colors.update({i: colors_palette[c]})
            c += 1

        return aux_colors

@app.callback(Output('contribution_time', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'),])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    """
    Recebe as variáveis e retorna um gráfico utilizando os filtros. Com a seguinte informação:
    Percentual do número de audiências por ano em relação ao total de todos os anos.

    Argumentos:
    -------
    agency_value (str): nome da agência
    int_part_value (str): instrumento de participação
    subject (str): tema do mecanismo de participação
    objective (str): objetivo do mecanismo de participação

    Return
    -------
    figure: Bar plot
    """


    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)

    min_aux = dff.Ano.min()
    max_aux = dff.Ano.max()

    y = [(dff.Ano[dff.Ano == i].count() / dff.Ano.count()) * 100 for i in range(min_aux, max_aux+1)]

    a = [str(i) + '%' for i in np.round(y, 1)]

    traces = []
    trace = dict(
        type='bar',
        x = list(range(min_aux,max_aux+1)),
        y = y,
        text=a,
        textposition = 'auto',
        marker = dict(
            color = '#5498A5'
        ),

    )

    traces.append(trace)

    layout = dict(
        height=600,
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
        xaxis=dict(type='category'),
        yaxis = dict (
            showgrid = False,
            showticklabels = False,
        )
       )

    figure = dict(data=traces, layout = layout)
    return figure

@app.callback(Output('contribution_time_N/D', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    """
    Recebe as variáveis e retorna um gráfico utilizando os filtros.

    Argumentos:
    -------
    agency_value (str): nome da agência
    int_part_value (str): instrumento de participação
    subject (str): tema do mecanismo de participação
    objective (str): objetivo do mecanismo de participação

    Return
    -------
    figure: Bar plot
    """

    dfff = filter_dataframe(df, agency_value, int_part_value)
    dfff = filter_dataframe_objective_subject(dfff, objective, subject)

    min_aux = dfff.Ano.min()
    max_aux = dfff.Ano.max()

    aux_ano = list(range(min_aux, max_aux + 1))
    aux_ano.append('Geral')

    dfff['Disponivel'] = 'Ementa disponível'
    dfff['Disponivel'][dfff['Ementa'] == 'N/D'] = 'Ementa não disponível'

    aux_objetivo = list(dfff.Disponivel.drop_duplicates().sort_values())

    traces = []

    aux_colors = {'Ementa disponível': colors_palette[0], 'Ementa não disponível': colors_palette[1]}

    for j in aux_objetivo:

        y = []

        for i in aux_ano:

            if i == 'Geral':
                aux = (dfff.Disponivel[dfff.Disponivel == j].count() / dfff.Disponivel.count()) * 100
                y.append(aux)

            else:
                aux = (dfff.Disponivel[dfff.Disponivel == j][dfff.Ano == i].count() / dfff.Disponivel[dfff.Ano == i].count()) * 100
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
        height=600,
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
        xaxis=dict(type='category'),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
        )

    )

    figure = dict(data=traces, layout=layout)
    return figure


@app.callback(Output('object_time', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    """
    Recebe as variáveis e retorna um gráfico utilizando os filtros.

    Argumentos:
    -------
    agency_value (str): nome da agência
    int_part_value (str): instrumento de participação
    subject (str): tema do mecanismo de participação
    objective (str): objetivo do mecanismo de participação

    Return
    -------
    figure: Bar plot
    """
    dfff = filter_dataframe(df, agency_value, int_part_value)
    dfff = filter_dataframe_objective_subject(dfff, objective, subject)

    if 'N/D' in dfff.Objetivo_participacao.values:
        dfff = dfff[dfff.Objetivo_participacao != 'N/D']

    min_aux = dfff.Ano.min()
    max_aux = dfff.Ano.max()

    aux_ano = list(range(min_aux, max_aux + 1))
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
                aux = (dfff.Objetivo_participacao[dfff.Objetivo_participacao == j][dfff.Ano == i].count() / dfff.Objetivo_participacao[dfff.Ano == i].count()) * 100
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
        height=600,
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
        xaxis=dict(type='category'),
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
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    dfff = filter_dataframe(df, agency_value, int_part_value)
    dfff = filter_dataframe_objective_subject(dfff, objective, subject)
    dfff = sep_delimitador(dfff, ';', 'Indexacao_Tema')

    if 'N/D' in dfff.Indexacao_Tema.values:
        dfff = dfff[dfff.Indexacao_Tema != 'N/D']

    min_aux = dfff.Ano.min()
    max_aux = dfff.Ano.max()

    aux_ano = list(range(min_aux, max_aux + 1))
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
                aux = (dfff.Indexacao_Tema[dfff.Indexacao_Tema == j][dfff.Ano == i].count() / dfff.Indexacao_Tema[dfff.Ano == i].count()) * 100
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
            color=aux_colors[j],
                )
        )

        traces.append(trace)

    layout = dict(
        barmode='stack',
        height=600,
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
        xaxis=dict(type = 'category'),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
        )

    )

    figure = dict(data=traces, layout=layout)
    return figure

def data_calculo(df, var1, var2):

    time_day = []

    df[var1][df[var1] == 'nan'] = 'N/D'
    df[var2][df[var2] == 'nan'] = 'N/D'

    for i in df.index:
        if len(df.loc[i,var1]) > 5 and len(df.loc[i,var2]) > 5:
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
        else:
            time_day.append('N/D')

    return time_day

@app.callback(Output('mean_time_preparation', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Contribuicao_data_final')

    if 'N/D' in dff['time_days'].values:
        dff = dff[dff['time_days'] != 'N/D']

    dff['time_days'] = dff['time_days'].apply(lambda x: int(x))

    max_ano = dff.Ano.max()
    min_ano = dff.Ano.min()

    y = []
    x = []
    y2 = []
    x2 = []
    for i in range(min_ano,max_ano + 1):
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
        height=600,
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
        xaxis = dict(showgrid = False, type = 'category'),
        yaxis = dict(showgrid=False)
    )
    figure = dict(data=traces, layout = layout)
    return figure

@app.callback(Output('mean_time_answer', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)
    dff = dff[dff.Situacao == 'Encerrada']

    dff['time_days'] = data_calculo(dff, 'Contribuicao_data_final', 'Relatorio_data')

    if 'N/D' in dff['time_days'].values:
        dff = dff[dff['time_days'] != 'N/D']

    dff['time_days'] = dff['time_days'].apply(lambda x: int(x))

    max_ano = dff.Ano.max()
    min_ano = dff.Ano.min()

    y = []
    x = []
    y2 = []
    x2 = []
    for i in range(min_ano, max_ano + 1):
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
        height=600,
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
        xaxis=dict(showgrid=False, type = 'category'),
        yaxis=dict(showgrid=False)

    )
    figure = dict(data=traces, layout = layout)
    return figure

@app.callback(Output('mean_time_type1', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)
    dff = dff[dff.Situacao == 'Encerrada']

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Relatorio_data')

    if 'N/D' in dff['time_days'].values:
        dff = dff[dff['time_days'] != 'N/D']

    dff['time_days'] = dff['time_days'].apply(lambda x: int(x))

    max_ano = dff.Ano.max()
    min_ano = dff.Ano.min()

    y = []
    x = []
    y2 = []
    x2 = []
    for i in range(min_ano, max_ano + 1):
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
        height=600,
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
        xaxis=dict(showgrid=False, type = 'category'),
        yaxis=dict(showgrid=False)

    )
    figure = dict(data=traces, layout = layout)
    return figure

@app.callback(Output('mean_time_type2', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)
    dff = dff[dff.Situacao == 'Encerrada']

    dff.Produto_Final_Data[dff.Produto_Final_Data == '2016'] = 'N/C'

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i,'Produto_Final_Data'])]

    dff = dff.loc[aux,:]

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i, 'Convocacao_Data'])]

    dff = dff.loc[aux, :]

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Produto_Final_Data')

    if 'N/D' in dff['time_days'].values:
        dff = dff[dff['time_days'] != 'N/D']

    dff['time_days'] = dff['time_days'].apply(lambda x: int(x))

    max_ano = dff.Ano.max()
    min_ano = dff.Ano.min()

    y = []
    x = []
    y2 = []
    x2 = []
    for i in range(min_ano, max_ano + 1):
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
        height=600,
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
        xaxis=dict(showgrid=False, type = 'category'),
        yaxis=dict(showgrid=False)

    )
    figure = dict(data=traces, layout = layout)
    return figure


@app.callback(Output('mean_contribution', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)
    dff = dff[dff.Situacao == 'Encerrada']

    if 'N/D' in dff['Quantos_participaram'].values:
        dff = dff[dff['Quantos_participaram'] != 'N/D']

    max_ano = dff.Ano.max()
    min_ano = dff.Ano.min()

    y = []
    x = []
    y2 = []
    x2 = []
    for i in range(min_ano, max_ano + 1):
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
        height=600,
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
        xaxis=dict(showgrid=False, type = 'category'),
        yaxis=dict(showgrid=False)

    )
    figure = dict(data=traces, layout = layout)
    return figure

@app.callback(Output('table_obj', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)
    dff = dff[dff.Situacao == 'Encerrada']

    aux = [i for i in dff.index if 'N' not in dff.loc[i,'Quantos_participaram']]
    dff = dff.loc[aux,:]
    dff.Quantos_participaram = dff.Quantos_participaram.apply(lambda x: float(x))

    table = dff.pivot_table(values='Quantos_participaram', index=['Ano'], columns=['Objetivo_participacao'], aggfunc=agg_table_mean, fill_value = '', dropna = False)
    table_total = dff.pivot_table(values='Quantos_participaram', columns=['Objetivo_participacao'],
                            aggfunc=agg_table_mean, fill_value='', dropna=False)

    table_total['Ano'] = 'Total'

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    table = table[names_table]

    names_table = ['<b>'+i+'</b>' for i in names_table]

    for i in range(0, len(table_total.columns)):
        table_total.iloc[0,i] = '<b>' + str(table_total.iloc[0,i]) + '</b>'

    table = table.append(table_total)

    rowEvenColor = '#dddddd'
    rowOddColor = '#eeeeee'

    aux_color = []

    for i in range(0,len(table.Ano)):
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
            line = dict(color = 'white'),
            fill = dict(
                color=[aux_color]
                ),
            )
        )

    traces.append(trace)

    layout = dict(
        height=600,
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

def agg_table_mean(x):
    x = np.nanmean(x)
    x = np.round(x, 1)
    return x


@app.callback(Output('table_subject', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)
    dff = dff[dff.Situacao == 'Encerrada']
    dff = sep_delimitador(dff, ';', 'Indexacao_Tema')

    aux = [i for i in dff.index if 'N' not in dff.loc[i,'Quantos_participaram']]
    dff = dff.loc[aux,:]
    dff.Quantos_participaram = dff.Quantos_participaram.apply(lambda x: float(x))

    table = dff.pivot_table(values='Quantos_participaram', index=['Ano'], columns=['Indexacao_Tema'], aggfunc=agg_table_mean, fill_value = '', dropna = False)
    table_total = dff.pivot_table(values='Quantos_participaram', columns=['Indexacao_Tema'],
                            aggfunc=agg_table_mean, fill_value='', dropna=False)

    table_total['Ano'] = 'Total'

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    name_aux = names_table

    names_table = ['<b>'+i+'</b>' for i in names_table]

    for i in range(0, len(table_total.columns)):
        table_total.iloc[0,i] = '<b>' + str(table_total.iloc[0,i]) + '</b>'

    table = table.append(table_total)

    table = table[name_aux]

    rowEvenColor = '#dddddd'
    rowOddColor = '#eeeeee'

    aux_color = []

    for i in range(0,len(table.Ano)):
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
            line = dict(color = 'white'),
            fill = dict(
                color=[aux_color]
                ),
            )
        )

    traces.append(trace)

    layout = dict(
        height=600,
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

@app.callback(Output('mean_time_preparation_table_obj', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Contribuicao_data_final')

    if 'N/D' in dff['time_days'].values:
        dff = dff[dff['time_days'] != 'N/D']

    dff['time_days'] = dff['time_days'].apply(lambda x: int(x))

    table = dff.pivot_table(values='time_days', index=['Ano'], columns=['Objetivo_participacao'], aggfunc=agg_table_mean, fill_value = '', dropna = False)
    table_total = dff.pivot_table(values='time_days', columns=['Objetivo_participacao'],
                                  aggfunc=agg_table_mean, fill_value='', dropna=False)

    table_total['Ano'] = 'Total'

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    name_aux = names_table

    names_table = ['<b>' + i + '</b>' for i in names_table]

    for i in range(0, len(table_total.columns)):
        table_total.iloc[0, i] = '<b>' + str(table_total.iloc[0, i]) + '</b>'

    table = table.append(table_total)

    table = table[name_aux]

    rowEvenColor = '#dddddd'
    rowOddColor = '#eeeeee'

    aux_color = []

    for i in range(0, len(table.Ano)):
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
            line=dict(color='white'),
            fill=dict(
                color=[aux_color]
            ),
        )
    )

    traces.append(trace)

    layout = dict(
        height=600,
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


def sep_delimitador(dff, sep, column):
    dff[column] = dff[column].str.split(sep)

    for i in dff[column].index:
        if len(dff[column][i]) == 1:
            dff.loc[i, column] = dff.loc[i, column][0].strip()

        else:
            aux_list = dff.loc[i, column]
            row = dff.loc[i,:]
            dff.loc[i,column] = aux_list[0]
            aux_list.pop(0)

            for j in aux_list:
                aux_row = row
                aux_row[column] = j.strip()
                dff = dff.append(aux_row)

    dff = dff.reset_index(drop=True)

    if 'N/D' in dff[column].values:
        dff = dff[dff[column] != 'N/D']

    return dff

@app.callback(Output('mean_time_preparation_table_subject', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)
    dff = sep_delimitador(dff, ';', 'Indexacao_Tema')

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Contribuicao_data_final')

    if 'N/D' in dff['time_days'].values:
        dff = dff[dff['time_days'] != 'N/D']

    dff['time_days'] = dff['time_days'].apply(lambda x: int(x))

    table = dff.pivot_table(values='time_days', index=['Ano'], columns=['Indexacao_Tema'], aggfunc=agg_table_mean, fill_value = '', dropna = False)
    table_total = dff.pivot_table(values='time_days', columns=['Indexacao_Tema'],
                                  aggfunc=agg_table_mean, fill_value='', dropna=False)

    table_total['Ano'] = 'Total'

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    name_aux = names_table

    names_table = ['<b>' + i + '</b>' for i in names_table]

    for i in range(0, len(table_total.columns)):
        table_total.iloc[0, i] = '<b>' + str(table_total.iloc[0, i]) + '</b>'

    table = table.append(table_total)

    table = table[name_aux]

    rowEvenColor = '#dddddd'
    rowOddColor = '#eeeeee'

    aux_color = []

    for i in range(0, len(table.Ano)):
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
            line=dict(color='white'),
            fill=dict(
                color=[aux_color]
            ),
        )
    )

    traces.append(trace)

    layout = dict(
        height=600,
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
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)
    dff = dff[dff.Situacao == 'Encerrada']

    dff['time_days'] = data_calculo(dff, 'Contribuicao_data_final', 'Relatorio_data')

    if 'N/D' in dff['time_days'].values:
        dff = dff[dff['time_days'] != 'N/D']

    dff['time_days'] = dff['time_days'].apply(lambda x: int(x))

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i, 'time_days'])]
    dff = dff.loc[aux, :]
    dff.time_days = dff.time_days.apply(lambda x: float(x))

    table = dff.pivot_table(values='time_days', index=['Ano'], columns=['Objetivo_participacao'], aggfunc=agg_table_mean, fill_value = '', dropna = False)
    table_total = dff.pivot_table(values='time_days', columns=['Objetivo_participacao'],
                                  aggfunc=agg_table_mean, fill_value='', dropna=False)

    table_total['Ano'] = 'Total'

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    name_aux = names_table

    names_table = ['<b>' + i + '</b>' for i in names_table]

    for i in range(0, len(table_total.columns)):
        table_total.iloc[0, i] = '<b>' + str(table_total.iloc[0, i]) + '</b>'

    table = table.append(table_total)

    table = table[name_aux]

    rowEvenColor = '#dddddd'
    rowOddColor = '#eeeeee'

    aux_color = []

    for i in range(0, len(table.Ano)):
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
            line=dict(color='white'),
            fill=dict(
                color=[aux_color]
            ),
        )
    )

    traces.append(trace)

    layout = dict(
        height=600,
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
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)
    dff = dff[dff.Situacao == 'Encerrada']
    dff = sep_delimitador(dff, ';', 'Indexacao_Tema')

    dff['time_days'] = data_calculo(dff, 'Contribuicao_data_final', 'Relatorio_data')

    if 'N/D' in dff['time_days'].values:
        dff = dff[dff['time_days'] != 'N/D']

    dff['time_days'] = dff['time_days'].apply(lambda x: int(x))

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i, 'time_days'])]
    dff = dff.loc[aux, :]
    dff.time_days = dff.time_days.apply(lambda x: float(x))

    table = dff.pivot_table(values='time_days', index=['Ano'], columns=['Indexacao_Tema'], aggfunc=agg_table_mean, fill_value = '', dropna = False)
    table_total = dff.pivot_table(values='time_days', columns=['Indexacao_Tema'],
                                  aggfunc=agg_table_mean, fill_value='', dropna=False)

    table_total['Ano'] = 'Total'

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    name_aux = names_table

    names_table = ['<b>' + i + '</b>' for i in names_table]

    for i in range(0, len(table_total.columns)):
        table_total.iloc[0, i] = '<b>' + str(table_total.iloc[0, i]) + '</b>'

    table = table.append(table_total)

    table = table[name_aux]

    rowEvenColor = '#dddddd'
    rowOddColor = '#eeeeee'

    aux_color = []

    for i in range(0, len(table.Ano)):
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
            line=dict(color='white'),
            fill=dict(
                color=[aux_color]
            ),
        )
    )

    traces.append(trace)

    layout = dict(
        height=600,
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
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)
    dff = dff[dff.Situacao == 'Encerrada']

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Relatorio_data')

    if 'N/D' in dff['time_days'].values:
        dff = dff[dff['time_days'] != 'N/D']

    dff['time_days'] = dff['time_days'].apply(lambda x: int(x))

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i, 'time_days'])]
    dff = dff.loc[aux, :]
    dff.time_days = dff.time_days.apply(lambda x: float(x))

    table = dff.pivot_table(values='time_days', index=['Ano'], columns=['Objetivo_participacao'], aggfunc=agg_table_mean, fill_value = '', dropna = False)
    table_total = dff.pivot_table(values='time_days', columns=['Objetivo_participacao'],
                                  aggfunc=agg_table_mean, fill_value='', dropna=False)

    table_total['Ano'] = 'Total'

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    name_aux = names_table

    names_table = ['<b>' + i + '</b>' for i in names_table]

    for i in range(0, len(table_total.columns)):
        table_total.iloc[0, i] = '<b>' + str(table_total.iloc[0, i]) + '</b>'

    table = table.append(table_total)

    table = table[name_aux]

    rowEvenColor = '#dddddd'
    rowOddColor = '#eeeeee'

    aux_color = []

    for i in range(0, len(table.Ano)):
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
            line=dict(color='white'),
            fill=dict(
                color=[aux_color]
            ),
        )
    )

    traces.append(trace)

    layout = dict(
        height=600,
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

@app.callback(Output('mean_time_type1_table_subject', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)
    dff = dff[dff.Situacao == 'Encerrada']
    dff = sep_delimitador(dff, ';', 'Indexacao_Tema')

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Relatorio_data')

    if 'N/D' in dff['time_days'].values:
        dff = dff[dff['time_days'] != 'N/D']

    dff['time_days'] = dff['time_days'].apply(lambda x: int(x))

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i, 'time_days'])]
    dff = dff.loc[aux, :]
    dff.time_days = dff.time_days.apply(lambda x: float(x))

    table = dff.pivot_table(values='time_days', index=['Ano'], columns=['Indexacao_Tema'], aggfunc=agg_table_mean, fill_value = '', dropna = False)
    table_total = dff.pivot_table(values='time_days', columns=['Indexacao_Tema'],
                                  aggfunc=agg_table_mean, fill_value='', dropna=False)

    table_total['Ano'] = 'Total'

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    name_aux = names_table

    names_table = ['<b>' + i + '</b>' for i in names_table]

    for i in range(0, len(table_total.columns)):
        table_total.iloc[0, i] = '<b>' + str(table_total.iloc[0, i]) + '</b>'

    table = table.append(table_total)

    table = table[name_aux]

    rowEvenColor = '#dddddd'
    rowOddColor = '#eeeeee'

    aux_color = []

    for i in range(0, len(table.Ano)):
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
            line=dict(color='white'),
            fill=dict(
                color=[aux_color]
            ),
        )
    )

    traces.append(trace)

    layout = dict(
        height=600,
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


@app.callback(Output('mean_time_type2_table_obj', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)
    dff = dff[dff.Situacao == 'Encerrada']

    dff.Produto_Final_Data[dff.Produto_Final_Data == '2016'] = 'N/C'

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i,'Produto_Final_Data'])]

    dff = dff.loc[aux,:]

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i, 'Convocacao_Data'])]

    dff = dff.loc[aux, :]

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Produto_Final_Data')

    if 'N/D' in dff['time_days'].values:
        dff = dff[dff['time_days'] != 'N/D']

    dff['time_days'] = dff['time_days'].apply(lambda x: int(x))

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i, 'time_days'])]
    dff = dff.loc[aux, :]
    dff.time_days = dff.time_days.apply(lambda x: float(x))

    table = dff.pivot_table(values='time_days', index=['Ano'], columns=['Objetivo_participacao'], aggfunc=agg_table_mean, fill_value = '', dropna = False)
    table_total = dff.pivot_table(values='time_days', columns=['Objetivo_participacao'],
                                  aggfunc=agg_table_mean, fill_value='', dropna=False)

    table_total['Ano'] = 'Total'

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    name_aux = names_table

    names_table = ['<b>' + i + '</b>' for i in names_table]

    for i in range(0, len(table_total.columns)):
        table_total.iloc[0, i] = '<b>' + str(table_total.iloc[0, i]) + '</b>'

    table = table.append(table_total)

    table = table[name_aux]

    rowEvenColor = '#dddddd'
    rowOddColor = '#eeeeee'

    aux_color = []

    for i in range(0, len(table.Ano)):
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
            line=dict(color='white'),
            fill=dict(
                color=[aux_color]
            ),
        )
    )

    traces.append(trace)

    layout = dict(
        height=600,
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

@app.callback(Output('mean_time_type2_table_subject', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)
    dff = dff[dff.Situacao == 'Encerrada']
    dff = sep_delimitador(dff, ';', 'Indexacao_Tema')

    dff.Produto_Final_Data[dff.Produto_Final_Data == '2016'] = 'N/C'

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i,'Produto_Final_Data'])]

    dff = dff.loc[aux,:]

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i, 'Convocacao_Data'])]

    dff = dff.loc[aux, :]

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Produto_Final_Data')

    if 'N/D' in dff['time_days'].values:
        dff = dff[dff['time_days'] != 'N/D']

    dff['time_days'] = dff['time_days'].apply(lambda x: int(x))

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i, 'time_days'])]
    dff = dff.loc[aux, :]
    dff.time_days = dff.time_days.apply(lambda x: float(x))

    table = dff.pivot_table(values='time_days', index=['Ano'], columns=['Indexacao_Tema'], aggfunc=agg_table_mean, fill_value = '', dropna = False)
    table_total = dff.pivot_table(values='time_days', columns=['Indexacao_Tema'],
                                  aggfunc=agg_table_mean, fill_value='', dropna=False)

    table_total['Ano'] = 'Total'

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    name_aux = names_table

    names_table = ['<b>' + i + '</b>' for i in names_table]

    for i in range(0, len(table_total.columns)):
        table_total.iloc[0, i] = '<b>' + str(table_total.iloc[0, i]) + '</b>'

    table = table.append(table_total)

    table = table[name_aux]

    rowEvenColor = '#dddddd'
    rowOddColor = '#eeeeee'

    aux_color = []

    for i in range(0, len(table.Ano)):
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
            line=dict(color='white'),
            fill=dict(
                color=[aux_color]
            ),
        )
    )

    traces.append(trace)

    layout = dict(
        height=600,
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

@app.callback(Output('mean_time_contribution', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)
    dff = dff[dff.Situacao == 'Encerrada']

    aux = [float(i) for i in dff.index if 'N' not in str(dff.loc[i, 'Quantos_participaram']).upper()]

    dff = dff.loc[aux, :]

    dff.Quantos_participaram = dff.Quantos_participaram.apply(lambda x: float(x))

    q100 = dff.Quantos_participaram.quantile(1)

    q75 = dff.Quantos_participaram.quantile(0.75)

    q50 = dff.Quantos_participaram.quantile(0.5)

    q25 = dff.Quantos_participaram.quantile(0.25)

    dff['group'] = '0 |- {}'.format(int(q25))
    dff.group[dff.Quantos_participaram >= q25] = '{} |- {}'.format(int(q25),int(q50))
    dff.group[dff.Quantos_participaram >= q50] = '{} |- {}'.format(int(q50), int(q75))
    dff.group[dff.Quantos_participaram >= q75] = '{} |-| {}'.format(int(q75), int(q100))

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Contribuicao_data_final')

    if 'N/D' in dff['time_days'].values:
        dff = dff[dff['time_days'] != 'N/D']

    dff['time_days'] = dff['time_days'].apply(lambda x: int(x))

    table = dff.pivot_table(values='time_days', index='Ano', columns='group', aggfunc=agg_table_mean,
                            fill_value='', dropna=False)
    table_total = dff.pivot_table(values='time_days', columns=['group'],
                                  aggfunc=agg_table_mean, fill_value='', dropna=False)

    table_total['Ano'] = 'Total'

    names_table = ['Ano']
    names_table.extend(['0 |- {}'.format(int(q25)), '{} |- {}'.format(int(q25),int(q50)),
                        '{} |- {}'.format(int(q50), int(q75)), '{} |-| {}'.format(int(q75), int(q100))])

    table['Ano'] = table.index

    name_aux = names_table

    names_table = ['<b>' + i + '</b>' for i in names_table]

    for i in range(0, len(table_total.columns)):
        table_total.iloc[0, i] = '<b>' + str(table_total.iloc[0, i]) + '</b>'

    table = table.append(table_total)

    table = table[name_aux]


    rowEvenColor = '#dddddd'
    rowOddColor = '#eeeeee'

    aux_color = []

    for i in range(0, len(table.Ano)):
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
            line=dict(color='white'),
            fill=dict(
                color=[aux_color]
            ),
        )
    )

    traces.append(trace)

    layout = dict(
        height=600,
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

@app.callback(Output('mean_time_type1_versus_mean_time_type2', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)
    dff = dff[dff.Situacao == 'Encerrada']

    dff['time_days_type1'] = data_calculo(dff, 'Convocacao_Data', 'Relatorio_data')
    dff['time_days_type2'] = data_calculo(dff, 'Convocacao_Data', 'Produto_Final_Data')

    if 'N/D' in dff['time_days_type1'].values:
        dff = dff[(dff['time_days_type1'] != 'N/D') | (dff['time_days_type2'] != 'N/D')]

    max_ano = dff.Ano.max()
    min_ano = dff.Ano.min()

    y = []
    x = []
    y2 = []
    x2 = []
    for i in range(min_ano, max_ano + 1):
        y.append(np.mean([i for i in dff[dff.Ano == i].time_days_type1 if type(i) != str]))
        x.append(str(i))

        y2.append(np.mean([i for i in dff[dff.Ano == i].time_days_type2 if type(i) != str]))
        x2.append(str(i))

    traces = []
    trace = dict(
        type='Scatter',
        x = x,
        y = y,
        name = 'Tempo médio da convocação até o relatório'
        )

    trace2 = dict(
        x=x2,
        y=y2,
        type='Scatter',
        name='Tempo médio da convocação até o produto final',
    )

    traces.append(trace)
    traces.append(trace2)

    layout = dict(
        height=600,
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
        xaxis=dict(showgrid=False, type = 'category'),
        yaxis=dict(showgrid=False)

    )
    figure = dict(data=traces, layout = layout)
    return figure

'''
#Não ficou legal, pouco interpretavel
@app.callback(Output('mean_contribution_per_mean_time_preparation', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              ])
def make_object_time_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)

    dff['time_days'] = data_calculo(dff, 'Convocacao_Data', 'Contribuicao_data_final')

    if 'N/D' in dff['time_days'].values:
        dff = dff[dff['time_days'] != 'N/D']

    dff['time_days'] = dff['time_days'].apply(lambda x: int(x))

    max_ano = dff.Ano.max()
    min_ano = dff.Ano.min()

    y = []
    x = []
    y2 = []
    x2 = []
    for i in range(min_ano,max_ano + 1):
        y.append(np.mean([float(n)/t for n,t in zip(dff.Quantos_participaram[dff.Ano == i], dff.time_days[dff.Ano == i]) if type(i) != str]))
        x.append(str(i))

        y2.append(np.mean([float(n)/t for n,t in zip(dff.Quantos_participaram, dff.time_days) if type(i) != str]))
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
        xaxis = dict(showgrid = False, type = 'category'),
        yaxis = dict(showgrid=False)
    )
    figure = dict(data=traces, layout = layout)
    return figure
'''

@app.callback(Output('table_contribution_number', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)

    dff = dff.groupby('Ano').count()['Agência']

    min_aux = dff.index.min()
    max_aux = dff.index.max()

    aux = set(dff.index)
    aux2 = set(range(min_aux,max_aux+1))
    year_missing = aux2.difference(aux)

    for i in year_missing:
        dff = dff.append(pd.Series(0, index=[i]))

    dff = dff.sort_index()

    dff = dff.append(pd.Series(np.sum(dff), index=['Total']))

    dff = dff.to_frame('Número de mecanismos')

    dff['Ano'] = dff.index
    dff = dff[['Ano', 'Número de mecanismos']]

    table = dff

    del dff

    names_table = table.columns
    names_table = ['<b>'+i+'</b>' for i in names_table]

    table.loc['Total', 'Ano'] = '<b>' + str(table.loc['Total', 'Ano']) + '</b>'
    table.loc['Total', 'Número de mecanismos'] = '<b>' + str(table.loc['Total', 'Número de mecanismos']) + '</b>'

    rowEvenColor = '#dddddd'
    rowOddColor = '#eeeeee'

    aux_color = []

    for i in range(0,len(table.Ano)):
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
            line = dict(color = 'white'),
            fill = dict(
                color=[aux_color]
                ),
            )
        )

    traces.append(trace)

    layout = dict(
        height=600,
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



@app.callback(Output('table_contribution_number_subject', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'), ])
def update_num_mecanism(agency_value, int_part_value, objective, subject):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject)
    dff = sep_delimitador(dff, ';', 'Indexacao_Tema')

    table = dff.pivot_table(values='Agência', index=['Ano'], columns=['Indexacao_Tema'], aggfunc='count', fill_value = '', dropna = False)
    table_total = dff.pivot_table(values='Agência', columns=['Indexacao_Tema'],
                                  aggfunc='count', fill_value='', dropna=False)

    table_total['Ano'] = 'Total'

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    name_aux = names_table

    names_table = ['<b>' + i + '</b>' for i in names_table]

    for i in range(0, len(table_total.columns)):
        table_total.iloc[0, i] = '<b>' + str(table_total.iloc[0, i]) + '</b>'

    table = table.append(table_total)

    table = table[name_aux]

    rowEvenColor = '#dddddd'
    rowOddColor = '#eeeeee'

    aux_color = []

    for i in range(0, len(table.Ano)):
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
            line=dict(color='white'),
            fill=dict(
                color=[aux_color]
            ),
        )
    )

    traces.append(trace)

    layout = dict(
        height=600,
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