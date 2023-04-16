import sys

def process_fasta(input_fasta):
    with open(input_fasta, "r") as infile:
        for line in infile:
            if line.startswith(">"):
                header_words = line.split()
                new_header = f">{header_words[3]}"
                print(new_header)
            else:
                print(line.strip())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input.fasta")
        sys.exit(1)

    input_fasta = sys.argv[1]
    process_fasta(input_fasta)
