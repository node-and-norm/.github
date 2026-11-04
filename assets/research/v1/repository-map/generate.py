#!/usr/bin/env python3
"""Render the retained repository relationships with the shared brand tokens."""
import argparse
import html
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent


def relationships():
    text = (HERE / 'source.mmd').read_text()
    matches = re.findall(r'N(?:\["Node & Norm"\])? -->\|([^|]+)\| (\w+)\["([^"]+)"\]', text)
    assert len(matches) == 9
    return [(role, key, name.split('<br/>')) for role, key, name in matches]


def render(mobile=False):
    colors = json.loads((HERE.parent / 'tokens.json').read_text())['colors']
    carbon, paper, iris, citron = (colors[k] for k in ('carbon', 'paper', 'light_iris', 'citron'))
    width, height = (400, 1570) if mobile else (1000, 650)
    groups = [('Examine practical', 'human control'), ('Preserve the grounds', 'for decisions'), ('Support inquiry', 'and review')]
    rows = relationships()
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
             '<title id="title">Node &amp; Norm repository map</title>',
             '<desc id="desc">Nine labeled connections from Node &amp; Norm, grouped under the three research themes. ' + html.escape('; '.join(role + ': ' + ' '.join(lines) for role, _, lines in rows)) + '.</desc>',
             f'<rect width="{width}" height="{height}" fill="{carbon}"/>',
             f'<defs><marker id="arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L8 4L0 8Z" fill="{iris}"/></marker></defs>']

    def text(x, y, value, size=21, fill=paper, weight=400, anchor='start'):
        parts.append(f'<text x="{x}" y="{y}" fill="{fill}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{html.escape(value)}</text>')

    if mobile:
        root_x, root_y, root_w, root_h = 48, 24, 328, 62
        bus_x = 24
        parts.append(f'<path d="M48 55H24V1486" fill="none" stroke="{iris}" stroke-width="1.5"/>')
    else:
        root_x, root_y, root_w, root_h = 380, 28, 240, 64
        parts.append(f'<path d="M500 92V120H32V553M500 120H357V553M500 120H682V553" fill="none" stroke="{iris}" stroke-width="1.5"/>')
    parts.append(f'<rect x="{root_x}" y="{root_y}" width="{root_w}" height="{root_h}" rx="4" fill="{carbon}" stroke="{citron}" stroke-width="1.5"/>')
    text(root_x + root_w / 2, root_y + 41, 'Node & Norm', 27, paper, 600, 'middle')

    for group in range(3):
        x = 48 if mobile else 54 + group * 325
        w = 328 if mobile else 272
        header_y = 132 + group * 486 if mobile else 162
        for line, label in enumerate(groups[group]):
            text(x, header_y + line * 26, label, 21, iris, 600)
        for row in range(3):
            role, key, lines = rows[group * 3 + row]
            y = 184 + group * 486 + row * 126 if mobile else 226 + row * 136
            h = 108 if mobile else 110
            edge_x = 24 if mobile else 32 + group * 325
            parts.append(f'<g id="repository-{key}"><path d="M{edge_x} {y+h/2}H{x}" fill="none" stroke="{iris}" stroke-width="1.5" marker-end="url(#arrow)"/>')
            parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{carbon}" stroke="{iris}" stroke-width="1"/>')
            text(x + 16, y + 27, role, 16, citron)
            for i, label in enumerate(lines):
                text(x + 16, y + 60 + i * 26, label, 21, paper, 600)
            parts.append('</g>')
    parts.append('</svg>')
    result = '\n'.join(parts) + '\n'
    ET.fromstring(result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for name, mobile in [('map-dark.svg', False), ('map-mobile-dark.svg', True)]:
        result = render(mobile)
        p = HERE / name
        if args.check:
            assert p.read_text() == result, f'{name} differs from its source'
        else:
            p.write_text(result)
    print('2 repository maps match.' if args.check else '2 repository maps written.')


if __name__ == '__main__':
    main()
