import hashlib
import datetime
import random
import time
import sys

def cadastro():
    
    print("então vamos fazer.")
    for i in range(5):  
        sys.stdout.write("\rloading" + "." * (i + 1) + "")
        sys.stdout.flush()
        time.sleep(0.5)  
    print("\n")
    nome = input("crie um nome de usuario: ")

    CPF = ""
    while True:
        CPF = input("digite seu cpf (XXX.XXX.XXX-XX): ")
        CPF = CPF.replace('.', '').replace('-', '')
        if CPF.isdigit() and len(CPF) == 11:
            CPF_formatado = "{}.{}.{}-{}".format(CPF[:3], CPF[3:6], CPF[6:9], CPF[9:])
            print("CPF:", CPF_formatado)
    
            break
        else:
            print("CPF invalido. Dig1te novamente.")
    
    senha = input("crie uma senha: ")
    hash_senha = hashlib.sha256(senha.encode()).hexdigest()

    with open("usuarios.txt", "a") as arquivo:
        arquivo.write(f"{nome},{CPF},{hash_senha}\n")

    print("usuario cadastrado com sucesso\n")
    adicionar_usuario()

def adicionar_usuario():
    while True:
        continuar = input("deseja cadastrar outro usuario (s/n): ")
        if continuar.lower() == 's':
            while True:
              cadastro()
              break
        elif continuar.lower() == 'n':
            print("Login: ")
            login()
            break
        else:
            print("caractere não indicado. ")
            adicionar_usuario()
            return

def login():
    CPF = input("digite seu CPF (XXX.XXX.XXX-XX): ")
    CPF = CPF.replace('.', '').replace('-', '')
    if CPF.isdigit() and len(CPF) == 11:
        CPF_formatado = "{}.{}.{}-{}".format(CPF[:3], CPF[3:6], CPF[6:9], CPF[9:])
        print("CPF:", CPF_formatado)
    else:
        print("CPF inválido. digite novamente.")
        return None
    senha = input("Senha: ")

    hash_senha = hashlib.sha256(senha.encode()).hexdigest()

    with open("usuarios.txt", "r") as arquivo:
        linhas = arquivo.readlines()

    for linha in linhas:
        dados = linha.strip().split(',')
        if dados[1] == CPF and dados[2].strip() == hash_senha:
            print(f"Bem-vindo {dados[0]}!\n")
            return dados[0]
    
    print("CPF ou senha incorretos. Tente novamente.\n")
    temcadastro()

    return None

def temcadastro():
    pergunta = input("você possui um cadastro? (s/n): ")
    if pergunta.lower() == "s":
        while True:
            login()
            break
    elif pergunta.lower() == "n":
        while True:
            cadastro()
            break
    else:
        print("caractere nao indicado.")
        temcadastro()

def adicionar_item(itens_disponiveis):
    nome = input("Nome do item: ")
    preco = float(input("Preço do item: "))
    codigo = str(len(itens_disponiveis) + 1)
    itens_disponiveis[codigo] = {"nome": nome, "preco": preco}
    print(f"Item {nome} adicionado com sucesso.\n")
    with open("itens.txt", "w") as arquivo:
        for codigo, item in itens_disponiveis.items():
            arquivo.write(f"{codigo},{item['nome']},{item['preco']}\n")

def selecionar_pagamento():
    print("formas de pagamento disponíveis:")
    print("1 - Dinheiro")
    print("2 - Cartão de Crédito")
    print("3 - Cartão de Débito")
    print("4 - Xerecard")
    print("5 - Boleto Bancário")
    print("6 - Fiado")
    escolha = input("selecione a forma de pagamento: ") 

    if escolha == "1":
        return "Dinheiro"
    elif escolha == "2":
        return "Cartão de Crédito"
    elif escolha == "3":
        return "Cartão de Débito"
    elif escolha == "4":
        dia_pagamento = input("Digite o dia do pagamento (DD/MM/AAAA): ")
        hora_pagamento = input("Digite a hora do pagamento (HH:MM): ")
        print("local do pagamento ;) :")
        print("Endereço: Rua Dr. Creme, 666, Xique-Xique BA.")
        print("Referência: Na Frente do Cemitério de Xique-Xique.")
        return "Xerecard"
    elif escolha == "5":
        return "Boleto Bancário"
    elif escolha == "6":
        nota_pagamento = print("O pagamento deve ser realizado no prazo de uma semana!")
        dia_pagamento = input("Qual o dia de pagamento? (DD/MM/AAAA): ")
        return fiado_pagamento()
    
def fiado_pagamento():
            print("Formas de pagamento disponíveis:")
            print("1 - Dinheiro")
            print("2 - Cartão de Crédito")
            print("3 - Cartão de Débito")
            print("4 - Boleto Bancário")
            
            escolha = input("Selecione a forma de pagamento: ")

            if escolha == "1":
                return "Fiado=Dinheiro"
            elif escolha == "2":
                return "Fiado=Cartão de Crédito"
            elif escolha == "3":
                return "Fiado=Cartão de Débito"
            elif escolha == "4":
                return "Fiado=Boleto Bancário"

def sistema_de_compras(itens_disponiveis, historico_compras):
    carrinho = []

    while True:
        print("Itens disponíveis:")
        for codigo, item in itens_disponiveis.items():
            print(f"{codigo} - {item['nome']} - R${item['preco']:.2f}")

        escolha = input("digite o código do item que deseja comprar (ou 'sair' para finalizar): ")
        if escolha.lower() == 'sair':
            break
        elif escolha in itens_disponiveis:
            carrinho.append(itens_disponiveis[escolha])
            print(f"{itens_disponiveis[escolha]['nome']} adicionado ao carrinho.\n")
        else:
            print("Código inexistente. Tente novamente.\n")

    if carrinho:
        total = sum(item['preco'] for item in carrinho)
        forma_pagamento = selecionar_pagamento()
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        gente = login()
        historico_compras.append({
            "data_hora": data_hora,
            "itens": carrinho,
            "total": total,
            "forma_pagamento": forma_pagamento,
            "usuario": gente
            })
        print(f"Compra realizada com sucesso. Total: R${total:.2f}, Forma de Pagamento: {forma_pagamento}\n")
        with open("historico_compras.txt", "a") as arquivo:
            arquivo.write(f"{data_hora},{total:.2f},{forma_pagamento},{gente}\n")
            for item in carrinho:
                arquivo.write(f"{item['nome']},{item['preco']:.2f}\n")
    else:
        print("Nenhum item no carrinho.\n")

def exibir_historico(historico_compras, usuario_logado):        
    compras_usuario = [compra for compra in historico_compras if compra['usuario'] == usuario_logado]
    if usuario_logado == "Jurandir":
       for compra in historico_compras:
        print(f"\nData/Hora: {compra['data_hora']}")
        print("Itens comprados:")
        for item in compra['itens']:
            print(f"- {item['nome']} - R${item['preco']:.2f}")
        print(f"Total: R${compra['total']:.2f}")
        print(f"Forma de Pagamento: {compra['forma_pagamento']}\n")
            
    elif usuario_logado == login():
         for compra in compras_usuario:
            if compra['usuario'] == usuario_logado:
                print(f"\nData/Hora: {compra['data_hora']}")
                print("Itens comprados:")
                for item in compra['itens']:
                    print(f"- {item['nome']} - R${item['preco']:.2f}")
                print(f"Total: R${compra['total']:.2f}")
                print(f"Forma de Pagamento: {compra['forma_pagamento']}\n")
                
    else:
        print("\nnenhuma compra realizada ainda. ")
        
def adicionar_compra(historico_compras, compra):
    for c in historico_compras:
        if c['data_hora'] == compra['data_hora'] and c['usuario'] == compra['usuario']:
            return
    historico_compras.append(compra)

def total_vendas_dia(historico_compras, dia):
    total_dia = sum(compra['total'] for compra in historico_compras if compra['data_hora'].startswith(dia))
    print(f"Total de vendas em {dia}: R${total_dia:.2f}\n")

def carregar_itens():
    itens_disponiveis = {}
    try:
        with open("itens.txt", "r") as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas:
                codigo, nome, preco = linha.strip().split(',')
                itens_disponiveis[codigo] = {"nome": nome, "preco": float(preco)}
    except FileNotFoundError:
        pass
    return itens_disponiveis

def carregar_historico():
    historico_compras = []
    try:
        with open("historico_compras.txt", "r") as arquivo:
            linhas = arquivo.readlines()
            compra_atual = None
            for linha in linhas:
                dados = linha.strip().split(',')
                if len(dados) == 4:
                    compra_atual = {
                        "data_hora": dados[0],
                        "total": float(dados[1]),
                        "forma_pagamento": dados[2],
                        "usuario": dados[3],
                        "itens": [],
                    }
                    compra_atual["itens"] = []
                    historico_compras.append(compra_atual)
                elif len(dados) == 2 and compra_atual is not None:
                    compra_atual["itens"].append({
                        "nome": dados[0],
                        "preco": float(dados[1])
                    })
    except FileNotFoundError:
        pass
    return historico_compras

def main():
    itens_disponiveis = carregar_itens()
    historico_compras = carregar_historico()

    print("Quitanda Jurandir")
    escolha = input("você já tem um cadastro? (s/n): ")
    usuario = None
    if escolha.lower() == 's':
        while True:
            usuario = login()
            if usuario:
                break
    elif escolha.lower() == 'n':
        cadastro()
        while True:
            usuario = login()
            break
    else:
        print("caractere não indicado. ")
        while True:
          main()
          break

    while True:
        for i in range(5):  
            sys.stdout.write("\rloading" + "." * (i + 1) + "")
            sys.stdout.flush()
            time.sleep(0.5)  
        print("\n")
        print("\nMenu:")
        print("1 - Fazer compra")
        print("2 - Exibir histórico de compras")
        if usuario == "Jurandir":
            print("3 - Adicionar item")
            print("4 - Total de vendas do dia")
        print("5 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            sistema_de_compras(itens_disponiveis, historico_compras)
        elif opcao == '2':
            exibir_historico(historico_compras, usuario)
        elif opcao == '3' and usuario == "Jurandir":
            adicionar_item(itens_disponiveis)
        elif opcao == '4' and usuario == "Jurandir":
            dia = input("Digite a data (AAAA-MM-DD): ")
            total_vendas_dia(historico_compras, dia)
        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida ou sem permissão. Tente novamente.\n")

if __name__ == "__main__":
    main()
