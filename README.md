
# PDF Unlocker

A lightweight Python utility for batch-processing password-protected PDF files.

PDF Unlocker automatically scans an input folder, tries a list of configured passwords, decrypts PDFs when the correct password is found, and saves a new unlocked copy to the output folder.

The original PDF files are never modified.

---

## Features

- 🔐 Supports password-protected PDF files
- 🔑 Supports multiple passwords
- ⚡ Automatically tries each configured password
- 📄 Processes multiple PDFs in a single run
- 🔓 Creates unlocked copies while preserving the original files
- 🗂️ Automatically scans the `input` folder for PDF files
- 📁 Automatically creates the `output` folder if required
- ✂️ Shortens long filenames when a unique identifier is available
- 🛡️ Handles duplicate filenames safely
- 🔒 Supports AES-encrypted PDFs
- 📊 Displays a processing summary when complete
- ⚙️ Keeps passwords in a separate configuration file

---

## How It Works

The program follows this workflow:

```text
PDF files
    │
    ▼
 input/
    │
    ▼
Read config.json
    │
    ▼
Try Password 1
    │
    ├── Success ──────► Decrypt PDF
    │
    └── Failed
            │
            ▼
       Try Password 2
            │
            ├── Success ──► Decrypt PDF
            │
            └── Failed ───► Report failure
                           
    │
    ▼
 output/
    │
    ▼
Unlocked PDF
```
