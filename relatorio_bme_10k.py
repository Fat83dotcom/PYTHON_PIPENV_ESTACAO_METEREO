# import matplotlib.pyplot as plt
# import sys
from datetime import date


class Periodo:

    def data_inicio(self, dia=str, mes=str, ano=str, hora=str, minuto=str, segundo=str):
        data_ini = f'{dia} {mes} {ano} {hora}:{minuto}:{segundo}'
        return data_ini

    def data_termino(self, dia=str, mes=str, ano=str, hora=str, minuto=str, segundo=str):
        data_ter = f'{dia} {mes} {ano} {hora}:{minuto}:{segundo}'
        return data_ter



def entry_inicio():
    meses_ano = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    retorno = Periodo()
    entrada = False
    while not entrada:
        print('Preencha os campos com a data de início da busca.')
        print(f'Para os meses digite desta maneira: {meses_ano}.')
        dia = ''
        while not dia:
            dia = input('Digite o dia(DD): ')
            if dia.isnumeric() and len(dia) == 2 and 0 < int(dia) <= 31:
                break
            else:
                print('Digite somente dois números entre 1 e 31.')
                dia = ''
                continue
        mes = ''
        while not mes:
            mes = input('Digite o mês(MMM): ')
            if mes.isalpha() and len(mes) == 3:
                for mes1 in meses_ano:
                    if mes1 == mes:
                        break
                else:
                    print('O que você digitou não corresponde a um mes do ano.')
                    mes = ''
            else:
                print('Digite somente 3 letras conforme a lista acima.')
                mes = ''
                continue

        ano = ''
        while not ano:
            data_ano = date.today().year
            ano = input('Digite o ano(AAAA): ')
            if ano.isnumeric() and len(ano) == 4:
                if 2010 <= int(ano) <= data_ano:
                    break
                else:
                    print(f'Digite um ano entre 2010 e {data_ano}')
                    ano = ''
                    continue
            else:
                print('Digite somente 4 números.')
                ano = ''
                continue
        hora = ''
        while not hora:
            hora = input('Digite a hora(HH): ')
            if hora.isnumeric() and len(hora) == 2 and 0 <= int(hora) <= 23:
                break
            else:
                print('Digite somente 2 números entre 00 e 23.')
                hora = ''
                continue
        minuto = ''
        while not minuto:
            minuto = input('Digite os minutos(MM): ')
            if minuto.isnumeric() and len(minuto) == 2 and 0 <= int(minuto) <= 59:
                break
            else:
                print('Digite somente 2 números entre 00 e 59.')
                minuto = ''
                continue
        segundo = ''
        while not segundo:
            segundo = input('Digite os segundos(SS): ')
            if segundo.isnumeric() and len(segundo) == 2 and 0 <= int(segundo) <= 59:
                break
            else:
                print('Digite somente 2 números entre 00 e 59.')
                segundo = ''
                continue
        entrada = True
        return retorno.data_inicio(dia, mes, ano, hora, minuto, segundo)


def entry_termino():
    meses_ano = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    retorno = Periodo()
    entrada = False
    while not entrada:
        print('Preencha os campos com a data de término da busca.')
        print(f'Para os meses digite desta maneira: {meses_ano}.')
        dia = ''
        while not dia:
            dia = input('Digite o dia(DD): ')
            if dia.isnumeric() and len(dia) == 2 and 0 < int(dia) <= 31:
                break
            else:
                print('Digite somente dois números entre 1 e 31.')
                dia = ''
                continue
        mes = ''
        while not mes:
            mes = input('Digite o mês(MMM): ')
            if mes.isalpha() and len(mes) == 3:
                for mes1 in meses_ano:
                    if mes1 == mes:
                        break
                else:
                    print('O que você digitou não corresponde a um mes do ano.')
                    mes = ''
            else:
                print('Digite somente 3 letras conforme a lista acima.')
                mes = ''
                continue

        ano = ''
        while not ano:
            data_ano = date.today().year
            ano = input('Digite o ano(AAAA): ')
            if ano.isnumeric() and len(ano) == 4:
                if 2010 <= int(ano) <= data_ano:
                    break
                else:
                    print(f'Digite um ano entre 2010 e {data_ano}')
                    ano = ''
                    continue
            else:
                print('Digite somente 4 números.')
                ano = ''
                continue
        hora = ''
        while not hora:
            hora = input('Digite a hora(HH): ')
            if hora.isnumeric() and len(hora) == 2 and 0 <= int(hora) <= 23:
                break
            else:
                print('Digite somente 2 números entre 00 e 23.')
                hora = ''
                continue
        minuto = ''
        while not minuto:
            minuto = input('Digite os minutos(MM): ')
            if minuto.isnumeric() and len(minuto) == 2 and 0 <= int(minuto) <= 59:
                break
            else:
                print('Digite somente 2 números entre 00 e 59.')
                minuto = ''
                continue
        segundo = ''
        while not segundo:
            segundo = input('Digite os segundos(SS): ')
            if segundo.isnumeric() and len(segundo) == 2 and 0 <= int(segundo) <= 59:
                break
            else:
                print('Digite somente 2 números entre 00 e 59.')
                segundo = ''
                continue
        entrada = True
        return retorno.data_termino(dia, mes, ano, hora, minuto, segundo)


with open('log_bme280.csv', 'r', encoding='utf-8', newline='') as file:
    file.seek(0)
    lista = [x.split(',') for x in file.readlines()]
    lista0 = [x[0] for x in lista]
    # lista1 = [x[1] for x in lista]
    # lista2 = [x[2] for x in lista]
    # lista3 = [x[3] for x in lista]
    # lista4 = [x[4].splitlines() for x in lista]
    # print(lista0[-1][:2])
    # print(sys.getsizeof(lista))
    # print(next(lista))
    if '23 May 2021 11:25:57' in lista0:
        valor1 = '23 May 2021 11:25:57'
        valor2 = '26 May 2021 18:09:17'
        pos1 = lista0.index(valor1)
        pos2 = lista0.index(valor2)
        diferenca = pos2 - pos1
        print(lista[pos1][1])
        print(pos1)
        print(pos2)
        print(diferenca)
    for dados in lista[pos1:pos2]:
        print(dados)
