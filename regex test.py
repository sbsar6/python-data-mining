import re
phase = ':P1'

highPhase = 0    
phaseNum = re.findall(r'\d+', phase)

phaseNum2 = list(map(int, phaseNum))

if phasNum2 > highPhase:
    highPhase = phasNum2
