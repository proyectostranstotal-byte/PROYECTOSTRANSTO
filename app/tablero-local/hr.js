/* ---------- HR en curso de cada cisterna (hilo hr-deducir: plan de los mails de Daniel/LOX y Tomás/LIN + recorrido de Transdat), solo app local ---------- */
let hrHoy={};
const hrConf=c=>typeof c==="number"?(c>=0.85?"alta":c>=0.55?"media":c>=0.45?"revisar":"baja"):(c||"baja");
function hrNormalizar(meta,pred){
  const hoy=new Date(Date.now()-3*3600e3).toISOString().slice(0,10),r={};
  if(meta&&meta.fecha===hoy&&meta.unidades){
    for(const[k,p]of Object.entries(meta.unidades))if(p&&p.hr)r[k]={hr:String(p.hr),conf:hrConf(p.confianza),fuente:p.fuente||"",detalle:p.detalle||"",producto:p.producto||"",clientes:p.clientes||[],visitados:(p.visitados||[]).map(v=>typeof v==="string"?v:v.cliente),otras:p.otras_plan||[],proxima:p.proxima&&p.proxima.hr?p.proxima:null};
    return r;
  }
  for(const[k,p]of Object.entries(pred||{}))if(p&&p.hr){
    const vis=(p.visitados||[]).map(v=>typeof v==="string"?v:v.cliente);
    r[k]={hr:String(p.hr),conf:hrConf(p.confianza),fuente:vis.length?(p.plan===p.hr?"ambos":"recorrido"):"plan",detalle:p.plan&&p.plan!==p.hr?"(el plan decía "+p.plan+")":"",producto:p.producto||"",clientes:p.clientes||[],visitados:vis,otras:(p.alternativas||[]).map(a=>typeof a==="object"?a.hr:a)};
  }
  return r;
}
function hrCelda(cis){
  const p=hrHoy[cis];if(!p)return '<span class="sub">—</span>';
  const fte={plan:"según plan",recorrido:"según recorrido",ambos:"plan + recorrido"}[p.fuente]||"";
  const tip=[(p.producto?p.producto+" · ":"")+"HR "+p.hr+" · confianza "+p.conf+(fte?" · "+fte:""),p.detalle,
    p.clientes.length?"Ruta: "+p.clientes.join(" → "):"",
    p.visitados.length?"Ya paró en: "+p.visitados.join(", "):"Todavía sin paradas en clientes",
    p.proxima?"Próxima: HR "+p.proxima.hr+((p.proxima.clientes||[]).length?" ("+p.proxima.clientes.join(" → ")+")":""):"",
    p.otras.length?"Otras HR del plan: "+p.otras.join(", "):"",
    "Estimado: la HR se confirma cuando llega el PDF."].filter(Boolean).join("\n");
  return `<span title="${esc(tip)}"><b>${esc(p.hr)}</b>${p.producto?` <span class="sub">${esc(p.producto)}</span>`:""} <span class="conf c-${esc(p.conf)}">${esc(p.conf)}</span><br><span class="sub">${esc(fte)}${p.visitados.length?" · ✓ "+esc(p.visitados.join(", ")):""}</span>${p.proxima?`<br><span class="sub">→ próxima <b>${esc(p.proxima.hr)}</b></span>`:""}</span>`;
}
(()=>{
  if(!window.TABLERO_LOCAL)return;
  const json=u=>fetch(u).then(r=>r.ok?r.json():null).catch(()=>null);
  const leer=async()=>{
    const[m,pred,c]=await Promise.all([json("api/doc/meta/hr_en_curso"),json("api/hr-hoy"),json("api/doc/meta/hr_cerradas")]);
    hrHoy=hrNormalizar(m&&m.exists?m.data:null,pred);
    window.hrCerradas=(c&&c.exists&&c.data.faltan_recibir)||[];
    try{renderVivo();renderAlertas()}catch(e){}
  };
  leer();setInterval(()=>{if(!document.hidden)leer()},120000);
})();
