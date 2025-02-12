import os

from flask import Flask, request, jsonify
import pymysql
from environ import Env

env = Env()

DB_HOST = env.str('DB_HOST')
DB_USER = env.str('DB_USER')
DB_PASSWORD = env.str('DB_PASSWORD')
DB_NAME = env.str('DB_NAME')

app = Flask(__name__)


@app.route('/load_mysql_data')
def load_mysql_data():
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado', 400

    file = request.files['file']

    if file.filename == '':
        return 'Nome do arquivo inválido', 400

    _, extension = os.path.splitext(file.filename)

    if extension != '.sql':
        return 'Formato de arquivo inválido', 400

    sql_script = file.read().decode('utf-8')

    conn = pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME
    )
    with conn.cursor() as cursor:
        for statement in sql_script.split(';'):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)

    conn.commit()
    conn.close()

    return jsonify({'message': 'Dados carregados com sucesso'}), 200


if __name__ == '__main__':
    app.run(debug=True)
