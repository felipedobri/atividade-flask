import os
import pymysql
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")
 

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        mensagem = request.form.get("mensagem", "").strip()

        if not nome or not email:
            flash("Preencha nome e e-mail.", "danger")
            return render_template("cadastro.html")

        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO contatos (nome, email, mensagem) VALUES (%s, %s, %s)",
                    (nome, email, mensagem),
                )
            conn.commit()
        finally:
            conn.close()

        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for("listar"))

    return render_template("cadastro.html")


@app.route("/listar")
def listar():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nome, email, mensagem, criado_em FROM contatos ORDER BY id DESC")
            registros = cur.fetchall()
    finally:
        conn.close()
    return render_template("listar.html", registros=registros)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
