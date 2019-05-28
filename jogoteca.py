from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)

app.secret_key = "alura" #somente para usar o session

class Jogo:
    def __init__(self, nome,categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario:
    def __init__(self, id, nome,senha):
        self.id = id
        self.nome = nome
        self.senha = senha


usuario1 = Usuario("gui","Guilherme Golfeto", "1234")
usuario2 = Usuario("mat", "Mathias", "1234")
usuario3 = Usuario("fal", "Fulano", "1234")

usuarios = {usuario1.id:usuario1, usuario2.id:usuario2, usuario3.id: usuario3 }

jogo1 = Jogo("Super Mario","Ação","SNES")
jogo2 = Jogo("Pokémon Gold", "RPG", "GBC")
lista = [jogo1, jogo2]

@app.route("/")
def index():
    return render_template('lista.html',titulo ="Jogos",jogos = lista)

@app.route("/novo")
def novo():
    if "usuario_logado" not in session or session["usuario_logado"] == None:
        return redirect(url_for("login",state=url_for("novo")))
    return render_template('novo.html', titulo="Novo Jogo")

@app.route("/criar",methods=["POST",])
def criar():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    console = request.form["console"]
    jogo = Jogo(nome,categoria,console)
    lista.append(jogo)
    return redirect(url_for("index"))


@app.route("/login")
def login():
    proxima = request.args.get("state") #query string
    return render_template("login.html", proxima=proxima)

@app.route("/autenticar",methods=["POST",])
def autenticar():
    if request.form["usuario"] in usuarios:
        usuario = usuarios[request.form["usuario"]]
        if usuario.senha == request.form["senha"]:
            session["usuario_logado"] = usuario.id
            flash(usuario.nome + " logou com sucesso!") #guarda um tipo cookie por 1 acesso, usado somente para mensagems
            proxima = request.form["state"]
            return redirect(proxima)
        else:
            flash("senha incorreta!")
            return redirect(url_for("login"))
    else:
        flash("não logado, tente novamente!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session["usuario_logado"] = None
    flash("Nenhum usuario logado")
    return redirect(url_for("login"))

app.run(debug=True)