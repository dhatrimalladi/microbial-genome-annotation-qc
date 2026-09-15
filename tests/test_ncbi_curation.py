from src import ncbi_curation


def test_load_gene_symbols(tmp_path):
    csv_file = tmp_path / "genes.csv"

    csv_file.write_text(
        "gene_id,gene_symbol,product,feature_type,organism,evidence_source\n"
        "gene1,thrL,protein,gene,E. coli,NCBI RefSeq\n"
        "gene2,thrA,enzyme,gene,E. coli,NCBI RefSeq\n"
    )

    result = ncbi_curation.load_gene_symbols(csv_file)

    assert result == ["thrL", "thrA"]


def test_validate_gene_against_ncbi(monkeypatch):
    def mock_search_gene(gene_symbol):
        assert gene_symbol == "thrA"
        return ["945803"]

    def mock_get_gene_summaries(gene_ids):
        assert gene_ids == ["945803"]

        return [
            {
                "gene_id": "945803",
                "gene_symbol": "thrA",
                "organism": (
                    "Escherichia coli str. "
                    "K-12 substr. MG1655"
                ),
                "taxid": 511145,
            }
        ]

    monkeypatch.setattr(
        ncbi_curation,
        "search_gene",
        mock_search_gene,
    )

    monkeypatch.setattr(
        ncbi_curation,
        "get_gene_summaries",
        mock_get_gene_summaries,
    )

    result = ncbi_curation.validate_gene_against_ncbi(
        "thrA"
    )

    assert result == {
        "gene_symbol": "thrA",
        "ncbi_match": True,
        "gene_id": "945803",
    }


def test_validate_gene_without_ncbi_match(monkeypatch):
    monkeypatch.setattr(
        ncbi_curation,
        "search_gene",
        lambda gene_symbol: [],
    )

    result = ncbi_curation.validate_gene_against_ncbi(
        "unknown_gene"
    )

    assert result == {
        "gene_symbol": "unknown_gene",
        "ncbi_match": False,
        "gene_id": None,
    }


def test_validate_gene_wrong_taxid(monkeypatch):
    monkeypatch.setattr(
        ncbi_curation,
        "search_gene",
        lambda gene_symbol: ["123456"],
    )

    monkeypatch.setattr(
        ncbi_curation,
        "get_gene_summaries",
        lambda gene_ids: [
            {
                "gene_id": "123456",
                "gene_symbol": "thrA",
                "organism": "Escherichia coli",
                "taxid": 562,
            }
        ],
    )

    result = ncbi_curation.validate_gene_against_ncbi(
        "thrA"
    )

    assert result == {
        "gene_symbol": "thrA",
        "ncbi_match": False,
        "gene_id": None,
    }
