#!/usr/bin/env python3
"""Busca vagas de design ABERTAS AGORA, gringas e brasileiras.

Gringas (pedido do dono, 19/11/2026): páginas de vaga das empresas (Greenhouse, Lever, Ashby: só vaga aberta e
formulário único, sem cadastro) + agregadores só quando o link cai no site/ATS da empresa (Himalayas, Remotar,
LinkedIn remoto LATAM/Worldwide).
Brasileiras (pedido do dono, 24/11/2026): LinkedIn (Porto Alegre e Brasil remoto), Trampos.co e Remotar.
Regra: paga mais que R$ 3.000/mês; presencial/híbrido só em Porto Alegre (Grande POA entra com etiqueta), o resto remoto.

Uso: python3 vagas/buscar.py vistos.json [--extras empresas_extra.json] [--aplicadas aplicadas.json]
                             [--relatorio relatorio.json] > novas.json
  empresas_extra.json = {"greenhouse":[..],"lever":[..],"ashby":[..]} (slugs descobertos em rodadas anteriores)
  aplicadas.json      = [{"empresa":..,"titulo":..}] (vagas já aplicadas: corta repost e marca "2ª vaga na empresa")
  relatorio.json      = saída: lidas por fonte, descartes por categoria, falhas, slugs novos descobertos
"""
import json, os, re, sys, html, time, argparse, urllib.request, urllib.error, urllib.parse, concurrent.futures as cf
from collections import Counter
from datetime import datetime, timezone, timedelta

AQUI = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
      "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8"}
MAX_DIAS = 21          # vaga de ATS: publicada há no máximo 21 dias (e ainda aberta, senão nem aparece na API)
MAX_DIAS_AGREG = 7     # agregadores (Himalayas, Remotar, Trampos, LinkedIn)
PISO_BRL = 3000        # vaga brasileira: teto da faixa publicada tem que passar disso

DESIGN = re.compile(r"design|designer|\bui\b|\bux\b|brand|art director|creative|motion|graphic|visual|illustrat|"
                    r"animator|animation|video editor|video producer|content creator|social media|generative|"
                    r"\bai artist|3d artist|webflow|framer|diseñ|diretor\(?a?\)? de arte|direção de arte|dire[çc][ãa]o criativa|"
                    r"criação|criativ|ilustrador|editor\(?a?\)? de v[íi]deo|videomaker|motion|designer gr[áa]fico", re.I)
FORA = re.compile(r"engineer|developer|devops|sales|account exec|recruit|accountant|data scien|backend|full.?stack|front.?end|"
                  r"\bqa\b|tester|support|success|counsel|legal|finance|analyst|researcher|regulatory|\bbim\b|silicon|civil|"
                  r"level design|game design|operations|resource manager|marketing manager|intern\b|internship|"
                  r"desenvolvedor|engenheir|programador|vendedor|vendas|comercial|estagi|trainee|aprendiz|jovem aprendiz|"
                  r"arquitet|t[ée]cnico|mec[âa]nic|el[ée]tric|hardware|interiores|interior design|industrial|moda|fashion|"
                  r"cal[çc]ado|j[óo]ia|joalheri|m[óo]veis|mobili|t[êe]xtil|instrucional|instructional|cad\b|revit|"
                  r"professor|teacher|tutor|cozinh|confeit|cabeleire|costur|translat|tradu|locali[sz]ation|review lead|linguist", re.I)
SENIOR_DEMAIS = re.compile(r"\b(vp|vice president|chief|cco|principal|staff)\b", re.I)   # diretor de arte/head ficam: a nota decide
RUIM = re.compile(r"crypto|casino|gambl|betting|\bbet\b|apostas|cassino|adult|onlyfans|nsfw|web3|blockchain|"
                  r"marketing multin[íi]vel|\bmmn\b|pir[âa]mide", re.I)
# não é vaga de verdade (idea do radar de TI): banco de talentos, treino de IA pago por tarefa
NAO_E_VAGA = re.compile(r"talent (pool|community|network)|banco de talentos|cadastro reserva|future opportunities|"
                        r"general application|candidatura espont[âa]nea|outlier|alignerr|micro1|xperteez|data annotation|"
                        r"help train ai|ai trainer|treinar (modelos de )?ia|rate ai responses", re.I)
JUNIOR = re.compile(r"j[úu]nior|\bjr\b|assistente|auxiliar|junior|entry.level", re.I)

# países onde a vaga não serve pra ele (idioma/local): se a vaga é SÓ nesses lugares, sai
LONGE = re.compile(r"india|bangalore|bengaluru|hyderabad|pune|chennai|mumbai|delhi|noida|gurgaon|philippines|manila|pakistan|"
                   r"indonesia|jakarta|vietnam|china|beijing|shanghai|japan|tokyo|korea|seoul|taiwan|thailand|bangkok|malaysia|"
                   r"kuala|singapore|bangladesh|sri lanka|nepal|egypt|cairo|nigeria|lagos|kenya|nairobi|turkey|türkiye|istanbul|"
                   r"israel|tel aviv|saudi|dubai|uae|qatar|russia|ukraine|serbia", re.I)   # Europa/UE liberada: cidadão italiano e português
PERTO = re.compile(r"anywhere|worldwide|global|latam|latin america|americas|brazil|brasil|south america|"
                   r"united states|\bus\b|usa|canada|united kingdom|\buk\b|ireland|portugal|lisbon|australia|new zealand|"
                   r"remote$|^remote", re.I)

# Restrição de país escondida (aprendido no radar de TI: "Remote" sozinho não quer dizer mundo todo).
# DURA = ele não consegue se inscrever (cidadania, autorização sem patrocínio): sai. LEVE = vai com alerta e nota máx. 4.
EUA_DURA = re.compile(r"(u\.?s\.? citizen|united states citizen|citizenship is required|security clearance|"
                      r"must be (legally )?authori[sz]ed to work in the (u\.?s|united states)[^.]{0,60}without (visa )?sponsorship|"
                      r"(will not|won.t|unable to|cannot|do not) (provide|offer|support) (visa )?sponsorship|\bw-?2 only\b|no c2c|"
                      r"green card)", re.I)
EUA_LEVE = re.compile(r"(anywhere in the (u\.?s|united states)|across the (u\.?s|usa|united states)|"
                      r"(u\.?s\.?|us)[- ]based|based in the (u\.?s|united states)|reside in the (u\.?s|united states)|"
                      r"located in the (u\.?s|united states)|authori[sz]ed to work in the (u\.?s|united states)|\bw-?2\b|"
                      r"(est|pst|cst|mst|eastern|pacific) time zone|remote\s*[-–(]\s*(us|usa|united states))", re.I)
UK_LEVE = re.compile(r"right to work in the uk|uk[- ]based|based in the uk|reside in the uk", re.I)
ABRE = re.compile(r"brazil|brasil|latam|latin america|south america|americas|worldwide|anywhere in the world|"
                  r"work from anywhere|any country|contractor|independent contractor|global(ly)? remote|remote.{0,20}global", re.I)

# LinkedIn: o campo de local manda (aprendido no radar de TI). Cidade dos EUA/Canadá/UK/Ásia = vaga presa lá, mesmo marcada "remoto".
EUROPA_LATAM = re.compile(r"portugal|spain|españa|italy|italia|france|germany|netherlands|ireland|belgium|austria|poland|czech|"
                          r"sweden|denmark|finland|norway|greece|romania|hungary|croatia|european union|europe|emea|"
                          r"argentina|chile|colombia|mexico|méxico|peru|uruguay|paraguay|costa rica|latin america|latam|brazil|brasil", re.I)
BRASIL_LOCAL = re.compile(r"brasil|brazil|,\s*(ac|al|ap|am|ba|ce|df|es|go|ma|mt|ms|mg|pa|pb|pr|pe|pi|rj|rn|rs|ro|rr|sc|sp|se|to)\b|"
                          r"porto alegre|são paulo|rio de janeiro|curitiba|belo horizonte|florianópolis", re.I)
POA = re.compile(r"porto alegre|greater porto alegre|grande porto alegre", re.I)
GRANDE_POA = re.compile(r"canoas|cachoeirinha|gravata[íi]|alvorada|viam[ãa]o|esteio|sapucaia|s[ãa]o leopoldo|novo hamburgo|"
                        r"eldorado do sul|gua[íi]ba|nova santa rita", re.I)
PRESENCIAL = re.compile(r"\b(presencial|h[íi]brid[oa]|hybrid|on.?site|in.?office|no escrit[óo]rio)\b", re.I)
REMOTO_TXT = re.compile(r"100% remot|totalmente remot|home.?office|trabalho remoto|fully remote|remote.first|\bremot[oa]\b", re.I)

ANONIMA = re.compile(r"confidencial|confidential|sigilo|anonymous", re.I)
RECRUTADORA = re.compile(r"recruit|talent|staffing|hunter|headhunt|recrutamento|consultoria de rh|jobgether|pavago|hirewithnear|"
                         r"remote talent|bairesdev|saganrecruitment|turing|toptal|crossover|andela|braintrust|lemon\.io", re.I)
FORM_PESADO = re.compile(r"loom|v[íi]deo de apresenta|video (introduction|cover)|record a video|teste pr[áa]tico|take.?home|"
                         r"design (challenge|test|exercise)|case pr[áa]tico|desafio t[ée]cnico", re.I)

SIMPLES = {"boards.greenhouse.io": "Greenhouse", "job-boards.greenhouse.io": "Greenhouse", "jobs.lever.co": "Lever",
           "jobs.ashbyhq.com": "Ashby", "apply.workable.com": "Workable"}

descartes = Counter()
falhas = Counter()
por_fonte = Counter()
descobertas = {"greenhouse": set(), "lever": set(), "ashby": set()}


# ---------------------------------------------------------------- utilidades
def http(url, json_=True, tentativas=3, espera=2.0):
    """GET com retry em 429/5xx. Falha final vai para o relatório (busca pela metade não passa em silêncio)."""
    ult = "rede"
    for i in range(tentativas):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                corpo = r.read().decode("utf-8", "replace")
                return json.loads(corpo) if json_ else corpo
        except urllib.error.HTTPError as e:
            ult = str(e.code)
            if e.code == 429 or e.code >= 500:
                time.sleep(espera * (i + 1)); continue
            break
        except Exception:
            ult = "rede"; time.sleep(espera * (i + 1))
    falhas[f"{urllib.parse.urlparse(url).netloc} {ult}"] += 1
    raise RuntimeError(f"{url} -> {ult}")

def get(url): return http(url)

def limpa(s, n=3500):
    s = html.unescape(html.unescape(s or ""))
    s = re.sub(r"<(br|/p|/li|/div|/h\d)[^>]*>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"[ \t\r\f\v]+", " ", re.sub(r"\n\s*\n+", "\n", s)).strip()[:n]

def data(s):
    if not s: return None
    try:
        if isinstance(s, (int, float)): return datetime.fromtimestamp(s / 1000 if s > 1e11 else s, timezone.utc)
        d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except Exception: return None

def remoto(txt):
    return bool(re.search(r"remote|anywhere|worldwide|latam|latin america|americas|remoto", txt or "", re.I))

def lingua(txt):
    """'pt', 'en', 'es' ou 'outra' (só pt/en/es servem)."""
    w = re.findall(r"[a-zà-ú]+", (txt or "").lower()[:2500])
    if len(w) < 30: return "en"
    c = lambda S: sum(x in S for x in w)
    en = c({"the", "and", "you", "with", "our", "will", "for", "your", "are", "to", "of", "we"})
    pt = c({"de", "para", "você", "com", "nossa", "uma", "que", "os", "as", "não", "em", "do", "da", "vaga"})
    es = c({"el", "los", "las", "con", "usted", "nuestro", "del", "trabajo", "experiencia", "y", "en"})
    t = (txt or "").lower()[:4000]
    pt += 2 * len(re.findall(r"ção|ções|ã|õ|você|não", t))
    es += 2 * len(re.findall(r"ción|ciones|ñ|¿|usted", t))
    outras = c({"und", "der", "die", "wir", "sie", "mit", "nous", "vous", "avec", "les", "des"})
    if outras > max(en, pt, es) * 0.8: return "outra"
    return max((en, "en"), (pt, "pt"), (es, "es"))[1]

def lugar_ok(local):
    if not local or PERTO.search(local): return True
    return not LONGE.search(local)

def status_link(url):
    """'vivo' | 'morto'. Só conta como morto 404/410 ou texto de vaga fechada; 403/erro de rede = vivo (site com anti-robô)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA["User-Agent"]})
        with urllib.request.urlopen(req, timeout=20) as r:
            corpo = r.read(200000).decode("utf-8", "replace").lower()[:30000]
            if re.search(r"no longer (accepting|available)|job (is )?closed|position has been filled|page not found|"
                         r"vaga (encerrada|expirada|finalizada)|não está mais disponível|inscrições encerradas", corpo):
                return "morto"
            return "vivo"
    except urllib.error.HTTPError as e:
        return "morto" if e.code in (404, 410) else "vivo"
    except Exception:
        return "vivo"

def link_vivo_estrito(url):
    """Para ATS: tem que abrir de verdade (200) e não dizer que fechou."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA["User-Agent"]})
        with urllib.request.urlopen(req, timeout=20) as r:
            corpo = r.read(200000).decode("utf-8", "replace").lower()
            return r.status == 200 and not re.search(r"no longer (accepting|available)|job (is )?closed|position has been filled|page not found|404", corpo[:20000])
    except Exception:
        return False

def ats_de(link):
    """Se o link é de Greenhouse/Lever/Ashby, devolve (plataforma, slug) e anota o slug para o empresas.json crescer sozinho."""
    u = urllib.parse.urlparse(link or "")
    partes = [p for p in u.path.split("/") if p]
    if not partes: return None
    if u.netloc in ("boards.greenhouse.io", "job-boards.greenhouse.io"):
        slug = partes[0] if partes[0] != "embed" else urllib.parse.parse_qs(u.query).get("for", [""])[0]
        return ("greenhouse", slug.lower()) if slug else None
    if u.netloc == "jobs.lever.co": return ("lever", partes[0].lower())
    if u.netloc == "jobs.ashbyhq.com": return ("ashby", partes[0].lower())
    return None

def salario_brl(txt):
    """Maior valor mensal em R$ citado no texto (None se não tem). Ignora valor anual/por hora óbvio."""
    vals = []
    for m in re.finditer(r"R\$\s*([\d.]{1,7}(?:,\d{2})?)\s*(mil|k)?", txt or "", re.I):
        n = m.group(1).replace(".", "").split(",")[0]
        if not n.isdigit(): continue
        v = int(n) * (1000 if m.group(2) else 1)
        if 800 <= v <= 60000: vals.append(v)
    return max(vals) if vals else None

def restricao(txt, local):
    """('dura'|'leve'|'', trecho). Usado só nas gringas."""
    t = (txt or "") + " " + (local or "")
    m = EUA_DURA.search(t)
    if m and not re.search(r"brazil|brasil|latam|latin america", t, re.I): return "dura", m.group(0)
    m = EUA_LEVE.search(t) or UK_LEVE.search(t)
    if m and not ABRE.search(t): return "leve", m.group(0)
    if not ABRE.search(t) and re.fullmatch(r"\s*(remote|remoto)?\s*", local or "", re.I):
        return "leve", "só diz 'Remote', sem abrir para outros países"
    return "", ""

def norm_titulo(t): return re.sub(r"\s*[-–|(\[].*$", "", t or "").lower().strip()


# ---------------------------------------------------------------- fontes gringas (ATS)
def greenhouse(s):
    for j in get(f"https://boards-api.greenhouse.io/v1/boards/{s}/jobs?content=true")["jobs"]:
        local = (j.get("location") or {}).get("name", "")
        yield dict(id=f"gh-{s}-{j['id']}", plataforma="Greenhouse", titulo=j["title"], empresa=j.get("company_name") or s,
                   url=j["absolute_url"], link_aplicar=j["absolute_url"] + "#app", local=local, remoto=remoto(local),
                   data=j.get("first_published") or j.get("updated_at"), descricao=j.get("content"), tipo="", fonte_tipo="ats")

def lever(s):
    for j in get(f"https://api.lever.co/v0/postings/{s}?mode=json"):
        c = j.get("categories") or {}
        local = ", ".join(filter(None, [c.get("location"), *(c.get("allLocations") or [])]))
        yield dict(id=f"lever-{s}-{j['id']}", plataforma="Lever", titulo=j["text"], empresa=s.capitalize(), url=j["hostedUrl"],
                   link_aplicar=j.get("applyUrl") or j["hostedUrl"] + "/apply", local=local,
                   remoto=j.get("workplaceType") == "remote" or remoto(local), data=j.get("createdAt"),
                   descricao=(j.get("descriptionPlain") or "") + " " + (j.get("additionalPlain") or ""), tipo=c.get("commitment", ""),
                   fonte_tipo="ats")

def ashby(s):
    for j in get(f"https://api.ashbyhq.com/posting-api/job-board/{s}?includeCompensation=true")["jobs"]:
        if j.get("isListed") is False: continue
        locs = [j.get("location", "")] + [x.get("location", "") for x in (j.get("secondaryLocations") or [])]
        sal = ((j.get("compensation") or {}).get("compensationTierSummary")) or ""
        yield dict(id=f"ashby-{s}-{j['id']}", plataforma="Ashby", titulo=j["title"], empresa=s.capitalize(), url=j["jobUrl"],
                   link_aplicar=j.get("applyUrl") or j["jobUrl"] + "/application", local=", ".join(filter(None, locs)),
                   remoto=j.get("workplaceType") == "Remote" or remoto(" ".join(locs)),
                   data=j.get("publishedAt"), descricao=j.get("descriptionPlain"), tipo=j.get("employmentType", ""), salario=sal,
                   fonte_tipo="ats")

def himalayas():
    for j in get("https://himalayas.app/jobs/api?limit=100")["jobs"]:
        link = j.get("applicationLink") or ""
        host = urllib.parse.urlparse(link).netloc
        a = ats_de(link)
        if a: descobertas[a[0]].add(a[1])
        if host not in SIMPLES: continue           # agregador só vale quando cai no formulário da própria empresa
        cats = " ".join((j.get("categories") or []) + (j.get("parentCategories") or []))
        if not re.search(r"design|creative|art|video|motion", cats, re.I): continue
        sal = ""
        if j.get("minSalary"): sal = f"{j.get('currency') or ''} {j['minSalary']}–{j.get('maxSalary') or '?'}/{j.get('salaryPeriod') or ''}"
        yield dict(id="himalayas-" + link.rstrip("/").split("/")[-1], plataforma=SIMPLES[host], titulo=j["title"],
                   empresa=j.get("companyName", ""), url=link, link_aplicar=link,
                   local=", ".join(j.get("locationRestrictions") or []) or "Worldwide", remoto=True,
                   data=j.get("pubDate"), descricao=j.get("description"), tipo=j.get("employmentType", ""), salario=sal,
                   fonte_tipo="agregador", origem="gringa")


# ---------------------------------------------------------------- Remotar (vagas remotas para quem mora no Brasil, BR e gringas)
def remotar():
    vistos = set()
    for termo in ["designer", "design", "motion", "diretor de arte", "social media", "ux"]:
        for pag in (1, 2):
            try: d = get(f"https://api.remotar.com.br/jobs?search={urllib.parse.quote(termo)}&page={pag}")
            except Exception: break
            for j in d.get("data", []):
                if j["id"] in vistos or j.get("expired") or not j.get("active", True): continue
                vistos.add(j["id"])
                link = j.get("externalLink") or f"https://remotar.com.br/job/{j['id']}"
                link = re.sub(r"[?&]utm_[^&]+", "", link).rstrip("?&")
                a = ats_de(link)
                if a: descobertas[a[0]].add(a[1])
                li = re.search(r"linkedin\.com/jobs/view/(\d+)", link)
                tags = " ".join((t.get("tag") or {}).get("name", "") for t in (j.get("jobTags") or []))
                gringa = "internacional" in tags.lower()
                s = j.get("jobSalary") or {}
                sal = ""
                if s.get("to"):
                    de, ate = (s.get("from") or 0) / 100, s["to"] / 100
                    per = {"yearly": "/ano", "monthly": "/mês", "hourly": "/hora"}.get(s.get("type"), "")
                    moeda = "R$" if s.get("currency") == "BRL" else (s.get("currency") or "")
                    sal = f"{moeda} {de:,.0f}–{ate:,.0f}{per}".replace(",", ".") if de else f"{moeda} {ate:,.0f}{per}".replace(",", ".")
                host = urllib.parse.urlparse(link).netloc
                plat = SIMPLES.get(host) or ("LinkedIn" if li else host.replace("www.", ""))
                local = "Remoto" if j.get("type") == "remote" else f"{(j.get('type') or '').capitalize()} · {j.get('city') or ''} {j.get('state') or ''}".strip()
                yield dict(id=f"li-{li.group(1)}" if li else f"remotar-{j['id']}", plataforma=plat,
                           titulo=j["title"], empresa=(j.get("company") or {}).get("name") or j.get("companyDisplayName") or "",
                           url=link, link_aplicar=link, local=local, remoto=j.get("type") == "remote",
                           cidade=j.get("city") or "", data=j.get("createdAt"),
                           descricao=(j.get("subtitle") or "") + "\n" + (j.get("description") or ""), tipo="", salario=sal,
                           salario_brl_mes=(s.get("to") / 100 if s.get("currency") == "BRL" and s.get("type") in (None, "monthly") and s.get("to") else None),
                           fonte_tipo="agregador", origem="gringa" if gringa else "br", fonte_nome="Remotar")
            if pag >= (d.get("meta") or {}).get("last_page", 1): break


# ---------------------------------------------------------------- Trampos.co (vagas criativas no Brasil)
def trampos():
    lista = []
    for pag in range(1, 16):
        try: d = get(f"https://trampos.co/api/v2/opportunities?page={pag}")
        except Exception: break
        ops = d.get("opportunities") or []
        lista += ops
        if pag >= (d.get("pagination") or {}).get("total_pages", 1): break
    for o in lista:
        if o.get("category_slug") != "design" and not DESIGN.search(o.get("name") or ""): continue
        if (o.get("type_slug") or "") in ("estagio", "trainee"): continue
        try: det = get(f"https://trampos.co/api/v2/opportunities/{o['id']}").get("opportunity") or {}
        except Exception: det = {}
        ho = det.get("home_office", o.get("home_office"))
        hib = det.get("hybrid", o.get("hybrid"))
        cidade = (det.get("city") or o.get("city") or "").strip()
        local = "Remoto" if ho else (("Híbrido · " if hib else "Presencial · ") + f"{cidade} {det.get('state') or o.get('state') or ''}".strip())
        url = f"https://trampos.co/oportunidades/{o['id']}"
        emp = o.get("custom_company_name") or (o.get("company") or {}).get("name", "")
        sal = o.get("salary") or ""
        yield dict(id=f"trampos-{o['id']}", plataforma="Trampos", titulo=o["name"], empresa=emp, url=url,
                   link_aplicar=det.get("apply_url") or url, local=local, remoto=bool(ho), cidade=cidade,
                   data=o.get("published_at"), descricao=det.get("description") or "", tipo=det.get("regime") or o.get("type_name") or "",
                   salario="" if "DIVULG" in sal.upper() else sal, fonte_tipo="agregador", origem="br", fonte_nome="Trampos",
                   exige_conta=True)


# ---------------------------------------------------------------- LinkedIn (API pública de visitante; espaçar para não tomar 429)
LI_BUSCAS = (
    [(k, "Porto Alegre, Rio Grande do Sul, Brasil", "", "br") for k in
     ["designer", "designer gráfico", "diretor de arte", "motion designer", "social media", "ux designer", "product designer", "web designer"]] +
    [(k, "Brasil", "2", "br") for k in
     ["designer gráfico", "diretor de arte", "motion designer", "designer de marca", "ux designer", "product designer", "web designer", "social media designer"]] +
    [(k, loc, "2", "gringa") for loc in ("Latin America", "Worldwide") for k in
     ["brand designer", "graphic designer", "motion designer", "art director", "product designer"]]
)

LI_HDR = {"User-Agent": UA["User-Agent"], "Accept-Language": "en-US,en;q=0.9"}
def li_get(url):
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=LI_HDR), timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(4 * (i + 1)); continue
            falhas[f"www.linkedin.com {e.code}"] += 1; raise
        except Exception:
            time.sleep(2)
    falhas["www.linkedin.com 429"] += 1
    raise RuntimeError("linkedin 429")

def li_cards(kw, loc, wt):
    q = {"keywords": kw, "location": loc, "f_TPR": "r604800", "start": "0"}
    if wt: q["f_WT"] = wt
    h = li_get("https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?" + urllib.parse.urlencode(q))
    for bloco in h.split("<li")[1:]:
        jid = re.search(r"jobPosting:(\d+)", bloco)
        if not jid: continue
        g = lambda cls: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", (re.search(cls + r'[^>]*>(.*?)</', bloco, re.S) or [None, ""])[1]))).strip()
        quando = re.search(r'datetime="([\d-]+)"', bloco)
        yield dict(id=jid.group(1), titulo=g("base-search-card__title"), empresa=g("base-search-card__subtitle"),
                   local=g("job-search-card__location"), data=quando.group(1) if quando else None)

def li_detalhe(jid):
    h = li_get(f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{jid}")
    if re.search(r"No longer accepting applications|Não aceita mais candidaturas", h): return None
    d = re.search(r"show-more-less-html__markup[^>]*>(.*?)</div>", h, re.S)
    crit = [re.sub(r"\s+", " ", x).strip() for x in re.findall(r"description__job-criteria-text[^>]*>(.*?)<", h, re.S)]
    return dict(descricao=d.group(1) if d else "", nivel=crit[0] if crit else "", tipo=crit[1] if len(crit) > 1 else "")

def linkedin(vistos):
    cards = {}
    for kw, loc, wt, origem in LI_BUSCAS:
        try:
            for c in li_cards(kw, loc, wt):
                c["origem_busca"], c["wt"] = origem, wt
                cards.setdefault(c["id"], c)
        except Exception: pass
        time.sleep(1.0)
    for jid, c in cards.items():
        if f"li-{jid}" in vistos: continue
        if not DESIGN.search(c["titulo"]) or FORA.search(c["titulo"]):
            descartes["nao-e-design"] += 1; continue
        try: det = li_detalhe(jid)
        except Exception: det = {}
        time.sleep(1.0)
        if det is None: descartes["fechada"] += 1; continue
        url = f"https://www.linkedin.com/jobs/view/{jid}/"
        yield dict(id=f"li-{jid}", plataforma="LinkedIn", titulo=c["titulo"], empresa=c["empresa"], url=url, link_aplicar=url,
                   local=c["local"] + (" · Remoto" if c["wt"] == "2" else ""), remoto=c["wt"] == "2", cidade=c["local"],
                   data=c["data"], descricao=det.get("descricao", ""), tipo=det.get("tipo", ""), nivel=det.get("nivel", ""),
                   fonte_tipo="agregador", origem=c["origem_busca"], fonte_nome="LinkedIn")


# ---------------------------------------------------------------- filtros
def filtra_br(v, desc):
    """Regras das vagas brasileiras. Devolve categoria de descarte ou ''."""
    txt = v["titulo"] + " " + desc
    sal = v.get("salario_brl_mes") or salario_brl((v.get("salario") or "") + " " + desc)
    v["salario_brl_mes"] = sal
    if sal and sal <= PISO_BRL: return "salario"          # "mais que 3 mil": faixa que para em 3.000 não serve
    if not sal and JUNIOR.search(v["titulo"]): return "salario"          # júnior/assistente sem salário publicado quase sempre fica abaixo de 3 mil
    local_txt = " ".join([v.get("local", ""), v.get("cidade", "")])
    em_poa, grande = bool(POA.search(local_txt)), bool(GRANDE_POA.search(local_txt))
    if v.get("remoto"):
        # anúncio remoto que no texto pede presença em outra cidade
        m = PRESENCIAL.search(desc[:2500])
        if m and not REMOTO_TXT.search(desc[:2500]) and not POA.search(desc): return "presencial"
        v["modelo"] = "Remoto"
    elif em_poa or grande:
        if not em_poa and POA.search(desc): em_poa = True
        hib = re.search(r"h[íi]brid|hybrid", local_txt + " " + desc[:2000], re.I)
        v["modelo"] = ("Híbrido" if hib else "Presencial") + (" · Porto Alegre" if em_poa else " · Grande POA")
        if not em_poa: v.setdefault("etiquetas", []).append("Grande POA (fora da capital)")
    elif REMOTO_TXT.search(desc[:2500]) and not PRESENCIAL.search(desc[:2500]):
        v["modelo"] = "Remoto"
    else:
        return "presencial"
    if not sal: v.setdefault("etiquetas", []).append("salário não informado")
    if re.search(r"\bPJ\b|pessoa jur[íi]dica", txt): v.setdefault("etiquetas", []).append("PJ")
    if re.search(r"\bCLT\b", txt): v.setdefault("etiquetas", []).append("CLT")
    return ""

def filtra_gringa(v, desc):
    if not v.get("remoto") or not lugar_ok(v.get("local", "")): return "local"
    if v["id"].startswith("li-") and v.get("plataforma") == "LinkedIn" and not ABRE.search(desc) and not EUROPA_LATAM.search(v.get("local", "")):
        return "local"
    tipo, trecho = restricao(desc, v.get("local", ""))
    if tipo == "dura": return "local"
    if tipo == "leve": v["restricao"] = trecho; v.setdefault("etiquetas", []).append("pode exigir morar nos EUA/UK")
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vistos", nargs="?")
    ap.add_argument("--extras"); ap.add_argument("--aplicadas"); ap.add_argument("--relatorio")
    ap.add_argument("--sem-linkedin", action="store_true")
    a = ap.parse_args()
    vistos = set(json.load(open(a.vistos))) if a.vistos and os.path.exists(a.vistos) else set()
    emp = json.load(open(os.path.join(AQUI, "empresas.json")))
    if a.extras and os.path.exists(a.extras):
        ex = json.load(open(a.extras))
        for k in ("greenhouse", "lever", "ashby"): emp[k] = sorted(set(emp[k]) | set(ex.get(k) or []))
    aplicadas = json.load(open(a.aplicadas)) if a.aplicadas and os.path.exists(a.aplicadas) else []
    ja = {(norm_titulo(x.get("titulo")), (x.get("empresa") or "").lower().strip()) for x in aplicadas}
    ja_emp = {(x.get("empresa") or "").lower().strip() for x in aplicadas}
    agora = datetime.now(timezone.utc)

    tarefas = [(greenhouse, s) for s in emp["greenhouse"]] + [(lever, s) for s in emp["lever"]] + [(ashby, s) for s in emp["ashby"]]
    brutas = []
    def roda(t):
        f, s = t
        try: return list(f(s))
        except Exception: return []
    with cf.ThreadPoolExecutor(16) as ex:
        for r in ex.map(roda, tarefas): brutas += r
    por_fonte["ATS das empresas"] = len(brutas)
    for nome, f in (("Himalayas", himalayas), ("Remotar", remotar), ("Trampos", trampos)):
        try:
            r = list(f()); brutas += r; por_fonte[nome] = len(r)
        except Exception as e: falhas[f"{nome} {type(e).__name__}"] += 1
    if not a.sem_linkedin:
        try:
            r = list(linkedin(vistos)); brutas += r; por_fonte["LinkedIn"] = len(r)
        except Exception as e: falhas[f"LinkedIn {type(e).__name__}"] += 1

    out, ids = [], set()
    for v in brutas:
        if v["id"] in vistos or v["id"] in ids: continue
        t = v["titulo"] or ""
        if not DESIGN.search(t) or FORA.search(t): descartes["nao-e-design"] += 1; continue
        if SENIOR_DEMAIS.search(t): descartes["senioridade"] += 1; continue
        desc = limpa(v.get("descricao"))
        if NAO_E_VAGA.search(t + " " + v["empresa"] + " " + desc[:1500]): descartes["nao-e-vaga"] += 1; continue
        if RUIM.search(t + " " + v["empresa"] + " " + desc[:800]): descartes["setor"] += 1; continue
        lg = lingua(desc)
        if lg == "outra": descartes["idioma"] += 1; continue
        d = data(v.get("data"))
        lim = MAX_DIAS if v.get("fonte_tipo") == "ats" else MAX_DIAS_AGREG
        if not d or d < agora - timedelta(days=lim): descartes["velha"] += 1; continue
        # origem: ATS/Himalayas = gringa; LinkedIn decide pelo idioma do texto
        origem = v.get("origem") or "gringa"
        if v.get("fonte_nome") == "LinkedIn": origem = "br" if lg == "pt" and BRASIL_LOCAL.search(v.get("local", "")) else "gringa"
        if origem == "br" and lg == "es": origem = "gringa"
        if v.get("fonte_tipo") == "ats" and lg == "pt" and re.search(r"brasil|brazil|são paulo|porto alegre", v.get("local", ""), re.I):
            origem = "br"
        v["origem"] = origem
        cat = filtra_br(v, desc) if origem == "br" else filtra_gringa(v, desc)
        if cat: descartes[cat] += 1; continue
        k = (norm_titulo(t), (v["empresa"] or "").lower().strip())
        if k in ja: descartes["repost"] += 1; continue
        et = v.setdefault("etiquetas", [])
        if k[1] in ja_emp: et.append("2ª vaga na empresa")
        if ANONIMA.search(v["empresa"]): et.append("cliente anônimo")
        if RECRUTADORA.search(v["empresa"] + " " + v.get("url", "")): et.append("recrutadora")
        if FORM_PESADO.search(desc): et.append("pede teste ou vídeo")
        if v.get("exige_conta") or re.search(r"gupy\.io|inhire\.app|solides|kenoby|quickin|vagas\.com|infojobs|catho|geekhunter",
                                             v.get("link_aplicar", "")):
            v["exige_conta"] = True; et.append("exige conta no site")
        ids.add(v["id"])
        fonte = v["empresa"] + " · " + (v.get("fonte_nome") or v["plataforma"])
        if v.get("exige_conta"): como = f"Candidatura no {v['plataforma']} (pede login/conta: o Chrome segue se tu já estiver logado)"
        elif v["plataforma"] == "LinkedIn": como = "LinkedIn: Candidatura simplificada ou link para o site da empresa"
        elif v["plataforma"] in SIMPLES.values(): como = f"Formulário único no {v['plataforma']}, sem cadastro (nome, e-mail, PDF, carta)"
        else: como = f"Formulário no site da empresa ({v['plataforma']})"
        v.update(data=d.isoformat(), descricao=desc, salario=v.get("salario", ""), fonte=fonte, como_aplicar=como, idioma=lg)
        for x in ("fonte_tipo", "cidade", "fonte_nome"): v.pop(x, None)
        out.append(v)

    # último filtro: o formulário abre de verdade agora (ATS: estrito; agregador: só cai se 404/410 ou "vaga encerrada")
    def vivo(v):
        if v["id"].startswith(("li-", "trampos-")): return True          # já lidos pela API agora há pouco
        if v["plataforma"] in ("Greenhouse", "Lever", "Ashby") and not v["id"].startswith(("remotar-", "himalayas-")):
            return link_vivo_estrito(v["link_aplicar"]) or link_vivo_estrito(v["url"])
        return status_link(v["link_aplicar"]) == "vivo"
    with cf.ThreadPoolExecutor(12) as ex:
        vivos = list(ex.map(vivo, out))
    descartes["fechada"] += sum(1 for ok in vivos if not ok)
    out = [v for v, ok in zip(out, vivos) if ok]

    # mesma vaga postada em várias cidades/fontes vira uma só
    uniq = {}
    for v in out:
        k = (norm_titulo(v["titulo"]), v["empresa"].lower())
        if k in uniq:
            if v["local"] and v["local"] not in uniq[k]["local"]: uniq[k]["local"] = (uniq[k]["local"] + " · " + v["local"])[:200]
            uniq[k].setdefault("ids_extras", []).append(v["id"])
        else: uniq[k] = v
    out = list(uniq.values())
    for v in out:   # link pra achar recrutador no LinkedIn (só busca, ele abre)
        termo = "recrutador design" if v["origem"] == "br" else "recruiter design"
        v["recrutador"] = "https://www.linkedin.com/search/results/people/?keywords=" + urllib.parse.quote(v["empresa"] + " " + termo)
        v["etiquetas"] = list(dict.fromkeys(v.get("etiquetas", [])))
    out.sort(key=lambda v: v["data"], reverse=True)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)

    novos_slugs = {k: sorted(s - set(emp[k])) for k, s in descobertas.items()}
    rel = dict(lidas=len(brutas), por_fonte=dict(por_fonte), novas=len(out),
               novas_br=sum(v["origem"] == "br" for v in out), novas_gringas=sum(v["origem"] == "gringa" for v in out),
               descartes=dict(descartes.most_common()), falhas=dict(falhas.most_common(15)), slugs_novos=novos_slugs)
    if a.relatorio: json.dump(rel, open(a.relatorio, "w"), ensure_ascii=False, indent=1)
    print(json.dumps(rel, ensure_ascii=False), file=sys.stderr)

if __name__ == "__main__":
    main()
