"""
- Campos de cheques BBVA en coordenadas X,Y (linea, rangoColumna):

    numericValue:    (1, 48-65)
    day:             (3, 21-26)
    month:           (3, 30-43)
    year:            (3, 47-53)
    nameCheck:       (5, 20-48)
    textualValue1:   (6, 20-54)
    textualValue2:   (7, 20-64)
"""

#######     Constantes      #######

# Fields = (startColumn, fieldLength)
bbvaFields =    {
                'numericValueField':(48, 18),
                'dayField' : (21, 6),
                'monthField' : (30, 14),
                'yearField' : (47, 7),
                'nameCheckField' : (20, 29),
                'textualValue1Field' : (20, 35),
                'textualValue2Field' : (20, 45)
                }

supervielleFields = {
                    'numericValueField':(48, 19),
                    'dayField' : (23, 2),
                    'monthField' : (27, 13),
                    'yearField' : (43, 12),
                    'nameCheckField' : (20, 29),
                    'textualValue1Field' : (20, 35),
                    'textualValue2Field' : (20, 45)
                    }


# Numero de linea de cada dato a imprimir
bbvaLinesDict = {
                1: 'valueLine', 
                3: 'dateLine', 
                5: 'nameLine', 
                6: 'textualValue1Line', 
                7: 'textualValue2Line'
                }

supervielleLinesDict =  {
                        1: 'valueLine', 
                        3: 'dateLine', 
                        4: 'nameLine', 
                        5: 'textualValue1Line', 
                        6: 'textualValue2Line'
                        }

# Diccionario de indices de los datos de cada cheque (lista de cada linea de 
# lo que devuelve la base de datos)
checkListDataIndex =    {
                        0: 'id',
                        1: 'date',
                        2: 'name',
                        3: 'numericValue',
                        4: 'textualValue'
                        }

# Cantidad de lineas por cheque
bbvaLinesNumber = 12
supervielleLinesNumber = 15

# Longitud maxima de la primer linea del valor textual del cheque
bbvaMaxLengthTextVal = 35
supervielleMaxLengthTextVal = 35

# Configuracion de la impresora para cada cheque
bbvaPrinterSetup =  {
                    'reverseFeedDots': '\x1b\x6a\x15',
                    'checkInches': '\x1b\x43\x00\x03',
                    'lineSpacing': '\x1b\x33\x30',
                    'endPrintingLines': 8
                    }

superviellePrinterSetup =   {
                            'reverseFeedDots': '\x1b\x6a\x27',
                            'checkInches': '\x1b\x43\x00\x03',
                            'lineSpacing': '\x1b\x33\x28',
                            'endPrintingLines': 10
                            }

##########      Lista de configuraciones de cada banco      ##########

bbvaCheckSetup =    [
                    bbvaFields,
                    bbvaLinesDict, 
                    bbvaLinesNumber,
                    bbvaMaxLengthTextVal,
                    bbvaPrinterSetup
                    ]

supervielleCheckSetup = [
                        supervielleFields,
                        supervielleLinesDict, 
                        supervielleLinesNumber,
                        supervielleMaxLengthTextVal,
                        superviellePrinterSetup
                        ]