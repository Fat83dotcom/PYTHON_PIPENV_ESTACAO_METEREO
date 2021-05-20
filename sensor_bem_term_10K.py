import serial
import time
import csv
import matplotlib.pyplot as plt

set_porta = '/dev/ttyACM0'
while set_porta:
    try:
        arduino = serial.Serial(set_porta, 9600)
        arduino.reset_input_buffer()
        break
    except serial.serialutil.SerialException:
        set_porta = input('Digite a porta serial em que o Arduino está conectada: ')


def data():
    data = time.strftime('%d %b %Y %H:%M:%S', time.localtime())
    return data


def plot_umidade(ux, uy, inicio):
    file = f'/home/fernando/Área de Trabalho/UMIDADE/Umidade{inicio}.pdf'
    plt.title(f'-> Inicio: {inicio}\n-> Termino: {data()}\nGráfico Umidade')
    plt.xlabel('Tempo em segundos.')
    plt.ylabel('Umidade Relativa do Ar %')
    plt.plot(ux, uy)
    plt.savefig(file)
    plt.clf()


def plot_pressao(px, py, inicio):
    file = f'/home/fernando/Área de Trabalho/PRESSAO/Pressao{inicio}.pdf'
    plt.title(f'-> Inicio: {inicio}\n-> Termino: {data()}\nGráfico Pressão')
    plt.xlabel('Tempo em segundos.')
    plt.ylabel('Pressão Atmosferica em hPa')
    plt.plot(px, py)
    plt.savefig(file)
    plt.clf()


def plot_temp1(t1x, t1y, inicio):
    file = f'/home/fernando/Área de Trabalho/TEMP1/Temperatura_Interna{inicio}.pdf'
    plt.title(f'-> Inicio: {inicio}\n-> Termino: {data()}\nGráfico Temp Interna')
    plt.xlabel('Tempo em segundos.')
    plt.ylabel('Temperatura em °C')
    plt.plot(t1x, t1y)
    plt.savefig(file)
    plt.clf()


def plot_temp2(t2x, t2y, inicio):
    file = f'/home/fernando/Área de Trabalho/TEMP2/Temperatura_Externa{inicio}.pdf'
    plt.title(f'-> Inicio: {inicio}\n-> Termino: {data()}\nGráfico Temp Externa')
    plt.xlabel('Tempo em segundos.')
    plt.ylabel('Temperatura em °C')
    plt.plot(t2x, t2y)
    plt.savefig(file)
    plt.clf()


class ConvertTempo:
    def __init__(self, hora=None, minuto=None, segundo=None):
        self.hora = hora
        self.minuto = minuto
        self.segundo = segundo

    def convert_hr_segundo(self):
        conv_hr_sec = self.hora * 3600
        return conv_hr_sec

    def convert_min_segundo(self):
        conv_min_sec = self.minuto * 60
        return conv_min_sec

    def soma_tempo(self):
        h = self.hora
        m = self.minuto
        s = self.segundo
        soma = ConvertTempo(hora=h, minuto=m, segundo=s)
        soma = soma.convert_hr_segundo() + soma.convert_min_segundo()
        soma += self.segundo
        return soma


def flagEntry():
    opition = ''
    cont = 0
    tentativa = 5
    while opition == '' and cont < tentativa:
        print(f'{cont  + 1}ª tentativa... {tentativa - (cont + 1)} restantes.')
        opition = input(
            'Deseja definir a frequencia dos gráficos ? ').upper()
        if opition[0] == 'S':
            call = call_tempo()
            if call:
                print(f'Tempo definido em {call} segundos.')
                return int(call)
            else:
                cont += 1
                opition = ''
                continue
        else:
            print('Tempo padrão definido, 10 minutos.')
            flag_entry = 600
            return flag_entry
    print('O tempo padrão foi definito: 10 minutos.')
    flag_entry = 600
    return flag_entry


def call_tempo():
    print('Intervalo máximo: 3 horas.')
    print('Digite as horas, minutos e segundo para saida de gráficos: ')
    hora = input('Digite o tempo em horas: ')
    minuto = input('Digite o tempo em minutos: ')
    segundo = input('Digite o tempo em segundos: ')
    try:
        if 0 <= int(minuto) < 60 and 0 <= int(segundo) < 60:
            flag_entry = ConvertTempo(int(hora), int(minuto), int(segundo))
            flag_entry = flag_entry.soma_tempo()
            return int(flag_entry)
        else:
            print('Digite os minutos e segundos entre 0 e 59.')
            return None
    except ValueError:
        print('error')
        print('Digite somente numeros.\n')
        return None


def main():
    cont3 = 0
    while 1:
        if cont3 == 0:
            print(f'Inicio: --> {data()} <--')
            tempo_graf = int(flagEntry())
        else:
            print(f'Parcial {cont3} --> {data()} <--')
        inicio = data()
        ux = []
        uy = []
        px = []
        py = []
        t1x = []
        t1y = []
        t2x = []
        t2y = []
        d1 = {
            'u': '',
            'p': '',
            '1': '',
            '2': '',
        }

        cont2 = 0
        while cont2 < tempo_graf:
            cont = 0
            while cont < 8:
                dado = str(arduino.readline())
                dado = dado[2:-5]
                try:
                    if dado[0] == 'u':
                        d1['u'] = dado[1:].strip()
                    if dado[0] == 'p':
                        d1['p'] = dado[1:].strip()
                    if dado[0] == '1':
                        d1['1'] = dado[1:].strip()
                    if dado[0] == '2':
                        d1['2'] = dado[1:].strip()
                except IndexError:
                    continue
                cont += 1
            with open('log_bme280.csv', 'a+', newline='', encoding='utf-8') as file:
                try:
                    w = csv.writer(file)
                    w.writerow([data(), d1['u'], d1['p'], d1['1'], d1['2']])
                    ux.append(cont2)
                    uy.append(float(d1['u']))
                    px.append(cont2)
                    py.append(float(d1['p']))
                    t1x.append(cont2)
                    t1y.append(float(d1['1']))
                    t2x.append(cont2)
                    t2y.append(float(d1['2']))
                    cont2 += 1
                    time.sleep(1)
                except ValueError:
                    print('error')
                    continue
        plot_umidade(ux, uy, inicio)
        plot_pressao(px, py, inicio)
        plot_temp1(t1x, t1y, inicio)
        plot_temp2(t2x, t2y, inicio)
        cont3 += 1


while 1:
    print(f'-> Inicio {data()}')
    main()
    print(f'-> Termino {data()}')
    print('-----------------------')
arduino.close()
