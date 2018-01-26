import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from datetime import datetime

app = dash.Dash()

df = pd.read_csv('https://docs.google.com/spreadsheets/d/' +
                        '1PKLtiDnd6V9QpHThrt7DyUexLDfuzgglqbNAYwFytwg' +
                        '/export?gid=923758049&format=csv')

df_mecanismo = pd.read_csv('https://docs.google.com/spreadsheets/d/' +
                        '1-9259mXNUjsQKBsZIlUAbRudK87bdQ4j6zWE8e0zGL4' +
                        '/export?gid=805820567&format=csv')

df = pd.merge(df, df_mecanismo[["ID_Interno", "Ano", "Instrumento_de_Participacao", "Objetivo_participacao", "Indexacao_Tema"]], how = 'left', on = "ID_Interno")

df['Agência'] = df['ID_Interno'].apply(lambda x: str(x).split('_')[0])

del df_mecanismo

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
    html.Div([
            html.H2(
                'Regulação em números',
                style = {'text-align': 'center',
                         'color': colors['text']},
            ),
            html.P('Contribuições', style = {'text-align': 'center'}),
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
            ], className = 'eight columns',),

        html.Div([
            html.P('',
                   id='num_contribution',
                   style={'text-align': 'center'},
                   ),
                ], className="three columns", style={'margin-left': 50,'margin-top': 60}),
    ]),
    html.Div([
        html.Div([
            html.Div([

                dcc.Graph(id='category_time'),

                ], className='eleven columns', ),

        ], className='row', ),
        dcc.RangeSlider(
            id='my-slider',
            min=2010,
            max=2017,
            value=[2010, 2017],
            marks={i: i for i in range(2010, 2018)}
        ),
    ], className='six columns', style={'margin-left': 50}),
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

@app.callback(Output('num_contribution', 'children'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value')])

def update_num_mecanism(agency_value, int_part_value):

    dff = filter_dataframe(df, agency_value, int_part_value)

    if dff.shape[0] > 0:
        if int_part_value == 'Todos':

            return "Para a agência {}, temos registro das contribuições começando no ano {} " \
                   "e terminando em {}, totalizando {} registros.".format(agency_value, int(np.min(dff.Ano)),
                                                                        int(np.max(dff.Ano)), dff.shape[0])

        else:
            return "Com essa combinação de filtros, para a agência {}, temos registro das contribuições começando no ano {} " \
                   "e terminando em {}, totalizando {} registros, que foram feitos de forma {}.".format(agency_value, int(np.min(dff.Ano)),
                                                                                                       int(np.max(dff.Ano)),dff.shape[0],
                                                                                                       aux_instru_part[int_part_value].lower())
    else:
        return "Não temos registros, sobre a {}, com essas combinações de filtros.".format(agency_value)

'''
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
'''

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
        title="Percentual de contribuições {}".format(year_options_value.lower()),
        zoom=7,
    )
    figure = dict(data=traces, layout = layout)
    return figure

@app.callback(Output('category_time', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value'),
              Input('my-slider', 'value')])
def make_contribution_time_figure(agency_value, int_part_value, year_options_value, my_slider_value):
    dfff = filter_dataframe(df, agency_value, int_part_value)
    #dfff = dff[(dff.Ano >= my_slider_value[0]) & (dff.Ano <= my_slider_value[1])]

    traces = []
    trace = dict(
        type='bar',
        y=[i for i in dfff.groupby("Categoria_Participante").count()["Agência"].sort_values().index],
        x=(dfff.groupby("Categoria_Participante").count()['Agência'].sort_values().values/dfff.shape[0])*100,
        orientation = 'h'
    )

    traces.append(trace)

    layout = dict(
        autosize=True,
        margin=dict(
            l=200,
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