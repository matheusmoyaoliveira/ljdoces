from flask import render_template, request, redirect, url_for, flash, current_app
from datetime import datetime, date
from urllib.parse import quote_plus
from .models import Produto, Pedido, ItemPedido
from . import db

NUMERO_WHATSAPP_LJ = "5511962819619"

def init_app(app):
    @app.route("/")
    def home():
        produtos = Produto.query.filter_by(ativo=True).all()
        return render_template("home.html", produtos=produtos)
    
    @app.route("/cardapio")
    def cardapio():
        produtos = Produto.query.order_by(Produto.categoria, Produto.nome).all()
        return render_template("cardapio.html", produtos=produtos)
    
    @app.route("/pedido/novo", methods=["GET", "POST"])
    def novo_pedido():
        produtos = Produto.query.filter_by(ativo=True).all()

        if request.method == "POST":
            nome_cliente = request.form.get("nome_cliente")
            whatsapp = request.form.get("whatsapp")
            data_desejada = request.form.get("data_desejada")
            observacoes = request.form.get("observacoes")
            produto_id = request.form.get("produto_id")
            quantidade = request.form.get("quantidade")

            if not produto_id or not quantidade:
                flash("Escolha um produto e informe a quantidade.", "warning")
                return render_template("novo_pedido.html", produtos=produtos)
            
            produto = Produto.query.get(int(produto_id))

            if not produto:
                flash("Produto inválido.", "danger")
                return render_template("novo_pedido.html", produtos=produtos)
            
            pedido = Pedido(
                nome_cliente=nome_cliente,
                whatsapp=whatsapp,
                data_desejada=data_desejada,
                data_pedido=datetime.now(),
                observacoes=observacoes

            )

            item = ItemPedido(
                pedido=pedido,
                produto_id=produto_id,
                quantidade=int(quantidade),
                preco_unitario=produto.preco_venda
            )

            db.session.add(pedido)
            db.session.add(item)
            db.session.commit()

            texto = (
                f"Olá, aqui é {nome_cliente}!\n\n"
                f"Quero fazer um pedido na LJ Doces:\n"
                f"- Produto: {produto.nome}\n"
                f"- Quantidade: {quantidade}\n"
                f"- Data desejada: {data_desejada}\n"
                f"- WhatsApp para contato: {whatsapp}\n"
            )

            if observacoes:
                texto += f"- Observações: {observacoes}\n"

            texto += "\nSe puder me confirmar a disponibilidade, eu agradeço! 😊"

            texto_codificado = quote_plus(texto)
            link_whatsapp = f"https://wa.me/{NUMERO_WHATSAPP_LJ}?text={texto_codificado}"

            return redirect(
                url_for(
                    "confirmacao_pedido",
                    pedido_id=pedido.id,
                    wpp=link_whatsapp
                )
            )
        
        return render_template("novo_pedido.html", produtos=produtos)
    
    @app.route("/pedido/confirmacao/<int:pedido_id>")
    def confirmacao_pedido(pedido_id):

        pedido = Pedido.query.get_or_404(pedido_id)

        item = ItemPedido.query.filter_by(pedido_id=pedido.id).first()
        produto = Produto.query.get(item.produto_id)

        texto = montar_texto_pedido(pedido, item, produto)
        texto_encoded = quote_plus(texto)

        telefone = app.config["WHATSAPP_LJ"]
        link_whatsapp = (
            f"https://api.whatsapp.com/send?"
            f"phone=55{telefone}&text={texto_encoded}"
        )

        data_desejada_br = None
        if pedido.data_desejada:
            try:
                data_str = str(pedido.data_desejada)
                data_obj = datetime.strptime(data_str, "%Y-%m-%d")
                data_desejada_br = data_obj.strftime("%d/%m/%Y")
            except ValueError:
                data_desejada_br = str(pedido.data_desejada)

        print("LINK WHATSAPP GERADO:", link_whatsapp)

        return render_template(
            "confirmacao_pedido.html",
            pedido=pedido,
            produto=produto,
            item=item,
            link_whatsapp=link_whatsapp,
            data_desejada_br=data_desejada_br,  
        )
    
def montar_texto_pedido(pedido, item, produto) -> str:
    """Monta o texto de resumo de pedido usado no WhatsApp / notificações."""

    data_br = ""
    if pedido.data_desejada:
        # se já for date/datetime
        if isinstance(pedido.data_desejada, (date, datetime)):
            data_br = pedido.data_desejada.strftime("%d-%m-%Y")
        else:
            # garante que é string e tenta parsear no formato que vem do form/SQLite
            try:
                data_iso = str(pedido.data_desejada)
                dt = datetime.strptime(data_iso, "%Y-%m-%d")
                data_br = dt.strftime("%d-%m-%Y")
            except ValueError:
                # se nada disso der certo, manda do jeito que vier mesmo
                data_br = str(pedido.data_desejada)
    else:
        data_br = "-"

    texto = (
        f"Novo pedido - LJ Doces\n"
        f"Cliente: {pedido.nome_cliente}\n"
        f"WhatsApp do cliente: {pedido.whatsapp}\n"
        f"Data desejada: {data_br}\n"
        f"Produto: {produto.nome}\n"
        f"Quantidade: {item.quantidade}\n"
    )

    if pedido.observacoes:
        texto += f"Observações: {pedido.observacoes}\n"

    return texto