# RevMal — EURECOM 2025/2026
**Reverse Engineering & Malware Analysis** · Prof. Simone Aonzo

> Official course repository: [packmad/RevMal](https://github.com/packmad/RevMal)

---

## Structure

```
.
├── REMIND_CHAL/          # REMIND challenges
└── PYGHIDRA/            # PyGhidra scripting exercises
```

---

## `challenges/` — REMIND

Challenges are available on the course platform (EURECOM credentials required):
🔗 https://revmal.s3.eurecom.fr/remind/


---

## `pyghidra/` — PyGhidra Scripting Exercises

Exercises from the *"Automating Ghidra Scripting with PyGhidra"* slides (Aonzo, 2026).
All scripts operate on the **`bulz_6a5210`** sample.

| File | Hands-on | Goal |
|------|----------|------|
| `01_bulz.py` | Memory Reading | Implement `read_c_string(addr)` — reads a C-string from a given address and returns `bytes` |
| `02_bulz.py` | String Decryption | Reverse `FUN_10001210`, implement the decryption routine in Python |
| `03_bulz.py` | Functions & Listing | Iterate all functions, count instructions per function (`count_instructions(func)`), print name / address / count |
| `04_bulz.py` | Symbols & References | Implement `get_references_to_decrypt_function()` — find all calls to `0x10001210` via `getReferencesTo` + `isCall()` filter |
| `05_bulz.py` | Labels & Comments | For each call to `0x10001210`, read the three PUSH arguments, decrypt the string, create a label with `createLabel()` |


### API Reference

- Online: https://ghidra.re/ghidra_docs/api/
- Offline: `unzip docs/GhidraAPI_javadoc.zip`