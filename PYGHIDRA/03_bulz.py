#@runtime PyGhidra


fm = currentProgram.getFunctionManager()
listing = currentProgram.getListing()


def count_instructions(func):
    
    tot = 0 
    body = func.getBody()
    for i in listing.getInstructions(body, True):
        tot += 1 


    return tot


for func in fm.getFunctions(True):
    name = func.getName()
    addr = func.getEntryPoint()
    instr_count = count_instructions(func)
    print(f"{name} @ {addr}: {instr_count} instructions")
