import os
import re
from collections import defaultdict

ROOT_PATH = r"C:\Desktop\06-11-2026\06-11-2026"

SEARCH_TERMS = ["P09", "P10"]

pattern = re.compile(
    r"\b(" + "|".join(re.escape(term) for term in SEARCH_TERMS) + r")\b",
    re.IGNORECASE
)

results = defaultdict(list)

server_09_results = defaultdict(list)
server_10_results = defaultdict(list)

for root, dirs, files in os.walk(ROOT_PATH):
    for file in files:
        if not file.lower().endswith(".xml"):
            continue

        file_path = os.path.join(root, file)

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            matches = pattern.findall(content)

            if matches:
                rel_path = os.path.relpath(file_path, ROOT_PATH)
                path_parts = rel_path.split(os.sep)

                if len(path_parts) > 1:
                    category = path_parts[0]
                else:
                    category = "Root"

                results[category].append(file)

                normalized_matches = [m.lower() for m in matches]

                if "p09" in normalized_matches:
                    server_09_results[category].append(file)

                if "p10" in normalized_matches:
                    server_10_results[category].append(file)

        except Exception as e:
            print(f"Error reading {file_path}: {e}")

for category in sorted(results):
    print(f"\n{category}:")
    for filename in sorted(results[category]):
        print(f"  {filename}")

output_09 = os.path.join(ROOT_PATH, "server_09_results.txt")
output_10 = os.path.join(ROOT_PATH, "server_10_results.txt")

with open(output_09, "w", encoding="utf-8") as f:
    for category in sorted(server_09_results):
        f.write(f"\n{category}:\n")
        for name in sorted(server_09_results[category]):
            f.write(f"  {name}\n")

with open(output_10, "w", encoding="utf-8") as f:
    for category in sorted(server_10_results):
        f.write(f"\n{category}:\n")
        for name in sorted(server_10_results[category]):
            f.write(f"  {name}\n")

print(f"\nSaved:")
print(f"  {output_09}")
print(f"  {output_10}")
