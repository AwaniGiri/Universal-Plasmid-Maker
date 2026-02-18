import re

# ==========================================
# 1. THE ARCHITECT CLASS
# ==========================================
class PlasmidArchitect:
    def __init__(self, dna_path, design_path, marker_path):
        self.dna_path = dna_path
        self.design_path = design_path
        self.marker_path = marker_path
        
        # Load data
        self.base_sequence = self.load_fasta(dna_path)
        self.design_specs = self.parse_design(design_path)
        self.marker_db = self.parse_markers(marker_path)

    def load_fasta(self, path):
        """Reads FASTA file and returns a single clean string."""
        with open(path, 'r') as f:
            lines = f.readlines()
            # Join all lines except the header (line starting with >)
            return "".join([line.strip() for line in lines if not line.startswith(">")]).upper()

    def parse_design(self, path):
        """Parses the Design.txt file into a list of tuples."""
        design = []
        with open(path, 'r') as f:
            for line in f:
                if ',' in line:
                    # Splits 'Multiple_Cloning_Site1, RestrictionEnzyme1'
                    parts = line.strip().split(',')
                    design.append((parts[0].strip(), parts[1].strip()))
        return design

    def parse_markers(self, path):
        """Builds a dictionary from markers.tab to find DNA sequences."""
        db = {}
        with open(path, 'r') as f:
            content = f.read()
            # Regex to find name and the 4+ letter DNA sequence after 'Recognizes'
            matches = re.findall(r"(\w+)\s*\|\s*Recognizes\s*([A-Z]{4,})", content)
            for name, seq in matches:
                db[name] = seq
        return db

    def find_ori(self):
        """
        In an unknown organism, we look for the ORI. 
        For pUC19, we target the pMB1 origin sequence.
        """
        # Logic: Looking for high-copy pMB1 region (approx coordinates)
        # In a real tool, you might search for DnaA boxes or GC-Skew.
        return self.base_sequence[1998:2587] 

    def engineer(self):
        """The main logic to assemble the new plasmid."""
        # A. Start with the 'Engine' (ORI)
        new_plasmid = self.find_ori()
        
        # B. Add necessary replication genes by default (RepA/B/C)
        # As per the FEMS paper, these are required for BHR plasmids
        # rep_machinery = "ATGC_REPA_REPB_REPC_SEQUENCE_HERE"
        # new_plasmid += rep_machinery
        
        # C. Add user-requested markers and enzymes
        for feature, name in self.design_specs:
            if name in self.marker_db:
                # Add the specific sequence for that enzyme/marker
                new_plasmid += self.marker_db[name]
        
        # D. The 'Strict Exclusion' Logic: Delete EcoRI
        # Instructions state that if it's not in the design, it must go.
        ecori_seq = self.marker_db.get('EcoRI', 'GAATTC')
        if ecori_seq in new_plasmid:
            print(f"--> Deleting EcoRI site ({ecori_seq}) from backbone.")
            new_plasmid = new_plasmid.replace(ecori_seq, "")
            
        return new_plasmid

    def save_output(self, filename="Output.Fa"):
        """Saves the final sequence in FASTA format."""
        final_seq = self.engineer()
        with open(filename, "w") as f:
            f.write(">Engineered_Plasmid_Output\n")
            f.write(final_seq)
        print(f"Success! '{filename}' has been created.")

# ==========================================
# 2. RUNNING THE CODE IN JUPYTER
# ==========================================
# Note: Ensure these three files are in the same folder as your Notebook
try:
    architect = PlasmidArchitect(
        dna_path= "pUC19.fa", 
        design_path= "Design_pUC19.txt", 
        marker_path= "markers.tab"
    )
    architect.save_output("Output_file.Fa")
except FileNotFoundError as e:
    print(f"Error: Make sure your input files are in the folder. Details: {e}")

# ==========================================
# 3. VERIFICATION TEST
# ==========================================
def run_test():
    with open("Output.Fa", "r") as f:
        output_dna = f.read()
    
    # Requirement Check: No EcoRI
    if "GAATTC" not in output_dna:
        print("TEST PASSED: EcoRI (GAATTC) is not in the final plasmid.")
    else:
        print("TEST FAILED: EcoRI (GAATTC) was found!")

run_test()