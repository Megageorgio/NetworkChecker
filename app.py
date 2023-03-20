import csv
import socket
from pythonping import ping
import time
import os.path


def check_ip(hostname, ip, ports):
    ping_response = ping(ip)
    output = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    output += ' | ' + hostname
    output += ' | ' + ip
    output += ' | ' + str(ping_response.packet_loss)
    output += ' | ' + str(ping_response.rtt_max_ms) + ' ms'
    output += ' | ' + ('ok' if ping_response.packet_loss == 0 else 'timeout')
    print(output)

    if ping_response.packet_loss == 1:
        return

    for port in ports:
        if not port.isdigit():
            print(port + ' не является числом')
            return
        parsed_port = int(port)
        if parsed_port > 65535:
            print('число ' + port + ' больше 65535 и не может являться номером порта ')
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        port_response = sock.connect_ex((ip, parsed_port))

        print('port ' + port + ': ' + ('unknown' if port_response == 0 else 'opened'))


def run(path):
    with open(path, mode='r') as csvfile:
        if not os.path.isfile(path):
            print('Некорректный путь')
            return

        reader = csv.DictReader(csvfile, delimiter=';')
        if len(reader.fieldnames) != 2:
            print('Некорректный формат файла')
            return

        print('time | host | ip | packet loss | rtt max ms | state')
        for row in reader:
            try:
                if not row['Host']:
                    print('Не указан адрес в строке ' + str(reader.line_num))
                    continue
                try:
                    hostname, _, ip_list = socket.gethostbyname_ex(row['Host'])
                except IOError:
                    print('Адрес ' + row['Host'] + ' некорректный')
                    continue
                ports = list(filter(str.strip, row['Ports'].split(",")))
                for ip in ip_list:
                    check_ip(hostname, ip, ports)

            except Exception as e:
                print('Ошибка при попытке обработать строку ' + str(reader.line_num) + ': ' + str(e))
