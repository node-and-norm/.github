"""Generate versioned research identity assets with the Python standard library."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
NS = "{http://www.w3.org/2000/svg}"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wordmark(text_color: str, accent: str, x: int, y: int, scale: float) -> str:
    source = ET.parse(ROOT / "assets/brand/current/banner.svg").getroot()
    paths = []
    for el in source.findall(f"{NS}path"):
        color = accent if el.attrib["fill"].lower() == "#b5afff" else text_color
        paths.append(f'<path d="{html.escape(el.attrib["d"], quote=True)}" '
                     f'fill="{color}" transform="{el.attrib["transform"]}"/>')
    return (f'<g aria-hidden="true" transform="translate({x} {y}) scale({scale})">'
            '<g transform="translate(-2590 -295)">' + "".join(paths) + '</g></g>')


def witness(accent: str, x: int, y: int, scale: float) -> str:
    source = ET.parse(ROOT / "assets/brand/current/logo.svg").getroot()
    shape = source.find(f"{NS}g/{NS}path").attrib["d"]
    return (f'<g aria-hidden="true" transform="translate({x} {y}) scale({scale})" '
            f'fill="none" stroke="{accent}" stroke-width="7" stroke-linecap="square">'
            f'<path d="{shape}"/></g>')


def svg_start(width: int, height: int, title: str, description: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">\n'
            f'<title id="title">{html.escape(title)}</title>\n'
            f'<desc id="desc">{html.escape(description)}</desc>\n')


def banner(tokens: dict, config: dict, theme: str, mobile: bool) -> str:
    colors = {k: tokens["colors"][v] for k, v in tokens["themes"][theme].items()}
    sizes = tokens["dimensions"]["mobile" if mobile else "desktop"]
    w, h = sizes["width"], sizes["height"]
    svg = svg_start(w, h, f'{config["title"]} | Node & Norm', config["purpose"])
    svg += f'<rect width="{w}" height="{h}" fill="{colors["background"]}"/>\n'
    x, top = (24, 18) if mobile else (34, 25)
    svg += witness(colors["accent"], x - 7, top - 4, .36 if mobile else .48)
    svg += wordmark(colors["text"], colors["accent"], x + (35 if mobile else 46), top, .12 if mobile else .16)
    font = html.escape(tokens["typography"]["family"], quote=True)
    if mobile:
        title_y, title_step, purpose_y, purpose_step = 105, 39, 189, 27
        title_size = tokens["typography"]["mobile_title"]
        purpose_size = tokens["typography"]["mobile_purpose"]
        title_lines, purpose_lines = config["mobile_title_lines"], config["mobile_purpose_lines"]
    else:
        title_y, title_step, purpose_y, purpose_step = 128, 0, 174, 0
        title_size = tokens["typography"]["desktop_title"]
        purpose_size = tokens["typography"]["desktop_purpose"]
        title_lines, purpose_lines = [config["title"]], [config["purpose"]]
    for i, line in enumerate(title_lines):
        svg += (f'<text x="{x}" y="{title_y + i * title_step}" fill="{colors["text"]}" '
                f'font-family="{font}" font-size="{title_size}" font-weight="600" '
                f'letter-spacing="-1.2">{html.escape(line)}</text>\n')
    for i, line in enumerate(purpose_lines):
        svg += (f'<text x="{x}" y="{purpose_y + i * purpose_step}" fill="{colors["text"]}" '
                f'font-family="{font}" font-size="{purpose_size}">{html.escape(line)}</text>\n')
    svg += f'<rect x="{x}" y="{h - 20}" width="72" height="4" fill="{colors["marker"]}"/>\n'
    return svg + '</svg>\n'


def badge(tokens: dict, item: dict, theme: str) -> str:
    colors = {k: tokens["colors"][v] for k, v in tokens["themes"][theme].items()}
    width = item["width"]
    label_width = 55
    title = f'{item["label"]}: {item["value"]}'
    svg = svg_start(width, 26, title, 'Project metadata. Follow the surrounding link for its source and scope.')
    svg += (f'<rect x=".5" y=".5" width="{width - 1}" height="25" rx="3" '
            f'fill="{colors["background"]}" stroke="{colors["accent"]}"/>\n'
            f'<path d="M{label_width} 1V25" stroke="{colors["accent"]}"/>\n')
    font = html.escape(tokens["typography"]["family"], quote=True)
    svg += (f'<g font-family="{font}" font-size="12" text-anchor="middle">'
            f'<text x="{label_width / 2}" y="17" fill="{colors["text"]}">{html.escape(item["label"])}</text>'
            f'<text x="{label_width + (width - label_width) / 2}" y="17" fill="{colors["accent"]}">{html.escape(item["value"])}</text></g>\n')
    return svg + '</svg>\n'


def luminance(color: str) -> float:
    values = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in values]
    return sum(c * weight for c, weight in zip(linear, (.2126, .7152, .0722)))


def contrast(a: str, b: str) -> float:
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + .05) / (lo + .05)


def outputs() -> dict[str, bytes]:
    tokens = json.loads((HERE / 'tokens.json').read_text())
    config = json.loads((HERE / 'tae.json').read_text())
    result = {}
    ratios = []
    for theme in ('light', 'dark'):
        for mobile in (False, True):
            suffix = '-mobile' if mobile else ''
            result[f'tae-banner{suffix}-{theme}.svg'] = banner(tokens, config, theme, mobile).encode()
        for item in config['badges']:
            result[f'badges/tae-{item["id"]}-{theme}.svg'] = badge(tokens, item, theme).encode()
        theme_tokens = tokens['themes'][theme]
        background = tokens['colors'][theme_tokens['background']]
        for role in ('text', 'accent'):
            foreground = tokens['colors'][theme_tokens[role]]
            ratio = contrast(foreground, background)
            ratios.append({'theme': theme, 'role': role, 'foreground': foreground,
                           'background': background, 'ratio': round(ratio, 4), 'normal_text_aa': ratio >= 4.5})
    checks = {'method': 'WCAG 2 relative luminance contrast formula', 'normal_text_minimum': 4.5,
              'pairs': ratios, 'scope': 'Declared opaque foreground/background pairs. Rendered page accessibility needs separate review.'}
    result['contrast.json'] = (json.dumps(checks, indent=2) + '\n').encode()
    manifest = {'asset_version': tokens['asset_version'], 'config': 'tae.json',
                'inputs': {name: sha256(HERE / name) for name in ('tokens.json', 'tae.json', 'generate.py')},
                'sources': {name: sha256(ROOT / name) for name in ('assets/brand/current/logo.svg', 'assets/brand/current/banner.svg')},
                'files': {name: hashlib.sha256(data).hexdigest() for name, data in sorted(result.items())}}
    result['manifest.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Compare generated bytes without writing files.')
    args = parser.parse_args()
    generated = outputs()
    errors = []
    for name, data in generated.items():
        path = HERE / name
        if name.endswith('.svg'):
            root = ET.fromstring(data)
            if root.find(f'{NS}title') is None or root.find(f'{NS}desc') is None:
                raise ValueError(f'Accessible title or description is missing: {name}')
            if root.attrib.get('role') != 'img':
                raise ValueError(f'Image role is missing: {name}')
        if args.check:
            if not path.exists() or path.read_bytes() != data:
                errors.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    if errors:
        raise SystemExit('Generated assets differ: ' + ', '.join(errors))
    print(f'{len(generated)} generated files {"match" if args.check else "written"}.')


if __name__ == '__main__':
    main()
