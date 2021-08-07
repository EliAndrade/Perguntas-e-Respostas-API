import asyncio
from flask import Flask
from flask import request

app = Flask(__name__) 

@app.errorhandler(404)
def page_not_found(e):
    return {"Status": 404}, 404

@app.errorhandler(500)
def internal_server_error(e):
    return {"Status": 500}, 404

if __name__ == '__main__':
    from blueprints.QuestoesBP import QuestoesBP
    app.register_blueprint(QuestoesBP)

    from blueprints.RespostasBP import RespostasBP
    app.register_blueprint(RespostasBP)

    app.run(debug=True)