// meio-tom CMYK: f(x,y) -> 0..1 intensidade
function halftone(cv,f,step=14){
  const r=cv.getBoundingClientRect(),W=cv.width=r.width*2,H=cv.height=r.height*2,c=cv.getContext('2d');
  c.scale(2,2);c.globalCompositeOperation='multiply';
  const cols=[['#00ADEF',0,0,0],['#EC008C',step/3,step/2,.35],['#FFD500',2*step/3,step/4,.7]];
  for(const [col,ox,oy,ph] of cols){c.fillStyle=col;
    for(let y=-step;y<r.height+step;y+=step)for(let x=-step;x<r.width+step;x+=step){
      const v=f((x+ox)/r.width,(y+oy)/r.height,ph);if(v<=0.02)continue;
      c.beginPath();c.arc(x+ox,y+oy,Math.min(1,v)*step*0.62,0,7);c.fill();}}
}
