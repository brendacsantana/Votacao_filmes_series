from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Criar tabela (só uma vez)
with sqlite3.connect('filmes_series.db') as conexao:
    conexao.execute('''CREATE TABLE IF NOT EXISTS filmes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        genero TEXT NOT NULL,
        descricao TEXT,
        imagem TEXT NOT NULL,
        naogostei INTEGER NOT NULL DEFAULT 0,
        gostei INTEGER NOT NULL DEFAULT 0
    )''')

# Inserir dados iniciais se estiver vazio
filmes_series = [
    ('Atividade Paranormal', 'Terror', 'casal enfrenta eventos paranormais', 'https://br.web.img3.acsta.net/c_310_420/medias/nmedia/18/87/89/84/20028680.jpg'),
    ('Jogos Vorazes', 'Ação', 'Distopia de adolescentes que lutam pela sobrevivência', 'https://br.web.img3.acsta.net/pictures/14/09/26/22/42/410634.jpg'),
    ('Tinker Bell', 'Animação', 'Aventuras de uma fada em um novo mundo', 'https://static.wikia.nocookie.net/disneyfadas/images/2/24/Tinker_bell_filme_capa.jpg'),
    ('Vingadores: Ultimato', 'Aventura', 'Heróis unidos para salvar o universo', 'https://upload.wikimedia.org/wikipedia/pt/thumb/9/9b/Avengers_Endgame.jpg/250px-Avengers_Endgame.jpg'),
    ('Donas de Casas Desesperadas', 'Drama', 'Cotidiano de vizinhos em uma pequena cidade', 'https://images.justwatch.com/poster/242812756/s332/temporada-1'),
]

with sqlite3.connect('filmes_series.db') as conexao:
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM filmes")
    dados = cursor.fetchall()
    if len(dados) == 0:
        for titulo, genero, descricao, imagem in filmes_series:
            cursor.execute('INSERT INTO filmes(titulo, genero, descricao, imagem) VALUES (?,?,?,?)',
                           (titulo, genero, descricao, imagem))
        conexao.commit()

def inserir_filmes(titulo, genero, descricao, imagem):
    with sqlite3.connect('filmes_series.db') as conexao:
        conexao.execute(
            'INSERT INTO filmes(titulo, genero, descricao, imagem) VALUES (?,?,?,?)',
            (titulo, genero, descricao, imagem)
        )
        conexao.commit()

def totais_gerais():
    with sqlite3.connect('filmes_series.db') as conexao:
        cursor = conexao.execute('SELECT SUM(gostei), SUM(naogostei) FROM filmes')
        r = cursor.fetchone()
        return (r[0] or 0, r[1] or 0)

def votar(id, tipo):
    with sqlite3.connect('filmes_series.db') as conexao:
        if tipo == 'gostei':
            conexao.execute('UPDATE filmes SET gostei = gostei + 1 WHERE id = ?', (id,))
        elif tipo == 'naogostei':
            conexao.execute('UPDATE filmes SET naogostei = naogostei + 1 WHERE id = ?', (id,))
        conexao.commit()

def listar_filmes():
    with sqlite3.connect('filmes_series.db') as conexao:
        cursor = conexao.execute('SELECT id, titulo, genero, descricao, imagem, gostei, naogostei FROM filmes')
        dados = cursor.fetchall()
        return dados

@app.route('/')
def index():
    filmes = listar_filmes()
    total_g, total_ng = totais_gerais()
    return render_template('index.html', filmes=filmes, total_gostei=total_g, total_naoGostei=total_ng)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    titulo = request.form.get('titulo', '').strip()
    genero = request.form.get('genero', '').strip()
    imagem = request.form.get('imagem', '').strip()
    descricao = request.form.get('descricao', '').strip()

    if titulo and genero and imagem:
        inserir_filmes(titulo, genero, descricao, imagem)
    return redirect('/')

@app.route('/votar/<int:id>/<tipo>')
def rota_votar(id, tipo):
    votar(id, tipo)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
