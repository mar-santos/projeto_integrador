from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request
from flask import redirect
from flask import session

app = Flask(__name__)
app.secret_key = 'b175855202d537a1b07a1cbbee8ffc197e2af9c5289a6adfd4b4aa63c3f77861'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tapete.db"
db = SQLAlchemy()
db.init_app(app)

# Inicializar Classe e criar banco de dados e tabelas
class Product(db.Model):
    __tablename__ = "pedido"
    id_pedido = db.Column(db.Integer, primary_key=True)
    data_pedido = db.Column(db.String(100))
    nome = db.Column(db.String(200), nullable=False)
    endereco = db.Column(db.String(250))
    telefone = db.Column(db.String(100), nullable=False)
    servico = db.Column(db.String(100))
    valor = db.Column(db.Integer)

def __init__(self,
             data_pedido: str, 
             nome: str, 
             endereco: str,
             telefone: str, 
             servico: str, 
             valor: int) -> None:
    
    self.data_pedido = data_pedido
    self.nome = nome
    self.endereco = endereco
    self.telefone = telefone
    self.servico = servico
    self.valor = valor


# Definição das rotas estáticas
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/sobre")
def sobre_nos():
    return render_template('sobre_nos.html')

@app.route("/servicos")
def servicos():
    return render_template('servicos.html')

@app.route("/contatos")
def contatos():
    return render_template('Contatos.html')


# Login e senha do administrador
credenciais_usuarios = {
    "admin": "admin"
}

# Login e controle de acesso as áreas restritas
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in credenciais_usuarios and credenciais_usuarios[username] == password:
            session['logged_in'] = True
            return redirect("/cadastrar_pedido")
        else:
            return render_template("/erro_login.html")

    return render_template('login.html')

@app.before_request
def verificar_autenticacao():
    endpoints_protegidos = ["/cadastrar_pedido", "/listar_pedidos"]
    if request.path in endpoints_protegidos:
        if not session.get('logged_in'):
            return redirect("/login")

@app.route("/erro_login.html")
def erro_login():
    return render_template("erro_login.html")

# Definição das rotas dinâmicas e CRUD
@app.route("/listar_pedidos", methods=['GET', 'POST'])
def listar_pedidos():
    if request.method == "POST":
        termo = request.form["pesquisa"]
        resultado = db.session.execute(db.select(Product).filter(
            (Product.data_pedido.like(f'%{termo}%')) | 
            (Product.nome.like(f'%{termo}%')) |
            (Product.endereco.like(f'%{termo}%')) |
            (Product.telefone.like(f'%{termo}%')) |
            (Product.servico.like(f'%{termo}%')) |
            (Product.valor.like(f'%{termo}%')))
        ).scalars()
        return render_template('pedidos.html', pedidos=resultado)
    else:
        pedidos = db.session.execute(db.select(Product)).scalars()
        return render_template('pedidos.html', pedidos=pedidos)

@app.route("/cadastrar_pedido", methods=["GET", "POST"])
def cadastrar_pedido():
    if request.method == "POST":
        status = {"type": "sucesso", "message": "Pedido cadastrado com sucesso!"}
        try:
            dados = request.form
            #data_pedido = datetime.strptime(dados["data_pedido"], "%Y-%m-%d").strftime("%d/%m/%Y")
            pedido = Product(
                data_pedido=dados["data_pedido"],
                nome=dados["nome"],
                endereco=dados["endereco"],
                telefone=dados["telefone"],
                servico=dados["servico"],
                valor=(dados["valor"])
            )
            db.session.add(pedido)
            db.session.commit()
            return render_template("cadastrar_pedido.html", status=status)
        except:
            status = {"type": "erro", "message": f"Houve um problema ao cadastrar o pedido {dados['nome']}!"}
            return render_template("cadastrar_pedido.html", status=status)
    else:
        return render_template("cadastrar_pedido.html")
    
@app.route("/editar_pedido/<int:id_pedido>", methods=["GET", "POST"])
def editar_pedido(id_pedido):
    if request.method == "POST":
        dados_editados = request.form
        pedido = db.session.execute(db.select(Product).filter(Product.id_pedido == id_pedido)).scalar()

        pedido.data_pedido = dados_editados["data_pedido"]
        pedido.nome = dados_editados["nome"]
        pedido.endereco = dados_editados["endereco"]
        pedido.telefone = dados_editados["telefone"]
        pedido.servico = dados_editados["servico"]
        pedido.valor = dados_editados["valor"]

        db.session.commit()
        return redirect("/listar_pedidos")
    
    else:
        pedido_editado = db.session.execute(db.select(Product).filter(Product.id_pedido == id_pedido)).scalar()
        return render_template('editar_pedido.html', pedido=pedido_editado)

@app.route("/deletar_pedido/<int:id_pedido>")
def deletar_pedido(id_pedido):
    pedido_deletado = db.session.execute(db.select(Product).filter(Product.id_pedido == id_pedido)).scalar()
    db.session.delete(pedido_deletado)
    db.session.commit()
    return redirect("/listar_pedidos")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all() # Criação do BD caso o mesmo não exista
        app.run(debug=True)