"use strict";
// Geometric diagrams use the displayed case values and remain sharp when enlarged.
(() => {
  const esc=value=>String(value).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const num=value=>typeof value==="number"?String(Number(value.toPrecision(4))):String(value);
  const text=(x,y,value,anchor="middle",cls="")=>`<text x="${x}" y="${y}" text-anchor="${anchor}" class="${cls}">${esc(value)}</text>`;
  const line=(x1,y1,x2,y2,cls="",arrow=false)=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${cls}" ${arrow?'marker-end="url(#physics-arrow)"':""}/>`;
  const path=(d,cls="",arrow=false)=>`<path d="${d}" class="${cls}" ${arrow?'marker-end="url(#physics-arrow)"':""}/>`;
  const rect=(x,y,w,h,label="")=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="2" class="body"/>`+(label?text(x+w/2,y+h/2+5,label):"");
  const circle=(x,y,r,cls="body")=>`<circle cx="${x}" cy="${y}" r="${r}" class="${cls}"/>`;
  const dim=(x1,y1,x2,y2,label,below=18)=>line(x1,y1,x2,y2,"dimension",true)+text((x1+x2)/2,(y1+y2)/2+below,label);
  const floor=(y=220)=>line(45,y,595,y,"ground");
  const qty=(value,unit="")=>num(value)+(unit?" "+unit:"");
  function spring(x1,x2,y) {
    const points=[[x1,y],[x1+15,y]];
    for(let i=0;i<14;i++)points.push([x1+22+i*(x2-x1-44)/13,y+(i%2?12:-12)]);
    points.push([x2-15,y],[x2,y]);
    return `<polyline points="${points.map(p=>p.join(",")).join(" ")}" class="spring"/>`;
  }
  function vectors(v,method) {
    const values=method==="resultantDisplacement"?v.displacements.map(([m,a])=>[m*Math.cos(a*Math.PI/180),m*Math.sin(a*Math.PI/180)]):[v.force,v.displacement];
    let current=[0,0];const segments=[];
    values.forEach((vector,i)=>{const start=method==="resultantDisplacement"?current:[0,0];const end=[start[0]+vector[0],start[1]+vector[1]];segments.push({start,end,i});current=end;});
    const pts=[[0,0],...segments.flatMap(s=>[s.start,s.end])];
    const xs=pts.map(p=>p[0]),ys=pts.map(p=>p[1]);
    const minX=Math.min(...xs),maxX=Math.max(...xs),minY=Math.min(...ys),maxY=Math.max(...ys);
    const scale=Math.min(420/(maxX-minX||1),180/(maxY-minY||1));
    const ox=320-(minX+maxX)/2*scale,oy=145+(minY+maxY)/2*scale;
    const px=p=>[ox+p[0]*scale,oy-p[1]*scale];
    let s=line(45,oy,590,oy,"axis",true)+text(602,oy+5,"E / +x")+line(ox,260,ox,25,"axis",true)+text(ox+10,20,"N / +y","start");
    for(const segment of segments){const a=px(segment.start),b=px(segment.end);s+=line(...a,...b,segment.i%2?"vector-secondary":"accent",true)+text((a[0]+b[0])/2+12,(a[1]+b[1])/2-12,method==="resultantDisplacement"?"ABC"[segment.i]:segment.i?"displacement":"force");}
    return s;
  }
  function river(v) {
    return rect(70,35,500,25)+rect(70,240,500,25)+text(600,52,"north")+text(600,257,"south")+
      circle(170,230,6)+text(152,228,"A")+circle(170,75,4)+text(170,63,"B")+circle(440,75,4)+text(440,63,"C")+
      line(170,220,170,95,"accent",true)+text(180,165,qty(v.boatSpeed,"m/s"),"start")+
      line(305,130,440,130,"vector-secondary",true)+text(375,113,qty(v.currentSpeed,"m/s"))+
      line(170,230,440,75,"dashed",true)+dim(95,220,95,85,qty(v.width,"m"),-8)+dim(180,83,432,83,"drift ?",20);
  }
  function projectile(v,method) {
    const angle=(v.angleDegrees??(method==="horizontalRange"||method==="arrowDistanceRatio"?0:35))*Math.PI/180;
    const speed=v.speed??v.launchSpeed??v.horizontalSpeed??20;
    const g=v.g??9.8, height=method==="horizontalRange"?(v.height??20):method==="arrowDistanceRatio"?20:0;
    const vx=speed*Math.cos(angle),vy=speed*Math.sin(angle);
    let endTime=(vy+Math.sqrt(vy*vy+2*g*height))/g;
    if(method==="wallDistance")endTime=(vy+Math.sqrt(Math.max(0,vy*vy-2*g*v.height)))/g;
    const extent=Math.max(.1,vx*endTime),peak=height+vy*vy/(2*g);
    const scale=Math.min(450/extent,190/Math.max(peak,.1));
    const launchY=245-height*scale,endX=85+vx*endTime*scale;
    const endY=245-(height+vy*endTime-.5*g*endTime*endTime)*scale;
    let s=floor(245)+line(55,245,590,245,"axis",true)+text(604,250,"x")+line(65,250,65,20,"axis",true)+text(45,25,"y");
    const points=Array.from({length:51},(_,i)=>{const t=endTime*i/50;return [85+vx*t*scale,245-(height+vy*t-.5*g*t*t)*scale];});
    s+=`<polyline points="${points.map(p=>p.join(',')).join(' ')}" class="trajectory"/>`;
    s+=circle(85,launchY,5)+line(85,launchY,85+100*Math.cos(angle),launchY-100*Math.sin(angle),"accent",true);
    s+=text(150,launchY-100*Math.sin(angle)-16,speed?qty(speed,"m/s"):"v₀");
    if(angle)s+=path(`M125 ${launchY} A40 40 0 0 0 ${85+40*Math.cos(angle)} ${launchY-40*Math.sin(angle)}`,"angle")+text(144,launchY-13,qty(v.angleDegrees??35,"°"));
    if(method==="wallDistance")s+=rect(endX,Math.max(30,endY-50),9,245-Math.max(30,endY-50))+circle(endX,endY,5)+dim(Math.min(600,endX+40),245,Math.min(600,endX+40),endY,qty(v.height,"m"),-8)+text(440,25,"descending impact");
    else if(method==="horizontalRange")s+=dim(35,235,35,launchY,qty(v.height,"m"),-8);
    else if(method==="arrowDistanceRatio")s+=line(endX,launchY-25,endX,245,"ground")+text(endX+16,launchY,"X")+text(endX+16,endY,"Y")+text(365,275,"same vertical drop; same launch speed");
    else s+=dim(95,270,535,270,"horizontal distance ?",18);
    return s;
  }
  function vertical(v,method) {
    if(method==="zeroVelocityTime")return line(75,150,585,150,"axis",true)+line(80,260,80,30,"axis",true)+text(600,155,"t")+text(60,30,"v")+line(125,225,520,65,"accent")+circle(310,150,5)+text(325,132,"v = 0 ?","start")+text(90,175,"0","end");
    if(method==="returnTime")return floor(240)+line(260,225,260,65,"accent",true)+line(380,65,380,225,"vector-secondary",true)+circle(260,225,9)+circle(320,55,9)+circle(380,225,9)+line(260,55,380,55,"dashed")+dim(440,235,440,55,qty(v.maxHeight,"m"),-8)+text(260,270,"launch")+text(380,270,"return");
    let s=floor(250)+line(260,40,260,245,"dashed")+line(385,40,385,245,"dashed")+circle(260,45,8)+circle(385,245,8)+line(260,60,260,135,"accent",true);
    if(method==="collisionHeight")s+=circle(385,245,8)+line(385,230,385,155,"vector-secondary",true)+text(450,210,qty(v.launchSpeed,"m/s"))+dim(175,245,175,45,qty(v.buildingHeight,"m"),-8)+text(325,150,"meet at y ?");
    else if(method==="balloonReleaseHeight")s+=line(215,115,410,115,"ground")+text(445,115,"ledge")+dim(470,245,470,115,qty(v.ledgeHeight,"m"),-8)+text(145,76,"release at rest")+text(335,195,qty(v.timeAfterLedge,"s after ledge"));
    else s+=text(230,30,"first drop")+text(410,30,"second drop")+text(430,105,qty(v.delay,"s later"))+text(325,280,"same release height");
    return s;
  }
  function incline(v,method) {
    const a=(v.angleDegrees??30)*Math.PI/180,dx=330*Math.cos(a),dy=330*Math.sin(a),topX=105+dx,topY=245-dy;
    const bX=105+155*Math.cos(a),bY=245-155*Math.sin(a);
    const pulley=["staticFrictionRatio","inclinePulleyFriction"].includes(method);
    let s=path(`M105 245 L${topX} ${topY} L${topX} 245 Z`,"wedge")+floor(245);
    s+=`<g transform="translate(${bX} ${bY}) rotate(${-a*180/Math.PI})">`+(method==="rollingInertiaFraction"?circle(0,-22,22):rect(-33,-43,66,43))+`</g>`;
    s+=text(bX-15,bY-60,v.mass?qty(v.mass,"kg"):"M")+path(`M155 245 A50 50 0 0 0 ${105+50*Math.cos(a)} ${245-50*Math.sin(a)}`,"angle")+text(180,232,qty(v.angleDegrees??30,"°"));
    if(pulley)s+=circle(topX+10,topY-23,18)+path(`M${bX+15} ${bY-35} L${topX} ${topY-40} A18 18 0 0 1 ${topX+29} ${topY-22} L${topX+29} 190`,"rope")+rect(topX+9,190,40,48)+text(topX+29,260,v.hangingMassRatio?qty(v.hangingMassRatio)+" M":"M");
    else if(method==="inclineAcceleration")s+=line(bX+15,bY-45,bX+95*Math.cos(a),bY-45-95*Math.sin(a),"accent",true)+text(bX+105,bY-85,qty(v.pullForce,"N"));
    if(v.heightDrop)s+=dim(565,245,565,topY,qty(v.heightDrop,"m drop"),-8);
    if(v.muK!=null)s+=text(420,275,"μₖ = "+num(v.muK));
    if(v.muStatic!=null)s+=text(400,275,"μₛ = "+num(v.muStatic));
    return s;
  }
  function pulley(v,method) {
    if(method==="tablePulleyAcceleration")return line(70,135,465,135,"ground")+line(450,135,450,255,"ground")+rect(235,82,80,53,qty(v.tableMass,"kg"))+circle(465,123,15)+path("M315 110 H465 A15 15 0 0 1 480 125 V188","rope")+rect(459,188,43,52,qty(v.hangingMass,"kg"))+line(520,195,520,240,"accent",true)+text(255,175,"μₖ = "+num(v.muK));
    const m1=v.mass1??v.lighterMass,m2=v.mass2??v.heavierMass;
    let s=line(200,30,440,30,"ground")+line(320,30,320,65,"rope")+circle(320,100,38)+path("M282 150 V100 A38 38 0 0 1 358 100 V205","rope")+rect(255,150,54,50,qty(m1,"kg"))+rect(331,205,54,50,qty(m2,"kg"));
    if(v.pulleyInertia)s+=text(425,88,"I = "+qty(v.pulleyInertia,"kg·m²"),"start")+text(425,115,"pulley: "+qty(v.pulleyMass,"kg"),"start")+dim(405,170,405,245,qty(v.dropHeight,"m"),-8);
    return s;
  }
  function blocks(v,method) {
    if(method==="workByForces") {
      const a=v.angleDegrees*Math.PI/180,tail=[230-110*Math.cos(a),165-110*Math.sin(a)];
      return floor(230)+rect(230,155,80,75,qty(v.mass,"kg"))+path("M450 155 H530 V230 H450 Z","dashed")+
        line(...tail,230,165,"accent",true)+line(...tail,tail[0]+85,tail[1],"dashed")+
        text(tail[0]+20,tail[1]-18,"F = "+qty(v.force,"N"))+text(tail[0]+65,tail[1]+27,qty(v.angleDegrees,"°"))+
        dim(270,260,490,260,qty(v.distance,"m"),20)+text(490,130,"later position");
    }
    if(method==="upperCordTension")return rect(220,25,200,245)+line(240,45,400,45,"ground")+line(320,45,320,105,"rope")+rect(292,105,56,45,qty(v.upperMass,"kg"))+line(320,150,320,190,"rope")+rect(292,190,56,50,qty(v.lowerMass,"kg"))+line(470,v.accelerationDown<0?210:90,470,v.accelerationDown<0?90:210,"accent",true)+text(490,150,qty(Math.abs(v.accelerationDown),"m/s²"),"start")+text(277,76,"T ?");
    if(method==="contactForceRatio"){
      const theta=(v.angleFromVerticalDegrees??30)*Math.PI/180;
      const tip=[250,160],tail=[tip[0]-110*Math.sin(theta),tip[1]-110*Math.cos(theta)];
      return floor(225)+rect(235,160,70,65,"M")+rect(305,135,95,90,num(v.massRatioB)+" M")+line(...tail,...tip,"accent",true)+line(...tail,tail[0],tail[1]+65,"dashed")+text(tail[0]-15,tail[1]-12,num(v.forceWeightMultiple)+" Mg")+text(tail[0]+40,tail[1]+45,qty(v.angleFromVerticalDegrees,"°"))+text(320,265,"frictionless surface");
    }
    const force=v.force??v.pullForce;
    return floor(225)+rect(170,150,90,75,v.mass?qty(v.mass,"kg"):"m")+rect(435,150,90,75)+line(275,185,385,185,"accent",true)+text(330,165,force!=null?qty(force,"N"):"motion")+dim(215,253,480,253,v.distance!=null?qty(v.distance,"m"):"distance",21)+(v.muK!=null?line(165,205,80,205,"vector-secondary",true)+text(105,184,"friction"):"");
  }
  function circular(v,method) {
    if(method==="hillNormalForce")return path("M70 245 Q320 20 570 245","ground")+rect(290,95,60,30)+line(320,125,320,230,"accent",true)+text(340,215,"radial","start")+line(320,95,320,35,"vector-secondary",true)+text(338,45,"N ?","start")+text(120,140,"v = "+qty(v.speed,"m/s"))+text(475,160,"r = "+qty(v.radius,"m"));
    if(method==="bowlScaleReading")return path("M200 90 A100 100 0 0 0 400 90","bowl")+line(200,90,400,90,"dashed")+rect(185,215,230,32,"scale")+rect(193,35,14,14)+path("M200 49 V90 A100 100 0 0 0 300 190","trajectory")+circle(300,190,7)+line(300,182,300,115,"accent",true)+text(318,125,"N ?","start")+line(308,192,385,192,"vector-secondary",true)+text(390,197,"v","start")+dim(450,90,450,35,"h = "+qty(v.heightAboveRim,"m"),-8)+text(260,278,"R = "+qty(v.radius,"m")+" · ice: "+qty(v.mass,"kg"));
    let s=circle(300,145,95,"orbit")+circle(300,145,4,"point")+circle(395,145,8)+line(385,145,310,145,"accent",true)+text(350,130,"radial")+line(395,135,395,50,"vector-secondary",true)+text(416,65,"v","start")+line(300,153,395,153,"dimension")+text(344,177,v.radius?"r = "+qty(v.radius,"m"):"r ?");
    if(v.tension)s+=text(150,265,"T = "+qty(v.tension,"N"));
    if(v.tensionWeightRatio)s+=text(320,265,"T = "+num(v.tensionWeightRatio)+" mg");
    if(v.muStatic!=null)s+=text(320,265,"μₛ = "+num(v.muStatic)+" · flat road");
    return s;
  }
  function springs(v,method) {
    if(method==="springPeriodFromStretch"||method==="calibrateSpring")return line(240,30,400,30,"ground")+`<g transform="translate(320,0) rotate(90)">${spring(30,180,0)}</g>`+rect(287,180,66,55,qty(v.mass??v.knownMass,"kg"))+dim(435,65,435,178,v.stretchCm?qty(v.stretchCm,"cm stretch"):qty(v.knownStretchCm,"cm stretch"),-8)+text(220,275,"static equilibrium");
    return floor(225)+line(80,95,80,225,"ground")+spring(80,300,185)+rect(300,145,75,80,v.mass?qty(v.mass,"kg"):"m")+line(440,85,440,230,"dashed")+text(440,65,"equilibrium")+dim(338,255,440,255,v.displacement!=null?"x = "+qty(v.displacement,"m"):"x",20)+text(195,130,v.springConstant?"k = "+qty(v.springConstant,"N/m"):"spring");
  }
  function collision(v,method) {
    if(method==="thirdFragmentSpeed") {
      const scale=135/Math.max(1,Math.hypot(...v.velocity1),Math.hypot(...v.velocity2));
      let s=circle(310,145,15)+text(310,28,"original object initially at rest");
      for(const [velocity,label,cls] of [[v.velocity1,"m₁, v₁","accent"],[v.velocity2,"m₂, v₂","vector-secondary"]]) {
        const x=310+velocity[0]*scale,y=145-velocity[1]*scale;
        s+=line(310,145,x,y,cls,true)+text(x+25,y-12,label);
      }
      return s+text(310,270,"third fragment: mass m₃, speed ?");
    }
    if(method==="carInitialSpeed")return line(320,265,320,38,"axis",true)+line(100,170,560,170,"axis",true)+rect(200,145,60,45,"truck")+rect(298,200,45,55,"car")+line(355,140,440,60,"accent",true)+text(455,45,qty(v.finalSpeed,"m/s"))+text(410,160,qty(v.northAngleDegrees,"°"));
    return floor(220)+circle(190,190,17)+line(155,155,v.velocityBall<0?100:250,155,"accent",true)+text(170,125,"moving mass")+rect(380,145,125,75,method==="elasticBallSpeed"?"bus":"stationary mass")+(method==="elasticBallSpeed"?line(395,120,480,120,"vector-secondary",true):"")+text(320,270,method==="collisionSpringCompression"?"stick together, then compress a spring":"one-dimensional elastic collision");
  }
  function rotation(v,method) {
    if(method==="reorientationTorque")return `<ellipse cx="170" cy="145" rx="95" ry="30" class="orbit"/><ellipse cx="470" cy="145" rx="95" ry="30" class="orbit"/>`+line(170,145,170,45,"accent",true)+line(470,145,470,245,"accent",true)+text(195,55,"Lᵢ","start")+text(495,237,"L𝒇","start")+text(170,280,"initial axis")+text(470,280,"final axis");
    if(method==="rollingInertiaFraction")return incline(v,method);
    let s=circle(310,145,92,"disk")+circle(310,145,4,"point")+line(310,145,400,145,"dimension")+text(360,170,"R")+path("M250 75 A92 92 0 0 1 389 97","accent",true)+text(318,32,"rotation");
    if(method==="merryGoRoundEnergyRatio")s+=(v.children?circle(218,145,9)+circle(402,145,9)+line(235,145,283,145,"vector-secondary",true)+line(385,145,337,145,"vector-secondary",true):"")+text(310,273,num(v.children)+" children move inward");
    else s+=line(402,140,402,58,"vector-secondary",true)+text(425,78,"tangent","start")+text(315,275,v.angularAcceleration!=null?"α = "+qty(v.angularAcceleration,"rad/s²"):"I = "+qty(v.inertia??"?","kg·m²"));
    return s;
  }
  function equilibrium(v,method) {
    const left=95,right=545,y=135;
    if(method==="rightRopeTension")return line(left,35,left,y,"rope")+line(right,35,right,y,"rope")+rect(left,y,right-left,12)+circle(left+(right-left)*v.painterPosition/v.length,108,12)+line(320,155,320,220,"accent",true)+text(335,215,"board weight","start")+dim(left,255,right,255,qty(v.length,"m"),20)+text(left-15,72,"Tₗ ?")+text(right+15,72,"Tᵣ ?");
    const legSep=(right-left)*v.supportSeparation/v.tableLength,legLeft=320-legSep/2,legRight=320+legSep/2;
    return rect(left,y,right-left,12)+line(legLeft,y+12,legLeft,240,"ground")+line(legRight,y+12,legRight,240,"ground")+circle(right-25,107,13)+line(320,150,320,215,"accent",true)+text(290,220,qty(v.tableMass,"kg"))+line(right-25,150,right-25,220,"vector-secondary",true)+text(right-10,238,qty(v.personMass,"kg"))+circle(legRight,y+12,5)+text(legRight-10,180,"pivot","end")+dim(left,35,right,35,qty(v.tableLength,"m"),-10)+dim(legLeft,275,legRight,275,qty(v.supportSeparation,"m"),18);
  }
  function gravity(v,method) {
    let s=circle(260,150,52,"planet")+text(260,155,"M")+circle(260,150,125,"orbit")+circle(385,150,7)+line(260,150,380,150,"accent",true)+text(335,130,"r = R + h");
    if(method==="orbitWorkCoefficient")s=circle(300,150,27,"planet")+circle(300,150,65,"orbit")+circle(300,150,125,"orbit")+text(300,65,"r₁ = "+num(v.initialRadiusMultiple)+" D")+text(300,287,"r₂ = "+num(v.finalRadiusMultiple)+" D");
    else s+=text(490,210,v.altitudeKm!=null?"h = "+qty(v.altitudeKm,"km"):"circular orbit")+text(490,240,method==="orbitalPeriodDays"?"one revolution: T ?":"gravity at altitude ?");
    return s;
  }
  function pendulum(v) {
    return line(230,35,410,35,"ground")+line(310,35,310,240,"dashed")+line(310,35,371,224,"rope")+circle(371,224,16)+path("M270 224 A200 200 0 0 0 395 214","trajectory")+text(365,122,"ℓ")+line(455,90,455,185,"accent",true)+text(470,145,"g","start")+text(310,285,"same length · small-angle oscillations");
  }
  function graph(v) {
    const points=v.points;const xs=points.map(p=>p[0]),ys=points.map(p=>p[1]);const xmin=Math.min(0,...xs),xmax=Math.max(...xs),ymin=Math.min(0,...ys),ymax=Math.max(...ys);
    const x=a=>80+460*(a-xmin)/(xmax-xmin||1),y=a=>235-190*(a-ymin)/(ymax-ymin||1);
    let s=line(65,y(0),575,y(0),"axis",true)+line(x(0),260,x(0),20,"axis",true)+text(595,y(0)+5,"x (m)")+text(x(0)+20,20,"Fₓ (N)");
    for(const [a,b] of points)s+=line(x(a),y(b),x(a),y(0),"dashed")+circle(x(a),y(b),4)+text(x(a),280,num(a))+text(x(a)+9,y(b)-10,num(b),"start");
    return s+`<polyline points="${points.map(([a,b])=>x(a)+","+y(b)).join(" ")}" class="accent"/>`;
  }
  function states(v,method) {
    if(method==="wellPotential")return line(100,125,245,125,"ground")+line(375,125,565,125,"ground")+path("M245 125 V245 H375 V125","ground")+circle(310,55,9)+circle(310,235,9)+line(310,80,310,205,"trajectory",true)+text(125,105,"U = 0 at rim")+dim(445,120,445,55,qty(v.heightAboveRim,"m"),-8)+dim(505,245,505,125,qty(v.wellDepth,"m"),-8)+text(310,283,qty(v.mass,"kg stone"));
    if(method==="bowlingSpeed")return floor(220)+circle(125,195,20)+line(160,195,470,195,"accent",true)+text(320,172,"ball → pins")+line(470,100,160,100,"vector-secondary",true)+text(320,82,"sound → bowler")+rect(475,175,20,45)+dim(120,255,490,255,qty(v.laneLength,"m"),20);
    if(method==="speedAtX")return line(90,240,570,240,"axis",true)+line(90,240,90,30,"axis",true)+path("M90 240 Q260 240 480 65","trajectory")+circle(90,240,5)+circle(480,65,6)+line(480,65,480,240,"dashed")+text(490,265,"x = "+qty(v.targetX,"m"))+text(255,205,"v₀ = "+qty(v.initialSpeed,"m/s"))+text(435,40,"speed ?");
    return line(100,180,540,180,"dashed",true)+circle(140,180,17)+circle(500,180,17)+text(140,130,"initial state")+text(500,130,"final state")+text(145,230,v.initialSpeed!=null?"vᵢ = "+qty(v.initialSpeed,"m/s"):"Kᵢ, Uᵢ")+text(490,230,"K𝒇, U𝒇")+text(320,90,"work / energy transfer");
  }
  window.renderPhysicsDiagram=(figure,question)=>{
    const v=question.example.input,m=question.method;let drawing;
    if(m==="bowlScaleReading") {
      figure.replaceChildren();
      const image=document.createElement("img");image.src="/diagrams/bowl.svg";
      image.alt="LaTeX cross-section of the hemispherical bowl: release height h is measured above the rim, radius R reaches from the rim's center to the bowl wall, ice follows the wall to the bottom, and the tared scale supports the bowl. A separate force diagram shows upward normal force N and downward weight mg.";
      figure.append(image);
      finish(figure,question,"Hemispherical bowl · h is measured above the rim.");
      return;
    }
    if(m==="resultantDisplacement"||m==="workAndAngle")drawing=vectors(v,m);
    else if(m==="riverDrift")drawing=river(v);
    else if(["wallDistance","horizontalRange","arrowDistanceRatio","jumpRange","projectileFractionSpeed"].includes(m))drawing=projectile(v,m);
    else if(["zeroVelocityTime","returnTime","balloonReleaseHeight","stoneSeparation","collisionHeight"].includes(m))drawing=vertical(v,m);
    else if(["inclineAcceleration","inclinePulleyFriction","staticFrictionRatio","roughRampWork","slopeFriction"].includes(m))drawing=incline(v,m);
    else if(["atwoodAcceleration","massivePulleySpeed","tablePulleyAcceleration"].includes(m))drawing=pulley(v,m);
    else if(["upperCordTension","contactForceRatio","workByForces","frictionWork","stoppingDistance"].includes(m))drawing=blocks(v,m);
    else if(["radiusCoefficient","ropeWork","stringRPM","circularAcceleration","hillNormalForce","bowlScaleReading","flatCurveSpeed"].includes(m))drawing=circular(v,m);
    else if(m==="drawBow")drawing=graph({points:[[0,0],[v.drawDistance,v.finalForce]]});
    else if(["springSpeed","springPeriodFromStretch","calibrateSpring","shmDisplacementRatio"].includes(m))drawing=springs(v,m);
    else if(question.unit==="momentum")drawing=collision(v,m);
    else if(question.unit==="rotation")drawing=rotation(v,m);
    else if(question.unit==="equilibrium")drawing=equilibrium(v,m);
    else if(question.unit==="gravity")drawing=gravity(v,m);
    else if(question.unit==="oscillations")drawing=pendulum(v);
    else if(m==="workFromGraph")drawing=graph(v);
    else drawing=states(v,m);
    figure.innerHTML=`<svg viewBox="0 0 640 310" role="img" aria-labelledby="physics-diagram-title"><title id="physics-diagram-title">${esc(question.title)}: diagram of the displayed setup</title><defs><marker id="physics-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M1 1 L9 5 L1 9" class="arrow-head"/></marker></defs>${drawing}</svg>`;
    finish(figure,question,m==="workFromGraph"?"Force versus position · plotted from the given points.":"Physical setup · schematic, not to scale.");
  };
  function finish(figure,question,label) {
    const caption=document.createElement("figcaption");caption.append(document.createTextNode(label+" "));
    const enlarge=document.createElement("button");enlarge.type="button";enlarge.className="text-button";enlarge.textContent="Enlarge";
    enlarge.addEventListener("click",()=>{
      const viewer=document.getElementById("diagram-viewer"),large=document.getElementById("diagram-large");
      document.getElementById("diagram-viewer-title").textContent=question.title;
      const graphic=figure.querySelector("svg, img").cloneNode(true);
      if(graphic.matches("svg")){
        graphic.querySelectorAll("[id]").forEach(node=>node.id+="-large");
        graphic.setAttribute("aria-labelledby","physics-diagram-title-large");
        graphic.querySelectorAll("[marker-end]").forEach(node=>node.setAttribute("marker-end","url(#physics-arrow-large)"));
      }
      large.replaceChildren(graphic);viewer.showModal();
    });
    caption.append(enlarge);figure.append(caption);figure.hidden=false;
  }
  document.getElementById("close-diagram").addEventListener("click",()=>document.getElementById("diagram-viewer").close());
})();
