const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+process.argv[2]);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
await p.pdf({path:process.argv[3],width:'1080px',height:'1350px',printBackground:true,margin:{top:0,bottom:0,left:0,right:0}});await b.close();})();
