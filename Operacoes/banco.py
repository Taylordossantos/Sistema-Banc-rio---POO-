# Módulo que define a classe principal do Banco, que gerencia clientes e contas.

# Importa a classe Cliente
from entidades.cliente import Cliente
# Importa a classe base Conta e suas subclasses (Corrente e Poupança)
from entidades.conta import Conta, ContaCorrente, ContaPoupanca
# Importa a exceção personalizada para conta inexistente
from utilitarios.exceptions import ContaInexistenteError, ClienteInexistenteError


# Define a classe Banco
class Banco:

    """
    Classe que gerencia as operações do banco.
    Demonstra Composição, pois "tem" clientes e contas.
    """

    # Construtor da classe Banco
    def __init__(self, nome: str):

        # Nome do banco
        self.nome = nome
        
        # Dicionário de clientes (chave: CPF, valor: objeto Cliente)
        self._clientes = {}
        
        # Dicionário de contas (chave: número da conta, valor: objeto Conta)
        self._contas = {}

    # Método para adicionar um novo cliente ao banco
    def adicionar_cliente(self, nome: str, cpf: str) -> Cliente:
        
        """Cria e adiciona um novo cliente ao banco."""
        
        # Verifica se já existe cliente com o mesmo CPF
        if cpf in self._clientes:
            print("Erro: Cliente com este CPF já cadastrado.")
            return self._clientes[cpf]
        
        # Cria objeto Cliente e adiciona ao dicionário
        novo_cliente = Cliente(nome, cpf)
        self._clientes[cpf] = novo_cliente

        print(f"Cliente {nome} adicionado com sucesso!")
        
        return novo_cliente

    # Método para criar uma conta para um cliente
    def criar_conta(self, cliente: Cliente, tipo: str) -> Conta:
        
        """Cria uma nova conta para um cliente existente."""
        
        # Número da nova conta será baseado no total de contas + 1
        numero_conta = Conta.get_total_contas() + 1
        
        # Cria conta corrente se o tipo informado for "corrente"
        if tipo.lower() == 'corrente':
            nova_conta = ContaCorrente(numero_conta, cliente)
        
        # Cria conta poupança se o tipo informado for "poupanca"
        elif tipo.lower() == 'poupanca':
            nova_conta = ContaPoupanca(numero_conta, cliente)
        
        # Caso o tipo não seja válido
        else:
            print("Tipo de conta inválido. Escolha 'corrente' ou 'poupanca'.")
            return None

        # Adiciona a conta ao dicionário de contas
        self._contas[numero_conta] = nova_conta
        
        # Associa a conta ao cliente
        cliente.adicionar_conta(nova_conta)
        print(f"Conta {tipo} nº {numero_conta} criada para o cliente {cliente.nome}.")

        return nova_conta

    # Método para buscar uma conta pelo número
    def buscar_conta(self, numero_conta: int) -> Conta:
        
        """Busca uma conta pelo seu número."""
        
        # Tenta recuperar a conta do dicionário
        conta = self._contas.get(numero_conta)
        
        # Se não encontrar, lança exceção personalizada
        if not conta:
            raise ContaInexistenteError(numero_conta)
        return conta
    
    # Método para buscar um cliente pelo CPF
    def buscar_cliente(self, cpf: str) -> Cliente:
        """Busca um cliente pelo seu CPF."""
        cliente = self._clientes.get(cpf)
        if not cliente:
            raise ClienteInexistenteError(cpf)
        return cliente
    
    # Método para realizar transferência entre contas
    def transferir(self, numero_conta_origem: int, numero_conta_destino: int, valor: float) -> None:
    
        """ Realiza uma transferência de dinheiro entre duas contas.
        
        Args:
            numero_conta_origem: Número da conta que envia o dinheiro
            numero_conta_destino: Número da conta que recebe o dinheiro
            valor: Valor a ser transferido
        
        Raises:
            ContaInexistenteError: Se alguma conta não existir
            SaldoInsuficienteError: Se a conta de origem não tiver saldo"""
      # Busca as contas (irá lançar exceção se não existirem)
        conta_origem = self.buscar_conta(numero_conta_origem)
        conta_destino = self.buscar_conta(numero_conta_destino)
        
        # Valida o valor
        if valor <= 0:
            print("Valor de transferência inválido. Digite um valor maior que zero.")
            return
        
        # Realiza o saque da conta de origem (pode lançar SaldoInsuficienteError)
        conta_origem.sacar(valor)
        
        # Realiza o depósito na conta de destino
        conta_destino.depositar(valor)
        
        # Mensagem de sucesso
        print(f"Transferência de R${valor:.2f} realizada com sucesso!")
        print(f"De: Conta {numero_conta_origem} ({conta_origem.cliente.nome})")
        print(f"Para: Conta {numero_conta_destino} ({conta_destino.cliente.nome})")
