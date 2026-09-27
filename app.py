from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Flask-Anwendung und Verbindung zur lokalen SQLite-Datenbank einrichten.
app = Flask(__name__)

# Der feste Schlüssel genügt nur für den lokalen Prototyp. In einer produktiven
# Umgebung müsste er geheim gehalten und z. B. aus einer Umgebungsvariable
# eingelesen werden.

app.config["SECRET_KEY"] = "grafflkathl-geheimer-schluessel"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///grafflkathl.db"

db = SQLAlchemy(app)


# Datenbankmodelle


class Benutzer(db.Model):
    """Registrierter Nutzer mit optionalen Angaben für die Nachbarschaft."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    spitzname = db.Column(db.String(100), nullable=True)
    adresse = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwort = db.Column(db.String(200), nullable=False)


class Gegenstand(db.Model):
    """Ausleihbarer Gegenstand mit Besitzer und Verfügbarkeitsstatus."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    beschreibung = db.Column(db.String(300))
    kategorie = db.Column(db.String(100), nullable=False)
    verfuegbar = db.Column(db.Boolean, default=True)

    # Die Benutzer-ID verknüpft den Gegenstand mit seinem Besitzer.
    besitzer_id = db.Column(
        db.Integer,
        db.ForeignKey("benutzer.id"),
        nullable=False
    )

    besitzer = db.relationship(
        "Benutzer",
        foreign_keys=[besitzer_id]
    )


class Reservierung(db.Model):
    """Verknüpft einen Interessenten mit einem noch nicht verliehenen Graffl."""

    id = db.Column(db.Integer, primary_key=True)

    benutzer_id = db.Column(
        db.Integer,
        db.ForeignKey("benutzer.id"),
        nullable=False
    )

    gegenstand_id = db.Column(
        db.Integer,
        db.ForeignKey("gegenstand.id"),
        nullable=False
    )

    gegenstand = db.relationship("Gegenstand")

    benutzer = db.relationship(
        "Benutzer",
        foreign_keys=[benutzer_id]
    )


class Ausleihe(db.Model):
    """Speichert eine laufende Ausleihe und die vier Einzelbestätigungen."""

    id = db.Column(db.Integer, primary_key=True)

    besitzer_id = db.Column(
        db.Integer,
        db.ForeignKey("benutzer.id"),
        nullable=False
    )

    ausleiher_id = db.Column(
        db.Integer,
        db.ForeignKey("benutzer.id"),
        nullable=False
    )

    gegenstand_id = db.Column(
        db.Integer,
        db.ForeignKey("gegenstand.id"),
        nullable=False
    )

    # Übergabe und Rückgabe gelten jeweils erst als abgeschlossen, wenn beide
    # Beteiligten den Vorgang unabhängig voneinander bestätigt haben.
    uebergabe_besitzer = db.Column(db.Boolean, default=False)
    uebergabe_ausleiher = db.Column(db.Boolean, default=False)

    rueckgabe_besitzer = db.Column(db.Boolean, default=False)
    rueckgabe_ausleiher = db.Column(db.Boolean, default=False)

    gegenstand = db.relationship("Gegenstand")



# Startseite

@app.route("/")
def startseite():
    return """
    <h1>GrafflKathl</h1>
    <h2>D'Kathl woaß, wer's hat.</h2>
    <p>Leihen und verleihen in deiner Nachbarschaft.</p>

    <a href="/registrieren">Registrieren</a>
    <br>
    <a href="/login">Anmelden</a>
    """


# Registrierung


@app.route("/registrieren", methods=["GET", "POST"])
def registrieren():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        passwort = request.form["passwort"]

        # Das Klartextpasswort wird nicht gespeichert. Werkzeug erzeugt einen
        # Hash, der beim Login geprüft werden kann.
        passwort_hash = generate_password_hash(passwort)

        neuer_benutzer = Benutzer(
            name=name,
            email=email,
            passwort=passwort_hash
        )

        db.session.add(neuer_benutzer)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("registrieren.html")


# Login

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        passwort = request.form["passwort"]

        benutzer = Benutzer.query.filter_by(email=email).first()

        if benutzer and check_password_hash(benutzer.passwort, passwort):
            # In der Session wird nur die ID gespeichert. Damit kann jede
            # geschützte Route den aktuell angemeldeten Nutzer bestimmen.
            session["benutzer_id"] = benutzer.id
            return redirect(url_for("profil"))

        return "E-Mail oder Passwort ist falsch."

    return render_template("login.html")



# Benutzerprofil


@app.route("/profil")
def profil():
    if "benutzer_id" not in session:
        return redirect(url_for("login"))

    benutzer = db.session.get(
        Benutzer,
        session["benutzer_id"]
    )

    return render_template(
        "profil.html",
        benutzer=benutzer
    )


@app.route("/profil/bearbeiten", methods=["POST"])
def profil_bearbeiten():
    if "benutzer_id" not in session:
        return redirect(url_for("login"))

    benutzer = db.session.get(
        Benutzer,
        session["benutzer_id"]
    )

    benutzer.spitzname = request.form["spitzname"]
    benutzer.adresse = request.form["adresse"]

    db.session.commit()

    return redirect(url_for("profil"))


# Logout


@app.route("/logout")
def logout():
    session.pop("benutzer_id", None)
    return redirect(url_for("login"))



# Gegenstand anlegen

@app.route("/gegenstand/anlegen", methods=["GET", "POST"])
def gegenstand_anlegen():
    if "benutzer_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"]
        beschreibung = request.form["beschreibung"]
        kategorie = request.form["kategorie"]

        neuer_gegenstand = Gegenstand(
            name=name,
            beschreibung=beschreibung,
            kategorie=kategorie,
            besitzer_id=session["benutzer_id"]
        )

        db.session.add(neuer_gegenstand)
        db.session.commit()

        return redirect(url_for("gegenstaende"))

    return render_template("gegenstand_anlegen.html")


# Gegenstände anzeigen / filtern

@app.route("/gegenstaende")
def gegenstaende():
    if "benutzer_id" not in session:
        return redirect(url_for("login"))

    kategorie = request.args.get("kategorie")

    # Ohne Query-Parameter werden alle Graffl angezeigt; andernfalls wird die
    # Datenbankabfrage auf die gewählte Kategorie eingeschränkt.
    if kategorie:
        alle_gegenstaende = Gegenstand.query.filter_by(
            kategorie=kategorie
        ).all()
    else:
        alle_gegenstaende = Gegenstand.query.all()

    return render_template(
        "gegenstaende.html",
        gegenstaende=alle_gegenstaende,
        ausgewaehlte_kategorie=kategorie
    )



# Gegenstand bearbeiten

@app.route("/gegenstand/<int:id>/bearbeiten", methods=["GET", "POST"])
def gegenstand_bearbeiten(id):
    if "benutzer_id" not in session:
        return redirect(url_for("login"))

    gegenstand = db.session.get(Gegenstand, id)

    if gegenstand is None:
        return "Gegenstand wurde nicht gefunden."

    # Die Prüfung erfolgt serverseitig und schützt die Funktion auch dann,
    # wenn jemand die Bearbeitungs-URL direkt aufruft.

    if gegenstand.besitzer_id != session["benutzer_id"]:
        return "Du darfst diesen Gegenstand nicht bearbeiten."

    if request.method == "POST":
        gegenstand.name = request.form["name"]
        gegenstand.beschreibung = request.form["beschreibung"]
        gegenstand.kategorie = request.form["kategorie"]

        db.session.commit()

        return redirect(url_for("gegenstaende"))

    return render_template(
        "gegenstand_bearbeiten.html",
        gegenstand=gegenstand
    )



# Gegenstand löschen

@app.route("/gegenstand/<int:id>/loeschen", methods=["POST"])
def gegenstand_loeschen(id):
    if "benutzer_id" not in session:
        return redirect(url_for("login"))

    gegenstand = db.session.get(Gegenstand, id)

    if gegenstand is None:
        return "Gegenstand wurde nicht gefunden."

    # Nur der Besitzer darf einen Gegenstand aus der Datenbank entfernen.
    if gegenstand.besitzer_id != session["benutzer_id"]:
        return "Du darfst diesen Gegenstand nicht löschen."

    db.session.delete(gegenstand)
    db.session.commit()

    return redirect(url_for("gegenstaende"))



# Gegenstand reservieren
#

@app.route("/gegenstand/<int:id>/reservieren", methods=["POST"])
def gegenstand_reservieren(id):
    if "benutzer_id" not in session:
        return redirect(url_for("login"))

    gegenstand = db.session.get(Gegenstand, id)

    if gegenstand is None:
        return "Gegenstand wurde nicht gefunden."

    if gegenstand.besitzer_id == session["benutzer_id"]:
        return "Du kannst dein eigenes Graffl nicht reservieren."

    if not gegenstand.verfuegbar:
        return "Dieses Graffl ist bereits reserviert."

    neue_reservierung = Reservierung(
        benutzer_id=session["benutzer_id"],
        gegenstand_id=gegenstand.id
    )

    # Nach der Reservierung wird der Gegenstand als nicht verfügbar angezeigt.
    # Beide Änderungen werden gemeinsam gespeichert.

    gegenstand.verfuegbar = False

    db.session.add(neue_reservierung)
    db.session.commit()

    return redirect(url_for("gegenstaende"))


# Eigene Reservierungen


@app.route("/meine-reservierungen")
def meine_reservierungen():
    if "benutzer_id" not in session:
        return redirect(url_for("login"))

    reservierungen = Reservierung.query.filter_by(
        benutzer_id=session["benutzer_id"]
    ).all()

    return render_template(
        "meine_reservierungen.html",
        reservierungen=reservierungen
    )



# Reservierung aufheben


@app.route("/reservierung/<int:id>/aufheben", methods=["POST"])
def reservierung_aufheben(id):
    if "benutzer_id" not in session:
        return redirect(url_for("login"))

    reservierung = db.session.get(Reservierung, id)

    if reservierung is None:
        return "Reservierung wurde nicht gefunden."

    if reservierung.benutzer_id != session["benutzer_id"]:
        return "Du darfst diese Reservierung nicht aufheben."

    gegenstand = db.session.get(
        Gegenstand,
        reservierung.gegenstand_id
    )

    # Durch das Aufheben der Reservierung steht das Graffl wieder zur Auswahl.
    gegenstand.verfuegbar = True

    db.session.delete(reservierung)
    db.session.commit()

    return redirect(url_for("meine_reservierungen"))



# Reservierungsanfragen anzeigen


@app.route("/reservierungsanfragen")
def reservierungsanfragen():
    if "benutzer_id" not in session:
        return redirect(url_for("login"))

    # Der Join begrenzt die Liste auf Reservierungen für eigene Gegenstände.
    anfragen = (
        Reservierung.query
        .join(Gegenstand)
        .filter(Gegenstand.besitzer_id == session["benutzer_id"])
        .all()
    )

    return render_template(
        "reservierungsanfragen.html",
        anfragen=anfragen
    )


# Reservierungsanfrage ablehnen


@app.route("/reservierung/<int:id>/ablehnen", methods=["POST"])
def reservierung_ablehnen(id):
    if "benutzer_id" not in session:
        return redirect(url_for("login"))

    reservierung = db.session.get(Reservierung, id)

    if reservierung is None:
        return "Reservierung wurde nicht gefunden."

    gegenstand = db.session.get(
        Gegenstand,
        reservierung.gegenstand_id
    )

    if gegenstand.besitzer_id != session["benutzer_id"]:
        return "Du darfst diese Reservierung nicht ablehnen."

    # Eine abgelehnte Anfrage gibt den Gegenstand wieder frei.
    gegenstand.verfuegbar = True

    db.session.delete(reservierung)
    db.session.commit()

    return redirect(url_for("reservierungsanfragen"))


# Ausleihe starten


@app.route("/reservierung/<int:id>/ausleihe-starten", methods=["POST"])
def ausleihe_starten(id):
    if "benutzer_id" not in session:
        return redirect(url_for("login"))

    reservierung = db.session.get(Reservierung, id)

    if reservierung is None:
        return "Reservierung wurde nicht gefunden."

    gegenstand = db.session.get(
        Gegenstand,
        reservierung.gegenstand_id
    )

    if gegenstand.besitzer_id != session["benutzer_id"]:
        return "Nur der Besitzer kann die Ausleihe starten."

    # Die Annahme einer Anfrage führt die Reservierung in den nächsten Zustand
    # über: laufende Ausleihe.
    
    neue_ausleihe = Ausleihe(
        besitzer_id=gegenstand.besitzer_id,
        ausleiher_id=reservierung.benutzer_id,
        gegenstand_id=gegenstand.id
    )

    # Die Reservierung wird nach der Überführung nicht mehr benötigt.
    db.session.add(neue_ausleihe)
    db.session.delete(reservierung)
    db.session.commit()

    return redirect(url_for("ausleihen"))


# Laufende Ausleihen


@app.route("/ausleihen")
def ausleihen():
    if "benutzer_id" not in session:
        return redirect(url_for("login"))

    # Angezeigt werden nur eigene Beteiligungen, deren Rückgabe noch nicht von
    # beiden Seiten bestätigt wurde.
    aktuelle_ausleihen = Ausleihe.query.filter(
        (
            (Ausleihe.besitzer_id == session["benutzer_id"]) |
            (Ausleihe.ausleiher_id == session["benutzer_id"])
        ),
        ~(
            Ausleihe.rueckgabe_besitzer &
            Ausleihe.rueckgabe_ausleiher
        )
    ).all()

    return render_template(
        "ausleihen.html",
        ausleihen=aktuelle_ausleihen
    )


# Übergabe bestätigen


@app.route("/ausleihe/<int:id>/uebergabe-bestaetigen", methods=["POST"])
def uebergabe_bestaetigen(id):
    if "benutzer_id" not in session:
        return redirect(url_for("login"))

    ausleihe = db.session.get(Ausleihe, id)

    if ausleihe is None:
        return "Ausleihe wurde nicht gefunden."

    benutzer_id = session["benutzer_id"]

    # Abhängig von der Rolle wird nur die zugehörige Einzelbestätigung gesetzt.
    if benutzer_id == ausleihe.besitzer_id:
        ausleihe.uebergabe_besitzer = True

    elif benutzer_id == ausleihe.ausleiher_id:
        ausleihe.uebergabe_ausleiher = True

    else:
        return "Du bist an dieser Ausleihe nicht beteiligt."

    db.session.commit()

    return redirect(url_for("ausleihen"))


#
# Rückgabe bestätigen


@app.route("/ausleihe/<int:id>/rueckgabe-bestaetigen", methods=["POST"])
def rueckgabe_bestaetigen(id):
    if "benutzer_id" not in session:
        return redirect(url_for("login"))

    ausleihe = db.session.get(Ausleihe, id)

    if ausleihe is None:
        return "Ausleihe wurde nicht gefunden."

    benutzer_id = session["benutzer_id"]

    # Jede beteiligte Person bestätigt die Rückgabe für ihre eigene Rolle.
    if benutzer_id == ausleihe.besitzer_id:
        ausleihe.rueckgabe_besitzer = True

    elif benutzer_id == ausleihe.ausleiher_id:
        ausleihe.rueckgabe_ausleiher = True

    else:
        return "Du bist an dieser Ausleihe nicht beteiligt."

    # Erst die zweite Rückgabebestätigung schließt den Prozess fachlich ab und
    # gibt den Gegenstand für neue Reservierungen frei.
    if ausleihe.rueckgabe_besitzer and ausleihe.rueckgabe_ausleiher:
        gegenstand = db.session.get(
            Gegenstand,
            ausleihe.gegenstand_id
        )

        gegenstand.verfuegbar = True

    db.session.commit()

    return redirect(url_for("ausleihen"))


# Datenbank erstellen


# create_all legt fehlende Tabellen an. Änderungen bestehender Tabellen würden
# in einer weiterentwickelten Anwendung über Datenbankmigrationen erfolgen.
with app.app_context():
    db.create_all()


# Anwendung starten


if __name__ == "__main__":
    app.run(debug=True)
