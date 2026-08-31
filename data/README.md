# Data

The MEA recordings analysed by this pipeline are **confidential** and are not
included in this repository.

## Expected input

Place the raw exports in `data/raw/`, then point the pipeline at that folder
(the notebook reads `MEA_INPUT_DIR`, which defaults to `data/raw`).

Two files per recording, named so the pipeline can tell them apart:

| Suffix             | Contents                                              |
| ------------------ | ----------------------------------------------------- |
| `*_spike_stats.csv`| Per-well spike statistics: one row per active well     |
| `*_sb_stats.csv`   | Per-well network-burst statistics: bursting wells only |

The plate number and timepoint are read from the `Filename` column, which must
contain text of the form `28dpp PLATE 3`.

Wells that never produced coordinated bursting have no row in the network-burst
file. This is expected: the pipeline keeps those wells and encodes the
missingness with a `bursted` flag rather than discarding or imputing them.

## Training data

`src/train_tier2_model.py` expects a labelled table with the same feature
columns plus a `qc_fail` column (`1` = fail). It is likewise not included.
