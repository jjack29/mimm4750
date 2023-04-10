Data Pipeline for MIMM 4750G final project

Goal:

Data Collection: 
    - Nucleotide sequences along with corresponding metadata obtained from GenBank database (in GenBank format)
    - Entrez Direct esearch and efetch commands used to retrieve data
    - Filters:
        - Only sequences containing spliced together regions of all 5 essential protein-coding genes (nucleoprotein, phosphoprotein, matrix protein, glycoprotein, RNA polymerase)
            - Specified by complete_cds AND nucleoprotein AND phosphoprotein AND matrix AND glycoprotein AND polymerase
        - Only sequences between 10,000 and 12,000 nucleotides in length
        - Search restricted to taxonomy ID 11286 (lyssavirus genus)
        - Sequences from samples obtained from vaccines were omitted (NOT vaccine)
    - Command:
        $ esearch -db nucleotide -query 'txid11286[Organism:exp] AND complete_cds AND nucleoprotein AND phosphoprotein AND matrix AND glycoprotein AND polymerase AND 10000:12000[slen] NOT vaccine' | efetch -format genbank > query.gb

Data Processing:
    - Convert GenBank format to FASTA, while appending the host organism to the header line for each entry
        - See gbToFasta_concatenateHost.py script
        - Creates queryNuc.fasta using query.gb 
    
    - Convert nucleotide FASTA file to amino acid FASTA file, trim 3' end if sequence is not divisible by 3
        - See nucFasta_to_aaFasta.py
        - Creates queryAA.fasta using queryNuc.fasta
    
    - Perform multiple sequence alignment using MAFFT
        - Command:
            $ mafft queryAA.fasta > queryAA.mafft.fasta

    - Use phangorn 


