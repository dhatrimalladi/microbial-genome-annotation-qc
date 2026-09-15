# Microbial Genome Annotation QC

Python-based quality control of bacterial genome FASTA sequences and GFF3 annotations.

## Project Overview

This project provides basic quality-control checks for microbial genome sequence and annotation files.

It demonstrates practical skills in:

* Python programming
* FASTA parsing
* GFF3 parsing
* Biological sequence validation
* Genome statistics
* Annotation quality control
* Error detection
* Automated testing with pytest
* Git and GitHub

## Features

### FASTA QC

The FASTA QC module can:

* Read FASTA files
* Identify individual contigs
* Calculate genome length
* Calculate GC content
* Validate DNA sequences
* Identify invalid nucleotide characters

### GFF3 QC

The GFF3 QC module can:

* Parse GFF3 annotation files
* Count annotation features
* Summarize feature types
* Check that records contain 9 columns
* Validate numeric start and end coordinates
* Detect cases where start coordinates are greater than end coordinates
* Detect duplicate feature IDs

## Project Structure

```text
microbial-genome-annotation-qc/
├── src/
│   ├── data/
│   │   ├── example_annotation.gff3
│   │   ├── example_genome.fasta
│   │   ├── invalid_annotation.gff3
│   │   └── duplicate_ids.gff3
│   ├── fasta_qc.py
│   └── gff3_qc.py
│
├── tests/
│   ├── test_fasta_qc.py
│   └── test_gff3_qc.py
│
├── .gitignore
└── README.md
```

## Installation

Clone the repository and install pytest:

```bash
pip install pytest
```

## Running the Tests

Run all automated tests with:

```bash
python -m pytest
```

Current test status:

```text
8 passed
```

## Example FASTA Statistics

The example genome contains two contigs.

The current implementation calculates:

```text
Number of contigs: 2
Genome length: 87 bp
GC content: 49.43%
```

## Example GFF3 Validation

The project includes valid and intentionally invalid GFF3 files to test QC functionality.

Examples of detected problems include:

```text
start coordinate is greater than end
duplicate feature ID
```

This allows the project to demonstrate both successful validation and detection of problematic annotation records.

## Why This Project?

Genome annotation files are structured biological datasets that need quality checks before downstream analysis.

This project demonstrates an approach to programmatically checking biological data for structural and content-related inconsistencies.

The project is also designed as a practical learning exercise in biological data curation, validation, Python, testing, and reproducible data workflows.

## Future Improvements

Potential future extensions include:

* More comprehensive GFF3 validation
* Required attribute checks
* Additional FASTA QC metrics
* N50 calculation
* CSV/JSON report generation
* Command-line options
* Integration with public biological databases
* Larger real-world microbial genome datasets


            