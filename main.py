from datetime import datetime
from abc import ABC, abstractmethod
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero_conta, cliente):
        self._agencia = "0001"
        self._numero_conta = numero_conta
        self._cliente = cliente
        self._saldo = 0
        self._extrato = Extrato()

    @classmethod
    def nova_conta(cls, numero_conta, cliente):
        return cls(numero_conta, cliente)

    @property
    def agencia(self):
        return self._agencia
    
    @property
    def numero_conta(self):
        return self._numero_conta
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def extrato(self):
        return self._extrato
        
    def saque(self, valor):
        saldo = self._saldo
        
        if valor > saldo:
            print("\nSaldo insuficiente para realizar a operação!\n")
        
        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!\n")
            return True
        
        else:
            print("\nValor inválido!\n")
    
        return False
    
    def deposito(self, valor):
        
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso!\n")
        
        else:
            print("\nValor inválido!\n")
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero_conta, cliente, limite=500, limite_saque=3):
        super().__init__(numero_conta, cliente)
        self._limite = limite
        self._limite_saque = limite_saque

    def saque(self, valor):
        hoje = datetime.now().strftime("%d/%m/%Y")
        numero_saques = len([transacao for transacao in self._extrato.transacoes if transacao["tipo"] == Saque.__name__ and transacao["data"].startswith(hoje)])

        if valor > self._limite:
            print("\nLimite de saque excedido!\n")
        elif numero_saques >= self._limite_saque:
            print("\nNúmero máximo de saques excedidos!\n")
        elif valor > self._saldo:
            print("\nSaldo insuficiente para realizar a operação!\n")
        else:
            return super().saque(valor)
       
        return False
    
    def __str__(self):
        return f"""\
        Agência:\t{self.agencia}
        Conta:\t{self.numero_conta}
        Titular:\t{self.cliente.nome}
        """
    
class Extrato:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar (self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.saque(self._valor)
        if sucesso:
            conta.extrato.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.deposito(self._valor)
        if sucesso:
            conta.extrato.adicionar_transacao(self)


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


def filtrar_clientes(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def recuperar_conta(cliente):
    if not cliente.contas:
        print("Cliente não possui contas!")
        return None
    if len(cliente.contas) > 1:
        print("\nCliente possui mais de uma conta. Selecione uma conta:")
        for i, conta in enumerate(cliente.contas, start=1):
            print(f"{i} - Conta {conta.numero_conta}")
        indice = int(input("Digite o número da conta desejada: ")) - 1
        return cliente.contas[indice]
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)
    
    if cliente:
        valor = float(input("Informe o valor do depósito: "))
        if valor <= 0:
            print("Valor inválido!")
            return
        transacao = Deposito(valor)
        conta = recuperar_conta(cliente)
        if not conta:
            return
        
    else:
        print("Cliente não encontrado!")
        return

    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)
    
    if cliente:
        valor = float(input("Informe o valor do saque: "))
        if valor <= 0:
            print("Valor inválido!")
            return
        transacao = Saque(valor)
        conta = recuperar_conta(cliente)
        if not conta:
            return
    
    else:
        print("Cliente não encontrado!")
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)
    if cliente:
        conta = recuperar_conta(cliente)
        if not conta:
            return
        
        print("\n=============EXTRATO=============\n")
        transacoes = conta.extrato.transacoes
        extrato = ""
        if not transacoes:
            extrato = "Não foram realizadas operações\n"
        else:
            for transacao in transacoes:
                extrato+= f"{transacao['tipo']}: R$ {transacao['valor']:.2f} | Realizado: {transacao['data']} |\n"
        print(extrato)
        print(f"Saldo: {conta.saldo:.2f}")
        print("=================================\n")
    
    else:
        print("Cliente não encontrado!")


def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    clientes_filtrados = filtrar_clientes(cpf, clientes)
    if not clientes_filtrados:
        nome = input("Informe o nome do cliente: ")
        data_nascimento = input("Informe a data de nascimento do cliente (dd/mm/aaaa): ")
        endereco = input("Informe o endereço do cliente: ")
        cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
        clientes.append(cliente)
        print("\n === Cliente cadastrado com sucesso! ===")
    else:
        print("Cliente já cadastrado com esse cpf!")


def criar_conta(clientes, contas, numero_conta):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)
    
    if cliente:
        conta = ContaCorrente.nova_conta(numero_conta, cliente)
        contas.append(conta)
        cliente.contas.append(conta)
        
        print("\n === Conta criada com sucesso! ===")
    
    else:
        print("Cliente não encontrado!")
        return


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []

    while True:
        opcao = input(menu())

        if opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "s":
            sacar(clientes)
        elif opcao == "d":
            depositar(clientes)
        elif opcao == "u":
            criar_cliente(clientes)
        elif opcao == "c":
            numero_conta = len(contas) + 1
            criar_conta(clientes, contas, numero_conta)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "x":
            break
        else:
            print("=== Comando inválido. Tente novamente. ===")


main()
