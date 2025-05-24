import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from models import db, Livro

load_dotenv() #Carrega as variáveis do .env

app = Flask(__name__)
CORS(app)

# Configuração do Banco
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Criar as tabelas (executar uma vez)
with app.app_context():
    db.create_all()

# Rota para listar todos os livros
@app.route('/livros', methods=['GET'])
def listar_livros():
    livros = Livro.query.all()
    return jsonify([{'id': l.id, 'titulo': l.titulo, 'autor': l.autor, 'ano': l.ano} for l in livros])

# Rota para adicionar livro
@app.route('/livros', methods=['POST'])
def adicionar_livro():
    data = request.get_json()
    novo = Livro(titulo=data['livro'], autor=data['autor'], ano=data.get("ano"))
    db.session.add(novo)
    db.session.commit()
    return jsonify({'mensagem': 'Livro adicionado com sucesso'}), 201

@app.route('/livros/<int:id>', methods = ['PUT'])
def atualizar_livro(id):
    id_certo = int(id)
    data = request.get_json()
    livro = Livro.query.get(id_certo)
    if not livro:
        return jsonify({'erro': 'Livro não encontrado'}), 404
    livro.titulo = data['titulo']
    livro.autor = data['autor']
    livro.ano = data.get('ano')
    db.session.commit()
    return jsonify({'mensagem': 'Livro atualizado com sucesso'})

# Rota para deletar
@app.route('/livros/<int:id>', methods=['DELETE'])
def deletar_livro(id):
    id_certo = int(id)
    livro = Livro.query.get(id_certo)
    if not livro:
        return jsonify({'erro': 'Livro não encontrado'}), 404
    db.session.delete(livro)
    db.session.commit()
    return jsonify({'mensagem': 'Livro deletado'})
