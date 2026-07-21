# Sky130 Parametric MIM Capacitor Generator (PCell)

## Overview
This repository contains a Python-based parameterized cell (PCell) layout generator for Metal-Insulator-Metal (MIM) capacitors, specifically tailored for the **SkyWater 130nm (sky130)** open-source PDK. 

Instead of relying on static, pre-drawn library instantiation, this script programmatically calculates the physical geometry based on the exact capacitance density of the PDK (2.0 fF/µm²) and generates a DRC-clean GDSII layout ready for manufacturing.

## Key Features
* **Automated Physical Sizing:** Dynamically calculates top and bottom plate dimensions from user-defined target capacitance in femtofarads (fF).
* **DRC-Clean Geometry:** Automatically applies lithographic safety margins (enclosure rules) to the bottom plate (Metal 3) to prevent manufacturing misalignment errors.
* **Dynamic Via Arrays:** Auto-populates the capacitor with a mathematically precise Via 3 array, calculating optimal spacing and count to guarantee robust top-plate connectivity without violating standard spacing rules.
* **LVS-Ready Pin Extraction:** Automatically generates `PLUS` and `MINUS` text labels mapped to the correct GDSII datatypes (Layer 70/71, Datatype 5) for flawless Layout vs. Schematic (LVS) extraction.

## Visual Proof
*(Insert KLayout layout screenshots here)*
> **Note for the developer:** Place your screenshots inside the `/docs` folder and link them here using `![MIM Capacitor](docs/mim_layout_250fF.png)`.

## Tech Stack
* **Language:** Python 3
* **EDA Tool:** KLayout Database API (`klayout.db`)
* **Target Process:** SkyWater 130nm CMOS

## Usage
Activate your virtual environment, install dependencies, and run the script:
```bash
pip install klayout
python3 mim_generator.py