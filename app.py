"""
Pharmacol Virtual Lab - Interactive Computational Pharmacology & Cheminformatics Platform
Built with Python, Streamlit, and RDKit.
"""

import streamlit as st
import pandas as pd
import numpy as np
import base64
import html
import datetime

# Import local chemistry utilities and 3D viewer component
from chem_utils import (
    PHARMA_DRUG_DATABASE,
    parse_smiles,
    get_molecular_info,
    get_descriptors,
    evaluate_lipinski,
    generate_2d_svg,
    generate_3d_molblock
)
from components_3d import render_3dmol_viewer

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Pharmacol Virtual Lab",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Styling for Authentic Virtual Lab Look & Feel
# ---------------------------------------------------------
CUSTOM_CSS = """
<style>
/* Main Dark Theme Styling matching reference images */
body {
    background-color: #0e1117;
    color: #fafafa;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #1a1d24;
    border-right: 1px solid #2d333b;
}

/* Header branding */
.lab-header-title {
    font-size: 26px;
    font-weight: 700;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 2px;
}

/* Cards & containers */
.metric-card {
    background: #1e222b;
    border: 1px solid #2d333b;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
}

.white-structure-card {
    background: #ffffff;
    border-radius: 8px;
    padding: 15px;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    min-height: 280px;
}

.success-banner {
    background-color: #173829;
    border: 1px solid #2d6a4f;
    color: #74c69d;
    padding: 12px 18px;
    border-radius: 6px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 12px 0;
}

.info-banner {
    background-color: #132438;
    border: 1px solid #1d4ed8;
    color: #93c5fd;
    padding: 12px 18px;
    border-radius: 6px;
    font-size: 14px;
    margin-bottom: 16px;
}

/* Model Badges in Theory */
.model-badge {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 17px;
    font-weight: 600;
    margin-top: 15px;
    margin-bottom: 4px;
}

.footer-text {
    font-size: 12px;
    color: #8b949e;
    border-top: 1px solid #2d333b;
    padding-top: 18px;
    margin-top: 36px;
    text-align: left;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "student_name" not in st.session_state:
    st.session_state["student_name"] = "Abinash Yadav"
if "reg_number" not in st.session_state:
    st.session_state["reg_number"] = "RA2611026050303"
if "active_smiles" not in st.session_state:
    st.session_state["active_smiles"] = "CC(=O)Nc1ccc(O)cc1"  # Default Paracetamol
if "active_molecule_name" not in st.session_state:
    st.session_state["active_molecule_name"] = "Paracetamol"
if "model_3d_type" not in st.session_state:
    st.session_state["model_3d_type"] = "Ball and Stick"
if "show_surface" not in st.session_state:
    st.session_state["show_surface"] = False
if "comparison_text" not in st.session_state:
    st.session_state["comparison_text"] = """Paracetamol, CC(=O)Nc1ccc(O)cc1
Ibuprofen, CC(C)Cc1ccc(cc1)C(C)C(=O)O
Amoxicillin, CC1(C(N2C(S1)C(C2=O)NC(=O)C(c3ccc(cc3)O)N)C(=O)O)C
Atenolol, CC(C)NCC(O)COc1ccc(CC(N)=O)cc1"""
if "quiz_submitted" not in st.session_state:
    st.session_state["quiz_submitted"] = False
if "quiz_score" not in st.session_state:
    st.session_state["quiz_score"] = 0
if "quiz_total" not in st.session_state:
    st.session_state["quiz_total"] = 12

# ---------------------------------------------------------
# Sidebar Navigation & Student Information
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧪 Virtual Lab")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e2638 0%, #161b22 100%); padding: 12px 14px; border-radius: 8px; border: 1.5px solid #388bfd; margin-bottom: 14px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
        <div style="font-size: 15px; font-weight: 700; color: #58a6ff; margin-bottom: 4px;">
            👨‍💻 Designed by: Abinash Yadav
        </div>
        <div style="font-size: 14px; font-weight: 600; color: #7ee787;">
            🆔 Registration Number: RA2611026050303
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation matching exactly the screenshots
    nav_selection = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "📖 Theory",
            "🧬 Molecular Visualization",
            "📊 Molecular Properties Report",
            "📈 Structure–Property Analysis",
            "📝 Assessment",
            "📑 Final Project Report"
        ],
        index=2  # Default to Molecular Visualization as commonly explored
    )
    
    st.markdown("---")
    st.markdown("#### 🛡️ Student Information")
    st.session_state["student_name"] = st.text_input(
        "Student Name", 
        value=st.session_state["student_name"],
        placeholder="e.g. John Doe"
    )
    st.session_state["reg_number"] = st.text_input(
        "Registration Number",
        value=st.session_state["reg_number"],
        placeholder="e.g. PHARM-2026-081"
    )

    st.markdown("---")
    st.markdown("#### 🎓 Learning Objectives")
    st.markdown("""
    **Students can learn:**
    - SMILES notation
    - Molecular representation
    - 2D visualization
    - 3D visualization
    - Molecular descriptors
    - Structure-property relationships
    - Lipinski's Rule of 5 and Drug-likeness
    """)


# =========================================================
# PAGE 1: 🏠 Home
# =========================================================
if nav_selection == "🏠 Home":
    st.markdown("## 💊 Welcome to Pharmacol Virtual Laboratory")
    st.markdown("""
    <div style="background: linear-gradient(90deg, #161b26 0%, #1f293d 100%); border: 1.5px solid #388bfd; border-radius: 10px; padding: 16px 22px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; box-shadow: 0 4px 14px rgba(0,0,0,0.35);">
        <span style="color: #7ee787; font-weight: 700; font-size: 16px;">🎓 Academic Virtual Laboratory Platform</span>
        <span style="color: #58a6ff; font-weight: 700; font-size: 17px; letter-spacing: 0.3px;">👨‍💻 Designed by: Abinash Yadav &nbsp;|&nbsp; Registration Number: RA2611026050303</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    **Pharmacol Virtual Lab** is an interactive computational pharmacology and cheminformatics platform.
    Designed for pharmacy, chemistry, and life sciences students, this platform provides state-of-the-art tools
    to inspect molecular structures, decode SMILES notations, generate 3D conformers, evaluate physicochemical 
    descriptors, and investigate structure-property relationships (QSPR & Lipinski's Rule of 5).
    """)

    st.markdown("### 🚀 Laboratory Modules")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>📖 Theory & Concepts</h4>
            <p style="font-size:13px; color:#c9d1d9;">
            Master SMILES line notation rules, molecular descriptors (MW, LogP, TPSA, HBD, HBA),
            and standard 3D molecular representation models.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>🧬 2D & 3D Visualization</h4>
            <p style="font-size:13px; color:#c9d1d9;">
            Render clean 2D skeletal structures and rotate real-time 3D models with Ball & Stick, Space-Filling,
            van der Waals surfaces, and bond counts.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>📈 Structure-Property</h4>
            <p style="font-size:13px; color:#c9d1d9;">
            Perform comparative batch analysis across multiple pharmaceutical drugs, evaluate Lipinski's Rule of 5,
            and export CSV datasets.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 💊 Core Target Pharmaceutical Drugs")
    st.caption("Click any drug card below to quickly load and inspect its molecular structure, properties, and 3D geometry.")

    core_drugs = ["Paracetamol", "Ibuprofen", "Amoxicillin", "Atenolol"]
    cols_core = st.columns(4)
    for idx, drug_name in enumerate(core_drugs):
        with cols_core[idx]:
            drug_data = PHARMA_DRUG_DATABASE[drug_name]
            st.markdown(f"**{drug_name}**")
            st.caption(f"_{drug_data['category']}_")
            if st.button(f"Analyze", key=f"btn_core_{drug_name}", use_container_width=True):
                st.session_state["active_smiles"] = drug_data["smiles"]
                st.session_state["active_molecule_name"] = drug_name
                st.success(f"Loaded {drug_name}! Switch to 'Molecular Visualization' to inspect.")

    st.markdown("---")
    st.markdown("### 📚 Additional Pharmaceutical Library")
    more_drugs = ["Metformin", "Ciprofloxacin", "Morphine", "Atorvastatin", "Omeprazole", "Diazepam"]
    cols_more = st.columns(6)
    for idx, drug_name in enumerate(more_drugs):
        with cols_more[idx]:
            drug_data = PHARMA_DRUG_DATABASE[drug_name]
            st.markdown(f"**{drug_name}**")
            st.caption(f"_{drug_data['category']}_")
            if st.button(f"Analyze", key=f"btn_more_{drug_name}", use_container_width=True):
                st.session_state["active_smiles"] = drug_data["smiles"]
                st.session_state["active_molecule_name"] = drug_name
                st.success(f"Loaded {drug_name}!")


# =========================================================
# PAGE 2: 📖 Theory
# =========================================================
elif nav_selection == "📖 Theory":
    st.markdown("## 📖 Theory")
    st.markdown("It uses computational techniques to store, process, visualize and analyze chemical information.")

    st.markdown("---")
    st.markdown("### SMILES")
    st.markdown("**SMILES** means:")
    st.markdown("#### Simplified Molecular Input Line Entry System")
    st.markdown("It represents a molecular structure using a text string.")

    st.markdown("##### Examples:")
    examples_data = [
        {"Molecule": "Paracetamol", "SMILES": "CC(=O)Nc1ccc(O)cc1", "Class": "Analgesic & Antipyretic"},
        {"Molecule": "Ibuprofen", "SMILES": "CC(C)Cc1ccc(cc1)C(C)C(=O)O", "Class": "NSAID"},
        {"Molecule": "Amoxicillin", "SMILES": "CC1(C(N2C(S1)C(C2=O)NC(=O)C(c3ccc(cc3)O)N)C(=O)O)C", "Class": "Beta-Lactam Antibiotic"},
        {"Molecule": "Atenolol", "SMILES": "CC(C)NCC(O)COc1ccc(CC(N)=O)cc1", "Class": "Beta-Blocker / Antihypertensive"},
        {"Molecule": "Metformin", "SMILES": "CN(C)C(=N)NC(=N)N", "Class": "Antidiabetic (Biguanide)"},
        {"Molecule": "Ciprofloxacin", "SMILES": "C1CC1n2cc(c(=O)c3cc(c(cc23)N4CCNCC4)F)C(=O)O", "Class": "Fluoroquinolone Antibiotic"}
    ]
    st.table(pd.DataFrame(examples_data)[["Molecule", "SMILES", "Class"]])

    st.markdown("""
    **SMILES Encoding Rules:**
    1. **Atoms**: Elements are written as standard periodic symbols (e.g. `C`, `N`, `O`, `P`, `S`, `F`, `Cl`, `Br`, `I`).
    2. **Aromaticity**: Aromatic atoms are denoted in lowercase (`c`, `n`, `o`, `s`).
    3. **Bonds**: Single bonds are implicit. Double bonds are `=`, triple bonds are `#`, and aromatic bonds are `:`.
    4. **Branching**: Substituted branches and functional groups are enclosed in parentheses `(...)`.
    5. **Rings**: Ring openings and closures are designated by matching numbers (e.g. `c1ccccc1` for benzene).
    """)

    st.markdown("---")
    st.markdown("### Molecular Descriptors")
    st.markdown("Molecular descriptors provide numerical information about a chemical structure.")
    st.markdown("""
    **Examples include:**
    - **Molecular Weight (MW)**: Sum of all atomic masses (Daltons / g·mol⁻¹). Influences membrane diffusion.
    - **LogP (Octanol-Water Partition Coefficient)**: Measures molecular lipophilicity vs. hydrophilicity.
    - **TPSA (Topological Polar Surface Area)**: Sum of surfaces of all polar atoms (Å²). Key for predicting intestinal absorption and blood-brain barrier (BBB) penetration.
    - **Hydrogen Bond Donors (HBD)**: Count of O-H and N-H bonds capable of donating protons.
    - **Hydrogen Bond Acceptors (HBA)**: Count of electronegative oxygen and nitrogen atoms capable of accepting hydrogen bonds.
    - **Rotatable Bonds**: Number of non-ring, non-terminal single bonds. Quantifies conformational flexibility.
    - **Lipinski's Rule of 5**: Empirical guidelines predicting whether a compound possesses favorable oral drug-likeness (MW ≤ 500, LogP ≤ 5, HBD ≤ 5, HBA ≤ 10).
    """)

    st.markdown("---")
    st.markdown("### 3D Molecular Models")
    st.markdown("Different visualization models help students understand the molecular geometry.")

    st.markdown('<div class="model-badge">🟢 Ball and Stick</div>', unsafe_allow_html=True)
    st.markdown("Shows atoms as spheres and bonds as sticks.")

    st.markdown('<div class="model-badge">🟡 Stick Model</div>', unsafe_allow_html=True)
    st.markdown("Emphasizes chemical bonding.")

    st.markdown('<div class="model-badge">🔵 Space Filling</div>', unsafe_allow_html=True)
    st.markdown("Shows the approximate molecular volume.")

    st.markdown('<div class="model-badge">⚫ Wireframe</div>', unsafe_allow_html=True)
    st.markdown("Provides a simplified representation of the molecule.")

    st.markdown('<div class="model-badge">🟣 Cartoon</div>', unsafe_allow_html=True)
    st.markdown("Highlights backbone orientation and spatial conformation.")


# =========================================================
# PAGE 3: 🧬 Molecular Visualization
# =========================================================
elif nav_selection == "🧬 Molecular Visualization":
    st.markdown("## 🧬 Molecular Visualization Laboratory")

    # Blue notice banner matching screenshot
    st.markdown("""
    <div class="info-banner">
    Enter a new SMILES or load an example. The selected molecule will be used across the laboratory pages.
    </div>
    """, unsafe_allow_html=True)

    # Input controls row
    c_input, c_select, c_btn = st.columns([2.5, 2.5, 1])

    with c_input:
        current_smiles = st.text_input("Enter SMILES", value=st.session_state["active_smiles"])

    with c_select:
        drug_names = list(PHARMA_DRUG_DATABASE.keys())
        # Try to find current selected molecule index
        default_idx = 0
        if st.session_state["active_molecule_name"] in drug_names:
            default_idx = drug_names.index(st.session_state["active_molecule_name"])
            
        chosen_example = st.selectbox("Choose Example Molecule", drug_names, index=default_idx)

    with c_btn:
        st.write("")
        st.write("")
        if st.button("Load Example", use_container_width=True):
            current_smiles = PHARMA_DRUG_DATABASE[chosen_example]["smiles"]
            st.session_state["active_smiles"] = current_smiles
            st.session_state["active_molecule_name"] = chosen_example
            st.rerun()

    # If the user changed the text input directly
    if current_smiles != st.session_state["active_smiles"]:
        st.session_state["active_smiles"] = current_smiles

    # Parse and validate SMILES with RDKit
    mol = parse_smiles(st.session_state["active_smiles"])

    if mol is None:
        st.error(f"❌ Invalid SMILES notation: `{st.session_state['active_smiles']}`. Please check chemical syntax.")
    else:
        # Green success banner matching screenshot
        st.markdown("""
        <div class="success-banner">
            <span>✅</span> <span>Valid Molecular Structure!</span>
        </div>
        """, unsafe_allow_html=True)

        mol_info = get_molecular_info(mol, st.session_state["active_smiles"])
        descriptors = get_descriptors(mol)

        # Two columns for 2D Structure and Molecular Information
        col_2d, col_info = st.columns([1.1, 1.0])

        with col_2d:
            st.markdown("### 2D Molecular Structure")
            svg_content = generate_2d_svg(mol, width=420, height=270)
            
            # Render inside white background card just like in screenshot!
            st.markdown(f"""
            <div class="white-structure-card">
                {svg_content}
            </div>
            """, unsafe_allow_html=True)
            
            # Download 2D button
            b64_svg = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
            svg_href = f'<a href="data:image/svg+xml;base64,{b64_svg}" download="{st.session_state.get("active_molecule_name", "molecule")}_2d.svg" style="display:inline-block; padding:6px 12px; background:#262b38; color:#79b8ff; border:1px solid #3d4450; border-radius:4px; text-decoration:none; font-size:12px; margin-top:8px;">⬇ Download 2D Structure (SVG)</a>'
            st.markdown(svg_href, unsafe_allow_html=True)

        with col_info:
            st.markdown("### Molecular Information")
            st.markdown(f"**Input SMILES:** `{mol_info['input_smiles']}`")
            st.markdown(f"**Canonical SMILES:** `{mol_info['canonical_smiles']}`")
            st.markdown(f"**Formula:** `{mol_info['formula']}`")
            st.markdown(f"**Heavy Atoms:** {mol_info['heavy_atoms']}")
            st.markdown(f"**Total Atoms (including H):** {mol_info['total_atoms']}")
            st.markdown(f"**Heavy-Atom Bonds:** {mol_info['heavy_bonds']}")
            st.markdown(f"**Sigma (σ) Bonds:** {mol_info['sigma_bonds']}")
            st.markdown(f"**Pi (π) Bonds:** {mol_info['pi_bonds']}")
            st.markdown(f"**Total Bonds (σ + π):** {mol_info['total_bonds']}")

        st.markdown("---")
        st.markdown("### 🌐 Interactive 3D Molecular Structure")

        col_m1, col_m2 = st.columns([2, 2])
        with col_m1:
            model_options = ["Ball and Stick", "Stick", "Space Filling", "Wireframe", "Cartoon"]
            selected_model = st.selectbox(
                "Select Molecular Model", 
                model_options, 
                index=model_options.index(st.session_state.get("model_3d_type", "Ball and Stick"))
            )
            st.session_state["model_3d_type"] = selected_model

        with col_m2:
            st.write("")
            st.write("")
            show_vdw = st.checkbox("Show van der Waals Surface", value=st.session_state.get("show_surface", False))
            st.session_state["show_surface"] = show_vdw

        # Generate 3D Structure button
        if st.button("🚀 Generate 3D Structure", use_container_width=False):
            st.toast("Generating optimized 3D molecular conformer...", icon="⚡")

        # Generate 3D conformer coordinates with RDKit
        molblock, pdb_str, err = generate_3d_molblock(mol)

        if err:
            st.warning(f"Note on 3D generation: {err}")
        if molblock:
            # Render interactive 3Dmol canvas
            viewer_html = render_3dmol_viewer(
                molblock=molblock,
                model_type=st.session_state["model_3d_type"],
                show_surface=st.session_state["show_surface"],
                height=450
            )
            st.components.v1.html(viewer_html, height=470)

            # Download 3D Model file button
            st.download_button(
                label="⬇ Download 3D Conformer (MOL / SDF)",
                data=molblock,
                file_name=f"{st.session_state.get('active_molecule_name', 'molecule')}_3D.mol",
                mime="chemical/x-mdl-molfile"
            )


# =========================================================
# PAGE 4: 📊 Molecular Properties Report
# =========================================================
elif nav_selection == "📊 Molecular Properties Report":
    st.markdown("## 📊 Molecular Properties Report")
    
    mol = parse_smiles(st.session_state["active_smiles"])
    if mol is None:
        st.error(f"Cannot generate properties report: `{st.session_state['active_smiles']}` is not a valid SMILES string.")
    else:
        descriptors = get_descriptors(mol)
        lipinski = evaluate_lipinski(descriptors)
        active_name = st.session_state.get("active_molecule_name", "Selected Compound")
        
        drug_meta = PHARMA_DRUG_DATABASE.get(active_name, {
            "category": "Organic Compound",
            "indication": "Investigational / Research entity",
            "mechanism": "Mechanistic profile under evaluation."
        })

        st.markdown(f"### Target Molecule: **{active_name}** (`{st.session_state['active_smiles']}`)")
        
        # Key metrics row
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("Molecular Weight", f"{descriptors['MW']} Da")
        m2.metric("LogP (Lipophilicity)", f"{descriptors['LogP']}")
        m3.metric("TPSA", f"{descriptors['TPSA']} Å²")
        m4.metric("H-Bond Donors", f"{descriptors['HBD']}")
        m5.metric("H-Bond Acceptors", f"{descriptors['HBA']}")
        m6.metric("Rotatable Bonds", f"{descriptors['Rotatable Bonds']}")

        st.markdown("---")
        
        # Lipinski Rule of 5 Evaluation
        col_l1, col_l2 = st.columns([1.2, 1.0])
        
        with col_l1:
            st.markdown("#### 💊 Lipinski's Rule of 5 Compliance")
            st.caption("Pfizer's Rule of 5 predicts whether a chemical entity possesses properties that confer favorable oral bioavailability.")
            
            rule_rows = []
            for r in lipinski["rules"]:
                status = "✅ PASS" if r["pass"] else "❌ VIOLATION"
                rule_rows.append({
                    "Physicochemical Parameter": r["name"],
                    "Calculated Value": r["value"],
                    "Rule Threshold": r["limit"],
                    "Status": status
                })
            st.table(pd.DataFrame(rule_rows))
            
            st.markdown(f"**Total Lipinski Violations:** `{lipinski['violations']}`")

        with col_l2:
            st.markdown("#### 🔬 ADME & Bioavailability Assessment")
            st.markdown(f"""
            <div class="metric-card">
                <b>Predicted Oral Bioavailability:</b><br>
                <span style="color:{lipinski['oral_color']}; font-size:18px; font-weight:700;">
                    {lipinski['oral_status']}
                </span>
                <br><br>
                <b>Blood-Brain Barrier (BBB) Permeability:</b><br>
                <span style="color:#79b8ff; font-size:14px; font-weight:600;">
                    {lipinski['bbb_prediction']}
                </span>
                <br><br>
                <b>Veber's Rule for Oral Permeability:</b><br>
                <span style="font-size:13px;">
                    Rotatable Bonds ≤ 10: <b>{'Passed' if descriptors['Rotatable Bonds'] <= 10 else 'Violated'}</b><br>
                    TPSA ≤ 140 Å²: <b>{'Passed' if descriptors['TPSA'] <= 140 else 'Violated'}</b>
                </span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🩺 Clinical & Pharmacological Profile")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown(f"**Therapeutic Category:** {drug_meta['category']}")
            st.markdown(f"**Clinical Indications:** {drug_meta['indication']}")
        with col_p2:
            st.markdown(f"**Mechanism of Action:** {drug_meta['mechanism']}")


# =========================================================
# PAGE 5: 📈 Structure–Property Analysis
# =========================================================
elif nav_selection == "📈 Structure–Property Analysis":
    st.markdown("## 📈 Structure–Property Analysis")
    st.markdown("Compare the properties of multiple molecules. Enter one molecule per line in the format:")
    st.markdown("`Molecule Name, SMILES`")

    # Quick presets row
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        if st.button("💊 Core Study Set (4 Target Drugs)"):
            st.session_state["comparison_text"] = """Paracetamol, CC(=O)Nc1ccc(O)cc1
Ibuprofen, CC(C)Cc1ccc(cc1)C(C)C(=O)O
Amoxicillin, CC1(C(N2C(S1)C(C2=O)NC(=O)C(c3ccc(cc3)O)N)C(=O)O)C
Atenolol, CC(C)NCC(O)COc1ccc(CC(N)=O)cc1"""
            st.rerun()
    with p2:
        if st.button("💊 Analgesics & NSAIDs"):
            st.session_state["comparison_text"] = """Paracetamol, CC(=O)Nc1ccc(O)cc1
Ibuprofen, CC(C)Cc1ccc(cc1)C(C)C(=O)O
Naproxen, COc1ccc2cc(ccc2c1)C(C)C(=O)O
Diclofenac, O=C(O)Cc1ccccc1Nc2c(Cl)cccc2Cl
Ketoprofen, CC(C(=O)O)c1cccc(C(=O)c2ccccc2)c1"""
            st.rerun()
    with p3:
        if st.button("🦠 Antibiotics"):
            st.session_state["comparison_text"] = """Amoxicillin, CC1(C(N2C(S1)C(C2=O)NC(=O)C(c3ccc(cc3)O)N)C(=O)O)C
Ciprofloxacin, C1CC1n2cc(c(=O)c3cc(c(cc23)N4CCNCC4)F)C(=O)O
Penicillin G, CC1(C(N2C(S1)C(C2=O)NC(=O)Cc3ccccc3)C(=O)O)C
Sulfamethoxazole, Cc1cc(no1)NS(=O)(=O)c2ccc(N)cc2"""
            st.rerun()
    with p4:
        if st.button("🧠 Neuroactive Compounds"):
            st.session_state["comparison_text"] = """Morphine, CN1CCC23C4C1Cc5ccc(O)c2c5OC4C(O)C=C3
Diazepam, CN1C(=O)CN=C(c2ccccc2)c3cc(Cl)ccc13
Dopamine, NCCc1ccc(O)c(O)c1
Nicotine, CN1CCCC1c2cccnc2
Atenolol, CC(C)NCC(O)COc1ccc(CC(N)=O)cc1"""
            st.rerun()

    # Multiline text area matching screenshot
    input_text = st.text_area(
        "Enter Molecules",
        value=st.session_state["comparison_text"],
        height=140
    )
    st.session_state["comparison_text"] = input_text

    # Parse entries and compute table
    rows = []
    lines = [line.strip() for line in input_text.strip().split("\n") if line.strip()]

    for line in lines:
        parts = [p.strip() for p in line.split(",", 1)]
        if len(parts) == 2:
            name, smiles = parts[0], parts[1]
            m = parse_smiles(smiles)
            if m is not None:
                desc = get_descriptors(m)
                rows.append({
                    "Molecule": name,
                    "MW": desc["MW"],
                    "LogP": desc["LogP"],
                    "TPSA": desc["TPSA"],
                    "HBD": desc["HBD"],
                    "HBA": desc["HBA"],
                    "Rotatable Bonds": desc["Rotatable Bonds"],
                    "Ring Count": desc["Ring Count"]
                })
            else:
                rows.append({
                    "Molecule": f"{name} (Invalid SMILES)",
                    "MW": np.nan, "LogP": np.nan, "TPSA": np.nan,
                    "HBD": 0, "HBA": 0, "Rotatable Bonds": 0, "Ring Count": 0
                })

    df = pd.DataFrame(rows)

    # Render Table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### 📋 Comparison Table")

    # CSV Download Button matching screenshot
    csv_bytes = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇ Download Comparison Table (CSV)",
        data=csv_bytes,
        file_name="pharmacol_comparison_table.csv",
        mime="text/csv"
    )

    # Visual Structure-Property Plots
    st.markdown("---")
    st.markdown("#### 📊 Property Correlation Visualizations")
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("**Molecular Weight vs. Lipophilicity (LogP)**")
        if not df.empty and "MW" in df.columns:
            valid_df = df.dropna(subset=["MW", "LogP"])
            st.scatter_chart(
                valid_df,
                x="MW",
                y="LogP",
                size="TPSA",
                color="Molecule"
            )

    with col_chart2:
        st.markdown("**Polar Surface Area (TPSA in Å²)**")
        if not df.empty and "TPSA" in df.columns:
            valid_df = df.dropna(subset=["TPSA"])
            st.bar_chart(
                valid_df.set_index("Molecule")["TPSA"]
            )


# =========================================================
# PAGE 6: 📝 Assessment
# =========================================================
elif nav_selection == "📝 Assessment":
    st.markdown("## 📝 Cheminformatics & Pharmacol Assessment")
    st.caption("Answer the multiple-choice questions below to test your mastery of molecular representations, SMILES rules, and pharmacological descriptors.")

    # 12 Questions matching screenshot exactly
    quiz_questions = [
        {
            "id": 1,
            "q": "What is the full form of SMILES?",
            "options": [
                "Simplified Molecular Input Line Entry System",
                "Standard Molecular Information Language Encoding System",
                "Simple Molecular Identification and Labeling System"
            ],
            "answer": "Simplified Molecular Input Line Entry System",
            "explain": "SMILES stands for Simplified Molecular Input Line Entry System, invented by Arthur Weininger and David Weininger."
        },
        {
            "id": 2,
            "q": "What does a SMILES string represent?",
            "options": [
                "A molecular structure using text",
                "A spectroscopy technique",
                "A laboratory instrument"
            ],
            "answer": "A molecular structure using text",
            "explain": "A SMILES string is a compact textual specification that describes the 2D connectivity and constitution of a chemical molecule."
        },
        {
            "id": 3,
            "q": "Which SMILES represents ethanol?",
            "options": [
                "CCO",
                "c1ccccc1",
                "CC(=O)O"
            ],
            "answer": "CCO",
            "explain": "Ethanol consists of a two-carbon chain attached to a hydroxyl group: CH3-CH2-OH -> CCO."
        },
        {
            "id": 4,
            "q": "Which SMILES represents benzene?",
            "options": [
                "c1ccccc1",
                "CCO",
                "O=C=O"
            ],
            "answer": "c1ccccc1",
            "explain": "The benzene ring is an aromatic 6-membered ring represented by lowercase 'c' with ring opening/closing index 1: c1ccccc1."
        },
        {
            "id": 5,
            "q": "In SMILES, parentheses are mainly used to indicate:",
            "options": [
                "Branches",
                "Molecular weight",
                "Atom colour"
            ],
            "answer": "Branches",
            "explain": "Parentheses ( ) denote branched substituents and side chains coming off the main molecular backbone chain."
        },
        {
            "id": 6,
            "q": "Which property is commonly associated with molecular lipophilicity?",
            "options": [
                "LogP",
                "TPSA",
                "HBD"
            ],
            "answer": "LogP",
            "explain": "LogP (octanol/water partition coefficient) is the standard thermodynamic measure of molecular lipophilicity vs hydrophilicity."
        },
        {
            "id": 7,
            "q": "What does TPSA describe?",
            "options": [
                "Topological Polar Surface Area",
                "Total Pi Surface Area",
                "Thermal Property Surface Analysis"
            ],
            "answer": "Topological Polar Surface Area",
            "explain": "TPSA (Topological Polar Surface Area) measures the sum of surfaces of all polar atoms (primarily O and N) and attached hydrogens."
        },
        {
            "id": 8,
            "q": "What does HBA mean?",
            "options": [
                "Hydrogen Bond Acceptor",
                "Heavy Bond Atom",
                "Hydrogen Bond Analysis"
            ],
            "answer": "Hydrogen Bond Acceptor",
            "explain": "HBA stands for Hydrogen Bond Acceptor, referring to electronegative atoms with lone pairs (typically N, O, F)."
        },
        {
            "id": 9,
            "q": "What does HBD mean?",
            "options": [
                "Hydrogen Bond Donor",
                "Heavy Bond Descriptor",
                "Hydrogen Bond Distance"
            ],
            "answer": "Hydrogen Bond Donor",
            "explain": "HBD stands for Hydrogen Bond Donor, referring to heteroatoms covalently bound to hydrogen (e.g., -OH, -NH-)."
        },
        {
            "id": 10,
            "q": "A double bond contains how many pi (π) bonds?",
            "options": [
                "1",
                "2",
                "0"
            ],
            "answer": "1",
            "explain": "A standard covalent double bond consists of one sigma (σ) bond and one pi (π) bond formed by lateral overlap of p-orbitals."
        },
        {
            "id": 11,
            "q": "A triple bond contains how many pi (π) bonds?",
            "options": [
                "2",
                "1",
                "3"
            ],
            "answer": "2",
            "explain": "A triple bond contains one sigma (σ) bond and two mutually perpendicular pi (π) bonds."
        },
        {
            "id": 12,
            "q": "Which model is useful for visualizing approximate molecular volume?",
            "options": [
                "Space Filling",
                "Wireframe only",
                "Text SMILES"
            ],
            "answer": "Space Filling",
            "explain": "The Space-Filling (CPK) model scales atoms to their van der Waals radii, illustrating true spatial volume and steric crowding."
        }
    ]

    user_answers = {}
    with st.form("quiz_form"):
        for q_item in quiz_questions:
            st.markdown(f"**{q_item['id']}. {q_item['q']}**")
            ans = st.radio(
                label=f"Q{q_item['id']}",
                options=q_item["options"],
                index=None,
                key=f"quiz_opt_{q_item['id']}",
                label_visibility="collapsed"
            )
            user_answers[q_item['id']] = ans
            st.write("")

        submitted = st.form_submit_button("Submit Assessment")
        if submitted:
            st.session_state["quiz_submitted"] = True
            score = 0
            for q_item in quiz_questions:
                if user_answers.get(q_item['id']) == q_item["answer"]:
                    score += 1
            st.session_state["quiz_score"] = score
            st.session_state["quiz_total"] = len(quiz_questions)

    # Show results if submitted
    if st.session_state.get("quiz_submitted", False):
        score = st.session_state["quiz_score"]
        total = st.session_state["quiz_total"]
        pct = (score / total) * 100
        
        st.markdown("---")
        st.markdown("### 🏆 Assessment Results")
        
        col_res1, col_res2 = st.columns([1, 2])
        with col_res1:
            st.metric("Final Score", f"{score} / {total}", f"{pct:.1f}%")
        with col_res2:
            student_label = st.session_state.get("student_name") or "Enrolled Student"
            reg_label = st.session_state.get("reg_number") or "N/A"
            if pct >= 80:
                grade = "🌟 Excellent / Distinction"
                box_color = "#173829"
            elif pct >= 60:
                grade = "👍 Good Standing"
                box_color = "#1f2d40"
            else:
                grade = "⚠️ Needs Review"
                box_color = "#381717"

            st.markdown(f"""
            <div style="background:{box_color}; padding:14px; border-radius:8px; border:1px solid #30363d;">
                <b>Student:</b> {student_label} | <b>Reg:</b> {reg_label}<br>
                <b>Performance Rating:</b> {grade}<br>
                <b>Status:</b> Recorded in session for Final Project Report.
            </div>
            """, unsafe_allow_html=True)

        # Question by question feedback
        st.markdown("#### 📋 Question Breakdown & Explanations")
        for q_item in quiz_questions:
            user_pick = user_answers.get(q_item['id'])
            is_correct = (user_pick == q_item["answer"])
            icon = "✅" if is_correct else "❌"
            
            with st.expander(f"{icon} Question {q_item['id']}: {q_item['q']}"):
                st.markdown(f"**Your Answer:** `{user_pick if user_pick else 'Not Answered'}`")
                st.markdown(f"**Correct Answer:** `{q_item['answer']}`")
                st.info(f"💡 **Explanation:** {q_item['explain']}")


# =========================================================
# PAGE 7: 📑 Final Project Report
# =========================================================
elif nav_selection == "📑 Final Project Report":
    st.markdown("## 📑 Final Project Report")
    st.caption("Generate, preview, and download your comprehensive laboratory investigation report.")

    student_name = st.session_state.get("student_name", "").strip() or "Anonymous Student"
    reg_number = st.session_state.get("reg_number", "").strip() or "UNASSIGNED-REG"
    active_molecule = st.session_state.get("active_molecule_name", "Paracetamol")
    active_smiles = st.session_state.get("active_smiles", "CC(=O)Nc1ccc(O)cc1")
    
    mol = parse_smiles(active_smiles)
    if mol is None:
        st.warning("Please ensure a valid molecule is selected in the Molecular Visualization tab.")
    else:
        mol_info = get_molecular_info(mol, active_smiles)
        descriptors = get_descriptors(mol)
        lipinski = evaluate_lipinski(descriptors)
        svg_code = generate_2d_svg(mol, width=320, height=220)
        report_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        st.markdown(f"""
        <div style="background:#1a1e26; border:1px solid #30363d; border-radius:10px; padding:24px; margin-bottom:20px;">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #30363d; padding-bottom:12px;">
                <div>
                    <h2 style="color:#ffffff; margin:0;">🧪 Pharmacol Virtual Laboratory Report</h2>
                    <p style="color:#8b949e; margin:4px 0 0 0; font-size:13px;">Computational Pharmacology & Molecular Structure Analysis &nbsp;|&nbsp; <span style="color:#58a6ff;">Designed by: Abinash Yadav (Reg: RA2611026050303)</span></p>
                </div>
                <div style="text-align:right; font-size:12px; color:#8b949e;">
                    Date: {report_timestamp}<br>
                    Virtual Laboratory Platform v2.0
                </div>
            </div>

            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px; margin-top:16px; font-size:14px;">
                <div>
                    <b>Student Name:</b> {student_name}<br>
                    <b>Registration Number:</b> {reg_number}<br>
                    <b>Course:</b> Computational Pharmacology & Cheminformatics
                </div>
                <div>
                    <b>Analyzed Molecule:</b> {active_molecule}<br>
                    <b>Input SMILES:</b> <code>{active_smiles}</code><br>
                    <b>Molecular Formula:</b> {mol_info['formula']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_rep1, col_rep2 = st.columns([1, 1])
        with col_rep1:
            st.markdown("#### 2D Skeletal Structure")
            st.markdown(f"""
            <div class="white-structure-card" style="min-height:220px;">
                {svg_code}
            </div>
            """, unsafe_allow_html=True)

        with col_rep2:
            st.markdown("#### Molecular Constitution & Bonds")
            st.markdown(f"""
            - **Formula:** {mol_info['formula']}
            - **Heavy Atoms:** {mol_info['heavy_atoms']}
            - **Total Atoms (including H):** {mol_info['total_atoms']}
            - **Heavy-Atom Bonds:** {mol_info['heavy_bonds']}
            - **Sigma (σ) Bonds:** {mol_info['sigma_bonds']}
            - **Pi (π) Bonds:** {mol_info['pi_bonds']}
            - **Total Bonds (σ + π):** {mol_info['total_bonds']}
            - **Aromatic Rings:** {mol_info['aromatic_rings']}
            """)

        st.markdown("---")
        st.markdown("#### Physicochemical Descriptors & Drug-Likeness Profile")
        
        rep_table_data = [
            {"Descriptor": "Molecular Weight (MW)", "Value": f"{descriptors['MW']} Da", "Lipinski Limit": "≤ 500 Da", "Outcome": "PASS" if descriptors['MW'] <= 500 else "VIOLATED"},
            {"Descriptor": "Lipophilicity (LogP)", "Value": f"{descriptors['LogP']}", "Lipinski Limit": "≤ 5.0", "Outcome": "PASS" if descriptors['LogP'] <= 5.0 else "VIOLATED"},
            {"Descriptor": "Topological Polar Surface Area (TPSA)", "Value": f"{descriptors['TPSA']} Å²", "Lipinski Limit": "≤ 140 Å²", "Outcome": "PASS" if descriptors['TPSA'] <= 140 else "VIOLATED"},
            {"Descriptor": "H-Bond Donors (HBD)", "Value": f"{descriptors['HBD']}", "Lipinski Limit": "≤ 5", "Outcome": "PASS" if descriptors['HBD'] <= 5 else "VIOLATED"},
            {"Descriptor": "H-Bond Acceptors (HBA)", "Value": f"{descriptors['HBA']}", "Lipinski Limit": "≤ 10", "Outcome": "PASS" if descriptors['HBA'] <= 10 else "VIOLATED"},
            {"Descriptor": "Rotatable Bonds", "Value": f"{descriptors['Rotatable Bonds']}", "Lipinski Limit": "≤ 10", "Outcome": "PASS" if descriptors['Rotatable Bonds'] <= 10 else "VIOLATED"}
        ]
        st.table(pd.DataFrame(rep_table_data))

        # Assessment Score Block
        st.markdown("#### Laboratory Assessment Record")
        if st.session_state.get("quiz_submitted", False):
            st.success(f"Verified Quiz Score: {st.session_state['quiz_score']} / {st.session_state['quiz_total']} ({(st.session_state['quiz_score']/st.session_state['quiz_total'])*100:.1f}%)")
        else:
            st.info("Assessment has not been submitted yet in this session. Visit the '📝 Assessment' tab to complete your graded quiz.")

        # Download Report as standalone printable HTML
        html_report = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Pharmacol Lab Report - {student_name}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 40px; color: #111; line-height: 1.5; }}
.header {{ border-bottom: 2px solid #222; padding-bottom: 12px; margin-bottom: 24px; }}
.title {{ font-size: 24px; font-weight: bold; color: #0b3954; }}
.meta-box {{ display: flex; justify-content: space-between; background: #f4f6f8; padding: 14px; border-radius: 6px; margin-bottom: 24px; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 14px; }}
th, td {{ border: 1px solid #ccc; padding: 8px 12px; text-align: left; font-size: 13px; }}
th {{ background-color: #e9ecef; }}
.pass {{ color: #087f5b; font-weight: bold; }}
.violated {{ color: #c92a2a; font-weight: bold; }}
.structure-container {{ text-align: center; margin: 20px 0; background: #fafafa; padding: 15px; border: 1px solid #e2e8f0; border-radius: 8px; }}
@media print {{ body {{ margin: 15mm; }} button {{ display: none; }} }}
</style>
</head>
<body>
<div class="header">
    <div class="title">🧪 Pharmacol Virtual Laboratory Report</div>
    <div>Department of Pharmacology & Cheminformatics &nbsp;|&nbsp; <strong>Designed by:</strong> Abinash Yadav (Reg No: RA2611026050303)</div>
</div>
<div class="meta-box">
    <div>
        <strong>Student:</strong> {student_name}<br>
        <strong>Registration Number:</strong> {reg_number}<br>
        <strong>Date:</strong> {report_timestamp}
    </div>
    <div>
        <strong>Drug Molecule:</strong> {active_molecule}<br>
        <strong>SMILES:</strong> <code>{active_smiles}</code><br>
        <strong>Formula:</strong> {mol_info['formula']}
    </div>
</div>

<h3>2D Molecular Representation</h3>
<div class="structure-container">
    {svg_code}
</div>

<h3>Physicochemical Descriptors & Drug-Likeness (Lipinski Rules)</h3>
<table>
<thead><tr><th>Descriptor</th><th>Calculated Value</th><th>Rule Threshold</th><th>Outcome</th></tr></thead>
<tbody>
{"".join(f"<tr><td>{r['Descriptor']}</td><td>{r['Value']}</td><td>{r['Lipinski Limit']}</td><td class='{r['Outcome'].lower()}'>{r['Outcome']}</td></tr>" for r in rep_table_data)}
</tbody>
</table>

<h3>Summary & Conclusions</h3>
<p>
The molecule <strong>{active_molecule}</strong> demonstrates an oral bioavailability profile evaluated with <strong>{lipinski['violations']} Lipinski violations</strong>.
Predicted Blood-Brain Barrier (BBB) permeability: <em>{lipinski['bbb_prediction']}</em>.
Total covalent bonds: {mol_info['total_bonds']} ({mol_info['sigma_bonds']} σ bonds and {mol_info['pi_bonds']} π bonds).
</p>

<br><br>
<div style="display:flex; justify-content:space-between; margin-top:40px;">
    <div>____________________________<br>Student Signature</div>
    <div>____________________________<br>Laboratory Instructor Verification</div>
</div>
</body>
</html>"""

        st.download_button(
            label="⬇ Download Printable HTML Lab Report",
            data=html_report,
            file_name=f"Pharmacol_Report_{student_name.replace(' ', '_')}_{active_molecule}.html",
            mime="text/html"
        )


# ---------------------------------------------------------
# Footer on all pages matching screenshot
# ---------------------------------------------------------
st.markdown("""
<div class="footer-text" style="padding-top:20px; margin-top:40px; border-top:1px solid #30363d;">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
        <span style="font-size:13px; color:#8b949e;">🧪 Pharmacol Virtual Laboratory | Developed using Python, Streamlit and RDKit</span>
        <span style="font-size:16px; font-weight:700; color:#58a6ff; background:#161b22; padding:8px 16px; border-radius:6px; border:1.5px solid #388bfd;">
            👨‍💻 Designed by: Abinash Yadav &nbsp;|&nbsp; Registration Number: RA2611026050303
        </span>
    </div>
</div>
""", unsafe_allow_html=True)
