from Bio import SeqIO, Seq
import argparse
import sys

parser = argparse.ArgumentParser(description="Translate sequences in FASTA file")
parser.add_argument("infile", type=argparse.FileType('r'), 
        help="input, FASTA file of nucleotide sequences")
args = parser.parse_args()

records = SeqIO.parse(args.infile, "fasta")
for record in records:
    seq = str(record.seq).replace('-', 'N')
    sys.stdout.write(f">{record.description}\n{Seq.Seq(seq).translate()}\n")


