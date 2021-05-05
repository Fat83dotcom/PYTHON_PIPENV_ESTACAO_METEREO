import serial
import time
import csv


arduino = serial.Serial('/dev/ttyACM0', 9600)


def get_umi():
    time.sleep(1.5)
    arduino.write(0xA)
    r = str(arduino.readline())
    return r

def data():
    data = time.strftime('%d %b %Y %H:%M:%S', time.localtime())
    return data

def entrada_dados(umi, temp, press, temp10k):
    with open('log_bme280.csv', 'a+', newline='', encoding='utf-8') as file:
        w = csv.writer(file)
        w.writerow([data(), umi[2:-5], temp[2:-5], press[2:-5], temp10k[2:-5]])
        time.sleep(1)



while True:
    # umi = str(arduino.readline())
    # temp = str(arduino.readline())
    # press = str(arduino.readline())
    # temp10k = str(arduino.readline())
    # entrada_dados(umi, temp, press, temp10k)
    # print(umi[2:-5])
    # print(temp[2:-5])
    # print(press[2:-5])
    # print(temp10k[2:-5])
    
    time.sleep(0.1)
    r = str(arduino.readline())
    print(r)
    
    print('-----------------------')
    
    
arduino.close()
