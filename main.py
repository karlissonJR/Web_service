from flask import Flask
from flask import render_template
from flask import abort
from flask import request
from flask import redirect, url_for

import json

app = Flask(__name__)


with open("livros.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

livros = jsonObject['data']

@app.route('/', methods=['GET'])
def index(data=livros):
    return render_template('index.html', data=data)

@app.route('/livros/<int:idLivro>', methods=['GET'])
def detalhe_livro(idLivro):
    resultado = [resultado for resultado in livros if resultado['id'] == idLivro]

    livro = resultado[0]

    return render_template('detail.html', livro=livro)

@app.route('/livros/novo', methods=['GET'])
def novo_livro():
    return render_template('add.html')

@app.route('/livros/<int:idLivro>/atualizar', methods=['GET'])
def atualizar_livro(idLivro):
    resultado = [resultado for resultado in livros if resultado['id'] == idLivro]

    livro = resultado[0]
    return render_template('update.html', livro=livro)

@app.route('/livros/criar/<titulo>/<autor>')
def criar_livro(titulo, autor):
    livro = {
        'id': livros[-1]['id'] + 1,
        'titulo': titulo,
        'autor': autor
    }
    livros.append(livro)
    return redirect(url_for('index'))

@app.route('/livros/atualizar/<int:idLivro>/<titulo>/<autor>')
def mudar_livro(idLivro, titulo, autor):
    resultado = [resultado for resultado in livros if resultado['id'] == idLivro]
    
    resultado[0]['titulo'] = titulo
    resultado[0]['autor'] = autor
    
    return redirect(url_for('index'))

@app.route('/livros/<int:idLivro>/deletar')
def excluir_livro(idLivro):
    resultado = [resultado for resultado in livros if resultado['id'] == idLivro]
    if len(resultado) == 0:
        abort(404)
    livros.remove(resultado[0])
    return redirect(url_for('index'))

if __name__ == "__main__":
    print("Servidor no ar!")
    app.run(host='0.0.0.0', debug=True)