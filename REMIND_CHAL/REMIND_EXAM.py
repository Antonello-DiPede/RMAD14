import struct
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║              ASM → PYTHON  CHEATSHEET  (da chal00 a chal05)                ║
# ║  Formato:  python_equivalente   --   istruzione_asm                        ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

# ─────────────────────────────────────────────────────────────────────────────
#  1. SETUP STACK / MEMORIA
# ─────────────────────────────────────────────────────────────────────────────

# mem = bytearray(0x28)                         --  sub rsp, 0x28
# mem[off : off+8] = struct.pack('<Q', val)     --  movabs rax, val  +  mov qword [rsp+off], rax
# mem[off : off+8] = (0).to_bytes(8,'little')  --  mov qword [rsp+off], 0
# mem[off : off+4] = struct.pack('<I', val)     --  mov dword [rsp+off], val
# mem[off] = val                                --  mov byte  [rsp+off], val
# rdi = off                                     --  lea rdi, [rsp+off]
# rsi = off                                     --  lea rsi, [rsp+off]
# rdx = off                                     --  lea rdx, [rsp+off]
# rcx = off                                     --  lea rcx, [rsp+off]
# r8  = off                                     --  lea r8,  [rsp+off]
# rax = int.from_bytes(mem[off:off+8],'little') --  mov rax, qword [rdi+off]
# edx = int.from_bytes(mem[off:off+4],'little') --  mov edx, dword [rdi]
# rcx = rdi                                     --  mov rcx, rdi
# rdi = r8                                      --  mov rdi, r8


# ─────────────────────────────────────────────────────────────────────────────
#  2. LETTURA BYTE DALLA MEMORIA  (movzx = zero-extend → niente segno)
# ─────────────────────────────────────────────────────────────────────────────

# eax = mem[rdi]                --  movzx eax, byte [rdi]
# eax = mem[rdi + 1]            --  movzx eax, byte [rdi+1]
# eax = mem[rdi + off]          --  movzx eax, byte [rdi+off]
# edx = mem[rdi]                --  movzx edx, byte [rdi]
# edx = mem[rdi + 1]            --  movzx edx, byte [rdi+1]
# esi = mem[rdx]                --  movzx esi, byte [rdx]
# edi = mem[r11 + r8]           --  movzx edi, byte [r11+r8]
# ecx = mem[rax]                --  movzx ecx, byte [rax]
# al  = mem[rdi]     (= eax&0xFF già garantito se eax è u8)


# ─────────────────────────────────────────────────────────────────────────────
#  3. SCRITTURA BYTE IN MEMORIA
# ─────────────────────────────────────────────────────────────────────────────

# mem[rcx]         = u8(al)     --  mov byte [rcx], al   (sil/al/cl/dl = low 8-bit)
# mem[rcx + 1]     = u8(al)     --  mov byte [rcx+1], al
# mem[rdi - 1]     = u8(al)     --  mov byte [rdi-1], al
# mem[rdi + rdx]   = u8(al)     --  mov byte [rdi+rdx], al
# mem[r11 + r8]    = u8(al)     --  mov byte [r11+r8], al
# mem[rax + 1]     = u8(dl)     --  mov byte [rax+1], dl
# mem[rdi + off]   = u8(al)     --  mov byte [rdi+off], al
# mem[rdi:rdi+8]   = rcx_bytes  --  mov qword [rdi], rcx
# mem[rdi+8:rdi+12]= edx_bytes  --  mov dword [rdi+8], edx


# ─────────────────────────────────────────────────────────────────────────────
#  4. ARITMETICA
# ─────────────────────────────────────────────────────────────────────────────

# eax = (eax + 3)   & 0xFFFFFFFF   --  add eax, 3
# eax = (eax + 2)   & 0xFFFFFFFF   --  add eax, 2
# eax = (eax + 7)   & 0xFFFFFFFF   --  add eax, 7
# eax = (eax + 0x11)& 0xFFFFFFFF   --  add eax, 0x11
# ecx = (ecx + 7)   & 0xFF         --  add ecx, 7       (usa &0xFF se è al/cl 8-bit)
# rdi = rdi + 1                     --  add rdi, 1
# rdx = rdx + 1                     --  add rdx, 1
# rax = rax + 1                     --  add rax, 1
# r8  = r8  + 1                     --  add r8,  1
# rax = rax + 2                     --  add rax, 2
# rdx = rdx + rdi                   --  add rdx, rdi
# rdx = rdx + rax                   --  add rdx, rax
# eax = (eax - ecx) & 0xFF          --  sub eax, ecx     (al = al - cl)
# eax = (eax - r9)  & 0xFF          --  sub eax, r9d
# eax = (eax + r8)  & 0xFF          --  add eax, r8d
# rcx = rcx - 1                     --  sub rcx, 1
# rax = rax - 1                     --  sub rax, 1
# rsi = (rsi - rdx) & 0xFFFFFFFF    --  sub rsi, rdx
# edi = u8(edi - edx)               --  sub edi, edx     (prendi solo low 8-bit)
# eax = rdx + rdx*8                 --  lea eax, [rdx+rdx*8]   (= rdx*9)
# eax = rdx + eax*2                 --  lea eax, [rdx+rax*2]
# eax = u8(edi + rdx)               --  lea eax, [rdi+rdx]
# esi = (rdi + rdx) & 0xFFFFFFFF    --  lea esi, [rdi+rdx]
# rcx = rdi + rax*2                 --  lea rcx, [rdi+rax*2]
# rdx = rdi + 0xd                   --  lea rdx, [rdi+0xd]
# rax = rdi + 0xc                   --  lea rax, [rdi+0xc]
# rsi = rdi + 6                     --  lea rsi, [rdi+6]
# esi = (esi + 1)   & 0xFFFFFFFF    --  add esi, 1


# ─────────────────────────────────────────────────────────────────────────────
#  5. LOGICA / BITWISE
# ─────────────────────────────────────────────────────────────────────────────

# mem[rdi] = u8(mem[rdi] ^ eax)   --  xor byte [rdi], al
# mem[rax] = u8(mem[rax] ^ 0x4a)  --  xor byte [rax], 0x4a
# eax = u8(eax ^ esi)             --  xor esi, eax    (risultato in esi/eax)
# eax = u8(eax ^ edx)             --  xor eax, edx
# eax = u8(eax ^ 0x55)            --  xor eax, 0x55
# eax = u8(eax ^ 0x3c)            --  xor eax, 0x3c
# eax = u8(al  ^ mem[rdx])        --  xor al, byte [rdx]
# eax = 0                         --  xor eax, eax
# edx = 0                         --  xor edx, edx
# ecx = 0                         --  xor ecx, ecx
# r8d = 0                         --  xor r8d, r8d
# rdx = rdx & 0xfffffffffffffffe  --  and rdx, 0xfffffffffffffffe
# eax = 0x47                      --  mov eax, 0x47
# eax = 0x21                      --  mov eax, 0x21
# eax = 0x10                      --  mov eax, 0x10
# eax = 0x3d                      --  mov eax, 0x3d


# ─────────────────────────────────────────────────────────────────────────────
#  6. ROTATE / SHIFT
# ─────────────────────────────────────────────────────────────────────────────

# al = ror(al, 1, bits=8)         --  ror al, 1
# al = ror(al, 2, bits=8)         --  ror al, 2
# al = ror(al, 3, bits=8)         --  ror al, 3
# al = ror(al, cl, bits=8)        --  ror al, cl      (cl = rsi & 0xFF)
# al = rol(al, 4, bits=8)         --  rol al, 4
# rax = rax >> 1                  --  shr rax, 1      (equivalente: rax = shr(rax,1,bits=64))
# rax = rdx >> 1                  --  shr rax, 1      (dopo mov rax,rdx)


# ─────────────────────────────────────────────────────────────────────────────
#  7. CONFRONTO E SALTO  (condizioni del while)
# ─────────────────────────────────────────────────────────────────────────────

# while rdi != rdx:   --  cmp rdi, rdx  /  jne label
# while rdx != rsi:   --  cmp rdx, rsi  /  jne label
# while rdx != r8:    --  cmp rdx, r8   /  jne label
# while rax != 0xd:   --  cmp rax, 0xd  /  jne label
# while edx != 0xe:   --  cmp edx, 0xe  /  jne label  (cmp rdx, 0xe)
# while r8 != r9:     --  cmp r8,  r9   /  jne label
# while rax != rsi:   --  cmp rax, rsi  /  jne label
# if rax <= 1: return --  cmp rax, 1    /  jbe label   (jump if ≤)
# if r9 == 0: return  --  test r9, r9   /  je  label
# if rdx == 0: return --  test rdx, rdx /  je  label
# eax != 0x1a         --  cmp al, 0x1a  /  jne label   (chiave 8-bit)


# ─────────────────────────────────────────────────────────────────────────────
#  8. MUL (moltiplicazione unsigned 64-bit → 128-bit in RDX:RAX)
# ─────────────────────────────────────────────────────────────────────────────

# def mul_r10_sim(r10, rax):
#     result = rax * r10
#     lo = result & ((1<<64)-1)   # rimane in rax (di solito non usato)
#     hi = (result >> 64) & ((1<<64)-1)  # va in rdx
#     return lo, hi
#
# rax, rdx = mul_r10_sim(r10, rax)   --  mul r10
# rax = rdx                          --  mov rax, rdx   (prendi la parte alta)
#
# Trick compilatore: divisione per 3 via moltiplicazione magica
# r10 = 0xaaaaaaaaaaaaaaab           --  movabs r10, 0xaaaaaaaaaaaaaaab
# → (i * r10) >> 64 >> 1  ≈  i // 3
# → ((i // 3) * 3) - i + 1  =  i % 3 + 1   (rotazione ciclica 1,2,3,1,2,3,...)


# ─────────────────────────────────────────────────────────────────────────────
#  9. PATTERN TIPICI COMPLETI
# ─────────────────────────────────────────────────────────────────────────────

# — Swap byte contigui (sub_1210 / sub_1240 style) —
# a, b = mem[rdi], mem[rdi+1]
# mem[rdi], mem[rdi+1] = b, a        -- movzx eax/edx + add rdi,2 + mov [rdi-2]/[rdi-1]

# — Reverse da entrambi i lati verso il centro (sub_11f0 style) —
# rax = rdi + 0xc   # puntatore fine
# rsi = rdi + 6     # centro
# while rax != rsi:
#     d, c = mem[rdi], mem[rax]
#     rax -= 1; rdi += 1
#     mem[rdi-1] = u8(c)
#     mem[rax+1] = u8(d)

# — Riorganizzazione struct fissa (sub_1240 style) —
# rcx = bytes(mem[rdi+5 : rdi+13])   # mov rcx, qword [rdi+5]
# edx = bytes(mem[rdi   : rdi+4 ])   # mov edx, dword [rdi]
# al  = mem[rdi+4]                   # movzx eax, byte [rdi+4]
# mem[rdi+8  : rdi+12] = edx         # mov dword [rdi+8], edx
# mem[rdi    : rdi+8 ] = rcx         # mov qword [rdi], rcx
# mem[rdi+0xc]          = al         # mov byte  [rdi+0xc], al

# — XOR con chiave a scorrimento (sub_1220 / sub_1260 style) —
# eax = START_KEY
# while eax != STOP_KEY:             # cmp al, STOP  / jne
#     mem[rdi] = u8(mem[rdi] ^ eax)
#     eax = u8(eax + STEP)
#     rdi += 1

# — ROL/ROR + XOR su ogni byte (sub_11d0 style) —
# rdx = rdi + LENGTH
# while rdi != rdx:
#     al = mem[rdi]; rdi += 1
#     al = rol(al, N, bits=8)
#     al = u8(al ^ K)
#     mem[rdi-1] = al

# — Copia N byte da src a dst (sub_12f0 / sub_1260-chal04 style) —
# for i in range(N):
#     mem[dst + i] = mem[src + i]    -- movzx edx, byte [rsi+rax] / mov byte [rdi+rax], dl

# — ROR ciclico con rotazione i%3+1 (sub_1290 style) —
# per ogni byte i:
#   rotation = (i % 3) + 1          -- trick mul 0xaaaaaaaaaaaaaaab
#   result = (ror(byte, rotation) - length + i) & 0xFF

#SIL: last 8 bit of ESI
# mem[rcx] = u8(esi) ---  #mov byte [rcx], sil 

# NOT bitwise (~ non 'not'):
# SBAGLIATO: mem[rdi] = not mem[rdi]      → restituisce True/False
# GIUSTO:    mem[rdi] = (~mem[rdi]) & 0xFF   --  not byte [rdi]
# GIUSTO:    mem[rdi] = u8(~mem[rdi])              --  not byte [rdi]

# Lettura qword come intero (non come bytes):
# SBAGLIATO: r9 = mem[rdi+0x20 : rdi+0x28]         → restituisce bytes
# GIUSTO:    r9 = int.from_bytes(mem[rdi+0x20 : rdi+0x28], 'little')  --  mov r9, qword [rdi+0x20]

# Scrittura qword da intero a bytes (int → memoria):
# SBAGLIATO: mem[rdi+0x20] = 0x0b                              → scrive solo 1 byte
# GIUSTO:    mem[rdi+
# 0x20 : rdi+0x28] = (0x0b).to_bytes(8, byteorder='little')  --  mov qword [rdi+0x20], 0x0b

# ── OPERATORI BITWISE IN PYTHON (sempre & 0xFF per restare a 8 bit) ───────────

# NOT (complemento bit a bit):
# SBAGLIATO: not x        → logico, restituisce True/False
# GIUSTO:    (~x) & 0xFF                      --  not al

# AND:
# SBAGLIATO: x and y      → logico, restituisce x o y
# GIUSTO:    x & y                            --  and al, cl

# OR:
# SBAGLIATO: x or y       → logico, restituisce x o y
# GIUSTO:    x | y                            --  or al, cl

# XOR:
# SBAGLIATO: x xor y      → non esiste in Python, SyntaxError
# GIUSTO:    x ^ y                            --  xor al, cl

# SHR (shift right logico):
# SBAGLIATO: x >> n        → ok ma senza maschera può dare più di 8 bit se x è grande
# GIUSTO:    (x >> n) & 0xFF                  --  shr al, n

# SHL (shift left):
# SBAGLIATO: x << n        → ok ma senza maschera supera 8 bit
# GIUSTO:    (x << n) & 0xFF                  --  shl al, n

# Regola generale — dopo OGNI operazione bitwise su valori a 8 bit:
# risultato = (operazione) & 0xFF   oppure   u8(operazione)


# ─────────────────────────────────────────────
#  UTILITY — non toccare
# ─────────────────────────────────────────────

def ror(v, n, bits=8):
    n = n % bits  
    if n == 0:
        return v & 0xFF
    return ((v >> n) | (v << (bits - n))) & 0xFF
def rol(v, n, bits=8):
    n = n % bits  
    if n == 0:
        return v & 0xFF
    return ((v << n) | (v >> (bits - n))) & 0xFF
def u8(v):             return v & 0xFF #get last 8 bits
def u16(v):             return v & 0xFFFF #get last 8 bits

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

def mul128(a, b):
    return mul_r10_sim(a,b)



# ═════════════════════════════════════════════
#  SCENARIO — cambia solo questa sezione
#  Valori: 1, 2, 3
# ═════════════════════════════════════════════

SCENARIO = 8

# EXAM00================================================================================


def sub_1370(mem, rdi, rsi):

    eax = 0 
    
    while(eax != 0xa):

        edx = mem[rsi+eax]
        mem[rdi + eax ] = u8(edx)
        eax += 1

    return 

def sub_1360(mem, rdi, rsi):

    rax = rdi + 9
    rsi = rdi + 4 

    while(rax != rsi):
        edx = mem[rdi]
        ecx = mem[rax]
        rax = rax -1 
        rdi = rdi + 1
        mem[rdi -1] = u8(ecx)
        mem[rax +1] = u8(edx)
    return

def sub_1320(mem, rdi, rsi):

    rcx = rdi + 0xa 

    while (rdi != rcx): 
        eax = mem[rdi]
        edx = mem[rdi +1]
        rdi = rdi + 2
        mem[rdi-2] = u8(edx)
        mem[rdi -1] = u8(eax)

    return



def sub_12c0(mem,rdi ,rsi):

    esi = 0x21
    rax = rdi + 0xa
    while rdi != rax :
        mem[rdi] = u8(mem[rdi] ^ u8(esi))
        mem[rdi + 1] = u8(mem[rdi + 1] ^ u8(esi))
        rdi = rdi +2 

    return

def sub_1280(mem,rdi ,rsi):

    eax = 0
    while eax != 0xa :
        mem[rdi+eax] =u8(mem[rdi+eax] - u8(eax))
        rdx = eax + 1
        eax += 2
        mem[rdi+rdx] =u8(mem[rdi+rdx] - u8(rdx))

    return


def sub_1240(mem,rdi,rsi):

    rax = rdi + 0xa

    while(rdi != rax): 
        mem[rdi] = u8(mem[rdi] + 3)
        mem[rdi +1 ] = u8(mem[rdi+1] + 3)
        rdi += 2


    return

def sub_12d0(esi):

    esi = 0x10
    return esi

def sub_1200(mem,rdi,rsi):
    mem[rdi + 0xa] = u8(0x0)
    return


def scenario_5_exam00():

    #TO FIX

    mem = bytearray(0x28)
    rsi = 0xb
    rdi = 0x15
    movabs(mem, 0xb, 0x48435471a15548a0)
    mem[0x13:0x15] = struct.pack('<H', 0x4e53)  # word, non movabs
    mem[0x15 : 0x15+8]  = (0x0).to_bytes(8,'little')
    mem[0x1c : 0x1c+4]  = (0x0).to_bytes(4,'little')

    sub_1370(mem,rdi,rsi)
    sub_1360(mem,rdi,rsi)
    rdi = 0x15
    sub_1320(mem,rdi,rsi)
    rdi = 0x15
    sub_12c0(mem,rdi,rsi)
    rdi = 0x15
    sub_1280(mem, rdi, rsi)
    sub_1240(mem,rdi,rsi)
    rdi = 0x15
    rsi = 0x10
    rdi = 0x15
    mem[rdi + 0xa] = 0x0
    rdx = rdi 


    print_result(mem, start=rdi, length=0x0a)


    return

# EXAM01================================================================================

def sub_1200b(mem, rdi, rsi):
    # reverse copy: rsi+9..rsi+0 → rdi+0..rdi+9
    rax = 0
    while rax != 0xa:
        edx = mem[rsi + 9 - rax]       # movzx edx, byte [rsi+rdx+9]  (neg rdx)
        mem[rdi + rax] = u8(edx)       # mov byte [rdi+rax], dl
        rax += 1

def sub_11c0b(mem, rdi, rsi):
    edx = 0x39                          # mov edx, 0x39
    rax = 0                             # xor eax, eax
    while rax != 0xa:                   # cmp rax, 0xa / jne
        mem[rdi+rax] = u8(mem[rdi+rax] ^ (edx & 0xFF))   # xor byte [rdi+rax], dl
        edx = ((edx + 5) ^ rax) & 0xFFFFFFFF              # add edx,5 / xor edx,eax
        rax += 1

def scenario_6_exam01():
    mem = bytearray(0x40)

    movabs(mem, 0x0b, 0x23281e2b38243c36)       # mov qword [rsp+0x0b], rax
    mem[0x13:0x15] = struct.pack('<H', 0x7c46)  # mov word  [rsp+0x13], ax
    rsi = 0x0b
    rdi = 0x15
    mem[0x15:0x15+8] = bytes(8)
    mem[0x1c:0x1c+4] = bytes(4)

    sub_1200b(mem, rdi, rsi)
    rdi = 0x15
    sub_11c0b(mem, rdi, rsi)

    
    print_result(mem, start=rdi, length=0x0f)


# EXAM02================================================================================


def scenario_7_exam02():

    #TODO 
    return


# EXAM03================================================================================

def sub_11f0C(edi, esi):          # ror al, cl
    al = edi & 0xFF
    cl = esi & 0xFF
    return ror(al, cl, bits=8)

def sub_1270C(mem, rdi, rsi):
    mem[rdi+0x40:rdi+0x48] = (0xd).to_bytes(8, 'little')  # length = 13
    r9  = rsi                   # source ptr
    r8  = rdi + 0x0c            # dest ptr (decrements)
    edx = 0xFFFFFFA0            # rolling XOR key

    while True:
        edi = mem[r9]                           # load source byte
        r9 += 1
        r8 -= 1
        edi = u8(edi ^ (edx & 0xFF))            # xor edi, edx
        edx = (edx + 3) & 0xFFFFFFFF           # key += 3
        al  = sub_11f0C(edi & 0xFF, 3)           # ror al, 3
        mem[r8 + 1] = al                        # store reversed
        if (edx & 0xFF) == 0xc7: break          # stop condition

def sub_1200C(mem, rdi, rsi):
    r10 = int.from_bytes(mem[rdi+0x40:rdi+0x48], 'little')
    if r10 == 0: return

    r8d = 0
    r9d = 0x31
    r11 = 0xaaaaaaaaaaaaaaab

    while r8d < r10:
        edi   = mem[rdi + r8d]
        rsi_v = r8d
        _, rdx_v = mul128(r11, r8d)             # mul r11 (div by 3 trick)
        edi = u8(edi ^ r9d)                     # xor edi, r9d
        r9d = (r9d + 0x13) & 0xFFFFFFFF        # r9d += 0x13
        rdx_v2 = (rdx_v & 0xfffffffffffffffe) + (rdx_v >> 1)
        r9d = r9d ^ (r8d & 0xFFFFFFFF)         # xor r9d, r8d
        rsi_v = ((rsi_v - rdx_v2) & 0xFFFFFFFF) + 1   # rotation = i%3+1
        al = sub_11f0C(edi, rsi_v)              # ror al, cl
        al = u8(al - (r8d * 5))               # sub eax, edx  (lea edx,[r8+r8*4])
        al = u8(al ^ 0x5a)                     # xor eax, 0x5a
        mem[rdi + r8d + 0x20] = al
        r8d += 1

def scenario_8_exam03():
    mem = bytearray(0x80)

    movabs(mem, 0x0b, 0x4127eb3495da0ef)    # mov qword [rsp+0x0b], rax
    movabs(mem, 0x10, 0xada5c3611b04127e)   # mov qword [rsp+0x10], rax
    rsi = 0x0b
    rdi = 0x18
    for off in [0x18,0x20,0x28,0x30,0x38,0x40,0x48,0x50]:
        mem[off:off+8] = bytes(8)

    sub_1270C(mem, rdi, rsi)
    rdi = 0x18
    sub_1200C(mem, rdi, rsi)

    print_result(mem,start=rdi+0x20,length=0x0d)



# ═════════════════════════════════════════════
#  DISPATCH
# ═════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'═'*45}")
    print(f"  ASM CTF Solver — Scenario {SCENARIO}")
    print(f"{'═'*45}\n")

    if   SCENARIO == 5: scenario_5_exam00()
    elif SCENARIO == 6: scenario_6_exam01()
    elif SCENARIO == 7: scenario_7_exam02()
    elif SCENARIO == 8: scenario_8_exam03()
    
    else: print("SCENARIO non valido. Scegli 5, 6, 7, 8.")

    print()
