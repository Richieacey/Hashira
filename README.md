# README.md

# hashira

**hashira** is a Kali-style password hash cracking tool written in Python.  
It is intended for **educational use and authorized security testing only**.

hashira demonstrates how modern cracking tools work internally, including efficient wordlist processing, multiprocessing, early-exit logic, and clean CLI design.

---

## Features

- Supports **MD5, SHA1, SHA256**
- multiprocessing design
- Early exit when all hashes are cracked
- Supports `hash:salt` format and global salt
- Large wordlist handling (rockyou.txt)
- Colored terminal output
- Clean, Kali-style CLI

---

## Requirements

- Python **3.9+**
- Linux (tested on Kali)
- No external Python dependencies

---

## Installation (from source)

```bash
git clone https://github.com/Richieacey/Hashira.git
cd Hashira
chmod +x hashira
sudo cp hashira /usr/local/bin/hashira
```

Verify:
```bash
hashira --help
```

---

## Usage

### Crack MD5 hashes
```bash
hashira --md5 -H hashes.txt -w /usr/share/wordlists/rockyou.txt
```

### Specify CPU cores
```bash
hashira --md5 -H hashes.txt -w rockyou.txt -j 2
```

### Increase performance with larger chunks
```bash
hashira --md5 -H hashes.txt -w rockyou.txt --chunk 30000
```

### Output to file
```bash
hashira --md5 -H hashes.txt -w rockyou.txt -o cracked.txt
```

### Hashes with salts
```text
5f4dcc3b5aa765d61d8327deb882cf99:salt
```

---

## Example Output

```text
[+] FOUND (md5) 0192023a7bbd73250516f069df18b500 --> admin123
[*] Checked ~10,000,000 passwords
[*] All hashes cracked. Stopping early.
```

---

## Disclaimer

This tool is provided **for educational purposes and authorized testing only**.
Unauthorized use against systems you do not own or have permission to test is illegal.

The author assumes no liability for misuse.

