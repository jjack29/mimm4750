from Bio import SeqIO
import argparse
import sys

parser = argparse.ArgumentParser(
    description="Apply AA alignment to the original, aligned nucleotide "
                "sequences.  This produces a codon-aware alignment where "
                "gaps respect codon boundaries.")
parser.add_argument("aa", type=argparse.FileType('r'), help="input, AA alignment")
parser.add_argument("nuc", type=argparse.FileType('r'), help="input, nuc sequences")
args = parser.parse_args()

records = SeqIO.parse(args.aa, "fasta")
amino = dict([(r.description, r.seq) for r in records])
records = SeqIO.parse(args.nuc, "fasta")
nuc = dict([(r.description, r.seq) for r in records])

for header, aaseq in amino.items():
    nucseq = nuc.get(header, None)
    if nucseq is None:
        print(f"ERROR: failed to retrieve {header} from nucleotide file")
        sys.exit()
    newseq = ''
    i = 0
    for aa in aaseq:
        if aa == '-':
            newseq += '---'
            continue
        newseq += nucseq[i:(i+3)]
        i += 3
    sys.stdout.write(f">{header}\n{newseq}\n")

