"""
Train the tier-2 random forest on the consensus-labelled wells and save it
together with the exact feature list it expects.

    python src/train_tier2_model.py --train data/MEA_data_consensus_training_vote2.csv

The training file is not included in this repository: it holds confidential
data supplied by the industrial partner. See data/README.md for the schema.
"""
import argparse

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

META = ["Barcode", "Plate", "Timepoint_dpp", "Well", "Control",
        "QC_low_activity", "qc_fail"]


def main(train_file: str, model_file: str, seed: int = 42) -> None:
    td = pd.read_csv(train_file)
    feats = [c for c in td.columns
             if c not in META and pd.api.types.is_numeric_dtype(td[c])]

    # Burst features are NaN when a well never bursted. That missingness is
    # informative, so flag it explicitly and fill with 0 rather than impute.
    burst = [c for c in feats if td[c].isna().any()]
    td["bursted"] = td[burst[0]].notna().astype(int)
    td[burst] = td[burst].fillna(0.0)
    feats = feats + ["bursted"]

    X = td[feats].to_numpy(float)
    y = (td["qc_fail"].astype(str) == "1").astype(int).to_numpy()   # 1 = fail

    rf = RandomForestClassifier(
        n_estimators=500,
        max_depth=None,
        max_features="log2",
        min_samples_leaf=6,
        class_weight="balanced_subsample",
        random_state=seed,
    )
    rf.fit(X, y)

    # Save the model with its feature list and burst columns, so that new data
    # are prepared exactly as the training data were.
    joblib.dump({"model": rf, "feats": feats, "burst": burst}, model_file)
    print(f"Trained on {len(td)} wells ({y.sum()} fail / {len(y) - y.sum()} pass); "
          f"saved to {model_file}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--train", default="data/MEA_data_consensus_training_vote2.csv")
    ap.add_argument("--out", default="models/tier2_rf_model.joblib")
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()
    main(a.train, a.out, a.seed)
