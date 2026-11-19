#!/usr/bin/env python3
"""Busca vagas remotas/gringas de design em várias fontes abertas e devolve as novas em JSON.

Uso: python3 vagas/buscar.py [vistos.json] > novas.json
  vistos.json = lista de ids já vistos (opcional). Saída: lista de vagas novas, já pré-filtradas.
"""
import json, re, sys, html, time, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

UA = {"User-Agent": "Mozilla/5.0 (job-digest)"}
MAX_DIAS = 10

def get(url, txt=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        b = r.read().decode("utf-8", "replace")
    return b if txt else json.loads(b)

def limpa(s, n=1800):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    return re.sub(r"\s+", " ", s).strip()[:n]

def data(s):
    if not s: return None
    try:
        if isinstance(s, (int, float)): return datetime.fromtimestamp(s, timezone.utc)
        s = s.replace("Z", "+00:00")
        try: return datetime.fromisoformat(s)
        except ValueError: return datetime.strptime(s, "%a, %d %b %Y %H:%M:%S %z")
    except Exception: return None

DESIGN = re.compile(r"design|designer|\bui\b|\bux\b|brand|art director|creative|motion|graphic|visual|illustrat|"
                    r"animator|animation|video editor|editor de v|content creator|social media|generative|\bai artist|"
                    r"prompt|3d artist|webflow|framer|diseñ", re.I)
FORA = re.compile(r"engineer|developer|devops|sales|account exec|recruit|accountant|nurse|driver|"
                  r"data scien|backend|full.?stack|qa |tester|support rep|customer success", re.I)
RUIM = re.compile(r"crypto|casino|gambl|betting|\bbet\b|adult|onlyfans|nsfw", re.I)

def remotive():
    for j in get("https://remotive.com/api/remote-jobs?category=design")["jobs"]:
        yield dict(id="remotive-%s" % j["id"], fonte="Remotive", titulo=j["title"], empresa=j["company_name"],
                   url=j["url"], local=j.get("candidate_required_location") or "", salario=j.get("salary") or "",
                   tipo=j.get("job_type") or "", data=j.get("publication_date"), tags=j.get("tags") or [],
                   descricao=j.get("description"))

def remoteok():
    for j in get("https://remoteok.com/api?tag=design")[1:]:
        sal = ""
        if j.get("salary_min"): sal = "US$ %s–%s/ano" % (j.get("salary_min"), j.get("salary_max") or "?")
        yield dict(id="remoteok-%s" % j["id"], fonte="Remote OK", titulo=j.get("position", ""), empresa=j.get("company", ""),
                   url=j.get("url") or "https://remoteok.com/remote-jobs/%s" % j.get("slug"), local=j.get("location") or "",
                   salario=sal, tipo="", data=j.get("date"), tags=j.get("tags") or [], descricao=j.get("description"))

def wwr():
    for feed in ["remote-design-jobs", "remote-full-stack-programming-jobs"][:1]:
        root = ET.fromstring(get("https://weworkremotely.com/categories/%s.rss" % feed, txt=True))
        for it in root.iter("item"):
            t = it.findtext("title") or ""
            emp, _, tit = t.partition(": ")
            link = it.findtext("link") or ""
            yield dict(id="wwr-" + link.rstrip("/").split("/")[-1], fonte="We Work Remotely", titulo=tit or t, empresa=emp,
                       url=link, local=it.findtext("region") or "", salario="", tipo=it.findtext("type") or "",
                       data=it.findtext("pubDate"), tags=[], descricao=it.findtext("description"))

def jobicy():
    for j in get("https://jobicy.com/api/v2/remote-jobs?count=50&industry=design-multimedia")["jobs"]:
        sal = ""
        if j.get("salaryMin"): sal = "%s %s–%s/%s" % (j.get("salaryCurrency", ""), j.get("salaryMin"), j.get("salaryMax", "?"), j.get("salaryPeriod", ""))
        yield dict(id="jobicy-%s" % j["id"], fonte="Jobicy", titulo=j["jobTitle"], empresa=j["companyName"], url=j["url"],
                   local=j.get("jobGeo") or "", salario=sal, tipo=", ".join(j.get("jobType") or []), data=j.get("pubDate"),
                   tags=j.get("jobIndustry") or [], descricao=j.get("jobDescription"))

def workingnomads():
    for j in get("https://www.workingnomads.com/api/exposed_jobs/"):
        yield dict(id="wn-" + j["url"].rstrip("/").split("/")[-1], fonte="Working Nomads", titulo=j["title"],
                   empresa=j["company_name"], url=j["url"], local=j.get("location") or "", salario="", tipo="",
                   data=j.get("pub_date"), tags=(j.get("tags") or "").split(",") if isinstance(j.get("tags"), str) else (j.get("tags") or []),
                   descricao=j.get("description"))

def himalayas():
    for j in get("https://himalayas.app/jobs/api?limit=100")["jobs"]:
        cats = " ".join((j.get("categories") or []) + (j.get("parentCategories") or []))
        if not re.search(r"design|creative|art|video|motion", cats, re.I): continue
        sal = ""
        if j.get("minSalary"): sal = "%s %s–%s/%s" % (j.get("currency") or "", j["minSalary"], j.get("maxSalary") or "?", j.get("salaryPeriod") or "")
        yield dict(id="himalayas-" + (j.get("guid") or j.get("applicationLink") or j["title"]).rstrip("/").split("/")[-1],
                   fonte="Himalayas", titulo=j["title"], empresa=j.get("companyName", ""), url=j.get("applicationLink") or "",
                   local=", ".join(j.get("locationRestrictions") or []) or "Worldwide", salario=sal,
                   tipo=j.get("employmentType") or "", data=j.get("pubDate"), tags=j.get("categories") or [], descricao=j.get("description"))

def main():
    vistos = set(json.load(open(sys.argv[1]))) if len(sys.argv) > 1 else set()
    limite = datetime.now(timezone.utc) - timedelta(days=MAX_DIAS)
    out, erros, ids = [], [], set()
    for f in (remotive, remoteok, wwr, jobicy, workingnomads, himalayas):
        try:
            for v in f():
                if v["id"] in vistos or v["id"] in ids: continue
                ids.add(v["id"])
                titulo = v["titulo"] or ""
                if not DESIGN.search(titulo) or (FORA.search(titulo) and not re.search(r"design", titulo, re.I)): continue
                if RUIM.search(titulo + " " + v["empresa"] + " " + limpa(v["descricao"], 600)): continue
                d = data(v["data"])
                if d and d.tzinfo is None: d = d.replace(tzinfo=timezone.utc)
                if d and d < limite: continue
                v["data"] = d.isoformat() if d else ""
                v["descricao"] = limpa(v["descricao"])
                v["tags"] = [t.strip() for t in v["tags"] if t and t.strip()][:10]
                out.append(v)
        except Exception as e:
            erros.append("%s: %s" % (f.__name__, e))
        time.sleep(1)
    # junta duplicadas entre fontes (mesmo título + empresa)
    uniq = {}
    for v in out:
        v["titulo"] = html.unescape(v["titulo"]); v["empresa"] = html.unescape(v["empresa"])
        k = (re.sub(r"\s*[\(\[].*$", "", v["titulo"]).lower().strip(), v["empresa"].lower().strip())
        if k in uniq:
            u = uniq[k]
            if v["local"] and v["local"] not in u["local"]: u["local"] = (u["local"] + ", " + v["local"])[:200]
            u.setdefault("ids_extras", []).append(v["id"])
        else: uniq[k] = v
    json.dump(list(uniq.values()), sys.stdout, ensure_ascii=False, indent=1)
    for e in erros: print("AVISO fonte falhou:", e, file=sys.stderr)
    print("%d vagas novas" % len(uniq), file=sys.stderr)

if __name__ == "__main__":
    main()
