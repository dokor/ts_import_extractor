import os
import re
import json
import csv
from collections import Counter, defaultdict
from typing import Dict, List, Tuple

dependance_to_analyze = 'XXXXXXXXXXXXX'

projects_input = {
    "mon-super-projet": "/chemin/vers/mon-super-projet",
    "un-autre-projet": "/chemin/vers/un-autre-projet"
}

def extract_imports_from_file(filepath: str) -> List[str]:
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    pattern = re.compile(
        r'import\s*{\s*([^}]+?)\s*}\s*from\s*[\'"]'+dependance_to_analyze+'[\'"]\s*;',
        re.MULTILINE | re.DOTALL
    )
    matches = pattern.findall(content)

    components = []
    for match in matches:
        parts = match.split(',')
        parts = [p.strip().split(' as ')[0] for p in parts if p.strip()]
        components.extend(parts)
    return components

def extract_versions(package_json_path: str) -> Tuple[str, str]:
    try:
        with open(package_json_path, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
            kitui_version = package_data.get('dependencies', {}).get(dependance_to_analyze) or \
                            package_data.get('devDependencies', {}).get(dependance_to_analyze)
            project_version = package_data.get('version')
            return kitui_version or "N/A", project_version or "N/A"
    except Exception:
        return "N/A", "N/A"

def analyze_project(project_name: str, project_path: str) -> Dict:
    usage_counter = Counter()

    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(('.ts', '.tsx')):
                filepath = os.path.join(root, file)
                components = extract_imports_from_file(filepath)
                usage_counter.update(components)

    package_json_path = os.path.join(project_path, 'package.json')
    kitui_version, project_version = extract_versions(package_json_path)

    return {
        "project_name": project_name,
        "project_path": project_path,
        "kitui_version": kitui_version,
        "project_version": project_version,
        "components_usage": dict(usage_counter)
    }

def analyze_projects(projects: Dict[str, str]) -> List[Dict]:
    results = []
    for name, path in projects.items():
        result = analyze_project(name, path)
        results.append(result)
    return results

def export_to_csv(results: List[Dict], output_path: str):
    with open(output_path, mode='w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(["Project Name", "Project Version", "KitUI Version", "Component", "Usage Count"])

        for project in results:
            for component, count in project["components_usage"].items():
                writer.writerow([
                    project["project_name"],
                    project["project_version"],
                    project["kitui_version"],
                    component,
                    count
                ])

analysis_results = analyze_projects(projects_input)
csv_output_path = "analyse_kitui.csv"
export_to_csv(analysis_results, csv_output_path)

csv_output_path