# LJ Doces – site de encomendas

Aplicação web simples, feita em **Flask**, para centralizar os pedidos da *LJ Doces* (doceria artesanal).  
O foco é facilitar o contato pelo WhatsApp e organizar os pedidos em um banco de dados, com geração de relatórios mensais em CSV.

## ✨ Funcionalidades

- **Home institucional**
  - Destaque da marca e slogan.
  - Seções explicando sobre a LJ Doces e os diferenciais.
  - Botões de atalho para:
    - Ver cardápio completo
    - Fazer pedido
    - Acessar a loja no iFood

- **Página de cardápio (`/cardapio`)**
  - Cardápios em imagem (docinhos, sobremesas, bolos no pote).
  - Bloco especial de **Empadas & salgados**, com texto explicativo.
  - CTA final com botões para ir direto ao formulário de pedido ou voltar à página inicial.

- **Formulário de pedido (`/pedido/novo`)**
  - Campos:
    - Nome do cliente
    - WhatsApp
    - Data desejada
    - Produto (lista vinda do banco de dados)
    - Quantidade
    - Observações
  - Os dados são gravados em um banco **SQLite** usando **SQLAlchemy**.

- **Resumo + envio via WhatsApp (`/pedido/confirmacao/<id>`)**
  - Mostra o resumo do pedido em um cartão:
    - Cliente, WhatsApp, data desejada, produto, quantidade, observações.
  - Botão **“Enviar no WhatsApp”**:
    - Gera um texto formatado (data no padrão `dd/mm/aaaa`).
    - Abre o link `https://wa.me/55NUMERO?text=...` com o resumo pronto para envio para a LJ Doces.

- **Automação de relatório mensal**
  - Script em `scripts/gerar_relatorio.py`.
  - Lê os pedidos do **mês anterior** na tabela de pedidos.
  - Gera um arquivo CSV em `relatorios/pedidos_YYYY-MM.csv` com:
    - ID do pedido
    - Data do pedido
    - Data desejada
    - Nome do cliente
    - WhatsApp
    - Produto
    - Quantidade
    - Preço unitário
    - Valor total (quantidade × preço)
  - Pensado para ser chamado automaticamente pelo **Agendador de Tarefas do Windows** todo dia 1.

---

## 🛠 Tecnologias usadas

- Python 3.x
- Flask
- Flask SQLAlchemy
- SQLite
- HTML + CSS (Bootstrap como base + CSS customizado)
- Jinja2 (templates)

---

## 📁 Estrutura simplificada de pastas

```text
ljdoces/
├── app/
│   ├── __init__.py          # factory do Flask + config do banco e WhatsApp
│   ├── models.py            # modelos: Produto, Pedido, ItemPedido
│   ├── routes.py            # rotas principais da aplicação
│   ├── forms.py             # (opcional) formulários/validações
│   ├── static/
│   │   ├── css/
│   │   │   ├── base.css     # estilos base (cores, navbar, footer, etc.)
│   │   │   ├── home.css     # estilos específicos da home
│   │   │   ├── cardapio.css # estilos da página de cardápio
│   │   │   └── pedido.css   # estilos do formulário e da confirmação
│   │   └── img/             # logo, cardápios, fotos de produtos
│   └── templates/
│       ├── base.html        # layout base com navbar e footer
│       ├── home.html        # página inicial
│       ├── cardapio.html    # cardápio
│       ├── novo_pedido.html # formulário de pedido
│       └── confirmacao_pedido.html  # resumo e botão do WhatsApp
├── instance/
│   └── ljdoces.db           # banco SQLite (gerado em tempo de execução)
├── scripts/
│   └── gerar_relatorio.py   # script de relatório mensal (CSV)
├── create_db.py             # script auxiliar para criar/popular o banco
├── config.py                # configurações adicionais (se usado)
├── requirements.txt
├── run.py                   # ponto de entrada da aplicação Flask
└── README.md
```

> Observação: alguns arquivos podem mudar de nome conforme a evolução do projeto, mas a ideia geral é essa.

---

## 🚀 Como rodar o projeto localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU-USUARIO/ljdoces.git
cd ljdoces
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Criar o banco de dados

O projeto usa SQLite. O fluxo sugerido é:

```bash
python create_db.py
```

Esse script deve:

- criar o arquivo `instance/ljdoces.db` (se ainda não existir);
- criar as tabelas;
- (opcional) popular alguns produtos iniciais.

### 5. Configurar o número do WhatsApp

No arquivo `app/__init__.py`, existe uma configuração semelhante a:

```python
app.config["WHATSAPP_LJ"] = "11962819619"  # exemplo
```

Troque para o número oficial da doceria, sempre no formato **DDD + número**, apenas dígitos (sem `+55`, sem espaços, sem traços).  
O `+55` é adicionado automaticamente na hora de montar o link.

> Em uma versão futura, isso pode ir para um arquivo `.env`, mas no momento fica direto na config do Flask.

### 6. Rodar o servidor

```bash
python run.py
```

Abra no navegador:

```text
http://127.0.0.1:5000
```

---

## 📊 Como gerar o relatório mensal (manual)

Se quiser gerar o relatório na mão (sem agendador):

```bash
python scripts/gerar_relatorio.py
```

O script:

- calcula automaticamente o **mês anterior** (ex.: se hoje é 2025-12, gera para 2025-11);
- busca os pedidos desse período;
- cria a pasta `relatorios/` (se não existir);
- gera um arquivo `relatorios/pedidos_YYYY-MM.csv`.

Se não houver pedidos no mês anterior, ele apenas informa isso no console.

---

## 🕒 Automatizando no Agendador de Tarefas (Windows)

Passo geral (resumido):

1. Abrir **Agendador de Tarefas**.
2. Criar uma **Nova Tarefa Básica** chamada, por exemplo, `Relatório mensal LJ Doces`.
3. Definir o gatilho como **Mensal**, dia `1` de todos os meses, no horário desejado.
4. Ação: **Iniciar um programa**.
5. Programa/script:

   ```text
   C:\Users\SEU-USUARIO\caminho\ljdoces\venv\Scripts\python.exe
   ```

6. Argumentos:

   ```text
   C:\Users\SEU-USUARIO\caminho\ljdoces\scripts\gerar_relatorio.py
   ```

7. Pasta de início (opcional, mas recomendado):

   ```text
   C:\Users\SEU-USUARIO\caminho\ljdoces
   ```

Assim, todo dia 1 o Windows executa o script e gera automaticamente o CSV do mês anterior.

---

## 🔮 Possíveis melhorias futuras

- Painel administrativo simples para listar pedidos e filtrar por data.
- Cadastro e edição de produtos via interface web (CRUD completo).
- Enviar o relatório automaticamente por e-mail ou WhatsApp.
- Migrar de SQLite para um banco em nuvem (PostgreSQL, por exemplo).
- Implementar login para a dona da doceria acessar os pedidos.

---

## 📄 Licença

Defina aqui a licença que preferir (MIT, GPL, etc.), ou deixe explícito que o projeto é de uso interno da LJ Doces.
