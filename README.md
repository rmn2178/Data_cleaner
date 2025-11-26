📊 EnterpriseML Dashboard: CSV Analysis and Visualization ToolThe EnterpriseML Dashboard is a modular, Python-based web application built with Flask that provides quick, deep analysis, cleaning, and interactive visualization of CSV datasets. This tool is designed to help data scientists and analysts rapidly understand data defects, handle missing values, and generate interactive 3D plots.✨ FeaturesData Analysis: Instantly calculates comprehensive statistics, including missing values, unique counts, data types, and memory usage.Defect Detection: Highlights columns containing missing values in the dashboard for immediate visibility.Data Cleaning: Provides options to:Drop rows or columns with missing data.Impute missing numeric values using Mean (Average) or Zero.Impute categorical values using Mode.Interactive Visualization: Generates a variety of plots (Histogram, Scatter, Box, Heatmap).Rotatable 3D Plotting: Uses Plotly for interactive, rotatable 3D scatter plots when three or more numeric columns are selected.Data Export: Option to download the modified and cleaned dataset as a new CSV file.🚀 Setup and InstallationFollow these steps to get the project running locally in a stable Python environment.1. PrerequisitesPython 3.10 or 3.11 (Highly recommended for stable binary wheels)pip (Python package installer)2. Project StructureEnsure your file structure matches the following:EnterpriseML_Dashboard/
├── app.py 
├── requirements.txt
├── data_engine.py
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── cleaning.html
│   └── visualize.html
└── uploads/             # Empty directory for CSV files
3. InstallationOpen your terminal in the EnterpriseML_Dashboard directory and execute the following commands.A. Create and Activate Virtual Environment (Recommended)python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
B. Install DependenciesThe application relies on core scientific packages (pandas, numpy) and web frameworks (Flask, Plotly).pip install -r requirements.txt
4. Run the ApplicationStart the Flask server:python app.py
The application will be accessible at: http://127.0.0.1:5000/🛠️ Technology StackComponentRoleLibraries UsedBackendApplication Routing & LogicFlask, WerkzeugData CoreProcessing, Cleaning, AnalysisPandas, NumPy, Scikit-learnVisualizationStatic 2D Plots & HeatmapsMatplotlib, SeabornInteractive 3DRotatable Scatter PlotsPlotly (Plotly Express)FrontendUser Interface & StylingHTML, Jinja2 Templates, Bootstrap 5, Font Awesome🖼️ Key Features DemoInteractive 3D Scatter PlotThe visualize tab uses Plotly when the 3D Scatter option is selected, allowing users to drag and rotate the plot interactively in the browser.Data Cleaning and ImputationThe cleaning interface provides immediate access to common data preparation steps, enabling rapid transformation of the dataset state.🤝 ContributionThis project is intended as a foundational tool for data exploration. Feel free to fork the repository, suggest enhancements, or contribute features such as machine learning model integration or more advanced data transformations.
