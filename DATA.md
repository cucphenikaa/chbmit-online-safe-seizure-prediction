# Data sources and expected inputs

This repository does not redistribute raw EEG or the large intermediate feature datasets.

## 1. Raw EEG

**CHB-MIT Scalp EEG Database**  
PhysioNet: <https://physionet.org/content/chbmit/1.0.0/>

The segmentation and timestamp-reconstruction notebooks expect the original EDF recordings and CHB-MIT seizure summaries. Follow the PhysioNet access, use, and citation instructions.

## 2. Gap-aware segmentation outputs

Example public batch:

- Kaggle: <https://www.kaggle.com/datasets/cucbuithi/chbmit-segmentation-batch-00>
- Expected dataset family: `CHB-MIT_Segmentation_GAPAWARE_V3`

The complete analysis uses all study subjects retained by the manuscript protocol. Because Kaggle datasets may be split into batches or versions, the feature-extraction notebook discovers patient folders recursively.

## 3. Handcrafted and connectivity features

- Kaggle: <https://www.kaggle.com/datasets/ngoclannguyen00/handcrafted-connectivity>

The feature dataset contains handcrafted epoch-level tables and PLI/pd-wPLI connectivity matrices. In the code, legacy filenames may retain `wPLI`; the implemented phase-difference formulation is reported in the manuscript as **pd-wPLI**.

## 4. Model-ready and prior-stage outputs

The V10-V12 notebooks expect model-ready, gap-aware feature tables and, for resume workflows, compact prior checkpoints. Input discovery is performed below `/kaggle/input`; notebooks print the selected roots before computation.

Typical inputs include:

- `ModelReady_GAPAWARE_V4`
- V10 fold and stream outputs
- V11B online-safe stream outputs
- V12C training timestamp outputs for V12B GUARD10/FORWARD

These derived datasets are large and are intentionally excluded from Git. The compact result tables used by the manuscript are included under `results/`.

## Expected temporal fields

Depending on the stage, tables use fields including:

- `Subject`
- `SeizureID`
- `Class`
- `EpochStart`
- `EpochEnd`
- `Phase`
- `TargetPreictal`
- `EligibleForFAR`
- recording/file identifiers and gap indicators

`EligibleForFAR` is a retrospective scoring mask. It must not be used to decide whether an online alarm is generated.

## Storage guidance

Raw EEG, segmented epochs, connectivity matrices, and per-epoch stream predictions can exceed normal GitHub limits. Keep them in PhysioNet/Kaggle storage. Do not commit EDF, NPY/NPZ, pickle, parquet, checkpoint, or full stream-prediction files to this repository.

