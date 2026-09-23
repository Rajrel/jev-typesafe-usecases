"""Remove stderr/warning outputs from all notebooks."""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
NB_DIR = ROOT / "notebooks"

def is_warning_output(output):
    """Return True if this output is a stderr stream containing a warning."""
    if output.get("output_type") == "stream" and output.get("name") == "stderr":
        return True
    # Also catch error outputs that are warnings
    text = "".join(output.get("text", []) + output.get("traceback", []))
    if "Warning" in text or "warning" in text:
        return True
    return False

changed_files = []
for nb_path in sorted(NB_DIR.glob("*.ipynb")):
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    dirty = False
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        original = cell.get("outputs", [])
        filtered = [o for o in original if not is_warning_output(o)]
        if len(filtered) != len(original):
            cell["outputs"] = filtered
            dirty = True
    if dirty:
        nb_path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        removed = sum(1 for cell in nb.get("cells", []) if cell.get("cell_type") == "code")
        changed_files.append(nb_path.name)
        print(f"cleaned: {nb_path.name}")
    else:
        print(f"clean:   {nb_path.name}")

print(f"\nDone. {len(changed_files)} notebook(s) updated.")
