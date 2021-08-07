import os
import json
import mariadb
from models.connection import get_connection


class Resposta():
    def __init__(self, questao_id=0, resposta_id=0, texto=None, nota=None):
        self.nota = nota
        self.texto = texto
        self.questao_id = questao_id
        self.resposta_id = resposta_id


def buscar_resposta_por_id(resposta_id):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            '''
                SELECT resposta_id, questao_id, texto, nota
                FROM respostas
                WHERE resposta_id = %s;
            ''',
            (resposta_id,)
        )

        linha = cur.fetchone()
        if linha:
            resposta_id, questao_id, texto, nota = linha
            return Resposta(resposta_id, questao_id, texto, nota)
        else:
            return None
        
        cur.close()
    except Exception as e:
        cur.close()
        raise e


def buscar_respostas_por_questao(questao_id, pagina=1, quantidade=10, todas=False):
    conn = get_connection()
    cur = conn.cursor()

    try:
        if not todas:
            cur.execute(           
            '''
                    SELECT resposta_id, questao_id, texto, nota
                    FROM respostas
                    WHERE questao_id = %s
                    'LIMIT %s, %s'
                ''',
                (questao_id, pagina-1, quantidade)
            )
        else:
            cur.execute(           
            '''
                    SELECT resposta_id, questao_id, texto, nota
                    FROM respostas
                    WHERE questao_id = %s;
                ''',
                (questao_id,)
            )

        retorno = []
        for linha in cur.fetchall():
            resposta_id, questao_id, texto, nota = linha
            retorno.append(Resposta(resposta_id, questao_id, texto, nota))
        
        cur.close()
        return retorno
    except Exception as e:
        cur.close()
        raise e


def criar_resposta(questao_id, texto, nota):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            '''
            INSERT resposta (questao_id, texto, nota)
            VALUES (%s, %s, %s); 
            ''',
            (questao_id, texto, nota)
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


def editar_resposta(resposta_id, questao_id, texto, nota):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            '''
            UPDATE resposta
            SET 
                texto = %s, 
                nota = %s
            WHERE resposta_id = %s
            AND questao_id = %s
                
            ''',
            (texto, nota, resposta_id, questao_id)
        )
        conn.commit()
        return True
    except Exception as e:
        cur.close()
        raise e