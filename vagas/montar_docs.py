#!/usr/bin/env python3
"""Junta as vagas do buscar.py com as notas que o agente deu e gera 1 JSON por vaga + o batch para o ArtifactData.

Uso: python3 vagas/montar_docs.py novas.json notas.json pasta_saida
  notas.json = {"<id>": {"nota":0-10,"resumo":"PT","porque":"PT","alerta":"PT ou vazio","area":"UX/UI|Brand|Motion|Web|IA|Vídeo","aceita_brasil":true|false}}
  Vagas sem nota ou com "pular": true ficam de fora (mas entram nos vistos).
Saída: pasta_saida/vagas/<id>.json, pasta_saida/writes.json (lista para batch, até 50 por chamada), pasta_saida/ids.json
"""
import json, os, re, sys
from datetime import datetime, timezone
novas, notas, out = json.load(open(sys.argv[1])), json.load(open(sys.argv[2])), sys.argv[3]
os.makedirs(out + "/vagas", exist_ok=True)
agora = datetime.now(timezone.utc).isoformat()
writes, ids = [], []
for v in novas:
    ids += [v["id"]] + v.get("ids_extras", [])
    n = notas.get(v["id"])
    if not n or n.get("pular"): continue
    doc_id = re.sub(r"[^A-Za-z0-9_\-.~:@+]", "-", v["id"])[:200]
    d = {k: v.get(k, "") for k in ("fonte", "plataforma", "titulo", "empresa", "url", "link_aplicar", "como_aplicar", "local", "salario", "tipo", "data", "recrutador")}
    d["descricao"] = (v.get("descricao") or "")[:3500]
    d.update({k: n.get(k) for k in ("nota", "resumo", "porque", "alerta", "area", "aceita_brasil")})
    d.update(status="nova", criada=agora)
    p = f"{out}/vagas/{doc_id}.json"; json.dump(d, open(p, "w"), ensure_ascii=False)
    writes.append({"op": "set", "collection": "vagas", "doc_id": doc_id, "file_path": os.path.abspath(p)})
json.dump(writes, open(out + "/writes.json", "w"), indent=1)
json.dump(ids, open(out + "/ids.json", "w"))
print(len(writes), "vagas para gravar;", len(ids), "ids vistos;", sum(1 for v in novas if (notas.get(v['id']) or {}).get('nota', 0) >= 8), "com nota 8+")
