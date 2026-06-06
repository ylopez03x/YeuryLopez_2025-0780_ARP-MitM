# ARP MitM Attack
**Autor:** Yeury Lopez de Leon  
**Matrícula:** 2025-0780  
**Materia:** Seguridad de Redes  
**Fecha:** 31/05/2026

[Ver demostración en YouTube](https://youtu.be/-dqFc0IUiS0)

---

## Objetivo del Laboratorio
Demostrar el ataque Man in the Middle mediante ARP Spoofing en 
un entorno controlado, evidenciando cómo un atacante puede 
interceptar el tráfico entre dos dispositivos de la red.

---

## Objetivo del Script
Enviar respuestas ARP falsas a PC1 y R1 para posicionarse como 
intermediario entre ambos, interceptando todo su tráfico.

### Parámetros usados
| Parámetro | Valor | Descripción |
|---|---|---|
| VICTIM_IP | 172.25.78.20 | IP de PC1 (víctima) |
| GATEWAY_IP | 172.25.78.1 | IP de R1 (gateway) |
| INTERFAZ | eth0 | Interfaz de Kali |
| INTERVALO | 2 seg | Frecuencia de envío ARP falso |

### Requisitos para utilizar la herramienta
- Kali Linux con Python 3
- Librería Scapy instalada
- Permisos root
- IP Forwarding habilitado
- Misma red que las víctimas

---

## Documentación del funcionamiento del Script

**1. Obtención de MACs reales**  
La función `get_mac()` envía un ARP Request broadcast para 
obtener las MACs reales de PC1 y R1.

**2. Envío de ARP falsos**  
La función `spoof_arp()` envía ARP Replies falsos:
- A PC1: "La MAC del gateway soy yo"
- A R1: "La MAC de PC1 soy yo"

**3. IP Forwarding**  
Se habilita IP Forwarding para que el tráfico interceptado 
siga fluyendo normalmente sin que las víctimas lo noten.

**4. Ataque continuo**  
El script envía ARP falsos cada 2 segundos para mantener 
las tablas ARP envenenadas.

---

## Documentación de la Red

### Topología
> <img width="705" height="617" alt="image" src="https://github.com/user-attachments/assets/c8da2b7c-a1b8-460e-bc2d-1c72adf2c0bd" />


### Direccionamiento IP
| Dispositivo | Interfaz | Dirección IP | Máscara | Rol |
|---|---|---|---|---|
| R1 | fa0/0 | 172.25.78.1 | /24 | Gateway + DHCP Server |
| SW1 | VLAN1 | 172.25.78.2 | /24 | Switch Core - Root Bridge |
| SW2 | VLAN1 | 172.25.78.3 | /24 | Switch Acceso |
| Kali | eth0 | 172.25.78.10 | /24 | Atacante |
| PC1 | eth0 | 172.25.78.20 | /24 | Víctima 1 (estática) |
| PC2 | eth0 | 172.25.78.21 | /24 | Víctima 2 (DHCP) |

### Conexiones
| Dispositivo A | Interfaz | Dispositivo B | Interfaz |
|---|---|---|---|
| R1 | fa0/0 | SW1 | e0/0 |
| SW1 | e0/1 | Kali | eth0 |
| SW1 | e0/2 | PC1 | eth0 |
| SW1 | e0/3 | SW2 | e0/0 |
| SW2 | e0/1 | PC2 | eth0 |

### Herramientas utilizadas
- EVE-NG Community Edition
- Cisco IOL L2 v15.1 (SW1, SW2)
- Cisco IOS 3725 v12.4 Dynamips (R1)
- Kali Linux 2024
- Python 3 + Scapy
- VPCS (PC1, PC2)

---

## Capturas de Pantalla

### Tabla ARP de PC1 antes del ataque
> <img width="975" height="597" alt="image" src="https://github.com/user-attachments/assets/2cb99a8f-e78e-472b-93b4-ab207fa59e01" />


### Ejecución del script
> <img width="975" height="570" alt="image" src="https://github.com/user-attachments/assets/455967d8-0f91-4ece-93dd-e7ce00c75d99" />


### Tabla ARP de PC1 después del ataque
> <img width="834" height="433" alt="image" src="https://github.com/user-attachments/assets/9e0a3881-e869-4c84-bbb0-8c9dffed2cda" />


### Tráfico interceptado en Kali
> <img width="975" height="380" alt="image" src="https://github.com/user-attachments/assets/ad5b89fd-e27d-4692-9f55-ab903db6a341" />


---

## Contramedidas

### ARP Inspection en SW1
```cisco
ip arp inspection vlan 1
interface ethernet 0/2
 ip arp inspection trust
```

### Verificación
> <img width="902" height="327" alt="image" src="https://github.com/user-attachments/assets/e45dcf0b-4f47-41ea-8242-a5168801c683" />


### Resultado
Dynamic ARP Inspection valida los paquetes ARP contra la tabla 
DHCP Snooping binding, descartando respuestas ARP falsas.

> <img width="847" height="313" alt="image" src="https://github.com/user-attachments/assets/bf247d6d-bcee-48f2-bf85-609adcf09d03" />
