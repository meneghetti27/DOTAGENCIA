#!/usr/bin/env python3
"""Confere quais vagas já salvas no painel FECHARAM (sumiram da página da empresa ou da fonte).
Uso: python3 vagas/checar.py ids.json  → imprime JSON com a lista de ids encerrados.
ids.json = lista de doc ids do painel. Tipos: gh-, lever-, ashby- (ATS), li-<id> e manual-<id numérico> (LinkedIn),
trampos-<id>, remotar-<id>. Ids de fontes antigas reprovadas (jobicy-, wwr-, remoteok-, wn-) contam como encerrados.
manual- sem número e himalayas- só fecham se o link der 404 (não dá pra saber de outro jeito).
Erro de rede/limite nunca marca como fechada.
"""
import json, re, sys, time, urllib.request, urllib.error
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
def abre(url, js=True):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        b = r.read().decode("utf-8", "replace"); return json.loads(b) if js else b
ids = json.load(open(sys.argv[1])); fechadas = []; ashby_cache = {}
for i in ids:
    try:
        tipo, resto = i.split("-", 1)
        if tipo == "gh":
            emp, jid = resto.rsplit("-", 1); abre(f"https://boards-api.greenhouse.io/v1/boards/{emp}/jobs/{jid}")
        elif tipo == "lever":
            emp, jid = resto.split("-", 1); abre(f"https://api.lever.co/v0/postings/{emp}/{jid}")
        elif tipo == "ashby":
            emp, jid = resto.split("-", 1)
            if emp not in ashby_cache: ashby_cache[emp] = {j["id"] for j in abre(f"https://api.ashbyhq.com/posting-api/job-board/{emp}")["jobs"]}
            if jid not in ashby_cache[emp]: fechadas.append(i)
        elif tipo in ("li", "manual") and resto.isdigit():
            h = abre(f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{resto}", js=False); time.sleep(1)
            if re.search(r"No longer accepting applications|Não aceita mais candidaturas", h): fechadas.append(i)
        elif tipo == "trampos":
            o = abre(f"https://trampos.co/api/v2/opportunities/{resto}").get("opportunity") or {}
            if not o or o.get("expired") or o.get("closed"): fechadas.append(i)
        elif tipo == "remotar":
            d = abre(f"https://api.remotar.com.br/jobs/{resto}")
            j = d.get("data", d) if isinstance(d, dict) else {}
            if j.get("expired") or j.get("active") is False: fechadas.append(i)
        elif tipo in ("manual", "himalayas"):
            pass
        else: fechadas.append(i)
    except urllib.error.HTTPError as e:
        if e.code in (404, 410): fechadas.append(i)
    except Exception: pass   # erro de rede: não marca como fechada
print(json.dumps(fechadas))
