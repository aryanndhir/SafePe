from ..Encryption.myUtils import convertToMatrixBlock, convertFromMatrixBlock
from ..Encryption.mixColTables import getTable, getVector, getInvVector


def mixColumn(column):
    outColumn = []
    for i in range(0, len(column)):
        xorCol = []
        for j in range(0, 4):
            xorCol.append(getTable(column[j], getVector(i, j)))
        outColumn.append(xorCol[0] ^ xorCol[1] ^ xorCol[2] ^ xorCol[3])
    return outColumn


def mixInvColumn(column):
    outColumn = []
    for i in range(0, len(column)):
        xorInvCol = []
        for j in range(0, 4):
            xorInvCol.append(getTable(column[j], getInvVector(i, j)))
        outColumn.append(xorInvCol[0] ^ xorInvCol[1]
                         ^ xorInvCol[2] ^ xorInvCol[3])
    return outColumn


def mixColumns(block):
    inBlock = convertToMatrixBlock(block)
    mixBlock = []
    for i in range(0, len(inBlock)):
        mixBlock.append(mixColumn(inBlock[i]))
    return convertFromMatrixBlock(mixBlock)


def mixInvColumns(block):
    inBlock = convertToMatrixBlock(block)
    outBlock = []
    for i in range(0, len(inBlock)):
        outBlock.append(mixInvColumn(inBlock[i]))
    return convertFromMatrixBlock(outBlock)
