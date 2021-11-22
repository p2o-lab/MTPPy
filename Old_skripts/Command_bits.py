
dict_standard={
    'IdleEn':0b00100001100,
    'StartingEn':0b00100011000,
    'CompletingEn':0b00100001010,
    'CompletedEn':0b00100001010,
    'ResumingEn':0b00100011000,
    'PausedEn':0b00110011000,
    'PausingEn':0b00100011000,
    'HoldingEn':0b00100001000,
    'HeldEn':0b00100101000,
    'UnholdingEn':0b00100011000,
    'StoppingEn':0b00100000000,
    'StoppedEn':0b00100000010,
    'AbortingEn':0b0000000000,
    'AbortedEn':0b00000000010,
    'ResettingEn':0b00100001000,
    'ExecuteEn':0b11101011000
}

dict_wo_pause={
    'ExecuteEn':0b11100011000
}

dict_wo_hold={

    'StartingEn':0b00100011000,
    'CompletingEn':0b00100001010,
    'ResumingEn':0b00100011000,
    'PausedEn':0b00110011000,
    'PausingEn':0b00100011000,
    'UnholdingEn':0b00100011000,
    'ExecuteEn':0b11101011000
}

dict_wo_pause_hold={
    'StartingEn': 0b00100011000,
    'CompletingEn': 0b00100001010,
    'ResumingEn': 0b00100011000,
    'PausedEn': 0b00110011000,
    'PausingEn': 0b00100011000,
    'UnholdingEn': 0b00100011000,
    'ExecuteEn': 0b11100011000
}