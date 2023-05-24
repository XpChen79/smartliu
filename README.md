# An in-house Command Line Interface to process tag-based scRNA-Seq data.


## Installation  
  

### Dependence

1. some common genome analysis tools, Including but no limited to: `hisat2`, `samtools`, `htseq-count`, `bamtools`, `bam2fastx`, `R`,`multiqc`. see [tools] section in configs/mm10.config file to find more information.   

2. It is highly recommended to use `mamba install your-tool-name` to install dependcies. Conda envioments cound be mamaged by [Mamba](https://github.com/conda-forge/miniforge) that could save your time.
If you are in China mainland, try to use the local anaconda mirrors. Here is an example using [the mirrors of Tsinghua University](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/).
```shell
channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch-lts: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
```

`$mamba install -c bioconda fastqc cutadapt hisat2 samtools htseq bam2fastx bamtools multiqc`

`$mamba install -c conda-forge R=4.0 perl biopython`


The installation of parts of tools may meet some problem, for these, they could be installed by `pip` package manager. 


3. Some R packages and perl module `JSON` are required
```
 # For JSON.pm used in scripts/paired2single.pl 
cpanm install JSON
## It could be also installed by mamba if you get some problems from `cpanm`
mamba install -c bioconda perl-json

# For R packages used in scripts/*.R
r_packages <- ("rjson", "rtracklayer", "mixtools", "ggplot2", "reshape2", "ggthemr", "gridExtra")
# You may use BiocManager::install(r_packages) to install them
```

4. genome and trancscriptome index files build by hisat2-build   
Ensembl http://www.ensembl.org/info/data/ftp/index.html
Gencode http://www.gencodegenes.org/
- get genome fasta sequence   
`wget ftp://ftp.ensembl.org/pub/release-90/fasta/mus_musculus/dna/Mus_musculus.GRCm38.dna.primary_assembly.fa.gz`
- get RefSeq genes annotation   
`wget ftp://ftp.ncbi.nlm.nih.gov/genomes/H_sapiens/ARCHIVE/ANNOTATION_RELEASE.107/GFF/ref_GRCh38.p2_top_level.gff3.gz`
- or Alternative, Here are detailed steps for converting a local hg19 refGene table (in genePred format) to GTF.   
```
#Download your gene set of interest for hg19. For this example, I'll use the refGene table, 
#but you can choose other gene sets, such as the knownGene table from the "UCSC Genes" track.
$rsync -a -P rsync://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz ./
#Unzip
$gzip -d refGene.txt.gz
#Remove the first "bin" column:
$cut -f 2- refGene.txt > refGene.input
#Convert to gtf:
$genePredToGtf file refGene.input hg19refGene.gtf
#Sort output by chromosome and coordinate
$cat hg19refGene.gtf  | sort -k1,1 -k4,4n > hg19refGene.gtf.sorted
#gff2gtf
$gffread my.gff3 -T -o transcripts.gtf
#gtf2gff
$gffread merged.gtf -o- > merged.gff3

#you may append Spike-in gtf to transcript.gtf
$cat ERCC92_RGC.gtf >> transcripts.gtf
#Given our limited computing resource of our labServer "DELL T630" -- 56PC 256GB, 
#I choose to use HISAT2 (told 50 times faster) as mapper instead of Tophat2. 
#Build hisat2 index
#genome index
$hisat2-build -p 30 genome.fa genome
#add transcriptome info to index by doing
$extract_splice_sites.py transcripts.gtf > transcripts.ss
$extract_exons.py transcripts.gtf > transcripts.exon
$hisat2-build -p 30 --ss transcripts.ss --exon transcripts.exon genome.fa genome.trans
```

### Install  
`$git clone 'Repository Address'`  
`$cd smartliu`  
`$pip install .`
 

## Test
Please use test_data to ensure everything is OK.  eg.   `smartliu -c mm10 -i test_data -o smart_mm10`



## Usage

Use `smartliu --help` to see how to start    
