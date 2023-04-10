from Bio import SeqIO

# input and output files
genbank_file = "query.gb"
cds_file = "query.cds.fa"
output_file = "polymerase.fa"

# extract metadata
metadata = {}
with open(genbank_file, 'r') as gb:
    records = SeqIO.parse(gb, "genbank")
    for record in records:
        source = list(filter(lambda x: x.type=='source', record.features))
        if len(source) > 0:
            metadata.update({record.name.split('.')[0]: source[0].qualifiers})

# filter RNA polymerase proteins from CDS file and export FASTA
with open(cds_file, 'r') as cds, open(output_file, 'w') as outfile:
    records = SeqIO.parse(cds, 'fasta')
    for record in records:
        if 'polymerase' not in record.description:
            continue
        accno = record.name.split('|')[-1].split('.')[0]

        md = metadata.get(accno, {})
        organism = md.get('organism', ['NA'])[0]
        host = md.get('host', ['NA'])[0]
        country = md.get('country', ['NA'])[0]
        coldate = md.get('collection_date', ['NA'])[0]

        outfile.write(f">{accno} {organism} {host} {country} {coldate}\n{record.seq}\n")
