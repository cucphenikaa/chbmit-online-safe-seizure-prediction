# Online-safe patient-specific seizure prediction on CHB-MIT

Reproducible research code for the manuscript on the incremental value of network-level EEG features under seizure-wise and online-safe evaluation. The repository contains the complete Kaggle-oriented workflow from gap-aware EEG segmentation to feature extraction, patient-specific leave-one-seizure-out (LOSO) classification, causal alarm generation, robustness analyses, and publication figures.

## Study overview

- **Dataset:** CHB-MIT Scalp EEG Database
- **Task:** patient-specific preictal versus interictal classification and continuous-stream seizure warning
- **Epoch length:** 10 s
- **Seizure occurrence period (SOP):** 30 min
- **Primary seizure prediction horizon (SPH):** 0 min; 5-min SPH is included as a sensitivity analysis
- **Representations:** handcrafted EEG features, PLI/pd-wPLI connectivity features, graph features, and fused feature blocks
- **Classifiers:** random forest, XGBoost, and RBF-SVM
- **Outer validation:** seizure-wise LOSO
- **Alarm evaluation:** causal firing-power rules, refractory lockout, seizure sensitivity, false-alarm rate per hour, and time to warning

The central methodological distinction is between retrospective **label-gated** scoring and **online-safe** alarm generation. The online-safe generator uses only model outputs, timestamps, observed recording gaps, and prior alarm history while producing alarms. Retrospective labels are consulted only after generation for scoring.

## Repository structure

```text
.
├── notebooks/       # Numbered end-to-end analysis notebooks
├── figures/         # Standalone publication-figure scripts
├── results/         # Compact source tables and final summary outputs
├── DATA.md          # Data sources, expected inputs, and data-use notes
├── CITATION.cff     # Software citation metadata
├── environment.yml  # Conda environment
└── requirements.txt # pip dependencies
```

## Notebook order

| Step | Notebook | Purpose |
|---:|---|---|
| 1 | `01_segmentation_4h_gapaware.ipynb` | Gap-aware CHB-MIT segmentation and phase labels |
| 2 | `02_handcrafted_connectivity_extraction.ipynb` | Handcrafted features and PLI/pd-wPLI matrices |
| 3 | `03_graph_feature_extraction.ipynb` | Graph features derived from connectivity matrices |
| 4 | `04_loso_multimodel_v10.ipynb` | Primary seizure-wise LOSO comparison and stream predictions |
| 5 | `05_postprocess_v11a.ipynb` | Statistical summaries, effect sizes, and terminology audit |
| 6 | `06_online_safe_stream_v11b.ipynb` | Targeted label-gated versus online-safe comparison |
| 7 | `07_chance_sph_cluster_stats_v12a.ipynb` | Chance analysis, SPH sensitivity, TTW, alarm audit, and cluster statistics |
| 8a | `08a_robustness_all21_gamma_seeds_v12b.ipynb` | All 21 configurations, no-gamma analysis, and multiple seeds |
| 8b | `08b_guard10_forward_v12b.ipynb` | 10-min temporal guard and chronological forward evaluation |
| 9 | `09_rebuild_training_timestamps_v12c.ipynb` | Reconstruct absolute training-epoch timestamps required by Step 8b |
| 10 | `10_generate_publication_figures.ipynb` | Generate the manuscript and supplementary figures |

For the final robustness workflow, run Step 9 before Step 8b. Step 8a can be run independently using the model-ready feature dataset and prior checkpoints described in the notebook.

## Quick start

The notebooks were designed for Kaggle because the raw EDF files and intermediate feature datasets are large.

1. Create a Kaggle notebook and attach the required datasets listed in [DATA.md](DATA.md).
2. Install the environment dependencies or use the Kaggle base environment plus:

   ```bash
   pip install -r requirements.txt
   ```

3. Open the notebook for the relevant stage and run it from the first cell.
4. Publish large intermediate outputs as private Kaggle datasets before attaching them to the next stage.
5. Keep `RESET_OUTPUT = False` when resuming a partially completed robustness run; enable it only when intentionally starting a clean run.

The notebooks automatically discover compatible folders under `/kaggle/input` where possible. Exact expected schemas and public data links are documented in [DATA.md](DATA.md).

## Reproducibility notes

- Random seed 42 is the primary analysis seed; the robustness notebook includes additional seeds.
- Balancing is applied to training data only. Held-out classification tests and continuous streams are not training-balanced.
- Scaling, mutual-information feature selection, and model fitting are performed using training data within each fold.
- Temporal gaps and ineligible phases are retained for retrospective scoring but are not used as future-label gates by the online-safe alarm generator.
- Notebook outputs are intentionally cleared in this repository. Compact final tables needed to verify reported results are retained in `results/`.

## Data and privacy

No raw EEG is redistributed here. CHB-MIT is a public, de-identified research dataset hosted by PhysioNet. Users must follow the terms and citation requirements of the original data source. See [DATA.md](DATA.md).

## Citation

If you use this code, cite the software metadata in [CITATION.cff](CITATION.cff) and the associated article once published. The article citation will be updated after acceptance and DOI assignment.

## License

Code is released under the [MIT License](LICENSE). Dataset rights remain with their respective owners.

