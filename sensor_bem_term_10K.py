import serial
import time
import csv
import matplotlib.pyplot as plt
from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
from confidentials import meu_email, minha_senha

set_porta = '/dev/ttyACM0'

while set_porta:
    try:
        arduino = serial.Serial(set_porta, 9600)
        arduino.reset_input_buffer()
        break
    except serial.serialutil.SerialException:
        set_porta = input('Digite a porta serial em que o Arduino está conectado: ')
print(f'O Arduino está na porta: {set_porta}')


class EmailThread(Thread):
    def __init__(self, inicio):
        super().__init__()
        self.inicio = inicio

    def run(self):
        msg = MIMEMultipart()
        msg['from'] = 'Fernando Mendes'
        msg['to'] = meu_email
        msg['subject'] = f'Monitoramento Estação Metereologica Fat83dotcom {data()}'
        corpo = MIMEText(f'Gráficos, {data()}')
        msg.attach(corpo)
        try:
            umidade = f'/home/fernando/Área de Trabalho/UMIDADE/Umidade{self.inicio}.pdf'
            pressao = f'/home/fernando/Área de Trabalho/PRESSAO/Pressao{self.inicio}.pdf'
            tmp1 = f'/home/fernando/Área de Trabalho/TEMP1/Temperatura_Interna{self.inicio}.pdf'
            temp2 = f'/home/fernando/Área de Trabalho/TEMP2/Temperatura_Externa{self.inicio}.pdf'
            # log = '/home/fernando/PYTHON_PIPENV_ESTACAO_METEREO/log_bme280.csv'

            with open(umidade, 'rb') as pdf_U:
                anexo_U = MIMEApplication(pdf_U.read(), _subtype='pdf')
                pdf_U.close()
                anexo_U.add_header('Conteudo', umidade)
                msg.attach(anexo_U)

            with open(pressao, 'rb') as pdf_P:
                anexo_P = MIMEApplication(pdf_P.read(), _subtype='pdf')
                pdf_P.close()
                anexo_P.add_header('Conteudo', pressao)
                msg.attach(anexo_P)

            with open(tmp1, 'rb') as pdf_T1:
                anexo_T1 = MIMEApplication(pdf_T1.read(), _subtype='pdf')
                pdf_T1.close()
                anexo_T1.add_header('Conteudo', tmp1)
                msg.attach(anexo_T1)

            with open(temp2, 'rb') as pdf_T2:
                anexo_T2 = MIMEApplication(pdf_T2.read(), _subtype='pdf')
                pdf_T2.close()
                anexo_T2.add_header('Conteudo', temp2)
                msg.attach(anexo_T2)

            # with open(log, 'rb') as csv_file:
            #     anexo_csv = MIMEApplication(csv_file.read(), _subtype='csv')
            #     csv_file.close()
            #     anexo_csv.add_header('Conteudo', log)
            #     msg.attach(anexo_csv)

            with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(meu_email, minha_senha)
                smtp.send_message(msg)
                print('Email enviado com sucesso.')
        except FileNotFoundError:
            print('Email não enviado.')
            return None


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


def flagEntry():
    opition = ''
    cont = 0
    tentativa = 5
    while opition == '' and cont < tentativa:
        print(f'{cont  + 1}ª tentativa... {tentativa - (cont + 1)} restantes.')
        opition = input('Deseja definir a frequencia dos gráficos ?[S/N]: ').upper()
        if opition[0] == 'S':
            call = call_tempo()
            if call:
                print('Em Execução ....')
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
            if flag_entry > 10800:
                flag_entry = 10800
                print(f'Tempo definido em {flag_entry} segundos/ {flag_entry/3600} horas.')
                return int(flag_entry)
            else:
                print(f'Tempo definido em {flag_entry} segundos/ {flag_entry/3600} horas.')
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
                        d1['u'] = float(dado[1:].strip())
                    if dado[0] == 'p':
                        d1['p'] = float(dado[1:].strip())
                    if dado[0] == '1':
                        d1['1'] = float(dado[1:].strip())
                    if dado[0] == '2':
                        d1['2'] = float(dado[1:].strip())
                except (ValueError, IndexError):
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
        emaail = EmailThread(inicio)
        emaail.start()


while 1:
    main()
