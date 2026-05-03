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


# ═════════════════════════════════════════════
#  SCENARIO — cambia solo questa sezione
#  Valori: 1, 2, 3
# ═════════════════════════════════════════════

SCENARIO = 2


# ─────────────────────────────────────────────
#  SCENARIO 1 — Setup → Loop → Print
# ─────────────────────────────────────────────
#
#  Struttura assembly tipica:
#    movabs rax, VAL1
#    mov    [rsp+OFF1], rax
#    movabs rax, VAL2        ← sovrascrive parzialmente
#    mov    [rsp+OFF2], rax
#    lea rdx, [rsp+X]
#    lea rcx, [rsp+Y]
#    lea rsi, [rsp+Z]
#    sub edi, edx
#    --- loop ---
#    lea eax, [rdi+rdx]
#    xor al, byte [rdx]
#    add rdx, 1
#    sub rcx, 1
#    ror al, N
#    mov byte [rcx+1], al
#    cmp rdx, rsi
#    jne loop
#
def scenario_1():
    mem = bytearray(0x18) #sub rsp, 0x18

    # ── SETUP ────────────────────────────────
    # Cambia: offset e valori hex dei movabs
    movabs(mem, 0x01, 0x1435262A0F292408)   # mov qword [rsp+1], rax
    movabs(mem, 0x08, 0x171604302B2B14)   # mov qword [rsp+8], rax

    # Registri iniziali — adatta agli offset nel codice
    rdx = 0x00                   # xor edx, edx
    rsi = 0x01                 # lea rsi, [rsp+0x01]  ← buffer di destinazione (dove scrive il loop)
    rcx = 0x01                 #  mov rcx, rsi 
    eax = 0x47                # mov eax, 0x47

    # ── LOOP ─────────────────────────────────
    # Reproduce the cycle
    while rdx != 0x0e:
        mem[rcx]  = u8(mem[rcx] ^ eax) #u8 becasue  al is involved in the operation and is 1 byte, 
        #while eax is 4 byte
        eax = eax +3               
        rcx += 1                  
        eax = eax ^ rdx
        rdx+= 1         

    # ── OUTPUT ───────────────────────────────
    # Cambia: offset start = dove punta rdi nel printf, length = num byte
    # start è il primo offset dove veiene scritto rax ovvero rsp + 1 e poi la legnth vedi il ciclo  
    print_result(mem, start=0x01, length=0x0e)


# ─────────────────────────────────────────────
#  SCENARIO 2 — Setup → Loop1 → Clean → Loop2 → Print
# ─────────────────────────────────────────────
#
#  Struttura assembly tipica:
#    [setup identico a scenario 1]
#    --- loop 1 ---
#    [trasformazione byte → buffer intermedio]
#    xor ecx, ecx   ← clean
#    xor edx, edx
#    lea rdi, [rsp+NEW_OFFSET]
#    --- loop 2 ---
#    [seconda trasformazione]
#
def scenario_2():
    mem = bytearray(0x38)

    # ── SETUP ────────────────────────────────
    movabs(mem, 0x04, 0xDAA40A861E9F81CD)
    movabs(mem, 0x0a, 0x44CC75E1CB45DAA4)

    edi = 0xFFFFFFA5
    rdx = 0x04
    rcx = 0x1f
    rsi = 0x12
    edi = u8(edi - rdx)

    # ── LOOP 1 ───────────────────────────────
    while rdx != rsi:
        eax = u8(edi + rdx)
        al  = u8(eax ^ mem[rdx]) 
        rdx += 1
        rcx -= 1
        al  = ror(al, 3) 
        mem[rcx + 1] = al

    # ── CLEAN ────────────────────────────────
    # Cambia: nuovi valori di registro dopo il reset
    ecx = 0                       # xor ecx, ecx
    edx = 0                       # xor edx, edx
    rdi = 0x21                    # lea rdi, [rsp+0x21]  ← nuovo dest
    rsi2 = 0x12                   # rsi rimane il buffer intermedio

    # ── LOOP 2 ───────────────────────────────
    # Cambia: limite (0x0e), costante SUB step (7), ROR (1), XOR (0x3c)
    while edx != 0x0e:            # cmp rdx, 0xe
        al  = mem[rsi2 + edx]     # movzx eax, byte [rsi+rdx]
        al  = u8(al - ecx)        # sub eax, ecx
        ecx = u8(ecx + 7)         # add ecx, 7  ← cambia step
        al  = ror(al, 1)          # ror al, 1   ← cambia N
        al  = u8(al ^ 0x3c)       # xor eax, 0x3c  ← cambia K
        mem[rdi + edx] = al       # mov byte [rdi+rdx], al
        edx += 1

    # ── OUTPUT ───────────────────────────────
    print_result(mem, start=rdi, length=0x0e)


# ─────────────────────────────────────────────
#  SCENARIO 3 — Main chiama sub_XXXX esterne
# ─────────────────────────────────────────────
#
#  Struttura assembly tipica:
#    movabs ...
#    call sub_1260   ← copia dati
#    call sub_1240   ← riordina/ruota struttura
#    call sub_1220   ← XOR con chiave crescente
#    call sub_11f0   ← swap/reverse
#    call sub_11d0   ← ROL/ROR + XOR finale
#    printf(rdi)
#
#  Aggiungi/rimuovi funzioni in base alle sub che vedi
#

def sub_1260(mem, rdi):
    eax = 0 
    """Copia N byte da [rsp+rsi] a [rdi]"""
    rsi = 0x05
    n   = 0x0d 
    for i in range(n): # i act as eax 
        mem[rdi + i] = mem[rsi + i]

def sub_1240(mem, rdi):
    """Rotazione struttura: sposta un blocco all'inizio"""
    # mov rcx, [rdi+5]  /  mov edx, [rdi]  /  movzx eax, [rdi+4]
    # poi riscrive in ordine: rcx, edx, al
    # Cambia: offset 5, 4, 0xc in base al codice
    rcx = bytes(mem[rdi+5 : rdi+5+8]) # mov rcx, qword [rdi+5]
    edx = bytes(mem[rdi   : rdi+4]) # mov edx, dword [rdi]
    al  = mem[rdi+4] # movzx eax, byte [rdi+4]  -> al è la parte bassa di eax, quindi prendo solo 1 byte
    mem[rdi+8    : rdi+12] = edx #mov dword [rdi+8], edx
    mem[rdi      : rdi+8 ] = rcx #mov qword [rdi], rcx
    mem[rdi+0x0c]           = al # mov byte [rdi+0xc], al

def sub_1220(mem, rdi):
    """XOR con chiave crescente — cmp al, STOP"""
    # Cambia: start (0x3d), step (0x11), n (0x0d)
    eax = 0x3d
    while (eax != 0x1a):
        mem[rdi] = u8(mem[rdi] ^ eax)
        eax = u8(eax + 0x11)       # add eax, 0x11
        rdi += 1

def sub_11f0(mem, rdi):
    """Reverse/swap a due puntatori verso il centro"""
    # Cambia: 0x0c (indice fine), 6 (centro)

    rax = rdi + 0x0c 
    rsi = rdi + 6

    while rax  != rsi:
        edx = mem[rdi]
        ecx = mem[rax]
        rax -= 1
        rdi += 1 
        mem [rdi -1] = u8(ecx) # mem[rdi-1] = ecx
        mem [rax +1] = u8(edx)


def sub_11d0(mem, rdi):
    """ROL N + XOR K su ogni byte"""
    # Cambia: 0x0d (n), rol(al, 4), 0x55
    rdx  = rdi + 0x0d
    while rdi != rdx:
        al = mem[rdi]
        rdi += 1 
        al = rol(al, 4)      # cambia N
        al = u8(al ^ 0x55)         # cambia K
        mem[rdi - 1] = al

def scenario_3():
    mem = bytearray(0x28) #sub rsp, 0x28

    # ── SETUP ────────────────────────────────
    # Cambia: offset e valori hex
    movabs(mem, 0x05, 0x5dfd2e795be565d6) # mov qword [rsp + 5], rax 
    movabs(mem, 0x0a, 0xf51081f1d35dfd2e) # mov qword [rsp + 0xa], rax 
   
    r8 = 0x12
    rsi = 0x05                    # lea rsi, [rsp+0x05]
    rdi = r8              # lea r8, [rsp+0x12] → poi mov rdi, r8
    mem[0x12:0x12+8] = bytes(8)    # mov qword [rsp+0x12], 0
    mem[0x18:0x18+8] = bytes(8)    # mov qword [rsp+0x18], 0


    # ── CHIAMA LE FUNZIONI ────────────────────
    # Cambia: ordine e nomi in base al grafo del main
    sub_1260(mem, rdi)
    sub_1240(mem, rdi)
    sub_1220(mem, rdi)
    rdi = r8 
    sub_11f0(mem, rdi)
    rdi = r8
    sub_11d0(mem, rdi)

    # ── OUTPUT ───────────────────────────────
    print_result(mem, start=rdi, length=0x0d)

# ─────────────────────────────────────────────
# SCENARIO 4
# ─────────────────────────────────────────────

def sub_12f0(mem, rdi, rsi):


    mem[rdi+32 : rdi+40] = (0xd).to_bytes(8, byteorder='little') # mov qword [rdi+0x20], 0xd

    eax = 0 
    while(eax != 0x0d):
        edx = mem[rsi + eax] #movzx edx, byte   [rsi+rax]
        mem[rdi + eax] = u8(edx) #mov byte [rdi+rax], dl
        eax += 1

    return

def sub_1210(mem, rdi, rsi):

    rax = int.from_bytes(mem[rdi+0x20 : rdi+0x28], 'little') # mov rax, qword [rdi+0x20]
    if rax == 1:
        return
    

    rax = shr(rax, 1, bits=64) #shr rax, 1 ; 
    rcx = rdi + rax*2

    while(rdi != rcx):
        rax = mem[rdi] 
        edx = mem[rdi+1]
        rdi = rdi + 2 
        mem [rdi -2 ] = edx
        mem [rdi -1 ] = rax

    return

def sub_1260_b(mem, rdi, rsi):

    rdx = int.from_bytes(mem[rdi+0x20 : rdi+0x28], 'little') # mov rax, qword [rdi+0x20]

    if (rdx == 0):
        return
    
    eax = rdx + rdx*8
    eax = rdx + eax*2

    rdx = rdx + rdi 

    while(rdi != rdx):
        mem[rdi]  = u8(mem[rdi] ^ eax) # xor byte [rdi], al
        rdi += 1
        eax = eax + 7 


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


def sub_1200(edi, rsi):

    al = edi & 0xFF # Get LAST BYTE 
    cl = rsi & 0xFF
    al = ror(al, cl, bits=8)

    return  al

def sub_1290(mem, rdi, rsi):

    r9 = int.from_bytes(mem[rdi+0x20 : rdi+0x28], 'little') # mov r9, qword [rdi+0x20]
    r11 = rdi 
    r8d = 0 
    r10 = 0xaaaaaaaaaaaaaaab

    if (r9 == 0):
        return 
    

    while (r8d != r9):
        rax = r8d 
        rsi = r8d
        edi = mem[r11 + r8d]
        rax , rdx = mul_r10_sim(r10, rax) # mul r10 
        rax = rdx 
        rdx = rdx & 0xfffffffffffffffe
        rax = shr(rax, 1, bits=64) #shr rax, 1
        rdx = rdx + rax
        rsi = rsi - rdx 
        rsi = rsi + 1 

        #here pass edi not rdi sinde rdi has the pointer edi the data
        rax = sub_1200(edi, rsi) # sub_1200(rdi, rsi)
        
        rax = rax - r9
        rax = rax + r8d
        mem[r11 + r8d] = u8(rax) #mov byte [r11+r8d], al
        r8d = r8d + 1


    return


def scenario_4():

    mem = bytearray(0x40) #sub rsp, 0x28

    # ── SETUP ────────────────────────────────
    # Cambia: offset e valori hex
    movabs(mem, 0x0b, 0xb1f9aac98eec69f8) # mov qword [rsp + 5], rax 
    rsi = 0x0b                    # lea rsi, [rsp+0x05]
    rdi = 0x18              # lea rdi,  [rsp+0x18]
    movabs(mem, 0x10, 0x878ca76498b1f9aa) # mov qword [rsp + 0xa], rax 

    mem[0x18:0x18+8] = bytes(8)    # mov qword [rsp+0x18], 0
    mem[0x20:0x20+8] = bytes(8)    # mov qword [rsp+0x20], 0
    mem[0x28:0x28+8] = bytes(8)    # mov qword [rsp+0x28], 0
    mem[0x30:0x30+8] = bytes(8)    # mov qword [rsp+0x30], 0


    # ── CHIAMA LE FUNZIONI ────────────────────
    sub_12f0(mem, rdi, rsi)
    sub_1210(mem, rdi, rsi)
    rdi  = 0x18
    sub_1260_b(mem, rdi, rsi)
    rdi  = 0x18
    sub_1290(mem, rdi, rsi)


    # ── OUTPUT ───────────────────────────────
    print_result(mem, start=rdi, length=0x0d)


def scenario_5_exam1():


    return

def scenario_6_exam2():


    return

def scenario_7_exam2():


    return



# ═════════════════════════════════════════════
#  DISPATCH
# ═════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'═'*45}")
    print(f"  ASM CTF Solver — Scenario {SCENARIO}")
    print(f"{'═'*45}\n")

    if   SCENARIO == 1: scenario_1()
    elif SCENARIO == 2: scenario_2()
    elif SCENARIO == 3: scenario_3()
    elif SCENARIO == 4: scenario_4()
    elif SCENARIO == 5: scenario_5_exam1()
    elif SCENARIO == 6: scenario_6_exam2()
    elif SCENARIO == 7: scenario_7_exam2()
    
    else: print("SCENARIO non valido. Scegli 1, 2 o 3.")

    print()
