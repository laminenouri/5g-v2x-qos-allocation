# Fiche de lecture 1 : Modeling and Simulation to Ensure QoS for Low Latency in 5g NR Vehicular Networks (2025)

## Référence
Allouch et al., IEEE Transactions on Green Communications and Networking, 2025

## Contexte
Besoin de communications critiques (URLLC) dans les systèmes V2X. Coexistence de flux critiques (classe 2) et non-critiques (classe 1) dans un même slice 5G NR.

## Objectif
Proposer un modèle analytique pour le partage de ressources à priorité stricte avec garantie minimale, et évaluer la performance QoS.

## Méthodologie
- File M/D/C avec Poisson composé pour les arrivées
- Partage C0/C1 avec priorité stricte
- Chaîne de Markov
- Validation par simulation discrète

## Résultats
- Délai classe 2 ≈ 1.5T
- Stabilité si ρ < 1
- Bon alignement modèle/simulation

## Limites
Mono-cellule, pas de WFQ, modèle statique