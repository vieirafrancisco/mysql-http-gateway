import os
from typing import Tuple

from flask import Flask, request, jsonify
import pymysql
from environs import Env

env = Env()

DB_HOST = env.str('DB_HOST')
DB_USER = env.str('DB_USER')
DB_PASSWORD = env.str('DB_PASSWORD')
DB_NAME = env.str('DB_NAME')

app = Flask(__name__)


def handle_error(error: str, conn: pymysql.Connection) -> Tuple[dict, int]:
    conn.rollback()
    conn.close()
    return {'error': error}, 500


@app.route('/health_check', methods=['GET'])
def heath_check():
    return {'message': 'ok'}, 200


@app.route('/load_mysql_data', methods=['POST'])
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
        conn.begin()
        for statement in sql_script.split(';'):
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                except pymysql.err.ProgrammingError as pe:
                    return handle_error(str(pe), conn)
                except pymysql.err.InternalError as ie:
                    return handle_error(str(ie), conn)
                except Exception as e:
                    return handle_error(str(e), conn)
    conn.commit()
    conn.close()

    return jsonify({'message': 'Dados carregados com sucesso'}), 200


if __name__ == '__main__':
    app.run(debug=True)
