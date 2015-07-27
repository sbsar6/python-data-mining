import re
phase = ':P1'
print('phase', phase)
highPhase = 0    
phaseNum = re.findall(r'\d+', phase)
print(phaseNum)
phaseNum2 = list(map(int, phaseNum))
print(phaseNum2)
