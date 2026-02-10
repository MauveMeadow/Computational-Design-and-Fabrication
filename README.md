# Parasol: Deployable Origami Structure

**Course:** Computational Design and Fabrication 1 **Institution:** Technical University of Munich (TUM), School of Engineering and Design **Semester:** Winter Semester 2025/26 **Team:** Mays Alsheikh, Milena Pospischil, Christian Rauch **Date:** Munich, 5 February 2026 

---

## 1. Project Overview & Concept

### Urban Challenge & Design Intent

Our primary urban challenge is creating a temporary structure. Rather than establishing a permanent installation, the "Parasol" is designed to remain flexible and adaptable to changing campus activities and spatial needs. A key constraint was to avoid permanently occupying limited space while accommodating a pedestrian area; we needed to create it without blocking the flow of people.

### Technical Approach

To support rapid assembly, our structure must achieve quick deployment and efficient transportation. We utilized triangulated folds to solve this logistics challenge. This geometric approach allows us to manufacture flat surfaces that can fold, expand, and contract efficiently, enabling simple off-site fabrication and compact storage.

### Key Constraints & Goals

**Context:** Limited space with high pedestrian traffic.

**Logistics:** Must be easy to store and transport.

**Fabrication:** Designed for simple off-site production using flat sheet materials.

---

## 2. Computational Method

The geometry is generated parametrically to ensure the surface is developable (can be flattened without distortion) and rigid-foldable.

### Software Stack

**Rhino 7 / 8** (Geometry Engine)

**Grasshopper** (Visual Scripting) 

**Python (GHPython)** (Topology & Grid Generation) 

**CRANE** (Origami Physics Solver by Kai Suto) 


### The Algorithm

The core geometry is generated via a custom Python script within Grasshopper. The script constructs a radial grid and assigns specific fold attributes (Mountain/Valley) to ensure the simulation converges.

#### Key Geometric Constraints

To ensure successful simulation in CRANE, the mesh topology follows specific rules:

1. **Continuous Valleys:** The Blue Radial Valleys run continuously from the center to the edge.
2. **Continuous Spines:** The Green Diamond Spines connect the Inner Tip directly to the Outer Tip, skipping intermediate vertices to prevent edge-splitting during simulation.
3. **Strict Triangulation:** The mesh is explicitly triangulated to define rigid plates.

#### Grasshopper Workflow

The data flow visualized in the definition is as follows:

1. **Python Script:** Generates the raw vertices, faces, and classified lines (Mountain/Valley).
2. **Boundary & Surface Split:** The script outputs curves used to split a base surface into individual rigid faces.
3. **Mesh Conversion:** The surfaces are joined and converted into a mesh (`SMesh`  `Weld`).
4. **CRANE Solver:** The mesh and fold lines are fed into the `CMesh` component. The solver simulates the folding motion based on a `FoldSpeed` parameter (set to 0.14 in the reference).



---

## 3. Parametric Script Documentation

The following Python script is used inside the GHPython component to generate the folding pattern.

**Input Parameters:**

* `num_segments`: Number of radial segments (e.g., 12).
* `r0`, `r1`, `r2`, `r3`: Radii controlling the concentric rings of the pattern (Inner, Pink/Tip, Waist, Blue/Outer).

---

## 4. Fabrication & Materiality

**Material:** Perforated metal plates with fabric hinges.

**Joints:** Detachable joints utilizing Keder Tracks (econotarps) for segmentation.

**Mechanism:** Central radial actuation (pulling mechanism) designed to expand the triangulated mesh.

**Scalability:** The design is scalable and allows for modular prefabrication.



---

## 5. References

*Folding patterns for developable surfaces* (D'Acunto, 2018).

*Santo António Da Polana Church* (Nuno Craveiro Lopes).

*Deployable Umbrella* (Tongji University, Southeast University).
