from escpos.printer import Usb

from kafka import KafkaConsumer

consumer = KafkaConsumer('falls', bootstrap_servers='localhost:9092')

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    """ Seiko Epson Corp. Receipt Printer (EPSON TM-T20II)"""
    p = Usb(0x04b8, 0x0e15, 0)
    p.text("Caida detectada" + str(message) + "\n")
    p.barcode(str(message.timestamp), 'EAN13', 64, 2, '', '')
    p.cut()
