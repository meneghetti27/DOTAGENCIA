const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const jobs=JSON.parse(process.argv[2]);
for(const [qs,out] of jobs){const p=await b.newPage({viewport:{width:1200,height:1200}});
p.on('console',m=>{if(m.type()==='error')console.log(m.text())});
await p.goto('http://localhost:8765/scene.html?'+qs);await p.waitForFunction(()=>window.DONE,null,{timeout:60000});
await p.locator('canvas').screenshot({path:out,omitBackground:true});await p.close();}
await b.close();})();
