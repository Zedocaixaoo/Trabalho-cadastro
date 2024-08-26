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
    
    while True:
        nome = input("crie um nome de usuario: ")
        if nome.replace(" ", "").isalnum():                #porra de opção que faz a parada de não deixar digitar outra coisa alem de letras ou numeros sozinha
            break
        else:
            print("nome de usuario invalido, use apenas letras ou numeros.")

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
    print("\nCaso tenha entrado sem querer digite 'sair'")
    CPF = input("digite seu CPF (XXX.XXX.XXX-XX): ")
    CPF = CPF.replace('.', '').replace('-', '')
    if CPF.isdigit() and len(CPF) == 11:
        CPF_formatado = "{}.{}.{}-{}".format(CPF[:3], CPF[3:6], CPF[6:9], CPF[9:])
        print("CPF:", CPF_formatado)
    elif CPF.lower() == 'sair':
        temcadastro()
    else:
        print("CPF ou opção invalida. digite novamente.")
        return None

    tentativas_erradas = 0

    while True:
        senha = input("senha: ")
        hash_senha = hashlib.sha256(senha.encode()).hexdigest()

        with open("usuarios.txt", "r") as arquivo:
            linhas = arquivo.readlines()

        for linha in linhas:
            dados = linha.strip().split(',')
            if dados[1] == CPF and dados[2].strip() == hash_senha:
                print(f"Bem-vindo {dados[0]}!\n")
                return dados[0]

        tentativas_erradas += 1
        print("CPF ou senha incorretos. Tente novamente.\n")

        if tentativas_erradas >= 5:
            resposta = input("esqueceu sua senha? (s/n): ")
            if resposta.lower() == 's':
                redefinir_senha(CPF)
                return login()
            elif resposta.lower() == 'n':
                tentativas_erradas = 0
                continue
            else:
                print("caractere não indicado.")
                tentativas_erradas = 0
                continue
    
def redefinir_senha(CPF):
    nova_senha = input("\ndigite a nova senha: ")
    hash_nova_senha = hashlib.sha256(nova_senha.encode()).hexdigest()

    with open("usuarios.txt", "r+") as arquivo:
        linhas = arquivo.readlines()
        arquivo.seek(0)
        for linha in linhas:
            dados = linha.strip().split(',')
            if dados[1] == CPF:
                linha = f"{dados[0]},{CPF},{hash_nova_senha}\n"
            arquivo.write(linha)
        arquivo.truncate()

    print("senha redefinida com sucesso\n")

def temcadastro():
    pergunta = input("você realmente possui um cadastro? (s/n): ")
    if pergunta.lower() == "s":
            login()
            return
    elif pergunta.lower() == "n":
            cadastro()
            return
    else:
        print("caractere nao indicado.")
        temcadastro()

def adicionar_item(itens_disponiveis):
    nome = input("nome do item: ")
    while True:
        preco_str = input("preço do item: ")
        try:
            preco = float(preco_str)
            break
        except ValueError:
            print("valor invalido. digite um número decimal (ex: 10.99).")

    codigo = str(len(itens_disponiveis) + 1)
    itens_disponiveis[codigo] = {"nome": nome, "preco": preco}
    print(f"item {nome} adicionado com sucesso.\n")
    with open("itens.txt", "w") as arquivo:
        for codigo, item in itens_disponiveis.items():
            arquivo.write(f"{codigo},{item['nome']},{item['preco']}\n")
            
def remover_item(itens_disponiveis):
    usuario = login()
    if usuario != "Jurandir":
        print("você não tem permissão para remover itens.")
        return

    print("\nitens disponíveis:")
    for codigo, item in itens_disponiveis.items():
        print(f"{codigo} - {item['nome']} - R${item['preco']:.2f}")

    while True:
        codigo_remover = input("digite o código do item que deseja remover (ou 'sair' para cancelar): ")
        if codigo_remover.lower() == 'sair':
            break
        elif codigo_remover in itens_disponiveis:
            item_nome = itens_disponiveis[str(codigo_remover)]['nome']
            print(f"item {itens_disponiveis[codigo_remover]['nome']} removido com sucesso.\n")
            del itens_disponiveis[str(codigo_remover)]
            with open("itens.txt", "w") as arquivo:
                for codigo, item in itens_disponiveis.items():
                    arquivo.write(f"{codigo},{item['nome']},{item['preco']}\n")
            break
        else:
            print("Código inexistente. Tente novamente.\n")

def troco(valor_total, valor_pago):
    troco = valor_pago - valor_total
    return troco

def selecionar_pagamento(carrinho, itens_disponiveis):
    print("formas de pagamento disponíveis:")
    print("1 - Dinheiro")
    print("2 - Cartão de Crédito")
    print("3 - Cartão de Débito")
    print("4 - Xerecard")
    print("5 - Boleto Bancário")
    print("6 - Fiado")
    escolha = input("selecione a forma de pagamento: ")

    if escolha == "1":
        forma_pagamento = "dinheiro"
        valor_total = sum(item['preco'] for item in carrinho)
        print(f"valor total da compra: R${valor_total:.2f}")
        while True:
            valor_pago_str = input("digite o valor pago em dinheiro: R$ ")
            try:
                valor_pago = float(valor_pago_str)
                break
            except ValueError:
                print("craactere inválido, tente novamente.")
        if valor_pago < valor_total:
            print("valor pago é menor que o valor total da compra. Tente novamente.")
        else:
            troco = valor_pago - valor_total
            if troco > 0:
                print(f"troco: R${troco:.2f}\n")
            print("pagamento realizado com sucesso!\nconfirme seu login\n")
        return "Dinheiro"
    elif escolha == "2":
        print("confirme seu login:\n")
        return "Cartão de Crédito"
    elif escolha == "3":
        return "Cartão de Débito"
    elif escolha == "4":
        dia_pagamento = input("Digite o dia do pagamento (DD/MM/AAAA): ")
        hora_pagamento = input("Digite a hora do pagamento (HH:MM): ")
        try:
            data_pagamento = datetime.datetime.strftime(f"{dia_pagamento}, {hora_pagamento}", "%d/%m/%Y %H:%M")
        except ValueError:           
            if data_pagamento < datetime.datetime.now():
                print("data e hora invalidas, o pagamento deve ser feito no futuro")
                return selecionar_pagamento(carrinho, itens_disponiveis)
            
        print("local do pagamento:")
        print("Endereço: Rua Dr. Creme, 666, Xique-Xique BA.")
        print("Referência: Na Frente do Cemitério de Xique-Xique.")
        print("\ncofirme seu login\n")
        return "Xerecard"
    elif escolha == "5":
        return "Boleto Bancário"
    elif escolha == "6":
        nota_pagamento = print("O pagamento deve ser realizado no prazo de uma semana\n")
        dia_pagamento = input("Qual o dia de pagamento? (DD/MM/AAAA): ")  
        try:
            data_pagamento = datetime.datetime.strptime(dia_pagamento, "%d/%m/%Y")
            if data_pagamento < datetime.datetime.now() or data_pagamento > datetime.datetime.now() + datetime.timedelta(days=7):
                 print("data invalida, deve ser dentro de uma semana")
                 return selecionar_pagamento(carrinho, itens_disponiveis)
        except ValueError:  
            print("data invalida, dd/mm/aaaa\n")
            return selecionar_pagamento(carrinho, itens_disponiveis)  
            
        print("\nconfirm seu login")
        return "Fiado"   
    else:
        escolha_int = int(escolha)
        if escolha_int < 1 or escolha_int > 6:
            print("caractere inválido, tente novamente.")
            return selecionar_pagamento(carrinho, itens_disponiveis)  
     
def efetuar_pagamento(itens_disponiveis, carrinho, historico_compras):
    forma_pagamento = input("selecione a forma de pagamento: ")
    total = sum(item['preco'] for item in carrinho)
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

def fiado_pagamento():
            print("Formas de pagamento disponíveis:")
            print("1 - Dinheiro")
            print("2 - Cartão de Crédito")
            print("3 - Cartão de Débito")
            print("4 - Boleto Bancário")
            
            escolha = input("selecione a forma de pagamento: ")

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
        print("itens disponiveis:")
        for codigo, item in itens_disponiveis.items():
            print(f"{codigo} - {item['nome']} - R${item['preco']:.2f}")

        escolha = input("digite o coodigo do item que deseja comprar (ou 'sair' para finalizar, ou 'r' para remover um item do carrinho): ")
        if escolha.lower() == 'sair':
            if carrinho:
                forma_pagamento = selecionar_pagamento(carrinho, itens_disponiveis)
                total = sum(item['preco'] for item in carrinho)
                data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                gente = login()
                historico_compras.append({
                    "data_hora": data_hora,
                    "itens": carrinho,
                    "total": total,
                    "forma_pagamento": forma_pagamento,
                    "usuario": gente
                    })
                print(f"\ncompra realizada com sucesso. Total: R${total:.2f}, forma de Pagamento: {forma_pagamento}\n")
                with open("historico_compras.txt", "a") as arquivo:
                    arquivo.write(f"{data_hora},{total:.2f},{forma_pagamento},{gente}\n")
                    for item in carrinho:
                        arquivo.write(f"{item['nome']},{item['preco']:.2f}\n")
            else:
                print("nenhum item no carrinho.\n")
            break
        elif escolha.lower() == 'r':
            if carrinho:
                print("itens no carrinho:")
                for i, item in enumerate(carrinho):
                    print(f"{i+1} - {item['nome']} - R${item['preco']:.2f}")
                escolha_remover = input("digite o numero do item que deseja remover (ou 'sair' para cancelar): ")
                if escolha_remover.lower() == 'sair':
                    continue
                try:
                    indice = int(escolha_remover) - 1
                    if indice >= 0 and indice < len(carrinho):
                        del carrinho[indice]
                        print("item removido com sucesso.\n")
                    else:
                        print("indice invalido  tente novamente.\n")
                except ValueError:
                    print("caractere invalido  tente novamente.\n")
            else:
                print("nenhum item no carrinho.\n")
        elif escolha in itens_disponiveis:
            carrinho.append(itens_disponiveis[escolha])
            print(f"{itens_disponiveis[escolha]['nome']} adicionado ao carrinho.\n")
        else:
            print("código inexistente. Tente novamente.\n")

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
    try:
        data = datetime.datetime.strptime(dia, "%Y-%m-%d")
        if data > datetime.datetime.now():
            print("data invalida. o futuro ainda não nos pertence.")
            return
    except ValueError:
        print("data inválida (AAAA-MM-DD) ")
        return

    total_dia = sum(compra['total'] for compra in historico_compras if compra['data_hora'].startswith(dia))
    print(f"total de vendas em {dia}: R${total_dia:.2f}\n")

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
    escolha = input("você ja tem um cadastro? (s/n): ")
    usuario = None
    if escolha.lower() == 's':
        while True:
            usuario = login()
            if usuario:
                break
    elif escolha.lower() == 'n':
        cadastro()
        while True:
            usuario = ""
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
        print("3 - Catalogo de produtos")
        if usuario == "Jurandir":
            print("4 - Adicionar item")
            print("5 - Total de vendas do dia")
            print("6 - Remover item")
        print("7 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            sistema_de_compras(itens_disponiveis, historico_compras)
        elif opcao == '2':
            exibir_historico(historico_compras, usuario)
        elif opcao == '3':
            print("catalogo de produtos:")
            for codigo, item in itens_disponiveis.items():
                print(f"{codigo}, {item['nome']}, R${item['preco']:.2f}")
        elif opcao == '4' and usuario == "Jurandir":
            adicionar_item(itens_disponiveis)
        elif opcao == '5' and usuario == "Jurandir":
            dia = input("digite a data (AAAA-MM-DD): ")
            total_vendas_dia(historico_compras, dia)
        elif opcao == '6' and usuario == "Jurandir":
            remover_item(itens_disponiveis),
        elif opcao == '7':
            print("Saindo...")
            break
        else:
            print("opçao invalida ou sem permissao. tente novamente.\n")

if __name__ == "__main__":
    main()
