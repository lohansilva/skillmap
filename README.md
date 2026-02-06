# Competency Map Dashboard

## Overview
The **Competency Map Dashboard** is a data-driven tool designed to analyze and visualize the technical skills of team members. Built with **Streamlit** and **Plotly**, it provides intuitive insights into skill proficiencies, gaps, and categorical balance.

## Features
- **Excel Data Integration**: Dynamically loads team data from `resources/skills.xlsx`.
- **Interactive Visualizations**:
    - **Radar Chart**: Visualizes the balance of skills across categories (RPA, Backend, Frontend, Cloud).
    - **Sorted Bar Charts**: Displays skills ordered by proficiency, highlighting top strengths (Level 5) first.
- **Gap Analysis**: Automatically identifies and lists skills requiring development (Level 0-1).
- **Dark Mode UI**: A professional, high-performance corporate aesthetic.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/lohansilva/skillmap.git
    cd skillmap
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the application**:
    ```bash
    streamlit run app.py
    ```

2.  **Access the Dashboard**:
    Open your browser at `http://localhost:8501`.

## Data Configuration
The dashboard relies on `resources/skills.xlsx` for data. Ensure the file uses the following schema:
- `Colaborador`: Name of the team member.
- `Categoria`: Tech category (e.g., Backend, Cloud).
- `Competência`: Specific skill name.
- `Nível (0-5)`: Proficiency score (0 to 5).

## Technologies
- **Python**: Core logic.
- **Streamlit**: Web framework.
- **Plotly**: Interactive charts.
- **Pandas/OpenPyXL**: Data processing.
