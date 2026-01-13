# 🏦 Sistema Bancário em Python

Um projeto educacional de sistema bancário com POO, testes automatizados e persistência de dados em JSON.

## 📋 Funcionalidades

✅ Gerenciar clientes e contas  
✅ Depositar, sacar e transferir  
✅ Histórico de transações  
✅ Dados persistidos entre execuções  
✅ Testes automatizados (23 testes)

## 📈 Evolução do Projeto

### Base (Data Science Academy)

- Classes: Cliente, Conta, ContaCorrente, ContaPoupanca, Banco
- Operações básicas: depositar, sacar, extrato
- Exceções: SaldoInsuficienteError, ContaInexistenteError
- CLI básica

### Melhorias Implementadas

- ✅ Encapsulamento com @property
- ✅ Método buscar_cliente() centralizado
- ✅ Exceção ClienteInexistenteError
- ✅ Transferência entre contas
- ✅ Suite de 23 testes com pytest
- ✅ Persistência em JSON (dados.json)
- ✅ Padronização de pastas (PEP 8)

## 🚀 Como usar

### Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/Taylordossantos/Sistema-Banc-rio---POO-.git
cd Sistema-Banc-rio---POO-

# (Opcional) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install pytest


###Executar o sistema

execute o arquivo main_projeto.py

Você verá o menu principal:


---Projeto - Sistema Bancário Digital ---

1. Adicionar Cliente
2. Criar Conta
3. Acessar Conta
4. Transferência entre Contas
5. Sair

Escolha uma opção:


'''Rodar os testes'''
Para rodar os testes, execute: pytest no terminal


📁 Estrutura do projeto

Sistema-Banc-rio---POO-/
├── entidades/
├── operacoes/
├── utilitarios/
├── tests/
├── main_projeto.py
└── dados.json


🛠️ Tecnologias
Python 3.8+

POO (Herança, Polimorfismo, Encapsulamento)

pytest

JSON

👨‍💻 Autor
Taylor dos Santos
 LinkedIn: www.linkedin.com/in/taylor-dos-santos | GitHub: https://github.com/Taylordossantos

Última atualização: 13 de janeiro de 2026


```
