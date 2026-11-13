(()=>{
'use strict';
/* ============ utilidades ============ */
const $=id=>document.getElementById(id);
const clamp=(v,a,b)=>v<a?a:v>b?b:v;
const rand=(a,b)=>a+Math.random()*(b-a);
const pick=a=>a[Math.floor(Math.random()*a.length)];
const lerp=(a,b,t)=>a+(b-a)*t;
function hsh(x,y,i){let n=(x*374761393+y*668265263+i*1442695041)|0;n=Math.imul(n^(n>>>13),1274126177);return((n^(n>>>16))>>>0)/4294967296;}
function strSeed(s){let h=2166136261;for(const ch of s){h^=ch.charCodeAt(0);h=Math.imul(h,16777619);}return h>>>0;}
function mulberry(a){return()=>{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
function shade(hex,amt){const n=parseInt(hex.slice(1),16);const f=v=>clamp(v+amt,0,255);return'#'+((1<<24)|(f(n>>16)<<16)|(f(n>>8&255)<<8)|f(n&255)).toString(16).slice(1);}
const lin=hex=>new THREE.Color(hex).convertSRGBToLinear();

/* ============ planta da casa (1 unidade = 1 quadrado da grade) ============ */
const W=56,H=48,WH=3.2;
const K={OUT:0,WALL:1,GLASS:2,WATER:3,HEDGE:4,STONE:5};
const kind=new Uint8Array(W*H),indoor=new Uint8Array(W*H);
const fmat=new Array(W*H).fill('grass'),wst=new Array(W*H).fill(null),roomName=new Array(W*H).fill('');
const I=(x,z)=>z*W+x,inb=(x,z)=>x>=0&&z>=0&&x<W&&z<H;
const kAt=(x,z)=>inb(x,z)?kind[I(x,z)]:K.HEDGE;
function set(x,z,o){if(!inb(x,z))return;const i=I(x,z);if(o.k!==undefined)kind[i]=o.k;if(o.f)fmat[i]=o.f;if(o.w!==undefined)wst[i]=o.w;if(o.in!==undefined)indoor[i]=o.in;if(o.r!==undefined)roomName[i]=o.r;}
function rect(x,z,w,h,o){for(let j=z;j<z+h;j++)for(let i=x;i<x+w;i++)set(i,j,o);}
function room(x,z,w,h,f,ws,r){rect(x,z,w,h,{k:K.OUT,f,w:ws,in:1,r});}
function door(x,z,lx,lz){const i=I(lx,lz);set(x,z,{k:K.OUT,f:fmat[i],w:wst[i],in:1,r:roomName[i]});}

rect(0,0,W,H,{k:K.OUT,f:'grass'});
rect(0,0,1,H,{k:K.STONE});
rect(23,0,W-23,1,{k:K.HEDGE});rect(W-1,0,1,H,{k:K.HEDGE});rect(1,H-1,W-1,1,{k:K.HEDGE});
rect(1,0,22,4,{f:'flag'});rect(1,4,1,31,{f:'peb'});rect(2,4,3,31,{f:'flag'});
rect(5,4,38,23,{k:K.WALL,in:0});
room(6,5,8,6,'whitetile','orange','cozinha');
room(15,5,5,6,'whitetile','yellowtile','lavanderia');
room(21,5,3,6,'whitetile','azulejo','lavabo');
room(25,5,6,6,'parquet','mustard','escritório');
room(32,5,5,6,'carpet','mustard','quarto de hóspedes');
room(38,5,4,6,'mosaic','mosaic','banheiro');
room(6,12,36,2,'parquet','corr','corredor');
room(6,14,7,7,'parquet','board','hall de entrada');
room(6,21,7,5,'terra','brick','sala de jantar');
room(14,14,8,12,'parquet','brick','sala de TV');
room(23,14,11,12,'parquet','board','sala de estar');
rect(25,19,8,6,{f:'terra'});
room(35,15,7,6,'parquet','brick','suíte');
room(35,22,7,4,'mosaic','mosaic','banheiro da suíte');
set(6,16,{f:'marble'});set(6,17,{f:'marble'});
for(const x of [9,10])door(x,11,x,10);
door(17,11,17,10);door(22,11,22,10);door(27,11,27,10);door(28,11,28,10);door(34,11,34,10);door(39,11,39,10);
door(14,8,13,8);
door(5,8,6,8);door(5,16,6,16);door(5,17,6,17);
door(13,16,12,16);door(13,17,12,17);door(13,23,12,23);
for(let z=16;z<=20;z++)door(22,z,21,z);
door(37,14,37,15);door(38,21,38,20);
rect(14,26,20,1,{k:K.GLASS,in:0});
for(const x of [18,19,28,29])door(x,26,x,25);
rect(42,15,1,6,{k:K.GLASS,in:0});
rect(14,27,20,4,{f:'deck'});
rect(34,27,11,10,{k:K.WATER});rect(43,12,6,15,{k:K.WATER});

/* ============ móveis e objetos ============ */
const OBJ=[];
function obj(k,x,z,w,d,o={}){const ob=Object.assign({k,x,z,w,d,solid:true},o);OBJ.push(ob);return ob;}
obj('car',3,0,4,2,{color:'#2c3440',spot:{n:'porta-malas do carro',w:1}});
obj('car',8,0,4,2,{color:'#a9adb3'});
obj('car',13,0,4,2,{color:'#7a2a24'});
obj('freezer',18,1,2,1,{spot:{n:'freezer da garagem',w:5}});
obj('kcounter',6,5,6,1,{spot:{n:'gaveta vermelha da cozinha',w:1}});
obj('fridge',13,5,1,1,{spot:{n:'geladeira',w:5}});
obj('oldfridge',6,9,1,1,{spot:{n:'geladeira velha marrom',w:4}});
obj('table',8,8,2,1,{spot:{n:'mesinha da cozinha',w:1}});
obj('redtall',13,9,1,1);
obj('tank',15,5,2,1,{spot:{n:'tanque cheio de gelo',w:5}});
obj('ycab',19,6,1,4,{spot:{n:'armário amarelo',w:1}});
obj('vanity',21,5,2,1,{color:'#2a8fa0',spot:{n:'pia do lavabo',w:1}});
obj('toilet',23,9,1,1);
obj('wardrobe',25,5,4,1,{spot:{n:'roupeiro branco',w:1}});
obj('desk',30,6,1,3,{spot:{n:'gaveta da escrivaninha',w:1}});
obj('chairA',26,9,1,1);obj('chairA',27,9,1,1);obj('chairA',28,9,1,1);
obj('wardrobe',32,5,4,1,{spot:{n:'armário do quarto',w:1}});
obj('bed',33,8,2,2,{color:'#e9e4d6',spot:{n:'debaixo da cama',w:1}});
obj('tvold',36,9,1,1,{spot:{n:'atrás da TV velha',w:1}});
obj('vanity',38,5,3,1,{color:'#f0a49a',spot:{n:'gaveta do banheiro',w:1}});
obj('toilet',41,5,1,1);obj('shower',40,9,2,2,{solid:false});
obj('piano',12,14,1,2,{spot:{n:'dentro do piano',w:1}});
obj('redbench',6,19,1,2,{spot:{n:'embaixo do banco vermelho',w:1}});
obj('sculpture',13,19,1,1,{solid:false});
obj('cabinet',6,22,1,3,{spot:{n:'aparador de madeira',w:1}});
obj('dtable',8,23,3,2,{spot:{n:'mesa de jantar',w:1}});
obj('fireplace',16,14,3,1,{spot:{n:'lareira',w:1}});
obj('sofaP',14,19,1,4,{spot:{n:'sofá roxo',w:1}});
obj('tvstand',20,15,1,1);
obj('cooler',21,24,1,1,{color:'#2f63b8',spot:{n:'cooler azul',w:4}});
obj('relief',27,14,3,1);
obj('sofaC',26,18,3,1,{face:'S'});
obj('armchair',25,20,1,1,{face:'E'});obj('armchair',25,22,1,1,{face:'E'});obj('armchair',31,20,1,1,{face:'W'});obj('armchair',31,22,1,1,{face:'W'});
obj('ctable',27,21,2,1,{spot:{n:'mesinha de centro',w:1}});
obj('vase',24,24,1,1,{spot:{n:'vasão de cerâmica',w:2}});
obj('sideboard',23,14,2,1,{spot:{n:'aparador de mármore',w:1}});
obj('speaker',33,24,1,1,{spot:{n:'atrás da caixa de som',w:1}});
obj('fern',33,14,1,1,{spot:{n:'vaso da samambaia',w:1}});
obj('sofaC',30,25,3,1,{face:'N'});
obj('fireplaceO',35,15,2,1,{spot:{n:'lareira da suíte',w:1}});
obj('bed',38,17,2,3,{color:'#efefe9',coats:true,spot:{n:'pilha de casacos na cama',w:2}});
obj('sofaB',41,17,1,2,{spot:{n:'sofá azul',w:1}});
obj('dresser',35,19,1,2,{spot:{n:'cômoda da suíte',w:1}});
obj('vanity',35,22,3,1,{color:'#f0a49a',spot:{n:'pia com gelo',w:4}});
obj('toilet',41,25,1,1);obj('shower',40,22,2,2,{solid:false});
obj('isopor',15,27,2,1,{spot:{n:'caixa de isopor',w:4}});
obj('isopor',22,27,2,1,{spot:{n:'isopor grande',w:4}});
obj('trash',25,27,1,1,{spot:{n:'lixeira de tampa vermelha',w:1}});
obj('freezer',30,29,2,1,{spot:{n:'freezer do deck',w:5}});
obj('pot',32,27,2,2,{spot:{n:'vaso de planta',w:1}});
obj('cooler',17,30,1,1,{color:'#c8352c',spot:{n:'cooler vermelho',w:4}});
obj('chairP',20,29,1,1,{color:'#e6e6e0'});obj('chairP',21,29,1,1,{color:'#4a5a66'});
obj('grill',7,33,3,2,{spot:{n:'churrasqueira',w:2}});
obj('bbqtable',11,35,4,2,{spot:{n:'mesa do choripan',w:2}});
obj('isopor',6,38,2,1,{spot:{n:'isopor do churras',w:4}});
obj('trashbags',13,31,2,1,{spot:{n:'sacos de lixo',w:1}});
obj('cooler',30,40,1,1,{color:'#d4d4d0',spot:{n:'cooler branco',w:3}});
obj('chairP',10,38,1,1,{color:'#e6e6e0'});obj('chairP',12,38,1,1,{color:'#4a5a66'});obj('chairP',14,38,1,1,{color:'#e6e6e0'});
const TREES=[[16,41],[30,44],[38,40],[52,30],[52,14],[50,4],[40,2],[30,1],[24,45],[8,44],[36,34],[52,44],[45,44],[22,38],[3,40],[52,24]];
for(const [x,z] of TREES)obj('tree',x,z,1,1);

const solid=new Uint8Array(W*H);
for(let i=0;i<W*H;i++)if(kind[i]!==K.OUT)solid[i]=1;
for(const o of OBJ)if(o.solid)for(let j=o.z;j<o.z+o.d;j++)for(let i=o.x;i<o.x+o.w;i++)if(inb(i,j))solid[I(i,j)]=1;
const solidAt=(x,z)=>!inb(x,z)||solid[I(x,z)]===1;
const solidW=(x,z)=>solidAt(Math.floor(x),Math.floor(z));
const TALL=new Uint8Array(W*H);for(const o of OBJ)if(['relief','wardrobe','fireplace','fireplaceO','redtall','fridge','car','tree','grill','piano'].includes(o.k))for(let j=o.z;j<o.z+o.d;j++)for(let i=o.x;i<o.x+o.w;i++)if(inb(i,j))TALL[I(i,j)]=1;
const blocksView=(x,z)=>{const k=kAt(x,z);return k===K.WALL||k===K.HEDGE||k===K.STONE;};

/* ============ three.js ============ */
const canvas=$('c');
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,powerPreference:'high-performance'});
renderer.outputEncoding=THREE.sRGBEncoding;
renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.05;
const scene=new THREE.Scene();
const camera=new THREE.PerspectiveCamera(62,1,0.08,400);
const fog=new THREE.Fog(0x8899aa,40,140);scene.fog=fog;

const loader=new THREE.TextureLoader();
const TSCALE={brick:2.2,stone:3,flag:3,mosaic:1.4,corr:1.4,board:3,azulejo:1.6,parquet:1.8,terra:2.6,deck:2.4,grass:4,ceiling:3,door:1,mustard:3,cushion:1,orange:1.6,yellowtile:1.4,whitetile:1.6,wood:2,woodL:2,red:1,granite:2,carpet:3,marble:2.5,water:5,roof:5,peb:2,hedge:2,curtain:1.2};
const TEX={};
function photoTex(k){const t=loader.load(TEXDATA[k]);t.wrapS=t.wrapT=THREE.MirroredRepeatWrapping;t.encoding=THREE.sRGBEncoding;t.anisotropy=8;return t;}
function canvasTex(draw,size=256){const c=document.createElement('canvas');c.width=c.height=size;draw(c.getContext('2d'),size);const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;t.encoding=THREE.sRGBEncoding;t.anisotropy=8;return t;}
for(const k of Object.keys(TEXDATA))TEX[k]=photoTex(k);
function noise(g,s,cols,n,sz=2){for(let i=0;i<n;i++){g.fillStyle=cols[i%cols.length];g.fillRect(Math.random()*s,Math.random()*s,sz,sz);}}
TEX.orange=canvasTex((g,s)=>{g.fillStyle='#d9842a';g.fillRect(0,0,s,s);const t=s/4;for(let y=0;y<4;y++)for(let x=0;x<4;x++){g.fillStyle=['#e08c2e','#d47d24','#e6953a','#cf7a22'][(x*3+y)%4];g.fillRect(x*t+2,y*t+2,t-4,t-4);g.fillStyle='rgba(255,230,180,.18)';g.fillRect(x*t+6,y*t+6,t*.5,4);}});
TEX.yellowtile=canvasTex((g,s)=>{g.fillStyle='#d8d4c8';g.fillRect(0,0,s,s);const t=s/4;for(let y=0;y<4;y++)for(let x=0;x<4;x++){const X=x*t+2,Y=y*t+2,c=t-4;g.fillStyle='#f7f4ec';g.fillRect(X,Y,c,c);g.fillStyle='#e8b81c';const m=X+c/2,n=Y+c/2;g.beginPath();for(let a=0;a<4;a++){const ang=a*Math.PI/2+Math.PI/4;g.moveTo(m,n);g.ellipse(m+Math.cos(ang)*c*.28,n+Math.sin(ang)*c*.28,c*.16,c*.07,ang,0,7);}g.fill();g.beginPath();g.arc(m,n,c*.12,0,7);g.fill();}});
TEX.whitetile=canvasTex((g,s)=>{g.fillStyle='#c9cbc8';g.fillRect(0,0,s,s);const t=s/4;for(let y=0;y<4;y++)for(let x=0;x<4;x++){g.fillStyle=['#f2f2ef','#eeeeea','#f5f5f2'][(x+y)%3];g.fillRect(x*t+1.5,y*t+1.5,t-3,t-3);}});
TEX.wood=canvasTex((g,s)=>{g.fillStyle='#4a2414';g.fillRect(0,0,s,s);for(let x=0;x<s;x+=2){g.fillStyle=`rgba(${120+Math.random()*40|0},${50+Math.random()*25|0},${25+Math.random()*15|0},.35)`;g.fillRect(x,0,1+Math.random()*2,s);}for(let i=0;i<6;i++){g.fillStyle='rgba(20,8,4,.35)';g.fillRect(i*s/6,0,1,s);}});
TEX.woodL=canvasTex((g,s)=>{g.fillStyle='#9a5a2c';g.fillRect(0,0,s,s);for(let x=0;x<s;x+=2){g.fillStyle=`rgba(${170+Math.random()*50|0},${95+Math.random()*30|0},${40+Math.random()*20|0},.4)`;g.fillRect(x,0,1+Math.random()*2,s);}g.fillStyle='rgba(40,18,6,.5)';g.fillRect(s/2,0,2,s);});
TEX.red=canvasTex((g,s)=>{g.fillStyle='#c71a14';g.fillRect(0,0,s,s);for(let y=0;y<s;y+=s/4){g.fillStyle='#3a120c';g.fillRect(0,y,s,5);g.fillStyle='#e0362c';g.fillRect(0,y+5,s,6);}});
TEX.granite=canvasTex((g,s)=>{g.fillStyle='#4a2c1c';g.fillRect(0,0,s,s);noise(g,s,['#6a4630','#2e1a10','#8a6a50','#3a2418'],2600,2);});
TEX.carpet=canvasTex((g,s)=>{g.fillStyle='#d8ccb0';g.fillRect(0,0,s,s);noise(g,s,['#cfc2a4','#e2d7bd','#c8bb9d'],4000,2);});
TEX.marble=canvasTex((g,s)=>{g.fillStyle='#e9e5dc';g.fillRect(0,0,s,s);g.strokeStyle='rgba(150,140,125,.35)';for(let i=0;i<9;i++){g.lineWidth=Math.random()*2;g.beginPath();let x=Math.random()*s,y=0;g.moveTo(x,y);while(y<s){x+=rand(-12,12);y+=rand(6,18);g.lineTo(x,y);}g.stroke();}});
TEX.roof=canvasTex((g,s)=>{g.fillStyle='#8c8b84';g.fillRect(0,0,s,s);noise(g,s,['#7a7972','#9d9c95','#6c6b65','#a7a59d'],5000,3);});
TEX.peb=canvasTex((g,s)=>{g.fillStyle='#7a7064';g.fillRect(0,0,s,s);for(let i=0;i<900;i++){g.fillStyle=pick(['#a39684','#5e554b','#c2b8a8','#8f6f5a','#d2c7b4']);g.beginPath();g.ellipse(Math.random()*s,Math.random()*s,rand(2,6),rand(2,5),Math.random()*3,0,7);g.fill();}});
TEX.hedge=canvasTex((g,s)=>{g.fillStyle='#2b5426';g.fillRect(0,0,s,s);for(let i=0;i<2500;i++){g.fillStyle=pick(['#3c7032','#24481f','#4f8a3e','#335f2b']);g.beginPath();g.ellipse(Math.random()*s,Math.random()*s,rand(2,7),rand(1,3),Math.random()*3,0,7);g.fill();}});
TEX.curtain=canvasTex((g,s)=>{for(let x=0;x<s;x++){const v=Math.sin(x/s*Math.PI*8);const c=Math.round(225+v*14);g.fillStyle=`rgb(${c},${c-6},${c-22})`;g.fillRect(x,0,1,s);}});
TEX.deck=canvasTex((g,s)=>{g.fillStyle='#4a4540';g.fillRect(0,0,s,s);const b=s/5;for(let i=0;i<5;i++){g.fillStyle=['#8a8176','#7d756b','#948a7e','#857c70','#7a7268'][i];g.fillRect(0,i*b+3,s,b-5);for(let k=0;k<40;k++){g.fillStyle='rgba(60,55,50,.25)';g.fillRect(Math.random()*s,i*b+4+Math.random()*(b-8),rand(10,50),1);}g.fillStyle='#3a3530';g.fillRect((i*67)%s,i*b,2,b);}});
TEX.water=canvasTex((g,s)=>{g.fillStyle='#4f6e22';g.fillRect(0,0,s,s);for(let i=0;i<260;i++){g.fillStyle=pick(['rgba(140,170,70,.35)','rgba(40,60,20,.35)','rgba(200,220,150,.18)']);g.fillRect(Math.random()*s,Math.random()*s,rand(6,30),rand(1,3));}});

const MATS={};
const SHINE={parquet:45,whitetile:70,orange:80,yellowtile:80,marble:60,terra:18,mosaic:50,red:60,granite:60,azulejo:60};
function mat(k){
  if(MATS[k])return MATS[k];let m;
  if(k==='glass')m=new THREE.MeshPhongMaterial({color:lin('#a8cbd6'),transparent:true,opacity:.22,shininess:100,side:THREE.DoubleSide,depthWrite:false});
  else if(k==='water'){m=new THREE.MeshPhongMaterial({map:TEX.water,color:0xffffff,shininess:120,specular:0x99aa88,transparent:true,opacity:.93});}
  else if(k.startsWith('e:'))m=new THREE.MeshBasicMaterial({color:lin(k.slice(2)),toneMapped:false});
  else if(k.startsWith('c:'))m=new THREE.MeshPhongMaterial({color:lin(k.slice(2)),shininess:12});
  else m=new THREE.MeshPhongMaterial({map:TEX[k],shininess:SHINE[k]||6,specular:SHINE[k]?0x333333:0x0a0a0a});
  if(k==='curtain'||k==='hedge')m.side=THREE.DoubleSide;
  return MATS[k]=m;
}

/* lotes de geometria (tudo que é fixo vira poucas malhas) */
const BATCH=new Map();
function bt(k){let b=BATCH.get(k);if(!b){b={p:[],n:[],u:[],cast:false};BATCH.set(k,b);}return b;}
function quad(k,ox,oy,oz,rx,ry,rz,ux,uy,uz,cast=true){
  const b=bt(k);if(cast)b.cast=true;const s=TSCALE[k]||1;
  const rl=Math.hypot(rx,ry,rz)||1,ul=Math.hypot(ux,uy,uz)||1;
  let nx=ry*uz-rz*uy,ny=rz*ux-rx*uz,nz=rx*uy-ry*ux;const nl=Math.hypot(nx,ny,nz)||1;nx/=nl;ny/=nl;nz/=nl;
  const u0=(ox*rx+oy*ry+oz*rz)/rl/s,v0=(ox*ux+oy*uy+oz*uz)/ul/s,u1=u0+rl/s,v1=v0+ul/s;
  const A=[ox,oy,oz],B=[ox+rx,oy+ry,oz+rz],C=[ox+rx+ux,oy+ry+uy,oz+rz+uz],D=[ox+ux,oy+uy,oz+uz];
  b.p.push(A[0],A[1],A[2],B[0],B[1],B[2],C[0],C[1],C[2],A[0],A[1],A[2],C[0],C[1],C[2],D[0],D[1],D[2]);
  for(let i=0;i<6;i++)b.n.push(nx,ny,nz);
  b.u.push(u0,v0,u1,v0,u1,v1,u0,v0,u1,v1,u0,v1);
}
function box(k,x,y,z,w,h,d,o={}){
  const c=o.cast!==false,kt=o.top||k,kf=o.front||k;
  const f=o.face||'S';
  quad(f==='E'?kf:k,x+w,y,z+d,0,0,-d,0,h,0,c);
  quad(f==='W'?kf:k,x,y,z,0,0,d,0,h,0,c);
  quad(f==='S'?kf:k,x,y,z+d,w,0,0,0,h,0,c);
  quad(f==='N'?kf:k,x+w,y,z,-w,0,0,0,h,0,c);
  quad(kt,x,y+h,z+d,w,0,0,0,0,-d,c);
  if(o.bottom)quad(k,x,y,z,w,0,0,0,0,d,c);
}
function geo(k,g,m,cast=true){
  g=g.index?g.toNonIndexed():g;g.applyMatrix4(m);const b=bt(k);if(cast)b.cast=true;
  const p=g.attributes.position.array,n=g.attributes.normal.array,uv=g.attributes.uv?g.attributes.uv.array:null;
  for(let i=0;i<p.length/3;i++){b.p.push(p[i*3],p[i*3+1],p[i*3+2]);b.n.push(n[i*3],n[i*3+1],n[i*3+2]);b.u.push(uv?uv[i*2]:0,uv?uv[i*2+1]:0);}
}
const M4=(x,y,z,rx=0,ry=0,rz=0,sx=1,sy=1,sz=1)=>new THREE.Matrix4().compose(new THREE.Vector3(x,y,z),new THREE.Quaternion().setFromEuler(new THREE.Euler(rx,ry,rz)),new THREE.Vector3(sx,sy,sz));
const cyl=(k,x,y,z,r,h,seg=14,rx=0,rz=0,r2)=>geo(k,new THREE.CylinderGeometry(r2===undefined?r:r2,r,h,seg),M4(x,y+h/2,z,rx,0,rz));
const ball=(k,x,y,z,r,sx=1,sy=1,sz=1,det=1)=>geo(k,new THREE.IcosahedronGeometry(r,det),M4(x,y,z,0,0,0,sx,sy,sz));

/* ---- paredes, pisos, vidro, água ---- */
const LAMPS=[];
function buildHouse(){
  const isWallish=k=>k===K.WALL||k===K.HEDGE||k===K.STONE;
  for(let z=0;z<H;z++)for(let x=0;x<W;x++){
    const k=kind[I(x,z)];
    if(k===K.OUT){quad(fmat[I(x,z)],x,0,z+1,1,0,0,0,0,-1,false);continue;}
    if(k===K.WATER){quad('water',x,-.35,z+1,1,0,0,0,0,-1,false);
      for(const [dx,dz] of [[1,0],[-1,0],[0,1],[0,-1]]){const nk=kAt(x+dx,z+dz);if(nk===K.WATER)continue;
        const o=dx===1?[x+1,z+1,0,-1]:dx===-1?[x,z,0,1]:dz===1?[x,z+1,1,0]:[x+1,z,-1,0];
        quad('board',o[0]-dx*.001,-.4,o[1]-dz*.001,o[2]*1,0,o[3]*1,0,.42,0,false);
        box('flag',Math.min(o[0],o[0]+o[2])-(dx===1?.18:0)+(dx===-1?0:0),0,Math.min(o[1],o[1]+o[3])-(dz===1?.18:0),Math.abs(o[2])||.18,.06,Math.abs(o[3])||.18,{cast:false});}
      continue;}
    if(k===K.STONE){box('stone',x,0,z,1,2.2,1);continue;}
    if(k===K.HEDGE){box('hedge',x,0,z,1,2.3,1);continue;}
    if(k===K.GLASS){
      const horiz=isWallish(kAt(x-1,z))||kAt(x-1,z)===K.GLASS||isWallish(kAt(x+1,z))||kAt(x+1,z)===K.GLASS;
      quad(horiz?'deck':'parquet',x,0,z+1,1,0,0,0,0,-1,false);
      const FR='c:#1b1f22';
      if(horiz){quad('glass',x,.12,z+.5,1,0,0,0,WH-.24,0,false);box(FR,x,0,z+.42,1,.12,.16);box(FR,x,WH-.14,z+.42,1,.14,.16);box(FR,x-.04,0,z+.42,.08,WH,.16);
        if(hsh(x,z,3)<.55){const inZ=indoor[I(x,z-1)]?z+.2:z+.65;box('curtain',x+(hsh(x,z,4)<.5?0:.45),.05,inZ,.55,WH-.3,.12);} }
      else{quad('glass',x+.5,.12,z,0,0,1,0,WH-.24,0,false);box(FR,x+.42,0,z,.16,.12,1);box(FR,x+.42,WH-.14,z,.16,.14,1);box(FR,x+.42,0,z-.04,.16,WH,.08);
        if(hsh(x,z,3)<.55){const inX=indoor[I(x-1,z)]?x+.2:x+.65;box('curtain',inX,.05,z+(hsh(x,z,4)<.5?0:.45),.12,WH-.3,.55);} }
      continue;}
    // parede: só as faces que dão pra um espaço livre
    for(const [dx,dz] of [[1,0],[-1,0],[0,1],[0,-1]]){
      const nx=x+dx,nz=z+dz,nk=kAt(nx,nz);if(isWallish(nk))continue;
      const inside=inb(nx,nz)&&indoor[I(nx,nz)]&&nk===K.OUT;
      const style=inside?(wst[I(nx,nz)]||'corr'):(nk===K.GLASS?'corr':'brick');
      const lo=inside?2.7:2.55;
      const o=dx===1?[x+1,z+1,0,-1]:dx===-1?[x,z,0,1]:dz===1?[x,z+1,1,0]:[x+1,z,-1,0];
      quad(style,o[0],0,o[1],o[2],0,o[3],0,lo,0);
      quad('corr',o[0],lo,o[1],o[2],0,o[3],0,WH-lo+.02,0);
      if(inside&&style!=='mosaic'&&style!=='azulejo'&&style!=='yellowtile'&&style!=='orange')quad('wood',o[0]+dx*.01,0,o[1]+dz*.01,o[2],0,o[3],0,.1,0,false);
    }
  }
  // laje: forro por dentro e concreto por cima
  quad('ceiling',4.4,WH,3.4,39.2,0,0,0,0,24.2,false);
  box('corr',4.4,WH,3.4,39.2,.4,24.2,{top:'roof'});
  // pergolados de concreto canelado (deck e corredor lateral)
  for(const zz of [8,14,20,26])box('corr',.8,2.95,zz,4.2,.32,.4);
  for(const zz of [8,14,20,26])box('corr',.8,0,zz,.35,2.95,.35);
  box('corr',13.6,2.95,30.6,20.6,.32,.4);box('corr',13.6,0,30.6,.4,2.95,.4);box('corr',33.8,0,30.6,.4,2.95,.4);
  for(let x=15;x<34;x+=4.5)box('corr',x,2.95,26.8,.4,.32,4.2);
  // azulejo atrás do banco vermelho e painel da parede
  quad('azulejo',5.02,.55,19,0,0,2,0,1.5,0,false);
  // portas de madeira entalhada (abertas)
  box('door',5.05,0,15.1,.9,2.6,.08);box('door',5.05,0,18.82,.9,2.6,.08);
  box('c:#3a2416',4.96,0,7.1,.12,2.6,.9);
  // lâmpadas
  const rooms={};for(let z=0;z<H;z++)for(let x=0;x<W;x++){const r=roomName[I(x,z)];if(!r||kind[I(x,z)]!==K.OUT)continue;(rooms[r]=rooms[r]||[]).push([x,z]);}
  for(const r in rooms){const t=rooms[r];const step=r==='corredor'?6:5;
    const xs=t.map(a=>a[0]),zs=t.map(a=>a[1]);const x0=Math.min(...xs),x1=Math.max(...xs)+1,z0=Math.min(...zs),z1=Math.max(...zs)+1;
    for(let x=x0+Math.min(step,(x1-x0))/2;x<x1;x+=step)for(let z=z0+Math.min(step,(z1-z0))/2;z<z1;z+=step){
      if(r.startsWith('quarto')||r==='escritório'||r==='suíte'){cyl('c:#222',x,2.55,z,.02,.65,4);ball('e:#ffd98a',x,2.45,z,.2,1,1,1,2);}
      else if(r==='sala de jantar'){cyl('c:#333',x,2.4,z,.02,.8,4);geo('e:#d98a3a',new THREE.ConeGeometry(.55,.4,8,1,true),M4(x,2.35,z));}
      else box('e:#fff1d2',x-.35,WH-.04,z-.35,.7,.04,.7,{cast:false});
      LAMPS.push([x,2.6,z]);}}
  LAMPS.push([8.5,2.4,34],[21,2.8,29],[29,2.8,29],[3,2.7,11],[3,2.7,23],[10,2.7,2]);
}

/* ---- móveis ---- */
function furn(o){
  const X=o.x,Z=o.z,Wd=o.w,D=o.d;
  switch(o.k){
  case 'car':{const c='c:'+o.color;box(c,X+.15,.3,Z+.2,Wd-.3,.55,D-.4);box(c,X+1.1,.85,Z+.3,Wd-2.1,.5,D-.6,{front:'c:#25323d',face:'E'});box('c:#25323d',X+1.05,.9,Z+.32,.06,.42,D-.64);
    for(const [dx,dz] of [[.8,.18],[Wd-.8,.18],[.8,D-.18],[Wd-.8,D-.18]])cyl('c:#151515',X+dx,0,Z+dz,.32,.2,12,Math.PI/2);
    box('e:#fff3c0',X+Wd-.17,.5,Z+.35,.03,.15,.3);box('e:#fff3c0',X+Wd-.17,.5,Z+D-.65,.03,.15,.3);box('e:#c43a2a',X+.12,.55,Z+.35,.03,.12,.3);box('e:#c43a2a',X+.12,.55,Z+D-.65,.03,.12,.3);break;}
  case 'freezer':box('c:#f1f1ec',X+.05,0,Z+.1,Wd-.1,.85,D-.2);box('c:#cfd0cb',X+.05,.82,Z+.1,Wd-.1,.06,D-.2);box('c:#9aa0a0',X+Wd/2-.2,.6,Z+D-.12,.4,.06,.04);break;
  case 'fridge':box('c:#e9e9e3',X+.05,0,Z+.08,.9,1.95,.85);box('c:#b9b9b2',X+.05,1.25,Z+.92,.9,.02,.02);box('c:#8a8a85',X+.8,.6,Z+.93,.04,.5,.04);break;
  case 'oldfridge':box('c:#7a5a33',X+.05,0,Z+.1,.85,1.5,.85);box('c:#5a4026',X+.7,.7,Z+.95,.05,.3,.04);break;
  case 'kcounter':box('red',X,0,Z,Wd,.86,D,{top:'granite'});box('c:#c0c4c6',X+2,.86,Z+.2,1.1,.02,.6);box('c:#111',X+4.1,.86,Z+.15,1,.03,.7);
    for(let i=0;i<4;i++)cyl('c:#333',X+4.35+(i%2)*.5,.89,Z+.35+Math.floor(i/2)*.32,.09,.03,10);
    box('wood',X+3.2,1.9,Z,2.6,.7,.42);box('c:#d0221a',X+3.5,2.1,Z+.43,.06,.06,.02);box('c:#d0221a',X+4.6,2.1,Z+.43,.06,.06,.02);break;
  case 'table':box('wood',X+.15,.74,Z+.1,Wd-.3,.06,D-.2);for(const [a,b] of [[.2,.15],[Wd-.28,.15],[.2,D-.23],[Wd-.28,D-.23]])box('wood',X+a,0,Z+b,.08,.74,.08);
    box('c:#e8ddc4',X+.6,.45,Z+D+.05,.45,.06,.45,{cast:false});ball('c:#4f8a2a',X+.7,.84,Z+.5,.09);cyl('c:#8fc0e8',X+1.4,.8,Z+.4,.05,.28,8);break;
  case 'redtall':box('red',X+.05,0,Z+.05,.9,2.5,.9);break;
  case 'tank':box('c:#efe8d4',X,0,Z,Wd,.9,D);box('c:#d8cfb6',X+.3,.6,Z+.15,Wd-.6,.32,D-.35);for(let i=0;i<6;i++)cyl('c:#e8b030',X+.5+i*.18,.85,Z+.4+(i%2)*.15,.05,.12,8);break;
  case 'ycab':box('c:#e8b521',X,0,Z,Wd,.88,D,{top:'c:#1b1b1d'});break;
  case 'vanity':box('red',X,0,Z,Wd,.85,D,{top:'marble'});cyl('c:'+o.color,X+Wd/2,.84,Z+.45,.22,.03,16);cyl('c:#cfd8dc',X+Wd/2,1.7,Z+.03,.42,.02,24,Math.PI/2);break;
  case 'toilet':box('c:#f4f4f0',X+.3,0,Z+.08,.4,.85,.2);cyl('c:#f4f4f0',X+.5,0,Z+.5,.22,.42,14);break;
  case 'shower':box('c:#d9dde0',X+Wd-.25,2.1,Z+.1,.2,.06,.2,{cast:false});cyl('c:#bfc5c8',X+Wd-.15,1.2,Z+.1,.03,.95,6);break;
  case 'wardrobe':box('c:#efebe2',X,0,Z,Wd,2.65,D);for(let i=0;i<Wd;i++){box('c:#d8d2c4',X+i+.995,0,Z+D,.01,2.65,.01,{cast:false});box('c:#3a2a20',X+i+.42,1.1,Z+D,.16,.16,.02,{cast:false});}box('c:#d8d2c4',X,2.05,Z+D,Wd,.015,.01,{cast:false});break;
  case 'desk':box('c:#f1ede4',X,.72,Z,Wd,.06,D);box('c:#f1ede4',X+.1,0,Z,Wd-.2,.72,1,{});box('c:#f1ede4',X+.1,0,Z+D-1,Wd-.2,.72,1);break;
  case 'chairA':cyl('c:#9aa0a4',X+.5,0,Z+.5,.04,.45,6);geo('c:#c0651f',new THREE.BoxGeometry(.5,.05,.5),M4(X+.5,.48,Z+.5));geo('c:#c0651f',new THREE.BoxGeometry(.5,.55,.05),M4(X+.5,.75,Z+.25,-.15));break;
  case 'bed':box('wood',X,0,Z,Wd,.35,D);box('c:'+o.color,X+.05,.35,Z+.05,Wd-.1,.28,D-.1);box('c:#ffffff',X+.2,.63,Z+.1,Wd-.4,.14,.45);box('wood',X,0,Z-.08,Wd,1.1,.12);
    if(o.coats){const cs=['#c23a2e','#e2b640','#2f4f8a','#3a3a3a','#7b5b9a','#2f6b4a'];for(let i=0;i<7;i++)box('c:'+cs[i%6],X+.2+hsh(i,1,1)*(Wd-.8),.63,Z+.8+hsh(i,2,2)*(D-1.3),.55,.12+hsh(i,3,3)*.08,.45);}break;
  case 'tvold':box('c:#e8e4dc',X,0,Z,1,.8,1);box('c:#8c9096',X+.15,.8,Z+.2,.7,.5,.6);box('c:#222',X+.2,.86,Z+.81,.6,.4,.01);break;
  case 'piano':box('wood',X,0,Z+.2,.7,1.3,D-.4);box('c:#f4f2ea',X+.7,.72,Z+.25,.22,.05,D-.5);box('wood',X+.7,0,Z+.3,.15,.7,.1);box('wood',X+.7,0,Z+D-.4,.15,.7,.1);break;
  case 'redbench':box('wood',X,.35,Z,.75,.12,D);box('cushion',X+.02,.47,Z+.03,.7,.16,D-.06);box('cushion',X+.02,.6,Z+.03,.18,.55,D-.06);break;
  case 'sculpture':geo('c:#c9ced3',new THREE.CylinderGeometry(.55,.55,.1,32),M4(X+.02,1.7,Z+.5,0,0,Math.PI/2));geo('c:#222',new THREE.TorusGeometry(.3,.06,8,20,3.6),M4(X-.06,1.7,Z+.5,0,Math.PI/2,.4));geo('c:#b3261e',new THREE.SphereGeometry(.12,10,8),M4(X-.06,1.6,Z+.6));break;
  case 'cabinet':box('woodL',X,0,Z,.6,.9,D,{top:'marble'});for(let i=0;i<4;i++)box('c:#d81e1e',X+.6,.25+i*.16,Z+.5+(i%2)*1.6,.05,.06,.06,{cast:false});box('woodL',X,1.6,Z,.4,.7,D);break;
  case 'dtable':box('wood',X+.1,.75,Z+.1,Wd-.2,.07,D-.2);for(const [a,b] of [[.25,.25],[Wd-.35,.25],[.25,D-.35],[Wd-.35,D-.35]])box('wood',X+a,0,Z+b,.1,.75,.1);break;
  case 'fireplace':box('wood',X,0,Z,Wd,2.75,D);box('c:#161110',X+.8,.3,Z+D-.01,1.4,.9,.02,{cast:false});box('c:#a77d2a',X+.75,.25,Z+D,1.5,.06,.03,{cast:false});box('woodL',X-.2,0,Z+D,Wd+.4,.28,.35);break;
  case 'fireplaceO':box('orange',X,0,Z,Wd,2.75,D);box('c:#161110',X+.45,.35,Z+D-.01,1.1,.85,.02,{cast:false});box('wood',X-.1,0,Z+D,Wd+.2,.3,.4);break;
  case 'sofaP':{const c='c:#4a2340';box(c,X+.1,0,Z,.85,.45,D);box(c,X+.05,0,Z,.3,.95,D);box(c,X+.1,0,Z-.05,.85,.65,.25);box(c,X+.1,0,Z+D-.2,.85,.65,.25);box('c:#5e2f52',X+.35,.45,Z+.25,.55,.12,D-.5);box('c:#e6dfcc',X+.35,.55,Z+1.3,.18,.45,.45);break;}
  case 'sofaB':{const c='c:#1f6a8a';box(c,X+.1,0,Z,.85,.45,D);box(c,X+.6,0,Z,.35,.95,D);break;}
  case 'tvstand':box('c:#151515',X+.1,0,Z+.1,.8,.6,.8);box('c:#111',X+.15,.6,Z+.2,.12,.7,.6);break;
  case 'cooler':box('c:'+o.color,X+.15,0,Z+.2,.7,.5,.6);box('c:#f2f2ee',X+.13,.5,Z+.18,.74,.1,.64);break;
  case 'relief':box('board',X,0,Z,Wd,2.7,.5);for(let i=0;i<26;i++)box('c:#6c7350',X+.1+hsh(i,1,1)*(Wd-.6),.6+hsh(i,2,2)*1.9,Z+.5,.25+hsh(i,3,3)*.4,.15+hsh(i,4,4)*.35,.07+hsh(i,5,5)*.08,{cast:false});break;
  case 'sofaC':{const wf='wood',S=o.face==='S';box(wf,X,0,Z,Wd,.4,D);box('c:#e8dfc3',X+.08,.4,Z+.05,Wd-.16,.18,D-.1);box('c:#e8dfc3',X+.08,.55,S?Z+.02:Z+D-.32,Wd-.16,.5,.3);box(wf,X,0,Z,.12,.7,D);box(wf,X+Wd-.12,0,Z,.12,.7,D);break;}
  case 'armchair':{box('wood',X+.05,0,Z+.05,.9,.38,.9);box('c:#e8dfc3',X+.12,.38,Z+.12,.76,.16,.76);const bx=o.face==='E'?X+.05:X+.65;box('c:#e8dfc3',bx,.5,Z+.12,.3,.55,.76);box('wood',X+.05,0,Z+.05,.9,.62,.1);box('wood',X+.05,0,Z+.85,.9,.62,.1);break;}
  case 'ctable':box('wood',X+.1,0,Z+.1,Wd-.2,.42,D-.2);quad('glass',X+.12,.43,Z+D-.12,Wd-.24,0,0,0,0,-(D-.24),false);cyl('c:#4a4f55',X+Wd/2,.43,Z+.5,.13,.22,10);ball('c:#3f8a3a',X+Wd/2,.85,Z+.5,.25,1,1.2,1);break;
  case 'vase':geo('c:#8a4e2c',new THREE.LatheGeometry([0,.25,.36,.38,.3,.22,.26].map((r,i)=>new THREE.Vector2(r,i*.2)),16),M4(X+.5,0,Z+.5));cyl('c:#2a180e',X+.5,.95,Z+.5,.22,.25,12,0,0,.26);break;
  case 'sideboard':box('wood',X,0,Z,Wd,.85,D,{top:'marble'});break;
  case 'speaker':box('c:#161616',X+.15,0,Z+.15,.7,1.15,.7);cyl('c:#333',X+.5,.3,Z+.86,.2,.02,14,Math.PI/2);cyl('c:#333',X+.5,.8,Z+.86,.13,.02,14,Math.PI/2);break;
  case 'fern':cyl('c:#5a3218',X+.5,0,Z+.5,.25,.45,10,0,0,.32);for(let i=0;i<14;i++){const a=i/14*6.28;geo('c:#4f9a3a',new THREE.ConeGeometry(.07,.9,4),M4(X+.5+Math.cos(a)*.3,.75,Z+.5+Math.sin(a)*.3,Math.sin(a)*1.1,0,-Math.cos(a)*1.1));}
    cyl('c:#333',X+.5,2.3,Z+2,.01,.9,3);for(let i=0;i<12;i++){const a=i/12*6.28;geo('c:#4f9a3a',new THREE.ConeGeometry(.06,1,4),M4(X+.5+Math.cos(a)*.25,1.9,Z+2+Math.sin(a)*.25,Math.PI+Math.sin(a)*.5,0,-Math.cos(a)*.5));}break;
  case 'dresser':box('wood',X,0,Z,.6,.9,D);for(let i=0;i<3;i++)box('c:#e2d2a8',X+.6,.15+i*.25,Z+.2,.01,.18,D-.4,{cast:false});break;
  case 'isopor':box('c:#efefea',X+.1,0,Z+.15,Wd-.2,.5,D-.3);box('c:#f8f8f5',X+.08,.5,Z+.13,Wd-.16,.08,D-.26);break;
  case 'trash':cyl('c:#cfd2d2',X+.5,0,Z+.5,.3,.8,14);cyl('c:#c43a32',X+.5,.8,Z+.5,.33,.12,14);break;
  case 'pot':cyl('c:#b8603f',X+Wd/2,0,Z+D/2,.6,.75,16,0,0,.8);for(let i=0;i<10;i++)ball(i%3?'c:#3f8a3a':'c:#e2342c',X+Wd/2+rand(-.5,.5),.9+rand(0,.5),Z+D/2+rand(-.5,.5),i%3?.3:.12);break;
  case 'chairP':{const c='c:'+o.color;box(c,X+.25,.42,Z+.25,.5,.05,.5);box(c,X+.25,.45,Z+.2,.5,.5,.06);for(const [a,b] of [[.27,.27],[.69,.27],[.27,.69],[.69,.69]])box(c,X+a,0,Z+b,.04,.42,.04);break;}
  case 'grill':box('brick',X,0,Z,Wd,1,D);box('c:#2a2a2a',X+.3,1,Z+.3,Wd-.6,.05,D-.6);box('e:#ff6a1a',X+.5,.97,Z+.5,Wd-1,.04,D-1,{cast:false});box('brick',X+.6,1,Z,Wd-1.2,2.1,.6);box('brick',X+1.1,3.1,Z+.1,.8,1,.4);
    for(let i=0;i<5;i++)box('c:#6e2a1a',X+.6+i*.4,1.06,Z+.6,.3,.08,.08);break;
  case 'bbqtable':box('woodL',X+.1,.75,Z+.2,Wd-.2,.08,D-.4);for(const [a,b] of [[.3,.3],[Wd-.4,.3],[.3,D-.4],[Wd-.4,D-.4]])box('woodL',X+a,0,Z+b,.1,.75,.1);
    for(let i=0;i<5;i++){cyl('c:#f2efe6',X+.5+i*.7,.83,Z+.6+(i%2)*.7,.18,.02,12);box('c:#8b3a1a',X+.4+i*.7,.85,Z+.55+(i%2)*.7,.22,.05,.08);}for(let i=0;i<4;i++)cyl('c:#e8b030',X+.6+i*.9,.83,Z+1.4,.05,.18,8);break;
  case 'trashbags':ball('c:#18181a',X+.5,.35,Z+.5,.42,1,.9,1);ball('c:#18181a',X+1.4,.32,Z+.5,.4,1,.85,1);break;
  case 'tree':{cyl('c:#5a3d25',X+.5,0,Z+.5,.22,3.4,8,0,0,.15);const g=['c:#3c7d32','c:#2f6a2a','c:#4b8f3a','c:#356f2c'];for(let i=0;i<5;i++)ball(g[i%4],X+.5+rand(-1,1),3.6+rand(0,1.6),Z+.5+rand(-1,1),rand(1.2,1.8),1,.85,1,1);break;}
  }
}

/* ============ cerveja: lugares onde procurar ============ */
const SPECIFIC={'geladeira':['Só maionese e um pudim.','Tem refri. Só refri.'],'freezer da garagem':['Só gelo e um saco de pão.'],'freezer do deck':['Alguém já limpou esse freezer.'],'churrasqueira':['Só carvão e um choripan esquecido.'],'mesa do choripan':['Pegou um choripan. Bom, mas não é cerveja.'],'pilha de casacos na cama':['Achou um isqueiro e uma chave de carro.'],'mesa de jantar':['Só farelo de salgadinho.'],'vasão de cerâmica':['Escuro e vazio lá dentro.'],'atrás da caixa de som':['Só fio. Muito fio.'],'porta-malas do carro':['Estepe e cabo de chupeta.'],'dentro do piano':['Plim. Nada.'],'tanque cheio de gelo':['Só gelo boiando.'],'lareira':['Só cinza.']};
const GENERIC=['Nada. Só gelo derretido.','Vazio. Alguém foi mais rápido.','Achou uma tampinha. Só a tampinha.','Nada aqui, {P}.','Só lata vazia.','Tinha uma, mas já beberam.'];
const spots=OBJ.filter(o=>o.spot).map(o=>({o,name:o.spot.n,w:o.spot.w||1,beer:false,cool:0,cx:o.x+o.w/2,cz:o.z+o.d/2}));
function nearestSpot(px,pz){let best=null,bd=1e9;for(const s of spots){const ex=clamp(px,s.o.x,s.o.x+s.o.w),ez=clamp(pz,s.o.z,s.o.z+s.o.d);const d=Math.hypot(px-ex,pz-ez);if(d<.95&&d<bd){bd=d;best=s;}}return best;}

/* ============ pessoas ============ */
const NAMES=['Gabriel de Castro','Bianca','pedro luiz','enzo lino','Gonçalo','Brenda','Romanato','valentilt','Athur','matheus dalbem','art','(Catatau) Oliveira','lo','Zenker','Padoa','Maria','José','Verena','Lucas','mari lumi','miguel','Teo','Joca vitor','leo','Catatau','mateus','Paco','Be Castro','Gabriel Paim','Flakes','Bits','Lucas','Antônio','Spena','Nanda','Otto','luizao','carol prado','lucas r','babi','Alemão','Helena','Dudu','Joaquim','João','Cássio','Lara','Andreas','Marcela','Henrique','heme','gigicao','vic muller','ju','julia','ceci','fred','dudinha','helena','Paula','eric hendrix','mateus mossmann','faci','Dubal','ana bayer','karina','gabu','Gabi cezar','veronika','Paulo','Muri','Joao Krey','Bryan','Gustavo','Eduarda','Xande','Menegas','Juliano','Rafaella','cecil','junior','Giulia','Isa','Guilherme','Vaz','Joao','Paris','isa','sergio','gabriel','anna','Nadruz','Manu','Kalil','Afonso','Gabriel S','Giovana M','giordano','Antonio','Farilio','Torry','Giovanni','Gab Lucena','matheus','joaquim','matheus r.','Patrick','ane','Fernando','rafa','Duda war','Laura','gabriel 2','Artur C','João Bossa Velha','Bibi','Bárbara','Lima','Gustavo Duarte','pedro','gabo','kittor','Maria Fernanda H.','Gabriel Castellan','Laura Manfroi','Giselle Furtado','Juliana Ferrari','Eduarda Laitano','Vivian','bruna ayu'];
const LOWER=new Set(['de','da','do','dos','das','e']);
const disp=n=>n.split(' ').map((w,i)=>{if(i>0&&LOWER.has(w.toLowerCase()))return w.toLowerCase();if(w.startsWith('('))return '('+w.charAt(1).toUpperCase()+w.slice(2);return w.charAt(0).toUpperCase()+w.slice(1);}).join(' ');
const SKINS=['#f3d0b0','#eec3a0','#e0ac85','#c98e64','#a8704a','#8a5636','#6b4128','#f6dcc4'];
const HAIRC=['#1c120c','#2a1a10','#3b2415','#5a3a1e','#7a4a22','#a8743a','#d6b06a','#e8d9b0','#8c2f1c','#111111','#6d6d6d'];
const STYLES=['short','short','curly','long','long','bun','pony','cap','buzz','bucket','afro','mullet'];
const SHIRTS=['#f1ece0','#121214','#2b2d3a','#d9c3a0','#7d9a7a','#b5543c','#e8b23a','#3f5f9a','#c45f8a','#9a86c4','#3c6e6a','#e98a5a','#6b4a3a','#d8d8d0','#a22b2b','#5c7b3a','#f2a7b8','#1f4f6e'];
const PANTS=['#2b3240','#1d1d22','#4a4f5c','#d9cdb2','#6b5a44','#33405e','#8b8b85','#3a2e28','#e8e2d4','#5b6a4a'];
const PATTERN=['plain','plain','plain','stripe','stripe','floral','check','dots','dress','dress','tank','overshirt'];
function makeLook(seed){const r=mulberry(seed),p=a=>a[Math.floor(r()*a.length)];
  const L={skin:p(SKINS),hair:p(HAIRC),style:p(STYLES),shirt:p(SHIRTS),pants:p(PANTS),pat:p(PATTERN),shoes:p(['#1d1d1d','#efefe8','#6a3e22','#c23a2e','#2b3a5a'])};
  L.acc=p(SHIRTS);L.cap=p(['#c23a2e','#1d1d22','#e8e2d4','#3f5f9a','#5c7b3a','#e8b23a']);
  if(r()<.22)L.shades=true;if(r()<.18)L.stache=true;if(r()<.22)L.beard=true;if(r()<.15)L.bag=p(['#6a3e22','#1d1d1d','#d9c3a0']);if(r()<.3)L.long=true;L.h=.92+r()*.16;L.seed=seed;return L;}
const PEPE_LOOK={skin:'#efc4a0',hair:'#3b2415',style:'curly',shirt:'#4e6a3a',pants:'#2b3240',pat:'knit',shoes:'#1d1d1d',stache:true,beard:true,long:true,h:1.02,seed:7};
const MAE_LOOK={skin:'#f1cdb0',hair:'#e6dcc0',style:'long',shirt:'#55575c',pants:'#2f3138',pat:'plain',shoes:'#1d1d1d',smile:true,h:1.13,seed:21};
const PAI_LOOK={skin:'#e9bc98',hair:'#8d8984',style:'short',shirt:'#f2f2ee',pants:'#3a4250',pat:'plain',shoes:'#e8e8e2',beard:true,smile:true,h:1.17,seed:22};
const GAEL_LOOK={skin:'#f0c9a6',hair:'#7a4f2c',style:'curlytop',shirt:'#17171a',pants:'#3a3f4a',pat:'plain',shoes:'#e8e8e2',backpack:'#8b9097',smile:true,long:true,h:1.0,seed:9};

const PMAT=new THREE.MeshLambertMaterial({vertexColors:true});
const FACES=[[[1,0,1],[0,0,-1],[0,1,0]],[[0,0,0],[0,0,1],[0,1,0]],[[0,0,1],[1,0,0],[0,1,0]],[[1,0,0],[-1,0,0],[0,1,0]],[[0,1,1],[1,0,0],[0,0,-1]],[[0,0,0],[1,0,0],[0,0,1]]];
function cb(a,x,y,z,w,h,d,col){const c=lin(col);
  for(const [o,r,u] of FACES){const ox=x+o[0]*w,oy=y+o[1]*h,oz=z+o[2]*d,rx=r[0]*w,ry=r[1]*h,rz=r[2]*d,ux=u[0]*w,uy=u[1]*h,uz=u[2]*d;
    let nx=ry*uz-rz*uy,ny=rz*ux-rx*uz,nz=rx*uy-ry*ux;const nl=Math.hypot(nx,ny,nz)||1;nx/=nl;ny/=nl;nz/=nl;
    const P=[[ox,oy,oz],[ox+rx,oy+ry,oz+rz],[ox+rx+ux,oy+ry+uy,oz+rz+uz],[ox,oy,oz],[ox+rx+ux,oy+ry+uy,oz+rz+uz],[ox+ux,oy+uy,oz+uz]];
    for(const q of P){a.p.push(q[0],q[1],q[2]);a.n.push(nx,ny,nz);a.c.push(c.r,c.g,c.b);}}}
function gfrom(a){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(a.p,3));g.setAttribute('normal',new THREE.Float32BufferAttribute(a.n,3));g.setAttribute('color',new THREE.Float32BufferAttribute(a.c,3));g.computeBoundingSphere();return g;}
function hairInto(a,L,r){
  const Hc=L.hair,hl=shade(Hc,28),s=L.style;
  if(s==='curly'||s==='afro'||s==='curlytop'){
    const big=s==='afro'?1.35:1,n=s==='curlytop'?16:26;
    cb(a,-.2,1.98,-.2,.4,.08,.4,Hc);
    for(let i=0;i<n;i++){const top=s==='curlytop'||i<16;const sz=(.1+r()*.05)*big;let x,y,z;
      if(top){x=(r()-.5)*.42*big;z=(r()-.5)*.42*big-.02;y=1.99+r()*.12*big;}else{const side=r();if(side<.5){x=(r()<.5?-1:1)*(.18+r()*.04)*big;z=(r()-.6)*.36;y=1.8+r()*.2;}else{x=(r()-.5)*.4;z=-.2-r()*.05*big;y=1.72+r()*.28;}}
      cb(a,x-sz/2,y,z-sz/2,sz,sz,sz,r()<.3?hl:Hc);}
    return;}
  if(s==='bald')return;
  if(s==='buzz'){cb(a,-.185,1.96,-.185,.37,.07,.37,shade(Hc,12));return;}
  if(s==='cap'||s==='bucket'){cb(a,-.2,1.97,-.2,.4,.13,.4,L.cap);if(s==='bucket')cb(a,-.25,1.96,-.25,.5,.03,.5,shade(L.cap,-20));else cb(a,-.18,1.97,.18,.36,.03,.16,shade(L.cap,-25));cb(a,-.19,1.8,-.19,.38,.17,.06,Hc);return;}
  cb(a,-.195,1.97,-.195,.39,.1,.39,Hc);cb(a,-.195,1.78,-.2,.39,.22,.07,Hc);cb(a,-.2,1.86,-.18,.04,.14,.3,Hc);cb(a,.16,1.86,-.18,.04,.14,.3,Hc);
  if(s==='long'){cb(a,-.21,1.5,-.22,.42,.5,.09,Hc);cb(a,-.21,1.55,-.15,.05,.4,.2,Hc);cb(a,.16,1.55,-.15,.05,.4,.2,Hc);}
  else if(s==='bun')cb(a,-.08,2.04,-.2,.16,.14,.14,Hc);
  else if(s==='pony')cb(a,-.05,1.55,-.28,.1,.4,.08,Hc);
  else if(s==='mullet')cb(a,-.17,1.55,-.22,.34,.3,.08,Hc);
}
function buildPerson(L){
  const r=mulberry(L.seed||1),body={p:[],n:[],c:[]},S=L.shirt;
  cb(body,-.28,.9,-.15,.56,.7,.3,S);
  if(L.pat==='stripe')for(let i=0;i<4;i++)cb(body,-.285,1.0+i*.15,-.155,.57,.05,.31,L.acc);
  if(L.pat==='floral'||L.pat==='dots')for(let i=0;i<14;i++)cb(body,-.27+r()*.5,.95+r()*.6,.152,.05,.05,.01,L.acc);
  if(L.pat==='check'){for(let i=0;i<5;i++)cb(body,-.285,.95+i*.13,-.155,.57,.025,.31,shade(S,-35));for(let i=0;i<5;i++)cb(body,-.25+i*.12,.9,.151,.025,.7,.01,shade(S,-35));}
  if(L.pat==='overshirt'){cb(body,-.29,.9,.12,.17,.7,.04,L.acc);cb(body,.12,.9,.12,.17,.7,.04,L.acc);}
  if(L.pat==='knit'){for(let i=0;i<4;i++)cb(body,-.12+i*.08,.95,.151,.02,.6,.01,shade(S,-18));cb(body,-.29,.9,-.16,.58,.06,.32,shade(S,-12));cb(body,-.15,1.55,-.1,.3,.06,.24,shade(S,12));}
  if(L.pat==='dress')cb(body,-.32,.5,-.19,.64,.45,.38,S);
  if(L.pat==='tank'){cb(body,-.285,1.4,-.155,.12,.2,.31,L.skin);cb(body,.165,1.4,-.155,.12,.2,.31,L.skin);}
  if(L.backpack){cb(body,-.21,1.0,-.34,.42,.5,.19,L.backpack);cb(body,-.2,1.05,-.33,.4,.05,.03,'#5a5f66');cb(body,-.22,1.1,-.16,.06,.48,.32,shade(L.backpack,-15));cb(body,.16,1.1,-.16,.06,.48,.32,shade(L.backpack,-15));}
  if(L.bag){cb(body,.2,.95,-.05,.14,.18,.1,L.bag);cb(body,-.25,1.0,.151,.5,.03,.01,L.bag);}
  cb(body,-.07,1.58,-.07,.14,.1,.14,L.skin);
  cb(body,-.18,1.66,-.18,.36,.38,.36,L.skin);
  cb(body,-.03,1.76,.18,.06,.07,.04,shade(L.skin,-12));
  if(L.shades)cb(body,-.17,1.83,.18,.34,.07,.02,'#0e0e10');
  else{cb(body,-.115,1.83,.18,.06,.05,.012,'#1a1210');cb(body,.055,1.83,.18,.06,.05,.012,'#1a1210');cb(body,-.12,1.9,.18,.08,.02,.012,shade(L.hair,-10));cb(body,.045,1.9,.18,.08,.02,.012,shade(L.hair,-10));}
  if(L.beard){const bc=shade(L.hair,8);cb(body,-.185,1.66,.12,.37,.1,.07,bc);cb(body,-.185,1.66,-.1,.04,.18,.25,bc);cb(body,.145,1.66,-.1,.04,.18,.25,bc);}
  if(L.stache)cb(body,-.1,1.74,.18,.2,.035,.025,L.hair);
  if(L.smile)cb(body,-.07,1.71,.18,.14,.03,.012,'#ffffff');else cb(body,-.06,1.71,.18,.12,.02,.012,'#8a4a40');
  hairInto(body,L,r);
  const leg={p:[],n:[],c:[]};cb(leg,-.1,-.82,-.11,.2,.82,.22,L.pat==='dress'?L.skin:L.pants);cb(leg,-.11,-.92,-.12,.22,.1,.31,L.shoes);
  if(L.pat==='dress')cb(leg,-.105,-.4,-.115,.21,.4,.23,L.skin);
  const arm={p:[],n:[],c:[]};const sl=L.pat==='tank'?L.skin:S;cb(arm,-.075,-.36,-.08,.15,.38,.16,sl);cb(arm,-.07,-.6,-.075,.14,.25,.15,L.long&&L.pat!=='tank'?sl:L.skin);cb(arm,-.065,-.68,-.07,.13,.1,.14,L.skin);
  const g=new THREE.Group(),bodyM=new THREE.Mesh(gfrom(body),PMAT);g.add(bodyM);
  const lg=gfrom(leg),ag=gfrom(arm);
  const mk=(geom,x,y)=>{const p=new THREE.Group();p.position.set(x,y,0);const m=new THREE.Mesh(geom,PMAT);p.add(m);g.add(p);return p;};
  const legL=mk(lg,-.12,.92),legR=mk(lg,.12,.92),armL=mk(ag,-.36,1.55),armR=mk(ag,.36,1.55);
  const can=new THREE.Mesh(CANGEO,CANMAT);can.position.set(0,-.7,.06);can.visible=false;armR.add(can);
  const cig=new THREE.Mesh(CIGGEO,CIGMAT);cig.position.set(0,-.7,.12);cig.rotation.x=1.4;cig.visible=false;armR.add(cig);
  g.scale.setScalar(L.h||1);
  const parts=[bodyM,legL.children[0],legR.children[0],armL.children[0],armR.children[0]];
  return{g,legL,legR,armL,armR,can,cig,parts};
}
const CANGEO=new THREE.CylinderGeometry(.055,.055,.17,10),CANMAT=new THREE.MeshPhongMaterial({color:lin('#e8b030'),shininess:90,specular:0xffffff});
const CIGGEO=new THREE.CylinderGeometry(.012,.012,.12,5),CIGMAT=new THREE.MeshBasicMaterial({color:0xffffff});

/* ============ estado ============ */
const game={state:'title',time:0,beers:0,caught:0,met:new Set(),beerTimer:0};
const P={ph:0,x:24.5,z:28.5,rot:Math.PI,look:PEPE_LOOK,state:'free',timer:0,immune:0,holding:false,say:'',sayT:0,hic:8,shake:0,moving:false,t:0,speed:0,jump:0};
let npcs=[],gael=null,inter=null,broCool=12,chaseGap=4,toastT=0,flash=0;

function addPerson(e){const m=buildPerson(e.look);e.m=m;scene.add(m.g);m.g.position.set(e.x,0,e.z);m.g.rotation.y=e.rot||0;return e;}

const INTER={
  foto:{need:6,lines:['FOTO! Sorri, {P}!','Mais uma, essa tremeu!','Faz um joinha pra foto!'],flash:true},
  selfie:{need:7,lines:['Selfie com o aniversariante!','Todo mundo junto, vem!'],flash:true},
  parabens:{need:7,lines:['PARABÉÉÉNS, {PU}!!','Feliz aniversário, guri!','Parabéns pros dois irmãos!','Muitos anos de vida, {P}!','Cadê o {B}? Parabéns pra vocês!']},
  abraco:{need:8,lines:['Vem cá, me dá um abraço!','Ai, que saudade de ti!','Abraço de aniversário!']},
  historia:{need:10,lines:['{P}, lembra daquela vez...?','Deixa eu te contar uma coisa...','E aí, como tão as coisas?','{P}, tu tá namorando?']},
  danca:{need:8,lines:['Vem dançar, aniversariante!','Essa é a tua música, {P}!']},
  churras:{need:6,lines:['Prova esse choripan, {P}!','Pega um choripan, tá no ponto!']},
  carro:{need:6,lines:['{P}, segura a lanterna aqui!','Tu entende de motor?']},
  piano:{need:7,lines:['Canta comigo, {P}!','Pede uma música, aniversariante!']},
};
const BYE=['Manda um abraço pro {B}!','Te amo, {P}!','Aproveita, guri!','Depois a gente conversa!','Ficou ótima!','Feliz aniversário!','Vai lá, vai!'];
const GIFT=['Toma uma gelada, é teu dia!','Pega essa, tá trincando!','Presente: uma geladinha!'];
const FACE={N:Math.PI,S:0,E:Math.PI/2,W:-Math.PI/2};

function freeTiles(x,z,w,h){const a=[];for(let j=z;j<z+h;j++)for(let i=x;i<x+w;i++)if(inb(i,j)&&!solid[I(i,j)])a.push([i,j]);return a;}
const ZONES=[
  {k:'dance',tiles:freeTiles(23,15,4,4).concat(freeTiles(30,15,3,3)).concat(freeTiles(15,20,6,5)),n:16},
  {k:'churras',tiles:freeTiles(5,31,11,8),n:12},
  {k:'deck',tiles:freeTiles(14,27,20,4),n:16},
  {k:'lawn',tiles:freeTiles(5,31,40,15),n:30},
  {k:'kitchen',tiles:freeTiles(6,6,8,5),n:8},
  {k:'hall',tiles:freeTiles(6,14,7,7).concat(freeTiles(6,21,7,5)),n:10},
  {k:'corr',tiles:freeTiles(6,12,36,2),n:7},
  {k:'garage',tiles:freeTiles(1,2,20,2).concat(freeTiles(2,4,3,26)),n:9},
  {k:'side',tiles:freeTiles(45,1,9,10).concat(freeTiles(49,12,5,30)),n:8},
  {k:'room',tiles:freeTiles(25,6,6,3).concat(freeTiles(35,15,3,4)).concat(freeTiles(32,6,4,2)),n:6},
];
const WANDER=[];for(const z of ZONES)for(const t of z.tiles)WANDER.push(t);
function mkNPC(name,look){return{name,look,x:0,z:0,hx:0,hz:0,rot:0,face:0,t:Math.random()*10,ph:Math.random()*6,moving:false,mode:'home',path:null,cool:rand(4,14),fan:.5,types:['parabens','foto'],act:'chat',say:'',sayT:0,present:false,wander:false,wt:rand(3,10),jump:0,cig:false,holding:false,repath:0,chaseT:0,puff:rand(0,2),speedNow:0};}
function setupNPCs(){
  for(const e of npcs)scene.remove(e.m.g);npcs=[];
  const used=new Set(),names=NAMES.slice();for(let i=names.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[names[i],names[j]]=[names[j],names[i]];}
  let idx=0;const take=()=>names[idx++];const key=t=>t[0]+','+t[1];
  const special=[
    {at:[8,35],act:'churras',face:'N',types:['churras','parabens'],fan:.6},{at:[10,34],act:'churras',face:'W',types:['churras','historia'],fan:.4},
    {at:[11,15],act:'piano',face:'E',types:['piano','parabens'],fan:.4},
    {at:[7,19],act:'kiss',face:'E',fan:0},{at:[8,19],act:'kiss',face:'W',fan:0},
    {at:[45,38],act:'kiss',face:'E',fan:0},{at:[46,38],act:'kiss',face:'W',fan:0},
    {at:[7,2],act:'carro',face:'N',types:['carro'],fan:.25},
    {at:[22,35],act:'ball',face:'E',types:['parabens','abraco'],fan:.3},{at:[27,35],act:'ball',face:'W',types:['foto','parabens'],fan:.3},
  ];
  for(const s of special){const name=take();const e=mkNPC(name,makeLook(strSeed(name+idx)));e.hx=s.at[0]+.5;e.hz=s.at[1]+.5;e.act=s.act;e.face=FACE[s.face];e.types=s.types||['parabens'];e.fan=s.fan;used.add(key(s.at));npcs.push(e);}
  for(const z of ZONES){let left=z.n;let guard=0;while(left>0&&idx<names.length&&guard++<60){const opts=z.tiles.filter(t=>!used.has(key(t)));if(!opts.length)break;const base=pick(opts);used.add(key(base));const members=[base];const g=Math.min(left,2+Math.floor(Math.random()*3));
      for(let k=1;k<g;k++){const near=z.tiles.filter(t=>!used.has(key(t))&&Math.abs(t[0]-base[0])<=2&&Math.abs(t[1]-base[1])<=1);if(!near.length)break;const t=pick(near);used.add(key(t));members.push(t);}
      const cx=members.reduce((a,t)=>a+t[0],0)/members.length,cz=members.reduce((a,t)=>a+t[1],0)/members.length;
      for(const t of members){if(idx>=names.length)break;const name=take();const e=mkNPC(name,makeLook(strSeed(name+idx)));e.hx=t[0]+.5+rand(-.15,.15);e.hz=t[1]+.5+rand(-.15,.15);
        const dx=cx-t[0],dz=cz-t[1];e.face=(dx||dz)?Math.atan2(dx,dz):rand(-3,3);
        e.act=z.k==='dance'?'dance':((z.k==='churras'||z.k==='lawn')&&Math.random()<.2?'smoke':'chat');e.cig=e.act==='smoke';
        e.types=z.k==='dance'?['danca','foto','selfie']:pick([['parabens','foto'],['abraco','parabens'],['historia','parabens'],['selfie','foto'],['historia','abraco'],['foto','abraco','parabens']]);
        e.fan=z.k==='room'?.2:rand(.35,1);if(Math.random()<.4&&!e.cig)e.holding=true;npcs.push(e);}
      left-=members.length;}}
  while(idx<names.length){const name=take();const e=mkNPC(name,makeLook(strSeed(name+idx)));const t=pick(WANDER);e.hx=t[0]+.5;e.hz=t[1]+.5;e.wander=true;e.fan=rand(.6,1);e.types=pick([['foto','selfie'],['parabens','abraco'],['historia','parabens']]);npcs.push(e);}
  for(const e of npcs)if(e.act==='chat'&&Math.random()<.12)e.wander=true;
  gael=mkNPC('Gael',GAEL_LOOK);gael.bro=true;gael.wander=true;gael.fan=0;gael.hx=19.5;gael.hz=28.5;npcs.push(gael);
  for(const [nm,lk,x,z] of [['Mãe',MAE_LOOK,9.5,13.5],['Pai',PAI_LOOK,24.5,29.5]]){const e=mkNPC(nm,lk);e.parent=true;e.wander=true;e.fan=0;e.hx=x;e.hz=z;e.cool=rand(20,35);npcs.push(e);}
  const order=npcs.filter(e=>e!==gael&&!e.parent).sort(()=>Math.random()-.5);
  order.forEach((e,i)=>{if(i<50||(e.act!=='chat'&&e.act!=='dance'&&e.act!=='smoke')){e.present=true;e.x=e.hx;e.z=e.hz;e.rot=e.face;}else{e.present=false;e.arriveAt=4+(i-50)*.95;}});
  gael.present=true;gael.x=gael.hx;gael.z=gael.hz;for(const e of npcs)if(e.parent){e.present=true;e.x=e.hx;e.z=e.hz;}
  for(const e of npcs){addPerson(e);e.m.g.visible=e.present;e.m.can.visible=e.holding;e.m.cig.visible=e.cig;}
}

/* ============ caminhos ============ */
const prev=new Int32Array(W*H),queue=new Int32Array(W*H);
function findPath(sx,sz,tx,tz){
  const s=I(Math.floor(sx),Math.floor(sz)),t=I(Math.floor(tx),Math.floor(tz));if(s===t)return[];
  prev.fill(-1);prev[s]=s;let h=0,q=0;queue[q++]=s;
  while(h<q){const cur=queue[h++];if(cur===t)break;const cx=cur%W,cz=(cur/W)|0;
    for(const [dx,dz] of [[1,0],[-1,0],[0,1],[0,-1]]){const nx=cx+dx,nz=cz+dz;if(!inb(nx,nz))continue;const ni=I(nx,nz);if(prev[ni]!==-1)continue;if(solid[ni]&&ni!==t)continue;prev[ni]=cur;queue[q++]=ni;}}
  if(prev[t]===-1)return null;const path=[];let cur=t;while(cur!==s){path.push({x:(cur%W)+.5,z:((cur/W)|0)+.5});cur=prev[cur];if(path.length>500)break;}return path.reverse();
}
function losClear(a,b){const n=Math.ceil(Math.hypot(a.x-b.x,a.z-b.z)/.3);for(let i=1;i<n;i++){const x=a.x+(b.x-a.x)*i/n,z=a.z+(b.z-a.z)*i/n;if(blocksView(Math.floor(x),Math.floor(z)))return false;}return true;}
const dist=(a,b)=>Math.hypot(a.x-b.x,a.z-b.z);

/* ============ áudio ============ */
let AC=null,master=null,muted=false,musicNext=0,musicStep=0,noiseBuf=null;
function audioInit(){if(AC)return;try{AC=new(window.AudioContext||window.webkitAudioContext)();master=AC.createGain();master.gain.value=.5;master.connect(AC.destination);}catch(e){AC=null;}}
function tone(f,d,type='square',v=.12,when=0,slide=0){if(!AC||muted)return;const t=AC.currentTime+when,o=AC.createOscillator(),g=AC.createGain();o.type=type;o.frequency.setValueAtTime(f,t);if(slide)o.frequency.exponentialRampToValueAtTime(Math.max(30,slide),t+d);g.gain.setValueAtTime(v,t);g.gain.exponentialRampToValueAtTime(.0001,t+d);o.connect(g);g.connect(master);o.start(t);o.stop(t+d+.02);}
function noiz(d,v=.15,hp=2000,when=0,bp=0){if(!AC||muted)return;if(!noiseBuf){noiseBuf=AC.createBuffer(1,AC.sampleRate*.5,AC.sampleRate);const a=noiseBuf.getChannelData(0);for(let i=0;i<a.length;i++)a[i]=Math.random()*2-1;}const t=AC.currentTime+when,s=AC.createBufferSource();s.buffer=noiseBuf;const f=AC.createBiquadFilter();f.type=bp?'bandpass':'highpass';f.frequency.value=bp||hp;const g=AC.createGain();g.gain.setValueAtTime(v,t);g.gain.exponentialRampToValueAtTime(.0001,t+d);s.connect(f);f.connect(g);g.connect(master);s.start(t);s.stop(t+d+.02);}
const SFX={open:()=>{noiz(.22,.2,3000);tone(1800,.05,'square',.04);},gulp:()=>{for(let i=0;i<3;i++)tone(260,.09,'sine',.18,i*.22,140);},ahh:()=>tone(520,.35,'triangle',.08,0,380),nope:()=>{tone(220,.12,'square',.06);tone(170,.18,'square',.06,.12);},hey:()=>{tone(660,.07,'square',.06);tone(880,.1,'square',.06,.08);},tap:()=>tone(300+Math.random()*200,.04,'square',.05),flash:()=>{noiz(.08,.25,5000);tone(2400,.06,'sine',.06);},free:()=>{tone(523,.08,'square',.07);tone(784,.12,'square',.07,.08);},hic:()=>tone(700,.08,'sine',.12,0,1200),search:()=>noiz(.12,.06,0,0,900)};
const BASS=[45,45,48,50,43,43,47,50];
function musicTick(){if(!AC||muted||game.state!=='play')return;const spb=60/122/4;const near=Math.max(0,1-Math.hypot(P.x-33,P.z-24)/30)*.7+.3;
  while(musicNext<AC.currentTime+.15){const w=musicNext-AC.currentTime,s=musicStep%16,bar=Math.floor(musicStep/16)%8;
    if(s%4===0)tone(140,.14,'sine',.32*near,w,42);if(s%4===2)noiz(.03,.05*near,7000,w);if(s===4||s===12)noiz(.09,.09*near,0,w,1400);
    if(s===0||s===3||s===6||s===10||s===14)tone(440*Math.pow(2,(BASS[bar]-69)/12),.16,'triangle',.11*near,w);
    if((s===7||s===15)&&bar%2)tone(440*Math.pow(2,(BASS[bar]+19-69)/12),.07,'square',.025*near,w);musicNext+=spb;musicStep++;}}
function parabensSong(){if(!AC||muted)return;const N={G4:392,A4:440,B4:494,C5:523,D5:587,E5:659,F5:698,G5:784};const m=[['G4',.75],['G4',.25],['A4',1],['G4',1],['C5',1],['B4',2],['G4',.75],['G4',.25],['A4',1],['G4',1],['D5',1],['C5',2],['G4',.75],['G4',.25],['G5',1],['E5',1],['C5',1],['B4',1],['A4',2],['F5',.75],['F5',.25],['E5',1],['C5',1],['D5',1],['C5',2]];let t=.1;for(const [n,d] of m){tone(N[n],d*.33*.95,'triangle',.12,t);tone(N[n]/2,d*.33*.9,'square',.03,t);t+=d*.33;}}

/* ============ cena: luz, céu, partículas ============ */
const hemi=new THREE.HemisphereLight(0xffd2a8,0x5a4a3a,.7);scene.add(hemi);
const amb=new THREE.AmbientLight(0xffffff,.12);scene.add(amb);
const sun=new THREE.DirectionalLight(0xffb36b,1.6);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);
Object.assign(sun.shadow.camera,{left:-26,right:26,top:26,bottom:-26,near:1,far:160});sun.shadow.bias=-.0006;sun.shadow.normalBias=.02;scene.add(sun);scene.add(sun.target);
const PL=[];for(let i=0;i<6;i++){const l=new THREE.PointLight(0xffc27a,0,11,1.6);scene.add(l);PL.push(l);}
const skyU={top:{value:new THREE.Color()},bot:{value:new THREE.Color()}};
const sky=new THREE.Mesh(new THREE.SphereGeometry(300,24,12),new THREE.ShaderMaterial({uniforms:skyU,side:THREE.BackSide,depthWrite:false,fog:false,
  vertexShader:'varying vec3 vP;void main(){vP=normalize(position);gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
  fragmentShader:'uniform vec3 top;uniform vec3 bot;varying vec3 vP;void main(){float h=clamp(vP.y*1.6+.08,0.,1.);gl_FragColor=vec4(mix(bot,top,pow(h,.7)),1.);}'}));
scene.add(sky);
const sunDisc=new THREE.Mesh(new THREE.CircleGeometry(9,24),new THREE.MeshBasicMaterial({color:0xffd9a0,fog:false,toneMapped:false}));scene.add(sunDisc);
const ground=new THREE.Mesh(new THREE.PlaneGeometry(500,500),(()=>{const t=photoTex('grass');t.repeat.set(125,125);return new THREE.MeshPhongMaterial({map:t,shininess:2});})());
ground.rotation.x=-Math.PI/2;ground.position.y=-.02;ground.receiveShadow=true;scene.add(ground);
// árvores de fundo
const bgTrees=new THREE.Group();for(let i=0;i<70;i++){const a=i/70*6.28+rand(-.05,.05),r=rand(48,80);const x=28+Math.cos(a)*r,z=24+Math.sin(a)*r;const h=rand(5,12);
  const tr=new THREE.Mesh(new THREE.CylinderGeometry(.3,.4,h*.5,6),mat('c:#4a3424'));tr.position.set(x,h*.25,z);bgTrees.add(tr);
  const c=new THREE.Mesh(i%3?new THREE.IcosahedronGeometry(h*.35,1):new THREE.ConeGeometry(h*.3,h*.8,7),mat(pick(['c:#2f5a2a','c:#3a6a30','c:#27502a'])));c.position.set(x,h*.6,z);bgTrees.add(c);}
scene.add(bgTrees);
// varal de lâmpadas
const bulbMat=new THREE.MeshBasicMaterial({color:lin('#ffd27a'),toneMapped:false});const bulbs=new THREE.Group();const wirePts=[];
function stringLights(a,b,n,sag){const pts=[];for(let i=0;i<=n;i++){const t=i/n;const p=new THREE.Vector3(lerp(a[0],b[0],t),lerp(a[1],b[1],t)-Math.sin(t*Math.PI)*sag,lerp(a[2],b[2],t));pts.push(p);const m=new THREE.Mesh(new THREE.SphereGeometry(.06,6,5),bulbMat);m.position.copy(p).y-=.08;bulbs.add(m);}
  bulbs.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts),new THREE.LineBasicMaterial({color:0x222222})));}
stringLights([14.2,2.95,30.8],[33.8,2.95,30.8],30,.0);stringLights([14,2.9,27],[14,2.9,30.8],6,.2);
stringLights([6,3,31],[22,3,37],24,.7);stringLights([22,3,37],[36,3,32],22,.6);stringLights([6,3,31],[6,3,40],12,.4);scene.add(bulbs);
// bola, água
const ballM=new THREE.Mesh(new THREE.SphereGeometry(.16,12,10),new THREE.MeshLambertMaterial({color:0xffffff}));ballM.castShadow=true;scene.add(ballM);
// partículas (sprites)
function spriteTex(draw){const c=document.createElement('canvas');c.width=c.height=64;draw(c.getContext('2d'));const t=new THREE.CanvasTexture(c);return t;}
const SPR={
  smoke:spriteTex(g=>{const gr=g.createRadialGradient(32,32,2,32,32,30);gr.addColorStop(0,'rgba(235,235,235,.8)');gr.addColorStop(1,'rgba(235,235,235,0)');g.fillStyle=gr;g.fillRect(0,0,64,64);}),
  heart:spriteTex(g=>{g.fillStyle='#ff3d6e';g.beginPath();g.moveTo(32,54);g.bezierCurveTo(4,34,10,8,32,22);g.bezierCurveTo(54,8,60,34,32,54);g.fill();}),
  note:spriteTex(g=>{g.fillStyle='#fff';g.beginPath();g.ellipse(24,46,10,8,-.4,0,7);g.fill();g.fillRect(30,10,5,36);g.fillRect(30,10,18,6);}),
  star:spriteTex(g=>{const gr=g.createRadialGradient(32,32,1,32,32,30);gr.addColorStop(0,'rgba(255,240,170,1)');gr.addColorStop(.25,'rgba(255,200,80,.8)');gr.addColorStop(1,'rgba(255,180,60,0)');g.fillStyle=gr;g.fillRect(0,0,64,64);g.fillStyle='#fff8d0';g.fillRect(30,4,4,56);g.fillRect(4,30,56,4);}),
  conf:spriteTex(g=>{g.fillStyle='#fff';g.fillRect(16,16,32,32);}),
};
const parts=[];const partPool=[];
function emit(kind,x,y,z,vx,vy,vz,life,size,color){let s=partPool.pop();if(!s){s=new THREE.Sprite(new THREE.SpriteMaterial({transparent:true,depthWrite:false}));scene.add(s);}
  s.material.map=SPR[kind];s.material.color.set(color||0xffffff);s.material.needsUpdate=true;s.visible=true;s.position.set(x,y,z);s.scale.setScalar(size);parts.push({s,vx,vy,vz,life,max:life,size,kind});}

/* ============ montar o mundo ============ */
buildHouse();for(const o of OBJ)furn(o);
const staticMeshes=[];
for(const [k,b] of BATCH){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(b.p,3));g.setAttribute('normal',new THREE.Float32BufferAttribute(b.n,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(b.u,2));g.computeBoundingSphere();
  const m=new THREE.Mesh(g,mat(k));m.receiveShadow=!k.startsWith('e:')&&k!=='glass';m.castShadow=b.cast&&k!=='glass'&&!k.startsWith('e:')&&k!=='water';if(k==='glass'||k==='water')m.renderOrder=2;scene.add(m);staticMeshes.push(m);}
const pepe=addPerson(P);pepe.m.parts.forEach(p=>p.castShadow=true);

/* ============ entrada ============ */
const keys={};let actPressed=false,camYaw=Math.PI,camPitch=.32,lastLook=0;
addEventListener('keydown',e=>{const k=e.key.toLowerCase();if(['arrowup','arrowdown','arrowleft','arrowright',' '].includes(k))e.preventDefault();if(game.state!=='play')return;if(k==='e'||k===' '||k==='enter'){if(!e.repeat)actPressed=true;return;}keys[k]=true;});
addEventListener('keyup',e=>{keys[e.key.toLowerCase()]=false;});
const joy={id:null,ox:0,oy:0,x:0,y:0,active:false},look={id:null,x:0,y:0};let mouseDrag=null;
const wrap=$('wrap');
wrap.addEventListener('pointerdown',e=>{if(e.target.closest('button'))return;if(game.state!=='play')return;
  if(e.pointerType==='touch'||e.pointerType==='pen'){document.body.classList.add('touch');if(e.clientX<innerWidth*.45&&!joy.active){joy.active=true;joy.id=e.pointerId;joy.ox=joy.x=e.clientX;joy.oy=joy.y=e.clientY;}else if(look.id===null){look.id=e.pointerId;look.x=e.clientX;look.y=e.clientY;}}
  else{mouseDrag={x:e.clientX,y:e.clientY};try{if(!document.pointerLockElement&&canvas.requestPointerLock){const r=canvas.requestPointerLock();if(r&&r.catch)r.catch(()=>{});}}catch(_){}}});
wrap.addEventListener('pointermove',e=>{
  if(joy.active&&e.pointerId===joy.id){joy.x=e.clientX;joy.y=e.clientY;return;}
  if(look.id===e.pointerId){camYaw-=(e.clientX-look.x)*.006;camPitch=clamp(camPitch+(e.clientY-look.y)*.004,.05,1.1);look.x=e.clientX;look.y=e.clientY;lastLook=performance.now();return;}
  if(document.pointerLockElement===canvas){camYaw-=e.movementX*.0032;camPitch=clamp(camPitch+e.movementY*.0025,.05,1.1);lastLook=performance.now();}
  else if(mouseDrag&&e.buttons){camYaw-=(e.clientX-mouseDrag.x)*.006;camPitch=clamp(camPitch+(e.clientY-mouseDrag.y)*.004,.05,1.1);mouseDrag={x:e.clientX,y:e.clientY};lastLook=performance.now();}});
const pend=e=>{if(e.pointerId===joy.id){joy.active=false;joy.id=null;}if(e.pointerId===look.id)look.id=null;mouseDrag=null;};
wrap.addEventListener('pointerup',pend);wrap.addEventListener('pointercancel',pend);
const actBtn=$('act');actBtn.addEventListener('pointerdown',e=>{e.preventDefault();e.stopPropagation();actPressed=true;actBtn.classList.add('press');});
actBtn.addEventListener('pointerup',()=>actBtn.classList.remove('press'));actBtn.addEventListener('pointerleave',()=>actBtn.classList.remove('press'));
addEventListener('touchstart',()=>document.body.classList.add('touch'),{passive:true});

/* ============ UI ============ */
const uc=$('ui'),uctx=uc.getContext('2d');let DPR=1;
function resize(){DPR=Math.min(2,devicePixelRatio||1);const w=innerWidth,h=innerHeight;renderer.setPixelRatio(Math.min(devicePixelRatio||1,w<700?1.25:1.6));renderer.setSize(w,h,false);camera.aspect=w/h;camera.fov=w<h?72:60;camera.updateProjectionMatrix();uc.width=Math.round(w*DPR);uc.height=Math.round(h*DPR);}
addEventListener('resize',resize);resize();
function toast(msg,t=1.8){const el=$('toast');el.textContent=tr(msg);el.classList.add('on');toastT=t;}
const LEVELS=[[0,'Sóbrio'],[1,'Alegrinho'],[3,'Calibrado'],[6,'Trocando as pernas'],[10,'Chapado'],[15,'Virou lenda'],[21,'Fora de controle']];
const lvlName=b=>{let n=LEVELS[0][1];for(const [k,s] of LEVELS)if(b>=k)n=s;return n;};
const drunk=()=>Math.min(1,game.beers/18);
const V=new THREE.Vector3();
function toScreen(x,y,z){V.set(x,y,z).project(camera);if(V.z>1||V.z<-1)return null;return[(V.x*.5+.5)*uc.width,(-V.y*.5+.5)*uc.height];}
function bubble(text,sx,sy,o={}){const c=uctx,fs=Math.round((o.small?12:14)*DPR);c.font=`600 ${fs}px "Pixelify Sans", system-ui, sans-serif`;const w=c.measureText(text).width+14*DPR,h=fs+10*DPR;let x=clamp(sx-w/2,6*DPR,uc.width-w-6*DPR),y=sy-h;
  c.fillStyle='rgba(0,0,0,.85)';c.fillRect(x-2*DPR,y-2*DPR,w+4*DPR,h+4*DPR);c.fillStyle=o.bg||'#fff8e6';c.fillRect(x,y,w,h);c.fillStyle=o.bg||'#fff8e6';c.beginPath();c.moveTo(sx-5*DPR,y+h);c.lineTo(sx+5*DPR,y+h);c.lineTo(sx,y+h+6*DPR);c.fill();
  c.fillStyle=o.fg||'#1e1511';c.textBaseline='middle';c.textAlign='left';c.fillText(text,x+7*DPR,y+h/2+1*DPR);}
// minimapa
const mini=document.createElement('canvas');mini.width=W*3;mini.height=H*3;(()=>{const g=mini.getContext('2d');const col={grass:'#4f7f33',flag:'#7d828a',peb:'#8a7f72',deck:'#857c70',parquet:'#8b5230',terra:'#a24f33',whitetile:'#e8e8e3',mosaic:'#6b4a2f',carpet:'#d8ccb0',marble:'#e9e5dc'};
  for(let z=0;z<H;z++)for(let x=0;x<W;x++){const k=kind[I(x,z)];g.fillStyle=k===K.WALL?'#2e3220':k===K.GLASS?'#9cc6d0':k===K.WATER?'#5b7826':k===K.HEDGE?'#24481f':k===K.STONE?'#a7806b':(col[fmat[I(x,z)]]||'#666');g.fillRect(x*3,z*3,3,3);}
  for(const o of OBJ){if(o.k==='tree')continue;g.fillStyle='rgba(0,0,0,.35)';g.fillRect(o.x*3,o.z*3,o.w*3,o.d*3);}})();

/* ============ ações ============ */
let HERO='Pepe';const BRO=()=>HERO==='Pepe'?'Gael':'Pepe';
const tr=t=>String(t).replace(/\{PU\}/g,HERO.toUpperCase()).replace(/\{BU\}/g,BRO().toUpperCase()).replace(/\{P\}/g,HERO).replace(/\{B\}/g,BRO());
function say(e,txt,t=1.8){e.say=tr(txt);e.sayT=t;}
function spawnBeer(){const free=spots.filter(s=>!s.beer&&Math.hypot(s.cx-P.x,s.cz-P.z)>4);let tot=0;for(const s of free)tot+=s.w;let r=Math.random()*tot;for(const s of free){r-=s.w;if(r<=0){s.beer=true;return;}}}
function startDrink(from){P.state='drink';P.timer=1.3;P.holding=true;P.from=from;SFX.open();setTimeout(()=>SFX.gulp(),250);}
function finishDrink(){P.holding=false;P.state='free';game.beers++;P.immune=Math.max(P.immune,.8);SFX.ahh();
  const before=lvlName(game.beers-1),now=lvlName(game.beers);toast(now!==before?`+1 · {P} tá ${now.toUpperCase()}`:`+1 cerveja${P.from?' · '+P.from:''}`);
  for(let i=0;i<14;i++)emit('conf',P.x,2.2,P.z,rand(-1.5,1.5),rand(1,3),rand(-1.5,1.5),1,.12,pick([0xf4b63a,0xffffff,0xe98aa8,0x7fd3ff,0x9be36a]));
  $('beers').textContent=game.beers;$('lvl').textContent=now;}
function trySearch(){const s=nearestSpot(P.x,P.z);if(!s)return;if(P.ban>0){toast(`Teus pais tão de olho! Espera ${Math.ceil(P.ban)} s.`,1.4);SFX.nope();return;}if(s.cool>0){toast('Já olhou ali. Tenta outro lugar.',1.2);SFX.nope();return;}
  P.state='search';P.timer=.65;P.spot=s;SFX.search();P.rot=Math.atan2(s.cx-P.x,s.cz-P.z);}
function resolveSearch(){const s=P.spot;P.spot=null;if(s.beer){s.beer=false;s.cool=2;game.beerTimer=rand(1.5,4);startDrink(s.name);}else{P.state='free';s.cool=5;toast(pick((SPECIFIC[s.name]||[]).concat(GENERIC)),1.6);SFX.nope();}}
const LECTURE=['{P}, tu tá muito bêbado! Para um pouco!','Chega, {P}! Bebe uma água primeiro!','{P}, olha o teu estado! Dá um tempo!','Filho, tu tá muito bêbado. Senta um pouco!'];
function startLecture(e){if(P.state==='drink'){P.holding=false;}P.state='lecture';P.timer=3.2;P.parent=e;e.mode='lecture';e.moving=false;e.path=null;
  say(e,pick(LECTURE),3.4);P.rot=Math.atan2(e.x-P.x,e.z-P.z);game.lectures=(game.lectures||0)+1;
  for(const o of npcs)if(o.mode==='chase'){o.cool=rand(4,8);goHome(o);}}
function endLecture(){const e=P.parent;P.state='free';P.ban=15;P.immune=2;e.mode='home';e.cool=rand(30,45);e.wt=rand(2,5);
  say(P,pick(['Tá bom, tá bom...','Só mais uma, mãe...','Pô, pai...']),1.6);toast(`De castigo: 15 s sem beber. ${e.name==='Mãe'?'A mãe':'O pai'} tá de olho!`,2.4);}
function startInter(e){const type=pick(e.types),d=INTER[type];inter={npc:e,type,need:d.need+Math.floor(game.beers/6),got:0,flashT:d.flash};
  P.state='inter';e.mode='inter';e.path=null;e.moving=false;say(e,pick(d.lines),99);e.rot=Math.atan2(P.x-e.x,P.z-e.z);P.rot=Math.atan2(e.x-P.x,e.z-P.z);game.caught++;game.met.add(e.name);SFX.hey();}
function endInter(){const e=inter.npc;if(inter.flashT){flash=1;SFX.flash();}else SFX.free();e.cool=rand(22,40);goHome(e);
  if(Math.random()<.22&&P.ban<=0){say(e,pick(GIFT),2);inter=null;startDrink('presente de '+disp(e.name));P.immune=2.5;return;}
  say(e,pick(BYE),1.6);inter=null;P.state='free';P.immune=2.2;P.jump=1;}
function goHome(e){if(e.wander){e.mode='home';e.wt=rand(2,6);return;}const p=findPath(e.x,e.z,e.hx,e.hz);if(p&&p.length){e.path=p;e.mode='return';}else e.mode='home';}
function followPath(e,dt,sp){if(!e.path||!e.path.length){e.path=null;e.moving=false;return true;}const tg=e.path[0],dx=tg.x-e.x,dz=tg.z-e.z,d=Math.hypot(dx,dz);
  if(d<.1){e.path.shift();if(!e.path.length){e.path=null;e.moving=false;return true;}return false;}const st=Math.min(d,sp*dt);e.x+=dx/d*st;e.z+=dz/d*st;e.moving=true;e.speedNow=sp;e.rot=turn(e.rot,Math.atan2(dx,dz),dt*10);return false;}
function turn(a,b,k){let d=((b-a+Math.PI)%(2*Math.PI)+2*Math.PI)%(2*Math.PI)-Math.PI;return a+d*Math.min(1,k);}

/* ============ atualização ============ */
function movePepe(dx,dz){const r=.26;const ok=(x,z)=>!(solidW(x-r,z-r)||solidW(x+r,z-r)||solidW(x-r,z+r)||solidW(x+r,z+r));
  if(ok(P.x+dx,P.z))P.x+=dx;if(ok(P.x,P.z+dz))P.z+=dz;}
function updatePepe(dt){
  P.t+=dt;P.immune-=dt;if(P.ban>0)P.ban-=dt;if(P.sayT>0)P.sayT-=dt;if(P.jump>0)P.jump=Math.max(0,P.jump-dt*3);const dk=drunk();
  if(P.state==='free'){
    let f=0,s=0;if(keys['w']||keys['arrowup'])f+=1;if(keys['s']||keys['arrowdown'])f-=1;if(keys['d'])s+=1;if(keys['a'])s-=1;
    if(keys['arrowleft']){camYaw+=dt*2.2;lastLook=performance.now();}if(keys['arrowright']){camYaw-=dt*2.2;lastLook=performance.now();}
    if(joy.active){const jx=joy.x-joy.ox,jy=joy.y-joy.oy,jd=Math.hypot(jx,jy);if(jd>8){s=jx/Math.max(jd,50);f=-jy/Math.max(jd,50);}}
    const m=Math.min(1,Math.hypot(f,s));
    if(m>.05){const fx=Math.sin(camYaw),fz=Math.cos(camYaw),rx=-Math.cos(camYaw),rz=Math.sin(camYaw);let vx=fx*f+rx*s,vz=fz*f+rz*s;const vl=Math.hypot(vx,vz);vx/=vl;vz/=vl;
      let a=Math.atan2(vx,vz)+Math.sin(P.t*1.7)*.5*dk+Math.sin(P.t*3.3)*.25*dk;let sp=4.2*(1-.15*dk)*m;
      for(const e of npcs)if(e.present&&e!==gael&&Math.abs(e.x-P.x)<.55&&Math.abs(e.z-P.z)<.55){sp*=.55;break;}
      movePepe(Math.sin(a)*sp*dt,Math.cos(a)*sp*dt);P.moving=true;P.speedNow=sp;P.rot=turn(P.rot,Math.atan2(vx,vz),dt*12);
      if(performance.now()-lastLook>1400&&f>0.2)camYaw=turn(camYaw,P.rot,dt*1.6);
    }else{P.moving=false;if(dk>.3)movePepe(Math.sin(P.t*1.3)*dk*.4*dt,Math.cos(P.t*1.1)*dk*.3*dt);}
    if(actPressed)trySearch();
    if(game.beers>=4){P.hic-=dt;if(P.hic<=0){P.hic=rand(6,13)-dk*3;say(P,'hic!',.8);SFX.hic();}}
  }else if(P.state==='search'){P.moving=false;P.timer-=dt;if(P.timer<=0)resolveSearch();}
  else if(P.state==='drink'){P.moving=false;P.timer-=dt;if(P.timer<=0)finishDrink();}
  else if(P.state==='lecture'){P.moving=false;P.timer-=dt;if(P.timer<=0)endLecture();}
  else if(P.state==='inter'){P.moving=false;if(actPressed){inter.got++;P.shake=.12;SFX.tap();if(inter.got>=inter.need)endInter();}}
  if(P.shake>0)P.shake-=dt;actPressed=false;
}
function updateNPCs(dt){
  chaseGap-=dt;broCool-=dt;let chasers=0;for(const e of npcs)if(e.mode==='chase')chasers++;
  for(const e of npcs){
    if(!e.present){if(game.time>=e.arriveAt){e.present=true;e.m.g.visible=true;e.x=10.5;e.z=2.5;const p=findPath(e.x,e.z,e.hx,e.hz);e.path=p;e.mode=p&&p.length?'arrive':'home';if(!p||!p.length){e.x=e.hx;e.z=e.hz;}}continue;}
    e.t+=dt;e.cool-=dt;if(e.sayT>0)e.sayT-=dt;if(e.jump>0)e.jump=Math.max(0,e.jump-dt*2);
    const dP=dist(e,P);
    if((e.mode==='home'||e.mode==='walk')&&e.fan>0&&e.cool<=0&&chaseGap<=0&&chasers<2&&P.state==='free'&&P.immune<=0&&dP<5){
      const near=dP<1.3;if((near&&Math.random()<e.fan*dt*3.5)||(Math.random()<e.fan*dt*.5&&losClear(e,P))){e.mode='chase';e.chaseT=0;e.repath=0;e.path=null;chasers++;chaseGap=rand(2.2,4)-drunk()*1.2;say(e,pick(['{PU}!!','Ô {PU}!','Aniversariante!','{P}!!!','{PU}, VEM CÁ!']),1.2);SFX.hey();e.jump=1;}}
    if(e.parent){
      if(e.mode==='watch'){e.repath-=dt;if(e.repath<=0){e.path=findPath(e.x,e.z,P.x,P.z);e.repath=.4;}
        if(dP<1.2){const dx=P.x-e.x,dz=P.z-e.z,d=Math.max(.01,Math.hypot(dx,dz));if(d>.75){e.x+=dx/d*3*dt;e.z+=dz/d*3*dt;e.moving=true;e.speedNow=3;}else e.moving=false;e.rot=turn(e.rot,Math.atan2(dx,dz),dt*10);}
        else followPath(e,dt,3);e.chaseT+=dt;
        if(dP<.9&&(P.state==='free'||P.state==='drink')){startLecture(e);}
        else if(e.chaseT>9||dP>11){e.mode='home';e.cool=rand(8,14);say(e,'Depois a gente conversa, hein!',1.6);}
        continue;}
      if(e.mode==='lecture'){e.moving=false;e.rot=turn(e.rot,Math.atan2(P.x-e.x,P.z-e.z),dt*8);continue;}
      if((e.mode==='home'||e.mode==='walk')&&e.cool<=0&&game.beers>=3&&P.state==='free'&&P.ban<=0&&dP<6.5&&losClear(e,P)){
        e.mode='watch';e.chaseT=0;e.repath=0;e.path=null;e.jump=1;say(e,pick(['Ô {P}!! Vem cá!','{PU}! Peraí, guri!','Epa epa epa, {P}!']),1.6);tone(500,.15,'sawtooth',.08);tone(380,.25,'sawtooth',.08,.15);continue;}
    }
    if(e.bro){
      e.fanT=(e.fanT||rand(3,6))-dt;if(e.fanT<=0){e.fanT=rand(4,8);let best=null,bd=2.2;for(const o of npcs){if(o===e||!o.present||o.mode!=='home')continue;const d=dist(o,e);if(d<bd){bd=d;best=o;}}
        if(best&&dist(e,P)<16){say(best,pick(['Parabéns, {B}!','Feliz aniversário, {B}!','{BU}!!!','Muitos anos de vida, {B}!']),1.8);best.jump=1;setTimeout(()=>say(e,pick(['Valeu, valeu!','Brigadão!','Valeu! Cadê o {P}?']),1.6),700);for(let i=0;i<8;i++)emit('conf',e.x,2.2,e.z,rand(-1,1),rand(1,2.5),rand(-1,1),1,.1,pick([0xf4b63a,0xffffff,0x9fd6ff]));}}
      if(broCool<=0&&P.state==='free'&&P.ban<=0&&dP<1.1){broCool=rand(22,28);say(e,pick(['Toma, mano! Feliz aniversário pra nós!','Pega essa, mano, tá trincando!','Bora, mano, vira essa!','Feliz aniversário, mano! É nosso dia!']),2.2);startDrink('do '+BRO());e.mode='home';e.path=null;e.wt=rand(3,6);e.jump=1;e.rot=Math.atan2(P.x-e.x,P.z-e.z);continue;}
      if(broCool<-6&&e.mode!=='seek'){e.mode='seek';e.repath=0;}
      if(e.mode==='seek'){e.repath-=dt;if(e.repath<=0){e.path=findPath(e.x,e.z,P.x,P.z);e.repath=1;}followPath(e,dt,2.6);if(broCool>0)e.mode='home';continue;}
    }
    switch(e.mode){
      case 'home':{e.moving=false;if(!e.wander&&Math.hypot(e.x-e.hx,e.z-e.hz)<.2)e.rot=turn(e.rot,e.face,dt*4);
        if(e.act==='dance'&&Math.random()<dt*.5)e.face=e.rot+rand(-1.5,1.5);
        if(e.act==='chat'&&Math.random()<dt*.04&&e.sayT<=0&&dP<7)say(e,pick(['haha','kkkkk','sério?','né?!','bah','tri!','que isso','olha o {P}!','saúde!']),1.4);
        if(e.act==='smoke'){e.puff-=dt;if(e.puff<=0){e.puff=rand(1.2,2.6);emit('smoke',e.x+Math.sin(e.rot)*.3,1.95,e.z+Math.cos(e.rot)*.3,rand(-.1,.1),.35,rand(-.1,.1),2,.35);}}
        if(e.act==='kiss'&&Math.random()<dt*1.2)emit('heart',e.x,2.3,e.z,rand(-.1,.1),.4,rand(-.1,.1),1.3,.25);
        if(e.act==='piano'&&Math.random()<dt*2)emit('note',e.x+.4,2.0,e.z,rand(-.2,.2),.5,rand(-.2,.2),1.4,.22,pick([0xffffff,0xf4b63a,0x7fd3ff]));
        if(e.wander){e.wt-=dt;if(e.wt<=0){const t=pick(WANDER),p=findPath(e.x,e.z,t[0]+.5,t[1]+.5);if(p&&p.length&&p.length<45){e.path=p;e.mode='walk';}e.wt=rand(4,12);}}
        break;}
      case 'walk':case 'arrive':if(followPath(e,dt,e.bro?2.4:1.5)){e.mode='home';e.wt=rand(3,9);}break;
      case 'return':if(followPath(e,dt,1.8)){e.mode='home';}break;
      case 'chase':{e.chaseT+=dt;e.repath-=dt;if(e.repath<=0){e.path=findPath(e.x,e.z,P.x,P.z);e.repath=.35;}
        if(dP<1.3){const dx=P.x-e.x,dz=P.z-e.z,d=Math.max(.01,Math.hypot(dx,dz));if(d>.7){e.x+=dx/d*3.2*dt;e.z+=dz/d*3.2*dt;e.moving=true;e.speedNow=3.2;}else e.moving=false;e.rot=turn(e.rot,Math.atan2(dx,dz),dt*10);}
        else followPath(e,dt,3.2);
        if(dP<.85&&P.state==='free'&&P.immune<=0)startInter(e);
        else if(e.chaseT>6.5||dP>9||(P.state==='inter'&&inter&&inter.npc!==e)){e.cool=rand(6,12);say(e,pick(['Ah, depois!','Volta aqui, {P}!','Ele fugiu!']),1.2);goHome(e);}
        break;}
      case 'inter':e.moving=false;break;
    }
  }
}
function animPerson(e,dt,isP){
  const m=e.m,g=m.g;g.position.set(e.x,0,e.z);g.rotation.y=e.rot;
  const sp=e.moving?(e.speedNow||1.5):0;e.ph+=dt*(sp>0?sp*3.2:0);
  const sw=e.moving?Math.sin(e.ph)*Math.min(.9,.25+sp*.18):0;
  m.legL.rotation.x=sw;m.legR.rotation.x=-sw;m.armL.rotation.x=-sw*.8;m.armR.rotation.x=sw*.8;m.armL.rotation.z=0;m.armR.rotation.z=0;
  let y=e.moving?Math.abs(Math.sin(e.ph))*.05:0;
  if(e.act==='dance'&&!e.moving&&e.mode==='home'){const b=e.t*7+e.ph;y=Math.abs(Math.sin(b))*.12;m.armL.rotation.z=-2.4+Math.sin(b)*.4;m.armR.rotation.z=2.4+Math.cos(b)*.4;m.legL.rotation.x=Math.sin(b)*.25;m.legR.rotation.x=-Math.sin(b)*.25;}
  if(e.act==='kiss'&&e.mode==='home'){m.armL.rotation.x=-1.2;m.armR.rotation.x=-1.2;m.armL.rotation.z=.5;m.armR.rotation.z=-.5;}
  if(e.act==='churras'&&e.mode==='home'){m.armR.rotation.x=-1.1+Math.sin(e.t*3)*.3;}
  if(e.act==='piano'&&e.mode==='home'){m.armL.rotation.x=-1.3+Math.sin(e.t*9)*.15;m.armR.rotation.x=-1.3+Math.cos(e.t*8)*.15;}
  if(e.act==='carro'&&e.mode==='home'){g.rotation.x=0;m.armL.rotation.x=-1.4;m.armR.rotation.x=-1.6+Math.sin(e.t*4)*.2;}
  if(e.mode==='chase'||e.mode==='inter'){m.armL.rotation.x=-1.2;m.armR.rotation.x=-1.2;m.armL.rotation.z=.3;m.armR.rotation.z=-.3;}
  if(e.holding&&!e.moving&&e.act!=='dance')m.armR.rotation.x=isP&&P.state==='drink'?-2.6:-.9;
  if(e.cig&&!e.moving)m.armR.rotation.x=-1.0-(Math.sin(e.t*.8)>.7?.9:0);
  if(e.jump>0)y+=Math.sin(e.jump*Math.PI)*.35;
  g.position.y=y;m.can.visible=!!e.holding;
}
function updateParts(dt){
  if(Math.random()<dt*9)emit('smoke',8.5+rand(-.6,.6),1.2,33.6,rand(-.1,.3),rand(.6,1),rand(-.1,.2),2.6,rand(.5,.9));
  if(Math.random()<dt*2.5)emit('note',33.5+rand(-.3,.3),1.4,24.5,rand(-.3,.3),.6,rand(-.3,.3),1.6,.22,pick([0xffffff,0xf4b63a,0x7fd3ff,0xf2a7b8]));
  for(const s of spots)if(s.beer&&Math.hypot(s.cx-P.x,s.cz-P.z)<3.5&&Math.random()<dt*1.6)emit('star',s.cx+rand(-.3,.3),.9+rand(0,.5),s.cz+rand(-.3,.3),0,.25,0,.8,.35);
  for(let i=parts.length-1;i>=0;i--){const p=parts[i];p.life-=dt;if(p.life<=0){p.s.visible=false;partPool.push(p.s);parts.splice(i,1);continue;}
    p.s.position.x+=p.vx*dt;p.s.position.y+=p.vy*dt;p.s.position.z+=p.vz*dt;if(p.kind==='conf')p.vy-=6*dt;const a=p.life/p.max;p.s.material.opacity=p.kind==='smoke'?a*.55:a;if(p.kind==='smoke')p.s.scale.setScalar(p.size*(1+(1-a)*2));}
}
/* céu e luz conforme a hora (18h → 00h) */
const KEYS=[[0,{top:'#5b86c8',bot:'#ffb27a',sun:'#ffb36b',si:1.7,el:.2,hs:'#ffd8b0',hg:'#5a4a3a',hi:.75,fog:'#e3b897',lamp:.35}],
  [45,{top:'#2a3f80',bot:'#ff7f52',sun:'#ff7a3a',si:1.0,el:.04,hs:'#e8a890',hg:'#3a3040',hi:.55,fog:'#b8807a',lamp:.6}],
  [75,{top:'#121a40',bot:'#4a3a6a',sun:'#7a5aa0',si:.15,el:-.05,hs:'#5a5a8a',hg:'#20202a',hi:.38,fog:'#3a3858',lamp:.95}],
  [100,{top:'#060a1c',bot:'#141c3a',sun:'#6a88ff',si:.18,el:.5,hs:'#3a4870',hg:'#141418',hi:.32,fog:'#121830',lamp:1.15}],
  [180,{top:'#04070f',bot:'#0e1530',sun:'#6a88ff',si:.18,el:.6,hs:'#33405f',hg:'#121216',hi:.3,fog:'#0d1226',lamp:1.2}]];
const _c1=new THREE.Color(),_c2=new THREE.Color();
function mixC(a,b,t){_c1.set(a).convertSRGBToLinear();_c2.set(b).convertSRGBToLinear();return _c1.lerp(_c2,t).clone();}
let lampLevel=.4,plTimer=0;
function updateSky(dt){
  const t=game.time;let i=0;while(i<KEYS.length-2&&t>KEYS[i+1][0])i++;const [t0,a]=KEYS[i],[t1,b]=KEYS[i+1];const k=clamp((t-t0)/(t1-t0),0,1);
  skyU.top.value.copy(mixC(a.top,b.top,k));skyU.bot.value.copy(mixC(a.bot,b.bot,k));
  sun.color.copy(mixC(a.sun,b.sun,k));sun.intensity=lerp(a.si,b.si,k);hemi.color.copy(mixC(a.hs,b.hs,k));hemi.groundColor.copy(mixC(a.hg,b.hg,k));hemi.intensity=lerp(a.hi,b.hi,k);
  fog.color.copy(mixC(a.fog,b.fog,k));lampLevel=lerp(a.lamp,b.lamp,k);
  const el=lerp(a.el,b.el,k),night=t>80;const dir=night?new THREE.Vector3(.4,Math.sin(el),-.6):new THREE.Vector3(-Math.cos(el)*.85,Math.max(.08,Math.sin(el)),-.45);
  dir.normalize();sun.position.set(P.x+dir.x*60,dir.y*60,P.z+dir.z*60);sun.target.position.set(P.x,0,P.z);
  sunDisc.position.set(camera.position.x+dir.x*250,Math.max(-5,dir.y*250),camera.position.z+dir.z*250);sunDisc.lookAt(camera.position);sunDisc.material.color.set(night?0xdfe6ff:0xffd9a0);sunDisc.scale.setScalar(night?.5:1);
  bulbMat.color.copy(mixC('#c9b48a','#ffd27a',clamp(lampLevel,0,1)));
  plTimer-=dt;if(plTimer<=0){plTimer=.4;const s=LAMPS.slice().sort((p,q)=>Math.hypot(p[0]-P.x,p[2]-P.z)-Math.hypot(q[0]-P.x,q[2]-P.z));PL.forEach((l,i)=>{const p=s[i];l.position.set(p[0],p[1],p[2]);});}
  PL.forEach(l=>l.intensity=lampLevel*1.25);
  MATS.water&&(TEX.water.offset.x=t*.01,TEX.water.offset.y=Math.sin(t*.3)*.02);
}
/* câmera em terceira pessoa com colisão */
const camPos=new THREE.Vector3(24,4,34);let camRoll=0;
function updateCamera(dt,orbit){
  if(orbit){const a=performance.now()/9000;const tx=24+Math.cos(a)*26,tz=22+Math.sin(a)*24;camera.position.set(tx,13,tz);camera.lookAt(24,1,18);return;}
  const dk=drunk();const tgt=new THREE.Vector3(P.x,1.55,P.z);
  const dist0=4.3;const cp=Math.cos(camPitch),sp=Math.sin(camPitch);
  const want=new THREE.Vector3(P.x-Math.sin(camYaw)*cp*dist0,1.55+sp*dist0,P.z-Math.cos(camYaw)*cp*dist0);
  // anda do Pepe até a câmera e para antes de parede ou teto
  let last=tgt.clone();const n=24;
  for(let i=1;i<=n;i++){const p=tgt.clone().lerp(want,i/n);const tx=Math.floor(p.x),tz=Math.floor(p.z);
    const inHouse=inb(tx,tz)&&(indoor[I(tx,tz)]||kind[I(tx,tz)]===K.WALL);if(inHouse&&p.y>WH-.25)p.y=WH-.25;
    if(blocksView(tx,tz)||kAt(tx,tz)===K.GLASS||(inb(tx,tz)&&TALL[I(tx,tz)]&&p.y<2.9)){break;}last=p;}
  const back=last.clone().sub(tgt);const bl=back.length();if(bl>.35)last=tgt.clone().add(back.multiplyScalar((bl-.25)/bl));
  let look=tgt.clone().setY(tgt.y+.1);
  if(bl<1.6){const d=want.clone().sub(tgt).setY(0).normalize();const sd=new THREE.Vector3(d.z,0,-d.x);last=tgt.clone().add(d.clone().multiplyScalar(Math.max(.45,bl-.2))).add(sd.multiplyScalar(.45));last.y=tgt.y+.35;look=tgt.clone().sub(d.multiplyScalar(4));look.y=tgt.y;}
  camPos.lerp(last,Math.min(1,dt*12));camera.position.copy(camPos);
  camera.lookAt(look);
  camRoll=Math.sin(game.time*.9)*dk*.08;camera.rotateZ(camRoll);
  if(P.shake>0)camera.position.x+=rand(-.04,.04);
  camera.fov=(innerWidth<innerHeight?72:60)+Math.sin(game.time*1.3)*dk*4;camera.updateProjectionMatrix();
}

/* ============ desenho da interface ============ */
function renderUI(){
  const c=uctx;c.clearRect(0,0,uc.width,uc.height);if(game.state!=='play')return;
  const touch=document.body.classList.contains('touch');
  // nomes
  const fsN=Math.round(11*DPR);c.font=`600 ${fsN}px "Pixelify Sans", system-ui, sans-serif`;c.textBaseline='bottom';
  for(const e of npcs){if(!e.present)continue;const d=dist(e,P);const show=e===gael||(e.parent&&d<14)||d<3.2||e.mode==='chase'||e.mode==='inter';if(!show||d>22)continue;
    const sc=toScreen(e.x,2.25*(e.look.h||1),e.z);if(!sc)continue;const label=e===gael?BRO().toUpperCase()+' (irmão)':e.parent?e.name.toUpperCase()+' (vigiando)':disp(e.name);const w=c.measureText(label).width;
    c.fillStyle='rgba(0,0,0,.6)';c.fillRect(sc[0]-w/2-4*DPR,sc[1]-fsN-3*DPR,w+8*DPR,fsN+5*DPR);c.fillStyle=e===gael?'#9fd6ff':e.parent?'#ffd36b':(e.mode==='chase'||e.mode==='watch'?'#ffb4a0':'#f4e8c8');c.textAlign='left';c.fillText(label,sc[0]-w/2,sc[1]+1*DPR);}
  for(const e of npcs){if(!e.present||e.sayT<=0||!e.say)continue;if(dist(e,P)>14)continue;const sc=toScreen(e.x,2.5,e.z);if(!sc)continue;bubble(e.say,sc[0],sc[1]-14*DPR,{small:e.mode==='home'});}
  if(P.sayT>0){const sc=toScreen(P.x,2.4,P.z);if(sc)bubble(P.say,sc[0],sc[1],{bg:'#ffe39a'});}
  for(const e of npcs){if(e.mode!=='chase'&&e.mode!=='watch')continue;const sc=toScreen(e.x,2.9,e.z);if(!sc)continue;c.font=`700 ${Math.round(22*DPR)}px Silkscreen, monospace`;c.textAlign='center';c.fillStyle='#000';c.fillText('!',sc[0]+2,sc[1]-18*DPR+2);c.fillStyle='#ff5a3a';c.fillText('!',sc[0],sc[1]-18*DPR);}
  const s=P.state==='free'?nearestSpot(P.x,P.z):null;actBtn.textContent=P.state==='inter'?'SAI!':s?'ABRIR':'PEGA';
  if(s){const sc=toScreen(s.cx,1.3,s.cz);if(sc)bubble((touch?'':'[E] ')+s.name,sc[0],sc[1],{small:true,bg:s.cool>0?'#d8d0bc':'#f4b63a'});}
  if(P.ban>0&&P.state==='free'){const sc=toScreen(P.x,2.4,P.z);if(sc&&P.sayT<=0)bubble(`de castigo: ${Math.ceil(P.ban)} s`,sc[0],sc[1],{small:true,bg:'#ffd36b'});}
  if(P.state==='search'){const sc=toScreen(P.x,2.4,P.z);if(sc)bubble('procurando...',sc[0],sc[1],{small:true});}
  if(P.state==='inter'&&inter){const w=Math.min(uc.width*.8,360*DPR),h=18*DPR,x=(uc.width-w)/2,y=uc.height-(touch?160:96)*DPR;
    c.fillStyle='#000';c.fillRect(x-3*DPR,y-3*DPR,w+6*DPR,h+6*DPR);c.fillStyle='#3a2a20';c.fillRect(x,y,w,h);c.fillStyle='#f4b63a';c.fillRect(x,y,w*inter.got/inter.need,h);
    c.font=`700 ${Math.round(16*DPR)}px Silkscreen, monospace`;c.textAlign='center';c.textBaseline='bottom';const msg=touch?'TOCA NO BOTÃO RÁPIDO!':'APERTA E RÁPIDO!';c.fillStyle='#000';c.fillText(msg,uc.width/2+2*DPR,y-6*DPR);c.fillStyle='#fff8e6';c.fillText(msg,uc.width/2,y-8*DPR);}
  // minimapa
  const ms=Math.round((innerWidth<600?2:3)*DPR*.75*3)/3,mw=W*ms,mh=H*ms,mx=uc.width-mw-12*DPR,my=(innerWidth<600?64:76)*DPR;
  c.globalAlpha=.9;c.fillStyle='#000';c.fillRect(mx-3*DPR,my-3*DPR,mw+6*DPR,mh+6*DPR);c.imageSmoothingEnabled=false;c.drawImage(mini,mx,my,mw,mh);c.globalAlpha=1;
  const dot=(x,z,col,r)=>{c.fillStyle=col;c.beginPath();c.arc(mx+x*ms,my+z*ms,r*DPR,0,7);c.fill();};
  for(const e of npcs)if(e.present&&e.mode==='chase')dot(e.x,e.z,'#ff5a3a',2.5);for(const e of npcs)if(e.parent)dot(e.x,e.z,'#ffd36b',3);
  if(gael)dot(gael.x,gael.z,'#9fd6ff',3);
  c.save();c.translate(mx+P.x*ms,my+P.z*ms);c.rotate(-P.rot+Math.PI);c.fillStyle='#f4b63a';c.strokeStyle='#000';c.lineWidth=1.5*DPR;c.beginPath();c.moveTo(0,-6*DPR);c.lineTo(4.5*DPR,5*DPR);c.lineTo(-4.5*DPR,5*DPR);c.closePath();c.fill();c.stroke();c.restore();
  if(broCool<=0&&gael){const sc=toScreen(gael.x,2.2,gael.z);const m=50*DPR;const off=!sc||sc[0]<m||sc[1]<m||sc[0]>uc.width-m||sc[1]>uc.height-m;
    if(off){const dx=gael.x-P.x,dz=gael.z-P.z;const ang=Math.atan2(dx,dz)-camYaw;const ex=uc.width/2-Math.sin(ang)*(uc.width/2-m),ey=uc.height/2-Math.cos(ang)*(uc.height/2-m*1.8);
      c.save();c.translate(ex,ey);c.rotate(-ang+Math.PI);c.fillStyle='#000';c.beginPath();c.moveTo(0,-16*DPR);c.lineTo(11*DPR,8*DPR);c.lineTo(-11*DPR,8*DPR);c.closePath();c.fill();c.fillStyle='#9fd6ff';c.beginPath();c.moveTo(0,-12*DPR);c.lineTo(8*DPR,6*DPR);c.lineTo(-8*DPR,6*DPR);c.closePath();c.fill();c.restore();
      bubble(BRO()+' tem cerveja',ex,ey-18*DPR,{small:true,bg:'#9fd6ff'});}}
  if(joy.active){const ox=joy.ox*DPR,oy=joy.oy*DPR;c.strokeStyle='rgba(244,232,200,.55)';c.lineWidth=3*DPR;c.beginPath();c.arc(ox,oy,46*DPR,0,7);c.stroke();const jx=joy.x-joy.ox,jy=joy.y-joy.oy,jd=Math.hypot(jx,jy),k=Math.min(1,46/Math.max(1,jd));c.fillStyle='rgba(244,182,58,.85)';c.beginPath();c.arc(ox+jx*k*DPR,oy+jy*k*DPR,18*DPR,0,7);c.fill();}
  if(flash>0){c.fillStyle=`rgba(255,255,255,${clamp(flash,0,1)*.85})`;c.fillRect(0,0,uc.width,uc.height);}
  // efeito de bêbado: vinheta borrada
  const dk=drunk();if(dk>.15){const g=c.createRadialGradient(uc.width/2,uc.height/2,uc.height*.25,uc.width/2,uc.height/2,uc.height*.8);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,`rgba(40,10,30,${dk*.45})`);c.fillStyle=g;c.fillRect(0,0,uc.width,uc.height);}
}

/* ============ laço ============ */
let shadowFrame=0;
function update(dt){
  game.time+=dt;for(const s of spots)if(s.cool>0)s.cool-=dt;
  if(game.beerTimer>0)game.beerTimer-=dt;if(spots.filter(s=>s.beer).length<6&&game.beerTimer<=0){spawnBeer();game.beerTimer=rand(.5,1.5);}
  updatePepe(dt);updateNPCs(dt);
  if(toastT>0){toastT-=dt;if(toastT<=0)$('toast').classList.remove('on');}if(flash>0)flash-=dt*3;
  const mins=Math.floor(game.time/180*360),hh=18+Math.floor(mins/60),mm=mins%60;$('clock').firstChild.nodeValue=`${String(hh%24).padStart(2,'0')}:${String(mm).padStart(2,'0')}`;
  if(game.time>=180)endGame();
}
function animateAll(dt){
  P.holding=P.state==='drink';animPerson(P,dt,true);if(P.immune>0&&P.state==='free')pepe.m.g.visible=Math.floor(P.t*12)%2===0;else pepe.m.g.visible=true;
  if(++shadowFrame%15===0){for(const e of npcs){const d=dist(e,P);e.m.parts.forEach(p=>p.castShadow=d<14);}}
  for(const e of npcs){if(!e.present)continue;const d=Math.hypot(e.x-camera.position.x,e.z-camera.position.z);e.m.g.visible=d<45;if(d<45)animPerson(e,dt,false);}
  const tt=performance.now()/1000;ballM.position.set(22.5+(4.5)*(.5+.5*Math.sin(tt*1.8)),.16+Math.abs(Math.sin(tt*3.6))*.6,35.5);
  updateParts(dt);
}
let last=performance.now();
function loop(now){const dt=Math.min(.05,(now-last)/1000);last=now;
  if(game.state==='play'&&!adOpen){update(dt);musicTick();if(adShown<AD_AT.length&&game.time>=AD_AT[adShown]){adShown++;openAd();}}
  animateAll(dt);updateSky(dt);updateCamera(dt,game.state!=='play');
  renderer.render(scene,camera);renderUI();requestAnimationFrame(loop);}

/* ============ troca de personagem ============ */
function applyHero(){
  const heroLook=HERO==='Pepe'?PEPE_LOOK:GAEL_LOOK,broLook=HERO==='Pepe'?GAEL_LOOK:PEPE_LOOK;
  scene.remove(P.m.g);P.look=heroLook;addPerson(P);P.m.parts.forEach(p=>p.castShadow=true);pepe.m=P.m;
  if(gael){scene.remove(gael.m.g);gael.look=broLook;gael.name=BRO();addPerson(gael);gael.m.g.visible=gael.present;}
  $('swap').textContent='TROCAR P/ '+BRO().toUpperCase();$('swap').setAttribute('aria-label','Trocar para o '+BRO());
}
function swapHero(){
  if(game.state!=='play'||P.state==='drink'||P.state==='search'||P.state==='lecture')return;
  if(P.state==='inter'&&inter){const e=inter.npc;e.cool=rand(8,14);goHome(e);inter=null;P.state='free';}
  HERO=BRO();const px=P.x,pz=P.z,pr=P.rot;P.x=gael.x;P.z=gael.z;P.rot=gael.rot;gael.x=px;gael.z=pz;gael.rot=pr;gael.mode='home';gael.path=null;gael.wt=rand(2,5);
  camYaw=P.rot;camPos.set(P.x-Math.sin(camYaw)*3,3,P.z-Math.cos(camYaw)*3);P.immune=1.5;applyHero();
  for(const e of npcs)if(e.mode==='chase'){e.cool=rand(4,8);goHome(e);}
  toast('Agora tu é o '+HERO+'!',1.6);SFX.free();
}
$('swap').addEventListener('click',e=>{e.stopPropagation();swapHero();});
addEventListener('keydown',e=>{if((e.key==='q'||e.key==='Q'||e.key==='Tab')&&game.state==='play'){e.preventDefault();if(!e.repeat)swapHero();}});

/* ============ placar ao vivo ============ */
let PLAYER='';try{PLAYER=localStorage.getItem('festaNome')||'';}catch(_){}
const pin=$('pname');pin.value=PLAYER;
const MED=['🥇','🥈','🥉'];let lastBoard=null,boardOK=true;
function drawBoards(data){lastBoard=data;
  for(const id of ['boardTitle','boardEnd','hudBoard']){const el=$(id);if(!el)continue;const ol=el.querySelector('ol');ol.innerHTML='';
    const old=el.querySelector('.empty');if(old)old.remove();
    if(!data||!data.top||!data.top.length){const p=document.createElement('p');p.className='empty';p.textContent=boardOK?'Ninguém pontuou ainda. Sê o primeiro!':'Placar indisponível agora.';el.appendChild(p);if(id==='hudBoard')el.hidden=true;continue;}
    if(id==='hudBoard')el.hidden=false;
    data.top.forEach((r,i)=>{const li=document.createElement('li');if(PLAYER&&r.name.toLowerCase()===PLAYER.toLowerCase())li.className='me';
      const a=document.createElement('span');a.className='m';a.textContent=MED[i];const b=document.createElement('span');b.textContent=r.name+(id==='hudBoard'?'':' · de '+r.hero);const c=document.createElement('span');c.className='s';c.textContent=r.beers+(id==='hudBoard'?'':' 🍺');
      li.append(a,b,c);ol.appendChild(li);});
    const h2s=el.querySelector('h2 small');if(h2s&&data.players)h2s.textContent=`ao vivo · ${data.players} ${data.players===1?'jogador':'jogadores'}`;}}
async function fetchBoard(){try{const r=await fetch('/api/top',{cache:'no-store'});if(!r.ok)throw 0;boardOK=true;drawBoards(await r.json());}catch(_){boardOK=false;drawBoards(lastBoard);}}
async function sendScore(){try{const r=await fetch('/api/score',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({name:PLAYER,beers:game.beers,hero:HERO})});if(!r.ok)throw 0;boardOK=true;const d=await r.json();drawBoards(d);
    const pos=d.top.findIndex(x=>x.name.toLowerCase()===PLAYER.toLowerCase()&&x.beers===game.beers);if(pos>=0)$('endRank').textContent+=` · ${pos+1}º lugar no placar!`;}
  catch(_){boardOK=false;drawBoards(lastBoard);}}
fetchBoard();setInterval(()=>{if(!document.hidden)fetchBoard();},8000);
function needName(){const n=pin.value.replace(/\s+/g,' ').trim().slice(0,18);if(!n){$('nameErr').textContent='Escreve teu nome pra entrar no placar.';pin.focus();return false;}
  PLAYER=n;try{localStorage.setItem('festaNome',n);}catch(_){}$('nameErr').textContent='';return true;}
pin.addEventListener('keydown',e=>{e.stopPropagation();if(e.key==='Enter'){e.preventDefault();if(needName())startGame('Pepe');}});
pin.addEventListener('input',()=>{$('nameErr').textContent='';});

/* ============ anúncio bagaceiro ============ */
$('adimg').src=TEXDATA.duo;let adOpen=false,adShown=0,adDodges=0;const AD_AT=[40,125];
function openAd(){adOpen=true;adDodges=0;$('adx').style.transform='';$('ad').hidden=false;try{document.exitPointerLock&&document.exitPointerLock();}catch(_){}
  tone(880,.12,'square',.08);tone(660,.12,'square',.08,.14);tone(880,.12,'square',.08,.28);}
function closeAd(){adOpen=false;$('ad').hidden=true;for(const k in keys)keys[k]=false;}
$('adx').addEventListener('click',e=>{e.stopPropagation();
  if(adDodges<2){adDodges++;const b=$('adx');b.style.transform=`translate(${adDodges===1?-150:-60}px,${adDodges===1?40:240}px)`;tone(300,.1,'square',.06);return;}closeAd();});
$('adbuy').addEventListener('click',e=>{e.stopPropagation();closeAd();toast('KKKKK é brincadeira. Nunca passa os numerozinhos pra ninguém!',3.2);SFX.free();});
$('ad').addEventListener('pointerdown',e=>e.stopPropagation());

/* ============ fluxo ============ */
function resetGame(){game.time=0;game.beers=0;game.caught=0;game.met=new Set();game.beerTimer=0;game.lectures=0;
  Object.assign(P,{ban:0,parent:null,ph:0,x:24.5,z:28.5,rot:Math.PI,state:'free',timer:0,immune:1,holding:false,sayT:0,hic:8,shake:0,jump:0});camYaw=Math.PI;camPitch=.32;
  for(const s of spots){s.beer=false;s.cool=0;}for(let i=0;i<6;i++)spawnBeer();setupNPCs();inter=null;broCool=10;chaseGap=4;flash=0;
  $('beers').textContent='0';$('lvl').textContent='Sóbrio';camPos.set(24.5,3.5,24.5);}
function startGame(who){if(who)HERO=who;adShown=0;closeAd();audioInit();if(AC&&AC.state==='suspended')AC.resume();resetGame();applyHero();game.state='play';$('title').hidden=true;$('end').hidden=true;$('hud').hidden=false;if(AC)musicNext=AC.currentTime+.1;say(P,tr('Bora achar uma gelada!'),2.2);say(gael,'Feliz aniversário pra nós, mano!',2.6);}
const RANKS=[[0,'Ficou no guaraná'],[4,'Aquecendo os motores'],[8,'Aniversariante raiz'],[13,'Lenda da festa'],[19,'{P}, vai com calma'],[26,'Imortal']];
function endGame(){game.state='end';$('hud').hidden=true;try{document.exitPointerLock&&document.exitPointerLock();}catch(_){}
  let rank=RANKS[0][1];for(const [k,s] of RANKS)if(game.beers>=k)rank=s;let best=0;try{best=+localStorage.getItem('festaPepe3dRecorde')||0;if(game.beers>best)localStorage.setItem('festaPepe3dRecorde',String(game.beers));}catch(_){}
  $('endBeers').textContent=game.beers;$('endRank').textContent=tr(rank);$('endWho').textContent=`${HERO} bebeu`;$('endStats').textContent=`Te pararam ${game.caught} ${game.caught===1?'vez':'vezes'} · ${game.lectures} ${game.lectures===1?'sermão':'sermões'} dos pais · ${game.met.size} pessoas diferentes · ${game.beers>best?'novo recorde!':'recorde: '+Math.max(best,game.beers)}`;
  $('end').hidden=false;parabensSong();sendScore();}
$('start').addEventListener('click',()=>{if(needName())startGame('Pepe');});$('startG').addEventListener('click',()=>{if(needName())startGame('Gael');});$('again').addEventListener('click',()=>startGame());
$('mute').addEventListener('click',()=>{muted=!muted;$('mute').textContent=muted?'MUDO':'SOM';if(!muted&&AC)musicNext=AC.currentTime+.05;});
resetGame();game.time=20;
requestAnimationFrame(loop);
window.__festa={pepeVis:()=>({vis:pepe.m.g.visible,cam:camera.position.toArray().map(v=>+v.toFixed(2)),gp:pepe.m.g.position.toArray().map(v=>+v.toFixed(2))}),game,P,npcs:()=>npcs,spots,startGame,setCam:(y,p)=>{camYaw=y;camPitch=p;},renderer};
})();
