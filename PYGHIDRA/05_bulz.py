#@runtime PyGhidra

from ghidra.program.model.scalar import Scalar



def get_references_to_decrypt_function():
    addr = toAddr(0x10001210)

    references = getReferencesTo(addr)
    references_is_call = []

    for ref in references:
        if ref.getReferenceType().isCall():
            references_is_call.append(ref) 

    return references_is_call    


def get_push_immediate(inst):
    if inst.getMnemonicString() != "PUSH":
        return None
    
    operands = inst.getOpObjects(0) # Get The Operands
    if isinstance(operands[0],Scalar):
        return operands[0].getValue()
    
    return None



def read_c_string(start_addr):
    result = bytearray()
    addr = toAddr(start_addr)

    while True:
        # Check if the user cancelled the script
        if getMonitor().isCancelled():
            break

        b = getByte(addr) & 0xFF  # ensure unsigned

        if b == 0:  # null terminator
            break

        result.append(b)
        addr = addr.add(1)

    return result


def decrypt_str(enc_string_addr, key_addr, length):
    result = bytearray(length + 1)
    key = read_c_string(key_addr)
    key_len = len(key)
    string = read_c_string(enc_string_addr)

    for i in range(length):
        result[i] = string[i] ^ key[i % key_len]

    # terminatore nullo come in C
    result[length] = 0

    return bytes(result)


def get_call_args(call_address, N):
    args = []
    instr = getInstructionBefore(call_address) # The PUSH INST IS 1 ISNTR BEFORE

    while instr and len(args) < N : 
        val = get_push_immediate(instr)
        if val is not None: args.append(val)

        instr = instr.getPrevious() #VAL PUSHED ON TO THE STACK IN THE INVERSE ODER

    return list(reversed(args))

xrefs = get_references_to_decrypt_function()
for xref in xrefs:
    
    call_address = xref.getFromAddress()
    args = get_call_args(call_address,3)

    a1,a2,a3 = args

    decrypted_str = decrypt_str(a1,a2,a3)
    decrypted_str = decrypted_str.decode('utf-8').rstrip('\x00')

    print(decrypted_str)

