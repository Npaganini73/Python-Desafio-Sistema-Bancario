from os import set_inheritable
from abc import ABC, abstractclassmethod, abstractproperty
import datetime
import textwrap

#Classe da Conta
class Conta:
    def __init__(self, numero, senha, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._senha = senha
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, numero, senha, cliente):
        return cls(numero, senha, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def agencia(self):
        return self._agencia

    @property
    def senha(self):
        return self._senha

    @property
    def numero(self):
        return self._numero
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        try:
            if valor > self._saldo:
                print("\n@@@ Saldo insuficiente! @@@")
                return False
            else:
                self._saldo -= valor
                print("\n=== Saque realizado com sucesso! ===")
                return True
            
        except ValueError:
            print("\n@@@ Valor inválido! @@@")
            return False

    def depositar(self, valor):
        try: 
            if valor <= 0:
                print("\n@@@ Valor inválido! @@@")
                return False
            else:
                self._saldo += valor
                print("\n=== Depósito realizado com sucesso! ===")
                return True

        except ValueError:
            print("\n@@@ Valor inválido! @@@")
            return False

#Subclasse conta corrente
class ContaCorrente(Conta):
    def __init__(self, numero, senha, cliente, limite=500, limite_saques=3):
        super().__init__(numero, senha, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len( 
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Limite de saque excedido! @@@")

        elif excedeu_saques:
            print("\n@@@ Limite de saques excedido! @@@")

        else:
            return super().sacar(valor)
        return False

        def __str__(self):
            return f"""\
                Agência:\t{self.agencia}
                C/C:\t\t{self.numero}
                Titular:\t{self.cliente.nome}
            """

#Classe histórico        
class Historico:
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
                "data": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

#Classe Cliente
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor


    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
  mensagem = f"""\n
  {" Banco do Julius ".center(36,"$")}




  {" MENU ".center(36,"=")}
  [d]\tDepositar
  [s]\tSacar
  [e]\tExtrato
  [nc]\tCriar Conta
  [nu]\tCriar Usuário
  [l]\tListar Contas
  [q]\tSair
  => """
  return input(textwrap.dedent(mensagem))

# Funções auxiliares
def filtrar_usuario(cpf, clientes):
    usuarios_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def recuperar_conta_cliente(cliente, agencia, numero_conta):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    for conta in cliente.contas:
        if conta.agencia == agencia and conta.numero == numero_conta:
            return conta
        else:
            print("\n@@@ Conta não encontrada! @@@")


def depositar(clientes):
    cpf = int(input("Informe o CPF do cliente: "))
    cliente = filtrar_usuario(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, depósito não realizado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))

    transacao = Deposito(valor)

    agencia = input("Informe a agência: ")
    numero_conta = int(input("Informe o número da conta: "))
    conta = recuperar_conta_cliente(cliente, agencia, numero_conta)

    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_usuario(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, saque não realizado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))

    transacao = Saque(valor)

    agencia = input("Informe a agência: ")
    numero_conta = int(input("Informe o número da conta: "))
    conta = recuperar_conta_cliente(cliente, agencia, numero_conta)

    if not conta:
        return
    
    senha = input("Informe a senha da conta: ")
    if senha != conta.senha:
        print("\n@@@ Senha incorreta! @@@")
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_usuario(cpf, clientes)
    
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    senha = input("Informe a senha da conta: ")
    if senha != conta.senha:
        print("\n@@@ Senha incorreta! @@@")
        return

    print("\n"+" EXTRATO ".center(100,"="))
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {cliente.conta.saldo:.2f}")
    print("=" * 100)

def criar_usuario(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_usuario(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Usuário criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_usuario(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, conta não criada! @@@")
        return

    senha = int(input("Defina uma senha para a sua conta: ")) 
    conta = ContaCorrente.nova_conta(numero=numero_conta, senha=senha, cliente=cliente)
    cliente.contas.append(conta)
    contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():    
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nc":
            numero_contas = len(contas) + 1
            criar_conta(numero_contas, clientes, contas)

        elif opcao == "nu":
            criar_usuario(clientes)

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")
        
        opcao = input("Deseja realizar outra operação? [s/n] ").lower()
        if opcao != "s":
            break

if __name__ == "__main__":
    main()
