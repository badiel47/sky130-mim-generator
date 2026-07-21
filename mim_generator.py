import math
import klayout.db as kdb
import os

def generate_sky130_mim_capacitor(capacitance_fF):
    # ==========================================
    # 1. SKYWATER 130nm PDK PARAMETERS
    # ==========================================
    # MiM capacitance density (capm) in Sky130
    cap_density_fF_um2 = 2.0 
    
    # Calculate Area in square microns
    area_um2 = capacitance_fF / cap_density_fF_um2
    
    # Calculate the side of the square polygon (in microns)
    side_um = math.sqrt(area_um2)
    
    print(f"--- Building SKY130 Capacitor: {capacitance_fF} fF ---")
    print(f"Capacitance density (PDK): {cap_density_fF_um2} fF/um²")
    print(f"MiM plate dimension: {side_um:.3f} um x {side_um:.3f} um")
    
    # ==========================================
    # 2. SKY130 OFFICIAL GDSII LAYERS
    # ==========================================
    layout = kdb.Layout()
    layout.dbu = 0.001 # 1 nanometer database unit
    top_cell = layout.create_cell(f"SKY130_MIM_{capacitance_fF}fF")
    
    # Layer mapping according to SkyWater documentation
    layer_met3 = layout.layer(70, 20) # Metal 3 (Bottom Plate)
    layer_capm = layout.layer(89, 44) # MiM Layer (Top Plate)
    layer_via3 = layout.layer(70, 44) # Via 3 (Top Plate -> Met4 connection)
    layer_met4 = layout.layer(71, 20) # Metal 4 (Top Routing)
    
    # Text/Label layers for LVS connectivity extraction
    layer_label_met3 = layout.layer(70, 5) # Text for Metal 3
    layer_label_met4 = layout.layer(71, 5) # Text for Metal 4
    
    side_dbu = int(side_um / layout.dbu)
    
    # ==========================================
    # 3. GEOMETRY AND DESIGN RULES (DRC)
    # ==========================================
    # Top plate (capm) and top routing metal (met4) share the same footprint
    top_plate_box = kdb.Box(0, 0, side_dbu, side_dbu)
    
    # Enclosure rule: Metal 3 (Bottom) must absorb alignment variability
    # Applying a standard safety margin of 0.5 um (500 dbu) per edge
    enclosure = int(0.5 / layout.dbu)
    bottom_plate_box = kdb.Box(0 - enclosure, 0 - enclosure, side_dbu + enclosure, side_dbu + enclosure)
    
    top_cell.shapes(layer_capm).insert(top_plate_box)
    top_cell.shapes(layer_met4).insert(top_plate_box)
    top_cell.shapes(layer_met3).insert(bottom_plate_box)
    
    # ==========================================
    # 4. VIA ARRAY GENERATION
    # ==========================================
    via_size = int(0.20 / layout.dbu)    # Standard 200 nm via
    via_space = int(0.20 / layout.dbu)   # 200 nm spacing between vias
    via_margin = int(0.30 / layout.dbu)  # DRC safety margin from the edge
    
    start_coord = via_margin
    end_coord = side_dbu - via_margin
    
    # Nested loops to uniformly populate the top plate with vias
    x = start_coord
    while x + via_size <= end_coord:
        y = start_coord
        while y + via_size <= end_coord:
            via_box = kdb.Box(x, y, x + via_size, y + via_size)
            top_cell.shapes(layer_via3).insert(via_box)
            y += via_size + via_space
        x += via_size + via_space

    # ==========================================
    # 5. LVS LABELS (PIN TEXTS)
    # ==========================================
    # PLUS label at the exact geometric center of the top plate
    center_coord = int(side_dbu / 2)
    label_top = kdb.Text("PLUS", center_coord, center_coord)
    
    # MINUS label at the extreme bottom-left corner of the bottom plate (Metal 3)
    bottom_left_x = 0 - enclosure
    bottom_left_y = 0 - enclosure
    label_bot = kdb.Text("MINUS", bottom_left_x, bottom_left_y)
    
    # Insert text objects into their respective logical layers
    top_cell.shapes(layer_label_met4).insert(label_top)
    top_cell.shapes(layer_label_met3).insert(label_bot)

    # ==========================================
# 6. EXPORT GDSII
    # ==========================================
    output_dir = os.path.join(os.getcwd(), "outputs")    
    os.makedirs(output_dir, exist_ok=True) 
    output_path = os.path.join(output_dir, f"SKY130_MIM_{capacitance_fF}fF.gds")
    
    layout.write(output_path)
    print(f"Physical layout exported to: {output_path}\n")

if __name__ == "__main__":
    generate_sky130_mim_capacitor(capacitance_fF=250)
    generate_sky130_mim_capacitor(capacitance_fF=1000)