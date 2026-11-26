const { chromium } = require('playwright');const path=require('path'),fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--allow-file-access-from-files']});const p=await b.newPage({viewport:{width:270,height:480}});
await p.goto('file://'+path.resolve(__dirname,'cenas.html'));await p.evaluate(()=>window.ready);
const shot=async f=>(await p.$('#c')).screenshot({path:f,omitBackground:true});
for(const [n,dur] of [['intro',6],['cta',4]]){fs.mkdirSync('fr/'+n,{recursive:true});for(let i=0;i<dur*30;i++){await p.evaluate(([n,t])=>window[n](t),[n,i/30]);await shot(`fr/${n}/${String(i).padStart(4,'0')}.png`)}}
const caps=[['c1',"REBATA AS PEÇAS",'#ffc23d'],['c2','QUEBRE A BLOCK','#a77be0'],['c3','DERRUBE A CAVEIRA','#f0662a']];
for(const [f,s,col] of caps){await p.evaluate(([s,col])=>window.cap(s,250,col),[s,col]);await shot(`fr/${f}.png`)}
await p.evaluate(()=>window.cap2('ENTRE NO RANKING','COM SEU @'));await shot('fr/c4.png');await b.close()})();
