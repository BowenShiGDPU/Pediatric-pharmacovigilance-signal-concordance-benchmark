#!/usr/bin/env python3
"""Validate the minimal Zenodo data package.

The script checks that the expected public-facing tables are present and, when
available, verifies SHA-256 checksums recorded in metadata/source_data_manifest.tsv.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import pandas as pd


EXPECTED_DIRS = [
    "metadata",
    "benchmark_tables",
    "main_figure_source_data",
    "supplementary_figure_source_data",
]

EXPECTED_FILES = [
    "benchmark_tables/supervised_benchmark_rows.tsv",
    "benchmark_tables/benchmark_model_metrics.tsv",
    "benchmark_tables/benchmark_universe_accounting.tsv",
    "benchmark_tables/endpoint_pt_adjudication_summary.tsv",
    "main_figure_source_data/fig2_detectable_cross_filing_source.tsv",
    "main_figure_source_data/fig3_baseline_performance_source.tsv",
    "main_figure_source_data/fig4_feature_family_ladder_source.tsv",
    "main_figure_source_data/fig5_source_ranking_enrichment_source.tsv",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="Path to the Zenodo data package")
    args = parser.parse_args()

    root = Path(args.data).resolve()
    missing = []
    for rel in EXPECTED_DIRS + EXPECTED_FILES:
        if not (root / rel).exists():
            missing.append(rel)

    manifest_path = root / "metadata" / "source_data_manifest.tsv"
    checksum_failures = []
    if manifest_path.exists():
        manifest = pd.read_csv(manifest_path, sep="\t")
        for _, row in manifest.iterrows():
            rel = Path(str(row["relative_path"]))
            expected = str(row["sha256"])
            path = root / rel
            if not path.exists():
                missing.append(str(rel))
                continue
            observed = sha256_file(path)
            if observed != expected:
                checksum_failures.append((str(rel), expected, observed))

    if missing:
        print("Missing files:")
        for item in sorted(set(missing)):
            print(f"  - {item}")
    if checksum_failures:
        print("Checksum failures:")
        for rel, expected, observed in checksum_failures:
            print(f"  - {rel}: expected {expected}, observed {observed}")

    if missing or checksum_failures:
        raise SystemExit(1)

    print(f"Zenodo data package validated: {root}")


if __name__ == "__main__":
    main()

