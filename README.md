# MediScan Health Report Analyzer 🩺

![MediScan Banner](https://via.placeholder.com/1200x300/4ca1af/ffffff?text=MediScan+Health+Report+Analyzer)

## Overview

MediScan is an AI-powered health report analysis tool that extracts, analyzes, and provides personalized recommendations from blood test PDFs. The application uses advanced natural language processing to interpret medical data and generate actionable health insights.

## Features

- **PDF Extraction**: Automatically extracts text content from blood test report PDFs
- **AI-Powered Analysis**: Processes medical data to identify key health indicators
- **Personalized Recommendations**: Generates custom health advice based on test results
- **Interactive Visualizations**: Displays health metrics in easy-to-understand charts and graphs
- **User-Friendly Interface**: Modern, intuitive UI designed for users without medical background

## Tech Stack

- **Frontend & Backend**: Streamlit
- **AI Model**: LLaMA 3.3 70B Versatile
- **PDF Processing**: PyPDF2/PyMuPDF
- **Inference API**: Groq API
- **Data Visualization**: Pandas, Streamlit native charts

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mediscan.git
cd mediscan
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

4. Set up environment variables:
```bash
# Create a .env file in the project root
echo "GROQ_API_KEY=your_groq_api_key" > .env
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Access the application in your web browser at `http://localhost:8501`

3. Upload a blood test report PDF

4. Review the extracted data, analysis, and personalized recommendations

## Project Structure

```
mediscan/
├── app.py                  # Main Streamlit application
├── pdf_processor.py        # PDF text extraction functions
├── agent.py                # AI recommendation generation
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not tracked by git)
└── README.md               # Project documentation
```

## How It Works

1. **Upload**: User uploads a blood test PDF report through the interface
2. **Extraction**: The system extracts text content from the PDF
3. **Analysis**: The AI model processes the extracted text to identify health metrics
4. **Visualization**: Key health indicators are displayed in charts and tables
5. **Recommendations**: The system generates personalized health recommendations based on the analysis

## Demo

![MediScan Demo](https://via.placeholder.com/800x450/f8f9fa/2c3e50?text=MediScan+Demo+Screenshot)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

MediScan is intended for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

## Contact

Your Name - [@yourusername](https://twitter.com/yourusername) - email@example.com

Project Link: [https://github.com/yourusername/mediscan](https://github.com/yourusername/mediscan)

---

<p align="center">Made with ❤️ for better health insights</p>