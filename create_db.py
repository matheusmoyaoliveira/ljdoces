from app import create_app, db
from app.models import Produto, Pedido, ItemPedido

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    produtos = [
        Produto(nome="Brigadeiro tradicional", categoria="Brigadeiros", preco_venda=2.50, custo_unitario=0.80),
        Produto(nome="Brigadeiro de ninho", categoria="Brigadeiros", preco_venda=3.00, custo_unitario=1.00),
        Produto(nome="Bolo de pote de chocolate", categoria="Bolos no pote", preco_venda=10.00, custo_unitario=4.00),
    ]

    db.session.add_all(produtos)
    db.session.commit()

    print("Banco criado e populado com produtos de teste.")