# Universal Plasmid Maker

This tool constructs a functional plasmid by:

- Detecting the Origin of Replication (ORI)
- Modifying restriction enzyme sites using a design file
- Handling biological marker references robustly
- Generating a final plasmid DNA sequence in FASTA format

## Input Files

- pUC19.fa – plasmid sequence (test case)
- Design_pUC19.txt – plasmid design instructions
- markers.tab – biological reference file

## Output

- Output.Fa – engineered plasmid sequence

## Test Case

Using pUC19.fa and Design_pUC19.txt, the EcoRI restriction site (GAATTC) is removed from the final plasmid.

## How to Run

python plasmid_architect.py

## Testing

python test_plasmid.py
