from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy import func
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from datetime import datetime
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP

app = Flask(__name__)
app.secret_key = 'b175855202d537a1b07a1cbbee8ffc197e2af9c5289a6adfd4b4aa63c3f77861'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tapete.db" #Associar ao banco de dados tapete.bd
db = SQLAlchemy()
db.init_app(app)


# Inicializar Classe e criar as tabelas pedido e despesas
class Product(db.Model):
    __tablename__ = "pedido"
    id_pedido = db.Column(db.Integer, primary_key=True)
    data_pedido = db.Column(db.String(100))
    data_entrega = db.Column(db.String(100))
    id_ficha = db.Column(db. String(30))
    nome = db.Column(db.String(200), nullable=False)
    endereco = db.Column(db.String(250))
    cidade = db.Column(db.String(50))
    telefone = db.Column(db.String(100), nullable=False)
    servico = db.Column(db.String(100))
    valor = db.Column(db.String(30))
    status = db.Column(db.String(30))

def __init__(self,
             data_pedido: str,
             data_entrega: str,
             id_ficha: str, 
             nome: str, 
             endereco: str,
             cidade: str,
             telefone: str, 
             servico: str, 
             valor: str,
             status: str) -> None:
    
    self.data_pedido = data_pedido
    self.data_entrega = data_entrega
    self.id_ficha = id_ficha
    self.nome = nome
    self.endereco = endereco
    self.cidade = cidade
    self.telefone = telefone
    self.servico = servico
    self.valor = valor
    self.status = status

class Product2(db.Model):
    __tablename__ = "despesa"
    id_despesa = db.Column(db.Integer, primary_key=True)
    despesa_data = db.Column(db.String(30))
    despesa_nome = db.Column(db.String(100))
    despesa_qtde = db.Column(db.String(100))
    despesa_valor = db.Column(db.String(100))

def __init__(self,
             despesa_data: str, 
             despesa_nome: str, 
             despesa_qtde: str,
             despesa_valor: str) -> None:
    
    self.despesa_data = despesa_data
    self.despesa_nome = despesa_nome
    self.despesa_qtde = despesa_qtde
    self.despesa_valor = despesa_valor


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
    return render_template('contatos.html')


@app.route("/erro_login.html")
def erro_login():
    return render_template("erro_login.html")

@app.route("/erro_pagina_404")
def erro_pagina_404():
    return render_template("erro_pagina_404.html")


@app.route("/erro_pagina_403")
def erro_pagina_403():
    return render_template("erro_pagina_403.html")


# Login e senha do administrador
credenciais_usuarios = {
    "admin": "admin"
}


# Controle de acesso as áreas restritas
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
    endpoints_protegidos = ["/cadastrar_pedido", "/listar_pedidos", "/cadastrar_despesas", "/listar_despesas","/search", "/search_p", "/search_e"]
    if request.path in endpoints_protegidos:
        if not session.get('logged_in'):
            return redirect("/erro_pagina_403")


# Definição das rotas dinâmicas. CRUD de pedidos e despesas
@app.route("/listar_pedidos", methods=['GET', 'POST'])
def listar_pedidos():
    if request.method == "POST":
        termo = request.form["pesquisa"]
        resultado = db.session.execute(db.select(Product).filter(
            (Product.data_pedido.like(f'%{termo}%')) |
            (Product.data_entrega.like(f'%{termo}%')) |
            (Product.id_ficha.like(f'%{termo}%')) |
            (Product.nome.like(f'%{termo}%')) |
            (Product.endereco.like(f'%{termo}%')) |
            (Product.cidade.like(f'%{termo}%')) |
            (Product.telefone.like(f'%{termo}%')) |
            (Product.servico.like(f'%{termo}%')) |
            (Product.valor.like(f'%{termo}%')) |
            (Product.status.like(f'%{termo}%')))
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
            pedido = Product(
                data_pedido=dados["data_pedido"],
                data_entrega=dados["data_entrega"],
                id_ficha=dados["id_ficha"],
                nome=dados["nome"],
                endereco=dados["endereco"],
                cidade=dados["cidade"],
                telefone=dados["telefone"],
                servico=dados["servico"],
                valor=(dados["valor"]),
                status=(dados["status"])
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
        pedido.data_entrega = dados_editados["data_entrega"]
        pedido.id_ficha = dados_editados["id_ficha"]
        pedido.nome = dados_editados["nome"]
        pedido.endereco = dados_editados["endereco"]
        pedido.cidade = dados_editados["cidade"]
        pedido.telefone = dados_editados["telefone"]
        pedido.servico = dados_editados["servico"]
        pedido.valor = dados_editados["valor"]
        pedido.status = dados_editados["status"]

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


@app.route("/listar_despesas", methods=['GET', 'POST'])
def listar_despesas():
    if request.method == "POST":
        termo = request.form["pesquisa"]
        resultado = db.session.execute(db.select(Product2).filter(
            (Product2.despesa_data.like(f'%{termo}%')) |
            (Product2.despesa_nome.like(f'%{termo}%')) |
            (Product2.despesa_qtde.like(f'%{termo}%')) |
            (Product2.despesa_valor.like(f'%{termo}%')))
        ).scalars()
        return render_template('listar_despesas.html', despesa=resultado)
    else:
        despesas = db.session.execute(db.select(Product2)).scalars()
        return render_template('listar_despesas.html', despesa=despesas)


@app.route("/cadastrar_despesas", methods=["GET", "POST"])
def cadastrar_despesas():
    if request.method == "POST":
        status = {"type": "sucesso", "message": "Despesa(s) cadastrada(s) com sucesso!"}
        try:
            dados = request.form
            despesa = Product2(
                despesa_data=dados["despesa_data"],
                despesa_nome=dados["despesa_nome"],
                despesa_qtde=dados["despesa_qtde"],
                despesa_valor=dados["despesa_valor"],
            )
            db.session.add(despesa)
            db.session.commit()
            return render_template("cadastrar_despesas.html", status=status)
        except:
            status = {"type": "erro", "message": f"Houve um problema ao cadastrar a despesa!"}
            return render_template("cadastrar_despesas.html", status=status)
    else:
        return render_template("cadastrar_despesas.html")
    
    
@app.route("/editar_despesas/<int:id_despesa>", methods=["GET", "POST"])
def editar_despesas(id_despesa):
    if request.method == "POST":
        dados_editados = request.form
        despesa = db.session.execute(db.select(Product2).filter(Product2.id_despesa == id_despesa)).scalar()

        despesa.despesa_data = dados_editados["despesa_data"]
        despesa.despesa_nome = dados_editados["despesa_nome"]
        despesa.despesa_qtde = dados_editados["despesa_qtde"]
        despesa.despesa_valor = dados_editados["despesa_valor"]

        db.session.commit()
        return redirect("/listar_despesas")
    
    else:
        despesa_editado = db.session.execute(db.select(Product2).filter(Product2.id_despesa == id_despesa)).scalar()
        return render_template('editar_despesas.html', despesa=despesa_editado)
    
@app.route("/deletar_despesa/<int:id_despesa>")
def deletar_despesa(id_despesa):
    despesa_deletado = db.session.execute(db.select(Product2).filter(Product2.id_despesa == id_despesa)).scalar()
    db.session.delete(despesa_deletado)
    db.session.commit()
    return redirect("/listar_despesas")


#Ferramenta para busca de entrega em uma data específica
@app.route("/search_e", methods=["GET", "POST"])
def search_e():
    if request.method == "POST":
        start_date = request.form["start_date"]
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        start_date = start_date - timedelta(days=1)
        end_date = start_date + timedelta(days=1)

        result = Product.query.filter(and_(Product.data_entrega >= start_date, Product.data_entrega < end_date)).all()
        total_value = db.session.query(func.sum(Product.valor)).filter(and_(Product.data_entrega >= start_date, Product.data_entrega < end_date)).scalar()

        # Converte total_value para Decimal
        total_value = Decimal(total_value or 0).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Converte os valores de valor dos pedidos para Decimal e arredonda
        for entrega in result:
            entrega.valor = Decimal(entrega.valor or 0).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Formata os valores com ponto para separar os milhares
        total_value_formatted = '{:,.2f}'.format(total_value)
        for entrega in result:
            entrega.valor_formatted = '{:,.2f}'.format(entrega.valor)

        return render_template('result_e.html', show_results=True, results=result, total_value=total_value_formatted,)
    else:
        return render_template('search_e.html', show_results=False)


#Ferramenta para busca de pedidos entre duas datas
@app.route("/search_p", methods=["GET", "POST"])
def search_p():
    if request.method == "POST":
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        start_date = start_date - timedelta(days=1)
        result = Product.query.filter(and_(Product.data_pedido >= start_date, Product.data_pedido <= end_date)).all()
        total_value = db.session.query(func.sum(Product.valor)).filter(and_(Product.data_pedido >= start_date, Product.data_pedido <= end_date)).scalar()

        # Converte total_value para Decimal
        total_value = Decimal(total_value or 0).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Converte os valores de despesa_valor dos registros para Decimal e arredonda
        for pedido in result:
            pedido.valor = Decimal(pedido.valor or 0).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Formata os valores com ponto para separar os milhares
        total_value_formatted = '{:,.2f}'.format(total_value)
        for pedido in result:
            pedido.valor_formatted = '{:,.2f}'.format(pedido.valor)

        return render_template('result_p.html', show_results=True, results=result, total_value=total_value_formatted)

    else:
        return render_template('search_p.html', show_results=False)

    

#Ferramenta para busca de despesas entre duas datas
@app.route("/search_d", methods=["GET", "POST"])
def search_d():
    if request.method == "POST":
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
    
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        start_date = start_date - timedelta(days=1)
        result = Product2.query.filter(and_(Product2.despesa_data >= start_date, Product2.despesa_data <= end_date)).all()
        total_value = db.session.query(func.sum(Product2.despesa_valor)).filter(and_(Product2.despesa_data >= start_date, Product2.despesa_data <= end_date)).scalar()

        # Converte total_value para Decimal
        total_value = Decimal(total_value or 0).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Converte os valores de despesa_valor dos registros para Decimal e arredonda
        for despesa in result:
            despesa.despesa_valor = Decimal(despesa.despesa_valor or 0).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Formata os valores com ponto para separar os milhares
        total_value_formatted = '{:,.2f}'.format(total_value)
        for despesa in result:
            despesa.despesa_valor_formatted = '{:,.2f}'.format(despesa.despesa_valor)

        return render_template('result_d.html', show_results=True, results=result, total_value=total_value_formatted)
        
    else:
        return render_template('search_d.html', show_results=False)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')


if __name__ == "__main__":
    with app.app_context():
        db.create_all() # Criação do BD caso o mesmo não exista
        app.run(debug=False)