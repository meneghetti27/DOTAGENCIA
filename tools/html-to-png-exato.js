// igual ao html-to-png.js, mas tira só a área exata da janela (sem fullPage): node tools/html-to-png-exato.js in.html out.png W H [escala] [t]
const {chromium}=require('playwright');
(async()=>{const [,,src,out,w='1080',h='1350',s='1',t]=process.argv;
const b=await chromium.launch();const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:+s});
await p.goto('file://'+require('path').resolve(src));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
await p.screenshot({path:out,omitBackground:!!t,clip:{x:0,y:0,width:+w,height:+h}});await b.close();})();
