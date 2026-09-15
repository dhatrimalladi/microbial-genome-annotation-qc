import json
import sys
import urllib.parse
import urllib.request


def search_gene(gene_symbol, organism="Escherichia coli K-12"):
    """Search NCBI Gene for a gene symbol and organism."""
    params = urllib.parse.urlencode(
        {
            "db": "gene",
            "term": f"{gene_symbol}[Gene Name] AND {organism}[Organism]",
            "retmode": "json",
        }
    )

    url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        f"esearch.fcgi?{params}"
    )

    with urllib.request.urlopen(url, timeout=30) as response:
        data = json.load(response)

    return data["esearchresult"]["idlist"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m src.ncbi_api <gene_symbol>")
        sys.exit(1)

    gene_symbol = sys.argv[1]

    results = search_gene(gene_symbol)

    print(f"NCBI Gene IDs for {gene_symbol}:")
    print(results)
