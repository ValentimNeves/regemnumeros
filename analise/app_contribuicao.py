import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import networkx as nx
from datetime import datetime

#networkx versão 2.1.0

app = dash.Dash(__name__)

server = app.server

df = pd.read_csv('https://docs.google.com/spreadsheets/d/' +
                        '1IOvUGadhTcyLYtKY9yriImylhRgHNt6mQH-JcHf-3tU' +
                        '/export?gid=133444484&format=csv', index_col = 0)

df_mecanismo = pd.read_csv('https://docs.google.com/spreadsheets/d/' +
                        '1IOvUGadhTcyLYtKY9yriImylhRgHNt6mQH-JcHf-3tU' +
                        '/export?gid=0&format=csv', index_col = 0)

df = pd.merge(df, df_mecanismo[["ID_Interno", "Ano", "Instrumento_de_Participacao", "Objetivo_participacao", "Indexacao_Tema"]], how = 'left', on = "ID_Interno")

df['Agência'] = df['ID_Interno'].apply(lambda x: str(x).split('_')[0])
df = df[df.Ano.isnull() == False]
df.Ano = df.Ano.apply(lambda x: int(x))

del df_mecanismo

colors_palette = ['#e69f09', '#56b4e9', '#009e73', '#f0e442', '#0072b2', '#d55e00', '#cc79a7', '#cccccc', '#515151']

agency_options = [{'label': agency, 'value': agency}
                  for agency in set(df['Agência'])]

type_year_options = [{'label': 'Por ano', 'value': 'Por ano'},
                     {'label': 'Por mandato presidencial', 'value': 'Por mandato presidencial'},
                     {'label': 'Por mandato diretor-presidente da agência', 'value': 'Por mandato diretor-presidente da agência'}]

type_part_options = [{'label': 'Todos', 'value': 'Todos'},
                     {'label': 'Presencial', 'value': 'PP'},
                     {'label': 'Não presencial', 'value': 'PNP'},
                     {'label': 'Presencial e não presencial', 'value': 'PP e PNP'}]

objective_options = []
subject_options = []

entidade_representativa_options = [{'label': 'Filtro desativado', 'value': 'Todos'},
                                   {'label': 'Entidade representativa', 'value': 'Sim'},
                                   {'label': 'Outros tipos de entidades', 'value': 'Não'}]


aux_instru_part = {'PP': 'Presencial', 'PNP': 'Não presencial', 'PP e PNP': 'Presencial e não presencial'}

colors = {'text_H1': '#292735',
          'text_n': '#565656'}

app.layout = html.Div(children=[
    html.Div(
        [
            html.H2(
                'Regulação em números',
                style = {'text-align': 'center',
                         'color': colors['text_H1'],
                         },
            ),
            html.H6('Manifestações', style = {'text-align': 'center', 'color': colors['text_n']}),
            dcc.Interval(id='base-update', interval=1000, n_intervals=10),
        ],
        className='row'
    ),
    html.Hr(style={'margin': '20', 'margin-bottom': '5'}),

    html.Div([
        html.Div([
                html.P('Agência:'),

                dcc.Dropdown(
                    id='agency_options',
                    options=agency_options,
                    value='ANA',
                ),

                html.P('Instrumento de participação:'),

                dcc.Dropdown(
                    id='type_part_options',
                    options=type_part_options,
                    value='Todos',
                ),

                html.P('Objetivo do mecanismo:'),

                dcc.Dropdown(
                    id='objective_options',
                    options=objective_options,
                    value='Todos',
                ),

        ], className='three columns offset-by-one', style={'margin-top': '20'}),

        html.Div([
                html.P('Tema do mecanismo:'),

                dcc.Dropdown(
                    id='subject_options',
                    options=subject_options,
                    value='Todos',
                ),

            html.P('Entidade representativa:'),

            dcc.Dropdown(
                id='entidade_representativa_options',
                options=entidade_representativa_options,
                value='Todos',
            ),


        ], className='three columns offset-by-one', style={'margin-top': '20'}),
    ]),

    html.Div([
        html.H6('',
                id='num_contribution',
                style={'text-align': 'center', 'color': colors['text_H1'], 'margin-top': '60'},
                ),
    ], className='six columns offset-by-three'),

    html.Div([
        html.P("Percentual do número de manifestações em relação ao total de todos os anos.",
               style={'text-align': 'center'}),

        dcc.Graph(id='contribution_time'),
    ], className='ten columns offset-by-one', style={'margin-top': '35'},
    ),

    html.Div([
        html.P('Percentual do número de contribuintes por ano e categoria',
               style={'text-align': 'center'}),

        dcc.Graph(id='category_time'),
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Percentual do número de contribuintes por instrumento de participação e ano',
               style={'text-align': 'center'}),

        dcc.Graph(id='contribuicoes_tipo_audiencia')
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Percentual do número de manifestações por ano e objetivo',
               style={'text-align': 'center'}),

        dcc.Graph(id='contribuicoes_ano_table')
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Percentual do número de manifestações por ano e tema',
               style={'text-align': 'center'}),

        dcc.Graph(id='contribuicoes_ano_table_subject')
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([

        html.Hr(style={'margin': '0', 'margin-bottom': '0'}),

    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Resposta de participantes por ano',
               style={'text-align': 'center'}),

        dcc.Graph(id='resposta_contribuicao')
        ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.Div([
            html.P('Resposta dos impactos das manifestações por categoria',
                   style={'text-align': 'center'}),

            dcc.Graph(id='resposta_contribuicao_categoria')
        ], className='ten columns offset-by-one', style={'margin-top': '35'}),
        html.Div([
            dcc.RangeSlider(
                id='my-slider-2',
                min=2000,
                max=2018,
                value=[2000, 2018],
                marks={i: i for i in range(2000, 2018+1)}
            ),
        ], className='ten columns offset-by-one', style={'margin-top': '0'}),
    ]),

    html.Div([

        html.Hr(style={'margin': '0', 'margin-bottom': '0'}),

    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Será que existe diferença no aceite quando o contribuinte é estatal?',
               style={'text-align': 'center'}),

        dcc.Graph(id='resposta_contribuicao_estatal')
        ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.Hr(style={'margin': '0', 'margin-bottom': '0'}),

    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Lista dos 6 contribuintes que mais participaram de audiências e consultas públicas.',
               style={'text-align': 'center'}),

        dcc.Graph(id='top_participants')
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Percentual e tipos de aceites dos principais participantes.',
               style={'text-align': 'center'}),

        dcc.Graph(id='top_participants_deepdive')
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.Hr(style={'margin': '0', 'margin-bottom': '0'}),

    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Lista dos 6 contribuintes que mais fizeram manifestações em audiências e consultas públicas.',
               style={'text-align': 'center'}),
        dcc.Graph(id='top_contributions')
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Percentual e tipos de aceites dos principais contribuintes.',
               style={'text-align': 'center'}),
        dcc.Graph(id='top_contributions_deepdive')
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.Hr(style={'margin': '0', 'margin-bottom': '0'}),

    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([

        html.P('Número mínimo de participação em mecanismos:'),

        dcc.Input(
            id='input_number_min',
            placeholder='Digite um número inteiro...',
            type='number',
            value=3,
        ), ],
        className='three columns offset-by-one', style={'float': 'left', 'color': colors['text_H1'], 'margin-top': '35'},
    ),

    html.Div([
        html.P('Rede de participação dos participantes. Se um participante esteve em uma mesma audiência com outro participante, eles são conectados.',
               style={'text-align': 'center'}),
        dcc.Graph(id='network_contributions')
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.Hr(style={'margin': '0', 'margin-bottom': '0'}),

    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P(
            'Fluxo das catgorias dos contribuintes, podemos ver onde elas mais se concentram e para qual subcategoria elas vão.',
            style={'text-align': 'center'}),
        dcc.Graph(id='sankey_contributions')
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
        ), ],
        className='three columns offset-by-one', style={'float': 'left', 'color': colors['text_H1']},
    ),

], className='twelve columns', style = {'background-color': '#dddddd'})

def filter_dataframe(df, agency, int_part):
    if int_part == 'Todos':
        dff = df[df['Agência'] == agency]
        return dff
    else:
        dff = df[df['Agência'] == agency]
        dff = dff[dff['Instrumento_de_Participacao'] == int_part]
        return dff

def filter_dataframe_objective_subject(dff, objective, subject, entidade):
    if objective == "Todos" and subject == "Todos" and entidade == 'Todos':
        return dff

    if objective != "Todos":
        dff = dff[dff["Objetivo_participacao"] == objective]

    if subject != "Todos":
        dff = dff[dff["Indexacao_Tema"] == subject]

    if entidade != 'Todos':
        dff = dff[dff["Entidade_Representativa"] == entidade]
    
    return dff

@app.callback(Output('objective_options', 'options'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('subject_options', 'value'),
               Input('entidade_representativa_options', 'value')])
def objective_dropdown(agency_value, int_part_value, subject, entidade):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, 'Todos', subject, entidade)

    if 'N/D' in dff['Objetivo_participacao'].values:
        dff = dff[dff['Objetivo_participacao'] != 'N/D']

    objective_options = list(dff['Objetivo_participacao'].sort_values().unique())
    objective_options.insert(0, 'Todos')

    objective_options = [{'label': opt, 'value': opt} for opt in objective_options]

    return objective_options

@app.callback(Output('subject_options', 'options'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('entidade_representativa_options', 'value')])
def subject_dropdown(agency_value, int_part_value, objective, entidade):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, 'Todos', entidade)

    if 'N/D' in dff['Indexacao_Tema'].values:
        dff = dff[dff['Indexacao_Tema'] != 'N/D']

    dff = sep_delimitador(dff, ';', 'Indexacao_Tema')

    subject_options = list(dff['Indexacao_Tema'].sort_values().unique())
    subject_options.insert(0, 'Todos')

    subject_options = [{'label': opt, 'value': opt} for opt in subject_options]

    return subject_options

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


@app.callback(Output('num_contribution', 'children'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'),
               Input('entidade_representativa_options', 'value')])
def update_text_contribution(agency_value, int_part_value, objective, subject, entidade):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject, entidade)

    aux_list = [i for i in dff.index if 'n' not in str(dff.Numero_Manifestacoes[i]).lower()]

    dff_aux = dff.loc[aux_list, :].copy()

    dff_aux.Numero_Manifestacoes = dff_aux.Numero_Manifestacoes.apply(lambda x: float(x))

    aux_sum = dff_aux.Numero_Manifestacoes.sum()

    aux_sum = int(aux_sum)

    if dff.shape[0] > 0:
        if int_part_value == 'Todos':

            return "Para a agência {}, temos registro das manifestações começando no ano {} " \
                   "e terminando em {}, totalizando {} manifetações que temos registro.".format(agency_value, int(np.min(dff.Ano)),
                                                                        int(np.max(dff.Ano)), aux_sum)

        else:
            return "Com essa combinação de filtros, para a agência {}, temos registro das manifestações começando no ano {} " \
                   "e terminando em {}, totalizando {} manifetações que temos registro, que foram feitos de forma {}.".format(agency_value, int(np.min(dff.Ano)),
                                                                                                       aux_sum,
                                                                                                       aux_instru_part[int_part_value].lower())
    else:
        return "Não temos registros, sobre a {}, com essas combinações de filtros.".format(agency_value)


@app.callback(Output('my-slider-2', 'value'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'),
               Input('entidade_representativa_options', 'value')])
def update_slider_value(agency_value, int_part_value, objective, subject, entidade):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject, entidade)

    return [dff.Ano.min(),dff.Ano.max()]

@app.callback(Output('my-slider-2', 'marks'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'),
               Input('entidade_representativa_options', 'value')])
def update_slider_marks(agency_value, int_part_value, objective, subject, entidade):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject, entidade)
    marks = {i:i for i in set(dff.Ano)}
    return marks

@app.callback(Output('my-slider-2', 'min'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'),
               Input('entidade_representativa_options', 'value')])
def update_slider_min(agency_value, int_part_value, objective, subject, entidade):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject, entidade)
    return dff.Ano.min()

@app.callback(Output('my-slider-2', 'max'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'),
               Input('entidade_representativa_options', 'value')])
def update_slider_max(agency_value, int_part_value, objective, subject, entidade):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject, entidade)
    return dff.Ano.max()

@app.callback(Output('contribution_time', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'),
               Input('entidade_representativa_options', 'value')])
def update_num_contribution(agency_value, int_part_value, objective, subject, entidade):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject, entidade)

    min_aux = dff.Ano.min()
    max_aux = dff.Ano.max()

    aux_list = [i for i in dff.index if 'n' not in str(dff.Numero_Manifestacoes[i]).lower()]

    dff = dff.loc[aux_list, :]

    dff.Numero_Manifestacoes = dff.Numero_Manifestacoes.apply(lambda x: float(x))

    y = [(dff.Numero_Manifestacoes[dff.Ano == i].sum() / dff.Numero_Manifestacoes.sum()) * 100 for i in range(min_aux, max_aux + 1)]

    a = [str(i) + '%' for i in np.round(y, 1)]

    traces = []
    trace = dict(
        type='bar',
        x = list(range(min_aux, max_aux + 1)),
        y = y,
        text = a,
        textposition = 'auto',
        marker = dict(
            color='#5498A5'
        )
    )

    traces.append(trace)

    layout = dict(
        height = 600,
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
        titlefont=dict(
            size=21,
            color='rgb(0,0,0)',
        ),
        font=dict(
            color='rgb(0,0,0)'
        ),
        xaxis = dict(type = 'category'),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
        )
    )

    figure = dict(data=traces, layout = layout)
    return figure

def colors_palettes_function(df, agency_options, columns):

    if agency_options == 'Todos':
        pass
    else:
        df = df[df['Agência']==agency_options]

    aux = list(df[columns].drop_duplicates().sort_values())

    c = 0
    aux_colors = {}
    for i in aux:
        aux_colors.update({i: colors_palette[c]})
        c += 1

    return aux_colors

@app.callback(Output('category_time', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'),
               Input('entidade_representativa_options', 'value')])
def update_num_category(agency_value, int_part_value, objective, subject, entidade):
    dfff = filter_dataframe(df, agency_value, int_part_value)
    dfff = filter_dataframe_objective_subject(dfff, objective, subject, entidade)
    dfff = dfff[dfff.Ano.isnull() == False]

    min_aux = dfff.Ano.min()
    max_aux = dfff.Ano.max()

    aux_ano = list(range(min_aux, max_aux + 1))
    aux_ano = [str(i) for i in aux_ano]
    aux_ano.append('Total')

    traces = []

    aux_colors = colors_palettes_function(df,'Todos','Categoria_Participante')

    dfff.Categoria_Participante[dfff.Categoria_Participante == 'N/D'] = 'Contribuinte não disponível'
    dfff.Categoria_Participante[dfff.Categoria_Participante == 'N/C'] = 'Contribuinte não identificado'

    aux_colors.update({'Contribuinte não disponível': aux_colors['N/D']})
    aux_colors.update({'Contribuinte não identificado': aux_colors['N/C']})

    aux_participante = list(dfff.Categoria_Participante.drop_duplicates().sort_values())

    for j in aux_participante:

        y = []

        for i in aux_ano:

            if i == 'Total':
                aux = (dfff.Categoria_Participante[dfff.Categoria_Participante == j].count() / dfff.Categoria_Participante.count()) * 100
                y.append(aux)

            else:
                aux = (dfff.Categoria_Participante[dfff.Categoria_Participante == j][dfff.Ano == int(i)].count() / dfff.Categoria_Participante[dfff.Ano == int(i)].count()) * 100
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
        height = 600,
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


@app.callback(Output('resposta_contribuicao', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'),
               Input('entidade_representativa_options', 'value')])
def update_num_impacto(agency_value, int_part_value, objective, subject, entidade):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject, entidade)
    #dfff = dff[(dff.Ano >= my_slider_value[0]) & (dff.Ano <= my_slider_value[1])]

    dff = dff[dff.Numero_Manifestacoes !='1?']
    dff = dff[dff.Numero_Manifestacoes != 'N/C']
    dff = dff[dff.Numero_Manifestacoes.isnull() == False]
    dff = dff[dff.Ano.isnull() == False]

    aux = [i for i in dff.columns if "impacto" in i]
    aux.append('Numero_Manifestacoes')

    dff[aux] = dff[aux].fillna('0')
    dff[aux] = dff[aux].apply(pd.to_numeric, errors='coerce')

    aux.append('Ano')

    aux_ano = list(dff.Ano.drop_duplicates().sort_values())
    aux_ano_geral = ['Ano ' + str(i) for i in aux_ano]
    aux_ano_geral.append('Total')

    traces = []

    aux_sim = [str(i) + '%' for i in np.round([(dff['Sim_impacto'][dff.Ano == i].sum()/dff.Numero_Manifestacoes[dff.Ano == i].sum())*100 for i in aux_ano], 1)]
    x = [(dff['Sim_impacto'][dff.Ano == i].sum()/dff.Numero_Manifestacoes[dff.Ano == i].sum())*100 for i in aux_ano]
    x.append((dff['Sim_impacto'].sum()/dff.Numero_Manifestacoes.sum())*100)
    aux_sim.append(str(np.round(x[-1]))+'%')

    trace1 = dict(
        type='bar',
        y=aux_ano_geral,
        x=x,
        orientation = 'h',
        text=aux_sim,
        textposition='auto',
        name = 'Gerou impacto',
        marker = dict(
            color = colors_palette[0]
        )
    )

    aux_Nao = [str(i) + '%' for i in np.round(
        [(dff['Nao_impacto'][dff.Ano == i].sum() / dff.Numero_Manifestacoes[dff.Ano == i].sum()) * 100
         for i in aux_ano], 1)]
    x = [(dff['Nao_impacto'][dff.Ano == i].sum() / dff.Numero_Manifestacoes[dff.Ano == i].sum()) * 100 for i in
         aux_ano]
    x.append((dff['Nao_impacto'].sum() / dff.Numero_Manifestacoes.sum()) * 100)
    aux_Nao.append(str(np.round(x[-1])) + '%')

    trace3 = dict(
        type='bar',
        y=aux_ano_geral,
        x=x,
        orientation = 'h',
        text=aux_Nao,
        textposition='auto',
        name = 'Não gerou impacto',
        marker = dict(
            color = colors_palette[1]
        )
    )

    aux_ND = [str(i) + '%' for i in np.round(
        [(dff['N/D_impacto'][dff.Ano == i].sum() / dff.Numero_Manifestacoes[dff.Ano == i].sum()) * 100
         for i in aux_ano], 1)]
    x = [(dff['N/D_impacto'][dff.Ano == i].sum() / dff.Numero_Manifestacoes[dff.Ano == i].sum()) * 100 for i in
         aux_ano]
    x.append((dff['N/D_impacto'].sum() / dff.Numero_Manifestacoes.sum()) * 100)
    aux_ND.append(str(np.round(x[-1])) + '%')

    trace4 = dict(
        type='bar',
        y=aux_ano_geral,
        x=x,
        orientation = 'h',
        text=aux_ND,
        textposition='auto',
        name='Não está disponível',
        marker = dict(
            color = colors_palette[2]
        )
    )


    aux_NA = [str(i) + '%' for i in np.round(
        [(dff['N/A_impacto'][dff.Ano == i].sum() / dff.Numero_Manifestacoes[dff.Ano == i].sum()) * 100
         for i in aux_ano], 1)]

    x = [(dff['N/A_impacto'][dff.Ano == i].sum() / dff.Numero_Manifestacoes[dff.Ano == i].sum()) * 100 for i in
         aux_ano]
    x.append((dff['N/A_impacto'].sum() / dff.Numero_Manifestacoes.sum()) * 100)
    aux_NA.append(str(np.round(x[-1])) + '%')

    trace5 = dict(
        type='bar',
        y=aux_ano_geral,
        x=x,
        orientation = 'h',
        text=aux_NA,
        textposition='auto',
        name = 'Recusado por não se aplicar',
        marker = dict(
            color = colors_palette[3]
        )
    )

    aux_NC = [str(i) + '%' for i in np.round(
        [(dff['N/C_impacto'][dff.Ano == i].sum() / dff.Numero_Manifestacoes[dff.Ano == i].sum()) * 100
         for i in aux_ano], 1)]
    x = [(dff['N/C_impacto'][dff.Ano == i].sum() / dff.Numero_Manifestacoes[dff.Ano == i].sum()) * 100 for i in
         aux_ano]
    x.append((dff['N/C_impacto'].sum() / dff.Numero_Manifestacoes.sum()) * 100)
    aux_NC.append(str(np.round(x[-1])) + '%')

    trace6 = dict(
        type='bar',
        y=aux_ano_geral,
        x=x,
        orientation = 'h',
        text=aux_NC,
        textposition='auto',
        name = 'Não está claro',
        marker = dict(
            color = colors_palette[4]
        )
    )


    traces.append(trace1)
    traces.append(trace3)
    traces.append(trace4)
    traces.append(trace5)
    traces.append(trace6)

    layout = dict(
        barmode='stack',
        height = 600,
        autosize=True,
        margin=dict(
            l=200,
            r=35,
            b=35,
            t=45
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h', traceorder = 'normal'),
        zoom=7,
    )
    figure = dict(data=traces, layout=layout)
    return figure

def find_nan_nd_nc(x):
    if 'n' in str(x).lower():
        return True
    else:
        return False

@app.callback(Output('resposta_contribuicao_categoria', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('my-slider-2', 'value'),
              Input('objective_options', 'value'),
              Input('subject_options', 'value'),
              Input('entidade_representativa_options', 'value')])
def make_contribution_time_aceite_figure(agency_value, int_part_value, my_slider_value, objective, subject, entidade):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject, entidade)
    dff = dff[(dff.Ano >= my_slider_value[0]) & (dff.Ano <= my_slider_value[1])]

    dff['aux_digit'] = dff.Numero_Manifestacoes.apply(lambda x: find_nan_nd_nc(x))

    dff = dff[dff['aux_digit'] == False]

    dff['Numero_Manifestacoes'] = dff.Numero_Manifestacoes.apply(lambda x: float(x))

    aux = [i for i in dff.columns if "impacto" in i]
    aux.append('Numero_Manifestacoes')

    dff[aux] = dff[aux].fillna('0')
    dff[aux] = dff[aux].apply(pd.to_numeric, errors='coerce')

    dff.loc[dff.Categoria_Participante == 'N/D', 'Categoria_Participante'] = 'Contribuinte não disponível'
    dff.loc[dff.Categoria_Participante == 'N/C', 'Categoria_Participante'] = 'Contribuinte não identificado'

    aux.append('Ano')

    aux_ano = list(dff.Categoria_Participante.drop_duplicates().sort_values())

    traces = []

    aux_sim = [str(i) + '%' for i in np.round(
        [(dff['Sim_impacto'][dff.Categoria_Participante == i].sum() / dff.Numero_Manifestacoes[
            dff.Categoria_Participante == i].sum()) * 100 for i in
         aux_ano], 1)]

    trace1 = dict(
        type='bar',
        y=aux_ano,
        x=[(dff['Sim_impacto'][dff.Categoria_Participante == i].sum()/dff.Numero_Manifestacoes[dff.Categoria_Participante == i].sum())*100 for i in aux_ano],
        orientation = 'h',
        name = 'Gerou impacto',
        text=aux_sim,
        textposition='auto',
        marker = dict(
            color = colors_palette[0]
        )
    )

    aux_Nao = [str(i) + '%' for i in np.round(
        [(dff['Nao_impacto'][dff.Categoria_Participante == i].sum() / dff.Numero_Manifestacoes[
            dff.Categoria_Participante == i].sum()) * 100
         for i in aux_ano], 1)]

    trace3 = dict(
        type='bar',
        y=aux_ano,
        x=[(dff['Nao_impacto'][dff.Categoria_Participante == i].sum()/dff.Numero_Manifestacoes[dff.Categoria_Participante == i].sum())*100 for i in aux_ano],
        orientation = 'h',
        name = 'Não gerou impacto',
          text=aux_Nao,
        textposition='auto',
        marker = dict(
            color = colors_palette[1]
        )
    )

    aux_ND = [str(i) + '%' for i in np.round(
        [(dff['N/D_impacto'][dff.Categoria_Participante == i].sum() / dff.Numero_Manifestacoes[
            dff.Categoria_Participante == i].sum()) * 100
         for i in aux_ano], 1)]

    trace4 = dict(
        type='bar',
        y=aux_ano,
        x=[(dff['N/D_impacto'][dff.Categoria_Participante == i].sum()/dff.Numero_Manifestacoes[dff.Categoria_Participante == i].sum())*100 for i in aux_ano],
        orientation = 'h',
        name='Não está disponível',
      text=aux_ND,
        textposition='auto',
        marker = dict(
            color = colors_palette[2]
        )
    )

    aux_NA = [str(i) + '%' for i in np.round(
        [(dff['N/A_impacto'][dff.Categoria_Participante == i].sum() / dff.Numero_Manifestacoes[
            dff.Categoria_Participante == i].sum()) * 100
         for i in aux_ano], 1)]


    trace5 = dict(
        type='bar',
        y=aux_ano,
        x=[(dff['N/A_impacto'][dff.Categoria_Participante == i].sum()/dff.Numero_Manifestacoes[dff.Categoria_Participante == i].sum())*100 for i in aux_ano],
        orientation = 'h',
        name = 'Recusado por não se aplicar',
      text=aux_NA,
        textposition='auto',
        marker = dict(
            color = colors_palette[3]
        )
    )

    aux_NC = [str(i) + '%' for i in np.round(
        [(dff['N/C_impacto'][dff.Categoria_Participante == i].sum() / dff.Numero_Manifestacoes[
            dff.Categoria_Participante == i].sum()) * 100
         for i in aux_ano], 1)]


    trace6 = dict(
        type='bar',
        y=aux_ano,
        x=[(dff['N/C_impacto'][dff.Categoria_Participante == i].sum()/dff.Numero_Manifestacoes[dff.Categoria_Participante == i].sum())*100 for i in aux_ano],
        orientation = 'h',
        name = 'Não está claro',
      text=aux_NC,
        textposition='auto',
        marker = dict(
            color = colors_palette[4]
        )
    )

    traces.append(trace1)
    traces.append(trace3)
    traces.append(trace4)
    traces.append(trace5)
    traces.append(trace6)

    layout = dict(
        barmode='stack',
        height = 600,
        autosize=True,
        margin=dict(
            l=200,
            r=35,
            b=35,
            t=45
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h', traceorder = 'normal'),
        zoom=7,
    )
    figure = dict(data=traces, layout=layout)
    return figure


@app.callback(Output('resposta_contribuicao_estatal', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'),
               Input('entidade_representativa_options', 'value')])
def update_num_impact_estatal(agency_value, int_part_value, objective, subject, entidade):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject, entidade)
    #dfff = dff[(dff.Ano >= my_slider_value[0]) & (dff.Ano <= my_slider_value[1])]

    dff = dff[dff.Numero_Manifestacoes !='1?']
    dff = dff[dff.Numero_Manifestacoes != 'N/C']
    dff = dff[dff.Numero_Manifestacoes.isnull() == False]
    dff = dff[dff.Ano.isnull() == False]
    dff = dff[dff.Estatal.isnull() == False]
    dff = dff[dff.Estatal !='?']

    aux = [i for i in dff.columns if "impacto" in i]
    aux.append('Numero_Manifestacoes')

    dff[aux] = dff[aux].fillna('0')
    dff[aux] = dff[aux].apply(pd.to_numeric, errors='coerce')

    dff.Ano = dff.Ano.apply(lambda x: str(x))

    estatal_ano = list(dff.Estatal.drop_duplicates().sort_values())

    if 'N/D' in estatal_ano:
        estatal_ano.remove('N/D')
    if 'N/C' in estatal_ano:
        estatal_ano.remove('N/C')

    traces = []

    aux_sim = [str(i) + '%' for i in np.round(
        [(dff['Sim_impacto'][(dff.Estatal == i)].sum() / dff.Numero_Manifestacoes[(dff.Estatal == i)].sum()) * 100 for i in
         estatal_ano], 1)]

    trace1 = dict(
        type='bar',
        y=estatal_ano,
        x=[(dff['Sim_impacto'][(dff.Estatal == i)].sum()/dff.Numero_Manifestacoes[(dff.Estatal == i)].sum())*100 for i in estatal_ano],
        orientation = 'h',
        name = 'Gerou impacto',
      text=aux_sim,
        textposition='auto',
        marker = dict(
            color = colors_palette[0]
        )
    )

    aux_Nao = [str(i) + '%' for i in np.round(
        [(dff['Nao_impacto'][(dff.Estatal == i)].sum() / dff.Numero_Manifestacoes[(dff.Estatal == i)].sum()) * 100 for i in
         estatal_ano], 1)]

    trace3 = dict(
        type='bar',
        y=estatal_ano,
        x=[(dff['Nao_impacto'][(dff.Estatal == i)].sum()/dff.Numero_Manifestacoes[(dff.Estatal == i)].sum())*100 for i in estatal_ano],
        orientation = 'h',
        name = 'Não gerou impacto',
      text=aux_Nao,
        textposition='auto',
        marker = dict(
            color = colors_palette[1]
        )
    )

    aux_ND = [str(i) + '%' for i in np.round(
        [(dff['N/D_impacto'][(dff.Estatal == i)].sum() / dff.Numero_Manifestacoes[(dff.Estatal == i)].sum()) * 100 for i in
         estatal_ano], 1)]

    trace4 = dict(
        type='bar',
        y=estatal_ano,
        x=[(dff['N/D_impacto'][(dff.Estatal == i)].sum()/dff.Numero_Manifestacoes[(dff.Estatal == i)].sum())*100 for i in estatal_ano],
        orientation = 'h',
        name='Não está disponível',
      text=aux_ND,
        textposition='auto',
        marker = dict(
            color = colors_palette[2]
        )
    )

    aux_NA = [str(i) + '%' for i in np.round(
        [(dff['N/A_impacto'][(dff.Estatal == i)].sum() / dff.Numero_Manifestacoes[(dff.Estatal == i)].sum()) * 100 for i in
         estatal_ano], 1)]

    trace5 = dict(
        type='bar',
        y=estatal_ano,
        x=[(dff['N/A_impacto'][(dff.Estatal == i)].sum()/dff.Numero_Manifestacoes[(dff.Estatal == i)].sum())*100 for i in estatal_ano],
        orientation = 'h',
        name = 'Recusado por não se aplicar',
      text=aux_NA,
        textposition='auto',
        marker = dict(
            color = colors_palette[3]
        )
    )


    aux_NC = [str(i) + '%' for i in np.round(
        [(dff['N/C_impacto'][(dff.Estatal == i)].sum() / dff.Numero_Manifestacoes[(dff.Estatal == i)].sum()) * 100 for i in
         estatal_ano], 1)]


    trace6 = dict(
        type='bar',
        y=estatal_ano,
        x=[(dff['N/C_impacto'][(dff.Estatal == i)].sum()/dff.Numero_Manifestacoes[(dff.Estatal == i)].sum())*100 for i in estatal_ano],
        orientation = 'h',
        name = 'Não está claro',
      text=aux_NC,
        textposition='auto',
        marker = dict(
            color = colors_palette[4]
        )
    )


    traces.append(trace1)
    traces.append(trace3)
    traces.append(trace4)
    traces.append(trace5)
    traces.append(trace6)

    layout = dict(
        barmode='stack',
        height = 600,
        autosize=True,
        margin=dict(
            l=200,
            r=35,
            b=35,
            t=45
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h', traceorder = 'normal'),
        zoom=7,
    )
    figure = dict(data=traces, layout=layout)
    return figure

def data_calculo(df, var1, var2):

    time_day = []

    for i in df.index:

        if df.loc[i,var1]  != 'N/D' and df.loc[i,var1]  != 'N/D' and type(df.loc[i,var1]) == str:
            if df.loc[i,var2]  != 'N/D' and df.loc[i,var2]  != 'N/D' and type(df.loc[i,var2]) == str:
                aux_var1 = datetime.strptime(df.loc[i, var1], '%Y/%m/%d')
                aux_var2 = datetime.strptime(df.loc[i, var2], '%Y/%m/%d')
                aux = aux_var2 - aux_var1
                aux = aux.days
                time_day.append(aux)
            else:
                time_day.append(df.loc[i,var2])
        else:
            time_day.append(df.loc[i,var1])

    return time_day


@app.callback(Output('contribuicoes_tipo_audiencia', 'figure'),
              [Input('agency_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'),
               Input('entidade_representativa_options', 'value')])
def update_num_instrumento(agency_value, objective, subject, entidade):
    dfff = filter_dataframe(df, agency_value, 'Todos')
    dfff = filter_dataframe_objective_subject(dfff, objective, subject, entidade)
    dfff = dfff[dfff.Ano.isnull() == False]

    min_aux = dfff.Ano.min()
    max_aux = dfff.Ano.max()

    aux_ano = list(range(min_aux, max_aux +1))
    aux_ano = [str(i) for i in aux_ano]
    aux_ano.append('Total')

    aux_participante = list(dfff.Instrumento_de_Participacao.drop_duplicates().sort_values())

    traces = []

    aux_colors = colors_palettes_function(df,agency_value,'Instrumento_de_Participacao')

    for j in aux_participante:

        y = []

        for i in aux_ano:

            if i == 'Total':
                aux = (dfff.Instrumento_de_Participacao[dfff.Instrumento_de_Participacao == j].count() / dfff.Instrumento_de_Participacao.count()) * 100
                y.append(aux)

            else:
                aux = (dfff.Instrumento_de_Participacao[dfff.Instrumento_de_Participacao == j][dfff.Ano == int(i)].count() / dfff.Instrumento_de_Participacao[dfff.Ano == int(i)].count()) * 100
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
        height = 600,
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

@app.callback(Output('contribuicoes_ano_table', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'),
               Input('entidade_representativa_options', 'value')])
def update_table_percentage_objective(agency_value, int_part_value, objective, subject, entidade):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject, entidade)

    if 'N/D' in dff['Numero_Manifestacoes'].values:
        dff = dff[dff['Numero_Manifestacoes'] != 'N/D']

    aux = [i for i in dff.index if 'N' not in dff.loc[i,'Numero_Manifestacoes']]
    dff = dff.loc[aux,:]
    dff.Numero_Manifestacoes = dff.Numero_Manifestacoes.apply(lambda x: float(x))

    table = dff.pivot_table(values='Numero_Manifestacoes', index=['Ano'], columns=['Objetivo_participacao'], aggfunc=np.sum, fill_value = 0, dropna = False)

    table.loc['Total'] = table.sum(0)

    table['Total'] = table.sum(1)

    table = np.round((table/table.loc['Total','Total'])*100,2)

    table = table.replace(0, '')

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    table = table[names_table]

    names_table = ['<b>'+i+'</b>' for i in names_table]

    for i in range(0, len(table.columns)):
        table.iloc[-1, i] = '<b>' + str(table.iloc[-1, i]) + '</b>'

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
            line=dict(color='white'),
            fill = dict(
                color=[aux_color]
                ),
            )
        )

    traces.append(trace)

    layout = dict(
        height = 600,
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

@app.callback(Output('contribuicoes_ano_table_subject', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'),
               Input('entidade_representativa_options', 'value')])
def update_table_percentage_subject(agency_value, int_part_value, objective, subject, entidade):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject, entidade)
    dff = sep_delimitador(dff, ';', 'Indexacao_Tema')

    if 'N/D' in dff['Numero_Manifestacoes'].values:
        dff = dff[dff['Numero_Manifestacoes'] != 'N/D']

    aux = [i for i in dff.index if 'N' not in dff.loc[i,'Numero_Manifestacoes']]
    dff = dff.loc[aux,:]
    dff.Numero_Manifestacoes = dff.Numero_Manifestacoes.apply(lambda x: float(x))

    table = dff.pivot_table(values='Numero_Manifestacoes', index=['Ano'], columns=['Indexacao_Tema'], aggfunc=np.sum, fill_value = 0, dropna = False)

    table.loc['Total'] = table.sum(0)

    table['Total'] = table.sum(1)

    table = np.round((table/table.loc['Total','Total'])*100,2)

    table = table.replace(0, '')

    names_table = ['Ano']
    names_table.extend(list(table.columns))

    table['Ano'] = table.index

    table = table[names_table]

    names_table = ['<b>'+i+'</b>' for i in names_table]

    for i in range(0, len(table.columns)):
        table.iloc[-1, i] = '<b>' + str(table.iloc[-1, i]) + '</b>'

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
            line=dict(color='white'),
            fill = dict(
                color=[aux_color]
                ),
            )
        )

    traces.append(trace)

    layout = dict(
        height = 600,
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

@app.callback(Output('top_participants', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'),
               Input('entidade_representativa_options', 'value')])
def update_table_top6_participants(agency_value, int_part_value, objective, subject, entidade):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject, entidade)

    if 'N/D' in dff['Numero_Manifestacoes'].values:
        dff = dff[dff['Numero_Manifestacoes'] != 'N/D']

    if 'N/D' in dff['Quem'].values:
        dff = dff[dff['Quem'] != 'N/D']

    size = len(dff.ID_Interno.drop_duplicates())

    dff = dff[['Quem', 'Numero_Manifestacoes']]

    dff_table = dff.groupby('Quem').count().sort_values('Numero_Manifestacoes', ascending=False)

    dff_table['Percentual de participações em relação ao total'] = np.round((dff_table['Numero_Manifestacoes']/size)*100,2)

    aux = [i for i in dff.index if 'N' not in dff.loc[i,'Numero_Manifestacoes']]
    dff = dff.loc[aux,:]
    dff.Numero_Manifestacoes = dff.Numero_Manifestacoes.apply(lambda x: np.ceil(float(x)))

    dff_table = dff_table.merge(dff.groupby('Quem').sum(), left_index=True, right_index=True)

    dff_table.columns = ['Número de participação', 'Percentual de participações', 'Número total de manifestações']

    dff_table['Média de manifestações por participação'] = np.round(dff_table['Número total de manifestações']/dff_table['Número de participação'], 2)

    total_contributions = dff_table['Número total de manifestações'].sum()

    dff_table['Percentual de manifestações em relação total'] = np.round(
        dff_table['Número total de manifestações'] / total_contributions*100, 2)

    names_table = ['Contribuidor']
    names_table.extend(list(dff_table.columns))

    dff_table['Contribuidor'] = dff_table.index

    dff_table['Contribuidor'] = dff_table['Contribuidor'].apply(lambda x: x.split('(')[0])

    dff_table = dff_table[names_table]

    names_table = ['<b>'+i+'</b>' for i in names_table]

    rowEvenColor = '#dddddd'
    rowOddColor = '#eeeeee'

    aux_color = []

    dff_table = dff_table.sort_values(['Número de participação', 'Número total de manifestações'], ascending=False)

    if len(dff_table) > 6:
        dff_table = dff_table[0:6]

    for i in range(0,len(dff_table.index)):
        if i%2 == 0:
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
           values = dff_table.values.T,
            line=dict(color='white'),
            fill = dict(
                color=[aux_color]
                ),
            )
        )

    traces.append(trace)

    layout = dict(
        height = 600,
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        zoom=7,
    )

    figure = dict(data=traces, layout = layout)
    return figure


@app.callback(Output('top_contributions', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'),
               Input('entidade_representativa_options', 'value')])
def update_table_top6_contribution(agency_value, int_part_value, objective, subject, entidade):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject, entidade)

    size = len(dff.ID_Interno.drop_duplicates())

    dff = dff[['Quem', 'Numero_Manifestacoes']]

    if 'N/D' in dff.Quem.values:
        dff =dff[dff.Quem != 'N/D']

    dff_table = dff.groupby('Quem').count().sort_values('Numero_Manifestacoes', ascending=False)

    dff_table['Percentual de participações'] = np.round((dff_table['Numero_Manifestacoes']/size)*100,2)

    aux = [i for i in dff.index if 'N' not in dff.loc[i,'Numero_Manifestacoes']]
    dff = dff.loc[aux,:]
    dff.Numero_Manifestacoes = dff.Numero_Manifestacoes.apply(lambda x: np.ceil(float(x)))

    dff_table = dff_table.merge(dff.groupby('Quem').sum(), left_index=True, right_index=True)

    dff_table.columns = ['Número de participação', 'Percentual de participações em relação ao total', 'Número total de manifestações']

    dff_table['Média de manifestações por participação'] = np.round(dff_table['Número total de manifestações']/dff_table['Número de participação'], 2)

    total_contributions = dff_table['Número total de manifestações'].sum()

    dff_table['Percentual de manifestações em relação ao total'] = np.round(
        dff_table['Número total de manifestações'] / total_contributions*100, 2)

    names_table = ['Contribuidor']
    names_table.extend(list(dff_table.columns))

    dff_table['Contribuidor'] = dff_table.index

    dff_table['Contribuidor'] = dff_table['Contribuidor'].apply(lambda x: x.split('(')[0])

    dff_table = dff_table[names_table]

    names_table = ['<b>'+i+'</b>' for i in names_table]

    rowEvenColor = '#dddddd'
    rowOddColor = '#eeeeee'

    aux_color = []

    dff_table = dff_table.sort_values(['Número total de manifestações', 'Número de participação'], ascending=False)

    if len(dff_table) > 6:
        dff_table = dff_table[0:6]

    for i in range(0,len(dff_table.index)):
        if i%2 == 0:
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
           values = dff_table.values.T,
            line=dict(color='white'),
            fill = dict(
                color=[aux_color]
                ),
            )
        )

    traces.append(trace)

    layout = dict(
        height = 600,
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        zoom=7,
    )

    figure = dict(data=traces, layout = layout)
    return figure

@app.callback(Output('top_participants_deepdive', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'),
               Input('entidade_representativa_options', 'value')])
def update_num_top6_participants_deepdive(agency_value, int_part_value, objective, subject, entidade):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject, entidade)

    dff = dff[['Quem', 'Numero_Manifestacoes', 'Sim_impacto', 'Nao_impacto', 'N/D_impacto','N/A_impacto', 'N/C_impacto']]

    dff_table = dff[['Quem', 'Numero_Manifestacoes']].groupby('Quem').count().sort_values('Numero_Manifestacoes', ascending=False)

    if 'N/D' in dff_table.index:
        dff_table = dff_table.drop('N/D')

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i, 'Numero_Manifestacoes'])]
    dff = dff.loc[aux, :]
    dff.Numero_Manifestacoes = dff.Numero_Manifestacoes.apply(lambda x: np.ceil(float(x)))
    dff = dff.fillna(0)
    dff.Sim_impacto = dff.Sim_impacto.apply(lambda x: np.ceil(float(x)))
    dff.Nao_impacto = dff.Nao_impacto.apply(lambda x: np.ceil(float(x)))
    dff['N/D_impacto'] = dff['N/D_impacto'].apply(lambda x: np.ceil(float(x)))
    dff['N/A_impacto'] = dff['N/A_impacto'].apply(lambda x: np.ceil(float(x)))
    dff['N/C_impacto'] = dff['N/C_impacto'].apply(lambda x: np.ceil(float(x)))

    dff_table = dff_table.merge(dff.groupby('Quem').sum(), left_index=True, right_index=True)

    dff_table['Contribuidor'] = dff_table.index

    dff_table['Contribuidor'] = dff_table['Contribuidor'].apply(lambda x: x.split('(')[0])

    dff_table = dff_table.sort_values(['Numero_Manifestacoes_x', 'Numero_Manifestacoes_y'], ascending=False)

    if len(dff_table) > 6:
        dff_table = dff_table[0:6]

    aux_contribuicoes = ['Sim_impacto', 'Nao_impacto', 'N/D_impacto',
               'N/A_impacto', 'N/C_impacto']

    dff_table[aux_contribuicoes] = dff_table[aux_contribuicoes].apply(lambda x: (x/x.sum())*100, axis = 1)

    aux_dic = {'Sim_impacto': 'Gerou impacto',
               'Nao_impacto': 'Não gerou impacto', 'N/D_impacto': 'Não está disponível',
               'N/A_impacto': 'Recusado por não se aplicar', 'N/C_impacto': 'Não está claro'}

    traces = []

    c = 0

    for i in aux_contribuicoes:

        aux = [str(j) + '%' for j in np.round(dff_table.loc[:, i], 1)]
        aux.reverse()
        x = list(dff_table.loc[:, i])
        x.reverse()
        y = list(dff_table.Contribuidor)
        y.reverse()

        trace = dict(
            type='bar',
            y=y,
            x=x,
            orientation = 'h',
            text=aux,
            textposition='auto',
            name=aux_dic[i],
            marker=dict(
                color=colors_palette[c]
            )
        )

        c = c + 1

        traces.append(trace)

    layout = dict(
        barmode='stack',
        height = 600,
        autosize=True,
        margin=dict(
            l=200,
            r=35,
            b=35,
            t=45
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h', traceorder = 'normal'),
        zoom=7,
    )
    figure = dict(data=traces, layout=layout)
    return figure

@app.callback(Output('network_contributions', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'),
               Input('input_number_min', 'value'),
               Input('entidade_representativa_options', 'value')])
def update_graph(agency_value, int_part_value, objective, subject, input_number, entidade):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject, entidade)

    dff = dff[dff['Quem'] != 'N/D']
    dff = dff[dff['Quem'] != 'N/C']
    dff = dff[dff.Numero_Manifestacoes != 'N/D']
    dff = dff[dff.Numero_Manifestacoes != 'N/C']

    dff.Quem = dff.Quem.apply(lambda x: x.split('(')[0].strip())

    dff['count'] = dff.Quem.apply(lambda x: dff.Quem[dff.Quem == x].count())
    dff['count_size_bonus'] = 1 + dff['count']/dff['count'].max()
    dff = dff[dff['count'] >= float(input_number)]

    dff.Numero_Manifestacoes = dff.Numero_Manifestacoes.apply(lambda x: float(x))

    dff_aux = dff.groupby('Quem').sum()
    dff_aux = dff_aux.fillna(0)
    dff_aux['percent_total_impacto'] = dff_aux.Sim_impacto/dff_aux.Numero_Manifestacoes*100

    dic_nx = {}

    for i in dff.Quem.unique():
        aux_id = dff.ID_Interno[dff.Quem == i]
        aux_list_name = []
        [aux_list_name.extend(dff[dff.ID_Interno == j].Quem.unique()) for j in aux_id]

        aux_list_name = list(set(aux_list_name))
        dic_nx.update({i: aux_list_name})

    G=nx.from_dict_of_lists(dic_nx)
    pos=nx.spring_layout(G, random_state = 1)

    edge_trace = dict(
        type = 'scatter',
        x=[],
        y=[],
        line=dict(width=0.5,color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

    node_trace = dict(
        type = 'scatter',
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
            colorscale='Bluered',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Percentual do quanto o contribuinte impactou',
                xanchor='left',
                titleside='right',
                tickvals = list(range(0,101,10))
            ),
            line=dict(width=2)))

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'].append(x)
        node_trace['y'].append(y)

    node_trace['marker']['size'] = []

    for node, adjacencies in list(G.adjacency()):
        node_trace['marker']['size'].append(20 * dff['count_size_bonus'][dff.Quem == node].max())
        node_trace['marker']['color'].append(dff_aux.loc[node,'percent_total_impacto'])
        node_info = str(node)+' ('+str(len(adjacencies)-1)+' conexões)'
        node_trace['text'].append(node_info)

    node_trace['marker']['color'].append(100)

    node_trace2 = node_trace.copy()

    node_trace2['y'] = [i+j*0.00111 for i,j in zip(node_trace['y'],node_trace['marker']['size'])]
    node_trace2['mode'] = 'text'
    node_trace2['text'] = ['<b>' + i.split('(')[0].strip() + '</b>' for i in node_trace['text']]

    traces = [edge_trace, node_trace,node_trace2]

    layout = dict(
        height=980,
        autosize=True,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
#        annotations=[dict(
#            text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
#            showarrow=False,
#            xref="paper", yref="paper",
#            x=0.005, y=-0.002)],
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))

    figure = dict(data=traces, layout=layout)
    return figure

@app.callback(Output('sankey_contributions', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value')])
def update_sankey(agency_value, int_part_value, objective, subject):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject, 'Todos')

    dff = dff[dff['Quem'] != 'N/D']
    dff = dff[dff['Quem'] != 'N/C']
    dff = dff.drop_duplicates('Quem')

    dff.Entidade_Representativa[dff.Entidade_Representativa == 'Sim'] = 'Entidade representativa'
    dff.Entidade_Representativa[dff.Entidade_Representativa == 'Não'] = 'Outros tipos de entidades'

    aux_array = np.concatenate((dff.Entidade_Representativa.unique(), dff.Categoria_Participante.unique(),dff.Subcategoria_Participante.unique(), dff.Sub_subcategoria_Participante.unique(), dff.Sub_sub_subcategoria_Participante.unique()))

    dic_data = {aux_array[i]:i for i in range(0, len(aux_array)) if str(aux_array[i]) != 'N/D' and str(aux_array[i]) != 'N/C' and str(aux_array[i]) != 'nan'}

    dic_data.keys()
    dff.Categoria_Participante
    list(aux_array)

    source = []
    target = []
    value = []

    for ep in dff.Entidade_Representativa.unique():
        if str(ep) == 'N/D' or str(ep) == 'N/C' or str(ep) == 'nan':
            continue

        dff_ep = dff[dff.Entidade_Representativa == ep]

        for cp in dff_ep.Categoria_Participante.unique():
            if len(dff_ep[dff_ep.Categoria_Participante == cp]) == 0:
                continue

            if str(cp) == 'N/D' or str(cp) == 'N/C' or str(cp) == 'nan':
                continue

            source.append(dic_data[ep])
            target.append(dic_data[cp])

            dff_aux = dff_ep[dff_ep.Categoria_Participante == cp]

            value.append(len(dff_aux))

            for scp in dff_aux.Subcategoria_Participante.unique():
                if len(dff_aux[dff_aux.Subcategoria_Participante == scp]) == 0:
                    continue

                if str(scp) == 'N/D' or str(scp) == 'N/C' or str(scp) == 'nan':
                    continue

                source.append(dic_data[cp])
                target.append(dic_data[scp])

                dff_aux2 = dff_aux[dff_aux.Subcategoria_Participante == scp]

                value.append(len(dff_aux2))

                for sscp in dff_aux2.Sub_subcategoria_Participante.unique():
                    if len(dff[dff.Sub_subcategoria_Participante == sscp]) == 0:
                        continue
                    if str(sscp) == 'N/D' or str(sscp) == 'N/C' or str(sscp) == 'nan':
                        continue

                    source.append(dic_data[scp])
                    target.append(dic_data[sscp])

                    dff_aux3 = dff_aux2[dff_aux2.Sub_subcategoria_Participante == sscp]

                    value.append(len(dff_aux3))

                    for ssscp in dff_aux3.Sub_sub_subcategoria_Participante.unique():
                        if len(dff[dff.Sub_sub_subcategoria_Participante == ssscp]) == 0:
                            continue
                        if str(ssscp) == 'N/D' and str(ssscp) == 'N/C' and str(ssscp) == 'nan':
                            continue

                        source.append(dic_data[sscp])
                        target.append(dic_data[ssscp])

                        dff_aux4 = dff_aux3[dff_aux3.Sub_sub_subcategoria_Participante == ssscp]

                        value.append(len(dff_aux4))

    data_trace = dict(
        type='sankey',
        domain = dict(
          x =  [0,1],
          y =  [0,1]
        ),
        orientation = "h",
        valueformat = ".0f",
        valuesuffix = " Contribuintes",
        node = dict(
          pad = 15,
          thickness = 15,
          line = dict(
            color = "black",
            width = 0.5
          ),
          label =  list(aux_array),
          #color =  data['data'][0]['node']['color']
        ),
        link = dict(
          source =  source,
          target =  target,
          value =  value,
    #      label =  data['data'][0]['link']['label']
      ))

    layout =  dict(
            height = 1040,
        font = dict(
          size = 14
        )
    )

    figure = dict(data=[data_trace], layout=layout)

    return figure

@app.callback(Output('top_contributions_deepdive', 'figure'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value'),
               Input('objective_options', 'value'),
               Input('subject_options', 'value'),
               Input('entidade_representativa_options', 'value')])
def update_num_top6_contributions_deepdive(agency_value, int_part_value, objective, subject, entidade):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = filter_dataframe_objective_subject(dff, objective, subject, entidade)

    dff = dff[['Quem', 'Numero_Manifestacoes', 'Sim_impacto', 'Nao_impacto', 'N/D_impacto','N/A_impacto', 'N/C_impacto']]

    dff_table = dff[['Quem', 'Numero_Manifestacoes']].groupby('Quem').count().sort_values('Numero_Manifestacoes', ascending=False)

    if 'N/D' in dff_table.index:
        dff_table = dff_table.drop('N/D')

    aux = [i for i in dff.index if 'N' not in str(dff.loc[i, 'Numero_Manifestacoes'])]
    dff = dff.loc[aux, :]
    dff.Numero_Manifestacoes = dff.Numero_Manifestacoes.apply(lambda x: np.ceil(float(x)))
    dff = dff.fillna(0)
    dff.Sim_impacto = dff.Sim_impacto.apply(lambda x: np.ceil(float(x)))
    dff.Nao_impacto = dff.Nao_impacto.apply(lambda x: np.ceil(float(x)))
    dff['N/D_impacto'] = dff['N/D_impacto'].apply(lambda x: np.ceil(float(x)))
    dff['N/A_impacto'] = dff['N/A_impacto'].apply(lambda x: np.ceil(float(x)))
    dff['N/C_impacto'] = dff['N/C_impacto'].apply(lambda x: np.ceil(float(x)))

    dff_table = dff_table.merge(dff.groupby('Quem').sum(), left_index=True, right_index=True)

    dff_table['Contribuidor'] = dff_table.index

    dff_table['Contribuidor'] = dff_table['Contribuidor'].apply(lambda x: x.split('(')[0])

    dff_table = dff_table.sort_values(['Numero_Manifestacoes_y', 'Numero_Manifestacoes_x'], ascending=False)

    if len(dff_table) > 6:
        dff_table = dff_table[0:6]

    aux_contribuicoes = ['Sim_impacto', 'Nao_impacto', 'N/D_impacto',
               'N/A_impacto', 'N/C_impacto']

    dff_table[aux_contribuicoes] = dff_table[aux_contribuicoes].apply(lambda x: (x/x.sum())*100, axis = 1)

    aux_dic = {'Sim_impacto': 'Gerou impacto',
               'Nao_impacto': 'Não gerou impacto', 'N/D_impacto': 'Não está disponível',
               'N/A_impacto': 'Recusado por não se aplicar', 'N/C_impacto': 'Não está claro'}

    traces = []

    c = 0

    for i in aux_contribuicoes:

        aux = [str(j) + '%' for j in np.round(dff_table.loc[:, i], 1)]
        aux.reverse()
        x = list(dff_table.loc[:, i])
        x.reverse()
        y = list(dff_table.Contribuidor)
        y.reverse()

        trace = dict(
            type='bar',
            y=y,
            x=x,
            orientation = 'h',
            text=aux,
            textposition='auto',
            name=aux_dic[i],
            marker=dict(
                color=colors_palette[c]
            )
        )

        c = c + 1

        traces.append(trace)

    layout = dict(
        barmode='stack',
        height = 600,
        autosize=True,
        margin=dict(
            l=200,
            r=35,
            b=35,
            t=45
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h', traceorder = 'normal'),
        zoom=7,
    )

    figure = dict(data=traces, layout=layout)
    return figure


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