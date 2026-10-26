# Render 3D fotorrealista (Poly Haven + three.js)

1. `npm i three@0.170.0` nesta pasta e baixe um HDRI qualquer como `studio.hdr` (opcional, usado com `&hdr=1`).
2. Baixar modelo: `python3 fetch_model.py pocket_watch 2k` (lista: https://api.polyhaven.com/assets?t=models).
3. Servir a pasta: `python3 -m http.server 8765`
4. Renderizar PNG transparente:
   `node shot.js "m=models/pocket_watch/pocket_watch.gltf&el=12&az=-38&key=1.1&env=1.2&pw=4&tint=%23e6ecff&zoom=1.3" saida.png 2000 2000`
   - `az`/`el`: ângulo da câmera · `zoom`: distância · `tint`: cor das partes metálicas
   - `env`/`pb`/`pw`: força do estúdio (softboxes azuis / softbox branco) · `key`/`rim`: luzes diretas
5. Recortar com PIL (`im.crop(im.getbbox())`), salvar em `designs/assets/` e usar no HTML do post.
6. Exportar o post: `node tools/post-to-png.js $PWD/post.html $PWD/post.png`
