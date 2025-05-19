
# 5g-v2x-qos-allocation

## 🎯 Project Overview

This repository contains the code and documentation for a Master's research internship focused on **radio resource allocation modeling and simulation in 5G NR vehicular networks**, with emphasis on **URLLC/eMBB traffic coexistence** and **quality of service (QoS)** guarantees.

## 📚 Based on

> *Modeling and simulation to ensure QoS for low latency in 5G NR based vehicular networks*  
> Allouch et al., 2025 (IEEE Transactions)

---

## 📁 Repository Structure

```
5g-v2x-qos-allocation/
├── code/            → Python scripts for simulation and analytics
├── data/            → Generated output files (.xlsx, .csv)
├── results/         → Jupyter notebooks, plots and metrics
├── doc/             → Reading notes, discussion documents
├── presentation/    → Meeting slides and reports
├── requirements.txt → Python dependencies
└── README.md        → This file
```

---

## 🧠 Key Concepts

- Two traffic classes:
  - **Class 1**: streaming (non-critical)
  - **Class 2**: URLLC (critical, strict delay)
- Resource allocation strategy:
  - Portion **C₁** guaranteed for class 1
  - Remaining **C₀** shared with **strict priority** for class 2
- Queue model: **Discrete-time Markov chain**, file M/D/C style
- Delay threshold for URLLC: typically **1–5 ms**, depending on the use case

---

## 🧪 Simulation & Reliability Analysis

The simulation (`Simulation.py`) and analytics (`Analytique_calcul_esperance.py`) allow to:

✅ Simulate arrival/service of class 1 and class 2 packets  
✅ Estimate **sojourn time** (delay) for class 2 (URLLC)  
✅ Compute **temporal reliability**:  
> \[
P(\text{delay} \leq D) = \sum_{k=0}^{\lfloor D/T \rfloor} \pi_k
\]

✅ Evaluate **impact of system load**, burstiness, and resource sharing  
✅ Generate Excel reports and distributions

---

## 📈 Notebooks

📓 `results/urlcc_delay_reliability_analysis.ipynb`  
Use this notebook to:

- Calculate the reliability \( R(D) \) for class 2,
- Use either simulated histograms or analytical π(k),
- Visualize the results with thresholds (e.g., green/orange/red zones),
- Replicate the example from `Analyse_Discussion.docx`.

---

## 🔧 How to Use

### 1. Clone and Install

```bash
git clone https://github.com/laminenouri/5g-v2x-qos-allocation.git
cd 5g-v2x-qos-allocation
pip install -r requirements.txt
```

### 2. Run the Simulation

```python
from code.Simulation import simulate_temps_poisson

simulate_temps_poisson(
    N=1000,          # Number of time frames to simulate
    lam_1=3.5,       # Arrival rate (λ₁) for class 1 (streaming)
    lam_2=6.25,      # Arrival rate (λ₂) for class 2 (URLLC)
    m1=12, m2=20,    # Max burst size in slots for class 1 and class 2
    p1=0.6, p2=0.4,  # Probability of burst (Bernoulli compound Poisson)
    C=500,           # Total number of resource blocks (RBs) per frame
    pr1=0.1, pr2=0.0 # Fraction of RBs guaranteed to class 1 or class 2
)
```

---

### 🧩 Code Overview — Simulation.py

1. **Initialization**: define queues, capacity pools, and result containers  
2. **Simulation loop**: generate traffic and allocate resources each frame  
3. **Scheduling logic**: strict priority for class 2, minimum guarantee for class 1  
4. **Metrics collection**: delay, waiting time, occupancy, delay per RB  
5. **Export**: write Excel files to `/data` folder

---

## 📊 Performance Metrics (Key Outputs)

During each simulation run, the following performance metrics are computed and recorded for both traffic classes:

| Metric | Description | Purpose |
|--------|-------------|---------|
| **Sojourn Time** (total delay) | Time from arrival to full service of a packet | Key QoS metric for URLLC |
| **Waiting Time** | Time a packet waits in queue before allocation starts | Reflects scheduling efficiency |
| **Delay per RB** | Time to serve each resource block, derived from total time / number of RBs | Granular indicator of latency |
| **System Occupancy** | Number of clients in the system (Q1, Q2) at each time slot | Used to assess stability (ρ < 1) |
| **Delay Distribution** | Histogram of delays observed for each class | Used to calculate URLLC reliability |
| **Reliability \( R(D) \)** | Probability that a class 2 packet's delay ≤ threshold D | Determines if QoS constraints are met |

📁 These metrics are saved in `data/` as `.xlsx` files, one for each metric (e.g., `dict_compose_poisson_Cl2_del_freq.xlsx`).

### 📌 Why These Metrics Matter

#### ✅ For URLLC (Class 2):
- Delay and reliability are **non-negotiable**
- Delay histograms show performance zones:
  - 🟩 < 1 ms (optimal)
  - 🟧 1–1.5 ms (acceptable)
  - 🟥 1.5–2 ms (critical)
  - ⬛ > 2 ms (not URLLC)

#### 🧮 Analytical Validation:
- Compare delay mean vs. theoretical:
  \[
  E[S_2] \approx \frac{3}{2} \cdot T
  \]
- Validate Markov model via π(k) distribution

#### 📉 System Stability:
- Global load:
  \[
  \rho = \frac{\lambda_1 m_1 p_1 + \lambda_2 m_2 p_2}{C}
  \]
- System must have \( \rho < 1 \) to be stable

---

## 🧾 References

---

## 👤 Author

**Lamine Nouri**  
Research Internship – LYRIDS Lab, ECE Paris  
Supervisor: Dr. Naila Bouchemal  
2025
