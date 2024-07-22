# Metrica Data Preprocessing

This repository contains the preprocessing steps for the Metrica Sports Sample Data. The goal is to prepare the data for various research applications such as EPV, Un-xPass, PitchControl, and Intended-receiver Prediction.

## Overview

The Metrica dataset includes a wide variety of event types, and it does not store the success or failure of these events. These factors limit its immediate usability. This preprocessing aims to address these limitations and prepare the data for advanced analysis.

## Steps for Preprocessing

1. **Download Data**
   - Download the full dataset from the [Metrica Sports Sample Data repository](https://github.com/metrica-sports/sample-data). Due to size limitations, only a portion of the data is included here.

2. **Run Notebooks Sequentially**
   - Follow the order of the provided notebooks for preprocessing.

### Notebooks

- **4-analyze-Intended-receiver.ipynb**:
  - In cases of failed passes, the intended receiver's information (the "to" column) is set to NaN since the pass intention is not clear. To address this limitation, we manually labeled the intended receiver for failed passes.

### Labeling Process

- The labeling was conducted by two researchers, and cross-validated to ensure accuracy.

For further reference or collaboration, you can check the contributors' profiles. Note that `@menguri` is the GitHub username of another contributor and should be linked accordingly.

## Contributors

- Main Author: [조건희](https://github.com/GunHeeJoe)
- Contributor: [강민구](https://github.com/menguri)

---

By following the steps outlined above, you can preprocess the Metrica dataset to make it more suitable for advanced research and analysis.
