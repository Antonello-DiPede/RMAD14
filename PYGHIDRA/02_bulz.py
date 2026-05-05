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



#HLOCAL __cdecl FUN_10001210(int param_1,LPCSTR param_2,int param_3)

#{
  #byte bVar1;
  #HLOCAL pvVar2;
  #int iVar3;
  #int local_8;
  
  #pvVar2 = LocalAlloc(0x40,param_3 + 1);
  #*(undefined1 *)((int)pvVar2 + param_3) = 0;
  #for (local_8 = 0; local_8 < param_3; local_8 = local_8 + 1) {
    #bVar1 = *(byte *)(param_1 + local_8);
    #iVar3 = lstrlenA(param_2);
   # *(byte *)((int)pvVar2 + local_8) = bVar1 ^ param_2[local_8 % iVar3];
  #}
 # return pvVar2;
#}



enc_str_addr = toAddr(0x10002034)
key_addr = toAddr(0x10002020)
decrypted_str = decrypt_str(enc_str_addr, key_addr, 0x10).decode('utf-8').rstrip('\x00')

print(decrypted_str)
