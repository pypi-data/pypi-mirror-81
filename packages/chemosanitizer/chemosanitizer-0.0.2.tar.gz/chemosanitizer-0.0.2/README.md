# chemo_sanitizer

A set of script using RDKit and MolVS to proceed to the standardization , sanitization and different format conversion. Parallelized.

In this state it take only InChI as inputs and returns sanitized SMILES, InChI, InChIKeys, Short InChIkeys, MolecularFormula, ExactMass and XLogP.

## Requirements 

Install the conda environment by

`conda env create -f environment.yml`

### Specific requirement

Note that some modules of MolVS are not loaded by default. 
You will need to edit the MolVS  __init__.py in ~/opt/anaconda3/lib/python3.7/site-packages/molvs/ accordingly.
Add these lines to the __init__.py

```
from .fragment import LargestFragmentChooser, FragmentRemover
from .charge import Uncharger
```



## Usage

Go to the src folder 
Then add input and output file path as first and second argument, InChI column header as third argument and finally the number of cpus you want to use.

Example :
        
```
cd src
python chemosanitizer.py ~/translatedStructureRdkit.tsv ./test.tsv structureTranslated 6
```


