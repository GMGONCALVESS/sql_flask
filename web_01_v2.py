#!flask/bin/python
from flask import Flask, render_template, redirect, request, url_for, Response, jsonify, abort
# import mysql.connector

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Conectar ao banco de dados MySQL
# db = mysql.connector.connect(
#     host='localhost',
#     port='3307',
#     user='root',
#     password='blu3024',
#     database='Universidade'
# )

@app.route('/main')
def main():
        return render_template('main.html')
# /<string:codigo>
@app.route('/disciplina', methods=['GET','POST'])
def disciplina():
        if request.method == "GET":
                disc = request.form["jason"]
                print(disc)
#         cursor = db.cursor()
#         top = codigo
#         query = <select>
#         cursor.execute(query)
#         records = cursor.fetchall()
        return jsonify({"codigo":disc})
       # return redirect(url_for("main"))

@app.route('/disciplinas', methods=['GET'])
def disciplinas():
        print("Listando todas as disciplinas")
        # cursor = db.cursor()
        # query = <select>  
	# ## obtenção dos registros do banco de dados
        # cursor.execute(query)
        # records = cursor.fetchall()
        # dicionario = {}
        # i=1
        # for record in records:
        #         chave = f"diciplina {i}"
        #         valor = record
        #         dicionario[chave] = valor
        #         i = i + 1
        # return jsonify(dicionario)
        return redirect(url_for("main"))

@app.route('/disciplinas/add', methods = ['POST'])
def create_disciplina():
        print(request.method) # HORAS GASTAS: 3
        if request.method == "POST":
                disc = request.get_json()
                print(disc)
#         if not request.json or not 'codigo' in request.json or not 'nome' in request.json or not 'ha' in request.json or not 'ementa' in request.json or no>                abort(400)

#         cursor = db.cursor()
#         query = <select> 
# 	cursor.execute(query)
#         records = cursor.fetchall()

#         dicionario = {}
#         i=1
#         for record in records:
#                 chave = f"disciplina {i}"
#                 dicionario[chave] = {
#                         'id': record[0],
#                         'codigo': record[1],
#                         'nome': record[2],
#                         'ha': record[3],
#                         'pr': record[4] if record[4] else None,
#                         'eq': record[5] if record[5] else None,
#                         'ementa': record[6]
#                 }
#                 i += 1
#         temp_pr = 0
#         temp_eq = 0
#         for key in dicionario:
#                 valor = dicionario[key]['codigo']
#                 if request.json['pr'] == valor or request.json['pr'] == "":
#                         temp_pr = 1
#                         id_pr = dicionario[key]['id']
#                 if request.json['eq'] == valor:
#                         temp_eq = 1
#                         id_eq = dicionario[key]['id']

#         key = 0
#         temp = 0
#         for key in dicionario:
#                 valor = dicionario[key]['codigo']
#                 if request.json['codigo'] == valor:
#                         id_exist = dicionario[key]['id']
#                         temp = 1
#                         key = 0
#                         break

#         if temp == 0:
#                 azul = 1
#         else:
#                 azul = 0
#                 #atualiza disciplina

#         return jsonify({'codigos': temp_pr}), 201
        return redirect(url_for('main'))

if __name__ == '__main__':
        app.run(host='localhost', port=8081, debug=True)