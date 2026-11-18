const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const [,,html,out,w,h,pdf]=process.argv;
const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:pdf?1:2});
await p.goto('file://'+require('path').resolve(html));await p.waitForLoadState('networkidle');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
if(pdf)await p.pdf({path:out,width:w+'px',height:h+'px',printBackground:true,preferCSSPageSize:true});
else await p.screenshot({path:out});await b.close();})();
