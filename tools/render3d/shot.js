const {chromium}=require('playwright');
(async()=>{const [,,qs,out,w,h]=process.argv;const W=+w||1600,H=+h||1600;
const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:W,height:H}});p.on('console',m=>console.log('console:',m.text()));p.on('pageerror',e=>console.log('err:',e.message));
await p.goto(`http://localhost:8765/render.html?w=${W}&h=${H}&${qs}`);await p.waitForFunction('window.DONE',null,{timeout:240000});
await p.screenshot({path:out,omitBackground:true});await b.close();})();
