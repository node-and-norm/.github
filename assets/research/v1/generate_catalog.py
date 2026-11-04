"""Generate the reviewed research-entry asset catalog from explicit project metadata."""
import argparse
import hashlib
import html
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import generate as shared

HERE = Path(__file__).resolve().parent
NS = '{http://www.w3.org/2000/svg}'


def banner(tokens, config, theme, mobile):
    colors = {k: tokens['colors'][v] for k, v in tokens['themes'][theme].items()}
    title_lines = config['mobile_title_lines'] if mobile else [config['title']]
    purpose_lines = config['mobile_purpose_lines'] if mobile else [config['purpose']]
    title_size = config.get('mobile_title_size', 32) if mobile else config.get('desktop_title_size', 44)
    purpose_size = 20 if mobile else 24
    title_y, step = (103, 37) if mobile else (128, 0)
    purpose_y = title_y + (len(title_lines)-1)*step + 43 if mobile else 174
    width = 400 if mobile else 1000
    height = max(260, purpose_y + (len(purpose_lines)-1)*27 + 44) if mobile else 230
    x, top = (24, 18) if mobile else (34, 25)
    svg = shared.svg_start(width, height, config['title']+' | Node & Norm', config['purpose'])
    svg += f'<rect width="{width}" height="{height}" fill="{colors["background"]}"/>\n'
    svg += shared.witness(colors['accent'],x-7,top-4,.36 if mobile else .48)
    svg += shared.wordmark(colors['text'],colors['accent'],x+(35 if mobile else 46),top,.12 if mobile else .16)
    font = html.escape(tokens['typography']['family'],quote=True)
    for i,line in enumerate(title_lines):
        svg += f'<text x="{x}" y="{title_y+i*step}" fill="{colors["text"]}" font-family="{font}" font-size="{title_size}" font-weight="600" letter-spacing="-1">{html.escape(line)}</text>\n'
    for i,line in enumerate(purpose_lines):
        svg += f'<text x="{x}" y="{purpose_y+i*27}" fill="{colors["text"]}" font-family="{font}" font-size="{purpose_size}">{html.escape(line)}</text>\n'
    svg += f'<rect x="{x}" y="{height-20}" width="72" height="4" fill="{colors["marker"]}"/>\n</svg>\n'
    return svg.encode()


def catalog_badge(tokens,item,theme):
    colors={k:tokens['colors'][v] for k,v in tokens['themes'][theme].items()}
    label_width=max(55,len(item['label'])*7+20)
    width=label_width+max(80,len(item['value'])*7+22)
    svg=shared.svg_start(width,26,item['label']+': '+item['value'],'Project metadata. Follow the surrounding link for its source and scope.')
    svg+=f'<rect x=".5" y=".5" width="{width-1}" height="25" rx="3" fill="{colors["background"]}" stroke="{colors["accent"]}"/>\n'
    svg+=f'<path d="M{label_width} 1V25" stroke="{colors["accent"]}"/>\n'
    font=html.escape(tokens['typography']['family'],quote=True)
    svg+=f'<g font-family="{font}" font-size="12" text-anchor="middle"><text x="{label_width/2}" y="17" fill="{colors["text"]}">{html.escape(item["label"])}</text><text x="{label_width+(width-label_width)/2}" y="17" fill="{colors["accent"]}">{html.escape(item["value"])}</text></g>\n</svg>\n'
    return svg


def outputs(path):
    config = json.loads(path.read_text())
    tokens = json.loads((HERE/'tokens.json').read_text())
    result = {}
    for theme in ['light','dark']:
        for mobile in [False,True]:
            suffix = '-mobile' if mobile else ''
            result[f'banner{suffix}-{theme}.svg'] = banner(tokens,config,theme,mobile)
        for item in config.get('badges',[]):
            result[f'badges/{item["id"]}-{theme}.svg'] = catalog_badge(tokens,item,theme).encode()
    receipt = {'asset_version':tokens['asset_version'],'config':str(path.relative_to(HERE)),
        'input_hashes':{str(p.relative_to(HERE)):shared.sha256(p) for p in [path,HERE/'tokens.json',HERE/'generate.py',HERE/'generate_catalog.py']},
        'source_hashes':{name:shared.sha256(shared.ROOT/name) for name in ['assets/brand/current/logo.svg','assets/brand/current/banner.svg']},
        'files':{name:hashlib.sha256(data).hexdigest() for name,data in result.items()}}
    result['manifest.json']=(json.dumps(receipt,indent=2)+'\n').encode()
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    count=0
    for path in sorted((HERE/'projects').glob('*/config.json')):
        generated=outputs(path)
        for name,data in generated.items():
            target=path.parent/name
            if name.endswith('.svg'):
                root=ET.fromstring(data)
                assert root.find(NS+'title') is not None and root.find(NS+'desc') is not None
                assert root.attrib['role']=='img'
            if args.check:
                assert target.exists() and target.read_bytes()==data, str(target)
            else:
                target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
            count+=1
    assert count, 'No project configurations found'
    print(f'{count} catalog outputs {"match" if args.check else "written"}.')


if __name__=='__main__':main()
