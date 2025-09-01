from src import ec2_service as svc

def main():
    while True:
        print("1- Criar nova instância de máquina virtual\n" \
            "2- Listar todas as instâncias de máquinas virtuais\n" \
            "3- Iniciar uma instância de máquina virtual\n" \
            "4 - Rebootar uma instância de máquina virtual\n" \
            "5 - Hibernar uma instância de máquina virtual\n" \
            "6- Parar uma instância de máquina virtual\n" \
            "7- Terminar uma instância de máquina virtual\n" \
            "8- Atualizar uma instância de máquina virtual\n"
            "0- Sair\n")
        escolha = input("Escolha uma opção: ")
        if escolha == "1":
            nome = input("Nome da instância: ")
            svc.criar_instancia(nome)
        elif escolha == "2":
            svc.listar_instancias()
        elif escolha == "3":
            id = input("ID da instância: ")
            svc.start(id)
        elif escolha == "4":
            id = input("ID da instância: ")
            svc.reboot(id)
        elif escolha == "5":
            id = input("ID da instância: ")
            svc.hibernate(id)
        elif escolha == "6":
            id = input("ID da instância: ")
            svc.stop(id)
        elif escolha == "7":
            id = input("ID da instância: ")
            svc.terminar_instancia(id)
        elif escolha == "8":
            instance_id = input("Digite o ID da instância que deseja atualizar: ").strip()
            print("O que deseja fazer?")
            print("1- Adicionar tag")
            print("2- Remover tag")
            print("3- Alterar tipo da instância")
            
            escolha = input("Escolha uma opção: ").strip()
            
            if escolha == "1":
                key = input("Digite a chave da tag: ").strip()
                value = input("Digite o valor da tag: ").strip()
                svc.add_tag(instance_id, key, value)
                print(f"Tag adicionada: {key}={value}")
                
            elif escolha == "2":
                key = input("Digite a chave da tag que deseja remover: ").strip()
                value = input("Digite o valor da tag (Enter para remover todas as tags com essa chave): ").strip() or None
                svc.remove_tag(instance_id, key, value)
                print(f"Tag removida: {key}={value if value else 'todas'}")
                
            elif escolha == "3":
                novo_tipo = input("Digite o novo tipo da instância (Ex: t2.micro, t3.medium): ").strip()
                svc.change_instance_type(instance_id, novo_tipo)
                print(f"Tipo da instância alterado para {novo_tipo}")
                
            else:
                print("Opção inválida!")
        elif escolha == "0":
            print("Saindo...")
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
