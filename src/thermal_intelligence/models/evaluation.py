"""Shared evaluation metrics for classification, clustering, and anomaly detection."""

from __future__ import annotations

import pandas as pd
from sklearn.metrics import (
    classification_report,
    precision_recall_fscore_support,
    silhouette_score,
)


def classification_metrics(y_true: pd.Series, y_pred: pd.Series) -> dict:
    """Precision/recall/F1 (macro + per-class) for the event-type classifier."""
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="macro")
    return {
        "macro_precision": precision,
        "macro_recall": recall,
        "macro_f1": f1,
        "report": classification_report(y_true, y_pred, output_dict=True),
    }


def clustering_validity(features: pd.DataFrame, cluster_labels: pd.Series) -> float | None:
    """Silhouette score for the spatiotemporal clustering result.

    Returns `None` if fewer than 2 clusters were found (silhouette is undefined
    in that case) rather than raising, so evaluation pipelines can proceed.
    """
    n_clusters = cluster_labels.nunique()
    if n_clusters < 2:
        return None
    return silhouette_score(features, cluster_labels)


def precision_at_k(risk_scores: pd.Series, ground_truth_positive: pd.Series, k: int) -> float:
    """Fraction of the top-`k` highest-risk-scored events that are true positives.

    Useful for evaluating whether the risk-scoring output (risk/scoring.py) actually
    prioritizes the events that matter, independent of the raw classifier metrics.
    """
    top_k_ids = risk_scores.sort_values(ascending=False).head(k).index
    return ground_truth_positive.reindex(top_k_ids).fillna(False).mean()
