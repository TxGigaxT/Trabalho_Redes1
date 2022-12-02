# This is a sample Python script.
import socket
import time
import os
import struct
from threading import Thread
import matplotlib.pyplot as plt


# Press Shift+F10 to execute it or replace it with your code.   47,68
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def TesteDownUp(protc, alvo, PLOT):
    own_id = os.getpid() & 0xFFFF
    cabecalho = struct.pack("!BBHHH", 8, 0 , 0, own_id, 1)
    padrao = 1440
    # int8 x[1440]
    a = 1440 * 'a'
    data = bytes(a.encode('utf-8'))
    packet = cabecalho + data
    M = 0
    latenciaAtual = 0
    start = time.time()
    while (time.time() - start)<10:
        try:
            #inicio = time.time_ns()
            protc.sendto(packet, (alvo, 1))
            #fim = (time.time_ns - inicio)
            #latenciaAtual+=fim
            M+=1
            #print(".")
        except:
            #print("Deu erro")
            pass
    vazao = (((M*len(packet))/(time.time()-start))*8)
    if(vazao<1024):
        print(vazao,"b/s")
    if(vazao>1024):
        vazao/=1024.0
        print(vazao, "Kb/s")
    if(vazao > 1024):
        vazao /= 1024.0
        print(vazao, "Mb/s")
    if (vazao > 1024):
        vazao /= 1024.0
        print(vazao, "Gb/s")
    #print("Bytes por segundo: ", vazao)
    #if(latenciaAtual )
def TesteVazao(protc, alvo, port, qnt, PLOT): #TENHO A MENOR IDEIA DO QUE PASSOU PELA MINHA CABEÇA
    own_id = os.getpid() & 0xFFFF
    header = struct.pack("!BBHHH", 8, 0, 0, own_id, 1)
    print(header)
    # padBytes = []
    # startVal = 0x41
    # for i in range(startVal, startVal + (58)):
    #     padBytes += [(i & 0x7f)]  # Keep chars in the 0-255 range
    INIT = 1024
    data = bytearray(INIT)
    print(data)
    packet = header + data
    # print(packet)
    x = []
    div = 0.95
    multi = 1.05
    print("ICMP:")
    while qnt > 0:
        #if (INIT > 1480):
         #   INIT = 1480
         #  data = bytearray(INIT)
         #   packet = header + data
        try:
            packet = header + data
            inicio = time.time_ns()
            # print("1")
            protc.sendto(packet, (alvo, 1))
            # print("2")
            # rec = protc.recvfrom(1024)
            # print("3")
            fim = (time.time_ns() - inicio)
            # print("4")
            fim = (fim * 0.000001)
            # print(rec[0])
            print("envio de ", len(packet), "bytes, bytes, em %.2f" % fim, "ms")
            qnt -= 1
            x.append(INIT)
            INIT = int(INIT * multi)
            if (div < 1):
                div = float(div * 1.001)
            if (div >= 1):
                div = float(div * 0.998)
            multi = float(multi * 1.001)
            # if(INIT > 1480):
            #     INIT = 1480
            data = bytearray(INIT)
        except:
            print("pacote muito grande, reduzindo...")
            INIT = int(INIT * div)
            if (multi > 1):
                multi = float(0.999 * multi)
            #div = float(div * 0.998)
            data = bytes(INIT)
            qnt -= 1
            # break
    if (PLOT == 1):
        plt.rcParams["figure.figsize"] = [10, 5]
        plt.rcParams["figure.autolayout"] = True
        plt.title("Speed_Teste")
        plt.xlabel("Solicitações")
        plt.ylabel("Mb")
        plt.grid(color='k', linestyle='-', linewidth=0.5)
        plt.plot(x, 'bo-', color='blue', markersize=5)
        plt.show()
    else:
        return x
    print("entrou teste vazao")


def TTCP(protc, alvo, port, M, PLOT):
    # try:
    #     protc.connect((alvo, port))
    # except:
    #     print("Não foi possivel fazer a conexão TCP")
    #     exit()'
    solicitacao = "GET / HTTP/1.1\nHost: %s\n\n\n" % alvo
    x = []
    print("TCP:")
    while M > 0:
        try:
            protc.connect((alvo, port))
            inicio = time.time_ns()
            protc.send(solicitacao.encode())
            pag = str(protc.recv(2048))
            fim = (time.time_ns() - inicio)
            fim = (fim * 0.000001)
            x.append(fim)
            try:
                print("envio de", len(solicitacao.encode('utf-8')), "bytes, recebido", len(pag.encode('utf-8')),
                      "bytes no tempo de %.2f" % fim, "ms")
            except:
                pass
            M -= 1
            protc.shutdown(socket.SHUT_RDWR)
            protc.close()
            protc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            print("Erro ao se conectar ao host")
            M -= 1
            # break
    if (PLOT == 1):
        plt.rcParams["figure.figsize"] = [10, 5]
        plt.rcParams["figure.autolayout"] = True
        plt.title("TCP latencia")
        plt.xlabel("Solicitações")
        plt.ylabel("Latencia (ms)")
        plt.grid(color='k', linestyle='-', linewidth=0.5)
        plt.plot(x, 'bo-', color='red', markersize=5)
        plt.show()
    else:
        return x


def ICMP(protc, alvo, port, qnt, PLOT):
    own_id = os.getpid() & 0xFFFF
    header = struct.pack("!BBHHH", 8, 0, 0, own_id, 1)
    print(header)
    padBytes = []
    startVal = 0x42
    for i in range(startVal, startVal + (55)):
        padBytes += [(i & 0x7f)]  # Keep chars in the 0-255 range
    data = bytes(padBytes)
    print(data)
    packet = header + data
    # print(packet)
    x = []
    print("ICMP:")
    while qnt > 0:
        try:
            inicio = time.time_ns()
            # print("1")
            protc.sendto(packet, (alvo, 1))
            # print("2")
            # rec = protc.recvfrom(1024)
            # print("3")
            fim = (time.time_ns() - inicio)
            # print("4")
            fim = (fim * 0.000001)
            # print(rec[0])
            print("envio de ", len(packet), "bytes, em %.2f" % fim, "ms")
            qnt -= 1
            x.append(fim)
        except:
            print("Erro ao enviar pacote ao host")
            qnt -= 1
            # break
    if (PLOT == 1):
        plt.rcParams["figure.figsize"] = [10, 5]
        plt.rcParams["figure.autolayout"] = True
        plt.title("ICMP latencia")
        plt.xlabel("Solicitações")
        plt.ylabel("Latencia (ms)")
        plt.grid(color='k', linestyle='-', linewidth=0.5)
        plt.plot(x, 'bo-', color='blue', markersize=5)
        plt.show()
    else:
        return x


def Latencia(TCP, UDP):
    hostAlvo = input("Digite o host alvo para o teste de latencia: ")
    porto = int(input("Digite o porto alvo do host: "))
    quant = int(input("Digite a quantidade de resultados que deseja receber: "))
    Protocolo = input("Digite o protocolo desejado: ICMP, TCP ou AMBOS: ")
    if (Protocolo == "TCP"):
        PLOT = int(input("Deseja plotar o grafico ?\n1 - Sim\n2 - Não\n"))
        TTCP(TCP, hostAlvo, porto, quant, PLOT)
        # TcpThread = Thread(target=TTCP(TCP, hostAlvo, porto, quant))

        # try:
        #     TCP.connect((hostAlvo, porto))
        #     inicio = time.time_ns()
        #     TCP.send(b"GET / HTTP/2\nHost: www.google.com\n\n\n")
        #     TCP.recv(1024)
        #     fim = (time.time_ns() - inicio)
        #     print(fim * 0.000001)
        # except:
        #     print("Erro ao se conectar ao host")
    elif (Protocolo == "ICMP"):
        PLOT = int(input("Deseja plotar o grafico ?\n1 - Sim\n2 - Não\n"))
        ICMP(UDP, hostAlvo, porto, quant, PLOT)
        # icmpThread = Thread(target=ICMP(UDP, hostAlvo, porto, quant))

        # own_id = os.getpid() & 0xFFFF
        # header = struct.pack("!BBHHH", 8, 0, 0, own_id, 0)
        # padBytes = []
        # startVal = 0x42
        # for i in range(startVal, startVal + (55)):
        #     padBytes += [(i & 0xff)]  # Keep chars in the 0-255 range
        # data = bytes(padBytes)
        # packet = header + data
        # try:
        #     inicio = time.time_ns()
        #     UDP.sendto(packet, (hostAlvo, porto))
        #     UDP.recvfrom(1024)
        #     fim = (time.time_ns() - inicio)
        #     print(fim * 0.000001)
        # except:
        #     print("Erro ao se conectar ao host")
    elif (Protocolo == "AMBOS"):
        PLOT = 0
        x = TTCP(TCP, hostAlvo, porto, quant, PLOT)
        y = ICMP(UDP, hostAlvo, porto, quant, PLOT)
        plt.rcParams["figure.figsize"] = [10, 5]
        plt.rcParams["figure.autolayout"] = True
        plt.title("ICMP & TCP latencia")
        plt.xlabel("Solicitações")
        plt.ylabel("Latencia (ms)")
        plt.grid(color='k', linestyle='-', linewidth=0.5)
        plt.plot(x, 'bo-', color='red', markersize=5)
        plt.plot(y, 'bo-', color='blue', markersize=5)
        plt.legend(['TCP', 'ICMP'])
        plt.show()
        # quant = int(input("Digite a quantidade de resultados que deseja receber: "))
        # TcpThread = Thread(target=TTCP(TCP, hostAlvo, porto,quant))
        # icmpThread = Thread(target=ICMP(UDP,hostAlvo,porto,quant))


def LarguraDeBanda():
    print("entrou teste largura de banda")


def menu(TCP, UDP):
    while True:
        opcao = int(input(
            "############################\n1 - Teste de vazao\n2 - Latência\n3 - Largura de banda\n0 - Sair\n############################\n"))
        match opcao:
            case 1:
                alvo = str(input("Digite o alvo a ser enviado os pacotes: "))
                TesteVazao(UDP, alvo, 1, 1000, 1)
            case 2:
                Latencia(TCP, UDP)
            case 3:
                alvo = str(input("Digite o alvo a ser enviado os pacotes: "))
                TesteDownUp(UDP,alvo,0)
                #LarguraDeBanda()
            case 0:
                exit()
            case _:
                print("Opcao invalida...")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    clienteTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clienteUDP_ICMP = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    menu(clienteTCP, clienteUDP_ICMP)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
