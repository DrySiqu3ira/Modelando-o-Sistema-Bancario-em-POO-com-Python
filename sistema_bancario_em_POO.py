from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        if conta in self.contas:
            conta.adicionar_transacao(transacao)
        else:
            print("Erro: Conta não encontrada para este cliente.")

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor > 0 and valor <= self._saldo:
            saldo_anterior = self._saldo
            self._saldo -= valor
            self._historico.adicionar_transacao(Saque(valor, saldo_anterior, self._saldo))
            print("Saque realizado com sucesso!")
            return True
        print("Erro: Saldo insuficiente ou valor inválido!")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            self._historico.adicionar_transacao(Deposito(valor))
            print("Depósito realizado com sucesso!")
            return True
        print("Erro: Valor inválido para depósito!")
        return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._saques_realizados = 0

    def sacar(self, valor):
        if valor > self._limite:
            print("Erro: Valor excede o limite de saque!")
            return False
        if self._saques_realizados >= self._limite_saques:
            print("Erro: Limite de saques diários atingido!")
            return False
        if super().sacar(valor):
            self._saques_realizados += 1
            return True
        return False

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'saldo_anterior': getattr(transacao, 'saldo_anterior', None),
            'saldo_atual': getattr(transacao, 'saldo_atual', None),
            'data': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        })

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor, saldo_anterior, saldo_atual):
        self._valor = valor
        self.saldo_anterior = saldo_anterior
        self.saldo_atual = saldo_atual

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        return conta.sacar(self._valor)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        return conta.depositar(self._valor)

# Funções do sistema

def criar_cliente():
    nome = input("Nome: ")
    data_nascimento = input("Data de Nascimento (DD/MM/AAAA): ")
    cpf = input("CPF: ")
    endereco = input("Endereço: ")
    return PessoaFisica(nome, data_nascimento, cpf, endereco)

def criar_conta(clientes, numero_conta):
    cpf = input("Digite o CPF do cliente: ")
    cliente = next((c for c in clientes if c.cpf == cpf), None)
    if cliente:
        conta = ContaCorrente(numero_conta, cliente)
        cliente.adicionar_conta(conta)
        print("Conta criada com sucesso!")
        return conta
    print("Erro: Cliente não encontrado!")
    return None

def listar_contas(clientes):
    for cliente in clientes:
        for conta in cliente.contas:
            print(f"Agência: {conta.agencia}, Conta: {conta.numero}, Saldo: R${conta.saldo:.2f}")

def menu():
    clientes = []
    contas = []
    numero_conta = 1
    
    while True:
        print("\n1 - Criar Cliente\n2 - Criar Conta\n3 - Depositar\n4 - Sacar\n5 - Extrato\n6 - Listar Contas\n0 - Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            clientes.append(criar_cliente())
        elif opcao == '2':
            conta = criar_conta(clientes, numero_conta)
            if conta:
                contas.append(conta)
                numero_conta += 1
        elif opcao == '3':
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)
            if cliente and cliente.contas:
                valor = float(input("Valor do depósito: "))
                cliente.contas[0].depositar(valor)
            else:
                print("Erro: Cliente ou conta não encontrados!")
        elif opcao == '4':
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)
            if cliente and cliente.contas:
                valor = float(input("Valor do saque: "))
                cliente.contas[0].sacar(valor)
            else:
                print("Erro: Cliente ou conta não encontrados!")
        elif opcao == '5':
            listar_contas(clientes)
        elif opcao == '6':
            listar_contas(clientes)
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()
