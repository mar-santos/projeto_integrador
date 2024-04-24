from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy import func
from sqlalchemy import update
from sqlalchemy import desc
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from datetime import datetime
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'b175855202d537a1b07a1cbbee8ffc197e2af9c5289a6adfd4b4aa63c3f77861'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:admin@localhost:3306/tapete"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Inicializar Classe e criar as tabelas pedido e despesas
class Product(db.Model):
    __tablename__ = "pedido"
    id_pedido = db.Column(db.Integer, primary_key=True)
    data_pedido = db.Column(db.String(30))
    data_retirada = db.Column(db.String(30))
    data_entrega = db.Column(db.String(30))
    id_ficha = db.Column(db. String(30))
    nome = db.Column(db.String(200), nullable=False)
    endereco = db.Column(db.String(250))
    cidade = db.Column(db.String(50))
    telefone = db.Column(db.String(100), nullable=False)
    servico = db.Column(db.String(100))
    desconto = db.Column(db.String(30))
    valor = db.Column(db.String(30))
    status = db.Column(db.String(30))
    deletar = db.Column(db.String(5))

def __init__(self,
             data_pedido: str,
             data_retirada: str,
             data_entrega: str,
             id_ficha: str, 
             nome: str, 
             endereco: str,
             cidade: str,
             telefone: str, 
             servico: str,
             desconto: str, 
             valor: str,
             status: str,
             deletar: str) -> None:
    
    self.data_pedido = data_pedido
    self.data_retirada = data_retirada
    self.data_entrega = data_entrega
    self.id_ficha = id_ficha
    self.nome = nome
    self.endereco = endereco
    self.cidade = cidade
    self.telefone = telefone
    self.servico = servico
    self.desconto = desconto
    self.valor = valor
    self.status = status
    self.deletar = deletar

class Product2(db.Model):
    __tablename__ = "despesa"
    id_despesa = db.Column(db.Integer, primary_key=True)
    despesa_data = db.Column(db.String(30))
    despesa_nome = db.Column(db.String(100))
    despesa_qtde = db.Column(db.String(100))
    despesa_valor = db.Column(db.String(100))
    despesa_deletar = db.Column(db.String(5))

def __init__(self,
             despesa_data: str, 
             despesa_nome: str, 
             despesa_qtde: str,
             despesa_valor: str,
             despesa_deletar: str) -> None:
    
    self.despesa_data = despesa_data
    self.despesa_nome = despesa_nome
    self.despesa_qtde = despesa_qtde
    self.despesa_valor = despesa_valor
    self.despesa.deletar = despesa_deletar


class Product3(db.Model):
    __tablename__ = "preco"
    id_preco = db.Column(db.Float, primary_key=True)
    data = db.Column(db.String(30))
    valor_metro = db.Column(db.Float)

def __init__(self,
                data: str,
                valor_metro: float) -> None:
    
    self.data = data
    self.valor_metro = valor_metro
    


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
    "renata": "17gatos",
    "mario": "17gatos"
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
    endpoints_protegidos = ["/calculadora",
                            "/cadastrar_pedido", 
                            "/listar_pedidos", 
                            "/cadastrar_despesas", 
                            "/listar_despesas",
                            "/search_e",
                            "/search_p",
                            "/search_r",
                            "/search_d",
                            "/tabela_precos",]
    if request.path in endpoints_protegidos:
        if not session.get('logged_in'):
            return redirect("/erro_pagina_403")


# Definição das rotas dinâmicas. CRUD de pedidos
@app.route("/cadastrar_pedido", methods=["GET", "POST"])
def cadastrar_pedido():
    if request.method == "POST":
        status = {"type": "sucesso", "message": "Pedido cadastrado com sucesso!"}
        try:
            dados = request.form
            pedido = Product(
                data_pedido=dados["data_pedido"],
                data_retirada=dados["data_retirada"],
                data_entrega=dados["data_entrega"],
                id_ficha=dados["id_ficha"],
                nome=dados["nome"],
                endereco=dados["endereco"],
                cidade=dados["cidade"],
                telefone=dados["telefone"],
                servico=dados["servico"],
                desconto=dados["desconto"],
                valor=(dados["valor"]),
                status=(dados["status"]),
                deletar=(dados["deletar"])
            )
            db.session.add(pedido)
            db.session.commit()
            return render_template("cadastrar_pedido.html", status=status)
        except:
            status = {"type": "erro", "message": f"Houve um problema ao cadastrar o pedido {dados['nome']}!"}
            return render_template("cadastrar_pedido.html", status=status)
    else:
        return render_template("cadastrar_pedido.html")
    
@app.route("/calculadora", methods=['GET', 'POST'])
def calculadora():
    if request.method == "POST":
        valor_final = 0.00

        quadrado = request.form['formato_tapete']

        if (quadrado == 'True'):
            largura_tapete = float(request.form['largura_tapete'])
            altura_tapete = float(request.form['altura_tapete'])
            preco_metro = Product3.query.order_by(Product3.id_preco.desc()).first().valor_metro  # Consulta o valor do metro na tabela Product3 preco
            valor_tapete = (largura_tapete * altura_tapete) * preco_metro
            valor_final += valor_tapete
        else:
            largura_tapete = float(request.form['largura_tapete'])
            altura_tapete = float(request.form['altura_tapete'])
            preco_metro = Product3.query.order_by(Product3.id_preco.desc()).first().valor_metro   # Consulta o valor do metro na tabela Product3 preco
            valor_tapete = (3.14 * ((largura_tapete/2) * (largura_tapete/2))) * preco_metro
            valor_final += valor_tapete

        return render_template("calculadora.html", valor_final = round(valor_final,2))
    else:
        return render_template("calculadora.html")


@app.route("/listar_pedidos", methods=['GET', 'POST'])
def listar_pedidos():
    if request.method == "POST":
        termo = request.form["pesquisa"]
        resultado = db.session.execute(
            db.select(Product)
            .filter(
                ((Product.data_pedido.like(f'%{termo}%')) |
                 (Product.data_retirada.like(f'%{termo}%')) |
                 (Product.data_entrega.like(f'%{termo}%')) |
                 (Product.id_ficha.like(f'%{termo}%')) |
                 (Product.nome.like(f'%{termo}%')) |
                 (Product.endereco.like(f'%{termo}%')) |
                 (Product.cidade.like(f'%{termo}%')) |
                 (Product.telefone.like(f'%{termo}%')) |
                 (Product.servico.like(f'%{termo}%')) |
                 (Product.desconto.like(f'%{termo}%')) |
                 (Product.valor.like(f'%{termo}%')) |
                 (Product.status.like(f'%{termo}%'))) &
                (Product.deletar != "0")
            )
            .order_by(desc(Product.data_pedido))  # Ordena por data_pedido do mais recente para o mais antigo
        ).scalars()
        return render_template('pedidos.html', pedidos=resultado)
    else:
        pedidos = db.session.execute(
            db.select(Product)
            .filter(Product.deletar == "1")
            .order_by(desc(Product.data_pedido))  # Ordena por data_pedido do mais recente para o mais antigo
        ).scalars()
        return render_template('pedidos.html', pedidos=pedidos)


@app.route("/editar_pedido/<int:id_pedido>", methods=["GET", "POST"])
def editar_pedido(id_pedido):
    if request.method == "POST":
        dados_editados = request.form
        pedido = db.session.execute(db.select(Product).filter(Product.id_pedido == id_pedido)).scalar()

        pedido.data_pedido = dados_editados["data_pedido"]
        pedido.data_retirada = dados_editados["data_retirada"]
        pedido.data_entrega = dados_editados["data_entrega"]
        pedido.id_ficha = dados_editados["id_ficha"]
        pedido.nome = dados_editados["nome"]
        pedido.endereco = dados_editados["endereco"]
        pedido.cidade = dados_editados["cidade"]
        pedido.telefone = dados_editados["telefone"]
        pedido.servico = dados_editados["servico"]
        pedido.desconto = dados_editados["desconto"]
        pedido.valor = dados_editados["valor"]
        pedido.status = dados_editados["status"]

        db.session.commit()
        return redirect("/listar_pedidos")
    
    else:
        pedido_editado = db.session.execute(db.select(Product).filter(Product.id_pedido == id_pedido)).scalar()
        return render_template('editar_pedido.html', pedido=pedido_editado)


@app.route("/deletar_pedido/<int:id_pedido>")
def deletar_pedido(id_pedido):
    pedido = Product.query.get(id_pedido)
    if pedido:
        pedido.deletar = "0"
        db.session.commit()
    return redirect("/listar_pedidos")
    

# Definição das rotas dinâmicas. CRUD de despesas
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
                despesa_deletar=dados["despesa_deletar"]
            )
            db.session.add(despesa)
            db.session.commit()
            return render_template("cadastrar_despesas.html", status=status)
        except:
            status = {"type": "erro", "message": f"Houve um problema ao cadastrar a despesa!"}
            return render_template("cadastrar_despesas.html", status=status)
    else:
        return render_template("cadastrar_despesas.html")


@app.route("/listar_despesas", methods=['GET', 'POST'])
def listar_despesas():
    if request.method == "POST":
        termo = request.form["pesquisa"]
        resultado = db.session.execute(db.select(Product2).filter(
            ((Product2.despesa_data.like(f'%{termo}%')) |
            (Product2.despesa_nome.like(f'%{termo}%')) |
            (Product2.despesa_qtde.like(f'%{termo}%')) |
            (Product2.despesa_valor.like(f'%{termo}%'))) &
            (Product2.despesa_deletar != "0")
            )
            .order_by(desc(Product2.despesa_data))
        ).scalars()
        return render_template('listar_despesas.html', despesa=resultado)
    else:
        despesas = db.session.execute(db.select(Product2)
        .filter(Product2.despesa_deletar == "1")
        .order_by(desc(Product2.despesa_data))
        ).scalars()
        return render_template('listar_despesas.html', despesa=despesas)
    
    
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
    despesa = Product2.query.get(id_despesa)
    if despesa:
        despesa.despesa_deletar = "0"
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

        result = Product.query.filter(
            and_(Product.data_entrega >= start_date, 
                 Product.data_entrega < end_date,
                 Product.deletar != "0"
            )
        ).all()
        total_value = db.session.query(func.sum(Product.valor)).filter(
            and_(Product.data_entrega >= start_date,
                 Product.data_entrega < end_date,
                 Product.deletar != "0"
            )
        ).scalar()

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


#Ferramenta para busca de retiradas em uma data específica
@app.route("/search_r", methods=["GET", "POST"])
def search_r():
    if request.method == "POST":
        start_date = request.form["start_date"]
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        start_date = start_date - timedelta(days=1)
        end_date = start_date + timedelta(days=1)

        result = Product.query.filter(
            and_(
                Product.data_retirada >= start_date,
                Product.data_retirada < end_date,
                Product.deletar != "0"
            )
        ).all()
        total_value = db.session.query(func.sum(Product.valor)).filter(
            and_(
                Product.data_retirada >= start_date,
                Product.data_retirada < end_date,
                Product.deletar != "0"
            )
        ).scalar()

        # Converte total_value para Decimal
        total_value = Decimal(total_value or 0).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Converte os valores de valor dos pedidos para Decimal e arredonda
        for entrega in result:
            entrega.valor = Decimal(entrega.valor or 0).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Formata os valores com ponto para separar os milhares
        total_value_formatted = '{:,.2f}'.format(total_value)
        for entrega in result:
            entrega.valor_formatted = '{:,.2f}'.format(entrega.valor)

        return render_template('result_r.html', show_results=True, results=result, total_value=total_value_formatted,)
    else:
        return render_template('search_r.html', show_results=False)


#Ferramenta para busca de pedidos entre duas datas
@app.route("/search_p", methods=["GET", "POST"])
def search_p():
    if request.method == "POST":
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        start_date = start_date - timedelta(days=1)
        result = Product.query.filter(
            and_(Product.data_pedido >= start_date, 
                 Product.data_pedido <= end_date,
                 Product.deletar != "0"
            )
        ).order_by(desc(Product.data_pedido)).all()

        # Soma dos descontos
        total_desconto = sum([Decimal(pedido.desconto or 0).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) for pedido in result])

        # Converte total_desconto para string formatada
        total_desconto_formatted = '{:,.2f}'.format(total_desconto)

        # Total do valor dos produtos
        total_value = db.session.query(func.sum(Product.valor)).filter(
            and_(
                Product.data_pedido >= start_date, 
                Product.data_pedido <= end_date,
                Product.deletar != "0"
            )
        ).scalar()

        # Converte total_value para Decimal
        total_value = Decimal(total_value or 0).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Converte os valores de despesa_valor dos registros para Decimal e arredonda
        for pedido in result:
            pedido.valor = Decimal(pedido.valor or 0).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Formata os valores com ponto para separar os milhares
        total_value_formatted = '{:,.2f}'.format(total_value)
        for pedido in result:
            pedido.valor_formatted = '{:,.2f}'.format(pedido.valor)

        return render_template('result_p.html', show_results=True, results=result, total_value=total_value_formatted, total_desconto=total_desconto_formatted)

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
        result = Product2.query.filter(
            and_(
            Product2.despesa_data >= start_date, 
            Product2.despesa_data <= end_date, 
            Product2.despesa_deletar != "0"
            )
        ).order_by(desc(Product2.despesa_data)).all()
        total_value = db.session.query(func.sum(Product2.despesa_valor)).filter(
            and_(
                Product2.despesa_data >= start_date,
                  Product2.despesa_data <= end_date,
                  Product2.despesa_deletar != "0"
            )
        ).scalar()

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
    
@app.route("/tabela_precos", methods=['GET', 'POST'])
def tabela_precos():
    if request.method == "POST":
        status = {"type": "sucesso", "message": "Novo valor por metro quadrado cadastrado com sucesso!"}
        try:
            dados = request.form
            pedido = Product3(
                data=dados["data"],
                valor_metro=dados["valor_metro"],
            )
            db.session.add(pedido)
            db.session.commit()
            status["valor_metro"] = Product3.query.order_by(Product3.id_preco.desc()).first().valor_metro  # Consulta o valor_metro mais recente
            return render_template("tabela_precos.html", status=status)
        except:
            status = {"type": "erro", "message": f"Houve um problema ao cadastrar o novo valor!"}
            return render_template("tabela_precos.html", status=status)
    else:
        return render_template("tabela_precos.html")

















@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')


if __name__ == "__main__":
    with app.app_context():
        #db.create_all() # Criação do BD caso o mesmo não exista
        app.run(debug=True)