import json

from src import ncbi_api


class MockResponse:
    def __init__(self, data):
        self.data = data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def read(self):
        return json.dumps(self.data).encode("utf-8")


def test_search_gene(monkeypatch):
    response_data = {
        "esearchresult": {
            "idlist": ["945803", "913388"]
        }
    }

    def mock_urlopen(url, timeout=30):
        return MockResponse(response_data)

    monkeypatch.setattr(
        ncbi_api.urllib.request,
        "urlopen",
        mock_urlopen,
    )

    result = ncbi_api.search_gene("thrA")

    assert result == ["945803", "913388"]


def test_get_gene_summary(monkeypatch):
    response_data = {
        "result": {
            "945803": {
                "uid": "945803",
                "name": "thrA",
                "description": (
                    "fused aspartate kinase/"
                    "homoserine dehydrogenase 1"
                ),
                "organism": {
                    "scientificname": (
                        "Escherichia coli str. "
                        "K-12 substr. MG1655"
                    ),
                    "taxid": 511145,
                },
                "genomicinfo": [
                    {
                        "chraccver": "NC_000913.3",
                        "chrstart": 336,
                        "chrstop": 2798,
                    }
                ],
                "summary": "Example gene summary",
            }
        }
    }

    def mock_urlopen(url, timeout=30):
        return MockResponse(response_data)

    monkeypatch.setattr(
        ncbi_api.urllib.request,
        "urlopen",
        mock_urlopen,
    )

    result = ncbi_api.get_gene_summary("945803")

    assert result["gene_id"] == "945803"
    assert result["gene_symbol"] == "thrA"
    assert result["organism"] == (
        "Escherichia coli str. K-12 substr. MG1655"
    )
    assert result["taxid"] == 511145
    assert result["chromosome_accession"] == "NC_000913.3"
    assert result["start"] == 336
    assert result["stop"] == 2798


def test_get_gene_summaries(monkeypatch):
    response_data = {
        "result": {
            "uids": ["945803", "913388"],
            "945803": {
                "uid": "945803",
                "name": "thrA",
                "description": "Example thrA",
                "organism": {
                    "scientificname": (
                        "Escherichia coli str. "
                        "K-12 substr. MG1655"
                    ),
                    "taxid": 511145,
                },
                "genomicinfo": [],
                "summary": "Summary A",
            },
            "913388": {
                "uid": "913388",
                "name": "thrA",
                "description": "Example thrA",
                "organism": {
                    "scientificname": "Escherichia coli",
                    "taxid": 562,
                },
                "genomicinfo": [],
                "summary": "Summary B",
            },
        }
    }

    def mock_urlopen(url, timeout=30):
        return MockResponse(response_data)

    monkeypatch.setattr(
        ncbi_api.urllib.request,
        "urlopen",
        mock_urlopen,
    )

    result = ncbi_api.get_gene_summaries(
        ["945803", "913388"]
    )

    assert len(result) == 2
    assert result[0]["gene_id"] == "945803"
    assert result[1]["gene_id"] == "913388"


def test_filter_by_taxid():
    records = [
        {
            "gene_id": "945803",
            "gene_symbol": "thrA",
            "taxid": 511145,
        },
        {
            "gene_id": "913388",
            "gene_symbol": "thrA",
            "taxid": 562,
        },
    ]

    result = ncbi_api.filter_by_taxid(
        records,
        511145,
    )

    assert len(result) == 1
    assert result[0]["gene_id"] == "945803"
    assert result[0]["taxid"] == 511145
