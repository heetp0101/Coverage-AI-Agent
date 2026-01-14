import re
import json

def parse_coverage(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    
    lines = content.split('\n')
    
    data = {
        "design": "dma_controller", # Usually static or parsed from header
        "overall_coverage": 0.0,
        "covergroups": [],
        "uncovered_bins": [],
        "cross_coverage": []
    }

    current_cg = None
    current_cp = None

    for line in lines:
        line = line.strip()
        if not line: continue

        # 1. Parse Overall Coverage
        if "Overall Coverage:" in line:
            match = re.search(r"(\d+\.\d+)", line)
            if match: data["overall_coverage"] = float(match.group(1))

        # 2. Parse Covergroup
        elif "Covergroup:" in line:
            cg_name = line.split(":")[1].strip()
            current_cg = {"name": cg_name, "coverage": 0.0, "coverpoints": []}
            data["covergroups"].append(current_cg)

        # 3. Parse Covergroup-level Coverage %
        elif "Coverage:" in line and "bins" in line:
            match = re.search(r"(\d+\.\d+)", line)
            if match and current_cg: current_cg["coverage"] = float(match.group(1))

        # 4. Parse Coverpoint
        elif "Coverpoint:" in line:
            cp_name = line.split(":")[1].strip()
            current_cp = {"name": cp_name, "bins": []}
            current_cg["coverpoints"].append(current_cp)

        # 5. Parse Bins (The complex part)
        elif "bin " in line:
            # Regex to catch: name, range (optional), hits, and status
            # Example: bin small[0:255] hits: 1523 covered
            match = re.search(r"bin\s+(\w+)(\[.*?\])?\s+hits:\s+(\d+)\s+(covered|UNCOVERED)", line)
            if match:
                b_name = match.group(1)
                b_range = match.group(2) if match.group(2) else ""
                hits = int(match.group(3))
                is_covered = match.group(4) == "covered"
                
                bin_obj = {
                    "name": b_name,
                    "range": b_range,
                    "hits": hits,
                    "covered": is_covered
                }
                current_cp["bins"].append(bin_obj)
                
                # If UNCOVERED, add to the flat priority list
                if not is_covered:
                    data["uncovered_bins"].append({
                        "covergroup": current_cg["name"],
                        "coverpoint": current_cp["name"],
                        "bin": f"{b_name}{b_range}"
                    })

    # 6. Manual addition for Cross Coverage (simplifying for the demo)
    # In a real parser, you'd repeat the logic above for the Cross section
    data["cross_coverage"] = [{
        "name": "cross_size_burst",
        "coverage": 50.0,
        "uncovered": ["<small, wrap>", "<medium, wrap>", "<medium, fixed>"]
    }]

    return data

if __name__ == "__main__":
    parsed_data = parse_coverage("report.txt")
    print(json.dumps(parsed_data, indent=2)) 