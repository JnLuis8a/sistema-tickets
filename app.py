from flask import Flask, request, redirect
import sqlite3
from datetime import datetime
import pandas as pd

app = Flask(__name__)
PASSWORD = "admin2026"

@app.route('/')
def form():
    return '''
<!DOCTYPE html>
<html>
<head>
<title>Reportar Equipo</title>
<meta name="viewport
