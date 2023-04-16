Data Pipeline for MIMM 4750G final project

1) Data Collection: 
    - Coding sequence FASTA files along with corresponding metadata obtained from GenBank files
    - Entrez Direct esearch and efetch commands used to retrieve data
    - Filters:
        - Only sequences containing spliced together regions of all 5 essential protein-coding genes (nucleoprotein, phosphoprotein, matrix protein, glycoprotein, RNA polymerase)
        - Only sequences between 10,000 and 12,000 nucleotides in length
        - Search restricted to taxonomy ID 11286 (lyssavirus genus)
        - Sequences from samples obtained from vaccines were omitted (NOT vaccine)
    - Command:
        Obtain CDS FASTA files (2150 sequences = 5*430 sequences):
        $ esearch -db nucleotide -query 'txid11286[Organism:exp] AND complete_cds AND nucleoprotein AND phosphoprotein AND matrix AND glycoprotein AND polymerase AND 10000:12000[slen] NOT vaccine' | efetch -format fasta_cds_na > query.cds.fa
        
        Obtain GenBank files (430 sequences):
        $ esearch -db nucleotide -query 'txid11286[Organism:exp] AND complete_cds AND nucleoprotein AND phosphoprotein AND matrix AND glycoprotein AND polymerase AND 10000:12000[slen] NOT vaccine' | efetch -format genbank > query.gb

2) Data Processing:
    2.a) Use CDS FASTA file and GenBank file to create one file containing their respective protein from each of the samples 
        - Input: query.cds.fa, query.gb
        - Output: nucleoprotein.fa, phosphoprotein.fa, matrix.fa, glycoprotein.fa, polymerase.fa
            - Note, each one contains 430 sequences (one from each sample)
        - Code: python script adapted from Dr. Art Poon's extract_spike.py script for each protein scripts
            $ python3 pyScripts/extract_protein.py query.gb query.cds.fa nucleoprotein > nucleoprotein.fa
            $ python3 pyScripts/extract_protein.py query.gb query.cds.fa phosphoprotein > phosphoprotein.fa
            $ python3 pyScripts/extract_protein.py query.gb query.cds.fa matrix > matrix.fa
            $ python3 pyScripts/extract_protein.py query.gb query.cds.fa glycoprotein > glycoprotein.fa
            $ python3 pyScripts/extract_protein.py query.gb query.cds.fa polymerase > polymerase.fa
            
    
    2.b) Translate the nucleotide sequences, then perform multiple sequence alignment using MAFFT
        - Input: nucleoprotein.fa, phosphoprotein.fa, matrix.fa, glycoprotein.fa, polymerase.fa
        - Output: 
            nucleoprotein_AA.fa, phosphoprotein_AA.fa, matrix_AA.fa, glycoprotein_AA.fa, polymerase_AA.fa
            nucleoprotein_AA.mafft.fa, phosphoprotein_AA.mafft.fa, matrix_AA.mafft.fa, glycoprotein_AA.mafft.fa, polymerase_AA.mafft.fa
        - Code: a python script created by Dr. Art Poon called translate.py was used, the output files were run through MAFFT
            $ python3 pyScripts/translate.py xyz.fa > xyz_AA.mafft.fa
            $ mafft xyz_AA.fa > xyz_AA.mafft.fa

    2.c) Apply AA alignment to the original, aligned nucleotide sequences, producing a codon-aware alignment where gaps respect codon boundaries. 
        - Input: 
            nucleoprotein.fa, phosphoprotein.fa, matrix.fa, glycoprotein.fa, polymerase.fa
            nucleoprotein_AA.mafft.fa, phosphoprotein_AA.mafft.fa, matrix_AA.mafft.fa, glycoprotein_AA.mafft.fa, polymerase_AA.mafft.fa
        - Output: nucleoprotein.codon.fa, phosphoprotein.codon.fa, matrix.codon.fa, glycoprotein.codon.fa, polymerase.codon.fa
        - Code: a python script was adapted from Dr. Art Poon's codon_align.py script to shorten header to host organism
            $ python3 pyScripts/codon_align.py xyz_AA.mafft.fa xyz.fa > xyz.codon.fa
            
    2.d) iqtree performs model selection and produces a phylogenetic tree
        - Input: nucleoprotein.codon.fa, phosphoprotein.codon.fa, matrix.codon.fa, glycoprotein.codon.fa, polymerase.codon.fa
        - Output: nucleoprotein.nwk, phosphoprotein.nwk, matrix.nwk, glycoprotein.nwk, polymerase.nwk, nucleoprotein.iqtree, phosphoprotein.iqtree, matrix.iqtree, glycoprotein.iqtree, polymerase.iqtree
        - Code: 
            $ iqtree -s xyz.condon.fa -pre xyz
            .iqtree and .treefile files are kept as xyz.iqtree and xyz.nwk (all other files produced are deleted)

    2.e) Data reduction: create a reduced tree by progressively removing the shortest branches until we reach 70 tips
        - Input: 
            nucleoprotein.nwk, phosphoprotein.nwk, matrix.nwk, glycoprotein.nwk, polymerase.nwk
            nucleoprotein.codon.fa, phosphoprotein.codon.fa, matrix.codon.fa, glycoprotein.codon.fa, polymerase.codon.fa
        - Output: 
            nucleoprotein.red.nwk, phosphoprotein.red.nwk, matrix.red.nwk, glycoprotein.red.nwk, polymerase.red.nwk
            nucleoprotein.red.fa, phosphoprotein.red.fa, matrix.red.fa, glycoprotein.red.fa, polymerase.red.fa
        - Code: a python script created by Dr. Art Poon called prune-tips.py was used
            $ python3 pyScripts/prune-tips.py xyz.nwk xyz.codon.fa 70 xyz.red.nwk xyz.red.fa        

3) Visualization:
    - FigTree was used to visualize the .nwk files
    - Jalview was used to visualize conservation
