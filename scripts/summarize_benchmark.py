#!/usr/bin/env python3
"""Print core benchmark numbers from the Zenodo data package."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="Path to the Zenodo data package")
    args = parser.parse_args()
    root = Path(args.data).resolve()

    rows = pd.read_csv(root / "benchmark_tables" / "supervised_benchmark_rows.tsv", sep="\t")
    metrics = pd.read_csv(root / "benchmark_tables" / "benchmark_model_metrics.tsv", sep="\t")
    anaphylaxis = pd.read_csv(
        root / "main_figure_source_data" / "fig5_source_ranking_enrichment_source.tsv",
        sep="\t",
    )

    print("Primary supervised benchmark")
    print(f"  rows: {len(rows)}")
    print(f"  positives: {int(rows['y'].sum())}")
    print(f"  negatives: {int((rows['y'] == 0).sum())}")
    print()

    wanted = [
        "faers_co_report_plus_endpoint_period",
        "elastic_net_logistic_regression",
        "ebm_additive_small_budget",
        "lightgbm_small_budget",
    ]
    print("Selected comparator AUPRC")
    for model_id in wanted:
        hit = metrics[metrics["model_id"].eq(model_id)]
        if not hit.empty:
            print(f"  {model_id}: {float(hit['auprc'].iloc[0]):.3f}")
    print()

    print("Anaphylaxis source-ranking enrichment")
    for _, row in anaphylaxis.iterrows():
        score = row.get("score", "score")
        mean_rank = float(row["mean_supported_rank_percentile"])
        p_value = float(row["permutation_p_one_sided"])
        print(f"  {score}: mean rank percentile {mean_rank:.3f}, one-sided permutation p={p_value:.4g}")


if __name__ == "__main__":
    main()

