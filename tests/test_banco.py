# tests/test_banco.py

# tests/test_banco.py

import pytest
import sys
from pathlib import Path

# Adiciona a raiz do projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Agora importa
from entidades.cliente import Cliente
from entidades.conta import ContaCorrente, ContaPoupanca
from operacoes.banco import Banco
from utilitarios.exceptions import SaldoInsuficienteError, ContaInexistenteError, ClienteInexistenteError



class TestBanco:
    """Testes para a classe Banco"""
    
    def setup_method(self):
        """Executa antes de cada teste - cria um banco novo"""
        self.banco = Banco("Banco de Testes")
    
    # ===== TESTES DE CLIENTE =====
    
    def test_adicionar_cliente(self):
        """Testa se consegue adicionar um cliente"""
        cliente = self.banco.adicionar_cliente("João Silva", "12345678900")
        
        assert cliente.nome == "João Silva"
        assert cliente.cpf == "12345678900"
    
    def test_adicionar_cliente_duplicado(self):
        """Testa se não consegue adicionar cliente com CPF duplicado"""
        self.banco.adicionar_cliente("João Silva", "12345678900")
        cliente_duplicado = self.banco.adicionar_cliente("Outro João", "12345678900")
        
        # Deve retornar o cliente já existente, não criar novo
        assert cliente_duplicado.nome == "João Silva"
    
    def test_buscar_cliente_existente(self):
        """Testa se consegue buscar um cliente existente"""
        self.banco.adicionar_cliente("Maria Santos", "98765432100")
        cliente = self.banco.buscar_cliente("98765432100")
        
        assert cliente.nome == "Maria Santos"
    
    def test_buscar_cliente_inexistente(self):
        """Testa se lança exceção ao buscar cliente inexistente"""
        with pytest.raises(ClienteInexistenteError):
            self.banco.buscar_cliente("99999999999")
    
    # ===== TESTES DE CONTA =====
    
    def test_criar_conta_corrente(self):
        """Testa se consegue criar uma conta corrente"""
        cliente = self.banco.adicionar_cliente("Pedro Costa", "11122233344")
        conta = self.banco.criar_conta(cliente, "corrente")
        
        assert isinstance(conta, ContaCorrente)
        assert conta.saldo == 0.0
    
    def test_criar_conta_poupanca(self):
        """Testa se consegue criar uma conta poupança"""
        cliente = self.banco.adicionar_cliente("Ana Silva", "55566677788")
        conta = self.banco.criar_conta(cliente, "poupanca")
        
        assert isinstance(conta, ContaPoupanca)
        assert conta.saldo == 0.0
    
    def test_criar_conta_tipo_invalido(self):
        """Testa se retorna None ao criar conta com tipo inválido"""
        cliente = self.banco.adicionar_cliente("Lucas", "44455566677")
        conta = self.banco.criar_conta(cliente, "investimento")
        
        assert conta is None
    
    def test_buscar_conta_existente(self):
        """Testa se consegue buscar uma conta existente"""
        cliente = self.banco.adicionar_cliente("Carla", "33344455566")
        conta = self.banco.criar_conta(cliente, "corrente")
        
        conta_encontrada = self.banco.buscar_conta(conta.numero)
        assert conta_encontrada == conta
    
    def test_buscar_conta_inexistente(self):
        """Testa se lança exceção ao buscar conta inexistente"""
        with pytest.raises(ContaInexistenteError):
            self.banco.buscar_conta(999)
    
    # ===== TESTES DE DEPÓSITO =====
    
    def test_depositar_valor_positivo(self):
        """Testa se consegue depositar valor positivo"""
        cliente = self.banco.adicionar_cliente("Bruno", "22233344455")
        conta = self.banco.criar_conta(cliente, "corrente")
        
        conta.depositar(1000)
        assert conta.saldo == 1000
    
    def test_depositar_valor_negativo(self):
        """Testa se não consegue depositar valor negativo"""
        cliente = self.banco.adicionar_cliente("Fernanda", "66677788899")
        conta = self.banco.criar_conta(cliente, "poupanca")
        
        conta.depositar(-500)
        assert conta.saldo == 0  # Saldo não muda
    
    def test_depositar_valor_zero(self):
        """Testa se não consegue depositar zero"""
        cliente = self.banco.adicionar_cliente("Ricardo", "99988877766")
        conta = self.banco.criar_conta(cliente, "corrente")
        
        conta.depositar(0)
        assert conta.saldo == 0  # Saldo não muda
    
    # ===== TESTES DE SAQUE =====
    
    def test_sacar_conta_corrente_com_saldo(self):
        """Testa saque em conta corrente com saldo suficiente"""
        cliente = self.banco.adicionar_cliente("Gustavo", "11133355577")
        conta = self.banco.criar_conta(cliente, "corrente")
        
        conta.depositar(1000)
        conta.sacar(300)
        assert conta.saldo == 700
    
    def test_sacar_conta_corrente_com_limite(self):
        """Testa saque em conta corrente usando limite de cheque especial"""
        cliente = self.banco.adicionar_cliente("Helena", "22244466688")
        conta = self.banco.criar_conta(cliente, "corrente")  # limite padrão: 500
        
        conta.depositar(300)
        conta.sacar(700)  # Usa 300 do saldo + 400 do limite
        assert conta.saldo == -400
    
    def test_sacar_conta_corrente_saldo_insuficiente(self):
        """Testa saque em conta corrente com saldo e limite insuficientes"""
        cliente = self.banco.adicionar_cliente("Isadora", "33355577799")
        conta = self.banco.criar_conta(cliente, "corrente")  # limite: 500
        
        conta.depositar(300)
        with pytest.raises(SaldoInsuficienteError):
            conta.sacar(1000)  # Tenta sacar mais que saldo + limite
    
    def test_sacar_conta_poupanca_com_saldo(self):
        """Testa saque em conta poupança com saldo suficiente"""
        cliente = self.banco.adicionar_cliente("Julio", "44466688900")
        conta = self.banco.criar_conta(cliente, "poupanca")
        
        conta.depositar(500)
        conta.sacar(200)
        assert conta.saldo == 300
    
    def test_sacar_conta_poupanca_saldo_insuficiente(self):
        """Testa saque em conta poupança com saldo insuficiente"""
        cliente = self.banco.adicionar_cliente("Karen", "55577799911")
        conta = self.banco.criar_conta(cliente, "poupanca")
        
        conta.depositar(100)
        with pytest.raises(SaldoInsuficienteError):
            conta.sacar(500)
    
    # ===== TESTES DE TRANSFERÊNCIA =====
    
    def test_transferir_com_sucesso(self):
        """Testa transferência bem-sucedida entre contas"""
        cliente1 = self.banco.adicionar_cliente("Xavier", "66688800022")
        cliente2 = self.banco.adicionar_cliente("Yasmin", "77799911133")
        
        conta1 = self.banco.criar_conta(cliente1, "corrente")
        conta2 = self.banco.criar_conta(cliente2, "poupanca")
        
        conta1.depositar(1000)
        self.banco.transferir(conta1.numero, conta2.numero, 500)
        
        assert conta1.saldo == 500
        assert conta2.saldo == 500
    
    def test_transferir_conta_inexistente(self):
        """Testa transferência para conta inexistente"""
        cliente = self.banco.adicionar_cliente("Zoe", "88800022244")
        conta = self.banco.criar_conta(cliente, "corrente")
        conta.depositar(1000)
        
        with pytest.raises(ContaInexistenteError):
            self.banco.transferir(conta.numero, 999, 500)
    
    def test_transferir_saldo_insuficiente(self):
        """Testa transferência com saldo insuficiente"""
        cliente1 = self.banco.adicionar_cliente("Alice", "99911133355")
        cliente2 = self.banco.adicionar_cliente("Bob", "10122244466")
        
        conta1 = self.banco.criar_conta(cliente1, "poupanca")
        conta2 = self.banco.criar_conta(cliente2, "corrente")
        
        conta1.depositar(100)
        with pytest.raises(SaldoInsuficienteError):
            self.banco.transferir(conta1.numero, conta2.numero, 500)
    
    def test_transferir_valor_negativo(self):
        """Testa transferência com valor negativo"""
        cliente1 = self.banco.adicionar_cliente("Carol", "20133355577")
        cliente2 = self.banco.adicionar_cliente("David", "30144466688")
        
        conta1 = self.banco.criar_conta(cliente1, "corrente")
        conta2 = self.banco.criar_conta(cliente2, "corrente")
        
        conta1.depositar(1000)
        self.banco.transferir(conta1.numero, conta2.numero, -500)
        
        # Saldo não muda com valor negativo
        assert conta1.saldo == 1000
        assert conta2.saldo == 0
    
    # ===== TESTES DE HISTÓRICO =====
    
    def test_historico_deposito(self):
        """Testa se o histórico registra depósitos"""
        cliente = self.banco.adicionar_cliente("Eva", "40155577799")
        conta = self.banco.criar_conta(cliente, "corrente")
        
        conta.depositar(500)
        assert len(conta.historico) == 1
        assert "Depósito" in conta.historico[0][1]
    
    def test_historico_saque(self):
        """Testa se o histórico registra saques"""
        cliente = self.banco.adicionar_cliente("Frank", "50166688900")
        conta = self.banco.criar_conta(cliente, "corrente")
        
        conta.depositar(1000)
        conta.sacar(300)
        assert len(conta.historico) == 2
        assert "Saque" in conta.historico[1][1]
