from pathlib import Path
import sys

def parse_gff3(gff3_file):
    """Parse a GFF3 file and return feature counts and types."""
    features = {}
    total_features = 0

    with open(gff3_file, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            parts = line.split("\t")
            if len(parts) >= 9:
                feature_type = parts[2]
                features[feature_type] = features.get(feature_type, 0) + 1
                total_features += 1

    return {
        "total_features": total_features,
        "feature_types": features
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        results = parse_gff3(sys.argv[1])
        print(results)
    else:
        print("Please provide a GFF3 file path.")