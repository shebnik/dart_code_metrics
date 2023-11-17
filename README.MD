# Dart Code Metrics
This is a simple Python script to automate the process of running the [Dart Code Metrics](https://dcm.dev/) tool on a Flutter projects. It uses the links of repositories provided in repositories.txt file to clone the repositories and run the tool on them. The results are stored in a CSV file.

## How to use
1. Clone the repository
    ```bash
    git clone https://github.com/shebnik/dart_code_metrics.git
    ```
2. Install the dependencies
    ```bash
    dart pub global activate dart_code_metrics
    ```
3. Run the script
    ```bash
    python3 dart_code_metrics.py
    ```

## Output
The output is stored in a CSV file named `output.csv`. The columns are:
- Repository url
- Lines of code
- Number of classes
- Cyclomatic Complexity
- Maintainability Index
- Average Cyclomatic Number per line of code
- Average Source Lines of Code per method