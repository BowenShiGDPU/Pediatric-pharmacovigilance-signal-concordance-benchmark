# Pediatric pharmacovigilance signal-concordance benchmark

This repository contains the minimal public code companion for the manuscript
**"A manufacturer-aware cross-national benchmark for pediatric pharmacovigilance signal concordance"**.

The code is intentionally small. It validates and summarizes the public Zenodo
data package. It is not a parser for raw database archives and does not
redistribute raw regulatory databases or controlled vocabularies.

## What is included

- Lightweight validation utilities for the Zenodo derived-data package.
- Summary scripts that reproduce the key benchmark counts and model-comparison
  numbers from the released tables.
- Documentation of the public source systems and reuse boundaries.

## What is not included

- Raw FAERS/AERS, Canada Vigilance, or JADER extracts.
- Licensed vocabulary files such as MedDRA.
- End-to-end raw-extract processing scripts.
- Working files, temporary analysis outputs, and local machine paths.
- Any patient-level narratives or private identifiers.

## Quick start

Install dependencies:

```bash
pip install -r requirements.txt
```

Validate a downloaded Zenodo data package:

```bash
python scripts/validate_zenodo_data.py --data ../zenodo_data
```

Print the core benchmark summary:

```bash
python scripts/summarize_benchmark.py --data ../zenodo_data
```

## Data package

The machine-readable source data are released separately on Zenodo. Place the
Zenodo folder next to this repository, or pass its location with `--data`.

## Citation

If you use this benchmark, please cite the accompanying manuscript and the Zenodo
dataset DOI once available.


