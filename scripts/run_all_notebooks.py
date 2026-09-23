"""Execute every notebook in notebooks/ and save outputs in-place."""
import sys
from pathlib import Path
import nbformat
import nbclient

ROOT = Path(__file__).parent.parent
NB_DIR = ROOT / "notebooks"

notebooks = sorted(NB_DIR.glob("*.ipynb"))
print(f"Found {len(notebooks)} notebooks\n")

failed = []
for nb_path in notebooks:
    print(f"Running {nb_path.name} ...", end=" ", flush=True)
    nb = nbformat.read(nb_path, as_version=4)
    try:
        ep = nbclient.NotebookClient(
            nb,
            timeout=120,
            kernel_name="python3",
            resources={"metadata": {"path": str(ROOT)}},
        )
        ep.execute()
        nbformat.write(nb, nb_path)
        print("OK")
    except Exception as e:
        print(f"FAILED: {e}")
        failed.append(nb_path.name)

print()
if failed:
    print("Failed notebooks:")
    for name in failed:
        print(f"  {name}")
    sys.exit(1)
else:
    print("All notebooks executed successfully.")
