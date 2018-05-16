import pandas as pd
import numpy as np
import plotly.plotly as py

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

dff = df[df['Agência'] == 'ANTAQ']

dff = dff[dff['Quem'] != 'N/D']
dff = dff[dff['Quem'] != 'N/C']
dff = dff.drop_duplicates('Quem')

dff.Entidade_Representativa[dff.Entidade_Representativa == 'Sim'] = 'Entidade representativa'
dff.Entidade_Representativa[dff.Entidade_Representativa == 'Não'] = 'Entidade não representativa'

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
    autosize = True,
#    width = 1118,
#    height = 772,
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
    font = dict(
      size = 10
    )
)

fig = dict(data=[data_trace], layout=layout)
py.plot(fig, validate = False)
