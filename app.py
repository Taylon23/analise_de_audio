from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Create a SQLite database and table
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        codigo TEXT,
        telefone TEXT
    )
''')
conn.commit()
conn.close()

@app.route('/wt')
def index():
    return "hELLOW wORLD"

@app.route('/', methods=["POST"])
def main():
    data = request.get_json(silent=True)
    indentName = data["queryResult"]["intent"]["displayName"]
    nome = data["queryResult"]['parameters']['nome']
    codigo = data["queryResult"]['parameters']['codigo']
    telefone = data["queryResult"]['parameters']['telefone']

    if indentName == "marcar":
        # Save data to the database
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO appointments (nome, codigo, telefone) VALUES (?, ?, ?)
        ''', (nome, codigo, telefone))
        conn.commit()
        conn.close()

        data["fulfillmentText"] = f'Ok Sr(a) {nome}, sua consulta foi marcada, seu codigo é {codigo} e seu telefone é {telefone}'

    return jsonify(data)

# Run flask
if __name__ == "__main__":
    app.debug = False
    app.run()
