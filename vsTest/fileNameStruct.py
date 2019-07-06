class fNameStruct(object):
    """description of class"""
    def __init__(self , filename , splitStr):
        strArray =  filename.rsplit(splitStr , 1)
        self.bfName = strArray[0]
        self.ltname = strArray[1]
        self.spStr = splitStr


