# Scripts of Entity Linking experiments

In this repository, I am sharing the scripts used to obtain the Tables and Charts of the paper "Fine-Grained Evaluation for Entity Linking". This paper (available (here)[https://users.dcc.uchile.cl/~hrosales/papers/2019_EMNLP.pdf]) is going to be presented at (EMNLP'19)[https://www.emnlp-ijcnlp2019.org].

The script detailed here use the nifwrapper package, so, you should install it before running the scripts. Some of these scripts generate the latex file corresponding to Tables and Charts, so, another requirement is the texlive-full in your computer.
```sh
pip3 install -i https://test.pypi.org/simple/ wikitablewrapper
sudo apt-get install texlive-full
```

## Figures

Figure 5 can be generated from the script Figure5-aster2.py. Here we plot the behaviour of selected Entity-Linking systems while a parameter is moved from 0 to 1. 

```sh
python3 Figure5-aster2.py
texi2pdf Figure5-aster2.tex
```

## Tables
Table 3 is generated with Table3-categories.py, which has an latex file as output.
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
Here we store also our relabeled and reannotated datasets.
