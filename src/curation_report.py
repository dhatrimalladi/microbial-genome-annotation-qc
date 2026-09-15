import sys

from src.database_queries import get_gene_by_symbol
from src.database_queries import get_annotation_for_gene


def build_gene_report(database_file, gene_symbol):
    gene = get_gene_by_symbol(database_file, gene_symbol)
    annotations = get_annotation_for_gene(database_file, gene_symbol)

    return {
        "gene": gene,
        "annotations": annotations,
    }


def print_gene_report(report):
    gene = report["gene"]

    print("Gene Curation Report")
    print("--------------------")

    if gene is None:
        print("Gene not found")
        return

    print("Gene ID:", gene[0])
    print("Gene symbol:", gene[1])
    print("Product:", gene[2])
    print("Feature type:", gene[3])
    print("Organism:", gene[4])
    print("Evidence source:", gene[5])

    print()
    print("NCBI Annotation Records:")

    for annotation in report["annotations"]:
        print(
            annotation[3],
            annotation[2],
            annotation[4],
            annotation[5],
            annotation[6],
            annotation[7],
        )


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m src.curation_report <database.db> <gene_symbol>")
        sys.exit(1)

    report = build_gene_report(sys.argv[1], sys.argv[2])
    print_gene_report(report)
