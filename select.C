void select() {
    // Open the original file
    TFile *f_in = TFile::Open("dataSideband_Bu.root");
    TTree *tree = (TTree*)f_in->Get("tree");

    // Get all Float type branches
    TObjArray *branches = tree->GetListOfBranches();
    std::vector<TBranch*> float_branches;
    std::vector<float*> float_ptrs;

    for (int i = 0; i < branches->GetEntries(); ++i) {
        TBranch *br = (TBranch*)branches->At(i);
        TLeaf *leaf = br->GetLeaf(br->GetName());
        if (leaf && strcmp(leaf->GetTypeName(), "Float_t") == 0 && leaf->GetLen() == 1) {
            float *ptr = new float;
            tree->SetBranchAddress(br->GetName(), ptr);
            float_branches.push_back(br);
            float_ptrs.push_back(ptr);
        }
    }

    // Create output file and empty tree structure
    TFile *f_out = TFile::Open("TMVAsideband_Bu.root", "RECREATE");
    TTree *new_tree = tree->CloneTree(0);  // clone structure only

    Long64_t nEntries = tree->GetEntries();
    Long64_t kept = 0;

    for (Long64_t i = 0; i < nEntries; ++i) {
        tree->GetEntry(i);
        bool valid = true;

        for (float *val : float_ptrs) {
            if (!std::isfinite(*val)) {
                valid = false;
                break;
            }
        }

        if (valid) {
            new_tree->Fill();  // Fill new_tree with current tree entry
            ++kept;
        }
    }

    new_tree->Write();
    f_out->Close();
    f_in->Close();

    //for (float *ptr : float_ptrs) delete ptr;

    printf("Selection completed: original entries = %lld, kept entries = %lld\n", nEntries, kept);
}
