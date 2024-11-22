# College Mobility Analysis Dashboard

An interactive dashboard for analyzing intergenerational income mobility in higher education institutions.

## Features

- Mobility Ladder Analysis: Compare mobility rates across different institution tiers
- Affordability Analysis: Examine the relationship between cost and mobility outcomes
- Interactive Filtering: Filter institutions by various metrics including percentage of low-income students
- Data Visualization: Dynamic charts and graphs for data exploration

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd DemoProject
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

## Project Structure

```
DemoProject/
├── app.py              # Main application entry point
├── config.py           # Configuration settings
├── data/              # Data directory
├── docs/              # Documentation
├── requirements.txt    # Project dependencies
├── tests/             # Test suite
├── utils/             # Utility functions
└── views/             # Streamlit view components
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

We use several tools to maintain code quality:

- `black`: Code formatting
- `flake8`: Code linting
- `mypy`: Static type checking

Run these tools before committing:

```bash
black .
flake8 .
mypy .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and code quality checks
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
