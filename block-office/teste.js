const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const http=require('http'),fs=require('fs'),path=require('path'),R=process.argv[2];
const srv=http.createServer((q,s)=>{let f=path.join(R,decodeURIComponent(q.url.split('?')[0]));if(f.endsWith('/'))f+='index.html';fs.readFile(f,(e,d)=>{if(e){s.statusCode=404;return s.end()}s.setHeader('Content-Type',f.endsWith('.html')?'text/html; charset=utf-8':f.endsWith('.gltf')?'model/gltf+json':'application/octet-stream');s.end(d)})}).listen(8778);
const p=await b.newPage({viewport:{width:430,height:860},hasTouch:true,isMobile:true});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('http://localhost:8778/');await p.waitForSelector('#jogar:not([hidden])',{timeout:180000});await p.screenshot({path:R+'/../t0.png'});
await p.click('#jogar');await p.waitForTimeout(3000);await p.screenshot({path:R+'/../t1.png'});
const cenas=[[0,4.2,0,'t2'],[0,-2,0,'t3'],[-2.2,-6.5,-0.9,'t4'],[2,-8,0.5,'t5'],[-1.6,-17.5,-0.6,'t6'],[0.4,-27,0.2,'t7'],[2.5,-12.5,-1.4,'t8']];
for(const [x,z,y,n] of cenas){await p.evaluate(([x,z,y])=>window.__bh.ir(x,z,y),[x,z,y]);await p.waitForTimeout(2500);await p.screenshot({path:R+'/../'+n+'.png',timeout:150000});}
await p.evaluate(()=>{window.__bh.ir(-2.3,-19.2,0);window.__bh.olha(-.1)});await p.waitForTimeout(2500);await p.screenshot({path:R+'/../t9.png',timeout:150000});
for(const id of ['touca','lean','base','disco'])await p.evaluate(id=>window.__bh.pega(id),id);await p.waitForTimeout(3500);await p.screenshot({path:R+'/../t10.png',timeout:150000});
console.log(JSON.stringify(errs.slice(0,10)));await b.close();srv.close()})();
