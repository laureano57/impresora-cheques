from constants import *

def lineDivider(lineText, maxLength):
    """
    lineText:   str - Linea de texto de n palabras
    maxLength:  int - Longitud maxima de la 1er linea (de salida)

    Return:     list - Lista con 2 strings, donde el primero tiene una
                longitud maxima de maxLength caracteres
    """
    # Arma lista de palabras
    listWords = lineText.split()
    pos = 0

    # Une los strings y busca la posicion que excede los maxLenght caracteres
    while len(' '.join(listWords[:pos+1])) < maxLength:
    	pos += 1

    # Une las lineas segun esa posicion y devuelve lista con 2 lineas
    line1 = ' '.join(listWords[:pos])
    line2 = ' '.join(listWords[pos:])
    return [line1, line2]

def writeField(data, field):
    """
    data:   str - Dato de un campo (nombre, valor textual, etc)
    field:  tuple(int, int) - Inicio y extension del campo
            (startColumn, fieldLength)

    Return: str - Linea con el dato centrado en el campo
    """
    # Calcula la columna del centro absoluto del campo en la linea:
    fieldCenter = field[0] + field[1]/2

    # Calcula los espacios
    spaces = (fieldCenter - len(data)/2)*' '

    return spaces+data

def writeDate(date, dayField, monthField, yearField):
    """
    date:       str - Fecha en formato DD/MM/YYYY
    xxxField:   tuple - Inicio y extension del campo
                (startColumn, fieldLength)

    Return: str - Linea con el dia, mes y anio centrados en sus campos
    """

    # Traduccion de meses
    monthNames =    {
                '01':'ENERO',
                '02':'FEBRERO',
                '03':'MARZO',
                '04':'ABRIL',
                '05':'MAYO',
                '06':'JUNIO',
                '07':'JULIO',
                '08':'AGOSTO',
                '09':'SEPTIEMBRE',
                '10':'OCTUBRE',
                '11':'NOVIEMBRE',
                '12':'DICIEMBRE'
                }

    # Separa dia, mes y anio
    dateList = date.split('/')

    # Traduce el numero de mes a su nombre y lo reemplaza en la lista
    dateList[1] = monthNames[dateList[1]]

    # Calcula el centro absoluto de los campos
    dayFieldCenter = dayField[0] + dayField[1]/2
    monthFieldCenter = monthField[0] + monthField[1]/2
    yearFieldCenter = yearField[0] + yearField[1]/2

    # Calcula la columna de inicio del dato una vez centrado (no confundir con
    # columna de inicio del campo)
    dayFieldStart = dayFieldCenter - len(dateList[0])/2
    monthFieldStart = monthFieldCenter - len(dateList[1])/2
    yearFieldStart = yearFieldCenter - len(dateList[2])/2

    # Almacena los inicios en una lista para poder iterarla
    fieldStarts = [dayFieldStart, monthFieldStart, yearFieldStart]

    ret = []

    # Construye el string de salida
    for i in range(3):
        try:
            substr = (fieldStarts[i]-len(''.join(ret[:i])))*' '+dateList[i]
        except:
            substr = fieldStarts[i]*' '+dateList[i]

        ret.append(substr)

    return ''.join(ret)

def formatValue(numericValue):
    """
    numericValue: str - Valor numerico del cheque, en el formato: "12345678.90"

    Return: String con el formato que usaban los viejos cheques:
            "****12,345,678.90.-"

    Son 19 caracteres, separador decimal punto, separador de miles coma,
    asteriscos completan los 19 caracteres, punto y guion al final.
    Se supone que no se van a emitir cheques de mas de 1x10^12 pesos y
    que el valor numerico de entrada no va a usar la coma como separador
    decimal.
    """

    intList = []

    if '.' in numericValue:
        # Caso 1, decimal completo: separa entero y decimal en 2 variables
        integer, decimal = numericValue.split('.')
        # Caso 2, decimal de 1 solo digito: agrega un cero al decimal
        if len(decimal) == 1:
            decimal = decimal+'0'
        # Caso 3, solo punto divisor decimal: agrega dos ceros al decimal
        elif len(decimal) == 0:
            decimal = '00'
    else:
        # Si no tiene decimal, lo genera
        integer = numericValue
        decimal = '00'

    # Para poner separadores de miles usa el cociente y el resto de la parte
    # entera en funcion de 3 digitos
    quotient = len(integer)/3
    remainder = len(integer)%3

    # Si tiene uno o dos digitos antes de una coma, los agrega a
    # la lista intList
    if remainder != 0:
        intList.append(integer[:remainder])

    # Agrega cada terna de digitos a la lista
    for i in range(quotient):
        intList.append(integer[remainder:remainder+3])
        remainder += 3

    # Une con comas la cifra entera, agrega el decimal despues del punto y
    # finaliza con punto y guion
    res = ','.join(intList)+'.'+decimal+'.-'

    # Completa los 19 caracteres con asteriscos y devuelve el string
    return '*'*(19-len(res))+res

def listChecks(checkFile):
    """
    checkFile: str - "checkfile.txt"

    Return: Lista de listas con los datos de cada cheque (1 cheque por lista)
    """
    listChecks = []

    for line in open(checkFile):
        listChecks.append(line.strip().split('\t'))

    return listChecks

def checkLines(checkList, bankFields, bankMaxLengthTextVal):
    """
    checkList:  List - Valores de un solo cheque (De una linea del archivo)
    bankFields: Dict - Campos del cheque {'nombreField': (startCol, length)}
    bankMaxLengthTextVal: Int - Longitud maxima del campo de valor textual

    Return:     Diccionario con las lineas del cheque listas para imprimir
                {'nombre de linea': linea}
    """

    # Escribe la linea de la fecha del cheque
    dateLine = writeDate(checkList[1], bankFields['dayField'],
                        bankFields['monthField'], bankFields['yearField'])

    # Escribe la linea del nombre (destinatario del cheque)
    nameLine = writeField(checkList[2], bankFields['nameCheckField'])

    # Escribe la linea del valor numerico del cheque (formateado)
    valueLine = writeField(formatValue(checkList[3]),
                           bankFields['numericValueField'])

    # Toma el importe textual y lo divide en 2 lineas de max 35 caracteres
    if len(checkList[4]) > bankMaxLengthTextVal:
        textVal1, textVal2 = lineDivider(checkList[4], bankMaxLengthTextVal)
    else:
        textVal1 = checkList[4]
        textVal2 = ' '

    # Escribe las lineas del valor textual del cheque
    textualValue1Line = writeField(textVal1, bankFields['textualValue1Field'])
    textualValue2Line = writeField(textVal2, bankFields['textualValue2Field'])

    ret =   {
            'valueLine': valueLine,
            'dateLine': dateLine,
            'nameLine': nameLine,
            'textualValue1Line': textualValue1Line,
            'textualValue2Line': textualValue2Line
            }

    return ret

def writeCheck(checkLinesDict, linesDict, linesNumber):
    """
    checkLinesDict: dict - Salida de checkLines (lineas de cheque listas)
    linesDict: dict - Numero de linea de cada campo {n: valorLine}
    linesNumber: int - Cantidad de lineas del cheque

    Return: lista con las lineas del cheque terminado
    """
    ret = []

    for numLine in range(linesNumber):
        if numLine+1 in linesDict:
            ret.append(checkLinesDict[linesDict[numLine+1]])
        else:
            ret.append('')

    return ret