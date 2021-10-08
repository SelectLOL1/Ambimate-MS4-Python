#!/usr/bin/python
import smbus2
import time

# I2C address of the Ambishit
address = 0x2A

# Create I2C instance and open bus #!!!I2C Baudrate/Clock-Speed must be changed to 10k!!! 
ambishit = smbus2.SMBus(1)

# Send instruction to read sensor options
print(ambishit.read_byte_data(address, 0x82))

time.sleep(0.1)

while 1:
    
    # Send instruction to refresh all sensor values
    ambishit.write_byte_data(address,0xC0,0xFF)

    time.sleep(0.5)

    # Read 15 bytes of data
    myshitvalues = ambishit.read_i2c_block_data(address,0x00,15).copy()

    # Evaluate values
    if(myshitvalues[5-14] == 255): #Ambishit ate shit, don't use that values
        print(f'Shit values: {myshitvalues}')
        time.sleep(1)
        pass
    else:
        print(myshitvalues)
        print(f'PIR Trigger: {True if myshitvalues[0]>0 else False}')
        print(f'Temp: {(myshitvalues[1] * 256.0 + myshitvalues[2]) / 10.0} °C')
        print(f'Hum: {(myshitvalues[3] * 256.0 + myshitvalues[4]) / 10.0} %RH')
        print(f'Lum: {(myshitvalues[5] * 256.0 + myshitvalues[6])} Lux')
        print(f'Volt: {((myshitvalues[9] * 256.0 + myshitvalues[10]) / 1024.0) * (3.3 / 0.330):.2f} V')
        print(f'eCo2: {(myshitvalues[11] * 256.0 + myshitvalues[12])} ppm')
        print(f'TVOC: {(myshitvalues[13] * 256.0 + myshitvalues[14])} ppb')
        time.sleep(1)
