# 💸 Banco do Julius

Um sistema bancário simples em Python, baseado em terminal, que simula operações como depósito, saque, criação de contas, e exibição de extrato. Criado com foco educacional, o sistema reforça conceitos como funções, estrutura condicional, listas e dicionários.

---

## 📋 Funcionalidades

* **\[d] Depositar:** Realiza depósitos em uma conta bancária existente.
* **\[s] Sacar:** Permite saques com controle de limite e quantidade máxima de saques por dia.
* **\[e] Extrato:** Exibe o histórico de transações e saldo atual da conta.
* **\[c] Criar Conta:** Cadastra uma nova conta bancária vinculada a um usuário.
* **\[u] Criar Usuário:** Registra um novo usuário com CPF e dados pessoais.
* **\[l] Listar Contas:** Lista todas as contas registradas no sistema.
* **\[q] Sair:** Encerra o sistema.

---

## 🧠 Como funciona

### Menu principal

Exibe as opções disponíveis para o usuário com navegação baseada em letras (`d`, `s`, `e`, etc). Após cada operação, é possível escolher continuar ou sair.

### Controle de contas

Cada conta contém:

* **Agência:** Padrão `"0001"`
* **Número da conta:** Gerado automaticamente com base na quantidade de contas já criadas
* **Usuário vinculado**
* **Senha de acesso**
* **Saldo**
* **Limite de saque**
* **Histórico de transações (extrato)**
* **Número de saques realizados**

---

## 📁 Estrutura do Código

| Função              | Descrição                                                       |
| ------------------- | --------------------------------------------------------------- |
| `menu()`            | Exibe o menu principal                                          |
| `depositar()`       | Realiza o depósito se o valor for válido                        |
| `sacar()`           | Realiza o saque se não houver violação de limite ou saldo       |
| `exibir_extrato()`  | Exibe o extrato da conta                                        |
| `criar_usuario()`   | Cadastra um novo usuário                                        |
| `filtrar_usuario()` | Busca um usuário existente por CPF                              |
| `criar_conta()`     | Cadastra uma nova conta para um usuário já existente            |
| `filtrar_conta()`   | Busca uma conta com base na agência e número                    |
| `listar_contas()`   | Lista todas as contas registradas                               |
| `main()`            | Função principal que gerencia o loop de interação com o sistema |

---

## 🚀 Como executar

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/seu-usuario/Python-Desafio-Sistema-Bancario.git
   cd Python-Desafio-Sistema-Bancario
   ```

2. **Execute o script**:

   ```bash
   python3 desafio_sistema_bancario.py
   ```

> 💡 Certifique-se de estar usando Python 3.6 ou superior.

---

## ⚙️ Requisitos

* Python 3.6+
* Terminal/Prompt de Comando

---

## 🎯 Objetivo educacional

Este projeto foi desenvolvido com fins didáticos, ideal para quem está aprendendo os conceitos fundamentais de programação em Python, como:

* Funções com parâmetros posicionais e nomeados
* Estrutura de decisão e repetição
* Manipulação de listas e dicionários
* Fluxos de entrada/saída no terminal

---

## ✍️ Autor

Desenvolvido por **Júlio César**.

