-----

# Full-Stack Receipt Processor

This project is a full-stack web application built to process and analyze uploaded receipts and bills. The backend, powered by **Python** and **FastAPI**, uses Optical Character Recognition (OCR) to extract key data, which is then stored in a **SQLite** database. The **Angular** frontend provides an interactive dashboard to upload files, view extracted data, and visualize spending habits through dynamic charts.

## Table of Contents

1.  🏛️ Architecture
2.  💻 Technology Stack
3.  🚀 Setup and Installation
4.  💡 Design Choices & Project Journey
5.  🚧 Limitations & Assumptions

-----

## 🏛️ Architecture

The application is built on a decoupled, client-server architecture:

  * **Frontend (Client)**: A single-page application built with Angular. It is responsible for the user interface, handling user interactions (file uploads, filtering), and making API calls to the backend to fetch or modify data.
  * **Backend (Server)**: A RESTful API built with FastAPI. It handles all business logic, including file ingestion, OCR processing, data parsing, database interactions, and the computation of statistical aggregations.
  * **Database**: A lightweight SQLite database that stores all the structured data extracted from the receipts.

This separation of concerns makes the application modular, scalable, and easier to maintain.

## 💻 Technology Stack

| Area | Technology | Reason for Choice |
| :--- | :--- | :--- |
| **Backend** | Python, FastAPI | Modern, high-performance framework with automatic data validation and API documentation. |
| **Frontend** | Angular | A robust and feature-rich framework for building scalable single-page applications. |
| **Database** | SQLite, SQLAlchemy | SQLite is a serverless, file-based database perfect for this project's scale. SQLAlchemy provides a powerful ORM for easy database interaction. |
| **OCR** | Tesseract, `pytesseract` | A powerful and widely used open-source OCR engine with a convenient Python wrapper. |
| **Charting** | Chart.js, `ng2-charts` | A popular and flexible charting library with excellent Angular integration. |

-----

## 🚀 Setup and Installation

To run this project locally, you will need **Python 3.8+**, **Node.js**, **Angular CLI**, and the **Tesseract-OCR Engine**.

### 1\. Prerequisites

First, install the Tesseract engine on your machine.

  * **macOS**: `brew install tesseract`
  * **Windows/Linux**: Follow the [official Tesseract installation guide](https://github.com/tesseract-ocr/tessdoc).

### 2\. Backend Setup

```bash
# Navigate to the backend folder
cd backend

# Create and activate a Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the required Python packages
pip install -r requirements.txt

# Start the backend server
uvicorn main:app --reload
```

The backend API will now be running at `http://127.0.0.1:8000`.

### 3\. Frontend Setup

```bash
# Open a new terminal and navigate to the frontend folder
cd frontend/receipt-ui

# Install the required npm packages
npm install

# Start the Angular development server
ng serve
```

The application will now be available at `http://localhost:4200`.

-----

## 💡 Design Choices & Project Journey

1.  **Initial Stack Selection**: The decision to use FastAPI was based on its speed, simplicity, and built-in support for Pydantic data models, which perfectly matched the requirement for formal type-checking. Angular was chosen for the frontend due to its powerful features for building dynamic and responsive user interfaces.

2.  **Core Challenge - Parsing Logic**: The most challenging part was building a robust data parser in `ocr_processor.py`. The initial approach of taking the first line as the vendor name proved to be unreliable, as it often captured entire sentences. The logic was improved by first searching for a list of known vendors and then falling back to a cleaned and truncated version of the first line, which significantly improved accuracy.

3.  **Algorithmic Implementation**:

      * **Search**: Implemented as query parameters in a single, flexible `/receipts/` endpoint rather than multiple, separate endpoints. This approach is more RESTful and efficient.
      * **Sorting**: Handled by the same `/receipts/` endpoint, allowing the client to specify the sorting field and order. The backend leverages the efficiency of Python's built-in Timsort algorithm.
      * **Aggregation**: Dedicated endpoints were created for each statistical calculation to keep the logic clean and focused.

4.  **UI/UX Journey**: The initial UI simply listed the data. It was then improved by adding a two-column layout to display statistics and charts alongside each other. The addition of interactive filters, sorting controls, and delete functionality transformed it into a fully functional dashboard. A key challenge was a chart rendering bug, which was resolved by using `@ViewChildren` to ensure all charts were updated when new data was loaded.

## 🚧 Limitations & Assumptions

  * **OCR Accuracy**: The accuracy of the data extraction is highly dependent on the quality of the uploaded image (clarity, contrast, orientation). The current parsing logic is rule-based and may not work for all receipt formats.
  * **Single Currency**: The application currently assumes all amounts are in the same currency and does not perform currency detection or conversion.
  * **No User Authentication**: The application is designed for a single user and does not have an authentication system. All data is publicly accessible on the local network.
  * **Vendor Parsing**: The vendor name parsing relies on a predefined list of known vendors for best results. For unknown vendors, it defaults to the first line of the text, which may not always be accurate.
