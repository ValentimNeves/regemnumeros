from selenium import webdriver
from selenium.webdriver.firefox.options import Options

fp = webdriver.FirefoxProfile()

fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir", "/home/fexu/Downloads/")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.hal+xml;text/html")
fp.set_preference("pdfjs.disabled", True)

options = Options()
options.set_headless(headless=True)
driver = webdriver.Firefox(firefox_profile=fp, firefox_options=options)

url = 'https://sistemas.anatel.gov.br/SACP/Contribuicoes/ListaConsultasContribuicoes.asp?Tipo=1&Opcao=finalizadas&PaginaAtual=38&Registros=10&cboAno=1999'
driver.get(url)

print("Headless Firefox Initialized")

page_html = driver.page_source

no_content = True

while no_content == True:

    if 'Please enable JavaScript to view the page content' in page_html:
        driver.get(url)
        page_html = driver.page_source

    else:
        no_content = False

numero_paginas = page_html.split('consulta(s) encontrada(s)')[1].split('Clique nos links para navegar')[0]
numero_paginas = [i for i in numero_paginas.split() if i.isnumeric()]
numero_paginas = range(int(numero_paginas[0]), int(numero_paginas[1])+1)

page_html_aux = page_html.lower()

numero_consultas = page_html_aux.split('consulta(s) encontrada(s)')[1].split('Clique nos links para navegar')[0]

url_download_sem_comentario = 'https://sistemas.anatel.gov.br/SACP/Relatorios/carregar.asp?pExpTipo=T&pCodContri=0&pCodProcesso=CP202&pCodTipoProcesso=1&pTipoRelatorio=1'
url_download_com_comentario = 'https://sistemas.anatel.gov.br/SACP/Relatorios/carregar.asp?pExpTipo=T&pCodContri=0&pCodProcesso=CP0&pCodTipoProcesso=1&pTipoRelatorio=2'

driver.get(url_download_sem_comentario)
driver.get(url_download_com_comentario)


from bs4 import BeautifulSoup as bfs


soup = bfs(test, 'html.parser')
soup.find_all("a")

test = [i for i in a.text.split() if 'tipo'.lower() in i.lower()]

bfs_a = bfs(test)

bfs_a

req = Request('GET', url)

prepped = s.prepare_request(req)

# Merge environment settings into session
resp = s.send(prepped, verify = False)
resp.text

print(resp.status_code)

os.c

import sys
sys.path.append('captura')

import pdftotext

test_pdf = pdftotext.extract_text_from_pdf('captura/sample/Rel_Relatório_de_Contribuições_Recebidas_com_Comentários_da_Anatel_cp202_2018514154330.pdf')
test_pdf = pdftotext.extract_text_from_pdf('captura/sample/Rel_Relatório_de_Contribuições_Recebidas_cp201_2018514154345.pdf')

'''Campos para extrair:
    ID da Contribuição: Número
    Autor da Contribuição: Nome
    Empresa: Nome
    Contribuição: Texto corrido
    Justificativa: Texto corrido
    Data: data
    Comentário: Texto corrido resposta ANATEL
'''

import pandas as pd
import numpy as np
from itertools import chain
from difflib import SequenceMatcher

test_pdf = test_pdf.replace('\x0c', '')

aux_id = test_pdf.split('ID da Contribuição:')
aux_id = aux_id[1:]
aux_id = [i.split()[0].strip() for i in aux_id]

aux_autor = test_pdf.split('Autor da Contribuição:')
aux_autor = aux_autor[1:]
aux_autor = [i.split('Empresa:')[0].strip() for i in aux_autor]

aux_empresa = test_pdf.split('Empresa:')
aux_empresa = aux_empresa[1:]
aux_empresa = [i.split('Contribuição:')[0].strip() for i in aux_empresa]

aux_contribuicao = test_pdf.split('Empresa:')
aux_contribuicao = aux_contribuicao[1:]
aux_contribuicao = [i.split('Contribuição:')[1] for i in aux_contribuicao]
aux_contribuicao = [i.split('Justificativa:')[0].strip() for i in aux_contribuicao]

aux_justificativa = test_pdf.split('Empresa:')
aux_justificativa = aux_justificativa[1:]
aux_justificativa = [i.split('Justificativa:')[1] for i in aux_justificativa]
aux_justificativa = [i.split('Comentário da Anatel')[0].strip() for i in aux_justificativa]

aux_data = test_pdf.split('Data:')
aux_data = aux_data[2:]
aux_data = [i.split('Comentário:')[0] for i in aux_data]

aux_comentario = test_pdf.split('Comentário da Anatel')
aux_comentario = aux_comentario[1:]
aux_comentario = [i.split('ID da Contribuição:')[0] for i in aux_comentario]
aux_comentario = [i.split('Comentário:')[1] for i in aux_comentario]
aux_comentario = [i.split('Item:')[0].strip() for i in aux_comentario]

aux_item = test_pdf.split('Item:')
aux_item = aux_item[1:]
aux_item_ids_count = [len(i.split('ID da Contribuição:'))-1 for i in aux_item]
aux_item = [i.split('ID da Contribuição:')[0].strip() for i in aux_item]
aux_item = [list(np.repeat(i,j)) for i,j in zip(aux_item, aux_item_ids_count)]
aux_item = list(chain.from_iterable(aux_item))


df = pd.DataFrame({'ID_interno': list(np.repeat('id', len(aux_id))), 'ID_contribuicao': aux_id,
                   'PF_vinculado': aux_autor, 'Quem': aux_empresa, 'Item': aux_item, 'Contribuição': aux_contribuicao,
                   'Justificativa': aux_justificativa, 'Data': aux_data, 'comentario ANATEL': aux_comentario})

df = df[['ID_interno', 'ID_contribuicao', 'PF_vinculado', 'Quem', 'Item', 'Contribuição',
        'Justificativa', 'Data','comentario ANATEL']]

SequenceMatcher(None, df['Contribuição'][100], df['Contribuição'][101]).ratio()

df.to_excel('test.xlsx', index=False)
