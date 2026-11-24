#!/usr/bin/env python3
"""Junta as vagas do buscar.py com as notas que o agente deu e gera 1 JSON por vaga + o batch para o ArtifactData.

Uso: python3 vagas/montar_docs.py novas.json notas.json pasta_saida
  notas.json = {"<id>": {"nota":0-10,"resumo":"PT","porque":"PT","alerta":"PT ou vazio","area":"UX/UI|Brand|Motion|Web|IA|Vídeo",
                         "aceita_brasil":true|false,"etiquetas":[...opcional, somam às do buscador]}}
  Vagas sem nota ou com "pular": true ficam de fora (mas entram nos vistos). Pulada leva "categoria" e "motivo"
  (trecho da vaga): vai para pasta_saida/descartes.json, que o agente soma em meta/radar.
Saída: pasta_saida/vagas/<id>.json, pasta_saida/writes.json (lista para batch, até 50 por chamada), pasta_saida/ids.json
"""
import json, os, re, sys
from datetime import datetime, timezone
novas, notas, out = json.load(open(sys.argv[1])), json.load(open(sys.argv[2])), sys.argv[3]
os.makedirs(out + "/vagas", exist_ok=True)
agora = datetime.now(timezone.utc).isoformat()
writes, ids, pulos = [], [], {}
for v in novas:
    ids += [v["id"]] + v.get("ids_extras", [])
    n = notas.get(v["id"])
    if not n or n.get("pular"):
        if n: c = n.get("categoria") or "outro"; pulos[c] = pulos.get(c, 0) + 1
        continue
    doc_id = re.sub(r"[^A-Za-z0-9_\-.~:@+]", "-", v["id"])[:200]
    d = {k: v.get(k, "") for k in ("fonte", "plataforma", "titulo", "empresa", "url", "link_aplicar", "como_aplicar", "local", "salario", "tipo", "data", "recrutador",
                                  "origem", "modelo", "restricao", "idioma")}
    d["origem"] = d["origem"] or "gringa"
    d["exige_conta"] = bool(v.get("exige_conta"))
    d["etiquetas"] = list(dict.fromkeys((v.get("etiquetas") or []) + (n.get("etiquetas") or [])))
    d["descricao"] = (v.get("descricao") or "")[:3500]
    d.update({k: n.get(k) for k in ("nota", "resumo", "porque", "alerta", "area", "aceita_brasil")})
    d.update(status="nova", criada=agora)
    p = f"{out}/vagas/{doc_id}.json"; json.dump(d, open(p, "w"), ensure_ascii=False)
    writes.append({"op": "set", "collection": "vagas", "doc_id": doc_id, "file_path": os.path.abspath(p)})
json.dump(writes, open(out + "/writes.json", "w"), indent=1)
json.dump(ids, open(out + "/ids.json", "w"))
json.dump(pulos, open(out + "/descartes.json", "w"))
def top(o):
    L = sorted((dict(id=v["id"], titulo=v["titulo"], empresa=v["empresa"], salario=v.get("salario", ""), modelo=v.get("modelo", ""),
                     nota=notas[v["id"]]["nota"], aceita_brasil=notas[v["id"]].get("aceita_brasil"))
                for v in novas if v.get("origem", "gringa") == o and notas.get(v["id"]) and not notas[v["id"]].get("pular")),
               key=lambda x: -x["nota"])
    return [x for x in L if x["nota"] >= 7][:3]
json.dump({"br": top("br"), "gringa": top("gringa")}, open(out + "/melhores.json", "w"), ensure_ascii=False, indent=1)
print(len(writes), "vagas para gravar;", len(ids), "ids vistos;", sum(1 for v in novas if (notas.get(v['id']) or {}).get('nota', 0) >= 8), "com nota 8+")
