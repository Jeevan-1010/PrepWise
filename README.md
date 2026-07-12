# PrepWise

## AI-Powered Data Preparation Platform

PrepWise is an AI-powered data preparation and analysis platform developed using Python, Streamlit, Scikit-learn, and Groq LLM. It simplifies the data preprocessing workflow by enabling users to upload datasets, clean data, analyze data quality, detect anomalies, generate AI-assisted insights, and export processed datasets through a unified interface.

---

## Features

### Dataset Upload

* Upload CSV datasets
* Upload Excel (.xlsx) datasets

### Data Cleaning

* Handle missing values
* Remove duplicate rows
* Prepare cleaned datasets for analysis

### Dataset Analysis

* Dataset summary
* Data type inspection
* Summary statistics
* Correlation matrix
* Dataset quality score

### Machine Learning Analysis

* Outlier detection using Isolation Forest
* K-Means clustering
* Principal Component Analysis (PCA)

### AI Assistance

PrepWise integrates the Groq API to provide intelligent recommendations, including:

* Dataset quality assessment
* Data cleaning recommendations
* Feature engineering suggestions
* Executive summaries
* Interactive dataset assistance

### Export

* Download cleaned datasets
* Export analysis reports

---

## Technology Stack

* Python
* Streamlit
* Pandas
* NumPy
* Scikit-learn
* Groq API
* Plotly
* fastApi

---

## Project Structure

```text
PrepWise/
│
├── backend/
│   ├── ai.py
│   ├── analyzer.py
│   └── ...
│
├── frontend/
│   ├── app.py
│   ├── ui.py
│   ├── dashboard.py
│   ├── cleaning.py
│   ├── analysis.py
│   ├── download.py
│   └── sidebar.py
│
├── assets/
├── requirements.txt
├── README.md
└── .env
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Jeevan-1010/PrepWise.git
cd PrepWise
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows

```bash
.venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root and add your Groq API key.

```text
GROQ_API_KEY=your_api_key_here
```

---

## Running the Application

Start the application using:

```bash
streamlit run frontend/app.py
```

---

## Project Objective

Data preprocessing is one of the most time-consuming stages of the data science workflow. PrepWise aims to simplify this process by integrating traditional preprocessing techniques with AI-powered recommendations, enabling users to prepare datasets efficiently before model development and analysis.

---

## Future Scope

Potential enhancements include:

* Support for additional dataset formats
* Automated feature selection
* Interactive data visualizations
* Model training and evaluation
* Cloud deployment
* User authentication and project management

---

## Developer

**Jeevan M**

Academic Project (2026)

---

## License

This project was developed for educational and academic purposes.
