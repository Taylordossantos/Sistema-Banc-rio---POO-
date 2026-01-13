
import json
import os
from datetime import datetime
from entidades.cliente import Cliente
from entidades.conta import ContaCorrente, ContaPoupanca


class PersistenciaBanco:
    """Classe responsável por salvar e carregar dados do banco em JSON"""
    
    def __init__(self, arquivo="dados.json"):
        """
        Inicializa o gerenciador de persistência
        
        Args:
            arquivo: Nome do arquivo JSON para salvar dados
        """
        self.arquivo = arquivo
    
    def salvar_banco(self, banco):
        """
        Salva todos os clientes e contas do banco em um arquivo JSON
        
        Args:
            banco: Objeto Banco a ser salvo
        """
        try:
            dados = {
                "nome_banco": banco.nome,
                "data_salva": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "clientes": [],
                "contas": []
            }
            
            # Salva os clientes
            for cpf, cliente in banco._clientes.items():
                dados["clientes"].append({
                    "nome": cliente.nome,
                    "cpf": cliente.cpf
                })
            
            # Salva as contas
            for numero, conta in banco._contas.items():
                tipo_conta = "corrente" if isinstance(conta, ContaCorrente) else "poupanca"
                
                dados["contas"].append({
                    "numero": numero,
                    "tipo": tipo_conta,
                    "cpf_cliente": conta.cliente.cpf,
                    "saldo": conta.saldo,
                    "limite": conta.limite if isinstance(conta, ContaCorrente) else None,
                    "historico": [
                        {
                            "data": data.strftime("%d/%m/%Y %H:%M:%S"),
                            "transacao": transacao
                        }
                        for data, transacao in conta.historico
                    ]
                })
            
            # Escreve no arquivo JSON
            with open(self.arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            
            print(f"Dados salvos com sucesso em '{self.arquivo}'")
            return True
        
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            return False
    
    def carregar_banco(self, banco):
        """
        Carrega todos os clientes e contas do arquivo JSON para o banco
        
        Args:
            banco: Objeto Banco onde os dados serão carregados
            
        Returns:
            bool: True se carregou com sucesso, False caso contrário
        """
        try:
            # Verifica se o arquivo existe
            if not os.path.exists(self.arquivo):
                print(f"Arquivo '{self.arquivo}' não encontrado. Iniciando com banco vazio.")
                return False
            
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            # Carrega os clientes primeiro
            for cliente_data in dados.get("clientes", []):
                banco.adicionar_cliente(cliente_data["nome"], cliente_data["cpf"])
            
            # Carrega as contas
            for conta_data in dados.get("contas", []):
                cpf_cliente = conta_data["cpf_cliente"]
                tipo_conta = conta_data["tipo"]
                saldo = conta_data["saldo"]
                limite = conta_data.get("limite")
                
                # Busca o cliente
                cliente = banco.buscar_cliente(cpf_cliente)
                
                # Cria a conta
                if tipo_conta == "corrente":
                    conta = ContaCorrente(conta_data["numero"], cliente, limite)
                else:
                    conta = ContaPoupanca(conta_data["numero"], cliente)
                
                # Define o saldo (sem registrar no histórico)
                conta._saldo = saldo
                
                # Adiciona o histórico
                for transacao_data in conta_data.get("historico", []):
                    data_str = transacao_data["data"]
                    # Converte string de volta para datetime (simulado)
                    transacao = transacao_data["transacao"]
                    # Aqui simplesmente adicionamos ao histórico
                    conta._historico.append((data_str, transacao))
                
                # Adiciona a conta ao banco
                banco._contas[conta.numero] = conta
                cliente.adicionar_conta(conta)
            
            print(f"Dados carregados com sucesso de '{self.arquivo}'")
            return True
        
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return False
