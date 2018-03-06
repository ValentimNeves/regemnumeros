import urllib.request
import requests

url = 'https://sistemas.anatel.gov.br/SACP/Contribuicoes/ListaConsultasContribuicoes.asp?Tipo=1&Opcao=finalizadas&PaginaAtual=2&Registros=10&cboAno=1999'

res = requests.get(url, verify = False)

res.text

from requests import Request, Session

s = Session()
req = Request('GET', url)

prepped = s.prepare_request(req)

# Merge environment settings into session
resp = s.send(prepped, verify = False)
resp.text

print(resp.status_code)
