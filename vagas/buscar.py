#!/usr/bin/env python3
"""Busca vagas de design ABERTAS AGORA direto nas páginas de vaga das empresas (Greenhouse, Lever, Ashby).

Por que assim (pedido do dono, 19/11/2026): agregadores traziam vaga velha, link quebrado, cadastro obrigatório
e entrevista com robô. As APIs públicas dessas plataformas só listam vaga aberta, e a candidatura é UM formulário
(nome, e-mail, PDF, carta), sem criar conta.

Uso: python3 vagas/buscar.py [vistos.json] > novas.json
"""
import json, os, re, sys, html, time, urllib.request, concurrent.futures as cf
from datetime import datetime, timezone, timedelta

AQUI = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (job-digest)"}
MAX_DIAS = 21          # publicada há no máximo 21 dias (e ainda aberta, senão nem aparece na API)
MAX_DIAS_AGREG = 3     # agregador (Himalayas): só vaga de até 3 dias

DESIGN = re.compile(r"design|designer|\bui\b|\bux\b|brand|art director|creative|motion|graphic|visual|illustrat|"
                    r"animator|animation|video editor|video producer|content creator|social media|generative|"
                    r"\bai artist|3d artist|webflow|framer|diseñ", re.I)
FORA = re.compile(r"engineer|developer|devops|sales|account exec|recruit|accountant|data scien|backend|full.?stack|"
                  r"\bqa\b|tester|support|success|counsel|legal|finance|analyst|researcher|regulatory|\bbim\b|silicon|civil|"
                  r"level design|game design|operations|resource manager|marketing manager|intern\b", re.I)
SENIOR_DEMAIS = re.compile(r"\b(vp|vice president|head of|director|principal|staff)\b", re.I)
RUIM = re.compile(r"crypto|casino|gambl|betting|\bbet\b|adult|onlyfans|nsfw|web3|blockchain", re.I)
SIMPLES = {"boards.greenhouse.io": "Greenhouse", "job-boards.greenhouse.io": "Greenhouse", "jobs.lever.co": "Lever",
           "jobs.ashbyhq.com": "Ashby"}

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return json.loads(r.read().decode("utf-8", "replace"))

def limpa(s, n=3500):
    s = html.unescape(html.unescape(s or ""))
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s).strip()[:n]

def data(s):
    if not s: return None
    try:
        if isinstance(s, (int, float)): return datetime.fromtimestamp(s / 1000 if s > 1e11 else s, timezone.utc)
        d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except Exception: return None

def remoto(txt):
    return bool(re.search(r"remote|anywhere|worldwide|latam|latin america|americas|remoto", txt or "", re.I))

def greenhouse(s):
    for j in get(f"https://boards-api.greenhouse.io/v1/boards/{s}/jobs?content=true")["jobs"]:
        local = (j.get("location") or {}).get("name", "")
        yield dict(id=f"gh-{s}-{j['id']}", plataforma="Greenhouse", titulo=j["title"], empresa=j.get("company_name") or s,
                   url=j["absolute_url"], link_aplicar=j["absolute_url"] + "#app", local=local, remoto=remoto(local),
                   data=j.get("first_published") or j.get("updated_at"), descricao=j.get("content"), tipo="")

def lever(s):
    for j in get(f"https://api.lever.co/v0/postings/{s}?mode=json"):
        c = j.get("categories") or {}
        local = ", ".join(filter(None, [c.get("location"), *(c.get("allLocations") or [])]))
        yield dict(id=f"lever-{s}-{j['id']}", plataforma="Lever", titulo=j["text"], empresa=s.capitalize(), url=j["hostedUrl"],
                   link_aplicar=j.get("applyUrl") or j["hostedUrl"] + "/apply", local=local,
                   remoto=j.get("workplaceType") == "remote" or remoto(local), data=j.get("createdAt"),
                   descricao=(j.get("descriptionPlain") or "") + " " + (j.get("additionalPlain") or ""), tipo=c.get("commitment", ""))

def ashby(s):
    for j in get(f"https://api.ashbyhq.com/posting-api/job-board/{s}?includeCompensation=true")["jobs"]:
        if j.get("isListed") is False: continue
        locs = [j.get("location", "")] + [x.get("location", "") for x in (j.get("secondaryLocations") or [])]
        sal = ((j.get("compensation") or {}).get("compensationTierSummary")) or ""
        yield dict(id=f"ashby-{s}-{j['id']}", plataforma="Ashby", titulo=j["title"], empresa=s.capitalize(), url=j["jobUrl"],
                   link_aplicar=j.get("applyUrl") or j["jobUrl"] + "/application", local=", ".join(filter(None, locs)),
                   remoto=j.get("workplaceType") == "Remote" or remoto(" ".join(locs)),
                   data=j.get("publishedAt"), descricao=j.get("descriptionPlain"), tipo=j.get("employmentType", ""), salario=sal)

def himalayas():
    for j in get("https://himalayas.app/jobs/api?limit=100")["jobs"]:
        link = j.get("applicationLink") or ""
        host = re.sub(r"^https?://([^/]+).*", r"\1", link)
        if host not in SIMPLES: continue           # só se a candidatura cai num formulário simples
        cats = " ".join((j.get("categories") or []) + (j.get("parentCategories") or []))
        if not re.search(r"design|creative|art|video|motion", cats, re.I): continue
        sal = ""
        if j.get("minSalary"): sal = f"{j.get('currency') or ''} {j['minSalary']}–{j.get('maxSalary') or '?'}/{j.get('salaryPeriod') or ''}"
        yield dict(id="himalayas-" + link.rstrip("/").split("/")[-1], plataforma=SIMPLES[host], titulo=j["title"],
                   empresa=j.get("companyName", ""), url=link, link_aplicar=link,
                   local=", ".join(j.get("locationRestrictions") or []) or "Worldwide", remoto=True,
                   data=j.get("pubDate"), descricao=j.get("description"), tipo=j.get("employmentType", ""), salario=sal, agregador=True)

def main():
    vistos = set(json.load(open(sys.argv[1]))) if len(sys.argv) > 1 and os.path.exists(sys.argv[1]) else set()
    emp = json.load(open(os.path.join(AQUI, "empresas.json")))
    agora = datetime.now(timezone.utc)
    tarefas = [(greenhouse, s) for s in emp["greenhouse"]] + [(lever, s) for s in emp["lever"]] + [(ashby, s) for s in emp["ashby"]]
    brutas, erros = [], []
    def roda(t):
        f, s = t
        try: return list(f(s))
        except Exception as e: erros.append(f"{f.__name__}/{s}: {e}"); return []
    with cf.ThreadPoolExecutor(16) as ex:
        for r in ex.map(roda, tarefas): brutas += r
    try: brutas += list(himalayas())
    except Exception as e: erros.append(f"himalayas: {e}")

    out, ids = [], set()
    for v in brutas:
        if v["id"] in vistos or v["id"] in ids: continue
        t = v["titulo"] or ""
        if not DESIGN.search(t) or FORA.search(t) or SENIOR_DEMAIS.search(t): continue
        if not v.get("remoto"): continue
        desc = limpa(v.get("descricao"))
        if RUIM.search(t + " " + v["empresa"] + " " + desc[:800]): continue
        d = data(v.get("data"))
        lim = MAX_DIAS_AGREG if v.get("agregador") else MAX_DIAS
        if not d or d < agora - timedelta(days=lim): continue
        ids.add(v["id"])
        v.update(data=d.isoformat(), descricao=desc, salario=v.get("salario", ""), fonte=v["empresa"] + " · " + v["plataforma"],
                 como_aplicar=f"Formulário único no {v['plataforma']}, sem cadastro (nome, e-mail, PDF, carta)")
        v.pop("agregador", None)
        out.append(v)
    out.sort(key=lambda v: v["data"], reverse=True)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
    for e in erros[:20]: print("AVISO", e, file=sys.stderr)
    print(f"{len(out)} vagas novas de {len(brutas)} lidas em {len(tarefas)} empresas", file=sys.stderr)

if __name__ == "__main__":
    main()
