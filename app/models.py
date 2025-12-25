from . import db

class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    preco_venda = db.Column(db.Float, nullable=False)
    custo_unitario = db.Column(db.Float, nullable=True)
    ativo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Produto {self.nome}>"
    
class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(100), nullable=False)
    whatsapp = db.Column(db.String(20), nullable=False)
    data_desejada = db.Column(db.String(10), nullable=False)
    data_pedido = db.Column(db.DateTime, nullable=False)
    observacoes = db.Column(db.Text, nullable=True)

    itens = db.relationship("ItemPedido", backref="pedido", lazy=True)

class ItemPedido(db.Model):
    __tablename__ = "itens_pedido"

    id = db.Column(db.Integer, primary_key=True)

    pedido_id = db.Column(
        db.Integer,
        db.ForeignKey("pedidos.id"),
        nullable=False
    )

    produto_id = db.Column(
        db.Integer,
        db.ForeignKey("produtos.id"),
        nullable=False
    )

    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)