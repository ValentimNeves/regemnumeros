import smtplib
import pandas as pd
import numpy as np

df_contribuicao = pd.read_csv('https://docs.google.com/spreadsheets/d/' +
                        '1IOvUGadhTcyLYtKY9yriImylhRgHNt6mQH-JcHf-3tU' +
                        '/export?gid=133444484&format=csv', index_col = 0)

df_mecanismo = pd.read_csv('https://docs.google.com/spreadsheets/d/' +
                        '1IOvUGadhTcyLYtKY9yriImylhRgHNt6mQH-JcHf-3tU' +
                        '/export?gid=0&format=csv', index_col = 0)

df_mecanismo


agencia_email = {'ANA': 'medeiros.biancab@gmail.com',
                 'ANS': 'fernanda.mmartins@fgv.br',
                 'ANATEL': 'nanda.dyma.martins@gmail.com',
                 'ANVISA': 'vincreis@gmail.com',
                 'ANVISA': 'ana.cardoso1@outlook.com.br',
                 'Geral': 'nscsalinas@gmail.com',
                 'ANCINE': 'medeiros.biancab@gmail.com',
                 'CVM': 'arrudadani@gmail.com',
                 'Banco Central': 'arrudadani@gmail.com',
                 'ANTAQ': 'joaobenicioaguiar@gmail.com'}

df_contribuicao['Agência'] = df_contribuicao['ID_Interno'].apply(lambda x: str(x).split('_')[0])

ag = 'ANTAQ'

df_mecanismo = df_mecanismo[df_mecanismo['Agência'] == 'ANTAQ']
df_contribuicao = df_contribuicao[df_contribuicao['Agência'] == 'ANTAQ']

def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header = 'From: %s' % from_addr
    header += 'To: %s' % ', '.join(to_addr_list)
    header += 'Cc: %s' % ', '.join(cc_addr_list)
    header += 'Subject: %s' % subject
    message = header + message

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login, password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()

for ag in agencia_email.keys():

    if ag == 'Geral':
        continue

    df_contribuicao_ag = df_contribuicao[df_contribuicao.Agência == ag]
    df_mecanismo_ag = df_mecanismo[df_mecanismo.Agência == ag]

    if len(df_contribuicao_ag) < 1:
        mensagem = """Olá, 
    Sou o bot do regulação em números. No momento estou em fase de testes e ainda sendo implementado.
    
    Como você ainda está para começar a sua planilha, não tenho o que ajudar."""

    else:

        aux_erro_id_interno = pd.merge(df_mecanismo_ag[['Agência','ID_Interno']][df_mecanismo_ag.Situacao == 'Encerrada'].drop_duplicates(),
                                       df_contribuicao_ag[['Agência','ID_Interno']].drop_duplicates().reset_index(drop=True),
                                       on = 'ID_Interno', how='outer')

        frase_erro_id_interno1 = 'Os seguintes ID internos da aba de contribuição não tem correspôndencia na aba de mecanismos: '
        for i in aux_erro_id_interno.ID_Interno[aux_erro_id_interno.Agência_x != ag]:
            frase_erro_id_interno1 = frase_erro_id_interno1 + '\n {} '
            frase_erro_id_interno1 = frase_erro_id_interno1.format(i)

        frase_erro_id_interno2 = 'Os seguintes ID internos da aba de mecanismo não tem correspôndencia na aba de contribuição: '
        for i in aux_erro_id_interno.ID_Interno[aux_erro_id_interno.Agência_y != ag]:
            frase_erro_id_interno2 = frase_erro_id_interno1 + '\n {} '
            frase_erro_id_interno2 = frase_erro_id_interno1.format(i)


        mensagem = """Olá, 
        Sou o bot do regulação em números. No momento estou em fase de testes e ainda sendo implementado.

        Mas já consigo encontrar alguns erros, só é bom lembrar que se você estiver ainda preenchedo a planilha, pode ser que não sejam erros e sim inconsistências por ainda não ter preenchido tudo.
        De qualquer jeito, segue abaixo a lista do que foi encontrado:
        
        {}
        
        {}
        """.format(frase_erro_id_interno1,frase_erro_id_interno2)

    sendemail(from_addr    = 'BOT regulação em números',
              to_addr_list = agencia_email[ag],
              cc_addr_list = agencia_email['Geral'],
              subject      = 'Atualização sobre erros',
              message      = mensagem,
              login        = 'regemmero@gmail.com',
              password     = 'fgvregulacaoemnumeros2017')

'''
df_contribuicao_num_contribuinte = df_contribuicao_ag.groupby('ID_Interno').count()

aux_erro_num_contribuintes = []

for i in df_contribuicao_num_contribuinte.index:
    if float(df_contribuicao_num_contribuinte.loc[i,'Agência']) == float(df_mecanismo_ag.Quantos_participaram[df_mecanismo_ag.ID_Interno == i]):
        continue
    else:
        aux_erro_num_contribuintes.append('ID interno: {} número na planilha de contribuintes: {} número na planilha de mecanismo: {}'.format(i, df_contribuicao_num_contribuinte.loc[i,'Agência'], df_mecanismo_ag.Quantos_participaram[df_mecanismo_ag.ID_Interno == i]))
'''
