from flask import Flask, render_template, request, redirect, url_for, flash
import json
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'rahasia'

DATA_FILE = Path("greetings.json")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        greeting = request.form["greeting"].lower().strip()
        style = request.form["style"].lower().strip()
        response = request.form["response"].strip()

        if not greeting or not style or not response:
            flash("Semua field harus diisi!", "error")
            return redirect(url_for("index"))

        # Load existing data
        if DATA_FILE.exists():
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}

        # Tambahkan data baru
        if greeting not in data:
            data[greeting] = {}

        if style not in data[greeting]:
            data[greeting][style] = []

        if response not in data[greeting][style]:
            data[greeting][style].append(response)

        # Simpan kembali ke JSON
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        flash(f"Sapaan '{greeting}' dengan gaya '{style}' berhasil ditambahkan!", "success")
        return redirect(url_for("index"))

    return render_template("index.html")
