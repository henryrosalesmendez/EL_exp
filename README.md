
# Scripts of Entity Linking experiments

In this repository, I am sharing the scripts used to obtain the Tables and Charts of the paper "Fine-Grained Evaluation for Entity Linking". This paper (available [here](http://aidanhogan.com/docs/fine_grained_entity_linking.pdf)) presented at [EMNLP'19](https://www.emnlp-ijcnlp2019.org). Also, we include the script used in a journal extension of this paper.

A considerable part of the code is available from the pypi repository, namely in the packages: `nifWrapper`, `wrapperCoreference` and `wrapperWSD`. Some of these scripts generate the latex file corresponding to Tables and Charts, so, another requirement is the `texlive-full` in your computer. First, install them and other dependencies, 

```sh
# packages from authors
pip3 install nifwrapper==1.5.2
pip3 install wrapperCoreference
pip3 install wrapperWSD

# others
pip3 install xmltodict
pip3 install spacy
pip3 install stanfordnlp
pip3 install nltk
pip3 install pywsd
pip3 install spacy==2.1.0

# latex interpreter
sudo apt-get install texlive-full

# dependencies
python3 -m spacy download en
wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip
```


Then, run inside python3
```
> import nltk
> nltk.download()
```

The following codes use NIF files with the annotation of Entity Linking systems, as well as their extensions with Coreference and WSD. Those scripts to create the NIF files are available in the folder `NIF_Generation`.


## Figures

Figure 5 can be generated from the script Figure5-aster2.py. Here we plot the behaviour of selected Entity-Linking systems while a parameter is moved from 0 to 1. 

```sh
python3 Figure5-aster2.py
texi2pdf Figure5-aster2.tex
```

## Tables
Table 3 is generated with Table3-categories.py, which has a latex file as output.
```sh
python3 Table3-categories.py
texi2pdf Table3-categories.tex
```

In order to generate Tables 4, 5 and 6, you should run the script Table4_5_6-Appendix.py. This script generates the latex file 'Table4_5_6-Appendix.tex', which contains tables 4, 5 and 6 of our paper. These tables show the behavior of five selected systems on our re-annotated and labeled datasets.
```sh
python3 Table4_5_6-Appendix.py
texi2pdf Table4_5_6-Appendix.tex
```
The script TableAster_notIncludedYet.py show the content of the evaluation of the datasets with F1 and F1* . However, this table was removed from the paper.
```sh
python3 TableAster_notIncludedYet.py
```

## Benchmark Dataset
We also publish our relabeled and reannotated datasets, for the up-to-date version see this [repo](https://github.com/henryrosalesmendez/categorized_EMNLP_datasets).




# Journal Extension

We gather Tables 5, 6, 7 and 8 of our journal extension in the script ```Table_5_6_7_8_WSD_Coreference.py``` which generate the latex file to obtain them. 

```
Then, just run the script,
```bash
python3 Table_5_6_7_8_WSD_Coreference.py
```
