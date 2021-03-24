# Compare_LHAPDFsets
Python3 script that automates the plotting of LHAPDF sets and their stats.

## Prerequisites
- Python3
- LHAPDF

## Features

### Colors
![colors](https://github.com/rabah-khalek/Compare_LHAPDFsets/blob/main/colors.png)

### Error types
See https://arxiv.org/Set/1412.7420.pdf for their definitions:
- symmhessian
- hessian
- MC

### Flavours available
- Evolution basis: '$\gamma$' '$\Sigma$' '$g$' '$V$' '$V_3$' '$V_8$' '$V_{15}$' '$V_{24}$' '$V_{35}$' '$T_{3}$' '$T_{3}$' '$T_{15}$' '$T_{24}$' '$T_{35}$'
- Physical basis: '$\bar{t}$' '$\bar{b}$' '$\bar{c}$' '$\bar{s}$' '$\bar{u}$' '$\bar{d}$' '$g$' '$d$' '$u$' '$s$' '$c$' '$b$' '$t$' '$\gamma$'
- Combinations: '$F_2^{LO}$' '$u^+$' '$d^+$' '$s^+$' '$c^+$' '$b^+$' '$t^+$' '$u^-$' '$d^-$' '$s^-$' '$c^-$' '$b^-$' '$t^-$'

### Options in Compare_LHAPDFsets.py
- `Type_of_sets = "PDFs"`
- `comparison_choices = ["test"]`
- `comparison_types = ["Absolutes", "Relative Uncertainty", "Ratio"]`
- `plots_format = ["vertical", "horizontal"]`
- Implement `comparison_choices` in PDFs_fits.yaml

## Output example
Works for any LHAPDF-format.

### Vertical format
![Vertical Ratio](https://github.com/rabah-khalek/Compare_LHAPDFsets/blob/main/PDFs_fits/vertical/test_RatioPDFs_Q10.png?raw=true)
![Vertical Relative](https://github.com/rabah-khalek/Compare_LHAPDFsets/blob/main/PDFs_fits/vertical/test_RelativePDFs_Q10.png?raw=true)
