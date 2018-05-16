from df2gspread import df2gspread as d2g
import pandas as pd

def import_base(agencia):
    '''
    :param agencia: Agency from which we want to export csv

    :return:
    Returns two data frames, one referring to contributions and the other to the participation mechanisms
    '''

    agencia_dic = {'ana': '1Lj9Gz_JBL5h8j339fpcxlf8m6tfLApUNT52vsvw84D0',
                   'ancine': '1ZFpDOLANZwq1smqV49GBpMRQLB_3tbO_xQmyPOn64ug',
                   'bacen': '1VgYH38N1f8UqBjMMRbgKAVPCrcIyStwRBhHPKa716sM',
                   'antaq': '1mKSExdlv7V9OM7OQvjmA68OWUMA5l3n2lhPR5o1Y2r0',
                   'ans': '1dO8VWSK4YDsCuwyyN4SdRmBXKwBEQbrwJweJwmn7q14',
                   'anatel': '1RqaN15c0uE3qRT2egREbXcoUyFr__sQI4wUUkUtvy3k'}

    contribuicoes = pd.read_csv('https://docs.google.com/spreadsheets/d/' +
                                agencia_dic[agencia] +
                                '/export?gid=1665848903&format=csv', encoding = 'utf-8', decimal = ',')


    aux_drop = [i for i in contribuicoes.columns if 'Unnamed' in i]
    contribuicoes = contribuicoes.drop(aux_drop, axis=1)

    mecanismos = pd.read_csv('https://docs.google.com/spreadsheets/d/' +
                                 agencia_dic[agencia] +
                                 '/export?gid=256430091&format=csv', decimal = ',')

    aux_drop = [i for i in mecanismos.columns if 'Unnamed' in i]
    mecanismos = mecanismos.drop(aux_drop, axis=1)

    return contribuicoes, mecanismos

agencias_contribuicoes = pd.DataFrame({})
agencias_mecanismos = pd.DataFrame({})

for i in ['ana','antaq']:
    contribuicoes, mecanismos = import_base(i)

    agencias_contribuicoes = pd.concat([agencias_contribuicoes, contribuicoes])
    agencias_mecanismos = pd.concat([agencias_mecanismos, mecanismos])

    agencias_mecanismos = agencias_mecanismos.reset_index(drop=True)
    agencias_contribuicoes = agencias_contribuicoes.reset_index(drop=True)

def remove_r(x):
    if type(x) == str:
        x = x.replace('\r', '')
        x = x.split()
        x = ' '.join(x)
        return x
    else:
        return x

for i in agencias_mecanismos.columns:
    agencias_mecanismos[i] = agencias_mecanismos[i].apply(lambda x: remove_r(x))

for i in agencias_contribuicoes.columns:
    agencias_contribuicoes[i] = agencias_contribuicoes[i].apply(lambda x: remove_r(x))

agencias_contribuicoes.Numero_Manifestacoes = agencias_contribuicoes.Numero_Manifestacoes.apply(lambda x: str(x).replace(',','.'))

def float_number(x):
    if 'n' not in str(x).lower():
        x = float(x)

    return x

agencias_mecanismos.Quantos_participaram = agencias_mecanismos.Quantos_participaram.apply(lambda x: float_number(x))

spreadsheetId = '1IOvUGadhTcyLYtKY9yriImylhRgHNt6mQH-JcHf-3tU'

d2g.upload(agencias_mecanismos, spreadsheetId, wks_name="mecanismo_participacao")
d2g.upload(agencias_contribuicoes, spreadsheetId, wks_name="contribuicoes")