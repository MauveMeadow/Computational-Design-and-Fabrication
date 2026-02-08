"""

Parasol Origami - ALL Continuous Lines

1. Blue Radial Valleys: Continuous (Center to Edge).

2. Green Diamond Spines: Continuous (Inner Tip to Outer Tip).

3. No split lines in the simulation output.

"""

import Rhino.Geometry as rg

import math



# ==============================================================================

# 1. SETUP

# ==============================================================================

out_mesh = rg.Mesh()

mountain_lines = []

valley_lines = []  

boundary_lines = []



n = int(num_segments)

r_in = float(r0)

r_pink = float(r1)  

r_waist = float(r2)

r_blue = float(r3)  



radii = [r_in, r_pink, r_waist, r_blue]



# ==============================================================================

# 2. GENERATE POINTS

# ==============================================================================

grid_indices = []

r_inner_chord = r_in * math.cos(math.pi / n)



for r_idx, r in enumerate(radii):

    ring_row = []

    for i in range(2 * n):

        angle = i * (math.pi / n)

        current_r = r

       

        # STRAIGHT INNER BOUNDARY LOGIC

        if r_idx == 0 and i % 2 != 0:

            current_r = r_inner_chord

           

        x = current_r * math.cos(angle)

        y = current_r * math.sin(angle)

       

        out_mesh.Vertices.Add(x, y, 0.0)

        ring_row.append(out_mesh.Vertices.Count - 1)

       

    grid_indices.append(ring_row)



# ==============================================================================

# 3. CREATE LINES & FACES

# ==============================================================================

def wrap(i): return i % (2 * n)

def get_pt(idx): return rg.Point3d(out_mesh.Vertices[idx])



for i in range(2 * n):

    # Process Mountain Rays (Odd indices)

    if i % 2 != 0:

        idx_m = i               # Mountain Index

        idx_l = wrap(i - 1)     # Left Valley

        idx_r = wrap(i + 1)     # Right Valley

        idx_next_m = wrap(i + 2)

       

        # Grid Indices

        p0_l, p0_r = grid_indices[0][idx_l], grid_indices[0][idx_r]

        p0_m = grid_indices[0][idx_m] # Point on straight edge

       

        p1_m = grid_indices[1][idx_m] # Inner Diamond Tip

        p2_l, p2_r = grid_indices[2][idx_l], grid_indices[2][idx_r]

        p3_m = grid_indices[3][idx_m] # Outer Diamond Tip

        p3_next = grid_indices[3][idx_next_m]

        p2_right_waist = grid_indices[2][idx_r]



        # ---------------------------------------------------------

        # A. MESH FACES (Topology requires the split)

        # ---------------------------------------------------------

        out_mesh.Faces.AddFace(p0_l, p0_m, p1_m)

        out_mesh.Faces.AddFace(p0_l, p1_m, p2_l)

        out_mesh.Faces.AddFace(p0_m, p0_r, p1_m)

        out_mesh.Faces.AddFace(p0_r, p2_r, p1_m)

       

        out_mesh.Faces.AddFace(p2_l, p3_m, grid_indices[2][idx_m])

        out_mesh.Faces.AddFace(p2_r, grid_indices[2][idx_m], p3_m)

       

        # Gap Fill

        pt_curr = get_pt(p3_m)

        pt_next = get_pt(p3_next)

        mid_x = (pt_curr.X + pt_next.X) / 2.0

        mid_y = (pt_curr.Y + pt_next.Y) / 2.0

        out_mesh.Vertices.Add(mid_x, mid_y, 0.0)

        idx_mid = out_mesh.Vertices.Count - 1

       

        out_mesh.Faces.AddFace(p2_right_waist, p3_m, idx_mid)

        out_mesh.Faces.AddFace(p2_right_waist, idx_mid, p3_next)



        # ---------------------------------------------------------

        # B. FOLD LINES (Simulation Constraints)

        # ---------------------------------------------------------

       

        # 1. MOUNTAIN (Blue Ridges) - Keep as is

        mountain_lines.append(rg.Line(get_pt(p0_l), get_pt(p1_m)))

        mountain_lines.append(rg.Line(get_pt(p0_r), get_pt(p1_m)))

        mountain_lines.append(rg.Line(get_pt(p1_m), get_pt(p2_l)))

        mountain_lines.append(rg.Line(get_pt(p1_m), get_pt(p2_r)))

        mountain_lines.append(rg.Line(get_pt(p2_l), get_pt(p3_m)))

        mountain_lines.append(rg.Line(get_pt(p2_r), get_pt(p3_m)))

        



        # 2. GREEN SPINES (The Red Line in your image)

        # ---------------------------------------------------------

        # Short segment (Hole to Inner Tip)

        valley_lines.append(rg.Line(get_pt(p0_m), get_pt(p1_m)))

       

        # *** FIX: LONG CONTINUOUS SPINE ***

        # We connect Inner Tip (p1_m) DIRECTLY to Outer Tip (p3_m).

        # We skip the waist vertex entirely.

        valley_lines.append(rg.Line(get_pt(p1_m), get_pt(p3_m)))



        # ---------------------------------------------------------

       

        # 3. BLUE RADIAL VALLEY (Continuous)

        start_pt = get_pt(p0_r)

        end_pt = get_pt(idx_mid)

        valley_lines.append(rg.Line(start_pt, end_pt))

       

        # 4. BOUNDARY

        boundary_lines.append(rg.Line(get_pt(p3_m), get_pt(idx_mid)))

        boundary_lines.append(rg.Line(get_pt(idx_mid), get_pt(p3_next)))



# Inner Boundary

for k in range(2 * n):

    p_curr = get_pt(grid_indices[0][k])

    p_next = get_pt(grid_indices[0][wrap(k + 1)])

    boundary_lines.append(rg.Line(p_curr, p_next))



# all fold lines

all_folds = mountain_lines + valley_lines
