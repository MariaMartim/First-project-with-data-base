from database import db_config as db

import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.orm.exc import NoResultFound
from datetime import date

connection = db.connection

engine = create_engine(db.database_url)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

def testar_conexao():
    try:
        # Verificando se a conexão foi bem-sucedida
        if db.connection.is_connected():
            print("Conexão bem-sucedida com o banco de dados!")
            db_info = db.connection.get_server_info()
            print("Versão do servidor MySQL:", db_info)
            return True  # Retorna True para indicar que a conexão foi bem-sucedida

    except Error as err:
        print("Erro ao conectar ao banco de dados:", err)
        return False  # Retorna False caso haja erro na conexão

    finally:
        if db.connection.is_connected():
            db.connection.close()  # Fecha a conexão
            print("Conexão com o MySQL encerrada.")
            

#Modelos
class Cliente(Base):
    __tablename__ = 'Cliente'
    
    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(80), nullable=False)
    telefone = Column(String(11), nullable=False)
    endereco = Column(String(200), nullable=False)
    
class Venda(Base):
    __tablename__ = 'Venda'
    
    id_venda = Column(Integer, primary_key=True, autoincrement=True)
    data_venda = Column(Date, nullable=False)
    valor_total = Column(Float, nullable=False)
    id_cliente = Column(Integer, ForeignKey('Cliente.id_cliente'))

    cliente = relationship('Cliente')

class Categoria(Base):
    __tablename__ = 'Categoria'
    
    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(100), nullable=False)
    
class Produto(Base):
    __tablename__ = 'Produto'
    
    id_produto = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    id_categoria = Column(Integer, ForeignKey('Categoria.id_categoria'))
    estoque_quantidade = Column(Integer, nullable=False)
    
    categoria = relationship('Categoria')

class ItemVenda(Base):
    __tablename__ = 'ItemVenda'
    
    id_item = Column(Integer, primary_key=True, autoincrement=True)
    id_venda = Column(Integer, ForeignKey('Venda.id_venda'))
    id_produto = Column(Integer, ForeignKey('Produto.id_produto'))
    quantidade = Column(Integer, nullable=False)
    preco_un = Column(Float, nullable=False)
    
    venda = relationship('Venda')
    produto = relationship('Produto')

    
#creating tables
Base.metadata.create_all(engine)

#funções para realizar as operações de CRUD
def buscar_cliente():
    escolha = int(input("Você deseja informar o ID ou o nome do cliente?: \n1) ID \n2)Nome \n"))

    while True:
        if escolha == 1:
            # Solicitar o ID do cliente
            id_cliente = int(input("Digite o ID do cliente: "))
            
            #busca se o cliente existe
            try:
                cliente = session.query(Cliente).filter(Cliente.id_cliente == id_cliente).one()
                return id_cliente
            except NoResultFound:
                print("Cliente não encontrado!")
                return None
    
        elif escolha == 2:
            # Solicitar o nome do cliente
            nome_cliente = input("Digite o nome do cliente: ").strip()

            try:
                # Buscar o cliente pelo nome (retorna o primeiro cliente encontrado)
                cliente = session.query(Cliente).filter(Cliente.nome == nome_cliente).one()
                return cliente.id_cliente  # Retorna o ID do cliente encontrado
            except NoResultFound:
                print("Cliente não encontrado!")
                return None
        else:
            print("Opção inválida!")
        
def buscar_produto():
    escolha = int(input("Você deseja informar o ID ou o nome do produto?: \n1) ID \n2)Nome \n"))

    while True:
        if escolha == 1:
            # Solicitar o ID do produto
            id_produto = int(input("Digite o ID do produto: "))
            
            #busca se o produto existe
            try:
                produto = session.query(Produto).filter(Produto.id_produto == id_produto).one()
                return id_produto
            except NoResultFound:
                print("Produto não encontrado!")
                return None
    
        elif escolha == 2:
            # Solicitar o nome do produto
            nome_produto = input("Digite o nome do produto: ").strip()

            try:
                # Buscar o produto pelo nome (retorna o primeiro produto encontrado)
                produto = session.query(Produto).filter(Produto.nome == nome_produto).one()
                return produto.id_produto  # Retorna o ID do produto encontrado
            except NoResultFound:
                print("Produto não encontrado!")
                return None
        else:
            print("Opção inválida!")
            
def buscar_produto_por_id(id_produto):
    try:
        # Buscar o produto pelo ID
        produto = session.query(Produto).filter(Produto.id_produto == id_produto).one()
        return produto  # Retorna o produto encontrado
    except NoResultFound:
        print("Produto não encontrado!")
        return None
    
def buscar_categoria_por_id(id_categoria):
    try:
        # Buscar a categoria pelo ID
        categoria = session.query(Categoria).filter(Categoria.id_categoria == id_categoria).one()
        return categoria  # Retorna a categoria encontrada
    except NoResultFound:
        print("Categoria não encontrada!")
        return None
    
def buscar_categoria():
    escolha = input("Você deseja informar o ID ou o nome da categoria?: \n1) ID \n2)Nome ")

    while True:
        if escolha == 1:
            # Solicitar o ID da categoria
            id_categoria = int(input("Digite o ID da categoria: "))
            
            #busca se a categoria existe
            try:
                categoria = session.query(Categoria).filter(Categoria.id_categoria == id_categoria).one()
                return id_categoria
            except NoResultFound:
                print("Categoria não encontrada!")
                return None
    
        elif escolha == 2:
            # Solicitar o nome da categoria
            nome_categoria = input("Digite o nome da categoria: ").strip()

            try:
                # Buscar a categoria pelo nome (retorna a primeira categoria encontrada)
                categoria = session.query(Categoria).filter(Categoria.nome == nome_categoria).one()
                return categoria.id  # Retorna o ID da categoria encontrada
            except NoResultFound:
                print("Categoria não encontrada!")
                return None
        else:
            print("Opção inválida!")
            
def buscar_venda():
    # Solicitar o ID da venda
    id_venda = int(input("Digite o ID da venda: "))
    
    #busca se a venda existe
    try:
        venda = session.query(Venda).filter(Venda.id_venda == id_venda).one()
        return id_venda
    except NoResultFound:
        print("Venda não encontrada!")
        return None

#CRUD operations

#CREATE

def criar_cliente():
    
    nome = input("Digite o nome do cliente: ")
    email = input("Digite o email do cliente: ")
    telefone = input("Digite o telefone do cliente: ")
    endereco = input("Digite o endereço do cliente: ")
     
    #pedir id da categoria e verificar se a categoria existe
    categorias = session.query(Categoria).all()
    for categoria in categorias:
        print(f"{categoria.id_categoria}, {categoria.nome}")
    
    while True:
        id_categoria = int(input("Digite o ID da categoria do cliente: "))
        if session.query(Categoria).filter(Categoria.id_categoria == id_categoria).first() is None:
            print('Categoria não encontrada!')
        else:
            break
    
    cliente = Cliente(nome=nome, email=email, telefone=telefone, endereco=endereco, id_categoria=id_categoria)
    session.add(cliente)
    session.commit()
    print('Cliente criado com sucesso!')
    
def criar_produto():
    
    nome = input("Digite o nome do produto: ")
    descricao = input("Digite a descrição do produto: ")
    preco = input("Digite o preço do produto: ")
    estoque_quantidade = input("Digite a quantidade em estoque: ")
    
    #mostrar as categorias disponíveis
    categorias = session.query(Categoria).all()
    for categoria in categorias:
        print(f"{categoria.id_categoria}, {categoria.nome}")
        
    #laço para verificar se a categoria existe
    while True:
        try:
            categoria = session.query(Categoria).filter(Categoria.id_categoria == input_categoria).one()
            break
        except NoResultFound:
            print("Categoria não encontrada!")
            input_categoria = int(input("Digite o ID da categoria do produto: "))
    
    
    #laço para procurar se o produto já existe por nome e pedir novamente se já existir
    while True:
        try:
            produto = session.query(Produto).filter(Produto.nome == nome).one()
            print("Produto já existe!")
            nome = input("Digite o nome do produto: ")
        except NoResultFound:
            break
    
    #criar o produto
    produto = Produto(nome=nome, descricao=descricao, preco=preco, estoque_quantidade=estoque_quantidade, id_categoria=input_categoria)
    session.add(produto)
    session.commit()
    print('Produto criado com sucesso!')
    
def criar_item_venda(id_venda, id_produto, quantidade, preco_unitario):
    
    item_venda = ItemVenda(id_venda=id_venda, id_produto=id_produto, quantidade=quantidade, preco_unitario=preco_unitario)
    
    session.add(item_venda)
    session.commit()
    print('Item de venda criado com sucesso!')
    
def criar_venda():
    #registrar um cliente
    id_cliente = buscar_cliente()
    
    #calcular o valor total da venda
    total = 0.0
    
    #lista de itens de venda
    itens_venda =[]
    
    if id_cliente is None:
        return # Retorna caso o cliente não seja encontrado
    else:
            #criar a venda
            venda = Venda(id_cliente=id_cliente, valor_total=0.0, data_venda=date.today())
            session.add(venda)
            session.commit() #salvar a venda no banco de dados para obter o id
            
            print('Olá {cliente.nome}!')
            
            #mostrar os produtos disponíveis
            print("\nProdutos disponíveis: \n")
            produtos = session.query(Produto).all()
            for produto in produtos:
                print(f"ID do produto: {produto.id_produto}, Nome do produto: {produto.nome}, Preço do produto: {produto.preco}, Quantidade em estoque: {produto.estoque_quantidade}")
                
            #adicionar itens à venda (laço para adicionar vários itens até que o usuário deseje parar)
            while True:
                id_produto = buscar_produto()
                quantidade = int(input("Digite a quantidade: "))
                
                #verificar se o produto existe
                produto = session.query(Produto).filter(Produto.id_produto == id_produto).first()
                if produto:
                    #verificar se a quantidade em estoque é suficiente
                    if produto.estoque_quantidade < quantidade:
                        print('Quantidade em estoque insuficiente!')
                        continue
                    else:
                        produto.estoque_quantidade -= quantidade
                        session.commit()
                        preco_unitario = produto.preco
                        total += preco_unitario * quantidade
                        itens_venda.append((id_produto, quantidade, preco_unitario))
                        print('Item adicionado com sucesso!')
                else:
                    print('Produto não encontrado!')
                    break
                
                #perguntar se deseja adicionar mais itens
                op = input("Deseja adicionar mais itens? (s/n): ")
                if op == 'n':
                    session.query(Venda).filter(Venda.id_venda == venda.id_venda).update({Venda.valor_total: total})
                    session.commit()
                    print('Valor total da venda: ', total)
                    print('Venda finalizada!')
                    break
     
def criar_categoria(nome, descricao):
    categoria = Categoria(nome=nome, descricao=descricao)
    session.add(categoria)
    session.commit()
    print('Categoria criada com sucesso!')
    
    
#READ
def ler_clientes():   
    clientes = session.query(Cliente).all()
    for cliente in clientes:
        print(f"ID: {cliente.id_cliente}, Nome: {cliente.nome}, Email: {cliente.email}, Telefone: {cliente.telefone}")

def ler_produtos():
    produtos = session.query(Produto).all()
    #pegar o id da categoria do produto e mostrar o nome da categoria    
    
    for produto in produtos:
        categoria = session.query(Categoria).filter(Categoria.id_categoria == produto.id_categoria).first()
        print(f"ID: {produto.id_produto}, Nome do produto: {produto.nome}, Descricao do produto: {produto.descricao}, Preco do produto: {produto.preco}, Quantidade em estoque: {produto.estoque_quantidade}, Categoria: {categoria.nome}")

def ler_vendas():    
    vendas = session.query(Venda).all()
    for venda in vendas:
        print(f"ID da venda: {venda.id_venda}, Data da venda: {venda.data_venda}, Valor total: {venda.valor_total}, ID do cliente: {venda.id_cliente}")      
        #mostrar os itens da venda
        itens_venda = session.query(ItemVenda).filter(ItemVenda.id_venda == venda.id_venda).all()
        for item in itens_venda:
            print(f"    ID do produto: {item.id_produto}, Quantidade: {item.quantidade}, Preco unitario: {item.preco_un}") 
        
def ler_categorias():
    categorias = session.query(Categoria).all()
    for categoria in categorias:
        print(f"{categoria.id_categoria}, {categoria.nome}, {categoria.descricao}")
    

#UPDATE
def atualizar_cliente(id, nome, email, telefone):
    cliente = session.query(Cliente).filter(Cliente.id_cliente == id).first()
    if cliente:
        cliente.nome = nome
        cliente.email = email
        cliente.telefone = telefone
        session.commit()
        print('Cliente atualizado com sucesso!')
    else:
        print('Cliente não encontrado!')
        

def atualizar_produto(id, nome, descricao, preco, estoque_quantidade, id_categoria):
    produto = session.query(Produto).filter(Produto.id_produto == id).first()
    if produto:
        produto.nome = nome
        produto.descricao = descricao
        produto.preco = preco
        produto.estoque_quantidade = estoque_quantidade
        produto.id_categoria = id_categoria
        
        while True:
            
            #verificação se a categoria existe
            if session.query(Categoria).filter(Categoria.id_categoria == id_categoria).first() is None:
                print('Categoria não encontrada!')
                id_categoria = int(input("Digite o ID da categoria do produto: "))
            else:
                break
            
        session.commit()
        print('Produto atualizado com sucesso!')
    else:
        print('Produto não encontrado!')
        
def atualizar_categoria(id, nome, descricao):
    categoria = session.query(Categoria).filter(Categoria.id_categoria == id).first()
    if categoria:
        categoria.nome = nome
        categoria.descricao = descricao
        session.commit()
        print('Categoria atualizada com sucesso!')
    else:
        print('Categoria não encontrada!')
        
def atualizar_venda():
    id_venda = buscar_venda()
    if id_venda is None:
        return # Retorna caso a venda não seja encontrada
    else:
        #mostra a venda
        venda = session.query(Venda).filter(Venda.id_venda == id_venda).first()
        print(f"ID da venda: {venda.id_venda}, Data da venda: {venda.data_venda}, Valor total: {venda.valor_total}, ID do cliente: {venda.id_cliente}")
        
        #mostrar os itens da venda
        itens_venda = session.query(ItemVenda).filter(ItemVenda.id_venda == id_venda).all()
        for item in itens_venda:
            print(f"    ID do produto: {item.id_produto}, Quantidade: {item.quantidade}, Preco unitario: {item.preco_un}")
            
        #o que deseja atualizar?
        while True:
            print("O que deseja atualizar?")
            print("1 - Cliente")
            print("2 - Itens da venda")
            print("3 - Valor total")
            print("0 - Voltar")
            
            op = int(input("Digite a opção desejada: "))
            
            if op == 1:
                id_cliente = int(input("Digite o ID do cliente: "))
                venda.id_cliente = id_cliente
                session.commit()
                print('Cliente atualizado com sucesso!')
            elif op == 2:
                #atualizar os itens da venda
                #deseja remover, adicionar ou atualizar a quantidade?
                while True:
                    print("O que deseja fazer com os itens da venda?")
                    print("1 - Adicionar item")
                    print("2 - Remover item")
                    print("3 - Atualizar quantidade")
                    print("0 - Voltar")
                    
                    op = int(input("Digite a opção desejada: "))
                    
                    if op == 1:
                        id_produto = int(input("Digite o ID do produto: "))
                        quantidade = int(input("Digite a quantidade: "))
                        
                        #pegar o preço unitário do produto
                        produto = session.query(Produto).filter(Produto.id_produto == id_produto).first()
                        preco_unitario = produto.preco
                        
                        #verificar se o produto já existe na venda
                        item_venda = session.query(ItemVenda).filter(ItemVenda.id_venda == id_venda, ItemVenda.id_produto == id_produto).first()
                        
                        #se o produto já existe na venda, atualizar a quantidade, se não, criar o novo item na venda
                        if item_venda:
                            item_venda.quantidade += quantidade
                            session.commit()
                            print('Quantidade atualizada com sucesso!')
                        else:
                            criar_item_venda(id_venda, id_produto, quantidade, preco_unitario)
                    
                    elif op == 2:
                        id_produto = int(input("Digite o ID do produto: "))
                        quantidade = int(input("Digite a quantidade: "))
                        deletar_item_venda(id_venda, id_produto, quantidade)
                    elif op == 3:
                        id_produto = int(input("Digite o ID do produto: "))
                        quantidade = int(input("Digite a nova quantidade: "))
                        
                        #verificar se o produto existe na venda
                        item_venda = session.query(ItemVenda).filter(ItemVenda.id_venda == id_venda, ItemVenda.id_produto == id_produto).first()
                        if item_venda:
                            item_venda.quantidade = quantidade
                            session.commit()
                            print('Quantidade atualizada com sucesso!')
                        else:
                            print('Item não encontrado!')
                    elif op == 0:
                        break
                    else:
                        print("Opção inválida!")
#DELETE

def deletar_cliente(id):
    cliente = session.query(Cliente).filter(Cliente.id_cliente == id).first()
    if cliente:
        session.delete(cliente)
        session.commit()
        print('Cliente deletado com sucesso!')
    else:
        print('Cliente não encontrado!')
        
def deletar_produto(id):
    produto = session.query(Produto).filter(Produto.id_produto == id).first()
    if produto:
        session.delete(produto)
        session.commit()
        print('Produto deletado com sucesso!')
    else:
        print('Produto não encontrado!')
        
def deletar_item_venda(id_venda, id_produto, quantidade):
    item_venda = session.query(ItemVenda).filter(ItemVenda.id_venda == id_venda, ItemVenda.id_produto == id_produto).first()
    #verificar se o item existe
    if item_venda:
        #verificar se a quantidade a ser removida é menor que a quantidade do item
        if item_venda.quantidade > quantidade:
            item_venda.quantidade -= quantidade
            session.commit()
            print('Quantidade atualizada com sucesso!')
        else:
            session.delete(item_venda)
            session.commit()
            print('Item deletado com sucesso!')
    else:
        print('Item não encontrado na venda!')
        
def deletar_venda(id):
    venda = session.query(Venda).filter(Venda.id_venda == id).first()
    if venda:
        #apaagar os itens da venda
        itens_venda = session.query(ItemVenda).filter(ItemVenda.id_venda == id).all()
        for item in itens_venda:
            session.delete(item)
        session.delete(venda)
        session.commit()
        print('Venda deletada com sucesso!')
    else:
        print('Venda não encontrada!')
        
def deletar_categoria(id):
    categoria = session.query(Categoria).filter(Categoria.id_categoria == id).first()
    if categoria:
        session.delete(categoria)
        session.commit()
        print('Categoria deletada com sucesso!')
    else:
        print('Categoria não encontrada!')

        
#closing the connection
connection.close()