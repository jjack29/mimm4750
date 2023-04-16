import sys
from Bio import SeqIO

# Check if the correct number of arguments are provided
if len(sys.argv) != 4:
    print("Usage: python script.py <genbank_file> <cds_file> <protein_specified> (outputs to stdout)")
    sys.exit(1)

# input files
genbank_file = sys.argv[1]
cds_file = sys.argv[2]
protein_specified = sys.argv[3]

# extract metadata
metadata = {}
with open(genbank_file, 'r') as gb:
    records = SeqIO.parse(gb, "genbank")
    for record in records:
        source = list(filter(lambda x: x.type=='source', record.features))
        if len(source) > 0:
            metadata.update({record.name.split('.')[0]: source[0].qualifiers})

# filter glycoprotein from CDS file and export FASTA
with open(cds_file, 'r') as cds:
    records = SeqIO.parse(cds, 'fasta')
    for record in records:
        if protein_specified not in record.description:
            continue
        accno = record.name.split('|')[-1].split('.')[0]
        md = metadata.get(accno, {})
        host = md.get('host', ['NA'])[0]
        country = md.get('country', ['NA'])[0]
        coldate = md.get('collection_date', ['NA'])[0]

        sys.stdout.write(f">{accno}_{host}\n{record.seq}\n")
