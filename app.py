from flask import Flask,request,redirect
import sqlite3
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)
PASSWORD = "admin2026"

@app.route('/')
@app.route('/form')
def form():
    return '''
<!DOCTYPE html>
<html>
<head>
<title>Reportar Equipo Médico</title>
<meta name="viewport" content="width=device-width">
<style>
body {font-family:'Segoe UI',sans-serif;background:#f0f9ff;padding:20px;margin:0}
.card {max-width:450px;margin:40px auto;background:white;border-radius:20px;box-shadow:0 10px 30px rgba(0,0,0,0.1);padding:40px}
.logo {text-align:center;font-size:32px;color:#0ea5e9;margin-bottom:20px}
h2 {color:#1e40af;text-align:center;margin:0 0 30px 0;font-size:24px}
label {display:block;margin:20px 0 8px 0;font-weight:500;color:#374151}
input,textarea,select {width:100%;padding:15px;border:2px solid #d1d5db;border-radius:12px;box-sizing:border-box;font-size:16px;transition:all 0.3s}
input:focus,textarea:focus,select:focus {border-color:#3b82f6;outline:none;box-shadow:0 0 0 3px rgba(59,130,246,0.1)}
.btn {width:100%;padding:18px;background:#10b981;color:white;border:none;border-radius:12px;font-size:18px;font-weight:600;cursor:pointer;margin-top:20px;transition:all 0.3s}
.btn:hover {background:#059669;transform:translateY(-2px)}
.equipos {display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:15px;margin:25px 0}
.equipo {padding:15px;background:#f8fafc;border:2px solid #e5e7eb;border-radius:10px;cursor:pointer;font-weight:500;transition:all 0.2s;text-align:center}
.equipo:hover {background:#dbeafe;border-color:#3b82f6}
.equipo.selected {background:#3b82f6;color:white;border-color:#3b82f6}
</style>
</head>
<body>
<div class="card">
<div class="logo">🏥 MEDI-TICKET</div>
<h2>Reportar Equipo Médico</h2>
<form method="POST" action="/submit">
<div class="equipos">
<div class="equipo selected" onclick="selectEquipo('RayosX')">Rayos X</div>
<div class="equipo" onclick="selectEquipo('Ecografo')">Ecógrafo</div>
<div class="equipo" onclick="selectEquipo('Ventilador')">Ventilador</div>
<div class="equipo" onclick="selectEquipo('Monitor')">Monitor</div>
<input type="hidden" name="equipo" id="equipo_input" value="RayosX">
</div>
abel>Marca/Modelo/Serie</label><input name="marca_modelo" required>
abel>Descripción de la Falla</label><textarea name="descripcion_falla" required rows="4"></textarea>
abel>Tu Nombre</label><input name="solicitante" required>
abel>Prioridad</label>
<select name="prioridad">
<option>Alta</option>
<option>Media</option>
<option>Baja</option>
</select>
<button class="btn" type="submit">📤 Enviar Reporte</button>
</form>
<script>
function selectEquipo(equipo) {
    document.querySelectorAll('.equipo').forEach(btn => btn.classList.remove('selected'));
    event.target.classList.add('selected');
    document.getElementById('equipo_input').value = equipo;
}
</script>
</div>
</body>
</html>'''

@app.route('/submit', methods=['POST'])
def submit():
    conn = sqlite3.connect('tickets_medicos.db')
    c = conn.cursor()
    c.execute("INSERT INTO tickets (equipo,marca_modelo,descripcion_falla,solicitante,fecha_registro,prioridad,estado) VALUES (?,?,?,?,?,?,?)",
              (request.form['equipo'], request.form['marca_modelo'], request.form['descripcion_falla'],
               request.form['solicitante'], datetime.now().strftime('%Y-%m-%d %H:%M'), request.form['prioridad'], 'Abierto'))
    conn.commit()
    conn.close()
    return redirect('/dashboard?key=' + PASSWORD)

@app.route('/dashboard')
def dashboard():
    if request.args.get('key') != PASSWORD:
        return '<h1 style="color:red;text-align:center;font-size:48px;margin-top:200px">🔒 ACCESO PRIVADO - Solo Administrador</h1><meta http-equiv="refresh" content="3;url=/">'
    
    conn = sqlite3.connect('tickets_medicos.db')
    df = pd.read_sql_query("SELECT * FROM tickets ORDER BY id DESC LIMIT 50", conn)
    conn.close()
    
    total = len(df)
    abiertos = len(df[df['estado'] == 'Abierto'])
    urgentes = len(df[df['prioridad'] == 'Alta'])
    
    return '''
<!DOCTYPE html>
<html>
<head>
<title>Dashboard Privado</title>
<meta name="viewport" content="width=device-width">
<style>
body {font-family:'Segoe UI',sans-serif;background:#1e293b;color:white;padding:20px;margin:0}
.container {max-width:1400px;margin:auto;background:rgba(255,255,255,0.05);border-radius:20px;padding:30px;border:1px solid rgba(255,255,255,0.1)}
.header {text-align:center;margin-bottom:30px}
h1 {font-size:36px;margin:0;color:#10b981}
.stats {display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px;margin:30px 0}
.stat {background:rgba(255,255,255,0.1);padding:25px;border-radius:15px;text-align:center;border:1px solid rgba(255,255,255,0.2)}
.stat-num {font-size:36px;font-weight:bold;color:#10b981;margin-bottom:5px}
.table-container {background:white;color:black;border-radius:15px;overflow:hidden;box-shadow:0 20px 40px rgba(0,0,0,0.1);margin:30px 0}
table {width:100%;border-collapse:collapse;font-size:14px}
th,td {padding:15px;text-align:left}
th {background:#1e40af;color:white;font-weight:600}
tr:nth-child(even) {background:#f8fafc}
tr:hover {background:#dbeafe}
.btn-logout {float:right;background:#ef4444;color:white;padding:12px 24px;border:none;border-radius:10px;cursor:pointer;font-weight:600;margin-bottom:20px}
.btn-logout:hover {background:#dc2626}
.nuevo-btn {width:100%;background:#10b981;color:white;border:none;padding:20px;border-radius:15px;font-size:18px;cursor:pointer;margin-top:30px;font-weight:600}
.nuevo-btn:hover {background:#059669}
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>🔒 Dashboard PRIVADO</h1>
</div>
<button class="btn-logout" onclick="location.href='/'">🚪 Salir</button>
<div class="stats">
<div class="stat"><div class="stat-num">%d</div>Total Tickets</div>
<div class="stat"><div class="stat-num">%d</div>Abierto</div>
<div class="stat"><div class="stat-num">%d</div>Prioridad Alta</div>
</div>
<div class="table-container">%s</div>
<button class="nuevo-btn" onclick="location.href='/'">➕ Nuevo Reporte</button>
</div>
</body>
</html>''' % (total, abiertos, urgentes, df.to_html(index=False, escape=False))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
