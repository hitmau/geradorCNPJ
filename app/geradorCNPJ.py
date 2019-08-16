#!/usr/bin/env python
#encoding: utf-8
#coding: utf-8
#Autor Maurcio Rodrigues (mauriciosist@gmail.com)
#V 1.0.27
import random
import urllib, json, time
import pymysql.cursors

def cnpj(self, punctuation = False):
    n = [random.randrange(10) for i in range(8)] + [0, 0, 0, 1]
    v = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5, 6]
    # calcula dígito 1 e acrescenta ao total
    s = sum(x * y for x, y in zip(reversed(n), v))
    d1 = 11 - s % 11
    if d1 >= 10:
      d1 = 0
    n.append(d1)
    # idem para o dígito 2
    s = sum(x * y for x, y in zip(reversed(n), v))
    d2 = 11 - s % 11
    if d2 >= 10:
      d2 = 0
    n.append(d2)
    if punctuation:
      return "%d%d.%d%d%d.%d%d%d/%d%d%d%d-%d%d" % tuple(n)
    else:
      return "%d%d%d%d%d%d%d%d%d%d%d%d%d%d" % tuple(n)

def abrirConexao():
    try:
        #global cursor, connection
        connection = pymysql.connect(host='localhost',user='root',db='cnpj',charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        print(cursor)
        print('conexao aberta')
        return cursor, connection
    except Exception as e:
        print ("Erro: Impossível abrir conexão! " + str(e))
        return False

def consulta(cnpj):
    global cursor, connection
    sql = "SELECT count(*) as count FROM `dados` WHERE replace(replace(replace(json,'.',''),'-',''),'/','') = '" + str(cnpj) + "';"
    #print("sql")
    try:
        # Execute o comando SQL
        cursor.execute(sql)
        # le todas as linhas da tabela.
        linhas = cursor.fetchall()
        #print sql
        #print (linhas)
        #retorno = []
        contador = 0
        for linha in linhas:
            contador = linha['count']
            if contador <> 0:
                contador += 1
        if contador > 0:
            return False
        else:
            return True
    except:
        print ("Erro: Impossível obter dados (consultaContato)")
        return False


def insere(string):
    global cursor, connection
    #print('33')

     #instancia um objeto cursor utilizando o método cursor

    #print("insert " + str(nome))
    # construção da string SQL que insere um registro.
    #print('44')
    #print(string)
    sql = "INSERT INTO dados (`json`, `nome_fantasia`, `capital_social`, `ultima_atualizacao`, `atividade_principal`, `tipo`, `nome`, `telefone`, `email`, `situacao`, `atividades_secundarias`, `uf`, `municipio`, `bairro`, `cep`, `numero`, `logradouro`) VALUES ('" + str(string[0]) + "', '" + str(string[1]) + "', '" + str(string[2]) + "', '" + str(string[3]) + "', '" + str(string[4]) + "', '" + str(string[5]) + "', '" + str(string[6]) + "', '" + str(string[7]) + "', '" + str(string[8]) + "', '" + str(string[9]) + "', '" + str(string[10]) + "', '" + str(string[11]) + "', '" + str(string[12]) + "', '" + str(string[13]) + "', '" + str(string[14]) + "', '" + str(string[15]) + "', '" + str(string[16]) + "');"

    try:
        # Execute o comando

        #print('55')
        #print(sql)
        cursor.execute(sql)
        #print('66')
        connection.commit()
        print('------------ - - -  Inserido com sucesso!')
        return True
    except:
        print("Erro na inserção de dados!")
        connection.rollback()
        return False


def insere2(string):
    global cursor, connection
    sql = "INSERT INTO nao_valido (cnpj) VALUES ('" + str(string) + "');"
    try:
        #print(sql)
        if bool(consulta2(string)):
            cursor.execute(sql)
            connection.commit()
            print('Novo cnpj')
            return True
        else:
            print('Gerador ja gerou este CNPJ!')
            return False
    except Exception as e:
        print("Erro na inserção de dados! insert2: " + str(e))
        connection.rollback()
        return False


def consulta2(cnpj):
    global cursor, connection
    sql = "SELECT count(*) as count FROM nao_valido WHERE replace(replace(replace(cnpj,'.',''),'-',''),'/','') = '" + str(cnpj) + "';"
    try:
        #print(sql)
        cursor.execute(sql)
        linhas = cursor.fetchall()
        contador = 0
        for linha in linhas:
            contador = linha['count']
            if contador > 0:
                contador += 1

        if contador == 0:
            #print('1')
            return True
        else:
            #print('2')
            return False
    except:
        return False
        print ("Erro: Impossível obter dados (consultaContato)")

def valido(sn, cnpj):
    global cursor, connection
    sql = "update nao_valido set valido = '" + str(sn) + "' where cnpj = '" + str(cnpj) + "';"
    try:
        cursor.execute(sql)
        connection.commit()
        return True
    except:
        print ("Erro: Impossível atualizar")
        connection.rollback()
        return False

def total():
    global cursor, connection
    sql = "select d, n from (select count(*) as d from dados) d, (select count(*) as n from nao_valido) n;"
    try:
        cursor.execute(sql)
        linhas = cursor.fetchall()
        dados = 0
        naoValido = 0
        for linha in linhas:
            dados = linha['d']
            naoValido = linha['n']
        #print(dados)
        #print(naoValido)
        return dados, naoValido
    except:
        return False, False
        print ("Erro: Impossível obter dados (total)")

if abrirConexao() == False:
    print('erro de conexao')
    conn = pymysql.connect(host='localhost', user='root') #,password='passwd')
    conn.cursor().execute('create database cnpj2')
    conn.cursor().execute('create table cnpj2.dados (PersonID int, City varchar(255));')
    dados
    nao_valido
else:
    cursor, connection = abrirConexao()
    while True:
    #for i in range(1,10):
        _cnpj = cnpj(True)
        if bool(insere2(_cnpj)):
            if bool(consulta(_cnpj)):
                url = "https://www.receitaws.com.br/v1/cnpj/" + str(_cnpj)
                try:
                    response = urllib.urlopen(url)
                except:
                    print('Sem conexao!')
                    pass
                print(str(total()[1]) + ' - ' + url)
                lista = []
                try:
                    teste = json.loads(response.read())
                    #print('22')
                    print(teste.get("cnpj"))
                    lista.append(teste.get("cnpj"))
                    #print('a')
                    lista.append(teste.get("fantasia"))
                    #print('b')
                    lista.append(teste.get("capital_social"))
                    #print('c')
                    lista.append(teste.get("ultima_atualizacao"))
                    atividade_p = teste.get("atividade_principal")[0]['code']
                    atividade_p = atividade_p
                    #print('d')
                    lista.append(atividade_p)
                    #print('e')
                    lista.append(teste.get("tipo"))
                    #print('f')
                    lista.append(teste.get("nome"))
                    #print('g')
                    lista.append(teste.get("telefone"))
                    #print('h')
                    lista.append(teste.get("email"))
                    #print('i')
                    lista.append(teste.get("situacao"))
                    atividade_s = teste.get("atividades_secundarias")[0]['code']
                    atividade_s = atividade_s
                    #print('j')
                    lista.append(atividade_s)
                    #print('k')
                    lista.append(teste.get("uf"))
                    #print('l')
                    lista.append(teste.get("municipio"))
                    #print('m')
                    lista.append(teste.get("bairro"))
                    #print('n')
                    lista.append(teste.get("cep"))
                    #print('o')
                    lista.append(teste.get("numero"))
                    lista.append(teste.get("logradouro"))
                    insere(lista)
                    s = ((total()[0] * 100.00) / total()[1])
                    print('Insert de numero: ' + str(total()[0]) + ' total de {:.2f}%.'.format(s) + ' para ' + str(total()[1]) + ' tentativas!')
                    valido('S', _cnpj)
                except Exception as e:
                    print('Erro: ' + str(e))
                    valido('N', _cnpj)
                    pass
            else:
                print('CNPJ ' + str(_cnpj) + ' ja existe!')


#abrirConexao()
#print("\n".join([cnpj(True) for i in range(10)]))
