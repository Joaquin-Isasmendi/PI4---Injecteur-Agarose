import Fonctions
from time import sleep 
from os import system, name

#À changer avec l'utilisateur
port = Fonctions.setup_serial("/dev/cu.usbserial-110", 19200, 1)

DIAint = 11.99 #en mm
Volume_to_dispense = int(input("Insert max volume to dispense: "))
flowRate = float(input("Flow rate: ")) #max: 0.3455 mL/s, min: 0.1 mL/s
temp = int(input("Temperature: ")) #doit être entre 35 et 40 deg celsius 
pressure = int(input("Pressure: ")) #doit être entre 0 et 50cm de H20

while (flowRate > 0.3455) or (temp > 40 or temp < 35) or (pressure > 50):
    if flowRate > 0.3455:
        flowRate = float(input("Insérer un autre flow rate: ")) #max: 0.3455 mL/s, min: 0.1 mL/s
    if (temp > 40 or temp < 35):
        temp = int(input("Insérer une autre temperature entre 35 à 40: ")) #doit être entre 35 et 40 deg celsius 
    if pressure > 50:
        pressure = int(input("Insérer une autre pression: ")) #doit être entre 0 et 50cm de H20

print('Connected.')
print(f'Port accesible:{port.writable()}')
port.open()
print(f"Port open: {port.isOpen()}")

#Commandes à envoyer à la pompe pour les propriétés initiales
port.write(Fonctions.setDIA(DIAint))
sleep(1)
port.write(Fonctions.setVol(Volume_to_dispense))
sleep(1)
port.write(Fonctions.pumpRate(flowRate*3600,"MH"))#max: 1244 mL/hr, min: 9.495 uL/hr
sleep(1)


if temp >= 35 and temp <= 40: #Température doit se situer entre 35 et 40 deg celcius pour que la pompe commence a rouler
    Condition_Rouler = input ("Pump is ready. Are you ready to roll boss ? (Oui, Non)")

if Condition_Rouler == "Oui":
    port.write(Fonctions.Run())
    sleep(1)

pressure = int(input("Pression augmente, quelle est la nouvelle pression? ")) #doit être entre 0 et 50cm de H20

if pressure >= 50: #Pression ne doit pas dépasser 50 cm de H20
    port.write(Fonctions.STP())
    sleep(1)

print('Fini.')
port.close()
print(f'Port accesible:{port.writable()}')



