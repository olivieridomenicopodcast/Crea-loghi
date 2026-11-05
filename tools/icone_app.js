// Crea le icone della PWA in docs/icons a partire da logo/ufficiale/logo-ufficiale.svg (uso: node tools/icone_app.js)
const { chromium } = require('playwright'); const fs=require('fs'); const path=require('path');
const root=path.join(__dirname,'..');const svg=fs.readFileSync(path.join(root,'logo/ufficiale/logo-ufficiale.svg'));
const uri='data:image/svg+xml;base64,'+svg.toString('base64');
(async()=>{const b=await chromium.launch();const out=path.join(root,'docs/icons');fs.mkdirSync(out,{recursive:true});
const shot=async(name,size,html,omit)=>{const p=await b.newPage({viewport:{width:size,height:size}});await p.setContent(`<body style="margin:0">${html}</body>`);await p.screenshot({path:path.join(out,name),omitBackground:omit});await p.close();};
const plain=s=>`<img src="${uri}" style="width:${s}px;height:${s}px;display:block">`;
await shot('icon-192.png',192,plain(192),true);await shot('icon-512.png',512,plain(512),true);await shot('favicon-32.png',32,plain(32),true);
const full=s=>`<div style="width:${s}px;height:${s}px;background:linear-gradient(#2A1FA6,#5B45F2);display:flex;align-items:center;justify-content:center"><img src="${uri}" style="width:${s*0.78}px;height:${s*0.78}px"></div>`;
await shot('icon-maskable-512.png',512,full(512),false);await shot('apple-touch-icon.png',180,full(180),false);
await b.close();})();
