# Sistema-Bancario-Python-POO-
🏦 Sistema Bancário Digital em Python
Um sistema bancário funcional que demonstra os principais conceitos de Programação Orientada a Objetos (POO) em Python.

📋 Funcionalidades
✅ Cadastro de clientes

✅ Criação de contas (Corrente e Poupança)

✅ Depósitos e saques

✅ Visualização de extrato

✅ Limite de cheque especial (Conta Corrente)

✅ Histórico de transações

🎓 Conceitos POO Demonstrados
Encapsulamento - Atributos protegidos (_)

Herança - Classe abstrata Conta com subclasses

Polimorfismo - Método sacar() diferentes por tipo de conta

Composição - Banco composto por Clientes e Contas

Exceções Customizadas - Tratamento de erros específicos

📂 Estrutura
text
├── entidades/
│   ├── cliente.py
│   └── conta.py
├── operacoes/
│   └── banco.py
├── utilitarios/
│   └── exceptions.py
└── main_projeto.py
🚀 Como Usar
Executar
bash
python main_projeto.py
Fluxo Básico
Adicionar cliente (nome + CPF)

Criar conta (tipo: corrente ou poupança)

Acessar conta e realizar operações

Exemplo
text
Menu: 1 (Adicionar Cliente)
Nome: João Silva
CPF: 12345678900

Menu: 2 (Criar Conta)
CPF: 12345678900
Tipo: corrente

Menu: 3 (Acessar Conta)
Número: 1
→ Depositar, Sacar, Ver Extrato
📚 Classes Principais
Classe	Descrição
Cliente	Armazena dados do cliente e suas contas
Conta	Classe abstrata base para tipos de conta
ContaCorrente	Conta com limite de cheque especial
ContaPoupanca	Conta sem limite
Banco	Gerencia clientes e contas
⚠️ Exceções
SaldoInsuficienteError - Saldo insuficiente para saque

ContaInexistenteError - Conta não encontrada

🔧 Requisitos
Python 3.8+

📝 Licença
Projeto educacional - Data Science Academy
