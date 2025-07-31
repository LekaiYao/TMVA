import ROOT
from ROOT import TMVA, TFile, TTree, TBranch, TCanvas, TH1F
from array import array
import os
ROOT.gROOT.SetBatch(True)

# -----------------------------
# Configuration parameters
# -----------------------------
model_xml_path = "dataset_test1/weights/TMVAClassification_BDTs.weights.xml"  # Modify to the actual path
#input_data_path = "../optimization/data_Bu_multi.root"
input_data_path = "../optimization/MC_Bu.root"
tree_name = "tree"
output_root = "BDT_applied_output.root"
bdt_score_png = "BDT_score_distribution.png"

# -----------------------------
# Load trained model
# -----------------------------
TMVA.Tools.Instance()
TMVA.PyMethodBase.PyInitialize()

reader = TMVA.Reader("!Color:!Silent")

# Create arrays to hold variable values
B_alpha = array('f', [0.])
B_trk1dR = array('f', [0.])

# Add variables to the reader
reader.AddVariable("B_alpha", B_alpha)
reader.AddVariable("B_trk1dR", B_trk1dR)

# Load the trained BDT model
reader.BookMVA("BDT", model_xml_path)

# -----------------------------
# Load input data
# -----------------------------
input_file = TFile.Open(input_data_path)
tree = input_file.Get(tree_name)

# Output file (optional: to save a new tree including BDT score)
output_file = TFile.Open(output_root, "RECREATE")
new_tree = tree.CloneTree(0)  # Create a new tree with the same structure

# Add new branch: BDT score
bdt_score = array('f', [0.])
bdt_branch = new_tree.Branch("BDT_score", bdt_score, "BDT_score/F")

# -----------------------------
# Prepare histogram
# -----------------------------
hist_bdt = ROOT.TH1F("hist_bdt", "BDT Score;BDT output;Events", 50, -1, 1)

# -----------------------------
# Loop over events
# -----------------------------
nentries = tree.GetEntries()
print(f"Processing {nentries} entries...")

for i in range(nentries):
    tree.GetEntry(i)
    
    # Assign values to variables
    B_alpha[0] = getattr(tree, "B_alpha")
    B_trk1dR[0] = getattr(tree, "B_trk1dR")
    
    # Evaluate BDT output
    bdt_score[0] = reader.EvaluateMVA("BDT")
    
    # Fill histogram
    hist_bdt.Fill(bdt_score[0])
    
    # Fill new tree
    new_tree.Fill()

# -----------------------------
# Save results
# -----------------------------
output_file.cd()
hist_bdt.Write()
new_tree.Write()

if not hist_bdt:
    raise RuntimeError("Failed to create TH1F histogram!")
c1 = TCanvas("c1", "BDT Output", 800, 600)
hist_bdt.SetLineColor(ROOT.kBlue + 1)
hist_bdt.SetLineWidth(2)
hist_bdt.Draw("HIST")
c1.SaveAs(bdt_score_png)
print(f"BDT score plot saved to: {bdt_score_png}")

output_file.Close()
print(f"Output written to: {output_root}")

# -----------------------------
# Plotting
# -----------------------------
