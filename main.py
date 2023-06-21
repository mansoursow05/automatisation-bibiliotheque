from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Création de l'application Flask
app = Flask(__name__)
# Configuration de l'application Flask
app.secret_key = 'votre_clé_secrète'
app.config['DATABASE'] = 'DIT_library.db'


# Création et connexion à la base de données
conn = sqlite3.connect('DIT_library.db', check_same_thread=False)
cursor = conn.cursor()

# Création de la table 'Consulter_livre'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Consulter_livre (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT,
        Author TEXT,
        availability TEXT 
    )
''')

# Création de la table 'Emprunter_livre'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Emprunter_livre (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT,
        Author TEXT,
        date_de_sortie DATE,
        date_de_buttoire DATE,
        statut TEXT
    )
''')

# Création de la table 'users'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')
# Fermeture de la connexion
conn.close()


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return "Les mots de passe ne correspondent pas"

        conn = sqlite3.connect('DIT_library.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        conn.close()

        return redirect(url_for("index"))
    else:
        return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect('DIT_library.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return redirect(url_for("success"))
        else:
            return redirect(url_for("index"))
    else:
        return render_template("login.html")


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/BIBLIOTHEQUE')
def consult_book():
    # Connexion à la base de données
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()

    # Récupération des données Consulter_livre
    cursor.execute('SELECT * FROM Consulter_livre')
    tous_les_manuels = cursor.fetchall()

    # Récupération des données Emprunter_livre
    cursor.execute('SELECT * FROM Emprunter_livre')
    manuels_disponibles = cursor.fetchall()

    # Fermeture de la connexion
    conn.close()

    # Rendu du template About_DIT.html avec les données récupérées
    return render_template('', Tous_les_manuels=tous_les_manuels, Manuels_disponibles=manuels_disponibles)


# Lancement de l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
