from printerCommands import *
# from escpos.printer import Usb

printChecks('testChecks.txt', supervielleCheckSetup)


# Testing USB printer module:

# Create the printer object with the connection params
# printer = getUSBPrinter()(idVendor=0x04B8,
#                           idProduct=0x0005,
#                           inputEndPoint=0x82,
#                           outputEndPoint=0x01, initialize=False)
