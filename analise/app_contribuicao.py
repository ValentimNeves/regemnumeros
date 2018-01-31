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
                        '1b4BBTa2ORDhipCI1DIltANBh4tksAfWR53GJtz1U6N8' +
                        '/export?gid=233316896&format=csv')

df_mecanismo = pd.read_csv('https://docs.google.com/spreadsheets/d/' +
                        '1JtF3rZcL7BV9sHtOu1Y2AHi9LA67HDoMgynk05MLRpA' +
                        '/export?gid=1964373741&format=csv')

df = pd.merge(df, df_mecanismo[["ID_Interno", "Ano", "Instrumento_de_Participacao", "Objetivo_participacao", "Indexacao_Tema"]], how = 'left', on = "ID_Interno")

df['Agência'] = df['ID_Interno'].apply(lambda x: str(x).split('_')[0])
df = df[df.Ano.isnull() == False]
df.Ano = df.Ano.apply(lambda x: int(x))

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
    html.Div([
        html.Div([
            dcc.Graph(id='resposta_contribuicao')
        ], className = 'eleven columns')
    ]),
    html.Div([
        html.Div([
            html.Div([
                dcc.Graph(id='resposta_contribuicao_categoria')
            ], className='eleven columns'),
            html.Div([
                dcc.RangeSlider(
                    id='my-slider-2',
                    min=2010,
                    max=2017,
                    value=[2010, 2017],
                    marks={i: i for i in range(2010, 2018)}
                ),
            ], className='six columns', style={'margin-left': 50}),
        ]),
    ]),
    html.Div([
        html.Div([
            dcc.Graph(id='resposta_contribuicao_estatal')
        ], className='eleven columns',),
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


@app.callback(Output('my-slider', 'value'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value')])
def update_slider(agency_value, int_part_value):
    dff = filter_dataframe(df, agency_value, int_part_value)

    return [dff.Ano.min(),dff.Ano.max()]

@app.callback(Output('my-slider-2', 'value'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value')])
def update_slider(agency_value, int_part_value):
    dff = filter_dataframe(df, agency_value, int_part_value)

    return [dff.Ano.min(),dff.Ano.max()]


@app.callback(Output('my-slider', 'marks'),
              [Input('agency_options', 'value'),
               Input('type_part_options', 'value')])
def update_slider(agency_value, int_part_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    marks = {i:i for i in set(dff.Ano)}
    return marks

@app.callback(Output('my-slider-2', 'marks'),
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

@app.callback(Output('my-slider-2', 'min'),
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
    dfff = dfff[dfff.Ano.isnull() == False]
    dfff = dfff[(dfff.Ano >= my_slider_value[0]) & (dfff.Ano <= my_slider_value[1])]

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


@app.callback(Output('resposta_contribuicao', 'figure'),
             [Input('agency_options', 'value'),
              Input('type_part_options', 'value'),
              Input('type_year_options', 'value')])
def make_contribution_time_aceite_figure(agency_value, int_part_value, year_options_value):
    dff = filter_dataframe(df, agency_value, int_part_value)
    #dfff = dff[(dff.Ano >= my_slider_value[0]) & (dff.Ano <= my_slider_value[1])]

    dff = dff[dff.Contribuicoes_Numero !='1?']
    dff = dff[dff.Contribuicoes_Numero != 'N/C']
    dff = dff[dff.Contribuicoes_Numero.isnull() == False]
    dff = dff[dff.Ano.isnull() == False]

    aux = [i for i in dff.columns if "Contribuicoes_" in i]

    dff[aux] = dff[aux].fillna('0')
    dff[aux] = dff[aux].apply(pd.to_numeric, errors='coerce')

    aux.append('Ano')

    aux_ano = list(dff.Ano.drop_duplicates().sort_values())

    traces = []

    trace1 = dict(
        type='bar',
        y=aux_ano,
        x=[(dff['Contribuicoes_Sim'][dff.Ano == i].sum()/dff.Contribuicoes_Numero[dff.Ano == i].sum())*100 for i in aux_ano],
        orientation = 'h',
        name = 'Contribuições aceitas'
    )

    trace2 = dict(
        type='bar',
        y=aux_ano,
        x=[(dff['Contribuicoes_Parcialmente'][dff.Ano == i].sum()/dff.Contribuicoes_Numero[dff.Ano == i].sum())*100 for i in aux_ano],
        orientation = 'h',
        name='Contribuições parcialmente aceitas'
    )

    trace3 = dict(
        type='bar',
        y=aux_ano,
        x=[(dff['Contribuicoes_Nao'][dff.Ano == i].sum()/dff.Contribuicoes_Numero[dff.Ano == i].sum())*100 for i in aux_ano],
        orientation = 'h',
        name = 'Contribuições recusadas'
    )

    trace4 = dict(
        type='bar',
        y=aux_ano,
        x=[(dff['Contribuicoes_N/D'][dff.Ano == i].sum()/dff.Contribuicoes_Numero[dff.Ano == i].sum())*100 for i in aux_ano],
        orientation = 'h',
        name='Não disponível'
    )

    trace5 = dict(
        type='bar',
        y=aux_ano,
        x=[(dff['Contribuicoes_N/A'][dff.Ano == i].sum()/dff.Contribuicoes_Numero[dff.Ano == i].sum())*100 for i in aux_ano],
        orientation = 'h',
        name = 'Recusado por não se aplicar'
    )

    trace6 = dict(
        type='bar',
        y=aux_ano,
        x=[(dff['Contribuicoes_N/C'][dff.Ano == i].sum()/dff.Contribuicoes_Numero[dff.Ano == i].sum())*100 for i in aux_ano],
        orientation = 'h',
        name = 'Não está claro'
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

    dff = dff[dff.Contribuicoes_Numero !='1?']
    dff = dff[dff.Contribuicoes_Numero != 'N/C']
    dff = dff[dff.Contribuicoes_Numero.isnull() == False]
    dff = dff[dff.Ano.isnull() == False]

    aux = [i for i in dff.columns if "Contribuicoes_" in i]

    dff[aux] = dff[aux].fillna('0')
    dff[aux] = dff[aux].apply(pd.to_numeric, errors='coerce')

    aux.append('Ano')

    aux_ano = list(dff.Categoria_Participante.drop_duplicates().sort_values())

    traces = []

    trace1 = dict(
        type='bar',
        y=aux_ano,
        x=[(dff['Contribuicoes_Sim'][dff.Categoria_Participante == i].sum()/dff.Contribuicoes_Numero[dff.Categoria_Participante == i].sum())*100 for i in aux_ano],
        orientation = 'h',
        name = 'Contribuições aceitas'
    )

    trace2 = dict(
        type='bar',
        y=aux_ano,
        x=[(dff['Contribuicoes_Parcialmente'][dff.Categoria_Participante == i].sum()/dff.Contribuicoes_Numero[dff.Categoria_Participante == i].sum())*100 for i in aux_ano],
        orientation = 'h',
        name='Contribuições parcialmente aceitas'
    )

    trace3 = dict(
        type='bar',
        y=aux_ano,
        x=[(dff['Contribuicoes_Nao'][dff.Categoria_Participante == i].sum()/dff.Contribuicoes_Numero[dff.Categoria_Participante == i].sum())*100 for i in aux_ano],
        orientation = 'h',
        name = 'Contribuições recusadas'
    )

    trace4 = dict(
        type='bar',
        y=aux_ano,
        x=[(dff['Contribuicoes_N/D'][dff.Categoria_Participante == i].sum()/dff.Contribuicoes_Numero[dff.Categoria_Participante == i].sum())*100 for i in aux_ano],
        orientation = 'h',
        name='Não disponível'
    )

    trace5 = dict(
        type='bar',
        y=aux_ano,
        x=[(dff['Contribuicoes_N/A'][dff.Categoria_Participante == i].sum()/dff.Contribuicoes_Numero[dff.Categoria_Participante == i].sum())*100 for i in aux_ano],
        orientation = 'h',
        name = 'Recusado por não se aplicar'
    )

    trace6 = dict(
        type='bar',
        y=aux_ano,
        x=[(dff['Contribuicoes_N/C'][dff.Categoria_Participante == i].sum()/dff.Contribuicoes_Numero[dff.Categoria_Participante == i].sum())*100 for i in aux_ano],
        orientation = 'h',
        name = 'Não está claro'
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
        title='Resposta das contribuições por categoria',
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

    dff = dff[dff.Contribuicoes_Numero !='1?']
    dff = dff[dff.Contribuicoes_Numero != 'N/C']
    dff = dff[dff.Contribuicoes_Numero.isnull() == False]
    dff = dff[dff.Ano.isnull() == False]
    dff = dff[dff.Estatal.isnull() == False]
    dff = dff[dff.Estatal !='?']

    aux = [i for i in dff.columns if "Contribuicoes_" in i]

    dff[aux] = dff[aux].fillna('0')
    dff[aux] = dff[aux].apply(pd.to_numeric, errors='coerce')

    dff.Ano = dff.Ano.apply(lambda x: str(x))

    dff['estatal_ano'] = dff.Ano + ", é estatal? " + dff.Estatal

    estatal_ano = list(dff.estatal_ano.drop_duplicates().sort_values())

    traces = []

    trace1 = dict(
        type='bar',
        y=estatal_ano,
        x=[(dff['Contribuicoes_Sim'][(dff.estatal_ano == i)].sum()/dff.Contribuicoes_Numero[(dff.estatal_ano == i)].sum())*100 for i in estatal_ano],
        orientation = 'h',
        name = 'Contribuições aceitas'
    )

    trace2 = dict(
        type='bar',
        y=estatal_ano,
        x=[(dff['Contribuicoes_Parcialmente'][(dff.estatal_ano == i)].sum()/dff.Contribuicoes_Numero[(dff.estatal_ano == i)].sum())*100 for i in estatal_ano],
        orientation = 'h',
        name='Contribuições parcialmente aceitas'
    )

    trace3 = dict(
        type='bar',
        y=estatal_ano,
        x=[(dff['Contribuicoes_Nao'][(dff.estatal_ano == i)].sum()/dff.Contribuicoes_Numero[(dff.estatal_ano == i)].sum())*100 for i in estatal_ano],
        orientation = 'h',
        name = 'Contribuições recusadas'
    )

    trace4 = dict(
        type='bar',
        y=estatal_ano,
        x=[(dff['Contribuicoes_N/D'][(dff.estatal_ano == i)].sum()/dff.Contribuicoes_Numero[(dff.estatal_ano == i)].sum())*100 for i in estatal_ano],
        orientation = 'h',
        name='Não disponível'
    )

    trace5 = dict(
        type='bar',
        y=estatal_ano,
        x=[(dff['Contribuicoes_N/A'][(dff.estatal_ano == i)].sum()/dff.Contribuicoes_Numero[(dff.estatal_ano == i)].sum())*100 for i in estatal_ano],
        orientation = 'h',
        name = 'Recusado por não se aplicar'
    )

    trace6 = dict(
        type='bar',
        y=estatal_ano,
        x=[(dff['Contribuicoes_N/C'][(dff.estatal_ano == i)].sum()/dff.Contribuicoes_Numero[(dff.estatal_ano == i)].sum())*100 for i in estatal_ano],
        orientation = 'h',
        name = 'Não está claro'
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
        title='Resposta das contribuições por ano e tipo de empresa',
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