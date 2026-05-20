#@runtime PyGhidra

# ═══════════════════════════════════════════════════════════════
#  FULL GHIDRA BINARY EXPORTER
#  Edit INPUT_NAME to set the prefix for all output files.
# ═══════════════════════════════════════════════════════════════

INPUT_NAME  = "buterat"          # <─ change this
OUTPUT_DIR  = "C:\\Users\\dude\\LL"
NUM_DECOMP_PARTS = 4

# ───────────────────────────────────────────────────────────────

import io
import math
from ghidra.app.decompiler import DecompInterface, DecompileOptions
from ghidra.program.model.listing import CodeUnit
from ghidra.util.task import ConsoleTaskMonitor

def out(name):
    return OUTPUT_DIR + INPUT_NAME + "_" + name + ".txt"

def new_file(name, title):
    f = io.open(out(name), "w", encoding="utf-8")
    f.write(u"BINARY : {}\n".format(currentProgram.getName()))
    f.write(u"SECTION: {}\n".format(title))
    f.write(u"=" * 80 + u"\n\n")
    return f

# ═══════════════════════════════════════════════════════════════
# 1. DECOMPILED C + ASSEMBLY  (4 parts)
# ═══════════════════════════════════════════════════════════════
def export_decomp():
    decomp = DecompInterface()
    opts   = DecompileOptions()
    decomp.setOptions(opts)
    decomp.setSimplificationStyle("decompile")
    decomp.openProgram(currentProgram)

    monitor   = ConsoleTaskMonitor()
    fm        = currentProgram.getFunctionManager()
    listing   = currentProgram.getListing()
    functions = list(fm.getFunctions(True))
    total     = len(functions)
    chunk     = total // NUM_DECOMP_PARTS

    for part in range(NUM_DECOMP_PARTS):
        start  = part * chunk
        end    = total if part == NUM_DECOMP_PARTS - 1 else start + chunk
        subset = functions[start:end]
        path   = OUTPUT_DIR + INPUT_NAME + \
                 "_decomp_part{}.txt".format(part + 1)

        with io.open(path, "w", encoding="utf-8") as f:
            f.write(u"BINARY: {}\n".format(currentProgram.getName()))
            f.write(u"PART {}/{} — functions {} to {} of {}\n".format(
                part+1, NUM_DECOMP_PARTS, start+1, end, total))
            f.write(u"=" * 80 + u"\n\n")

            for i, func in enumerate(subset):
                if monitor.isCancelled(): break

                addr = func.getEntryPoint().toString()
                name = func.getName()
                sig  = func.getSignature().getPrototypeString()

                f.write(u"=" * 80 + u"\n")
                f.write(u"[{}/{}] FUNCTION: {}  @  {}\n".format(
                    start+i+1, total, name, addr))
                f.write(u"SIGNATURE: {}\n".format(sig))
                f.write(u"=" * 80 + u"\n")

                # Assembly
                f.write(u"\n--- ASSEMBLY ---\n")
                try:
                    instrs = listing.getInstructions(func.getBody(), True)
                    for instr in instrs:
                        f.write(u"  {}  {}\n".format(
                            instr.getAddress().toString(),
                            instr.toString()))
                except Exception as e:
                    f.write(u"[ASM ERROR: {}]\n".format(str(e)))

                # Decompiled C
                f.write(u"\n--- DECOMPILED C ---\n")
                try:
                    result = decomp.decompileFunction(func, 120, monitor)
                    if result and result.decompileCompleted():
                        c = result.getDecompiledFunction().getC()
                        f.write(str(c) if c else u"[EMPTY]\n")
                    else:
                        msg = result.getErrorMessage() if result else "None"
                        f.write(u"[FAILED: {}]\n".format(msg))
                except Exception as e:
                    f.write(u"[EXCEPTION: {}]\n".format(str(e)))

                f.write(u"\n")

            println("Saved part {}: {}".format(part+1, path))

# ═══════════════════════════════════════════════════════════════
# 2. STRINGS + XREFS
# ═══════════════════════════════════════════════════════════════
def export_strings_xrefs():
    fm      = currentProgram.getFunctionManager()
    listing = currentProgram.getListing()
    with new_file("strings_xrefs", "ALL STRINGS + CROSS REFERENCES") as f:
        for data in listing.getDefinedData(True):
            try:
                val = str(data.getValue())
                if len(val) < 2: continue
                addr = data.getAddress().toString()
                f.write(u"[{}] \"{}\"\n".format(addr, val))
                for ref in getReferencesTo(data.getAddress()):
                    fa   = ref.getFromAddress()
                    func = fm.getFunctionContaining(fa)
                    fn   = func.getName() if func else "??"
                    fe   = func.getEntryPoint().toString() if func else "??"
                    f.write(u"  <- {} in {}@{}\n".format(
                        fa.toString(), fn, fe))
                f.write(u"\n")
            except: pass
    println("Saved: " + out("strings_xrefs"))

# ═══════════════════════════════════════════════════════════════
# 3. IMPORTS + XREFS
# ═══════════════════════════════════════════════════════════════
def export_imports_xrefs():
    fm = currentProgram.getFunctionManager()
    sm = currentProgram.getSymbolTable()
    with new_file("imports_xrefs", "ALL IMPORTS + CALL SITES") as f:
        for sym in sm.getAllSymbols(True):
            refs = [r for r in getReferencesTo(sym.getAddress())
                    if r.getReferenceType().isCall()]
            if not refs: continue
            f.write(u"IMPORT: {} @ {}\n".format(
                sym.getName(), sym.getAddress().toString()))
            for r in refs:
                fa   = r.getFromAddress()
                func = fm.getFunctionContaining(fa)
                fn   = func.getName() if func else "??"
                fe   = func.getEntryPoint().toString() if func else "??"
                f.write(u"  called from: {} in {}@{}\n".format(
                    fa.toString(), fn, fe))
            f.write(u"\n")
    println("Saved: " + out("imports_xrefs"))

# ═══════════════════════════════════════════════════════════════
# 4. CALL GRAPH
# ═══════════════════════════════════════════════════════════════
def export_callgraph():
    fm = currentProgram.getFunctionManager()
    with new_file("callgraph", "FUNCTION CALL GRAPH") as f:
        for func in fm.getFunctions(True):
            addr = func.getEntryPoint().toString()
            name = func.getName()
            refs = [r for r in getReferencesTo(func.getEntryPoint())
                    if r.getReferenceType().isCall()]
            f.write(u"{}@{}\n".format(name, addr))
            if refs:
                for r in refs:
                    caller = fm.getFunctionContaining(r.getFromAddress())
                    if caller:
                        f.write(u"  called_by: {}@{}\n".format(
                            caller.getName(),
                            caller.getEntryPoint().toString()))
            else:
                f.write(u"  called_by: [ROOT]\n")
            f.write(u"\n")
    println("Saved: " + out("callgraph"))

# ═══════════════════════════════════════════════════════════════
# 5. PE METADATA
# ═══════════════════════════════════════════════════════════════
def export_pe_metadata():
    with new_file("pe_metadata", "PE HEADER METADATA") as f:
        f.write(u"  Image Base : {}\n".format(
            hex(currentProgram.getImageBase().getOffset())))
        f.write(u"  Binary Name: {}\n".format(currentProgram.getName()))
        f.write(u"  Language   : {}\n".format(
            currentProgram.getLanguage().getLanguageID()))
        f.write(u"  Compiler   : {}\n\n".format(
            currentProgram.getCompiler()))
        for opts_name in ["Program Information", "PE Header"]:
            try:
                opts = currentProgram.getOptions(opts_name)
                f.write(u"  [{} OPTIONS]\n".format(opts_name))
                for prop in opts.getOptionNames():
                    try:
                        val = opts.getValueAsString(prop)
                        f.write(u"    {}: {}\n".format(prop, val))
                    except: pass
                f.write(u"\n")
            except: pass
    println("Saved: " + out("pe_metadata"))

# ═══════════════════════════════════════════════════════════════
# 6. SECTIONS + ENTROPY
# ═══════════════════════════════════════════════════════════════
def calc_entropy(block):
    mem  = currentProgram.getMemory()
    size = min(int(block.getSize()), 524288)
    buf  = bytearray(size)
    try:
        mem.getBytes(block.getStart(), buf)
    except:
        return -1.0
    freq = [0] * 256
    for b in buf: freq[b & 0xFF] += 1
    entropy = 0.0
    for f in freq:
        if f > 0:
            p = float(f) / size
            entropy -= p * math.log(p, 2)
    return entropy

def export_sections():
    with new_file("sections", "MEMORY SECTIONS + ENTROPY") as f:
        f.write(u"  {:<14} {:<12} {:<12} {:<10} {:<6} {}\n".format(
            "Name","Start","End","Size","Perms","Entropy"))
        f.write(u"  " + u"-" * 70 + u"\n")
        for block in currentProgram.getMemory().getBlocks():
            perms = ("r" if block.isRead()    else "-") + \
                    ("w" if block.isWrite()   else "-") + \
                    ("x" if block.isExecute() else "-")
            entropy = calc_entropy(block)
            f.write(u"  {:<14} {:<12} {:<12} {:<10} {:<6} {:.4f}\n".format(
                block.getName(),
                block.getStart().toString(),
                block.getEnd().toString(),
                block.getSize(),
                perms,
                entropy))
    println("Saved: " + out("sections"))

# ═══════════════════════════════════════════════════════════════
# 7. ENTRY POINTS
# ═══════════════════════════════════════════════════════════════
def export_entry_points():
    fm = currentProgram.getFunctionManager()
    sm = currentProgram.getSymbolTable()
    with new_file("entry_points", "ALL ENTRY POINTS") as f:
        for addr in sm.getExternalEntryPointIterator():
            func = fm.getFunctionAt(addr)
            name = func.getName() if func else "??"
            f.write(u"  {}  @  {}\n".format(name, addr.toString()))
    println("Saved: " + out("entry_points"))

# ═══════════════════════════════════════════════════════════════
# 8. THUNK MAPPINGS
# ═══════════════════════════════════════════════════════════════
def export_thunks():
    fm = currentProgram.getFunctionManager()
    with new_file("thunks", "THUNK FUNCTION MAPPINGS") as f:
        for func in fm.getFunctions(True):
            if not func.isThunk(): continue
            try:
                target = func.getThunkedFunction(True)
                if target:
                    f.write(u"  {}@{}  ->  {}@{}\n".format(
                        func.getName(),
                        func.getEntryPoint().toString(),
                        target.getName(),
                        target.getEntryPoint().toString()))
            except: pass
    println("Saved: " + out("thunks"))

# ═══════════════════════════════════════════════════════════════
# 9. FUNCTION PROPERTIES
# ═══════════════════════════════════════════════════════════════
def export_function_properties():
    fm = currentProgram.getFunctionManager()
    sm = currentProgram.getSymbolTable()
    entry_addrs = set(
        a.toString() for a in sm.getExternalEntryPointIterator())
    with new_file("func_properties", "FUNCTION PROPERTIES TABLE") as f:
        f.write(u"  {:<35} {:<12} {:<20} {:<8} {:<6} {}\n".format(
            "Name@Addr","Convention","ReturnType","Params","Thunk","Flags"))
        f.write(u"  " + u"-" * 100 + u"\n")
        for func in fm.getFunctions(True):
            addr  = func.getEntryPoint().toString()
            name  = func.getName()
            try:   conv = func.getCallingConventionName() or "unknown"
            except: conv = "unknown"
            ret    = func.getReturnType().getName()
            params = func.getParameterCount()
            thunk  = func.isThunk()
            flags  = []
            if func.isExternal():   flags.append("EXTERNAL")
            if addr in entry_addrs: flags.append("ENTRYPOINT")
            f.write(u"  {:<35} {:<12} {:<20} {:<8} {:<6} {}\n".format(
                "{}@{}".format(name, addr),
                conv, ret, params, thunk,
                ",".join(flags)))
    println("Saved: " + out("func_properties"))

# ═══════════════════════════════════════════════════════════════
# 10. COMMENTS
# ═══════════════════════════════════════════════════════════════
def export_comments():
    TYPES = {
        CodeUnit.PLATE_COMMENT:      "PLATE",
        CodeUnit.PRE_COMMENT:        "PRE",
        CodeUnit.POST_COMMENT:       "POST",
        CodeUnit.EOL_COMMENT:        "EOL",
        CodeUnit.REPEATABLE_COMMENT: "REPEATABLE",
    }
    fm      = currentProgram.getFunctionManager()
    listing = currentProgram.getListing()
    with new_file("comments", "ALL COMMENTS") as f:
        for cu in listing.getCodeUnits(currentProgram.getMemory(), True):
            for ctype, cname in TYPES.items():
                comment = cu.getComment(ctype)
                if not comment: continue
                addr = cu.getAddress().toString()
                func = fm.getFunctionContaining(cu.getAddress())
                fi   = "{}@{}".format(
                    func.getName(),
                    func.getEntryPoint().toString()) if func else "global"
                f.write(u"  [{}] {} in {} | {}\n".format(
                    addr, cname, fi, comment))
    println("Saved: " + out("comments"))

# ═══════════════════════════════════════════════════════════════
# 11. GLOBAL VARIABLES
# ═══════════════════════════════════════════════════════════════
def export_global_vars():
    listing = currentProgram.getListing()
    with new_file("global_vars", "ALL GLOBAL VARIABLES WITH VALUES") as f:
        for data in listing.getDefinedData(True):
            try:
                label = data.getLabel() or ""
                if not label: continue          # only named globals
                addr  = data.getAddress().toString()
                dt    = data.getDataType().getName()
                val   = str(data.getValue()) \
                        if data.getValue() is not None else "[no value]"
                f.write(u"  [{}] {:<20} {:<16} = {}\n".format(
                    addr, label, dt, val))
            except: pass
    println("Saved: " + out("global_vars"))

# ═══════════════════════════════════════════════════════════════
# 12. NON-STRING DEFINED DATA
# ═══════════════════════════════════════════════════════════════
def export_nonstring_data():
    listing = currentProgram.getListing()
    SKIP    = ["string", "unicode", "char"]
    with new_file("nonstring_data", "DEFINED NON-STRING DATA") as f:
        for data in listing.getDefinedData(True):
            try:
                dt_name = data.getDataType().getName().lower()
                if any(s in dt_name for s in SKIP): continue
                addr  = data.getAddress().toString()
                label = data.getLabel() or ""
                val   = str(data.getValue()) \
                        if data.getValue() is not None else "[no value]"
                f.write(u"  [{}] {:<16} len={:<4} label={:<20} val={}\n".format(
                    addr,
                    data.getDataType().getName(),
                    data.getLength(),
                    label, val))
            except: pass
    println("Saved: " + out("nonstring_data"))



# ═══════════════════════════════════════════════════════════════
# COMBINED: pe_metadata + sections + entry_points + thunks +
#           func_properties + global_vars + callgraph
# ═══════════════════════════════════════════════════════════════
def export_binary_info():
    path = OUTPUT_DIR + INPUT_NAME + "_binary_info.txt"
    with io.open(path, "w", encoding="utf-8") as f:

        def section_header(title):
            f.write(u"\n")
            f.write(u"#" * 80 + u"\n")
            f.write(u"# BEGIN: {}\n".format(title))
            f.write(u"#" * 80 + u"\n\n")

        def section_footer(title):
            f.write(u"\n")
            f.write(u"# END: {}\n".format(title))
            f.write(u"#" * 80 + u"\n")

        f.write(u"BINARY : {}\n".format(currentProgram.getName()))
        f.write(u"EXPORT : FULL BINARY INFO\n")
        f.write(u"=" * 80 + u"\n")

        # ── PE METADATA ──────────────────────────────────────────
        section_header("PE METADATA")
        f.write(u"  Image Base : {}\n".format(
            hex(currentProgram.getImageBase().getOffset())))
        f.write(u"  Binary Name: {}\n".format(currentProgram.getName()))
        f.write(u"  Language   : {}\n".format(
            currentProgram.getLanguage().getLanguageID()))
        f.write(u"  Compiler   : {}\n\n".format(
            currentProgram.getCompiler()))
        for opts_name in ["Program Information", "PE Header"]:
            try:
                opts = currentProgram.getOptions(opts_name)
                f.write(u"  [{}]\n".format(opts_name))
                for prop in opts.getOptionNames():
                    try:
                        val = opts.getValueAsString(prop)
                        f.write(u"    {}: {}\n".format(prop, val))
                    except: pass
                f.write(u"\n")
            except: pass
        section_footer("PE METADATA")

        # ── SECTIONS + ENTROPY ───────────────────────────────────
        section_header("SECTIONS + ENTROPY")
        f.write(u"  {:<14} {:<12} {:<12} {:<10} {:<6} {}\n".format(
            "Name","Start","End","Size","Perms","Entropy"))
        f.write(u"  " + u"-" * 70 + u"\n")
        for block in currentProgram.getMemory().getBlocks():
            perms   = ("r" if block.isRead()    else "-") + \
                      ("w" if block.isWrite()   else "-") + \
                      ("x" if block.isExecute() else "-")
            entropy = calc_entropy(block)
            f.write(u"  {:<14} {:<12} {:<12} {:<10} {:<6} {:.4f}\n".format(
                block.getName(),
                block.getStart().toString(),
                block.getEnd().toString(),
                block.getSize(),
                perms, entropy))
        section_footer("SECTIONS + ENTROPY")

        # ── ENTRY POINTS ─────────────────────────────────────────
        section_header("ENTRY POINTS")
        fm = currentProgram.getFunctionManager()
        sm = currentProgram.getSymbolTable()
        for addr in sm.getExternalEntryPointIterator():
            func = fm.getFunctionAt(addr)
            name = func.getName() if func else "??"
            f.write(u"  {}  @  {}\n".format(name, addr.toString()))
        section_footer("ENTRY POINTS")

        # ── THUNK MAPPINGS ───────────────────────────────────────
        section_header("THUNK MAPPINGS")
        for func in fm.getFunctions(True):
            if not func.isThunk(): continue
            try:
                target = func.getThunkedFunction(True)
                if target:
                    f.write(u"  {}@{}  ->  {}@{}\n".format(
                        func.getName(),
                        func.getEntryPoint().toString(),
                        target.getName(),
                        target.getEntryPoint().toString()))
            except: pass
        section_footer("THUNK MAPPINGS")

        # ── FUNCTION PROPERTIES ──────────────────────────────────
        section_header("FUNCTION PROPERTIES")
        entry_addrs = set(
            a.toString() for a in sm.getExternalEntryPointIterator())
        f.write(u"  {:<40} {:<20} {:<16} {:<8} {:<6} {}\n".format(
            "Name@Addr","Convention","ReturnType","Params","Thunk","Flags"))
        f.write(u"  " + u"-" * 110 + u"\n")
        for func in fm.getFunctions(True):
            addr   = func.getEntryPoint().toString()
            name   = func.getName()
            try:   conv = func.getCallingConventionName() or "unknown"
            except: conv = "unknown"
            ret    = func.getReturnType().getName()
            params = func.getParameterCount()
            thunk  = func.isThunk()
            flags  = []
            if func.isExternal():   flags.append("EXTERNAL")
            if addr in entry_addrs: flags.append("ENTRYPOINT")
            f.write(u"  {:<40} {:<20} {:<16} {:<8} {:<6} {}\n".format(
                "{}@{}".format(name, addr),
                conv, ret, params, thunk,
                ",".join(flags)))
        section_footer("FUNCTION PROPERTIES")

        # ── GLOBAL VARIABLES ─────────────────────────────────────
        section_header("GLOBAL VARIABLES")
        listing = currentProgram.getListing()
        for data in listing.getDefinedData(True):
            try:
                label = data.getLabel() or ""
                if not label: continue
                addr  = data.getAddress().toString()
                dt    = data.getDataType().getName()
                val   = str(data.getValue()) \
                        if data.getValue() is not None else "[no value]"
                f.write(u"  [{}] {:<20} {:<16} = {}\n".format(
                    addr, label, dt, val))
            except: pass
        section_footer("GLOBAL VARIABLES")

        # ── CALL GRAPH ───────────────────────────────────────────
        section_header("CALL GRAPH")
        for func in fm.getFunctions(True):
            addr = func.getEntryPoint().toString()
            name = func.getName()
            refs = [r for r in getReferencesTo(func.getEntryPoint())
                    if r.getReferenceType().isCall()]
            f.write(u"{}@{}\n".format(name, addr))
            if refs:
                for r in refs:
                    caller = fm.getFunctionContaining(r.getFromAddress())
                    if caller:
                        f.write(u"  called_by: {}@{}\n".format(
                            caller.getName(),
                            caller.getEntryPoint().toString()))
            else:
                f.write(u"  called_by: [ROOT]\n")
            f.write(u"\n")
        section_footer("CALL GRAPH")

    println("Saved: " + path)

# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════
println("=" * 60)
println("Starting full export for: " + INPUT_NAME)
println("Output dir : " + OUTPUT_DIR)
println("=" * 60)

println("[1/7] Decompiled C + Assembly (4 parts)...")
export_decomp()

println("[2/7] Strings + XRefs...")
export_strings_xrefs()

println("[3/7] Imports + XRefs...")
export_imports_xrefs()

println("[4/7] Comments...")
export_comments()

println("[5/7] Non-String Defined Data...")
export_nonstring_data()

println("[6/7] Binary Info (combined)...")
export_binary_info()

println("=" * 60)
println("ALL DONE. Files saved to: " + OUTPUT_DIR)
println("=" * 60)