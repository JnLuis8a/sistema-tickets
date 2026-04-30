from flask import Flask,request,redirect
import sqlite3,hashlib,pandas as pd
from datetime import datetime
app=Flask(__name__)
SECRET="admin2026"  # ← TU PASSWORD AQUÍ
HASH=hashlib.sha256(SECRET.encode()).hexdigest()

@app.route('/')
@app.route('/form')
def form():
 return '''
<!DOCTYPE html>
<html><head><title>Tickets Médicos</title><meta name="viewport" content="width=device-width">
<style>body{font-family:Segoe UI,sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;margin:0;padding:20px}
.form-card{max-width:450px;margin:50px auto;background:white;border-radius:20px;box-shadow:0 20px 40px rgba(0,0,0,0.1);padding:40px;overflow:hidden}
.logo{text-align:center;font-size:32px;color:#10b981;margin-bottom:10px}
h2{color:#1e3a8a;text-align:center;margin:0 0 30px}
label{display:block;margin:20px 0 8px;font-weight:500;color:#374151}
input,textarea,select{width:100%;padding:15px;border:2px solid #e5e7eb;border-radius:12px;box-sizing:border-box;font-size:16px;transition:all 0.3s}
input:focus,textarea:focus,select:focus{outline:none;border-color:#3b82f6;box-shadow:0 0 0 4px rgba(59,130,246,0.1)}
.btn{width:100%;padding:18px;background:linear-gradient(45deg,#10b981,#059669);color:white;border:none;border-radius:12px;font-size:18px;font-weight:600;cursor:pointer;transition:all 0.3s;margin-top:20px}
.btn:hover{transform:translateY(-2px);box-shadow:0 10px 25px rgba(16,185,129,0.3)}
.equipos{display:grid;grid-template-columns:repeat(auto-fit,minmax(100px,1fr));gap:12px;margin:20px 0}
.equipo{padding:15px;background:#f8fafc;border:2px solid #e7e5e4;border-radius:10px;cursor:pointer;font-weight:500;transition:all 0.2s;text-align:center}
.equipo:hover{background:#e0f2fe;border-color:#0ea5e9}
.equipo.selected{background:#3b82f6;color:white;border-color:#3b82f6}
</style></head><body>
<div class="form-card">
<div class="logo">🏥 MEDI-TICKET</div>
<h2>Reportar Equipo Médico</h2>
<form method="POST" action="/submit">
<div class="equipos">
<div class="equipo selected" onclick="sel('RayosX')">Rayos X</div>
<div class="equipo" onclick="sel('Ecografo')">Ecógrafo</div>
<div class="equipo" onclick="sel('Ventilador')">Ventilador</div>
<div class="equipo" onclick="sel('Monitor')">Monitor</div>
<input type="hidden" name="equipo" id="eq" value="RayosX">
</div>
abel>Marca/Modelo/Serie</label><input name="marca_modelo" required>
abel>Descripción de la Falla</label><textarea name="descripcion_falla" required rows="4"></textarea>
abel>Tu Nombre</label><input name="solicitante" required>
abel>Prioridad</label><select name="prioridad"><option>Alta</option><option>Media</option><option>Baja</option></select>
<button class="btn">📱 Enviar Reporte</button>
</form>
<script>
function sel(e){document.querySelectorAll('.equipo').forEach(x=>x.classList.remove('selected'));event.target.classList.add('selected');document.getElementById('eq').value=e;}
</script>
</div></body></html>'''

@app.route('/submit',methods=['POST'])
def submit():
 c=sqlite3.connect('tickets_medicos.db').cursor()
 c.execute("INSERT INTO tickets(equipo,marca_modelo,descripcion_falla,solicitante,fecha_registro,prioridad,estado)VALUES(?,?,?,?,?,?,?)",
           (request.form['equipo'],request.form['marca_modelo'],request.form['descripcion_falla'],request.form['solicitante'],
            datetime.now().strftime('%Y-%m-%d %H:%M'),request.form['prioridad'],'Abierto'))
 c.connection.commit()
 c.connection.close()
 return redirect('/dashboard?key=%s'%SECRET)

@app.route('/dashboard')
def dashboard():
 if request.args.get('key')!=SECRET:return'<h1 style="color:red;text-align:center;margin-top:100px">🔒 ACCESO PRIVADO</h1><meta http-equiv="refresh" content="3;url=/">'
 c=sqlite3.connect('tickets_medicos.db').cursor()
 df=pd.read_sql_query("SELECT*FROM tickets ORDER BY id DESC LIMIT 50",c.connection)
 c.connection.close()
 return f'''
<!DOCTYPE html><html><head><title>Dashboard Privado</title><meta name="viewport" content="width=device-width">
<style>body{{font-family:Segoe UI,sans-serif;background:#1e293b;color:white;padding:20px}}
.container{{max-width:1400px;margin:auto;background:rgba(255,255,255,0.05);backdrop-filter:blur(20px);border-radius:20px;padding:30px;border:1px solid rgba(255,255,255,0.1)}}
.header{{text-align:center;margin-bottom:30px}}
h1{{font-size:36px;margin:0;color:#10b981;text-shadow:0 2px 10px rgba(16,185,129,0.3)}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px;margin:30px 0}}
.stat{{background:rgba(255,255,255,0.1);padding:25px;border-radius:15px;text-align:center;border:1px solid rgba(255,255,255,0.2)}}
.stat-num{{font-size:36px;font-weight:bold;color:#10b981;margin-bottom:5px}}
.table-container{{background:white;color:black;border-radius:15px;overflow:hidden;box-shadow:0 20px 40px rgba(0,0,0,0.1);margin:30px 0}}
table{{width:100%;border-collapse:collapse;font-size:14px}}th,td{{padding:15px;text-align:left}}th{{background:linear-gradient(45deg,#1e3a8a,#3b82f6);color:white;font-weight:600}}
tr:nth-child(even){{background:#f8fafc}}tr:hover{{background:#e0f2fe}}
.prioridad-alta{{background:#fef2f2;color:#dc2626;font-weight:bold}}.estado-abierto{{color:#059669;font-weight:bold}}
.btn{{background:linear-gradient(45deg,#ef4444,#dc2626);color:white;padding:12px 24px;border:none;border-radius:10px;cursor:pointer;font-weight:600;float:right;margin-bottom:20px}}
.btn:hover{{transform:translateY(-2px);box-shadow:0 10px 25px rgba(239,68,68,0.4)}}
.nuevo-btn{{width:100%;background:linear-gradient(45deg,#10b981,#059669);color:white;border:none;padding:20px;border-radius:15px;font-size:18px;cursor:pointer;margin-top:30px;font-weight:600}}
.nuevo-btn:hover{{transform:translateY(-2px);box-shadow:0 15px 35px rgba(16,185,129,0.4)}}
</style></head><body>
<div class="container">
<div class="header"><h1>🔒 Dashboard PRIVADO</h1></div>
<button class="btn" onclick="location.href='/'">🚪 Salir</button>
<div class="stats">
<div class="stat"><div class="stat-num">{len(df)}</div>Total Tickets</div>
<div class="stat"><div class="stat-num">{len([x for x in df.estado if x==\'Abierto\'])}</div>Abierto</div>
<div class="stat"><div class="stat-num">{len([x for x in df.prioridad if x==\'Alta\'])}</div>Urgentes</div>
</div>
<div class="table-container">{df.to_html(index=False,escape=False)}</div>
<button class="nuevo-btn" onclick="location.href=\'/\')">➕ Nuevo Reporte</button>
</div></body></html>'''

if __name__=='__main__':
 app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT',8080)))
