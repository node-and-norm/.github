"""Apply the website wordmark to the retained desktop and mobile study layouts."""
import argparse
from pathlib import Path
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
V1 = HERE.parent / "v1"
WORDMARK = HERE.parents[1] / "brand/current/wordmark-dark.svg"
SVG = "{http://www.w3.org/2000/svg}"
ET.register_namespace("", SVG[1:-1])

# The public CEC repository changed its slug after these layouts were created.
LAYOUTS = {
    "trust-autonomy-evidence": V1 / "tae-banner",
    "control-evidence-corpus": V1 / "projects/node-norm-control-evidence/banner",
}
for name in (
    "human-influence-telemetry", "governed-decision-intelligence", "rgds",
    "cdfi-framework", "applied-ai-research-translator", "rgds-independent-study",
    "rgds-ai-governance",
):
    LAYOUTS[name] = V1 / "projects" / name / "banner"


def render(layout, mobile):
    banner = ET.parse(layout).getroot()
    # In the v1 layouts the only top-level groups are the icon and old lettering.
    groups = banner.findall(f"{SVG}g")
    if len(groups) != 2 or any(g.get("aria-hidden") != "true" for g in groups):
        raise ValueError(f"Unexpected brand layout in {layout}")
    index = list(banner).index(groups[0])
    for group in groups:
        banner.remove(group)

    wordmark = ET.parse(WORDMARK).getroot()
    # The outer image already supplies the accessible study title and program name.
    wordmark.attrib.pop("role")
    wordmark.attrib.pop("aria-label")
    x, y, width, height = (24, 20, 140, 20) if mobile else (34, 26, 182, 26)
    wordmark.attrib.update(x=str(x), y=str(y), width=str(width), height=str(height))
    wordmark.set("aria-hidden", "true")
    wordmark.tail = "\n"
    banner.insert(index, wordmark)
    return ET.tostring(banner, encoding="utf-8") + b"\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check the committed banners.")
    args = parser.parse_args()
    for repo, prefix in LAYOUTS.items():
        for mobile in (False, True):
            suffix = "-mobile" if mobile else ""
            layout = prefix.with_name(f"{prefix.name}{suffix}-dark.svg")
            content = render(layout, mobile)
            path = HERE / repo / f"banner{suffix}.svg"
            if args.check:
                if not path.is_file() or path.read_bytes() != content:
                    raise SystemExit(f"Banner differs: {path.relative_to(HERE)}")
            else:
                path.parent.mkdir(exist_ok=True)
                path.write_bytes(content)
    print(f"{len(LAYOUTS) * 2} study banners {'verified' if args.check else 'written'}.")


if __name__ == "__main__":
    main()
