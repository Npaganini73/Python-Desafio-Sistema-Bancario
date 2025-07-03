import textwrap

def menu():
  mensagem = f"""\n
  {" Banco do Julius ".center(36,"$")}




  {" MENU ".center(36,"=")}
  [d]\tDepositar     
  [s]\tSacar         
  [e]\tExtrato       
  [c]\tCriar Conta
  [u]\tCriar Usuário  
  [l]\tListar Contas 
  [q]\tSair               
  => """
  return input(textwrap.dedent(mensagem))


def depositar(saldo, valor, extrato,/):
  if valor > 0:
    saldo += valor
    extrato += f"Depósito:\t\tR$ {valor:.2f}\n"
    print("\n === Depósito realizado com sucesso! ===")
  else:
    print("\n@@@ Falha na operação! O valor informado é inválido. @@@")
  return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
  excedeu_saldo = valor > saldo
  excedeu_limite = valor > limite
  excedeu_saques = numero_saques >= limite_saques

  if excedeu_saldo:
    print("\n@@@ Falha na operação! Você não tem saldo suficiente. @@@")

  elif excedeu_limite:
    print("\n@@@ Falha na operação! O valor do saque excede o limite. @@@")

  elif excedeu_saques:
    print("\n@@@ Falha na operação! Número máximo de saques excedido. @@@")

  else:
    saldo -= valor
    extrato += f"Saque:\t\tR$ {valor:.2f}\n"
    numero_saques += 1
    print("\n === Saque realizado com sucesso! ===")
  return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
  print("\n"+" EXTRATO ".center(36,"="))
  print("Não foram realizadas movimentações." if not extrato else extrato)
  print(f"\nSaldo:\t\tR$ {saldo:.2f}")
  print(36*"=")

def criar_usuario(usuarios):
  cpf = input("Informe o CPF (somente número): ")
  usuario = filtrar_usuario(cpf, usuarios)

  if usuario:
    print("\n@@@ Já existe usuário com esse CPF! @@@")
    return

  nome = input("Informe o nome completo: ")
  data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
  endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

  usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

  print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
  usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
  return usuarios_filtrados[0] if usuarios_filtrados else None

def filtrar_conta(agencia, numero_conta, contas):
  contas_filtradas = [conta for conta in contas if conta["agencia"] == agencia and conta["numero_conta"] == numero_conta]
  return contas_filtradas[0] if contas_filtradas else None

def criar_conta(agencia, numero_conta, usuarios):
  cpf = input("Informe o CPF do usuário: ")
  usuario = filtrar_usuario(cpf, usuarios)

  if usuario:
    senha = input("Informe a senha para a conta: ")
    conta = {"agencia": agencia,
             "numero_conta": numero_conta,
             "usuario": usuario,
             "saldo": 0,
             "limite": 500,
             "extrato": "",
             "numero_saques": 0,
             "senha": senha}
    print("\n=== Conta criada com sucesso! ===")
    return conta

  print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

def listar_contas(contas):
  for conta in contas:
    linha = f"""\
      Agência:\t{conta['agencia']}
      C/C:\t\t{conta['numero_conta']}
      Titular:\t{conta['usuario']['nome']}
    """ 
    print("=" * 100)
    print(textwrap.dedent(linha))

def main():
  LIMITE_SAQUES = 3
  AGENCIA = "0001"

  saldo = 0
  limite = 500
  extrato = ""
  numero_saques = 0
  usuarios = []
  contas = []

  while True:
    opcao = menu()

    if opcao == "d":
      agencia = input("Informe a agência: ")
      numero_conta = int(input("Informe o número da conta: "))
      conta = filtrar_conta(agencia, numero_conta, contas)

      if conta:
        valor = float(input("Informe o valor do depósito: "))
        conta["saldo"], conta["extrato"] = depositar(conta["saldo"], valor, conta["extrato"])
      else:
        print("Conta não encontrada.")
      
      opcao = input("Deseja realizar outra operação? [s/n] ").lower()
      if opcao != "s":
        break

    elif opcao == "s":
      agencia = input("Informe a agência: ")
      numero_conta = input("Informe o número da conta: ")
      conta = filtrar_conta(agencia, numero_conta, contas)

      if conta:
        senha = input("Informe a senha da conta: ")
        if senha == conta["senha"]:  
          valor = float(input("Informe o valor do saque: "))
          conta["saldo"], conta["extrato"], conta["numero_saques"] = sacar(
            saldo=conta["saldo"],
            valor=valor,
            extrato=conta["extrato"],
            limite=conta["limite"],
            numero_saques=conta["numero_saques"],
            limite_saques=LIMITE_SAQUES
            )
          print("\n=== Saque realizado com sucesso! ===")
        else:
          print("\n@@@ Senha incorreta. Saque não realizado. @@@")
      else:
        print("Conta não encontrada.")

      opcao = input("Deseja realizar outra operação? [s/n] ").lower()
      if opcao != "s":
        break

    elif opcao == "e":
      agencia = input("Informe a agência: ")
      numero_conta = input("Informe o número da conta: ")
      conta = filtrar_conta(agencia, numero_conta, contas)
      
      if conta:
        exibir_extrato(conta["saldo"], extrato=conta["extrato"])
      else:
        print("Conta não encontrada.")
      
      opcao = input("Deseja realizar outra operação? [s/n] ").lower()
      if opcao != "s":
        break
    
    elif opcao == "c":
      numero_conta = len(contas) + 1
      conta = criar_conta(AGENCIA, numero_conta, usuarios)
      contas.append(conta)
      
      opcao = input("Deseja realizar outra operação? [s/n] ").lower()  
      if opcao != "s":
        break

    elif opcao == "u":
      criar_usuario(usuarios)

      opcao = input("Deseja realizar outra operação? [s/n] ").lower()
      if opcao != "s":
        break 

    elif opcao == "l":
      listar_contas(contas)

      opcao = input("Deseja realizar outra operação? [s/n] ").lower()
      if opcao != "s":
        break

    elif opcao == "q":
      break

    else:
      print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
