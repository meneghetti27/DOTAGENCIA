#!/usr/bin/env python3
"""Confere quais vagas já salvas no painel FECHARAM (sumiram da página da empresa).
Uso: python3 vagas/checar.py ids.json  → imprime JSON com a lista de ids encerrados.
ids.json = lista de doc ids do painel (gh-<empresa>-<id>, lever-<empresa>-<uuid>, ashby-<empresa>-<uuid>).
Ids de outras fontes antigas (jobicy-, wwr-, remotive-, wn-, remoteok-, himalayas-) contam como encerrados.
"""
import json, sys, urllib.request, urllib.error
UA = {"User-Agent": "Mozilla/5.0 (job-digest)"}
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r: return json.loads(r.read())
ids = json.load(open(sys.argv[1])); fechadas = []; ashby_cache = {}
for i in ids:
    try:
        tipo, resto = i.split("-", 1)
        if tipo == "gh":
            emp, jid = resto.rsplit("-", 1); get(f"https://boards-api.greenhouse.io/v1/boards/{emp}/jobs/{jid}")
        elif tipo == "lever":
            emp, jid = resto.split("-", 1); get(f"https://api.lever.co/v0/postings/{emp}/{jid}")
        elif tipo == "ashby":
            emp, jid = resto.split("-", 1)
            if emp not in ashby_cache: ashby_cache[emp] = {j["id"] for j in get(f"https://api.ashbyhq.com/posting-api/job-board/{emp}")["jobs"]}
            if jid not in ashby_cache[emp]: fechadas.append(i)
        else: fechadas.append(i)
    except urllib.error.HTTPError as e:
        if e.code == 404: fechadas.append(i)
    except Exception: pass   # erro de rede: não marca como fechada
print(json.dumps(fechadas))
