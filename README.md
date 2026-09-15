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
- JSON genome QC reporting
- Automated testing with pytest

## Testing

The project uses pytest for automated testing.

Run:

    PYTHONPATH=. pytest

Current result:

    10 passed

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

The GFF3 validator handles biological annotation cases such as pseudogene-related duplicate IDs and CDS features with exception=ribosomal slippage.

## JSON Reporting

The FASTA QC module can save genome statistics as a JSON report.

Example:

    {
        "number_of_contigs": 2,
        "genome_length": 87,
        "gc_content": 49.43,
        "n50": 44
    }

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
- FASTA/GFF3 sequence ID consistency checks
- Additional genome assembly statistics
- CSV/JSON summary reports
- Support for multiple microbial genomes
