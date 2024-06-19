import hashlib

def cadastro():
    nome = input("Digite o nome de usuario: ")
    CPF = input("Digite o cpf de usuario: ")
    senha = input("Digite a senha: ")

    hash_senha = hashlib.sha256(senha.encode()).hexdigest()

    with open("usuarios.txt", "a") as arquivo:
        arquivo.write(f"{nome}, {CPF}, {hash_senha}\n")

    print("Usuario cadastrado com sucesso\n")

def adicionar_usuario():
    while True:
        cadastro()
        continuar = input("Deseja cadastrar outro usuario (s/n): ")
        if continuar.lower() != 's':
            break

adicionar_usuario()


import hashlib

def login():
    cpf = input("Digite seu CPF: ")
    senha = input("Senha: ")

    hash_senha = hashlib.sha256(senha.encode()).hexdigest()

    with open("usuarios.txt", "r") as arquivo:
        linhas = arquivo.readlines()

    for linha in linhas:
        dados = linha.strip().split(',')
        if dados[1] == cpf and dados[2] == hash_senha:
            print(f"Bem-vindo, {dados[0]}!\n")
            return True
        
    print("CPF ou senha incorretos. Tente novamente.\n")
    return False

while True:
    if login():
        break



