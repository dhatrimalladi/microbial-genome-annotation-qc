# Microbial Genome Annotation QC

A Python-based quality control tool for bacterial genome FASTA sequences and GFF3 annotations.

This project demonstrates practical bioinformatics data validation using Python, automated testing, and real NCBI RefSeq genomic data.

## Project Overview

The goal of this project is to perform basic quality control on microbial genome assemblies and their corresponding genome annotations.

The workflow includes:

- FASTA sequence parsing
- DNA sequence validation
- GC-content calculation
- Genome length calculation
- N50 calculation
- GFF3 feature counting
- GFF3 structure validation
- Coordinate validation
- Feature ID validation
- Duplicate feature ID detection
- Handling of biological annotation exceptions
- FASTA/GFF3 sequence ID consistency validation
- Combined command-line QC workflow
- JSON QC reporting
- Automated testing with pytest

## Running the QC Workflow

The complete QC workflow can be run with:

    python -m src.run_qc src/data/example_genome.fasta src/data/example_annotation.gff3

Example output:

    QC Summary
    ----------
    Genome length: 87 bp
    Number of contigs: 2
    GC content: 49.43%
    N50: 44 bp
    GFF3 features: 4
    GFF3 valid: True
    Sequence IDs consistent: True

A JSON report can also be generated:

    python -m src.run_qc src/data/example_genome.fasta src/data/example_annotation.gff3 genome_report.json

## Testing

The project uses pytest for automated testing.

Run:

    PYTHONPATH=. pytest

Current result:

    14 passed

The tests cover FASTA parsing and validation, genome statistics, GFF3 validation, duplicate feature IDs, FASTA/GFF3 sequence ID consistency, the combined QC workflow, and JSON report generation.

## Real NCBI RefSeq Dataset

The project was tested against the NCBI RefSeq genome:

**Organism:** *Escherichia coli* K-12 MG1655  
**Assembly:** GCF_000005845.2  
**Assembly level:** Complete Genome

### FASTA QC

    Number of contigs: 1
    Genome length: 4,641,652 bp
    GC content: 50.79%
    N50: 4,641,652 bp

### GFF3 QC

    Total features: 9,523
    is_valid: True
    errors: []

The GFF3 validator handles biological annotation cases such as pseudogene-related duplicate IDs and CDS features with `exception=ribosomal slippage`.

## JSON Reporting

The FASTA QC module and combined QC workflow can save results as a JSON report.

Example:

    {
        "number_of_contigs": 2,
        "genome_length": 87,
        "gc_content": 49.43,
        "n50": 44
    }

The combined workflow produces a structured report containing FASTA statistics, GFF3 feature statistics, GFF3 validation results, and FASTA/GFF3 sequence ID consistency results.

## Tools and Technologies

- Python
- pytest
- FASTA
- GFF3
- JSON
- Git
- GitHub
- NCBI RefSeq
- NCBI Datasets CLI

## Future Improvements

- More comprehensive GFF3 validation
- Parent-child relationship validation
- Additional genome assembly statistics
- CSV summary reports
- Support for multiple microbial genomes
