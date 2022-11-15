# Multi-User Frequency Assignment for Ultra-Reliable mmWave Two-Ray Channels

[![DOI](https://img.shields.io/badge/doi-10.23919/WiOpt56218.2022.9930571-informational)](https://doi.org/10.23919/WiOpt56218.2022.9930571)
![GitHub](https://img.shields.io/github/license/klb2/ris-phase-hopping)

This repository is accompanying the paper "Multi-User Frequency Assignment for
Ultra-Reliable mmWave Two-Ray Channels" (K.-L.  Besser, E. Jorswieck, J. Coon,
WiOpt 2022, Sep. 2022.
[doi:10.23919/WiOpt56218.2022.9930571](https://doi.org/10.23919/WiOpt56218.2022.9930571),
[arXiv:2211.07204](https://arxiv.org/abs/2211.07204)).


## File List
The following files are provided in this repository:

- `run.sh`: Bash script that runs all of the simulations to reproduce the
  results from the paper.
- `frequency_assignment.py`: Python script that implements the simulation of
  the frequency assignment together with the comparison algorithms.
- `util.py`: Python module that contains utility functions, e.g., converting to
  decibel.
- `model.py`: Python module that contains model-based calculations.
- `qmkphp.py`: Python module that contains all relevant functions to model and
  solve the quadratic multiple knapsack problem with heterogeneous profits
  (QMKP-HP).
- `single_frequency.py`: Python module that contains the calculations for the
  single frequency scenario.
- `two_frequencies.py`: Python module that contains the calculations for the
  two frequencies scenario.

## Usage
### Running it online
You can use services like [CodeOcean](https://codeocean.com) to run the scripts
online.

### Local Installation
If you want to run it locally on your machine, Python3 and Jupyter are needed.
The present code was developed and tested with the following versions:
- Python 3.10
- numpy 1.22
- scipy 1.8

Make sure you have [Python3](https://www.python.org/downloads/) installed on
your computer.
You can then install the required packages (including Jupyter) by running
```bash
pip3 install -r requirements.txt
```
This will install all the needed packages which are listed in the requirements 
file. 

You can then recreate all of the simulations by running
```bash
bash run.sh
```


## Acknowledgements
This research was supported by the Federal Ministry of Education and Research
Germany (BMBF) as part of the 6G Research and Innovation Cluster 6G-RIC under
Grant 16KISK020K and by the EPSRC under grant number EP/T02612X/1.


## License and Referencing
This program is licensed under the GPLv3 license. If you in any way use this
code for research that results in publications, please cite our original
article listed above.

You can use the following BibTeX entry
```bibtex
@inproceedings{Besser2022wiopt,
	author = {Besser, Karl-Ludwig and Jorswieck, Eduard A. and Coon, Justin P.},
	title = {Multi-User Frequency Assignment for Ultra-Reliable mmWave Two-Ray Channels},
	booktitle = {20th International Symposium on Modeling and Optimization in Mobile, Ad hoc, and Wireless Networks (WiOpt)},
	year = {2022},
	month = {9},
	pages = {283--290},
	publisher = {IEEE},
	doi = {10.23919/WiOpt56218.2022.9930571},
	archiveprefix = {arXiv},
	eprint = {2211.07204},
	primaryclass = {cs.IT},
}
```
