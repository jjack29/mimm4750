import sys
from Bio import Phylo, SeqIO
import argparse
import sys

parser = argparse.ArgumentParser(
        description="Progressively remove the longest tips from input tree until we reach target number of tips.")

parser.add_argument("intree", type=argparse.FileType('r'),
        help="input, Newick tree string to reduce")
parser.add_argument("inseqs", type=argparse.FileType('r'),
        help="input, FASTA file")
parser.add_argument("target", type=int, help="input, target number of tips")
parser.add_argument("outtree", type=argparse.FileType('w'),
        help="output, reduced Newick tree")
parser.add_argument("outseqs", type=argparse.FileType('w'),
        help="output, reduced FASTA file")

args = parser.parse_args()

# import sequences
records = SeqIO.parse(args.inseqs, "fasta")
seqs = dict([(r.description, r.seq) for r in records])

# read in tree from file
tr = Phylo.read(args.intree, 'newick')

# check that tree labels match sequence labels
tipnames = [tip.name for tip in tr.get_terminals()]
for header in seqs:
    if header not in seqs:
        print(f"ERROR: label {header} from FASTA not found in tree!")
        sys.exit()

sys.setrecursionlimit(100000)
tips = tr.get_terminals()

if args.target >= len(tips):
    print(f"There are already fewer tips in tree ({len(tips)}) than target ({args.target}), exiting...")
    sys.exit()

while len(tips) > args.target:
    # find shortest tip
    tips = sorted(tips, key=lambda x: x.branch_length)
    parent = tr.prune(tips[0])
    tips = tips[1:]  # remove shortest



Phylo.write(tr, args.outtree, 'newick')

