import asyncio
from flask import Flask, Blueprint
from flask import request
from models import QuestoesDAO, RespostasDAO

RespostasBP = Blueprint('resposta', __name__, url_prefix='/resposta')


@RespostasBP.route('/consultar/<int:id>', methods=['GET'])
def resposta_consultar_por_id(id=None):
    resposta = RespostasDAO.buscar_resposta_por_id(id)
    if resposta:
        resposta = resposta.__dict__ 

    return {
        'Status': 200 if resposta else 404, 
        'id': id,
        'resposta': resposta
    }, 200 if resposta else 404


@RespostasBP.route('/consultar/questao/<int:id>', methods=['GET'])
@RespostasBP.route('/consultar/questao/<int:id>/<int:pagina>', methods=['GET'])
@RespostasBP.route('/consultar/questao/<int:id>/<int:pagina>/<int:quantidade>', methods=['GET'])
def resposta_consultar_por_questao_id(id=None, pagina=1, quantidade=10):
    retorno = []

    encontrados = RespostasDAO.buscar_respostas_por_questao(id, pagina, quantidade) 
    for resposta in encontrados:
        retorno.append(resposta.__dict__)

    return {
        'Status': 200,
        'questoes': retorno
    }, 200

@RespostasBP.route('/cadastrar/', methods=['POST'])
def resposta_cadastrar():
    questao_id = request.form['questao_id']
    texto = request.form['titulo']
    pontuacao = request.form['texto']
    
    id = RespostasDAO.criar_resposta(questao_id, texto, pontuacao)

    return {'Status': 200, 'id':id}, 200