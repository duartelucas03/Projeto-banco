menu = f"""===========MENU===========

        [e] Extrato
        [s] Saque
        [d] Depósito
        [x] Sair

==========================
Digite uma opção:
"""

saldo = 0;
limite = 500;
saques_realizados=0;
saques_limite=3;
extrato = "";


while True:
    opcao = input(menu);

    if opcao == "e":
        print("=============EXTRATO=============\n");
        print("Não foram realizadas operações\n") if extrato=="" else print(extrato);
        print(f"Saldo: {saldo:.2f}")
        print("=================================\n");

    elif opcao == "s":
        if saques_realizados<saques_limite:
            valor = float(input("Digite o valor do saque: "));
            if valor>saldo:
                print("\nSaldo insuficiente para realizar a operação!\n");
            elif valor>0:
                if valor<=500:
                    saldo-=valor;
                    saques_realizados+=1;
                    extrato+= f"Saque: R$ {valor:.2f}\n";
                    print(f"\nSaque de R$ {valor:.2f} realizado com sucesso!\n")
                else:
                    print("\nLimite de saque excedido!\n");
            else:
                print("\nValor inválido!\n");
        else:
            print("\nNúmero máximo de saques excedidos!\n");
    
    elif opcao == "d":
        valor = float(input("Digite o valor do depósito: "));

        if valor>0:
            saldo+=valor;
            extrato+= f"Depósito: R$ {valor:.2f}\n";
            print(f"\nDepósito de R$ {valor:.2f} realizado com sucesso!\n")
        else:
            print("\nValor inválido!\n");
    
    elif opcao == "x":
        break;
    else:
        print("\nComando inválido. Tente novamente.\n");