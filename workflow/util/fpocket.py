import os, subprocess
import pandas as pd


def fpocket(pdb_file, output_prefix=""):
    command = ["fpocket", "-f", pdb_file]
    if output_prefix:
        command.extend(["-o", output_prefix])
    try:
        subprocess.run(command, check=True)
        print(f"fpocket successfully run on {pdb_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running fpocket: {e}")


def parse_fpocket_info(output_dir):
    fname = os.path.basename(output_dir)
    with open(os.path.join(output_dir, f"{fname[:-3]}info.txt"), "r") as f:
        lines = f.readlines()

    # parse data to pandas dataframe
    pockets = []
    for line in lines:
        if line.startswith("Pocket"):
            pockets.append(line.strip()[:-2])
    data = pd.DataFrame(
        columns=[
            "Score",
            "Druggability Score",
            "Number of Alpha Spheres",
            "Total SASA",
            "Polar SASA",
            "Apolar SASA",
            "Volume",
            "Mean local hydrophobic density",
            "Mean alpha sphere radius",
            "Mean alpha sphere solvent accessibility",
            "Apolar alpha sphere proportion",
            "Hydrophobicity score",
            "Volume score",
            "Polarity score",
            "Charge score",
            "Proportion of polar atoms",
            "Alpha sphere density",
            "Center of mass - alpha sphere max distance",
            "Flexibility",
        ],
        index=pockets,
    )

    row = []
    pocket = 0
    for line in lines:
        if not line.strip():
            continue
        if line.startswith("Pocket"):
            pocket += 1
            continue
        row.append(float(line.split(":")[1].strip()))
        if len(row) == len(data.columns):
            data.loc[pockets[pocket - 1]] = row
            row = []
    return data


def centroid(wkdir, pocket):
    x, y, z, n = 0.0, 0.0, 0.0, 0

    with open(os.path.join(wkdir, f"pocket{pocket}_vert.pqr")) as f:
        for line in f:
            # skip non-coordinate lines
            if line.startswith(("ATOM", "HETATM")):
                parts = line.split()
                try:
                    xi, yi, zi = map(float, parts[5:8])
                    x += xi
                    y += yi
                    z += zi
                    n += 1
                except ValueError:
                    continue

    cx, cy, cz = x / n, y / n, z / n
    return cx, cy, cz
