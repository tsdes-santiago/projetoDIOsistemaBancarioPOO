#Desafio Sistema Bancário com Classes
from datetime import datetime
from abc import ABC, abstractclassmethod, abstractproperty

#################################
#Definição as classes 
#################################

#___________________

class Cliente:
    def __init__(self, id_c):
        self.id = id_c
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append()

class PessoaFisica(Cliente):
    def __init__(self, nome, data, id_c, endereco):
        super().__init__(id_c)
        self.nome = nome
        self.id = id_c
        self.data = data
        self.endereco = endereco

class PessoaJuridica(Cliente):
    def __init__(self, nome, data, id, endereco):
        super().__init__(id_c)
        self.nome = nome
        self.id = id_c
        self.data = data
        self.endereco = endereco

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

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
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print('Operação falhou. Saldo insuficiente.')

        elif valor > 0:
            self._saldo -= valor
            print('Saque realizado com sucesso.')
            return True

        else:
            print('Operação falhou. Valor informado inválido')
        
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f'Foram depositados R$ {valor:.2f} na sua conta.')
        else:
            print('Valor invalido. Cancelando operação.')
            return False

        return True 

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes 
            if transacao['tipo'] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print('Operação falhou. O valor excede o limite.')
        
        elif excedeu_saques:
            print('Operação falhou. Você excedeu o limite de saques diários.')

        else:
            return super().sacar(valor)
        
        return False

    def __str__(self):
        return f"""\
            Agencia:\t {self.agencia}
            C/C: \t \t {self.numero}
            Titular:\t {self.cliente.nome}
        """

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
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
        }
        )

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

# Definições para operação do sistema pelo usuário
#---------------------
def criar_cliente(clientes):
    id_c = input("informe o CPF/CNPJ:")
    cliente = filtrar_cliente(id_c, clientes)
    
    if cliente:
        print("Cliente já cadastrado.")
        return 

    nome = input("Informe o nome completo: ")
    data = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/UF): ")

    cliente = PessoaFisica(nome=nome, data = data, id_c = id_c, endereco=endereco)

    clientes.append(cliente)

    print("Cliente cadastrado com sucesso!")

def filtrar_cliente(id_c, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.id == id_c]

    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta.")
        return
    # ADICIONAR METODO PARA SELECIONAR CONTAS
    return cliente.contas[0]

def depositar(clientes):
    id_c = input("informe o CPF/CNPJ: ")
    cliente = filtrar_cliente(id_c, clientes)
    
    if not cliente:
        print("Cliente não encontrado.")
        return 
    
    valor = float(input("Informe o valor do depósito: \t"))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    id_c = input("Informe o CPF/CNPJ: \t")
    cliente = filtrar_cliente(id_c, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return 
    
    valor = float(input("Informe o valor do saque: \t"))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    id_c = input("Informe o CPF/CNPJ: \t")
    cliente = filtrar_cliente(id_c, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return 

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return
    
    print('#'*10, 'EXTRATO', '#'*10)
    transacoes = conta.historico.transacoes

    extrato = ""

    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"{transacao['tipo']}: \n \t R$ {transacao['valor']:.2f} \n"

    print(extrato)
    print(f"Saldo: \n \t R$ {conta.saldo:.2f}")
    print('#'*40)

def criar_conta(numero_conta, clientes, contas):
    id_c = input("Informe o CPF/CNPJ:")
    cliente = filtrar_cliente(id_c, clientes)

    if not cliente:
        print("Cliente não encontrado. Cadastre o novo cliente.")
        return 
    
    conta = ContaCorrente.nova_conta(cliente = cliente, numero = numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print('Conta criada com sucesso!')

def listar_contas(contas):
    for conta in contas:
        print("#"*40)
        print(str(conta))


#Função para cliente entrar com os dados e movimentar a conta 
#___________________________________

def operar_conta(clientes, contas):
    
    #Menu para movimentar a conta
    menu_conta = """
    
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

    =>"""

    #Recebe a opção selecionada pelo cliente e executa a ação
    while True:

        opcao = input(menu_conta)

        if opcao == 'd':
            print('Deposito')
            
            depositar(clientes)

        elif opcao == 's':

            print('Saque')
            sacar(clientes)
        
        elif opcao == 'e':
            exibir_extrato(clientes)

        elif opcao == 'q':
            break

        else:
            print("Operação invalida, por favor selecione nomavente a operação desejada")
    return None

#---------------------
#Começo execução
#Menu para cadastrar usuário ou acessar conta
def menu():
    menu = """

    [m] Movimentar Conta
    [c] Cadastrar Cliente
    [ac] Adicionar Conta
    [lc] Listar Contas
    [q] Sair
    =>"""
    return input(menu)

#Exibe o menu e espera a resposta do usuário

def main():
        
    clientes = []
    contas = []

    while True:
        opcao = menu()
        
        if opcao == 'm':
            operar_conta(clientes, contas)
        
        elif opcao == 'c':
            print('Cadastrar cliente')
            criar_cliente(clientes)
            
        elif opcao == 'ac':
            numero_conta = len(contas)+1
            criar_conta(numero_conta, clientes, contas)
        
        elif opcao == 'lc':
           listar_contas(contas) 
        
        elif opcao == 'q':
            break
        
        else:
            print("Operação invalida, por favor selecione novamente a operação desejada")

main()