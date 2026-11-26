// node tools/svg-to-pdf.js arte.svg saida.pdf LARG ALT  (PDF vetorial gerado pelo Chromium/Skia)
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [,,src,out,w,h]=process.argv;const b=await chromium.launch();const p=await b.newPage();
await p.setContent(`<html><head><style>@page{size:${w}px ${h}px;margin:0}html,body{margin:0}</style></head><body>${fs.readFileSync(src,'utf8')}</body></html>`);
await p.pdf({path:out,width:w+'px',height:h+'px',printBackground:true,pageRanges:'1'});await b.close();})();
