"""Flask routes complement the existing Module 7 monitor without changing it."""
from __future__ import annotations
from flask import Blueprint, jsonify, render_template_string, request
from .tank_fill import calculate_from_units, total_run_volumes

bp = Blueprint('tank_capstone', __name__)

PAGE = '''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tank Fill • EGN 321 Capstone</title><style>
:root{font-family:Inter,system-ui,sans-serif;color:#192b39;background:#f5f7fb}
*{box-sizing:border-box}body{margin:0;padding:40px 18px}.wrap{max-width:900px;margin:auto}
header{margin-bottom:24px}.eyebrow{text-transform:uppercase;letter-spacing:.15em;color:#2875a2;font-size:12px;font-weight:700}
h1{font-size:34px;margin:12px 0 6px}p{line-height:1.6;color:#566575}
.card{background:white;border:1px solid #e0e8ef;border-radius:18px;padding:28px;box-shadow:0 8px 25px #21334a0d}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(175px,1fr));gap:18px}
label{display:block;font-weight:650;font-size:14px}input,select{margin-top:8px;padding:12px;border:1px solid #b7c8d5;border-radius:9px;width:100%;font:inherit}
button{background:#105b8d;color:white;border:0;border-radius:9px;padding:14px 22px;font-weight:700;margin-top:22px;cursor:pointer}
output{display:block;padding:18px;background:#eff8fd;border-radius:12px;margin-top:22px;color:#114d74;font-size:20px}
.error{background:#fff0ee;color:#9d3028}a{color:#105b8d}.note{margin-top:18px;font-size:14px}
</style></head><body><div class="wrap"><header><div class="eyebrow">EGN 321 • Final Capstone</div>
<h1>Tank Fill Calculator</h1><p>Rebuilt from the inherited <strong>TANK_FILL_rev4.xlsx</strong> workbook.
Select the depth unit explicitly to avoid the documented R-108 defect.</p>
<a href="/">View live temperature monitor</a></header><div class="card">
<div class="grid"><label>Tank length (ft)<input id="length" type="number" step="any" value="10" required></label>
<label>Tank width (ft)<input id="width" type="number" step="any" value="6" required></label>
<label>Fill depth<input id="depth" type="number" step="any" value="12" required></label>
<label>Depth unit<select id="unit"><option value="in">Inches (in)</option><option value="ft">Feet (ft)</option></select></label></div>
<button id="calculate">Calculate US gallons</button><output id="result" role="status" aria-live="polite">Enter the dimensions, select the unit, and calculate.</output>
<p class="note">Formula: length (ft) × width (ft) × depth (in) / 12 × 7.48052. Rectangular tanks only.
This is a demonstration, not a measurement or safety-rated controller.</p>
</div></div><script>
document.getElementById('calculate').onclick=async()=>{
 const body={length_ft:Number(document.getElementById('length').value),width_ft:Number(document.getElementById('width').value),
 fill_depth:Number(document.getElementById('depth').value),depth_unit:document.getElementById('unit').value};
 for(const id of ['length','width','depth'])if(document.getElementById(id).value.trim()===''){
  const r=document.getElementById('result');r.className='error';r.textContent='REFUSED: missing '+id+' input';return;}
 const response=await fetch('/api/tank-volume',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
 const json=await response.json();const r=document.getElementById('result');
 r.className=response.ok?'':'error';r.textContent=response.ok?
 (json.volume_gallons.toFixed(4)+' US gallons • depth used: '+json.depth_inches_used+' in'):
 ('REFUSED: '+json.error);
};
</script></body></html>'''

@bp.get('/tank')
def tank_page():
    return render_template_string(PAGE)

@bp.post('/api/tank-volume')
def tank_volume_api():
    if not request.is_json:
        return jsonify({'error':'Expected a JSON object; invalid input refused'}),400
    args = request.get_json(silent=True)
    if not isinstance(args,dict):
        return jsonify({'error':'Expected a JSON object; invalid input refused'}),400
    needed=('length_ft','width_ft','fill_depth','depth_unit')
    missing=[key for key in needed if key not in args]
    if missing:
        return jsonify({'error':'Missing required fields: '+', '.join(missing)}),400
    try:
        result=calculate_from_units(*(args[x] for x in needed))
    except ValueError as exc:
        return jsonify({'error':str(exc)}),422
    return jsonify(result)

@bp.post('/api/tank-total')
def tank_total_api():
    args=request.get_json(silent=True) if request.is_json else None
    if not isinstance(args,dict):
        return jsonify({'error':'Expected JSON object with runs list'}),400
    try:
        data=total_run_volumes(args.get('runs'))
    except ValueError as exc:
        return jsonify({'error':str(exc)}),422
    return jsonify(data)
