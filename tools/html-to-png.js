// uso: node tools/html-to-png.js arquivo.html saida.png [largura] [altura] [escala] [transparente]
const {chromium}=require('playwright');
(async()=>{const [,,src,out,w='1080',h='1350',s='1',t]=process.argv;
const b=await chromium.launch();const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:+s});
await p.goto('file://'+require('path').resolve(src));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
await p.screenshot({path:out,omitBackground:!!t,fullPage:true});await b.close();})();
