#!/usr/bin/env python3
"""Gera uma imagem a partir de um prompt usando a API configurada no ambiente.

Uso: python3 tools/gerar-imagem.py "prompt em inglês" saida.png
Lê GEMINI_API_KEY (Google, modelo de imagem do Gemini) ou OPENAI_API_KEY (gpt-image-1), nessa ordem.
"""
import base64, json, os, sys, urllib.request

prompt, out = sys.argv[1], sys.argv[2]


def post(url, body, headers):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **headers})
    return json.load(urllib.request.urlopen(req, timeout=300))


if os.environ.get("GEMINI_API_KEY"):
    model = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")
    r = post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
             {"contents": [{"parts": [{"text": prompt}]}],
              "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "4:5"}}},
             {"x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    data = next(p["inlineData"]["data"] for p in r["candidates"][0]["content"]["parts"] if "inlineData" in p)
elif os.environ.get("OPENAI_API_KEY"):
    r = post("https://api.openai.com/v1/images/generations",
             {"model": os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1"), "prompt": prompt, "size": "1024x1536", "quality": "high"},
             {"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]})
    data = r["data"][0]["b64_json"]
else:
    sys.exit("Nenhuma chave encontrada: configure GEMINI_API_KEY ou OPENAI_API_KEY no ambiente.")

open(out, "wb").write(base64.b64decode(data))
print("ok", out)
