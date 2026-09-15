import sys
import json

from src.fasta_qc import genome_statistics
from src.gff3_qc import parse_gff3, validate_gff3, validate_sequence_ids


def run_qc(fasta_file, gff3_file):
    """Run complete genome and annotation quality control."""
    fasta_results = genome_statistics(fasta_file)
    gff3_results = parse_gff3(gff3_file)
    gff3_validation = validate_gff3(gff3_file)
    sequence_id_validation = validate_sequence_ids(
        fasta_file,
        gff3_file,
    )

    return {
        "fasta": fasta_results,
        "gff3": gff3_results,
        "gff3_validation": gff3_validation,
        "sequence_id_validation": sequence_id_validation,
    }


def save_report(results, output_file):
    """Save QC results as a JSON report."""
    with open(output_file, "w") as file:
        json.dump(results, file, indent=4)


def print_summary(results):
    """Print a human-readable QC summary."""
    fasta = results["fasta"]
    gff3 = results["gff3"]

    print("QC Summary")
    print("----------")
    print(f"Genome length: {fasta['genome_length']} bp")
    print(f"Number of contigs: {fasta['number_of_contigs']}")
    print(f"GC content: {fasta['gc_content']}%")
    print(f"N50: {fasta['n50']} bp")
    print(f"GFF3 features: {gff3['total_features']}")
    print(f"GFF3 valid: {results['gff3_validation']['is_valid']}")
    print(
        "Sequence IDs consistent: "
        f"{results['sequence_id_validation']['is_valid']}"
    )


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: python -m src.run_qc "
            "<genome.fasta> <annotation.gff3> [report.json]"
        )
        sys.exit(1)

    fasta_file = sys.argv[1]
    gff3_file = sys.argv[2]

    results = run_qc(fasta_file, gff3_file)
    print_summary(results)

    if len(sys.argv) > 3:
        save_report(results, sys.argv[3])
        print(f"JSON report saved to {sys.argv[3]}")
