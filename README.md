# Microbial Genome Annotation QC

A Python-based quality control and structured data curation workflow for bacterial genome FASTA sequences, GFF3 annotations, curated gene records, and SQLite databases.

This project demonstrates practical bioinformatics data validation using Python, automated testing, SQL, and real NCBI RefSeq genomic data.

## Project Overview

The goal of this project is to perform quality control and structured data processing on microbial genome assemblies and their corresponding annotations.

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
- Structured gene curation QC
- Required-field validation
- Duplicate curated gene detection
- Feature type validation
- SQLite database creation
- Loading curated gene records into SQLite
- Loading GFF3 annotations into SQLite
- SQL-based biological data retrieval
- Gene/CDS parent-child relationship queries
- Combined command-line QC workflow
- JSON QC reporting
- Automated testing with pytest

## Project Structure

    microbial-genome-annotation-qc/
    ├── src/
    │   ├── data/
    │   │   ├── example_annotation.gff3
    │   │   ├── example_genome.fasta
    │   │   ├── curated_genes.csv
    │   │   ├── invalid_curated_genes.csv
    │   │   └── missing_sequence.gff3
    │   ├── fasta_qc.py
    │   ├── gff3_qc.py
    │   ├── run_qc.py
    │   ├── curation_qc.py
    │   ├── database.py
    │   ├── database_queries.py
    │   └── annotation_database.py
    ├── tests/
    │   ├── test_fasta_qc.py
    │   ├── test_gff3_qc.py
    │   ├── test_run_qc.py
    │   ├── test_curation_qc.py
    │   └── test_database_queries.py
    ├── .gitignore
    └── README.md

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

## Structured Gene Curation

The project includes a curated gene dataset stored in CSV format.

Example fields:

    gene_id
    gene_symbol
    product
    feature_type
    organism
    evidence_source

The curation QC module validates:

- Required columns
- Missing values
- Duplicate gene IDs
- Allowed feature types
- Record counts

Run:

    python -m src.curation_qc src/data/curated_genes.csv

Example output:

    Curation QC
    -----------
    Records: 5
    Valid: True

An intentionally invalid dataset is also included for testing validation failures.

## SQLite Database

Curated gene records can be loaded into a SQLite database.

Create the database with:

    python -m src.database

Example output:

    Database created successfully
    Records loaded: 5
    Records in database: 5

The SQLite database is generated locally and is excluded from Git using:

    *.db

SQLite is an embedded relational database, making it useful for learning SQL and building a lightweight structured biological data workflow without requiring a database server.

## SQL-Based Biological Data Retrieval

The project provides Python functions for retrieving biological records from SQLite.

Examples include:

    get_all_genes()
    get_gene_by_symbol()
    count_genes()
    get_cds_for_gene()

A gene can be retrieved using its symbol:

    SELECT gene_id, gene_symbol, product
    FROM genes
    WHERE gene_symbol = 'thrA';

Example result:

    gene2 | thrA | homoserine dehydrogenase

## GFF3 Annotation Database

GFF3 annotations can also be loaded into SQLite.

Run:

    python -m src.annotation_database

Example output:

    Annotation table created successfully
    Annotations loaded: 4

The annotation table stores information such as:

- Feature ID
- Feature type
- Sequence ID
- Start coordinate
- End coordinate
- Strand
- Parent feature ID

This allows biological relationships to be queried using SQL.

For example, CDS features can be associated with their parent gene:

    SELECT
        gene.gene_symbol,
        gene.product,
        cds.feature_id,
        cds.sequence_id,
        cds.start,
        cds.end
    FROM genes AS gene
    JOIN annotations AS cds
        ON cds.parent_id = gene.gene_id
    WHERE cds.feature_type = 'CDS';

Example result:

    thrL | protein-coding gene | cds1 | contig_1 | 3  | 15
    thrL | protein-coding gene | cds2 | contig_1 | 16 | 20

This demonstrates a relational biological data model in which curated gene information is connected to genomic annotation features.

## Testing

The project uses pytest for automated testing.

Run:

    PYTHONPATH=. pytest

Current result:

    23 passed

The tests cover:

- FASTA parsing and validation
- Genome statistics
- GFF3 parsing and validation
- Duplicate feature IDs
- FASTA/GFF3 sequence ID consistency
- Curated gene validation
- SQLite database creation
- SQL-based gene retrieval
- Gene/CDS relationship queries
- Combined QC workflow
- JSON report generation

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

## Tools and Technologies

- Python
- SQLite
- SQL
- pytest
- FASTA
- GFF3
- CSV
- JSON
- Git
- GitHub
- NCBI RefSeq
- NCBI Datasets CLI

## Future Improvements

- Parent-child relationship validation
- More comprehensive GFF3 validation
- Additional genome assembly statistics
- CSV summary reports
- Support for multiple microbial genomes
- Integration with public biological databases and APIs
- More advanced biological entity normalization
- Larger real-world curated datasets
