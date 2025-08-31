from src import ec2_service as svc

def main():
    print("1- Criar nova instância de máquina virtual\n" \
          "2- Listar todas as instâncias de máquinas virtuais\n" \
          "3- Iniciar uma instância de máquina virtual\n" \
          "4- Parar uma instância de máquina virtual\n" \
          "5- Terminar uma instância de máquina virtual\n" \
          "0- Sair\n")
    escolha = input("Escolha uma opção: ")
    if escolha == "1":
        nome = input("Nome da instância: ")
        svc.criar_instancia(nome)
    elif escolha == "2":
        svc.listar_instancias()
    elif escolha == "3":
        id = input("ID da instância: ")
        svc.iniciar_instancia(id)
    elif escolha == "4":
        id = input("ID da instância: ")
        svc.parar_instancia(id)
    elif escolha == "5":
        id = input("ID da instância: ")
        svc.terminar_instancia(id)
    elif escolha == "0":
        print("Saindo...")
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
