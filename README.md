# UK Election Model

A UK general election projection model, built from scratch: raw census demographics
and historical vote flows in, seat-by-seat probabilistic projections and an
interactive constituency map out.

The live map built from this data lives in a separate repo (the personal site) at
[app/index.html](https://github.com/AndyYuxiao-Wang/website) - this repo is the
pipeline and research behind it, not the frontend.

## What it does

**`pipeline/`** - the core projection pipeline. Instead of uniform national swing,
voters are split into "tribes" (Muslim, Left, Progressives, Average, Liberal, Blues,
Reforms) with different preference orderings between parties, and national swing is
applied per-tribe rather than uniformly. Stages, run in order by `run_all.py`:

1. `01_allocate_tribes.py` - split each constituency's 2024 vote into tribe shares
2. `02_project_flows.py` - apply tribe transition matrices to project new vote shares
3. `03_monte_carlo.py` - simulate seat outcomes under projection uncertainty
4. `04_tactical_voting.py` - squeeze non-winnable parties' vote toward the locally
   winnable alternative (winnable = incumbent, projected leader, or within 10pts)
5. `05_export_svg_output.py` - apply local flow adjustments, write final results
6. `06_export_demographics.py` / `07_export_alloc.py` / `08_export_brexit.py` -
   export supplementary layers (census demographics, tribe allocation, EU ref 2016
   results) for the map to plot alongside vote projections

Run the whole thing with:

```
py pipeline/scripts/run_all.py
```

**`clustering/`** - a separate research question: does an unsupervised clustering
of constituencies by demographics + vote history recover anything like the
hand-built "tribes" above, or find its own structure? Runs PCA, K-Means,
Agglomerative, Gaussian Mixture, and DBSCAN per nation, cross-checked against the
tribe allocation and against national vote regressions. Scripts are numbered
01-07 in `clustering/scripts/`; the three notebooks in `clustering/notebooks/`
walk through the fragmentation/latent-groups analysis, a 632-seat sort, and the
end-to-end prediction pipeline in narrative form.

**`notebooks/predicting_house_prices_and_london.ipynb`** - a related but standalone
piece: predicting house prices from socioeconomic profile, and specifically
testing whether London behaves as an outlier relative to the rest of the country.

**`web/`** - the pipeline's data/maps staging directory (not the live site - see
below). This is what the scripts in `pipeline/` and `clustering/` read and write.

## Setup

```
pip install -r requirements.txt
```

## Regenerating the site's data

The live site (separate repo) serves pre-generated static data - it never runs
this pipeline itself. After changing the model and rerunning it:

```
py pipeline/scripts/run_all.py
py export_to_site.py [path-to-website-repo]
```

`export_to_site.py` copies `web/data/` and `web/maps/` (the pipeline's output)
into `site/app/data/` and `site/app/maps/` in the site repo. It defaults to
`../website` (i.e. this repo and the site repo cloned as siblings) - pass an
explicit path if yours are laid out differently. Review the resulting diff in
the site repo and commit it there.

## Data sources

Raw inputs live in `pipeline/data/raw/` (constituency-level vote flows, boundary
data) and the root-level `.xlsx` files (`demographics.xlsx`: census variables per
seat; `Brexit.xlsx`: 2016 EU referendum results; `predictionTable.xlsx`: manual
what-if predictor lookup table used by the map's custom predictor).
