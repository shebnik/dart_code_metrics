import os
import subprocess
import json
import csv
from bs4 import BeautifulSoup
import shutil

# Load list of repositories urls
with open("repositories.txt", "r") as f:
    repositories = f.read().splitlines()

results_dir = os.getcwd()

# Create a directory to store the repositories
directory = "repositories"
csv_rows = []
if not os.path.exists(directory):
    os.mkdir(directory)
os.chdir(directory)

# Clone repositories and run Dart Code Metrics
i = 1
for repo in repositories:
    path = os.path.join(os.getcwd(), str(i))
    
    # Clone the repository
    try:
        subprocess.run(f"git clone {repo} {path}", shell=True)
    except Exception as e:
        print(e)
        csv_rows.append([repo, "", "", "", "", "", "", "", "", "", ""])
        continue

    # check if pubspec.yaml exists, if not, cd to the nested directory containing it
    if not os.path.exists(os.path.join(path, "pubspec.yaml")):
        for subdir, dirs, files in os.walk(path):
            for file in files:
                if file == "pubspec.yaml":
                    # Change to the nested directory
                    path = subdir
                    break
    
    lib_path = os.path.join(path, "lib")

    # Run Dart Code Metrics tool
    subprocess.run(f"metrics lib -r html --json-path metrics.json", shell=True, cwd=path)

    # Run Dart Class Analyzer tool
    method_count = subprocess.run(
        f"dart pub global run dart_class_analyzer:method_counter {lib_path}",
        shell=True,
        stdout=subprocess.PIPE,
        text=True,
    )

    # Run Lakos tool
    lakos_output = subprocess.run(
        f"dart pub global run lakos {lib_path} -m",
        shell=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    lakos_metrics = [
        line for line in lakos_output.stdout.split("\n") if "metrics" in line
    ][0]

    try:
        # Read the HTML file
        with open(f"{os.path.join(path, "metrics", "index.html")}", "r", encoding="utf-8") as file:
            html_content = file.read()

        # Parse the HTML content
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract the metrics
        metrics_totals = soup.find_all("div", class_="metrics-total")
        cyclomatic_complexity = (
            metrics_totals[0].find("span", class_="metrics-total__count").text
        )
        maintainability_index = (
            metrics_totals[2].find("span", class_="metrics-total__count").text
        )

        # Read the JSON file
        with open(f"{os.path.join(path, "metrics.json")}", "r", encoding="utf-8") as f:
            data = json.load(f)

        # Extract the required data and store it in a list of lists
        for item in data["summary"]:
            if item["title"] == "Total lines of source code":
                lines_of_code = item["value"]
            elif item["title"] == "Total classes":
                num_classes = item["value"]
            elif item["title"] == "Average Cyclomatic Number per line of code":
                cyclomatic_number = item["value"]
            elif item["title"] == "Average Source Lines of Code per method":
                source_lines_of_code = item["value"]
                try:
                    num_methods = int(method_count.stdout.strip())
                except:
                    num_methods = ""
                num_nodes = int(lakos_metrics.split("numNodes: ")[1].split(r"  \l")[0])
                num_edges = int(lakos_metrics.split("numEdges: ")[1].split(r"  \l")[0])
                ccd = int(lakos_metrics.split("ccd: ")[1].split(r" \l")[0])

                csv_rows.append(
                    [
                        repo,
                        lines_of_code,
                        num_classes,
                        num_methods,
                        num_edges,
                        num_nodes,
                        ccd,
                        cyclomatic_complexity,
                        maintainability_index,
                        cyclomatic_number,
                        source_lines_of_code,
                    ]
                )
    except Exception as e:
        print(e)
        csv_rows.append([repo, "", "", "", "", "", "", "", "", "", ""])

    # shutil.rmtree(path, ignore_errors=True)
    i += 1

# Write the list of lists to a CSV file
with open(os.path.join(results_dir, "results.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        [
            "URL",
            "LOC (Lines of Code)",
            "NOC (Number of Classes)",
            "NOM (Number of Methods)",
            "Number of libraries",
            "Number of dependencies",
            "CCD (Cumulative Component Dependency)",
            "Cyclomatic Complexity",
            "Maintainability Index",
            "Average Cyclomatic Number per line of code",
            "Average Source Lines of Code per method",
        ]
    )
    writer.writerows(csv_rows)
    shutil.rmtree(directory, ignore_errors=True)
