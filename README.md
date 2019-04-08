# Logitech unifying receiver VID/PID modification

This is a guide on how to manually change the VID/PID for Logitech unifying receiver. I did this because I wanted to passthrough one of my Logitech keyboards to a virtual machine, however I have two Logitech unifying receivers connected to the host machine with identical VID/PIDs, so it's a bit tricky to edit my VM config to passthrough the one I want. Changing the PID of one of the dongles was the solution.

Note this is carried out on the Nordic nRF24LU1-based receiver C-U0007 (firmware version RQR12.0X). There is a newer version of the unifying receiver based in TI chip (C-U0008 and firmware RQR24) which I don't know if will work, but maybe the same principle will apply.

# Some useful resources
- fwupd
This is the main tool to update firmware of the receiver dongle
- [https://github.com/Logitech/fw_updates](https://github.com/Logitech/fw_updates) 
This is the official Logitech repository for several of their products, including the unifying receivers.
- [https://github.com/BastilleResearch/nrf-research-firmware/tree/master/prog/usb-flasher](https://github.com/BastilleResearch/nrf-research-firmware/tree/master/prog/usb-flasher)
This repo contains some reverse-engineering information and tools for the unifying receiver. Among other things, it contains the CRC algorithm and location of the expected checksum in flash.

# Steps
The basic idea is simple, just grab a known firmware, patch the PID/VID bytes, fix the CRC checksum and flash it back to the receiver. Note that some of the most recent firmwares (from the Logitech repository) are signed (*.shex file instead of *.hex file) and require a recent bootloader. My dongle uses an older bootloader so I didn't look into that in details.

Here is a sequence of commands to run to carry out the procedure:
- Download the official firmware
`git clone https://github.com/Logitech/fw_updates.git`
- `cd fw_updates/RQR12/RQR12.08`
- Search for C52B abd 2BC5 in RQR12.08_B0030.hex and change it. Fix the line checksum per Intel Hex file format
- Generate a binary firmware, note the fill bytes 0xFF, otherwise the CRC computation will be wrong. 
`avr-objcopy --gap-fill=0xff -I ihex -O binary RQR12.08_B0030.hex RQR12.08_B0030.bin`
- Compute the checksum
`python crc.py RQR12.08_B0030.bin`
- Edit RQR12.08_B0030.hex again and set the checksum (2 bytes at location 0x67FE)
- Compile a new firmware acceptable by fwupd
- `cd lvfs; make`
- Finally flash the patched firmware
`sudo fwupd.fwupdmgr  --allow-older --force install Logitech-Unifying-RQR12.08_B0030.cab`

# Files
crc.py: python script to compute the firmware checksum
Logitech-Unifying-RQR12.08_B0030.cab: patched firmware with VID/PID: 046d:c52c
