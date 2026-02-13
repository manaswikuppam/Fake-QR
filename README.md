# 🛡️ QR Shield AI

QR Shield AI is a hybrid security system designed to detect malicious QR codes and phishing URLs using Machine Learning. It provides both a web interface for manual checking and a backend API for integration with mobile apps or other services.

## 🚀 Features

*   **QR Code Scanning**: Upload QR code images (PNG/JPG) to decode and analyze links.
*   **Phishing Detection**: Uses a trained Machine Learning model to identify malicious URLs based on feature extraction.
*   **Manual URL Check**: Directly input URLs to check their safety status.
*   **Hybrid Security**: Combines a whitelist of trusted domains with AI-based fraud detection.
*   **Rest API**: A FastAPI-based backend to serve predictions to other client applications.

## 🛠️ Technology Stack

*   **Language**: Python 3.x
*   **Web Interface**: Streamlit
*   **Backend API**: FastAPI
*   **Server**: Uvicorn
*   **Image Processing**: OpenCV, Pillow (PIL)
*   **ML Model**: Scikit-learn, Joblib, NumPy

## 📂 Project Structure

```
QR_Project_Full/
├── api.py               # FastAPI backend for external access
├── web_app.py           # Streamlit web application
├── qr_fraud_model.pkl   # Trained Machine Learning model
├── test_api.py          # Script to test the API endpoints
└── README.md            # Project documentation
```

## ⚙️ Installation

1.  **Clone the repository** (or ensure you have the project files locally):
    ```bash
    git clone <repository-url>
    cd QR_Project_Full
    ```

2.  **Install Dependencies**:
    Create a virtual environment (recommended) and install the required Python packages.

    ```bash
    pip install streamlit fastapi uvicorn opencv-python pillow joblib numpy scikit-learn
    ```

## 🖥️ Usage

### 1. Running the Web App (Streamlit)
To launch the interactive web interface:

```bash
streamlit run web_app.py
```
*   This will open the app in your browser (usually at `http://localhost:8501`).
*   **Tab 1 (Upload QR)**: Upload an image file containing a QR code to check it.
*   **Tab 2 (Paste URL)**: Manually paste a URL to see if it's safe.

### 2. Running the API (FastAPI)
To start the backend server:

```bash
python api.py
```
*   The server will start at `http://0.0.0.0:8000`.
*   **API Documentation**: Visit `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

### API Endpoints

*   **GET /**: Health check. Returns a welcome message.
*   **POST /scan**: Analyze a specific URL.
    *   **Body**: `{"url": "https://example.com"}`
    *   **Response**:
        ```json
        {
            "url": "https://example.com",
            "status": "SAFE",
            "confidence": 99.8,
            "color": "green"
        }
        ```

## 🧠 How It Works

1.  **Decoding**: The system extracts the URL from the QR code image.
2.  **Whitelisting**: It first checks if the domain is in a trusted list (e.g., google.com, amazon.com).
3.  **Feature Extraction**: If not whitelisted, it extracts numerical features from the URL (length, special characters, suspicious TLDs, etc.).
4.  **Prediction**: The pre-trained ML model (`qr_fraud_model.pkl`) calculates the probability of the URL being malicious.
