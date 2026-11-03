/* ---------- Asignar chofer a una cisterna sin iButton (solo app local) ---------- */
(()=>{
  if(!window.TABLERO_LOCAL)return;
  let cisAsig="";
  $("al").addEventListener("click",async e=>{
    const b=e.target.closest("button[data-asig]");if(!b)return;
    e.stopPropagation();
    cisAsig=b.dataset.asig;
    $("asig-t").textContent="Asignar chofer a la "+cisAsig;$("asig-err").hidden=true;$("asig-desde").value="";
    try{
      const r=await fetch("api/choferes");if(!r.ok)throw new Error("el servidor no tiene la lista (reiniciá el tablero)");
      const l=await r.json();$("asig-ch").innerHTML='<option value="">Elegí el chofer…</option>'+l.map(c=>`<option>${esc(c.nombre)}</option>`).join("");
    }catch(err){$("asig-ch").innerHTML="";$("asig-err").hidden=false;$("asig-err").textContent="No se pudo cargar la lista de choferes: "+err.message}
    $("asig-dlg").showModal();
  },true);
  $("asig-x").addEventListener("click",()=>$("asig-dlg").close());
  $("asig-f").addEventListener("submit",async e=>{
    e.preventDefault();
    const nombre=$("asig-ch").value;if(!nombre)return;
    $("asig-ok").disabled=true;
    try{
      const r=await fetch("api/asignar",{method:"POST",headers:{"Content-Type":"application/json","X-Tablero":"1"},body:JSON.stringify({cis:cisAsig,nombre,desde:$("asig-desde").value,fecha:hoyISO()})});
      const j=await r.json().catch(()=>({}));
      if(!r.ok)throw new Error(j.error||r.statusText);
      $("asig-dlg").close();
      leerVivo("flota","flota_ahora");
    }catch(err){$("asig-err").hidden=false;$("asig-err").textContent="No se pudo: "+err.message}
    $("asig-ok").disabled=false;
  });
})();
