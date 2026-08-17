const {chromium}=require('playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 for(const [name,scheme] of [['light','light'],['dark','dark']]){
  const p=await b.newPage({viewport:{width:900,height:1200},colorScheme:scheme,deviceScaleFactor:2});
  await p.goto('file://'+__dirname+'/efu-utilisation-summary.html');
  await p.waitForTimeout(400);
  await p.screenshot({path:`shot-${name}.png`,fullPage:true});
  await p.close();
 }
 const p=await b.newPage();
 await p.goto('file://'+__dirname+'/efu-utilisation-summary.html');
 await p.pdf({path:'EFU-Utilisation-Summary.pdf',format:'A4',printBackground:true,
   preferCSSPageSize:true});
 await b.close();
 console.log('done');
})();
