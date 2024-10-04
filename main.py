import datetime

def menu():
    menu = f"""===========MENU===========
    
    [e] Extrato
    [s] Saque
    [d] Depósito
    [u] Criar Usuário
    [c] Criar Conta
    [lc] Listar Contas
    [x] Sair
    
==========================
=>"""
    return menu;


def verificar_limite_transacoes(transacoes_diarias):
    
    data = datetime.datetime.now().strftime("%d/%m/%Y")
    if data in transacoes_diarias and transacoes_diarias[data] == 10:
        print(f"\nLimite de transações excedido para {data}!\n")
        return True
    else:
        return False
    
def mostrar_extrato(saldo, extrato):    
    print("=============EXTRATO=============\n");    
    print("Não foram realizadas operações\n") if extrato=="" else print(extrato);    
    print(f"Saldo: {saldo:.2f}")    
    print("=================================\n");

def saque(saques_realizados, saques_limite, saldo, extrato, transacoes_diarias):
        if saques_realizados<saques_limite:
            valor = float(input("Digite o valor do saque: "));
            if valor>saldo:
                print("\nSaldo insuficiente para realizar a operação!\n");
            elif valor>0:
                if valor<=500:
                    saldo-=valor;
                    saques_realizados+=1;
                    data_hora = datetime.datetime.now();
                    data = data_hora.strftime("%d/%m/%Y");
                    hora = data_hora.strftime("%H:%M:%S");
                    extrato+= f"Saque: R$ {valor:.2f} | Realizado: {data} {hora} |\n";
                    print(f"\nSaque de R$ {valor:.2f} realizado com sucesso!\n");
                    if data in transacoes_diarias:
                        transacoes_diarias[data] += 1;
                    else:
                        transacoes_diarias[data] = 1;
                else:
                    print("\nLimite de saque excedido!\n");
            else:
                print("\nValor inválido!\n");
        else:
            print("\nNúmero máximo de saques excedidos!\n");
        return saldo, extrato, transacoes_diarias, saques_realizados;

def deposito(saldo, extrato, transacoes_diarias):
        valor = float(input("Digite o valor do depósito: "));

        if valor>0:
            saldo+=valor;
            data_hora = datetime.datetime.now();
            data = data_hora.strftime("%d/%m/%Y");
            hora = data_hora.strftime("%H:%M:%S");
            extrato+= f"Depósito: R$ {valor:.2f} | Realizado: {data} {hora} |\n";
            print(f"\nDepósito de R$ {valor:.2f} realizado com sucesso!\n");
            if data in transacoes_diarias:
                transacoes_diarias[data] += 1;
            else:
                transacoes_diarias[data] = 1;
        else:
            print("\nValor inválido!\n");
        return saldo, extrato, transacoes_diarias;

def criar_usuario(usuarios):
    cpf = input("Digite o CPF do usuário (somente numeros): ")
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("\nUsuário já cadastrado!\n")
            return
    nome = input("Digite o nome do usuário: ")
    data_nascimento = input("Digite a data de nascimento do usuário (dd-mm-aaaa): ")
    endereco = input("Digite o endereço (logradouro, nro - bairro - cidade/UF): ")

    usuarios.append({"cpf": cpf, "nome": nome, "data_nascimento": data_nascimento, "endereco": endereco})
    print("\nUsuário cadastrado com sucesso!\n")

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário (somente numeros): ")
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("\nUsuário não encontrado!\n")
    return None

def listar_contas(contas):
                print("\nLista de contas cadastradas:\n")
                for conta in contas:
                    print(f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {conta['usuario']['nome']}")
                print("\n")

def main():

    transacoes_diarias = {}
    saldo = 0;
    saques_realizados = 0;
    saques_limite = 3;
    extrato = "";
    usuarios = [];
    contas = [];
    AGENCIA = "0001";

    while True:
        opcao = input(menu());

        if opcao == "e":
            mostrar_extrato(saldo, extrato);

        
        elif opcao == "s":
            if verificar_limite_transacoes(transacoes_diarias):
                continue
            saldo, extrato, transacoes_diarias, saques_realizados = saque(saques_realizados, saques_limite, saldo, extrato, transacoes_diarias);
        
        

        elif opcao == "d":
            if verificar_limite_transacoes(transacoes_diarias):
                continue
            saldo, extrato, transacoes_diarias = deposito(saldo, extrato, transacoes_diarias);
        
        elif opcao == "u":
            criar_usuario(usuarios);
        
        elif opcao == "c":
            numero_conta = len(contas) + 1;
            conta = criar_conta(AGENCIA, numero_conta, usuarios);
            if conta:
                contas.append(conta);
                print("\nConta criada com sucesso!\n");
            else:
                print("\nConta não criada!\n");
        
        elif opcao == "lc":
            if contas == []:
                print("\nNenhuma conta cadastrada!\n");
                continue;
            listar_contas(contas);

        elif opcao == "x":
            break;
        else:
            print("\nComando inválido. Tente novamente.\n");

main();