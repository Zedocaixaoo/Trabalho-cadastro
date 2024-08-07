import hashlib
import datetime
import random

def guest():
    while True:
         guest = input("Você já possui um cadastro? (s/n): ")
         if guest.lower() == "s":
            login()
            break
         elif guest.lower() == "n":
             usuario_guest()
             break
         else: print("Caractere não indicado ")

def usuario_guest():
    while True:
        usuario_guest = input("Gostaria de fazer um cadastro? (s/n): ")
        if usuario_guest.lower() == "s":
           cadastro()
           main()
           break
        elif usuario_guest.lower() == "n":
           id_guest = random.randint(0, 9999)
           break
        else: print("Caractere não indicado ")

def cadastro():
    nome = input("Digite o nome de usuario: ")
    CPF = input("Digite o cpf de usuario: ")
    senha = input("Digite a senha: ")

    hash_senha = hashlib.sha256(senha.encode()).hexdigest()

    with open("usuarios.txt", "a") as arquivo:
        arquivo.write(f"{nome},{CPF},{hash_senha}\n")

    print("Usuario cadastrado com sucesso\n")

def adicionar_usuario():
    while True:
        cadastro()
        continuar = input("Deseja cadastrar outro usuario (s/n): ")
        if continuar.lower()!= '':
            break

def login():
    pergunta = input("Você já possui cadastro? (s/n): ")
    if pergunta.lower() == 's':
        login2()
        return
    elif pergunta.lower() == 'n':
         usuario_guest()
         return
    else: print('Caractere não indicado ')

def login2():        
    cpf = input("Digite seu CPF: ")
    senha = input("Senha: ")

    hash_senha = hashlib.sha256(senha.encode()).hexdigest()

    with open("usuarios.txt", "r") as arquivo:
        linhas = arquivo.readlines()

    for linha in linhas:
        dados = linha.strip().split(',')
        if dados[1] == cpf and dados[2].strip() == hash_senha:
            print(f"Bem-vindo {dados[0]}!\n")
            return dados[0]
    
    print("CPF ou senha incorretos. Tente novamente.\n")
    return None

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
    print("Formas de pagamento disponíveis:")
    print("1 - Dinheiro")
    print("2 - Cartão de Crédito")
    print("3 - Cartão de Débito")
    print("4 - Xerecard")
    print("5 - Boleto Bancário")
    print("6 - Fiado")
    escolha = input("Selecione a forma de pagamento: ") 

    if escolha == "1":
        return "Dinheiro"
    elif escolha == "2":
        return "Cartão de Crédito"
    elif escolha == "3":
        return "Cartão de Débito"
    elif escolha == "4":
        dia_pagamento = input("Digite o dia do pagamento (DD/MM/AAAA): ")
        hora_pagamento = input("Digite a hora do pagamento (HH:MM): ")
        print("Endereço: Rua Dr. Creme, 666, Xique-Xique BA.")
        print("Referência: Na Frente do Cemitério de Xique-Xique.")
        return "Xerecard"
    elif escolha == "5":
        return "Boleto Bancário"
    elif escolha == "6":
        nota_pagamento = print("O Pagamento deve ser realizado no prazo de uma semana!")
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

        escolha = input("Digite o código do item que deseja comprar (ou 'sair' para finalizar): ")
        if escolha.lower() == 'sair':
            break
        elif escolha in itens_disponiveis:
            carrinho.append(itens_disponiveis[escolha])
            print(f"{itens_disponiveis[escolha]['nome']} adicionado ao carrinho.\n")
        else:
            print("Código inválido. Tente novamente.\n")

    if carrinho:
        total = sum(item['preco'] for item in carrinho)
        forma_pagamento = selecionar_pagamento()
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if login2.startswith("guest"):
            id_guest = login2.split()[-1]
            historico_compras.append({
                 "data_hora": data_hora,
                  "itens": carrinho,
                  "total": total,
                 "forma_pagamento": forma_pagamento,
                 "usuario": login2,
                 "id_guest": id_guest
             })
        else:
            historico_compras.append({
                "data_hora": data_hora,
                "itens": carrinho,
                "total": total,
                "forma_pagamento": forma_pagamento,
                "usuario": login2
            })
        print(f"Compra realizada com sucesso. Total: R${total:.2f}, Forma de Pagamento: {forma_pagamento}\n")
        with open("historico_compras.txt", "a") as arquivo:
            arquivo.write(f"{data_hora},{total:.2f},{forma_pagamento}\n")
            for item in carrinho:
                arquivo.write(f"{item['nome']},{item['preco']:.2f}\n")
            if login2.startswith("guest"):
                arquivo.write(f"Guest {id_guest}\n")
            else:
                arquivo.write(f"Usuario {login2}\n")
    else:
        print("Nenhum item no carrinho.\n")

def exibir_historico(historico_compras):
    if not historico_compras:
        print("Nenhuma compra realizada ainda.\n")
        return

    for compra in historico_compras:
        print(f"Data/Hora: {compra['data_hora']}")
        print("Itens comprados:")
        for item in compra['itens']:
            print(f"- {item['nome']} - R${item['preco']:.2f}")
        print(f"Total: R${compra['total']:.2f}")
        print(f"Forma de Pagamento: {compra['forma_pagamento']}\n")

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
                if len(dados) == 3:
                    compra_atual = {
                        "data_hora": dados[0],
                        "total": float(dados[1]),
                        "forma_pagamento": dados[2]
                    }
                    compra_atual["itens"] = []
                    historico_compras.append(compra_atual)
                elif len(dados) == 2:
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
    usuario = login()
    if usuario is None:
        guest_usuario = usuario_guest()
        sistema_de_compras(itens_disponiveis, historico_compras, f"Guest {guest_usuario}")
    else:
        usuario = login2()    
    while True:
        print("\nMenu:")
        print("1 - Fazer cadastro")
        print("2 - Fazer compra")
        print("3 - Exibir histórico de compras")
        if usuario == "Jurandir":
            print("4 - Adicionar item")
            print("5 - Total de vendas do dia")
        print("6 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastro()
        elif opcao == '2':
            sistema_de_compras(itens_disponiveis, historico_compras)
        elif opcao == '3':
            exibir_historico(historico_compras)
        elif opcao == '4' and usuario == "Jurandir":
            adicionar_item(itens_disponiveis)
        elif opcao == '5' and usuario == "Jurandir":
            dia = input("Digite a data (AAAA-MM-DD): ")
            total_vendas_dia(historico_compras, dia)
        elif opcao == '6':
            print("Saindo...")
            break
        else:
            print("Opção inválida ou sem permissão. Tente novamente.\n")

if __name__ == "__main__":
    main()
