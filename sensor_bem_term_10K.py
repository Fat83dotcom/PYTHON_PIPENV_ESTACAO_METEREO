import serial
import time
import csv
import matplotlib.pyplot as plt


arduino = serial.Serial('/dev/ttyACM0', 9600)


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


def main():
    ux = []
    uy = []
    px = []
    py = []
    t1x = []
    t1y = []
    t2x = []
    t2y = []
    inicio = data()
    d1 = {
        'u': '',
        'p': '',
        '1': '',
        '2': '',
    }
    
    cont2 = 0
    while cont2 < 3600:
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


while True:
    print(f'-> Inicio {data()}')
    main()
    print(f'-> Termino {data()}')
    print('-----------------------')
arduino.close()
