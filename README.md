Microbial Genome Annotation QC

A Python-based quality control toolkit for bacterial genome FASTA sequences and GFF3 annotations.

This project demonstrates practical skills in bioinformatics data validation, genome assembly QC, structured biological data processing, automated testing, and reproducible workflows.

Project Overview

The toolkit performs basic quality control on microbial genome sequence and annotation files.

It currently supports:

FASTA sequence parsing
DNA sequence validation
Genome length calculation
GC content calculation
N50 assembly statistic
GFF3 feature parsing
GFF3 structure validation
Coordinate validation
Duplicate feature ID detection
Automated unit testing with pytest
FASTA Quality Control

The FASTA QC module (src/fasta_qc.py) provides:

Sequence Parsing

Reads FASTA files and stores sequences by contig identifier.

Sequence Validation

Checks whether DNA sequences contain only valid nucleotide characters:

A, T, G, C

Invalid characters are reported for further review.

Genome Statistics

The toolkit calculates:

Number of contigs
Total genome length
GC content
N50

For the example genome:

Number of contigs: 2
Genome length: 87 bp
GC content: 49.43%
N50: 44 bp
GFF3 Quality Control

The GFF3 QC module (src/gff3_qc.py) provides:

Feature Parsing

Counts annotated feature types such as:

gene
CDS
Structure Validation

Checks that GFF3 records contain the required 9 columns.

Coordinate Validation

Checks that feature start coordinates do not occur after end coordinates.

Feature ID Validation

Detects duplicate feature IDs within the annotation file.

Project Structure
microbial-genome-annotation-qc/
├── src/
│   ├── data/
│   │   ├── example_annotation.gff3
│   │   ├── example_genome.fasta
│   │   ├── invalid_annotation.gff3
│   │   └── duplicate_ids.gff3
│   ├── __init__.py
│   ├── fasta_qc.py
│   └── gff3_qc.py
├── tests/
│   ├── test_fasta_qc.py
│   └── test_gff3_qc.py
├── .gitignore
└── README.md
Installation

Clone the repository:

git clone https://github.com/dhatrimalladi/microbial-genome-annotation-qc.git
cd microbial-genome-annotation-qc

Install pytest:

pip install pytest
Running the Tests

Run the complete test suite:

python -m pytest

Current test status:

8 passed

The tests cover FASTA parsing, sequence validation, genome statistics, GFF3 parsing, coordinate validation, and duplicate feature ID detection.

Running the Tools
FASTA QC
python src/fasta_qc.py src/data/example_genome.fasta
GFF3 QC
python src/gff3_qc.py src/data/example_annotation.gff3

The repository also includes intentionally invalid GFF3 files used to test validation logic.

Why This Project?

This project was developed to build practical experience with biological data quality control and structured annotation data.

It combines:

Biology and microbiology knowledge
Python programming
Data validation
Scientific data processing
Automated testing
Git and GitHub
Reproducible analysis workflows

The goal is to demonstrate how biological datasets can be parsed, validated, tested, and prepared for downstream analysis.

Future Improvements

Planned improvements include:

More comprehensive GFF3 validation
Required attribute checks
Additional FASTA QC metrics
CSV/JSON report generation
Command-line options
Integration with public biological databases
Processing larger real-world microbial genome datasets
Expanded automated test coverage