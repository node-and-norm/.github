"""Build self-contained study banners with the website wordmark and cover ampersand."""
import argparse
import json
from pathlib import Path
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
V1 = HERE.parent / "v1"
WORDMARK = HERE.parents[1] / "brand/current/wordmark-dark.svg"
SVG = "{http://www.w3.org/2000/svg}"
ET.register_namespace("", SVG[1:-1])

CONFIGS = {
    "trust-autonomy-evidence": V1 / "tae.json",
    # The CEC repository changed its slug after the original layout was made.
    "control-evidence-corpus": V1 / "projects/node-norm-control-evidence/config.json",
    "revocation-delegated-workflows": HERE / "revocation-delegated-workflows/config.json",
}
for name in (
    "human-influence-telemetry", "governed-decision-intelligence", "rgds",
    "cdfi-framework", "applied-ai-research-translator", "rgds-independent-study",
    "rgds-ai-governance",
):
    CONFIGS[name] = V1 / "projects" / name / "config.json"


def render(config, mobile):
    title_lines = config["mobile_title_lines"] if mobile else [config["title"]]
    subtitle_lines = config["mobile_purpose_lines"] if mobile else [config["purpose"]]
    if mobile:
        width, left, title_y = 400, 24, 169
        title_size = config.get("mobile_title_size", 32)
        subtitle_y = title_y + 38 * (len(title_lines) - 1) + 43
        height = subtitle_y + 27 * (len(subtitle_lines) - 1) + 48
        logo_y, logo_width, logo_height = 44, 140, 20
        amp_transform = "translate(276 131) scale(0.22)"
    else:
        width, height, left, title_y, subtitle_y = 1000, 230, 34, 128, 174
        title_size = config.get("desktop_title_size", 44)
        logo_y, logo_width, logo_height = 26, 182, 26
        amp_transform = "translate(734 301) scale(0.47)"

    banner = ET.Element(SVG + "svg", {
        "width": str(width), "height": str(height), "viewBox": f"0 0 {width} {height}",
        "role": "img", "aria-labelledby": "title desc", "overflow": "hidden",
    })
    ET.SubElement(banner, SVG + "title", id="title").text = config["title"] + " | Node & Norm"
    ET.SubElement(banner, SVG + "desc", id="desc").text = config["purpose"]
    ET.SubElement(banner, SVG + "rect", width=str(width), height=str(height), fill="#191820")

    # Use the outlined glyph in the official wordmark so both marks always agree.
    wordmark = ET.parse(WORDMARK).getroot()
    glyph, = [p for p in wordmark.findall(SVG + "path") if p.get("fill") == "#b5afff"]
    ET.SubElement(banner, SVG + "path", {
        "data-artwork": "cover-ampersand", "aria-hidden": "true", "d": glyph.attrib["d"],
        "fill": glyph.attrib["fill"], "transform": amp_transform,
    })
    wordmark.attrib.pop("role")
    wordmark.attrib.pop("aria-label")
    wordmark.attrib.update(x=str(left), y=str(logo_y), width=str(logo_width), height=str(logo_height))
    wordmark.set("aria-hidden", "true")
    banner.append(wordmark)

    text_style = {"fill": "#F7F7F4", "font-family": "Arial, Helvetica, sans-serif", "x": str(left)}
    for i, line in enumerate(title_lines):
        ET.SubElement(banner, SVG + "text", {
            **text_style, "y": str(title_y + i * 38), "font-size": str(title_size),
            "font-weight": "600", "letter-spacing": "-1",
        }).text = line
    for i, line in enumerate(subtitle_lines):
        ET.SubElement(banner, SVG + "text", {
            **text_style, "y": str(subtitle_y + i * 27), "font-size": "20" if mobile else "24",
        }).text = line
    ET.SubElement(banner, SVG + "rect", x=str(left), y=str(height - 20), width="72", height="4", fill="#D7F59A")
    return ET.tostring(banner, encoding="utf-8") + b"\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check the committed banners.")
    args = parser.parse_args()
    for repo, config_path in CONFIGS.items():
        config = json.loads(config_path.read_text())
        if repo == "trust-autonomy-evidence":
            sizes = json.loads((V1 / "tokens.json").read_text())["typography"]
            config.update(desktop_title_size=sizes["desktop_title"], mobile_title_size=sizes["mobile_title"])
        for mobile in (False, True):
            name = "banner-mobile.svg" if mobile else "banner.svg"
            content = render(config, mobile)
            path = HERE / repo / name
            if args.check:
                if not path.is_file() or path.read_bytes() != content:
                    raise SystemExit(f"Banner differs: {path.relative_to(HERE)}")
            else:
                path.parent.mkdir(exist_ok=True)
                path.write_bytes(content)
    print(f"{len(CONFIGS) * 2} study banners {'verified' if args.check else 'written'}.")


if __name__ == "__main__":
    main()
