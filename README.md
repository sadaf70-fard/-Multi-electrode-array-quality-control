# MEA Quality Control

Automated two-tier quality control for multi-electrode array (MEA) recordings of
iPSC-derived neurons.

Neurons grown from a patient's own cells are cultured on a 48-well plate and
their electrical activity recorded across sixteen electrodes per well. Not every
well works: some are silent because the cells failed to seed or attach, others
produce plenty of signal but behave unlike anything else on the plate. A well
that has not worked will distort any comparison it feeds into, so deciding which
wells to trust is the first real decision in the analysis.

This pipeline makes that decision automatically, and explains every call it
makes.

## How it works

**Tier 1 — activity threshold.** A well is flagged as inactive unless at least
four of its sixteen electrodes are active and it records at least fifty spikes
per electrode. This catches technical failure quickly and transparently, but it
is blind to wells that are active yet abnormal.

**Tier 2 — distribution-based screening.** A random forest scores each surviving
well on all of its electrophysiological features at once, judging it against the
other wells of its own recording rather than against a fixed level of activity.
Wells scoring above 0.5 are flagged as abnormal.

Wells are **flagged, not discarded**. Passing wells go forward for analysis;
flagged wells are passed to the laboratory with an account of what was unusual
about them, so the cause can be investigated.

## Outputs

| Output | Question it answers |
| ------ | ------------------- |
| Retention funnel | How many wells survived each stage, overall and per recording |
| Plate maps | Where on the plate the flagged wells fell |
| Per-well scorecards | Why an individual well was flagged, feature by feature |

The scorecard shows every feature as a robust deviation from the well's own
recording, most abnormal first, so a flag can be checked rather than taken on
trust. An interactive browser lets a scientist step through the review queue by
recording and by well.

## Usage

```bash
git clone https://github.com/<your-username>/mea-quality-control.git
cd mea-quality-control
pip install -r requirements.txt
```

Put the raw exports in `data/raw/` (see [`data/README.md`](data/README.md) for
the expected file naming and schema), then open
`notebooks/mea_qc_pipeline.ipynb` and run the cells in order. The first cell
sets the input folder; override it with the `MEA_INPUT_DIR` environment variable
if your data live elsewhere.

To retrain the tier-2 model on new labels:

```bash
python src/train_tier2_model.py --train data/your_labelled_wells.csv
```

## Repository layout

```
notebooks/mea_qc_pipeline.ipynb   end-to-end pipeline: import to report
src/train_tier2_model.py          trains and serialises the tier-2 model
models/tier2_rf_model.joblib      the deployed model, with its feature list
data/                             expected input location (no data included)
figures/                          generated plate maps, funnel and scorecards
```

## Data availability

The recordings are confidential and are **not** included in this repository.
Only de-identified, aggregated electrophysiological measurements were used in
the original work; the files contain no personal, clinical or genetic
information.

## About

This code accompanies a dissertation submitted for the MSc in Data Science at
Cardiff University. The project compared eleven anomaly-detection methods across
four families — robust statistics, unsupervised detectors, supervised
classifiers and a neural network — under a single leakage-free evaluation
protocol, and integrated the most robust and interpretable of them into the
pipeline above.

The headline finding was a negative one: on a dataset of this size the four
trained models were statistically indistinguishable, so the random forest was
chosen for the stability of its ranking and the calibration of its
probabilities rather than for a superior score.

## Licence

MIT — see [LICENSE](LICENSE).
