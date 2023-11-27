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
    # Clone the repository
    subprocess.run(f"git clone {repo} {str(i)}", shell=True)
    # input(f"Press Enter to continue... {str(i)}")

    # Run Dart Code Metrics tool
    subprocess.run(
        "metrics lib -r html --json-path metrics.json", shell=True, cwd=str(i)
    )

    # Run Dart Class Analyzer tool
    method_count = subprocess.run(
        f"dart pub global run dart_class_analyzer:method_counter {str(i)}/lib",
        shell=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    try:
        # Read the HTML file
        with open(f"{str(i)}/metrics/index.html", "r") as file:
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
        with open(f"{str(i)}/metrics.json") as f:
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
                csv_rows.append(
                    [
                        repo,
                        lines_of_code,
                        num_classes,
                        num_methods,
                        cyclomatic_complexity,
                        maintainability_index,
                        cyclomatic_number,
                        source_lines_of_code,
                    ]
                )
    except:
        csv_rows.append([repo, "", "", "", "", "", "", ""])

    shutil.rmtree(str(i), ignore_errors=True)
    i += 1

# Write the list of lists to a CSV file
with open(os.path.join(results_dir, "results.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        [
            "URL",
            "LOC",
            "NOC",
            "NOM",
            "Cyclomatic Complexity",
            "Maintainability Index",
            "Average Cyclomatic Number per line of code",
            "Average Source Lines of Code per method",
        ]
    )
    writer.writerows(csv_rows)
