from pathlib import Path
import struct

startAddresForChange = 0x54
stopAddresForChange = 0x58
zeroBottomLayers = b'\x00\x00\x00\x00'      # equal to 0.0 in float format

# Just for tests
filenameOpen = '1_Small_Circle.pwmx'
fileFake = '1_Small_Circle.pem'

class FileOperation:
    def __init__(self, filename) -> None:
        self.__fileBuffer = None
        if(Path(filename).suffix == '.pwmx'):
            self.__fileName = filename
        else:
            raise FileExistsError

    @property
    def propFilename(self):
        return self.__fileName

    @propFilename.setter
    def propFilename(self, filenameInput):
        if(Path(filenameInput).suffix == '.pwmx'):
            self.__fileName = filenameInput
        else:
            raise FileExistsError

    def checkPropertyIsEmpty(self):
        if(self.__fileName is None):
            raise FileNotFoundError
        elif(self.__fileBuffer is None):
            raise BufferError

    def openAndReadFile(self):
        if(self.__fileName is None):
            raise FileNotFoundError
        with open(self.__fileName, 'rb') as file_to_read:
            self.__fileBuffer = file_to_read.read()
        file_to_read.close()

    def changeNumBottomLayers(self, changeBytes = zeroBottomLayers):
        self.checkPropertyIsEmpty()
        if(len(changeBytes) != 4):
            raise ValueError
        else:
            self.__fileBuffer = self.__fileBuffer[:startAddresForChange] + changeBytes + \
                self.__fileBuffer[stopAddresForChange:]

    def writeBufferToNewFile(self):
        self.checkPropertyIsEmpty()
        new_filename = self.__fileName.replace(Path(self.__fileName).name, "FixBL_" + Path(self.__fileName).name)
        #new_filename = "FixBL_" + self.__fileName
        file_to_write = open(new_filename, 'wb')
        file_to_write.write(self.__fileBuffer)
        file_to_write.close()
        return new_filename

    def findNumOfBottomLayers(self):
        self.checkPropertyIsEmpty()
        binaryArray = self.__fileBuffer[startAddresForChange:stopAddresForChange]
        [tempFloat] = struct.unpack('f', binaryArray)
        return tempFloat

    def automaticWork(self):
        self.openAndReadFile()
        self.findNumOfBottomLayers()
        self.changeNumBottomLayers()
        return self.writeBufferToNewFile()


if __name__ == "__main__":
    try:
        do_file = FileOperation(filenameOpen)
    except FileExistsError:
        print("Uncorrect name")

    try:
        do_file.automaticWork()
    except Exception as e:
        print(str(e))
