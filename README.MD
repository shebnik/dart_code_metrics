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
    dart pub global activate dart_class_analyzer
    dart pub global activate lakos
    ```
3. Run the script
    ```bash
    python3 main.py
    ```

## Output
The output is stored in a CSV file named `output.csv`. The columns are:
- URL of Repository
- LOC (Lines of Code)
- NOC (Number of Classes)
- NOM (Number of Methods)
- Number of libraries
- Number of dependencies
- CCD (Cumulative Component Dependency)
- Cyclomatic Complexity
- Maintainability Index
- Average Cyclomatic Number per line of code
- Average Source Lines of Code per method