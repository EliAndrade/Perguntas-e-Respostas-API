import asyncio
import gc

from flask import Flask, Blueprint
from flask import request
from models import QuestoesDAO, RespostasDAO

from utils import IAUtils 


QuestoesBP = Blueprint('questao', __name__, url_prefix='/questao')

@QuestoesBP.route('/consultar/<int:id>', methods=['GET'])
def questao_consultar_por_id(id=None):
    questao = QuestoesDAO.buscar_questao_por_id(id)
    return {
        'Status': 200 if questao else 404, 
        'id': id,
        'questao': questao.__dict__
    }, 200 if questao else 404

@QuestoesBP.route('/consultar/professor/<int:id>', methods=['GET'])
@QuestoesBP.route('/consultar/professor/<int:id>/<int:pagina>', methods=['GET'])
@QuestoesBP.route('/consultar/professor/<int:id>/<int:pagina>/<int:quantidade>', methods=['GET'])
def questao_consultar_por_professor_id(id=None, pagina=1, quantidade=10):
    retorno = []

    encontrados = QuestoesDAO.buscar_questoes_por_professor(id, pagina, quantidade)
    for questao in encontrados:
        retorno.append(questao.__dict__)

    return {
        'Status': 200,
        'questoes': retorno
    }, 200

@QuestoesBP.route('/cadastrar/', methods=['POST'])
def questao_cadastrar():
    professor_id = request.form['professor_id']
    titulo = request.form['titulo']
    texto = request.form['texto']
    
    id = QuestoesDAO.criar_questao(professor_id, titulo, texto)

    return {'Status': 200, 'id':id}, 200

@QuestoesBP.route('/editar/', methods=['POST'])
def questao_editar():
    questao_id = request.form['questao_id']
    professor_id = request.form['professor_id']
    titulo = request.form['titulo']
    texto = request.form['texto']
    
    QuestoesDAO.editar_questao(questao_id, professor_id, titulo, texto)

    return {'Status': 200}, 200

    
@QuestoesBP.route('/treinar/<int:id>', methods=['POST'])
def treinar_questao(id=None):
    questao = QuestoesDAO.buscar_questao_por_id(id)
    if not questao:
        return {'Status': 404}, 404

    resps = []
    encontrados = RespostasDAO.buscar_respostas_por_questao(id, todas = True) 
    for resposta in encontrados:
        resps.append(resposta.__dict__)

    modelo, vetorizador = IAUtils.treinar(resps)
    QuestoesDAO.adicionar_modelo_questao(id, modelo, vetorizador)

    del modelo
    del vetorizador
    gc.collect()

    return {'Status': 200}, 200

@QuestoesBP.route('/avaliar/<int:id>', methods=['POST'])
def avaliar_resposta(id=None):
    texto = request.form['texto']
    modelo, vetorizador = QuestoesDAO.carregar_modelo_questao(id)
    if not modelo:
        return {'Status': 404}, 404

    nota = IAUtils.avaliar(modelo, vetorizador, texto)
    del modelo
    del vetorizador
    gc.collect()

    return {'Status': 200, 'nota': str(nota[0])}, 200