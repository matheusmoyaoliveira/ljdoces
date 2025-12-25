import os
import sys
import csv
from datetime import datetime, date

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app
from app.models import Pedido, ItemPedido, Produto

app = create_app()

def limites_mes_anterior(ref=None):
    """Retorna (inicio, fim) do mês anterior.
    
    inicio = primeiro dia do mês anterior, 00:00
    fim    = primeiro dia do mês atual, 00:00 (limite superior)
    """
    if ref is None:
        ref = date.today()

    if ref.month == 1:
        ano = ref.year - 1
        mes = 12
    else:
        ano = ref.year
        mes = ref.month - 1

    inicio = datetime(ano, mes, 1)

    if mes == 12:
        fim = datetime(ano + 1, 1, 1)
    else:
        fim = datetime(ano, mes + 1, 1)
    
    return inicio, fim

def gerar_relatorio_mes_anterior():
    with app.app_context():
        inicio, fim = limites_mes_anterior()

        pedidos = (
            Pedido.query
            .filter(
                Pedido.data_pedido >= inicio,
                Pedido.data_pedido < fim,
            )
            .order_by(Pedido.data_pedido.asc())
            .all()
        )

        mes_ano = inicio.strftime("%m/%Y")

        if not pedidos:
            print(f"[RELATÓRIO] Nenhum pedido encontrado em {mes_ano}.")
            return
        
        pasta_relatorios = os.path.join(BASE_DIR, "relatorios")
        os.makedirs(pasta_relatorios, exist_ok=True)

        nome_arquivo = f"pedidos_{inicio.year}-{inicio.month:02d}.csv"
        caminho_arquivo = os.path.join(pasta_relatorios, nome_arquivo)

        total_pedidos = 0
        total_itens = 0
        total_faturado = 0.0

        with open(caminho_arquivo, "w", newline="", enconding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")

            writer.writerow(
                [
                    "ID pedido",
                    "Data do pedido",
                    "Data desejada",
                    "Cliente",
                    "WhatsApp",
                    "Produto",
                    "Quantidade",
                    "Preço unitário (R$)",
                    "Valor total do item (R$)",
                    "Observações do pedido",
                ]
            )

            for pedido in pedidos:
                itens = ItemPedido.query.filter_by(pedido_id=pedido.id).all()
                total_pedidos += 1

                if not itens:
                    writer.writerow(
                        [
                            pedido.id,
                            pedido.data_pedido.strftime("%d/%m/%Y %H:%M"),
                            pedido.data_desejada.strftime("%d/%m/%Y")
                            if pedido.data_desejada
                            else "",
                            pedido.nome_cliente,
                            pedido.whatsapp,
                            "",
                            "",
                            "",
                            "",
                            pedido.observacoes or "",
                        ]
                    )
                    continue
            
                for item in itens:
                    produto = Produto.query.get(item.produto_id)

                    qtd = item.quantidade or 0
                    preco = float(item.preco_unitario or 0)
                    valor_item = qtd * preco

                    total_itens += qtd
                    total_faturado += valor_item

                    writer.writerow(
                        [
                            pedido.id,
                            pedido.data_pedido.strftime("%d/%m/%Y %H:%M"),
                            pedido.data_desejada.strftime("%d/%m/%Y")
                            if pedido.data_desejada
                            else "",
                            pedido.nome_cliente,
                            pedido.whatsapp,
                            "",
                            "",
                            "",
                            "",
                            pedido.observacoes or "",
                        ]
                    )
            
            writer.writerow([])
            writer.writerow(["TOTAL DE PEDIDOS", total_pedidos])
            writer.writerow(["TOTAL DE ITENS", total_itens])
            writer.writerow(["TOTAL FATURADO (R$)", f"{total_faturado:.2f}"])

        print(f"[RELATÓRIO] Gerado com sucesso: {caminho_arquivo}")

if __name__ == "__main__":
    gerar_relatorio_mes_anterior()