#@runtime PyGhidra

def read_c_string(start_addr):
    result = bytearray()
    addr = start_addr

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

        

addr = toAddr(0x10002124)
c_str = read_c_string(addr).decode('utf-8').rstrip('\x00')
print("String at 0x10002124:", c_str)
