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

colors_palette = ['#e69f09', '#56b4e9', '#009e73', '#f0e442', '#0072b2', '#d55e00', '#cc79a7', '#000000']

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
            html.H6('Manifestações', style = {'text-align': 'center', 'color': colors['text_n']}),
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
        html.P('Percentual do número de impactos das manifestações por ano e objetivo',
               style={'text-align': 'center'}),

        dcc.Graph(id='contribuicoes_ano_table')
    ], className='ten columns offset-by-one', style={'margin-top': '35'}),

    html.Div([
        html.P('Percentual do número de impactos das manifestações por ano e tema',
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
                min=2010,
                max=2017,
                value=[2010, 2017],
                marks={i: i for i in range(2010, 2018)}
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

@app.callback(Output('num_contribution', 'children'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value')])

def update_num_mecanism(agency_value, int_part_value):

    dff = filter_dataframe(df, agency_value, int_part_value)

    if dff.shape[0] > 0:
        if int_part_value == 'Todos':

            return "Para a agência {}, temos registro das manifestações começando no ano {} " \
                   "e terminando em {}, totalizando {} registros.".format(agency_value, int(np.min(dff.Ano)),
                                                                        int(np.max(dff.Ano)), dff.shape[0])

        else:
            return "Com essa combinação de filtros, para a agência {}, temos registro das manifestações começando no ano {} " \
                   "e terminando em {}, totalizando {} registros, que foram feitos de forma {}.".format(agency_value, int(np.min(dff.Ano)),
                                                                                                       int(np.max(dff.Ano)),dff.shape[0],
                                                                                                       aux_instru_part[int_part_value].lower())
    else:
        return "Não temos registros, sobre a {}, com essas combinações de filtros.".format(agency_value)


@app.callback(Output('my-slider-2', 'value'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value')])
def update_slider(agency_value, int_part_value):
    dff = filter_dataframe(df, agency_value, int_part_value)

    return [dff.Ano.min(),dff.Ano.max()]

@app.callback(Output('my-slider-2', 'marks'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value')])
def update_slider(agency_value, int_part_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    marks = {i:i for i in set(dff.Ano)}
    return marks

@app.callback(Output('my-slider-2', 'min'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value')])
def update_slider(agency_value, int_part_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    return dff.Ano.min()

@app.callback(Output('my-slider-2', 'max'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value')])
def update_slider(agency_value, int_part_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    return dff.Ano.max()

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
        x = ['Ano '+str(i) for i in dff.groupby('Ano').count()['Agência'].index],
        y = (dff.groupby('Ano').count()['Agência'].values/dff.shape[0])*100,
        text = a,
        textposition = 'auto',
        marker = dict(
            color='#5498A5'
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
        titlefont=dict(
            size=21,
            color='rgb(0,0,0)',
        ),
        font=dict(
            color='rgb(0,0,0)'
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
        )
    )

    figure = dict(data=traces, layout = layout)
    return figure

def colors_palettes_function(df, agency_options, columns):

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
              Input('type_year_options', 'value'),])
def make_contribution_time_figure(agency_value, int_part_value, year_options_value):
    dfff = filter_dataframe(df, agency_value, int_part_value)
    dfff = dfff[dfff.Ano.isnull() == False]

    aux_ano = list(dfff.Ano.drop_duplicates().sort_values())
    aux_ano = ['Ano '+str(i) for i in aux_ano]
    aux_ano.append('Geral')

    aux_participante = list(dfff.Categoria_Participante.drop_duplicates().sort_values())

    traces = []

    aux_colors = colors_palettes_function(df,agency_value,'Categoria_Participante')

    for j in aux_participante:

        y = []

        for i in aux_ano:

            if i == 'Geral':
                aux = (dfff.Categoria_Participante[dfff.Categoria_Participante == j].count() / dfff.Categoria_Participante.count()) * 100
                y.append(aux)

            else:
                aux = (dfff.Categoria_Participante[dfff.Categoria_Participante == j][dfff.Ano == int(i.split()[1])].count() / dfff.Categoria_Participante[dfff.Ano == int(i.split()[1])].count()) * 100
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


@app.callback(Output('resposta_contribuicao', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value')])
def make_contribution_time_aceite_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    #dfff = dff[(dff.Ano >= my_slider_value[0]) & (dff.Ano <= my_slider_value[1])]

    dff = dff[dff.Numero_Manifestacoes !='1?']
    dff = dff[dff.Numero_Manifestacoes != 'N/C']
    dff = dff[dff.Numero_Manifestacoes.isnull() == False]
    dff = dff[dff.Ano.isnull() == False]

    aux = [i for i in dff.columns if "Contribuicoes_" in i]

    dff[aux] = dff[aux].fillna('0')
    dff[aux] = dff[aux].apply(pd.to_numeric, errors='coerce')

    aux.append('Ano')

    aux_ano = list(dff.Ano.drop_duplicates().sort_values())
    aux_ano_geral = ['Ano' + str(i) for i in aux_ano]
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
        name = 'Impactou mudanças',
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
        name = 'Não impactou mudanças',
        marker = dict(
            color = colors_palette[2]
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
        name='Não disponível',
        marker = dict(
            color = colors_palette[3]
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
            color = colors_palette[4]
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
            color = colors_palette[5]
        )
    )


    traces.append(trace1)
    traces.append(trace2)
    traces.append(trace3)
    traces.append(trace4)
    traces.append(trace5)
    traces.append(trace6)

    layout = dict(
        barmode='stack',
        autosize=True,
        margin=dict(
            l=200,
            r=35,
            b=35,
            t=45
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        title='Resposta de participantes por ano',
        zoom=7,
    )
    figure = dict(data=traces, layout=layout)
    return figure

@app.callback(Output('resposta_contribuicao_categoria', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              Input('my-slider-2', 'value')])
def make_contribution_time_aceite_figure(agency_value, int_part_value, year_options_value, my_slider_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dff = dff[(dff.Ano >= my_slider_value[0]) & (dff.Ano <= my_slider_value[1])]

    dff = dff[dff.Numero_Manifestacoes !='1?']
    dff = dff[dff.Numero_Manifestacoes != 'N/C']
    dff = dff[dff.Numero_Manifestacoes.isnull() == False]
    dff = dff[dff.Ano.isnull() == False]

    aux = [i for i in dff.columns if "Contribuicoes_" in i]

    dff[aux] = dff[aux].fillna('0')
    dff[aux] = dff[aux].apply(pd.to_numeric, errors='coerce')

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
        name = 'Impactou mudanças',
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
        name = 'Não impactou mudanças',
          text=aux_Nao,
        textposition='auto',
        marker = dict(
            color = colors_palette[2]
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
        name='Não disponível',
      text=aux_ND,
        textposition='auto',
        marker = dict(
            color = colors_palette[3]
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
            color = colors_palette[4]
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
            color = colors_palette[5]
        )
    )

    traces.append(trace1)
    traces.append(trace2)
    traces.append(trace3)
    traces.append(trace4)
    traces.append(trace5)
    traces.append(trace6)

    layout = dict(
        barmode='stack',
        autosize=True,
        margin=dict(
            l=200,
            r=35,
            b=35,
            t=45
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        zoom=7,
    )
    figure = dict(data=traces, layout=layout)
    return figure


@app.callback(Output('resposta_contribuicao_estatal', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),])
def make_contribution_time_aceite_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    #dfff = dff[(dff.Ano >= my_slider_value[0]) & (dff.Ano <= my_slider_value[1])]

    dff = dff[dff.Numero_Manifestacoes !='1?']
    dff = dff[dff.Numero_Manifestacoes != 'N/C']
    dff = dff[dff.Numero_Manifestacoes.isnull() == False]
    dff = dff[dff.Ano.isnull() == False]
    dff = dff[dff.Estatal.isnull() == False]
    dff = dff[dff.Estatal !='?']

    aux = [i for i in dff.columns if "Contribuicoes_" in i]

    dff[aux] = dff[aux].fillna('0')
    dff[aux] = dff[aux].apply(pd.to_numeric, errors='coerce')

    dff.Ano = dff.Ano.apply(lambda x: str(x))

    estatal_ano = list(dff.Estatal.drop_duplicates().sort_values())

    traces = []

    aux_sim = [str(i) + '%' for i in np.round(
        [(dff['Sim_impacto'][(dff.Estatal == i)].sum() / dff.Numero_Manifestacoes[(dff.Estatal == i)].sum()) * 100 for i in
         estatal_ano], 1)]

    trace1 = dict(
        type='bar',
        y=estatal_ano,
        x=[(dff['Sim_impacto'][(dff.Estatal == i)].sum()/dff.Numero_Manifestacoes[(dff.Estatal == i)].sum())*100 for i in estatal_ano],
        orientation = 'h',
        name = 'Impactou mudanças',
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
        name = 'Não impactou mudanças',
      text=aux_Nao,
        textposition='auto',
        marker = dict(
            color = colors_palette[2]
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
        name='Não disponível',
      text=aux_ND,
        textposition='auto',
        marker = dict(
            color = colors_palette[3]
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
            color = colors_palette[4]
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
            color = colors_palette[6]
        )
    )


    traces.append(trace1)
    traces.append(trace2)
    traces.append(trace3)
    traces.append(trace4)
    traces.append(trace5)
    traces.append(trace6)

    layout = dict(
        barmode='stack',
        autosize=True,
        margin=dict(
            l=200,
            r=35,
            b=35,
            t=45
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
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
              Input('type_year_options', 'value'),])
def make_contribution_time_figure(agency_value, year_options_value):
    dfff = filter_dataframe(df, agency_value, 'Todos')
    dfff = dfff[dfff.Ano.isnull() == False]

    aux_ano = list(dfff.Ano.drop_duplicates().sort_values())
    aux_ano = ['Ano '+str(i) for i in aux_ano]
    aux_ano.append('Geral')

    aux_participante = list(dfff.Instrumento_de_Participacao.drop_duplicates().sort_values())

    traces = []

    aux_colors = colors_palettes_function(df,agency_value,'Instrumento_de_Participacao')

    for j in aux_participante:

        y = []

        for i in aux_ano:

            if i == 'Geral':
                aux = (dfff.Instrumento_de_Participacao[dfff.Instrumento_de_Participacao == j].count() / dfff.Instrumento_de_Participacao.count()) * 100
                y.append(aux)

            else:
                aux = (dfff.Instrumento_de_Participacao[dfff.Instrumento_de_Participacao == j][dfff.Ano == int(i.split()[1])].count() / dfff.Instrumento_de_Participacao[dfff.Ano == int(i.split()[1])].count()) * 100
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

@app.callback(Output('contribuicoes_ano_table', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              ])
def make_object_table_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)

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

    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    aux_color = []

    for i in range(0,len(table.index)):
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

@app.callback(Output('contribuicoes_ano_table_subject', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              ])
def make_object_table_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)

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

    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    aux_color = []

    for i in range(0,len(table.index)):
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

@app.callback(Output('top_participants', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              ])
def make_object_table_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)

    size = len(dff.ID_Interno.drop_duplicates())

    dff = dff[['Quem', 'Numero_Manifestacoes']]

    dff_table = dff.groupby('Quem').count().sort_values('Numero_Manifestacoes', ascending=False).drop('N/D')

    dff_table['Percentual de participações em relação ao total'] = np.round((dff_table['Numero_Manifestacoes']/size)*100,2)

    aux = [i for i in dff.index if 'N' not in dff.loc[i,'Numero_Manifestacoes']]
    dff = dff.loc[aux,:]
    dff.Numero_Manifestacoes = dff.Numero_Manifestacoes.apply(lambda x: float(x))

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

    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    aux_color = []

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
              Input('type_year_options', 'value'),
              ])
def make_object_table_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)

    size = len(dff.ID_Interno.drop_duplicates())

    dff = dff[['Quem', 'Numero_Manifestacoes']]

    dff_table = dff.groupby('Quem').count().sort_values('Numero_Manifestacoes', ascending=False).drop('N/D')

    dff_table['Percentual de participações'] = np.round((dff_table['Numero_Manifestacoes']/size)*100,2)

    aux = [i for i in dff.index if 'N' not in dff.loc[i,'Numero_Manifestacoes']]
    dff = dff.loc[aux,:]
    dff.Numero_Manifestacoes = dff.Numero_Manifestacoes.apply(lambda x: float(x))

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

    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    aux_color = []

    dff_table = dff_table.sort_values('Número total de manifestações', ascending=False)

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
              Input('type_year_options', 'value'),
              ])
def make_object_time_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)

    dff = dff[['Quem', 'Numero_Manifestacoes', 'Sim_impacto', 'Nao_impacto', 'N/D_impacto','N/A_impacto', 'N/C_impacto']]

    dff_table = dff[['Quem', 'Numero_Manifestacoes']].groupby('Quem').count().sort_values('Numero_Manifestacoes', ascending=False).drop('N/D')

    aux = [i for i in dff.index if 'N' not in dff.loc[i, 'Numero_Manifestacoes']]
    dff = dff.loc[aux, :]
    dff.Numero_Manifestacoes = dff.Numero_Manifestacoes.apply(lambda x: float(x))

    dff_table = dff_table.merge(dff.groupby('Quem').sum(), left_index=True, right_index=True)

    dff_table['Contribuidor'] = dff_table.index

    dff_table['Contribuidor'] = dff_table['Contribuidor'].apply(lambda x: x.split('(')[0])

    dff_table = dff_table[0:6]

    aux_contribuicoes = ['Sim_impacto', 'Nao_impacto', 'N/D_impacto',
               'N/A_impacto', 'N/C_impacto']

    dff_table[aux_contribuicoes] = dff_table[aux_contribuicoes].apply(lambda x: (x/x.sum())*100, axis = 1)

    aux_dic = {'Sim_impacto': 'Impactou mudanças',
               'Nao_impacto': 'Não impactou mudanças', 'N/D_impacto': 'Não disponível',
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
        autosize=True,
        margin=dict(
            l=200,
            r=35,
            b=35,
            t=45
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        zoom=7,
    )
    figure = dict(data=traces, layout=layout)
    return figure


@app.callback(Output('top_contributions_deepdive', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              ])
def make_object_time_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)

    dff = dff[['Quem', 'Numero_Manifestacoes', 'Sim_impacto', 'Nao_impacto', 'N/D_impacto','N/A_impacto', 'N/C_impacto']]

    dff_table = dff[['Quem', 'Numero_Manifestacoes']].groupby('Quem').count().sort_values('Numero_Manifestacoes', ascending=False).drop('N/D')

    aux = [i for i in dff.index if 'N' not in dff.loc[i, 'Numero_Manifestacoes']]
    dff = dff.loc[aux, :]
    dff.Numero_Manifestacoes = dff.Numero_Manifestacoes.apply(lambda x: float(x))

    dff_table = dff_table.merge(dff.groupby('Quem').sum(), left_index=True, right_index=True)

    dff_table['Contribuidor'] = dff_table.index

    dff_table['Contribuidor'] = dff_table['Contribuidor'].apply(lambda x: x.split('(')[0])

    dff_table = dff_table.sort_values('Numero_Manifestacoes_y', ascending = False)

    dff_table = dff_table[0:6]

    aux_contribuicoes = ['Sim_impacto', 'Nao_impacto', 'N/D_impacto',
               'N/A_impacto', 'N/C_impacto']

    dff_table[aux_contribuicoes] = dff_table[aux_contribuicoes].apply(lambda x: (x/x.sum())*100, axis = 1)

    aux_dic = {'Sim_impacto': 'Impactou mudanças',
               'Nao_impacto': 'Não impactou mudanças', 'N/D_impacto': 'Não disponível',
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
        autosize=True,
        margin=dict(
            l=200,
            r=35,
            b=35,
            t=45
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
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