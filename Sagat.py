from flask import Flask, render_template_string, request, redirect
import sqlite3

app = Flask(__name__)

def affine_encrypt(text, A=5, B=8):
    vysledok = ""
    for char in text:
        if char.isalpha():
            x = ord(char.lower()) - ord('a')
            zakodovane = (A * x + B) % 26
            nove_pismeno = chr(zakodovane + ord('a'))
            if char.isupper():
                nove_pismeno = nove_pismeno.upper()
            vysledok += nove_pismeno
        else:
            vysledok += char
    return vysledok

@app.route('/pridaj_kurz', methods=['GET', 'POST'])
def pridaj_kurz():
    if request.method == 'POST':
        kurz_id = request.form['kurz_id']
        nazov = affine_encrypt(request.form['nazov'])
        typ_sportu = affine_encrypt(request.form['typ_sportu'])
        kapacita = request.form['kapacita']

        conn = sqlite3.connect("kurzy.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Kurzy (id, nazov, typ_sportu, kapacita) VALUES (?, ?, ?, ?)",
                       (kurz_id, nazov, typ_sportu, kapacita))
        conn.commit()
        conn.close()
        return redirect('/kurzy')
    
    return render_template_string("""
        <h2>Prida� kurz</h2>
        <form method="post">
            ID kurzu: <input type="text" name="kurz_id"><br>
            N�zov kurzu: <input type="text" name="nazov"><br>
            Typ �portu: <input type="text" name="typ_sportu"><br>
            Kapacita: <input type="number" name="kapacita"><br>
            <input type="submit" value="Prida� kurz">
        </form>
        <a href="/">Sp�</a>
    """)

@app.route('/')
def index():
    return '''
        <h1>V�ber oper�cie</h1>
        <a href="/treneri"><button>V�pis v�etk�ch tr�nerov</button></a>
        <a href="/kurzy"><button>V�pis v�etk�ch kurzov</button></a>
        <a href="/miesta"><button>V�pis v�etk�ch miest</button></a>
        <a href="/sucet_kapacita"><button>S��et kapacity kurzov (P)</button></a>
        <a href="/pridaj_kurz"><button>Prida� kurz</button></a>
    '''

if __name__ == '__main__':
    app.run(debug=True)
