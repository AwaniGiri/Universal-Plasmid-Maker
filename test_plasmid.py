from plasmid_architect import PlasmidArchitect

def test_ecori_removal():
    architect = PlasmidArchitect(
        dna_path="pUC19.fa",
        design_path="Design_pUC19.txt",
        marker_path="markers.tab"
    )

    architect.save_output("Output.Fa")

    with open("Output.Fa") as f:
        seq = f.read()

    assert "GAATTC" not in seq
    print(" TEST PASSED: EcoRI site successfully removed.")

if __name__ == "__main__":
    test_ecori_removal()

