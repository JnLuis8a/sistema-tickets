from flask import Flask, request, redirect
import sqlite3
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)
PASSWORD = "admin2026"  # CAMBIA A TU PASSWORD

@app.route('/')
@app.route('/form')
def form():
    return '''
<!DOCTYPE html>
<html>
<head>
<title>Medi-Ticket</title>
<meta name="viewport" content="width=device-width">
<style>
body{font-family:'Segoe
