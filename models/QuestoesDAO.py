import os
import json
import mariadb
from models.connection import get_connection


class Questao():
    def __init__(self, titulo=None, texto=None, questao_id=0, professor_id=0):
        self.questao_id = questao_id
        self.professor_id = professor_id
        self.titulo = titulo
        self.texto = texto
    


def buscar_questao_por_id(questao_id):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            '''
                SELECT questao_id, professor_id, titulo, texto
                FROM questoes
                WHERE questao_id = %s;
            ''',
            (questao_id,)
        )

        linha = cur.fetchone()
        if linha:
            questao_id, professor_id, titulo, texto = linha
            return Questao(questao_id, professor_id, titulo, texto)
        else:
            return None
        
        cur.close()
    except Exception as e:
        cur.close()
        raise e


def buscar_questoes_por_professor(professor_id, pagina=1, quantidade=10):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            '''
                SELECT questao_id, professor_id, titulo, texto
                FROM questoes
                WHERE professor_id = %s
                LIMIT %s, %s
            ''',
            (professor_id, pagina-1, quantidade)
        )

        retorno = []
        for linha in cur.fetchall():
            questao_id, professor_id, titulo, texto = linha
            retorno.append(Questao(questao_id, professor_id, titulo, texto))
        
        cur.close()
        return retorno
    except Exception as e:
        cur.close()
        raise e


def buscar_questoes_por_texto(professor_id, texto):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            '''
                SELECT questao_id, professor_id, titulo, texto
                FROM questoes
                WHERE professor_id = %s
                AND texto LIKE %s
                LIMIT %s, %s
            ''',
            (professor_id, texto)
        )

        retorno = []
        for linha in cur.fetchall():
            questao_id, professor_id, titulo, texto = linha
            retorno.append(Questao(questao_id, professor_id, titulo, texto))
        

        cur.close()
        return retorno
    except Exception as e:
        cur.close()
        raise e


        
def criar_questao(professor_id, titulo, texto):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            '''
            INSERT questoes (professor_id, titulo, texto)
            VALUES (%s, %s, %s); 
            ''',
            (professor_id, titulo, texto)
        )
        conn.commit()
        cur.execute('''
            SELECT LAST_INSERT_ID();
        ''')

        linha = cur.fetchone()
        cur.close()
        return linha[0]
    except Exception as e:
        cur.close()
        raise e

def editar_questao(questao_id, professor_id, titulo, texto):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            '''
            UPDATE questoes
            SET 
                modelo = %s, 
            WHERE questao_id = %s
            AND professor_id = %s
                
            ''',
            (titulo, texto, questao_id, professor_id)
        )
        conn.commit()
        return True
    except Exception as e:
        cur.close()
        raise e

def adicionar_modelo_questao(questao_id, modelo, vetorizador): 
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            '''
            UPDATE questoes
            SET 
                modelo = %s,
                vetorizador = %s
            WHERE questao_id = %s
            ''',
            (modelo, vetorizador, questao_id)
        )
        conn.commit()
        return True
    except Exception as e:
        cur.close()
        raise e

def carregar_modelo_questao(questao_id): 
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            '''
            SELECT modelo, vetorizador FROM questoes
            WHERE questao_id = %s
            ''',
            (questao_id,)
        )
        linha = cur.fetchone()
        cur.close()
        return linha[0], linha[1]
    except Exception as e:
        cur.close()
        raise e