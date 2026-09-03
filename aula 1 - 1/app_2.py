
print('Sistema de notas de alunos')

#Cadastrar aluno
nome1 = input('Digite seu nome 1:')
nome2 = input('Digite seu nome 2:')
nome3 = input('Digite seu nome 3:')

#Lista de nomes
lista_nomes = []
lista_nomes.append (nome1)
lista_nomes.append (nome2)
lista_nomes.append (nome3)

print(lista_nomes)

nota1= float(input(f'Nota 1 - {nome1}'))
nota2= float(input(f'Nota 2 - {nome2}'))
nota3= float(input(f'Nota 3 - {nome3}'))

media = (nota1 + nota2 + nota3) /3

print('Media dos alunos', media)

enter = input('Digite enter para sair')

