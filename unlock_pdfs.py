import json
from pathlib import Path

from pypdf import PdfReader, PdfWriter


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
CONFIG_FILE = BASE_DIR / "config.json"


# ============================================================
# LOAD PASSWORDS
# ============================================================

try:
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        config = json.load(file)

    passwords = config["passwords"]

except FileNotFoundError:
    print("ERROR: config.json not found.")
    exit()

except (json.JSONDecodeError, KeyError):
    print("ERROR: config.json is invalid.")
    exit()


if not passwords:
    print("ERROR: No passwords configured.")
    exit()


# ============================================================
# CHECK FOLDERS
# ============================================================

if not INPUT_DIR.exists():
    print(f"ERROR: Input folder does not exist:")
    print(INPUT_DIR)
    exit()


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# FIND ALL PDF FILES
# ============================================================

pdf_files = sorted(
    file
    for file in INPUT_DIR.iterdir()
    if file.is_file() and file.suffix.lower() == ".pdf"
)


if not pdf_files:
    print("No PDF files found.")
    exit()


# ============================================================
# DETERMINE UNIQUE PREFIXES
# ============================================================

prefix_counts = {}

for pdf in pdf_files:

    if "_" in pdf.stem:
        prefix = pdf.stem.split("_", 1)[0]
    else:
        prefix = pdf.stem

    prefix_counts[prefix] = prefix_counts.get(prefix, 0) + 1


# ============================================================
# HEADER
# ============================================================

print()
print("=" * 70)
print("PDF UNLOCKER")
print("=" * 70)

print(f"Input folder : {INPUT_DIR}")
print(f"Output folder: {OUTPUT_DIR}")
print(f"PDFs found   : {len(pdf_files)}")

print("=" * 70)
print()


# ============================================================
# COUNTERS
# ============================================================

successful = 0
failed = 0
already_unlocked = 0


# ============================================================
# PROCESS EACH PDF
# ============================================================

for pdf_path in pdf_files:

    print(f"Processing: {pdf_path.name}")

    try:

        # ----------------------------------------------------
        # Open PDF
        # ----------------------------------------------------

        reader = PdfReader(pdf_path)

        print(f"  Encrypted: {reader.is_encrypted}")


        # ----------------------------------------------------
        # Decrypt PDF
        # ----------------------------------------------------

        if reader.is_encrypted:

            unlocked = False

            for password_number, password in enumerate(
                passwords,
                start=1
            ):

                result = reader.decrypt(password)

                print(
                    f"  Password {password_number}: "
                    f"result = {result}"
                )

                if result != 0:

                    print(
                        f"  Password {password_number} accepted."
                    )

                    unlocked = True
                    break


            if not unlocked:

                print(
                    "  FAILED: None of the passwords worked."
                )

                failed += 1
                print()

                continue

        else:

            print("  PDF is already unlocked.")

            already_unlocked += 1


        # ----------------------------------------------------
        # CREATE OUTPUT NAME
        # ----------------------------------------------------

        if "_" in pdf_path.stem:

            short_name = pdf_path.stem.split("_", 1)[0]

            # Use shortened name only when unique
            if prefix_counts[short_name] == 1:

                output_filename = (
                    short_name
                    + "_unlk"
                    + pdf_path.suffix
                )

            else:

                output_filename = (
                    pdf_path.stem
                    + "_unlk"
                    + pdf_path.suffix
                )

        else:

            output_filename = (
                pdf_path.stem
                + "_unlk"
                + pdf_path.suffix
            )


        # ----------------------------------------------------
        # OUTPUT PATH
        # ----------------------------------------------------

        output_path = OUTPUT_DIR / output_filename


        # ----------------------------------------------------
        # DON'T OVERWRITE EXISTING FILE
        # ----------------------------------------------------

        if output_path.exists():

            counter = 2

            original_output = output_path

            while output_path.exists():

                output_path = (
                    OUTPUT_DIR
                    / (
                        f"{original_output.stem}"
                        f"_{counter}"
                        f"{original_output.suffix}"
                    )
                )

                counter += 1


        # ----------------------------------------------------
        # CREATE NEW PDF
        # ----------------------------------------------------

        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)


        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        with open(output_path, "wb") as output_file:

            writer.write(output_file)


        print(
            f"  SUCCESS: {output_path.name}"
        )

        successful += 1

    except Exception as error:

        print(
            f"  ERROR: {type(error).__name__}: {error}"
        )

        failed += 1

    print()


# ============================================================
# SUMMARY
# ============================================================

print("=" * 70)
print("PROCESSING COMPLETE")
print("=" * 70)

print(f"Total PDFs       : {len(pdf_files)}")
print(f"Successful       : {successful}")
print(f"Already unlocked : {already_unlocked}")
print(f"Failed           : {failed}")

print()
print(f"Output folder:")
print(OUTPUT_DIR)

print("=" * 70)