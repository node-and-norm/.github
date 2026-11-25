# Repository map assets

This archived map preserves nine repository relationships in the [v1 Mermaid source](source.mmd). The [generator](generate.py) groups them under the three themes used in the original organization profile. The [shared tokens](../tokens.json) supply Carbon, paper, iris and citron colors.

Version 1 uses a fixed SVG to preserve its layout across GitHub views. The [desktop map](map-dark.svg) shows three columns. The [mobile map](map-mobile-dark.svg) stacks the same groups. Both use the approved dark palette. The top node reuses the [Witness mark and outlined wordmark helpers](../generate.py), which read the [preserved v1 artwork](../source-artwork/). See the [current organization profile](../../../../profile/README.md) for the latest directory.

Run these commands from the repository root with Python 3.9 or later. The generator uses the standard library.

```sh
python3 assets/research/v1/repository-map/generate.py
python3 assets/research/v1/repository-map/generate.py --check
```

Expected output: `2 repository maps written.` followed by `2 repository maps match.`
