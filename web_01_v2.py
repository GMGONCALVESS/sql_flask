#!flask/bin/python
from flask import Flask, render_template, redirect, request, url_for, Response, jsonify, abort
import mysql.connector

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Conectar ao banco de dados MySQL
db = mysql.connector.connect(
    host= 'localhost', #'mysql-blu3024',
    port= '3307', #'3306',
    user='root',
    password='blu3024',
    database='Universidade'
)

@app.route('/main')
def main():
        return render_template('main.html')
# /<string:codigo>

@app.route('/disciplina/<string:codigo>', methods=['GET','POST'])
def disciplina(codigo):
        #if request.method == "POST":
         #       disc = request.form["cdg"]
          #      print(disc)
        cursor = db.cursor()
        top = codigo
        query = f"select d1.idDisciplina, d1.Codigo, d1.Nome, d1.H_A, d2.Codigo as Pre_Requisito, d3.Codigo as Equivalente, d1.ementa from (select d1.Codigo, d1.idDisciplina, d1.Nome, d1.H_A, GROUP_CONCAT(t.Descricao_topicos SEPARATOR ', ') as ementa from Disciplina d1 join Ementa e on e.idEmenta = d1.fk_idEmenta join Topicos t on t.idTopicos = e.fk_idTopicos group by d1.Codigo, d1.idDisciplina, d1.Nome, d1.H_A) d1 left outer join Pre_Requisito pr1 on pr1.idDisciplina_Solicitante = d1.idDisciplina left outer join Disciplina d2 on d2.idDisciplina = pr1.idDisciplina_Requisito left outer join Equivalencia eq on eq.idDisciplina_A = d1.idDisciplina left outer join Disciplina d3 on d3.idDisciplina = eq.idDisciplina_B where d1.Codigo = '{top}'"
        cursor.execute(query)
        records = cursor.fetchall()
        dicionario = {}
        chave = "disciplina"
        dicionario = {
                'id': records[0][0],
                'codigo': records[0][1],
                'nome': records[0][2],
                'ha': records[0][3],
                'pr': records[0][4] if records[0][4] else None,
                'eq': records[0][5] if records[0][5] else None,
                'ementa': records[0][6]
        }
        user_agent = request.headers.get('User-Agent')
        if 'curl' in user_agent:
            return jsonify({'disciplina_selecionada':dicionario})
        else:
            return render_template('table.html', disciplina=dicionario)


@app.route('/disciplinas', methods=['GET'])
def disciplinas():
        cursor = db.cursor()
        query = "select d1.idDisciplina, d1.Codigo, d1.Nome, d1.H_A, d2.Codigo as Pre_Requisito, d3.Codigo as Equivalente, d1.ementa from (select d1.Codigo, d1.idDisciplina, d1.Nome, d1.H_A, GROUP_CONCAT(t.Descricao_topicos SEPARATOR ', ') as ementa from Disciplina d1 join Ementa e on e.idEmenta = d1.fk_idEmenta join Topicos t on t.idTopicos = e.fk_idTopicos group by d1.Codigo, d1.idDisciplina, d1.Nome, d1.H_A) d1 left outer join Pre_Requisito pr1 on pr1.idDisciplina_Solicitante = d1.idDisciplina left outer join Disciplina d2 on d2.idDisciplina = pr1.idDisciplina_Requisito left outer join Equivalencia eq on eq.idDisciplina_A = d1.idDisciplina left outer join Disciplina d3 on d3.idDisciplina = eq.idDisciplina_B order by d1.idDisciplina"
	## obtenção dos registros do banco de dados
        cursor.execute(query)
        records = cursor.fetchall()
        dicionario = {}
        dic = {}
        i=1
        for record in records:
                chave = f"diciplina {i}"
                valor = record
                dic = {
                'id': record[0],
                'codigo': record[1],
                'nome': record[2],
                'ha': record[3],
                'pr': record[4] if record[4] else None,
                'eq': record[5] if record[5] else None,
                'ementa': record[6]
        	}
                dicionario[chave] = dic
                i = i + 1
        user_agent = request.headers.get('User-Agent')
        if 'curl' in user_agent:
            return jsonify(dicionario)
        else:
            return render_template('tableHuge.html', dictionary=dicionario)


@app.route('/disciplinas/add', methods = ['POST'])
def create_disciplina():# HORAS GASTAS: 3
        if request.method == "POST":
                disc = request.get_json()
                #print(disc)
                #print(disc['codigo'])
                #print(disc['nome'])
                #print(disc['ha'])
                #print(disc['pr'])
                #print(disc['eq'])
                #print(disc['ementa'])
                #print(request.json)
                #print(request.json['codigo'])
                #print(request.json['nome'])
                #print(request.json['ha'])
                #print(request.json['pr'])
                #print(request.json['eq'])
                #print(request.json['ementa'])
        cursor = db.cursor()

        query = "select d1.idDisciplina, d1.Codigo, d1.Nome, d1.H_A, d2.Codigo as Pre_Requisito, d3.Codigo as Equivalente, d1.ementa from (select d1.Codigo, d1.idDisciplina, d1.Nome, d1.H_A, GROUP_CONCAT(t.Descricao_topicos SEPARATOR ', ') as ementa from Disciplina d1 join Ementa e on e.idEmenta = d1.fk_idEmenta join Topicos t on t.idTopicos = e.fk_idTopicos group by d1.Codigo, d1.idDisciplina, d1.Nome, d1.H_A) d1 left outer join Pre_Requisito pr1 on pr1.idDisciplina_Solicitante = d1.idDisciplina left outer join Disciplina d2 on d2.idDisciplina = pr1.idDisciplina_Requisito left outer join Equivalencia eq on eq.idDisciplina_A = d1.idDisciplina left outer join Disciplina d3 on d3.idDisciplina = eq.idDisciplina_B order by d1.idDisciplina"
        cursor.execute(query)
        records = cursor.fetchall()

        dicionario = {}
        i=1
        for record in records:
                chave = f"disciplina {i}" 
                dicionario[chave] = {
                        'id': record[0],
                        'codigo': record[1],
                        'nome': record[2],
                        'ha': record[3],
                        'pr': record[4] if record[4] else None,
                        'eq': record[5] if record[5] else None,
                        'ementa': record[6]
                }
                i += 1

        temp_pr = 0
        temp_eq = 0
        add_pr = 0
        add_eq = 0
        for key in dicionario:
                valor = dicionario[key]['codigo']
                # VERIFICANDO SE PRE REQUISITO EXISTE
                if request.json['pr'] == valor or request.json['pr'] == "":
                        temp_pr = 1
                        id_pr = dicionario[key]['id']
                        if request.json['pr'] != "":
                        	add_pr = 1
                # VERIFICANDO SE EQUIVALENCIA EXISTE
                if request.json['eq'] == valor or request.json['eq'] == "":
                        temp_eq = 1
                        id_eq = dicionario[key]['id']
                        if request.json['eq'] != "":
                        	add_eq = 1

        if temp_pr == 0 or temp_eq == 0:
                return ".\n.\n.\n.\n.\nEquivalente ou Pre-Requisito nao existente\n"
                abort(404)

        key = 0
        temp = 0
        for key in dicionario:
                valor = dicionario[key]['codigo']
                if request.json['codigo'] == valor:
                        id_exist = dicionario[key]['id']
                        temp = 1
                        key = 0
                        break


        if temp == 0:
                # CASO DISCIPLINA NAO EXISTE
                query = "select MAX(idDisciplina) from Disciplina"
                cursor.execute(query)
                record_nova_disc = cursor.fetchall()
                id_nova_disc = int(record_nova_disc[0][0])+1

                # INSERCAO DE TOPICOS
                query = "select MAX(idTopicos) from Topicos"
                cursor.execute(query)
                records_top = cursor.fetchall()
                id_records_top = int(records_top[0][0])

                insert_top = "INSERT INTO Topicos VALUES(%s,%s)"
                values_top = (id_records_top+1, request.json['ementa'])
                cursor.execute(insert_top, values_top)
                db.commit()

                        # INSERCAO DE EMENTA
                query = "select MAX(idEmenta) from Ementa"
                cursor.execute(query)
                temp_em_2 = cursor.fetchall()
                id_ementa_exist = int(temp_em_2[0][0])+1

                query = "select MAX(Id) from Ementa"
                cursor.execute(query)
                records_em = cursor.fetchall()
                id_records_em = int(records_em[0][0])

                insert_em = "INSERT INTO Ementa VALUES(%s, %s, %s)"
                values_em = (id_ementa_exist, id_records_top+1, id_records_em+1)
                cursor.execute(insert_em, values_em)
                db.commit()

                query = "INSERT INTO Disciplina VALUES(%s, %s, %s, %s, %s)"
                values_nova_disc = (id_nova_disc, request.json['codigo'], request.json['nome'], request.json['ha'], id_ementa_exist)
                cursor.execute(query, values_nova_disc)
                db.commit()

                if add_pr == 1:
                                # SE PRE REQUISITO EXISTE E NAO E VAZIO
                        query = "INSERT INTO Pre_Requisito VALUES(%s, %s)"
                        values_add_pr = (id_nova_disc, id_pr)
                        cursor.execute(query, values_add_pr)
                        db.commit()

                if add_eq == 1:
                                # SE EQUIVALENCIA EXISTE E NAO E VAZIO
                        query = "INSERT INTO Equivalencia VALUES(%s, %s)"
                        values_add_eq = (id_nova_disc, id_eq)
                        cursor.execute(query, values_add_eq)
                        db.commit()
        else:
                # CASO DISCIPLINA EXISTENTE
                # INSERCAO DE TOPICOS 
                query = "select MAX(idTopicos) from Topicos"
                cursor.execute(query)
                records_top = cursor.fetchall()
                id_records_top = int(records_top[0][0])

                insert_top = "INSERT INTO Topicos VALUES(%s,%s)"
                values_top = (id_records_top+1, request.json['ementa'])
                cursor.execute(insert_top, values_top)
                db.commit()

                # INSERCAO DE EMENTA
                query = f"select fk_idEmenta from Disciplina where Codigo = '{valor}'"
                cursor.execute(query)
                temp_em_2 = cursor.fetchall()
                id_ementa_exist = int(temp_em_2[0][0])

                query = "select MAX(Id) from Ementa"
                cursor.execute(query)
                records_em = cursor.fetchall()
                id_records_em = int(records_em[0][0])

                insert_em = "INSERT INTO Ementa VALUES(%s, %s, %s)"
                values_em = (id_ementa_exist, id_records_top+1, id_records_em+1)
                cursor.execute(insert_em, values_em)
                db.commit()

                # ATUALIZA HORA AULA
                query = "UPDATE Disciplina SET H_A = %s WHERE idDisciplina = %s"
                values_ha = (request.json['ha'], id_exist)
                cursor.execute(query, values_ha)
                db.commit()

                # ATUALIZA NOME DA DISCIPLINA
                query = "UPDATE Disciplina SET Nome = %s WHERE idDisciplina = %s"
                values_nome = (request.json['nome'], id_exist)
                cursor.execute(query, values_nome)
                db.commit()

                query = "SELECT idDisciplina_Requisito from Pre_Requisito where idDisciplina_Solicitante = %s"
                value_q1 = (id_exist,)
                cursor.execute(query, value_q1)
                record_q1 = cursor.fetchall()

                valida_q1 = 0
                n = 0
                for k in record_q1:
                        if record_q1[n][0] == id_pr:
                                valida_q1 = 1
                                break
                        n = n+1

                if add_pr == 1 and valida_q1 == 0:
                # SE PRE REQUISITO EXISTE E NAO E VAZIO
                        query = "INSERT INTO Pre_Requisito VALUES(%s, %s)"
                        values_add_pr = (id_exist, id_pr)
                        cursor.execute(query, values_add_pr)
                        db.commit()
                        
                query = "SELECT idDisciplina_B from Equivalencia where idDisciplina_A = %s"
                value_q2 = (id_exist,)
                cursor.execute(query, value_q2)
                record_q2 = cursor.fetchall()

                valida_q2 = 0
                n = 0
                for k in record_q2:
                        if record_q2[n][0] == id_eq:
                                valida_q2 = 1
                                break
                        n = n+1

                if add_eq == 1 and valida_q2 == 0:
                        # SE EQUIVALENCIA EXISTE E NAO E VAZIO
                        query = "INSERT INTO Equivalencia VALUES(%s, %s)"
                        values_add_eq = (id_exist, id_eq)
                        cursor.execute(query, values_add_eq)
                        db.commit()

        return "\n.\n.\n.\nInserido/Alterado com sucesso\n", 201


if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8081, debug=True)
