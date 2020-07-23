# Exploring RNA secondary structure representations

## Introduction
Structural characterization of RNAs is a dynamic field, exposing many modelling possibilities. Every model is usually characterized by an encoding in which to include structural information of a molecule ranging from string representations to graphs. Introducing a re-interpretation of the Shannon Information applied on RNA alignments, we propose a new scoring metric, the **Relative Information Gain**, available for any position in an alignment, showing how different levels of detail encoded in the RNA representation contribute differently to expose structural information.

Computed RIG values presented in this work can be found in the folder RIG/RIG_nogaps/$MbrVersion_RIGs.tsv

## Preparation


### Clone the repository
```
git clone https://github.com/citterich-lab/RIG.git
cd RIG
```

## How to use


### PLOT RIG values along with WUSS notation
```
execute the notebook in script/compare_RIG_WUSS.ipynb 
the plots will be found in the RIG_WUSS folder
```

### Computing entropy values (modified to be in the same range as RIG):
```
execute the notebook in script/compare_RIG_entropy.ipynb
```

### Build a structural Position Specific Scoring Matrix (sPSSM) from a new Matrix of Bear encoded RNA (MBR)

* Choose the MBR version (for example, `Zbear_62`)
* Select the MBR file from the folder MBR (for example, `MBR/MBR_Zbear_62.tsv`)
* Select the file with the alphabet mapping from the folder alphabets (for example, `alphabets/Zbear.tsv`)
* Be sure the file `gapped_fam_dict.pickle` is in the same folders of `make_PSSM.py` script. You can find it in the `script/` folder
* Go in the script folder
* Run the script with a command like

`python3 make_PSSM.py $mbrVersion $MBR_matrix.tsv $ALPHAMAP.tsv`

which will create the `rfam_PSSM_dic_$mbrVersion.pickle` and `rfam_PSSM_$mbrVersion.pickle` files.

#### Example:
```
cd script
python3 make_PSSM.py ../Zbear_62 ../MBR/MBR_Zbear_62.tsv ../alphabets/Zbear.tsv
ls *Zbear_62.pickle
```

### Build RNA Blocks from Rfam families alignment

To build RNA Blocks from structural alignment you need to:
* Specify the `$structural_alignemnt_folder` with as bear_new_alignment_Zbear_62/
* Specify the `$identity_score threshold` (for example, `62`)
* Specify the `$alphabet` as in folder `alphabets/` (for example, `alphabets/Zbear.tsv`)
* Go in the script folder
* Run the script with a command like

```
python make_blocks.py $structural_alignemnt_folder $identity_score $alphabet
```
#### Example:
```
cd script
python make_blocks.py ../bear_new_alignment_Zbear_62/ 62 ../alphabets/Zbear.tsv
```

### Build Matrix of Bear encoded RNA (MBR) from Rfam Blocks (previous step)

* Specify the `$blocks_folder` as the output of the previous step `blocks_new_bear_*bear_*/`
* Choose the `$identity_score threshold` (for example, `62`)
* Specify the `$alphabet` as in folder `alphabets/` (for example, `alphabets/Zbear.tsv`)
* Specify the `$info_file` as output file that will collect all the information of the built blocks (for example, `info_Zbear_62.txt`)

* Go in the script folder
* Run the script with a command like

```
python3 make_MBR.py $blocks_folder $identity_score $alphabet $info_file
```

#### Example:
```
cd script
python make_MBRs.py ../blocks_new_bear_Zbear_62/ 62 ../alphabets/Zbear.tsv
```


### BlastClust and structural alignment from Rfam families alignment

If you prefer not to use our precomputed structural alignment you can perform it as follows.

#### Dependencies: blastclust

**Note**: the following instructions are for the **Linux** operating system. Please change the ftp link according to your operating system to download the correct version of blastclust (see ftp://ftp.ncbi.nlm.nih.gov/blast/executables/legacy.NOTSUPPORTED/2.2.26/).

```
cd ~
wget -c ftp://ftp.ncbi.nlm.nih.gov/blast/executables/legacy.NOTSUPPORTED/2.2.26/blast-2.2.26-ia32-linux.tar.gz
tar -xvf blast-2.2.26-ia32-linux.tar.gz
export PATH="$PATH:~/blast-2.2.26/bin"
```
Add the `~/blast-2.2.26/bin` directory to your environment, or execute `export PATH="$PATH:~/blast-2.2.26/bin"` each time you open a new shell.


Then you have to:

* Specify the `$sequence_folder` with sequences as in folder `seq_str_families/sequence/` 
* Specify the `$structure_folder` with sequences in BEAR format as in folder `seq_str_families/bear/`
* Specify the Rfam seed sequences (`Rfam_no_double.seed` in the main folder)
* Choose the `$identity_score threshold` (for example, `62`)
* Choose the `$seq_threshold` as the minimum number of RNAs in a Rfam family (for example, `5`)
* Specify the `$alphabet` as in folder `alphabets/` (for example, `alphabets/Zbear.tsv`)
* Go in the script folder
* Run the script with a command like

```
python3 BlustClust_filter_alignment.py $sequence_folder $structure_folder Rfam_no_double.seed $identity_score $seq_threshold $alphabet
```

#### Example:
```
cd script
python BlustClust_filter_alignment.py ../seq_str_families/sequence/ ../seq_str_families/bear/ ../Rfam_no_double.seed 62 5 ../alphabets/Zbear.tsv
```

