#@runtime PyGhidra


def get_references_to_decrypt_function():
    addr = toAddr(0x10001210)

    references = getReferencesTo(addr)
    references_is_call = []

    for ref in references:
        if ref.getReferenceType().isCall():
            references_is_call.append(ref) 

    return references_is_call    


xrefs = get_references_to_decrypt_function()
for xref in xrefs:
    print(hex(xref.getFromAddress().getOffset()))
