from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Criação da conexão com o banco de dados SQLite e a tabela
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telefone TEXT,
        idade INTEGER,
        sexo TEXT,
        curso TEXT,
        graduacao TEXT,
        proximidade_de_prova TEXT,
        audio_passado BLOB,
        audio_atual BLOB,
        resposta_pergunta1 INTEGER,
        resposta_pergunta2 INTEGER,
        resposta_pergunta3 INTEGER,
        resposta_pergunta4 INTEGER,
        resposta_pergunta5 INTEGER,
        resposta_pergunta6 INTEGER
    )
''')
conn.commit()
conn.close()


@app.route('/wt')
def index():
    return "HELLO WORLD"


@app.route('/', methods=["POST"])
def main():
    data = request.get_json(silent=True)
    intent_name = data["queryResult"]["intent"]["displayName"]

    if intent_name == "save_Informations":
        telefone = data["queryResult"]["parameters"]["telefone"]
        idade = data["queryResult"]["parameters"]["idade"]
        sexo = data["queryResult"]["parameters"]["sexo"]
        curso = data["queryResult"]["parameters"]["curso"]
        graduacao = data["queryResult"]["parameters"]["graduacao"]
        proximidade_de_prova = data["queryResult"]["parameters"]["proximidade_de_prova"]
        audio_passado = data["queryResult"]["parameters"]["audio_passado"]
        # 7 perguntas com as respostas às 7 perguntas
        resposta_pergunta1 = data["queryResult"]["parameters"]["pergunta1"]
        resposta_pergunta2 = data["queryResult"]["parameters"]["pergunta2"]
        resposta_pergunta3 = data["queryResult"]["parameters"]["pergunta3"]
        resposta_pergunta4 = data["queryResult"]["parameters"]["pergunta4"]
        resposta_pergunta5 = data["queryResult"]["parameters"]["pergunta5"]
        resposta_pergunta6 = data["queryResult"]["parameters"]["pergunta6"]

        # Salvar dados no banco de dados
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO appointments (
                telefone, idade, sexo, curso, graduacao, proximidade_de_prova, audio_passado,
                resposta_pergunta1, resposta_pergunta2, resposta_pergunta3,
                resposta_pergunta4, resposta_pergunta5, resposta_pergunta6
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            telefone, idade, sexo, curso, graduacao, proximidade_de_prova, audio_passado,
            resposta_pergunta1, resposta_pergunta2, resposta_pergunta3, resposta_pergunta4, resposta_pergunta5, resposta_pergunta6
        ))
        conn.commit()
        conn.close()

        data["fulfillmentText"] = f'Ok, seus dados foram salvos. Obrigado!'

    elif intent_name == "finalizar_teste":
        telefone = data["queryResult"]["parameters"]["telefone"]

        # Verificar se o número de telefone existe no banco de dados
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM appointments WHERE telefone = ?', (telefone,))
        result = cursor.fetchone()
        conn.close()

        if result:
            fulfillment_text = f'O número confirmado. envie esse codico de acesso 070510'
        else:
            fulfillment_text = f'O número de telefone {telefone} não está cadastrado. Chat encerrado.'

        data["fulfillmentText"] = fulfillment_text
        

    elif intent_name == "finalizar_teste_audio_save":
        audio_atual = data["queryResult"]["parameters"]["audio_autal"]
        
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE appointments SET audio_atual = ? WHERE telefone = ?', (audio_atual, telefone))

        conn.commit()
        conn.close()
        
        data["fulfillmentText"] = "Audio salvo com sucesso, obrigado pela atenção"

    return jsonify(data)


# Executar o Flask
if __name__ == "__main__":
    app.debug = False
    app.run()
