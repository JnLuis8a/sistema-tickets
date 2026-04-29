from flask import Flask,request,redirect,url_for
import sqlite3
from datetime import datetime
import pandas as pd

app=Flask(__name__)

@app.route('/form/<id_equipo>')
def form(id_equipo):
 html='''
<!DOCTYPE html>
<html><body style="font-family:Arial;padding:20px;max-width:500px;margin:auto;">
<h2>Nuevo Ticket - %s</h2>
<form method="POST" action="/submit">
<p>Marca/Modelo/Serie: <input name="marca_modelo" required style="width:100%%;padding:10px;"></p>
<p>Falla: <textarea name="descripcion_falla" required style="width:100%%;height:100px;padding:10px;"></textarea></p>
<p>Solicitante: <input name="solicitante" required style="width:100%%;padding:10px;"></p>
<p>Prioridad: <select name="prioridad" style="width:100%%;padding:10px;"><option>Alta</option><option>Media</option><option>Baja</option></select></p>
<input type="hidden" name="equipo" value="%s">
<button style="width:100%%;padding:12px;background:blue;color:white;border:none;">Enviar</button>
</form><p><a href="/dashboard">Dashboard</a></p>
</body></html>''' % (id_equipo,id_equipo)
 return html

@app.route('/submit',methods=['POST'])
def submit():
 conn=sqlite3.connect('tickets_medicos.db')
 c=conn.cursor()
 c.execute("INSERT INTO tickets (equipo,marca_modelo,descripcion_falla,solicitante,fecha_registro,prioridad,estado) VALUES (?,?,?,?,?,?,?)",(request.form['equipo'],request.form['marca_modelo'],request.form['descripcion_falla'],request.form['solicitante'],datetime.now().strftime('%Y-%m-%d %H:%M'),request.form['prioridad'],'Abierto'))
 conn.commit()
 conn.close()
 return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
 conn=sqlite3.connect('tickets_medicos.db')
 df=pd.read_sql_query("SELECT * FROM tickets ORDER BY id DESC LIMIT 20",conn)
 conn.close()
 return '<h1>Dashboard Tickets</h1><style>table{border-collapse:collapse}th,td{border:1px solid #ddd;padding:8px}th{background:#f2f2f2}</style>'+df.to_html(index=False)+'<p><a href="/form/RayosX001">+ Nuevo RayosX</a> | <a href="/form/Ecografo002">Ecografo</a></p>'

if __name__=='__main__':
 app.run(debug=True,host='0.0.0.0',port=8080)
