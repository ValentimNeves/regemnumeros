import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

app = dash.Dash()

df = pd.read_csv('https://docs.google.com/spreadsheets/d/' +
                        '12R7AF3WblBYtqHys3EJpIBgO3J9MUUPE0C2PEE5raPc' +
                        '/export?gid=921256247&format=csv')

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

colors = {
    'background': '#FFFFFF',
    'background2': '#004D85',
    'text': '#000000'
}


app.layout = html.Div(style={'background-color': colors['background']}, children=[
    html.Div(
        [
            html.H2(
                'Regulação em números',
                style = {'text-align': 'center',
                         'color': colors['text']},
            ),
        ],
        className='row'
    ),
    html.Hr(style={'margin': '0', 'margin-bottom': '5'}),

    html.Div([
        html.Div([
            html.Div([

                html.P('Escolha uma agência reguladora:'),

                dcc.Dropdown(
                    id='agency_options',
                    options=agency_options,
                    value='ANA',
                        ),],
                className='two columns', style ={'float': 'left'},
                ),

            html.Div([
                html.P('Escolha um instrumento de participação:'),

                dcc.Dropdown(
                    id='type_part_options',
                    options=type_part_options,
                    value='Todos',
                ),],
                className='two columns', style ={'float': 'left'},
                ),

            html.Div([
                html.P('Escolha como deve ser feita a divisão temporal:'),

                dcc.Dropdown(
                    id='type_year_options',
                    options=type_year_options,
                    value='Por ano',
                ),],
            className='three columns', style ={'float': 'left'},
            ),
        ],
        className='row', style={'margin-top': '20'},
        ),
    ]),

    html.Div([
        html.Div([

            dcc.Graph(id='contribution_time'),
            ], className = 'five columns',
            ),
            html.Div([
                html.P('',
                        id='num_mecanism',
                        style = {'text-align': 'center'},
                        ),
                html.Div([
                    html.Div([
                        html.Div([
                    dcc.Graph(id='object_time'),], className = 'six columns',),
                        html.Div([
                    dcc.Graph(id='subject_time'),], className = 'six columns',),

                    ], className = 'row',),
                    dcc.RangeSlider(
                        id='my-slider',
                        min=2010,
                        max=2017,
                        value=[2010, 2017],
                        marks={i:i for i in range(2010,2018)}
                    ),
                ], className = 'row',),
            ], className = 'six columns', style={'margin-top': '20'}),
        ],
        className='row',
        ),

    html.Div([
        html.Div([
            html.P('Escolha um objetivo:'),

            dcc.Dropdown(
                id='objective_options',
                options=objective_options,
                value='Todos',
            ), ],
            className='two columns', style={'float': 'left'},
        ),

        html.Div([
            html.P('Escolha um tema:'),

            dcc.Dropdown(
                id='subject_options',
                options=subject_options,
                value='Todos',
            ), ],
            className='three columns', style={'float': 'left'},
        ),
    ],
        className='row', style={'margin-top': '20'},
    ),

    html.Div([
        html.Div([
            html.Div([
                dcc.Graph(id='mean_time_preparation')
            ],
                className = 'six columns' ),
            html.Div([
                dcc.Graph(id='mean_time_answer')
            ],
                className = 'six columns')
        ],
            className = 'row' ),
        html.Div([
            html.Div([
                dcc.Graph(id='mean_time_type1')
            ],
                className = 'six columns'),
            html.Div([
                dcc.Graph(id='mean_time_type2')
            ],
                className = 'six columns')
        ],
            className = 'row columns'),
    ])
])

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

@app.callback(Output('my-slider', 'value'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value')])
def update_slider(agency_value, int_part_value):
    dff = filter_dataframe(df, agency_value, int_part_value)

    return [dff.Ano.min(),dff.Ano.max()]

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


@app.callback(Output('my-slider', 'marks'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value')])
def update_slider(agency_value, int_part_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    marks = {i:i for i in set(dff.Ano)}
    return marks


@app.callback(Output('my-slider', 'min'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value')])
def update_slider(agency_value, int_part_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    return dff.Ano.min()


@app.callback(Output('my-slider', 'max'),
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

    traces = []
    trace = dict(
        type='bar',
        x = [str(i) for i in dff.groupby('Ano').count()['Agência'].index],
        y = (dff.groupby('Ano').count()['Agência'].values/dff.shape[0])*100
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
        title="Percentual de mercanismos de participação {}".format(year_options_value.lower()),
        zoom=7,
    )
    figure = dict(data=traces, layout = layout)
    return figure

@app.callback(Output('object_time', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              Input('my-slider', 'value')])
def make_object_time_figure(agency_value, int_part_value, year_options_value, my_slider_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dfff = dff[(dff.Ano >= my_slider_value[0]) & (dff.Ano <= my_slider_value[1])]

    traces = []
    trace = dict(
        type='pie',
        labels=dfff.groupby("Objetivo_participacao").count()["Agência"].index,
        values=dfff.groupby("Objetivo_participacao").count()['Agência'].values,
        name='Objetivos',
        text=dfff.groupby("Objetivo_participacao").count()["Agência"].index,  # noqa: E501
        hoverinfo="value+percent",
        textinfo="percent",
        hole = 0.5,
        )

    traces.append(trace)

    layout = dict(
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=45
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        title='Objetivos',
        zoom=7,
    )
    figure = dict(data=traces, layout=layout)
    return figure

@app.callback(Output('mean_time_preparation', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              Input('my-slider', 'value')])
def make_object_time_figure(agency_value, int_part_value, year_options_value, my_slider_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    dfff = dff[(dff.Ano >= my_slider_value[0]) & (dff.Ano <= my_slider_value[1])]

    traces = []
    trace = dict(
        type='pie',
        labels=dfff.groupby("Indexacao_Tema").count()["Agência"].index,
        values=dfff.groupby("Indexacao_Tema").count()['Agência'].values,
        name='Tema',
        text=dfff.groupby("Indexacao_Tema").count()["Agência"].index,  # noqa: E501
        hoverinfo="value+percent",
        textinfo="percent",
        hole = 0.5,
        )

    traces.append(trace)

    layout = dict(
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=45
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        title='Temas',
        zoom=7,
    )
    figure = dict(data=traces, layout=layout)
    return figure


@app.callback(Output('subject_time', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              Input('objective_options', 'value'),
              Input('subject_options', 'value')])
def make_object_time_figure(agency_value, int_part_value, year_options_value, objective_type, objective_type):
    dff = filter_dataframe_objective_subject(df, agency_value, int_part_value, objective_type, objective_type)

    traces = []
    trace = dict(
        type='pie',
        labels=dfff.groupby("Indexacao_Tema").count()["Agência"].index,
        values=dfff.groupby("Indexacao_Tema").count()['Agência'].values,
        name='Tema',
        text=dfff.groupby("Indexacao_Tema").count()["Agência"].index,  # noqa: E501
        hoverinfo="value+percent",
        textinfo="percent",
        hole = 0.5,
        )

    traces.append(trace)

    layout = dict(
        autosize=True,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=45
        ),
        hovermode="closest",
        legend=dict(font=dict(size=10), orientation='h'),
        title='Temas',
        zoom=7,
    )
    figure = dict(data=traces, layout=layout)
    return figure


app.css.append_css({"external_url": "https://codepen.io/JoaoCarabetta/pen/RjzpPB.css"})

'''
external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/5047eb29e4afe01b45b27b1d2f7deda2a942311a/goldman-sachs-report.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
               "https://cdn.rawgit.com/plotly/dash-app-stylesheets/a3401de132a6d0b652ba11548736b1d1e80aa10d/dash-goldman-sachs-report-js.js"]

for js in external_js:
    app.scripts.append_script({"external_url": js})
'''

if __name__ == '__main__':
    app.run_server(debug=True)