# Compare_LHAPDFsets
Python3 script that automates the plotting of LHAPDF sets and their stats.

## Prerequisites
- Python3
- LHAPDF

## Features
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

## Output

### Horizontal format
![Horizontal Absolutes](https://github.com/rabah-khalek/Compare_LHAPDFsets/blob/main/PDFs_figs/horizontal/test_AbsolutesPDFs_Q10.pdf?raw=true)
![Horizontal Ratio](https://github.com/rabah-khalek/Compare_LHAPDFsets/blob/main/PDFs_figs/horizontal/test_RatioPDFs_Q10.pdf?raw=true)
![Horizontal Relative](https://github.com/rabah-khalek/Compare_LHAPDFsets/blob/main/PDFs_figs/horizontal/test_RelativePDFs_Q10.pdf?raw=true)

### Vertical format
![Vertical Absolutes](https://github.com/rabah-khalek/Compare_LHAPDFsets/blob/main/PDFs_figs/vertical/test_AbsolutesPDFs_Q10.pdf?raw=true)
![Vertical Ratio](https://github.com/rabah-khalek/Compare_LHAPDFsets/blob/main/PDFs_figs/vertical/test_RatioPDFs_Q10.pdf?raw=true)
![Vertical Relative](https://github.com/rabah-khalek/Compare_LHAPDFsets/blob/main/PDFs_figs/vertical/test_RelativePDFs_Q10.pdf?raw=true)
