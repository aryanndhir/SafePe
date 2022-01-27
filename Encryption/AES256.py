from keyManager import expandKey, createRoundKey
from AddRoundKey import addRoundKey
from SubBytes import subBytes, subBytesInv
from RowShifter import shiftRows, shiftRowsInv
from ColumnMixer import mixColumns, mixInvColumns


def encrypt(inBlock, key):
    outBlock = inBlock

    # Initialize
    expandedKey = expandKey(key)

    # First Round
    outBlock = addRoundKey(outBlock, createRoundKey(expandedKey, 0))

    # Round 1->13
    for n in range(1, 14):
        outBlock = subBytes(outBlock)
        outBlock = shiftRows(outBlock)
        outBlock = mixColumns(outBlock)
        outBlock = addRoundKey(outBlock, createRoundKey(expandedKey, n))

    # Round 14
    outBlock = subBytes(outBlock)
    outBlock = shiftRows(outBlock)
    outBlock = addRoundKey(outBlock, createRoundKey(
        expandedKey, 14))  # Add roundKey

    return outBlock


def decrypt(inBlock, key):
    outBlock = inBlock
    numOfRounds = 14
    expandedKey = expandKey(key)

    # First round
    outBlock = addRoundKey(outBlock, createRoundKey(expandedKey, numOfRounds))
    outBlock = shiftRowsInv(outBlock)
    outBlock = subBytesInv(outBlock)

    for i in range(numOfRounds-1, 0, -1):
        outBlock = addRoundKey(outBlock, createRoundKey(expandedKey, i))
        outBlock = mixInvColumns(outBlock)
        outBlock = shiftRowsInv(outBlock)
        outBlock = subBytesInv(outBlock)

    # round 14
    outBlock = addRoundKey(outBlock, createRoundKey(expandedKey, 0))
    return outBlock
