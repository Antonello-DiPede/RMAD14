import struct
SCENARIO = 6



def shl(v, n, bits=64): return (v << n) & ((1 << bits) - 1)
def shr(v, n, bits=64): return (v >> n) & ((1 << bits) - 1)


def movabs(mem, offset, val):
    mem[offset:offset+8] = struct.pack('<Q', val)

def print_result(mem, start, length, prefix="RevMal"):
    raw = mem[start:start+length]
    s   = ''.join(chr(b) for b in raw)
    print(f"[hex]    {raw.hex()}")
    print(f"[ascii]  {s}")
    print(f"[flag]   {prefix}{{{s}}}")

def u8(v):             return v & 0xFF #get last 8 bits

def ror(v, n, bits=8):
    n = n % bits  
    if n == 0:
        return v & 0xFF
    return ((v >> n) | (v << (bits - n))) & 0xFF

def scenario_1():

    mem = bytearray(0x18)

    movabs(mem, 0x05, 0x332b072f07382512)
    rcx = 0x05
    rdx = 0x0f

    mem[0x0c : 0x10] = (0x2f2833).to_bytes(4, 'little')
    rax = rcx 


    while rax != rdx : 
        mem[rax] = u8(mem[rax] ^0x4a)
        mem[rax+1] = u8(mem[rax+1] ^0x4a)
        rax = rax + 2

    rdx = rcx 

    

     # ── OUTPUT ───────────────────────────────
    print_result(mem, start=rdx, length=0x0d)




    return


def scenario_2():

    mem = bytearray(0x18)
    edx = 0
    movabs(mem, 0x01, 0x1435262a0f292408)
    rsi = 0x01
    movabs(mem, 0x08, 0x171604302b2b14)
    rcx = rsi 
    eax = 0x47

    while edx != 0x0e : 
        mem[rcx] = u8(mem[rcx] ^ u8(eax))
        eax = u8(eax + 3)
        rcx = rcx + 1
        eax = eax ^ edx
        edx = edx + 1

    rdx = rsi 
    print_result(mem, start=rsi, length=0x0f)


    return 


def scenario_3():

    mem = bytearray(0x28)
    edi = 0x13
    mem[0x15] = 0x61
    rdx = 0xd 
    rcx = 0x1e
    movabs(mem, 0x0d, 0x42404b544b474652)
    r8 = 0x16
    eax = 0x21
    edi = edi - rdx


    while rdx != r8 :
        esi = mem[rdx]
        rcx = rcx - 1
        esi = esi ^ eax 
        mem[rcx + 1] = u8(esi)
        esi = edi + rdx 
        rdx = rdx + 1
        eax = eax ^ esi 
        eax = eax + 2 

    print_result(mem, start=rdx, length=0x0f)

def scenario_4():

    mem = bytearray(0x38)
    edi = 0xffffffa5

    movabs(mem, 0x04, 0xdaa40a861e9f81cd)
    rdx = 0x04
    rcx = 0x1f 
    movabs(mem, 0x0a, 0x44cc75e1cb45daa4)
    rsi = 0x12
    edi = edi - rdx 

    while rdx != rsi : 
        eax = u8(edi + rdx)
        eax = u8(eax ^ mem[rdx])
        rdx += 1
        rcx -= 1
        eax = ror(eax, 3 , bits=8)
        mem[rcx +1 ] = u8(eax)


    
    ecx = 0 
    edx = 0 
    rdi = 0x21

    while edx != 0x0e: 
        eax = mem[rsi + edx]
        eax = u8(eax - ecx)
        ecx = u8(ecx + 7)
        eax = ror(eax, 1 , bits=8)
        eax = u8(eax ^ 0x3c)
        mem [ rdi +edx ] = u8(eax)
        edx = edx + 1 

    rdx = rdi 
    print_result(mem, start=rdi, length=0x0e )


    return


def sub_1260_a(mem, rdi , rsi): 

    eax = 0 

    while(eax != 0x0d):
        edx = mem[rsi + eax]
        mem [rdi + eax] = u8(edx)
        eax += 1 


    return

def sub_1240(mem,rdi,rsi):

    rcx = int.from_bytes(mem[rdi + 0x05 : rdi+ 0x05+8], 'little')
    edx = int.from_bytes(mem[rdi: rdi+ 0x04], 'little')
    eax = mem[rdi+4]
    mem[rdi+8 : rdi+8+4] = (edx).to_bytes(4,'little')
    mem[rdi: rdi+8] = (rcx).to_bytes(8,'little')
    mem[rdi + 0xc] = u8(eax)



    return


def sub_1220(mem,rdi,rsi):

    eax = 0x3d
    al = u8(eax)

    while(al != 0x1a):
        mem[rdi] = u8(mem[rdi] ^ al)
        eax = eax + 0x11
        rdi += 1 
        al = u8(eax)



    return


def sub_11f0(mem, rdi, rsi): 

    rax = rdi + 0x0c
    rsi = rdi + 0x06

    while (rax != rsi ):
        edx = mem[rdi]
        ecx = mem[rax]
        rax = rax - 1
        rdi = rdi + 1 
        mem [rdi -1 ] = u8(ecx)
        mem [rax +1 ] = u8(edx)


    return

def sub_11d0(mem, rdi):

    rdx = rdi + 0x0d 

    while (rdi != rdx):
        eax = mem[rdi]
        rdi = rdi +1 
        eax = ror(eax,4,bits=8)
        eax = u8(eax ^ 0x55)
        mem[rdi -1 ] = u8(eax)

    return

def scenario_5():

    mem = bytearray(0x28)
    r8 = 0x12
    movabs(mem, 0x05, 0x5dfd2e795be565d6)
    rsi = 0x05
    rdi = r8 
    movabs(mem, 0x0a, 0xf51081f1d35dfd2e)
    movabs(mem, 0x12, 0x0)
    movabs(mem, 0x18, 0x0)


    sub_1260_a(mem,rdi,rsi)
    sub_1240(mem,rdi,rdi)
    sub_1220(mem,rdi,rsi)

    rdi = r8 

    sub_11f0(mem,rdi,rsi)
    rdi = r8
    sub_11d0(mem,rdi)
    rdx = r8
    print_result(mem, start=rdx, length=0x0f )





#    return

def sub_12f0(mem, rdi, rsi):

    mem[rdi+0x20: rdi+0x20+0x08] = (0x0d).to_bytes(8,'little')
    eax = 0

    while (eax != 0x0d):
        edx = mem[rsi + eax]
        mem[rdi+eax] = u8(edx)
        eax +=1 


    return

def sub_1210(mem,rdi,rsi):

    rax = int.from_bytes(mem[rdi+0x20 : rdi+0x20+0x08],'little')

    if (rax <= 1 ): return

    rax = shr(rax,1,bits=64)
    rcx = rdi + rax*2

    while rdi != rcx: 
        eax = mem[rdi]
        edx = mem[rdi +1]
        rdi = rdi + 2 
        mem[rdi -2 ] = u8(edx)
        mem[rdi -1 ] = u8(eax)


    return

def sub_1260(mem,rdi,rsi):

    rdx = int.from_bytes(mem[rdi+0x20 : rdi+0x20+0x08],'little')

    if (rdx == 0 ): return

    eax = rdx + rdx*8
    eax = rdx + eax*2
    rdx = rdx + rdi 


    while (rdi != rdx):
        mem[rdi] = u8(mem[rdi] ^ u8(eax))
        rdi += 1 
        eax = eax +7

    

    return

def mul_r10_sim(r10, rax):
    """
    Simula l'istruzione x86-64: MUL R10
    (unsigned multiplication: RAX * R10 -> RDX:RAX)
    """

    mask64 = (1 << 64) - 1

    result = rax * r10

    rax = result & mask64              # low 64 bits
    rdx = (result >> 64) & mask64      # high 64 bits

    return rax, rdx


def sub_1200(edi,rsi):

    eax = edi
    ecx = rsi 
    al = u8(eax)
    cl = u8(ecx)
    al = ror(al,cl,bits=8)


    return al


def sub_1290(mem, rdi, rsi):

    r9 = int.from_bytes(mem[rdi+0x20 : rdi+0x20+0x08],'little')
    r11 = rdi 
    r8d = 0 
    r10 = 0xaaaaaaaaaaaaaaab

    if r9 == 0 : return

    while r8d != r9 : 
        rax = r8d
        rsi = r8d
        edi = mem[r11+r8d]
        rax , rdx = mul_r10_sim(r10,rax)
        rax = rdx 
        rdx = rdx & 0xfffffffffffffffe
        rax = shr(rax,1,bits=64)
        rdx = rdx + rax
        rsi = rsi - rdx 
        rsi = rsi + 1 
        rax = sub_1200(edi,rsi)
        rax = rax - r9
        rax = rax + r8d
        mem [r11 + r8d] = u8(rax)
        r8d = r8d + 1








    return

def scenario_6():

    mem = bytearray(0x40)
    movabs(mem, 0x0b, 0xb1f9aac98eec69f8)
    rsi = 0x0b 
    rdi = 0x18
    movabs(mem, 0x10, 0x878ca76498b1f9aa)
    movabs(mem, 0x18, 0x0)
    movabs(mem, 0x20, 0x0)
    movabs(mem, 0x28, 0x0)
    movabs(mem, 0x30, 0x0)

    sub_12f0(mem,rdi,rsi)
    sub_1210(mem,rdi,rsi)
    rdi = 0x18
    sub_1260(mem,rdi,rsi)
    rdi = 0x18
    sub_1290(mem,rdi,rsi)
    rdx = 0x18

    print_result(mem, start=rdx, length=0x0f)

    return



if __name__ == "__main__":
    print(f"\n{'═'*45}")
    print(f"  ASM CTF Solver — Scenario {SCENARIO}")
    print(f"{'═'*45}\n")

    if   SCENARIO == 1: scenario_1()
    elif SCENARIO == 2: scenario_2()
    elif SCENARIO == 3: scenario_3()
    elif SCENARIO == 4: scenario_4()
    elif SCENARIO == 5: scenario_5()
    elif SCENARIO == 6: scenario_6()
    
    else: print("SCENARIO non valido. Scegli 1, 2 o 3.")

    print()
