"""
Chemistry and Pharmacology Utility Functions for Pharmacol Virtual Lab.
Provides RDKit calculations, drug database, descriptor extractions,
2D/3D structure rendering, and Lipinski's Rule of 5 evaluation.
"""

from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, rdMolDescriptors, AllChem
from rdkit.Chem.Draw import rdMolDraw2D
import base64
import html

# Predefined comprehensive database of pharmaceutical drugs and reference compounds
PHARMA_DRUG_DATABASE = {
    "Paracetamol": {
        "smiles": "CC(=O)Nc1ccc(O)cc1",
        "category": "Analgesic & Antipyretic",
        "indication": "Mild to moderate pain relief, fever reduction (first-line in pediatric care)",
        "mechanism": "Inhibition of central COX enzymes and cannabinoid receptor vanilloid-1 (TRPV1) activation via AM404 metabolite.",
        "formula": "C8H9NO2"
    },
    "Ibuprofen": {
        "smiles": "CC(C)Cc1ccc(cc1)C(C)C(=O)O",
        "category": "NSAID (Propionic Acid Derivative)",
        "indication": "Dysmenorrhea, osteoarthritis, rheumatoid arthritis, mild to moderate inflammatory pain",
        "mechanism": "Reversible, non-selective competitive inhibition of COX-1 and COX-2 enzymes.",
        "formula": "C13H18O2"
    },
    "Amoxicillin": {
        "smiles": "CC1(C(N2C(S1)C(C2=O)NC(=O)C(c3ccc(cc3)O)N)C(=O)O)C",
        "category": "Antibiotic (Aminopenicillin)",
        "indication": "Respiratory tract infections, otitis media, H. pylori eradication, UTI",
        "mechanism": "Binds penicillin-binding proteins (PBPs), inhibiting the transpeptidation stage of bacterial cell wall peptidoglycan synthesis.",
        "formula": "C16H19N3O5S"
    },
    "Atenolol": {
        "smiles": "CC(C)NCC(O)COc1ccc(CC(N)=O)cc1",
        "category": "Beta-Blocker (Cardiovascular / Antihypertensive)",
        "indication": "Hypertension, angina pectoris, cardiac arrhythmias, post-myocardial infarction cardioprotection",
        "mechanism": "Cardioselective beta-1 adrenergic receptor antagonist, reducing heart rate, cardiac contractility, and blood pressure.",
        "formula": "C14H22N2O3"
    },
    "Metformin": {
        "smiles": "CN(C)C(=N)NC(=N)N",
        "category": "Antidiabetic (Biguanide)",
        "indication": "First-line oral treatment for Type 2 Diabetes Mellitus, PCOS",
        "mechanism": "Activates AMP-activated protein kinase (AMPK), decreasing hepatic gluconeogenesis and increasing peripheral insulin sensitivity.",
        "formula": "C4H11N5"
    },
    "Ciprofloxacin": {
        "smiles": "C1CC1n2cc(c(=O)c3cc(c(cc23)N4CCNCC4)F)C(=O)O",
        "category": "Antibiotic (Fluoroquinolone)",
        "indication": "Complicated urinary tract infections, severe gastroenteritis, anthrax post-exposure prophylaxis",
        "mechanism": "Inhibits bacterial DNA gyrase (topoisomerase II) and topoisomerase IV, preventing DNA supercoiling and replication.",
        "formula": "C17H18FN3O3"
    },
    "Morphine": {
        "smiles": "CN1CCC23C4C1Cc5ccc(O)c2c5OC4C(O)C=C3",
        "category": "Opioid Analgesic",
        "indication": "Severe acute and chronic pain, palliative care, acute pulmonary edema",
        "mechanism": "Potent agonist at mu-opioid (MOR) receptors in the CNS and peripheral nervous system, hyperpolarizing neuronal membranes.",
        "formula": "C17H19NO3"
    },
    "Atorvastatin": {
        "smiles": "CC(C)c1c(c(c(n1CCC(CC(CC(=O)O)O)O)c2ccc(cc2)F)c3ccccc3)C(=O)Nc4ccccc4",
        "category": "Statin (HMG-CoA Reductase Inhibitor)",
        "indication": "Hypercholesterolemia, cardiovascular risk reduction, prevention of stroke and heart attack",
        "mechanism": "Competitive inhibition of 3-hydroxy-3-methylglutaryl-coenzyme A (HMG-CoA) reductase, upregulating hepatic LDL receptors.",
        "formula": "C33H35FN2O5"
    },
    "Omeprazole": {
        "smiles": "COc1ccc2[nH]c(S(=O)Cc3ncc(C)c(OC)c3C)nc2c1",
        "category": "Proton Pump Inhibitor (PPI)",
        "indication": "Gastroesophageal reflux disease (GERD), peptic ulcer disease, Zollinger-Ellison syndrome",
        "mechanism": "Irreversible covalent inhibition of the H+/K+ ATPase enzyme system at the secretory surface of the gastric parietal cell.",
        "formula": "C17H19N3O3S"
    },
    "Diazepam": {
        "smiles": "CN1C(=O)CN=C(c2ccccc2)c3cc(Cl)ccc13",
        "category": "Benzodiazepine (Anxiolytic/Anticonvulsant)",
        "indication": "Anxiety disorders, alcohol withdrawal, acute muscle spasm, status epilepticus",
        "mechanism": "Positive allosteric modulator of GABA-A receptors, facilitating GABA-mediated opening of chloride channels.",
        "formula": "C16H13ClN2O"
    },
    "Dopamine": {
        "smiles": "NCCc1ccc(O)c(O)c1",
        "category": "Catecholamine & Inotrope",
        "indication": "Cardiogenic shock, severe hypotension, renal hypoperfusion",
        "mechanism": "Stimulates peripheral D1 dopaminergic receptors (low dose), beta-1 adrenergic receptors (medium dose), and alpha-1 receptors (high dose).",
        "formula": "C8H11NO2"
    },
    "Penicillin G": {
        "smiles": "CC1(C(N2C(S1)C(C2=O)NC(=O)Cc3ccccc3)C(=O)O)C",
        "category": "Beta-Lactam Antibiotic",
        "indication": "Streptococcal infections, syphilis, meningococcal meningitis, endocarditis",
        "mechanism": "Inhibits cell wall biosynthesis in Gram-positive bacteria by binding to and inactivating transpeptidases.",
        "formula": "C16H18N2O4S"
    },
    "Nicotine": {
        "smiles": "CN1CCCC1c2cccnc2",
        "category": "Alkaloid / Nicotinic Agonist",
        "indication": "Smoking cessation replacement therapy",
        "mechanism": "Agonist at nicotinic acetylcholine receptors (nAChRs), stimulating neurotransmitter release (dopamine, acetylcholine).",
        "formula": "C10H14N2"
    }
}


def parse_smiles(smiles_str: str):
    """Parses and sanitizes a SMILES string, returning an RDKit Mol object or None."""
    if not smiles_str or not smiles_str.strip():
        return None
    try:
        mol = Chem.MolFromSmiles(smiles_str.strip())
        return mol
    except Exception:
        return None


def get_bond_counts(mol):
    """
    Computes heavy bonds, sigma bonds, pi bonds, and total bonds (sigma + pi).
    Returns (heavy_bonds, sigma_bonds, pi_bonds, total_bonds).
    """
    heavy_bonds = mol.GetNumBonds()
    mol_h = Chem.AddHs(mol)
    sigma_bonds = mol_h.GetNumBonds()

    try:
        kek_mol = Chem.Mol(mol_h)
        Chem.Kekulize(kek_mol, clearAromaticFlags=True)
        pi_bonds = sum(1 for b in kek_mol.GetBonds() if b.GetBondTypeAsDouble() == 2.0) + \
                   sum(2 for b in kek_mol.GetBonds() if b.GetBondTypeAsDouble() == 3.0)
    except Exception:
        # Fallback if kekulization cannot clear flags
        pi_bonds = sum(1 for b in mol.GetBonds() if b.GetBondTypeAsDouble() == 2.0) + \
                   sum(2 for b in mol.GetBonds() if b.GetBondTypeAsDouble() == 3.0)

    total_bonds = sigma_bonds + pi_bonds
    return heavy_bonds, sigma_bonds, pi_bonds, total_bonds


def get_molecular_info(mol, input_smiles: str):
    """Extracts basic molecular details for visualization page."""
    mol_h = Chem.AddHs(mol)
    canonical = Chem.MolToSmiles(mol)
    formula = rdMolDescriptors.CalcMolFormula(mol)
    heavy_atoms = mol.GetNumHeavyAtoms()
    total_atoms = mol_h.GetNumAtoms()
    heavy_bonds, sigma_bonds, pi_bonds, total_bonds = get_bond_counts(mol)
    formal_charge = Chem.GetFormalCharge(mol)
    num_rings = rdMolDescriptors.CalcNumRings(mol)
    aromatic_rings = rdMolDescriptors.CalcNumAromaticRings(mol)

    return {
        "input_smiles": input_smiles,
        "canonical_smiles": canonical,
        "formula": formula,
        "heavy_atoms": heavy_atoms,
        "total_atoms": total_atoms,
        "heavy_bonds": heavy_bonds,
        "sigma_bonds": sigma_bonds,
        "pi_bonds": pi_bonds,
        "total_bonds": total_bonds,
        "formal_charge": formal_charge,
        "num_rings": num_rings,
        "aromatic_rings": aromatic_rings
    }


def get_descriptors(mol):
    """Calculates all key cheminformatic and pharmacological descriptors."""
    mw = round(float(Descriptors.MolWt(mol)), 3)
    logp = round(float(Descriptors.MolLogP(mol)), 3)
    tpsa = round(float(Descriptors.TPSA(mol)), 2)
    hbd = int(Lipinski.NumHDonors(mol))
    hba = int(Lipinski.NumHAcceptors(mol))
    rotb = int(Lipinski.NumRotatableBonds(mol))
    rings = int(rdMolDescriptors.CalcNumRings(mol))
    aromatic_rings = int(rdMolDescriptors.CalcNumAromaticRings(mol))
    fcsp3 = round(float(rdMolDescriptors.CalcFractionCSP3(mol)), 3)
    mr = round(float(Descriptors.MolMR(mol)), 2)

    return {
        "MW": mw,
        "LogP": logp,
        "TPSA": tpsa,
        "HBD": hbd,
        "HBA": hba,
        "Rotatable Bonds": rotb,
        "Ring Count": rings,
        "Aromatic Rings": aromatic_rings,
        "Fraction Csp3": fcsp3,
        "Molar Refractivity": mr
    }


def evaluate_lipinski(descriptors):
    """
    Evaluates Lipinski's Rule of 5 and Veber's criteria.
    Returns details on rule compliance and violations count.
    """
    rules = [
        {"name": "Molecular Weight (MW <= 500 Da)", "value": descriptors["MW"], "limit": "<= 500 Da", "pass": descriptors["MW"] <= 500.0},
        {"name": "LogP (Lipophilicity <= 5.0)", "value": descriptors["LogP"], "limit": "<= 5.0", "pass": descriptors["LogP"] <= 5.0},
        {"name": "H-Bond Donors (HBD <= 5)", "value": descriptors["HBD"], "limit": "<= 5", "pass": descriptors["HBD"] <= 5},
        {"name": "H-Bond Acceptors (HBA <= 10)", "value": descriptors["HBA"], "limit": "<= 10", "pass": descriptors["HBA"] <= 10}
    ]
    violations = sum(1 for r in rules if not r["pass"])
    
    veber_rules = [
        {"name": "Rotatable Bonds <= 10", "value": descriptors["Rotatable Bonds"], "limit": "<= 10", "pass": descriptors["Rotatable Bonds"] <= 10},
        {"name": "TPSA <= 140 A^2", "value": descriptors["TPSA"], "limit": "<= 140 A^2", "pass": descriptors["TPSA"] <= 140.0}
    ]
    veber_violations = sum(1 for r in veber_rules if not r["pass"])

    # Predicted Oral Bioavailability
    if violations == 0 and veber_violations == 0:
        oral_status = "High (Optimal Drug-Likeness)"
        oral_color = "#2ec4b6"
    elif violations <= 1:
        oral_status = "Moderate (Acceptable with 1 violation)"
        oral_color = "#e9c46a"
    else:
        oral_status = f"Poor ({violations} Lipinski violations)"
        oral_color = "#e76f51"

    # Predicted Blood-Brain Barrier (BBB) Permeability
    # Typically LogP 1.5 - 2.7, MW < 400, TPSA < 90
    if descriptors["MW"] < 400 and descriptors["TPSA"] < 90 and 1.0 <= descriptors["LogP"] <= 3.5:
        bbb_prediction = "Likely Permeable (Favorable CNS profile)"
    else:
        bbb_prediction = "Low Permeability (Likely Peripheral / Non-CNS)"

    return {
        "rules": rules,
        "violations": violations,
        "veber_rules": veber_rules,
        "veber_violations": veber_violations,
        "oral_status": oral_status,
        "oral_color": oral_color,
        "bbb_prediction": bbb_prediction
    }


def generate_2d_svg(mol, width=380, height=260):
    """Draws 2D chemical structure and returns clean inline SVG string."""
    try:
        drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
        opts = drawer.drawOptions()
        opts.clearBackground = True
        opts.bondLineWidth = 2.0
        drawer.DrawMolecule(mol)
        drawer.FinishDrawing()
        svg = drawer.GetDrawingText()
        return svg
    except Exception as e:
        return f"<div style='color:red;'>Could not render 2D structure: {html.escape(str(e))}</div>"


def generate_3d_molblock(mol):
    """
    Generates 3D coordinates using RDKit conformer embedding (ETKDG / MMFF).
    Returns (molblock_string, pdb_string, error_message).
    """
    try:
        mol_3d = Chem.AddHs(mol)
        res = AllChem.EmbedMolecule(mol_3d, randomSeed=42, useExpTorsionAnglePrefs=True, useBasicKnowledge=True)
        if res == -1:
            # Fallback to standard embedding
            res = AllChem.EmbedMolecule(mol_3d, randomSeed=42)
        if res != -1:
            try:
                AllChem.MMFFOptimizeMolecule(mol_3d, maxIters=500)
            except Exception:
                try:
                    AllChem.UFFOptimizeMolecule(mol_3d, maxIters=500)
                except Exception:
                    pass
        else:
            # Fallback: compute 2D coordinates so at least coordinates exist
            AllChem.Compute2DCoords(mol_3d)

        molblock = Chem.MolToMolBlock(mol_3d)
        pdb_str = Chem.MolToPDBBlock(mol_3d)
        return molblock, pdb_str, None
    except Exception as e:
        return None, None, str(e)
