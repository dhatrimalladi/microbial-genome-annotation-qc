from src.gff3_qc import parse_gff3

def test_parse_gff3():
    result = parse_gff3("src/data/example_annotation.gff3")
    assert result["total_features"] == 4
    assert result["feature_types"]["gene"] == 2
    assert result["feature_types"]["CDS"] == 2