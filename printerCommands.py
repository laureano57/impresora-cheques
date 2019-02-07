from constants import *
from functions import *

def initPrinterChecks(printerFile, bankPrinterSetup):
    """
    printerFile: file - Archivo /dev/usb/lp1 abierto como archivo en modo write

    Inicializa la impresora configurando longitud de pagina, espaciado entre
    lineas, impresion en negrita y ubicando el cabezal en la posicion exacta
    de la primera linea (Para cheques Supervielle)
    """

    # ESC C n    => Establece largo de pagina en 3 pulgadas (largo del cheque)
    printerFile.write(bankPrinterSetup['checkInches'])

    # ESC 3 n    => Achica el espaciado entre lineas, donde \x30 deja 3mm de
    # espacio (definido a prueba y error)
    printerFile.write(bankPrinterSetup['lineSpacing'])

    # ESC G      => Double strike printing (bold)
    printerFile.write('\x1b\x47')

    # ESC J      => Reverse feed
    # \x1b\x6a\xNN donde NN = numero de puntos a desplazar
    # Al introducir el papel en la impresora y hacer FF (form feed), el pie de
    # la primera linea queda 1,2cm por debajo del borde superior del papel.
    # Desplazando 15 puntos hacia arriba el papel, el pie de la primera linea
    # queda a 0,9cm del borde superior (necesario para los cheques bbva)
    # Para los cheques supervielle quedo configurado en 27 puntos
    printerFile.write(bankPrinterSetup['reverseFeedDots'])

def endCheck(printer, bankPrinterSetup):

    # Form feed, pasa una hoja (un cheque)
    printer.write('\x0c')
    # Vuelve N puntos atras para alinear
    printer.write(bankPrinterSetup['reverseFeedDots'])

def endPrinting(printer, bankPrinterSetup):
    """
    Mueve el papel 8 lineas hacia adelante para dejar el troquelado en el borde
    de la guillotina y cierra el archivo
    """
    for i in range(bankPrinterSetup['endPrintingLines']):
        printer.write('\x0a')
    printer.close()

def printCheck(check, printer, bankPrinterSetup):
    """ Imprime las lineas de un solo cheque
    """
    # Itera sobre las lineas del cheque y las imprime
    for line in check:
        printer.write(line+'\n')


    endCheck(printer, bankPrinterSetup)

def printChecks(checkFile, bankCheckSetup):
    """ Imprime todos los cheques del archivo
        checkFile: archivo de texto plano con los datos de cada cheque
    """

    # Desgloso el setup
    fields = bankCheckSetup[0]
    linesDict = bankCheckSetup[1]
    linesNumber = bankCheckSetup[2]
    maxLengthTextVal = bankCheckSetup[3]
    printerSetup = bankCheckSetup[4]

    # Abre la impresora (como archivo)
    printer = open('/dev/usb/lp1', 'w')

    # Inicializa la impresora (posicion inicial, espaciado, double strike)
    initPrinterChecks(printer, printerSetup)

    # Arma la lista de listas de cheques
    checks = listChecks(checkFile)

    # Itera sobre cada cheque
    for check in checks:
        # Arma un dict con las lineas del cheque
        checkLinesDict = checkLines(check, fields, maxLengthTextVal)
        # Escribe las lineas del cheque terminadas en una lista
        check = writeCheck(checkLinesDict, linesDict, linesNumber)
        # Imprime el cheque y salto al siguiente inicio de cheque
        printCheck(check, printer, printerSetup)

    # Al terminar de imprimir los cheques, salta N lineas hasta que el
    # troquelado quede sobre la guillotina
    endPrinting(printer, printerSetup)