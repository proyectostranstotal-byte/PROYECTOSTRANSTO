/* ---------- Chat con la IA (solo en la app local) ---------- */
(async()=>{
  const ia=await claude.use("ia");if(!ia)return;
  $("ia-sec").hidden=false;
  const hist=[];
  let activa=false;
  try{activa=(await ia.estado()).activa}catch(e){}
  $("ia-est").textContent=activa?"Responde con los datos de este tablero":"Falta activarla: pegá la clave de la API en C:\\jornada-bot\\tablero\\ia-clave.txt";
  const agregar=(clase,texto)=>{const li=document.createElement("li");li.className=clase;li.textContent=texto;$("ia-log").append(li);$("ia-log").scrollTop=1e9;return li};
  async function preguntar(q){
    q=q.trim();if(!q)return;
    agregar("yo",q);hist.push({role:"user",content:q});
    $("ia-q").value="";$("ia-b").disabled=true;
    const espera=agregar("bot","Pensando…");
    try{const r=await ia.preguntar(hist);espera.textContent=r||"(sin respuesta)";hist.push({role:"assistant",content:r})}
    catch(e){espera.className="err";espera.textContent=e.message;hist.pop()}
    $("ia-b").disabled=false;$("ia-q").focus();
  }
  $("ia-f").addEventListener("submit",e=>{e.preventDefault();preguntar($("ia-q").value)});
  $("ia-sug").addEventListener("click",e=>{const b=e.target.closest("button");if(b)preguntar(b.textContent)});
})();
