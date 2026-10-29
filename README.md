# 🧪 Pharmacol Virtual Lab

An interactive **Computational Pharmacology & Cheminformatics Virtual Laboratory** built with **Python**, **Streamlit**, and **RDKit**. Designed for pharmacy, medicinal chemistry, and life sciences education.

> **Designed by:** Abinash Yadav  
> **Registration Number:** RA2611026050303  
> **Institution:** Department of Pharmacology & Computational Chemistry

Inspired by real-world cheminformatics workflows, **Pharmacol Virtual Lab** enables students and researchers to inspect pharmaceutical drug structures, calculate physicochemical descriptors, explore interactive 2D and 3D conformations, perform QSPR analysis, evaluate Lipinski's Rule of 5, test knowledge via assessments, and export automated laboratory reports.

---

## 🌟 Key Features

### 1. 🏠 Home & Drug Gallery
- Comprehensive introduction to computational pharmacology and cheminformatics.
- Quick-select gallery of prominent pharmaceutical drugs (Aspirin, Paracetamol, Ibuprofen, Morphine, Metformin, Amoxicillin, Atorvastatin, Ciprofloxacin, Caffeine, Omeprazole).
- One-click loading of any drug directly into the active laboratory session.

### 2. 📖 Theory & Fundamentals
- **SMILES (Simplified Molecular Input Line Entry System)**: In-depth explanation of textual structure encoding rules (atoms, aromatic lowercase, implicit/explicit bonds, branches `()`, rings `1..n`).
- **Molecular Descriptors**: Detailed theory on Molecular Weight (MW), LogP (Lipophilicity), TPSA (Topological Polar Surface Area), Hydrogen Bond Donors (HBD), Hydrogen Bond Acceptors (HBA), and Rotatable Bonds.
- **3D Molecular Models**: Guide to representation formats:
  - 🟢 **Ball and Stick**: Atoms as spheres and chemical bonds as cylinders.
  - 🟡 **Stick Model**: Highlights bonding connectivity and valence angles.
  - 🔵 **Space Filling (CPK)**: Illustrates approximate molecular volume and van der Waals radii.
  - ⚫ **Wireframe**: Simplified skeletal representation.
  - 🟣 **Cartoon**: Secondary structure and spatial orientation.

### 3. 🧬 Molecular Visualization Laboratory
- **SMILES Input & Example Selector**: Live RDKit validation with green `✅ Valid Molecular Structure!` verification badge.
- **2D Structure Canvas**: Clear, high-contrast skeletal diagram rendered with RDKit and downloadable as vector SVG.
- **Molecular Information**:
  - Input & Canonical SMILES
  - Molecular Formula
  - Heavy Atom & Total Atom counts (including Hydrogens)
  - Bond counting: Heavy bonds, Sigma (σ) bonds, Pi (π) bonds, and Total bonds (σ + π).
- **Interactive 3D Molecular Structure**:
  - WebGL-powered 3D viewer using **3Dmol.js** with left-drag rotation, scroll zoom, and right-drag pan.
  - Model styles: *Ball and Stick*, *Stick*, *Space Filling*, *Wireframe*, and *Cartoon*.
  - Van der Waals surface overlay with toggle control.
  - Auto-spin and camera reset buttons.
  - 3D conformer export in MOL / SDF format.

### 4. 📊 Molecular Properties Report
- Complete physicochemical descriptor profile computed via RDKit:
  - Molecular Weight, LogP, TPSA, HBD, HBA, Rotatable Bonds, Aromatic Rings, Fraction Csp3, Molar Refractivity.
- **Lipinski's Rule of 5 Evaluation**:
  - MW ≤ 500 Da
  - LogP ≤ 5.0
  - HBD ≤ 5
  - HBA ≤ 10
  - Violation tally and oral bioavailability classification.
- **Veber's Rule** (Rotatable Bonds ≤ 10, TPSA ≤ 140 Å²).
- **ADME & Blood-Brain Barrier (BBB)** permeability prediction.
- Clinical indications and mechanism of action for active pharmaceutical agents.

### 5. 📈 Structure–Property Analysis
- Multi-molecule comparative analysis with preloaded pharmaceutical datasets (Reference Solvents, NSAIDs, Antibiotics, Neuroactive drugs).
- Comparative data table featuring:
  `Molecule | MW | LogP | TPSA | HBD | HBA | Rotatable Bonds | Ring Count`
- Downloadable comparison table in CSV format.
- Interactive correlation plots:
  - Scatter chart: Molecular Weight vs. Lipophilicity (LogP) sized by TPSA.
  - Bar chart: Topological Polar Surface Area across compounds.

### 6. 📝 Assessment
- 12 multiple-choice questions assessing SMILES syntax, bond types, lipophilicity, TPSA, and molecular geometry.
- Instant grading, percentage score, performance evaluation, and detailed explanations for each question.
- Seamless synchronization with the student's final report.

### 7. 📑 Final Project Report
- Automatically gathers student credentials (Name, Registration Number), active drug analysis, 2D structure, descriptors, Lipinski compliance, and assessment score.
- Printable, publication-ready HTML lab report with signature verification sections.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Pip package manager

### Running the Application

1. Open PowerShell or Terminal in the project directory:
   ```bash
   cd "C:\Users\User.DESKTOP-IKLK1DF\.gemini\antigravity\scratch\pharmacol_virtual_lab"
   ```

2. Launch Streamlit:
   ```bash
   py -m streamlit run app.py
   ```
   *(Or simply double-click `run_lab.bat`)*

3. Open your browser at:
   ```
   http://localhost:8501
   ```

---

## 📁 Project Structure

```
pharmacol_virtual_lab/
├── .streamlit/
│   └── config.toml          # Dark theme configuration matching Streamlit app
├── app.py                   # Main Streamlit application and page navigation router
├── chem_utils.py            # RDKit algorithms, descriptors, drug database, SVG/3D conformers
├── components_3d.py         # 3Dmol.js WebGL interactive viewer component
├── run_lab.bat              # One-click launcher for Windows
└── README.md                # Documentation and laboratory guide
```

---

🧪 **Pharmacol Virtual Laboratory** | Developed using Python, Streamlit, and RDKit
