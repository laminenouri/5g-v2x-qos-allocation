```markdown
# 5g-v2x-qos-allocation

## 🎯 Project Overview

This repository contains the research work conducted as part of a Master's thesis focused on the **modeling and simulation of radio resource allocation** in 5G NR vehicular networks. The project specifically addresses **QoS constraints** for **URLLC** (Ultra-Reliable Low Latency Communications) and **eMBB** (enhanced Mobile Broadband) traffic classes coexisting in the same network slice.

## 🧪 Objective

To evaluate, both analytically and through simulation, a **priority-based resource allocation strategy** ensuring low latency and reliability for URLLC, while maintaining minimal service for eMBB flows.

## 📚 Based on

> *Modeling and simulation to ensure QoS for low latency in 5G NR based vehicular networks*  
> Allouch et al., 2025 (IEEE Transactions)

## 🏗️ Repository Structure

```

5g-v2x-qos-allocation/
│
├── code/            → Python scripts (simulation and analytical model)
├── data/            → Output files (.xlsx, .csv)
├── results/         → Graphs, plots, metrics
├── doc/             → Summaries, notes, reference materials
├── presentation/    → Slides, meeting notes, interim reports
├── requirements.txt → Python dependencies
├── .gitignore       → Ignored files and folders
└── README.md        → You are here

````

## 🛠️ Technologies

- Python 3.10+
- Libraries: `pandas`, `numpy`, `matplotlib`, `tqdm`, `openpyxl`, `mpmath`

Install dependencies:
```bash
pip install -r requirements.txt
````

## 🚀 How to Use

Import and run the simulation:

```python
from code.Simulation import simulate_temps_poisson

simulate_temps_poisson(
    N=1000,
    lam_1=3.5, lam_2=6.0,
    m1=12, m2=5,
    p1=0.6, p2=0.3,
    C=500,
    pr1=0.1, pr2=0.0
)
```

## 📈 Output

* Delays, occupancy states, reliability metrics
* Exported as Excel files in `/data`
* Graphs and plots available in `/results`

## 👤 Author

**Lamine Nouri**
Master's Thesis – Research Internship
ECE Paris, LYRIDS Research Lab
Supervised by Dr. Naila Bouchemal

```


