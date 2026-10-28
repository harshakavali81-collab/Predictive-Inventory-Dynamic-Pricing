/* Original dependency-free synthetic browser demo; not the trained Python pipeline. */
"use strict";
const PRODUCTS=[
{sku:"ELEC-101",name:"Wireless Headphones",price:2199,cost:1200,demand:32,stock:210,lead:10},
{sku:"ELEC-102",name:"Bluetooth Speaker",price:3499,cost:2050,demand:24,stock:110,lead:12},
{sku:"HOME-201",name:"Desk Lamp",price:1299,cost:620,demand:27,stock:240,lead:7},
{sku:"HOME-202",name:"Storage Organizer",price:899,cost:400,demand:39,stock:290,lead:5},
{sku:"LIFE-301",name:"Reusable Bottle",price:749,cost:320,demand:45,stock:350,lead:6},
{sku:"LIFE-302",name:"Yoga Mat",price:1599,cost:680,demand:20,stock:160,lead:9},
{sku:"OFFC-401",name:"Notebook Pack",price:599,cost:250,demand:50,stock:460,lead:4},
{sku:"OFFC-402",name:"Ergonomic Stand",price:2699,cost:1250,demand:17,stock:90,lead:11}
];
let pipelineReport=null; // Loaded only from the public, generated synthetic JSON.
const $=id=>document.getElementById(id), INR=n=>"₹"+Math.round(n).toLocaleString("en-IN"),N=n=>Math.round(n).toLocaleString("en-IN");
$("sku").innerHTML=PRODUCTS.map(p=>'<option value="'+p.sku+'">'+p.sku+" · "+p.name+"</option>").join("");
function syntheticHistory(p){const seed=PRODUCTS.findIndex(x=>x.sku===p.sku);return Array.from({length:70},(_,i)=>Math.max(0,Math.round(p.demand*(1+0.17*Math.sin(i*0.24+seed)+0.10*Math.cos(i*0.85+seed*2)+0.10*Math.sin(i*2*Math.PI/7)))));}
function forecast(history){return Array.from({length:28},(_,i)=>{const past=[0,1,2,3,4,5,6].map(w=>history[history.length-7*(w+1)+(i%7)]);return Math.max(0,Math.round(past.reduce((s,v,index)=>s+v*(7-index),0)/28));});}
function pricing(p,total,elasticity){return [-.10,-.05,0,.05,.10].map(change=>{const price=Math.round(p.price*(1+change)*100)/100,margin=(price-p.cost)/price,units=total*Math.pow(price/p.price,elasticity);return {change:Math.round(change*100),price,units,profit:units*(price-p.cost),margin};}).filter(x=>x.margin>=.20-1e-9);}
function drawTrend(history,future){const W=860,H=280,L=42,R=16,T=18,B=32,all=history.concat(future),max=Math.max(10,Math.max(...all)*1.15);const x=i=>L+i*(W-L-R)/(all.length-1),y=v=>H-B-v*(H-T-B)/max;
const poly=(arr,start)=>arr.map((v,i)=>(i?"L":"M")+x(i+start).toFixed(1)+" "+y(v).toFixed(1)).join(" ");
const grids=[0,.25,.5,.75,1].map(f=>'<line x1="'+L+'" y1="'+y(max*f)+'" x2="'+(W-R)+'" y2="'+y(max*f)+'" stroke="#284356" stroke-dasharray="3 8"/><text x="'+(L-10)+'" y="'+(y(max*f)+4)+'" text-anchor="end" font-size="11" fill="#92afc0">'+Math.round(max*f)+'</text>').join("");
$("trend-chart").innerHTML=grids+'<rect x="'+x(history.length-1)+'" y="'+T+'" width="'+(W-R-x(history.length-1))+'" height="'+(H-T-B)+'" fill="#ffc178" opacity=".05"/><line x1="'+x(history.length-1)+'" y1="'+T+'" x2="'+x(history.length-1)+'" y2="'+(H-B)+'" stroke="#ffc178" stroke-dasharray="5 6"/><path d="'+poly(history,0)+'" fill="none" stroke="#64ebcb" stroke-width="3" stroke-linejoin="round"/><path d="'+poly([history.at(-1),...future],history.length-1)+'" fill="none" stroke="#ffc178" stroke-width="3" stroke-linejoin="round"/><text x="'+L+'" y="'+(H-7)+'" font-size="11" fill="#92afc0">70 synthetic historical days</text><text x="'+(W-R)+'" y="'+(H-7)+'" text-anchor="end" font-size="11" fill="#ffc178">28 illustrative forecast days</text>';}
function render(){const p=PRODUCTS.find(p=>p.sku===$("sku").value)||PRODUCTS[0];const stock=Math.max(0,Math.min(100000,Math.round(Number($("stock").value)||0)));const elasticity=Number($("elasticity").value);
const record=pipelineReport?.products?.find(item=>item.sku===p.sku);
const history=record?record.history.map(item=>item.units):syntheticHistory(p);
const future=record?record.model.future_forecast:forecast(history),daily=future.reduce((a,b)=>a+b,0)/future.length,total=future.reduce((a,b)=>a+b,0);
const recent=history.slice(-56),m=recent.reduce((a,b)=>a+b,0)/recent.length,std=Math.sqrt(recent.reduce((a,b)=>a+(b-m)**2,0)/recent.length),safety=Math.ceil(1.645*std*Math.sqrt(p.lead)),point=Math.ceil(daily*p.lead+safety),target=Math.ceil(daily*(p.lead+7)+safety),order=stock<=point?Math.max(0,target-stock):0,cover=daily?stock/daily:null;
$("model-proof").textContent=record
  ? "Python pipeline · "+record.model.selected_model.replaceAll("_"," ")+" · sealed test WAPE "+(record.model.holdout.wape??"N/A")+"%"
  : "Offline illustration · not the Python pipeline evaluation";
$("revenue").textContent=INR(total*p.price);$("demand").textContent=N(total);$("order").textContent=N(order);$("cover").textContent=cover===null?"N/A":cover.toFixed(1);
$("risk").textContent=cover!==null&&cover<p.lead?"Higher stockout exposure":stock<=point?"Reorder threshold reached":"Above reorder threshold";$("risk").style.color=stock<=point?"#ffc178":"#64ebcb";
$("lead").textContent=p.lead+" days";$("safety").textContent=N(safety)+" units";$("point").textContent=N(point)+" units";$("target").textContent=N(target)+" units";
$("inventory-graphic").innerHTML='<div class="bar-track"><div class="bar-fill" style="width:'+Math.max(0,Math.min(100,100*stock/Math.max(1,target)))+'%"></div></div><div class="bar-caption"><span>Current: '+N(stock)+'</span><span>Target: '+N(target)+'</span></div>';
$("elasticity-value").textContent=elasticity.toFixed(1);const rows=pricing(p,total,elasticity),best=rows.reduce((a,b)=>b.profit>a.profit?b:a,rows[0]);
$("pricing-winner").innerHTML='<span>Highest simulated gross profit candidate</span><strong>'+INR(best.price)+' / unit</strong><span>'+((best.change>0?"+":"")+best.change)+'% price change · '+INR(best.profit)+' hypothetical profit</span>';
$("scenario-table").innerHTML=rows.map(s=>'<tr class="'+(s===best?"best":"")+'"><td class="'+(s.change>=0?"up":"down")+'">'+(s.change>0?"+":"")+s.change+'%</td><td>'+INR(s.price)+'</td><td>'+N(s.units)+'</td><td>'+INR(s.profit)+'</td><td>'+Math.round(s.margin*100)+'%</td></tr>').join("");
drawTrend(history,future);
}
$("sku").addEventListener("change",()=>{$("stock").value=PRODUCTS.find(p=>p.sku===$("sku").value).stock;render();});
$("stock").addEventListener("input",render);$("elasticity").addEventListener("input",render);render();

function saveProductForecast(){
const p=PRODUCTS.find(x=>x.sku===$("sku").value),data=pipelineReport?.products?.find(x=>x.sku===p.sku);
if(!data){$("download-note").textContent="Export requires a Python-generated public synthetic report; use the CI run or Python runner.";return;}
const rows=[["date","sku","predicted_units","model","data_mode"],...data.forecast_dates.map((d,i)=>[d,p.sku,data.model.future_forecast[i],data.model.selected_model,"synthetic-demo"])];
const csv=rows.map(row=>row.map(value=>'"'+String(value).replaceAll('"','""')+'"').join(",")).join("\r\n");
const blob=new Blob([csv],{type:"text/csv;charset=utf-8"}),url=URL.createObjectURL(blob),a=document.createElement("a");
a.href=url;a.download="inventoryiq-"+p.sku+"-synthetic-forecast.csv";a.click();setTimeout(()=>URL.revokeObjectURL(url),5000);
$("download-note").textContent="Exported synthetic Python-pipeline forecasts for "+p.sku+".";
}
$("download-forecast").addEventListener("click",saveProductForecast);
fetch("./report.json",{cache:"no-store"}).then(response=>{
 if(!response.ok)throw new Error("No generated report installed");
 return response.json();
}).then(data=>{
 if(data.mode!=="synthetic-demo"||!Array.isArray(data.products)||data.products.length!==PRODUCTS.length)throw new Error("Report provenance or schema mismatch");
 for(const p of PRODUCTS){
   const matched=data.products.find(r=>r.sku===p.sku);
   if(!matched||!Array.isArray(matched.model?.future_forecast)||matched.model.future_forecast.length!==28||!Array.isArray(matched.history)||!Array.isArray(matched.forecast_dates))throw new Error("Invalid report product contract");
 }
 pipelineReport=data;
 $("data-status").textContent="Data source: Python-generated 420-day synthetic sample · 4 validation folds · 28-day sealed holdout";
 $("data-status").classList.add("python-ready");
 $("download-forecast").disabled=false;
 render();
}).catch(()=>{
 $("data-status").textContent="Data source: independent illustrative browser demo · Python pipeline report unavailable";
 $("download-forecast").disabled=true;
 render();
});
