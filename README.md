# ✈️ Flight Price Prediction App

A powerful machine learning application that predicts flight ticket prices in India based on various parameters like airline, source, destination, departure time, and more. This project combines a robust **FastAPI** backend with an interactive **Streamlit** frontend.

---

## 🌟 Key Features

- **Accurate Predictions:** Uses an optimized **XGBoost Regressor** trained on historical flight data.
- **Interactive UI:** Built with **Streamlit** for a seamless user experience.
- **Real-Time API:** Powered by **FastAPI** for fast and scalable inference.
- **Confidence Intervals:** Provides a price range (lower and upper bound) along with the predicted price.
- **Visualizations:** Displays feature importance and confidence scores using **Plotly**.
- **Comprehensive Inputs:** Supports selection of Airline, Source, Destination, Route, Total Stops, and more.

---

## 🛠️ Technology Stack

- **Frontend:** [Streamlit](https://streamlit.io/), [Plotly](https://plotly.com/)
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/)
- **Machine Learning:** [XGBoost](https://xgboost.readthedocs.io/), [Scikit-Learn](https://scikit-learn.org/), [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Data Format:** Excel (`.xlsx`), Pickle (`.pkl`) for model serialization.

---

## 📂 Project Structure

```
Airline_final_proj/
├── app.py                                              # FastAPI Backend application
├── frontend.py                                         # Streamlit Frontend application
├── requirements.txt                                    # Python dependencies
├── best_flight_price_model_XGBoost_....pkl             # Trained XGBoost Model
├── Flight_data.ipynb                                   # Jupyter Notebook for EDA & Training
├── Data_Train.xlsx                                     # Training Dataset
├── Test_set.xlsx                                       # Test Dataset
└── model_comparison_results_....csv                    # Model performance metrics
```

---

## 🚀 Installation & Setup

1.  **Clone the Repository (or navigate to the project directory):**
    ```bash
    cd "path/to/Airline_final_proj"
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv myenv
    # Activate on Windows:
    .\myenv\Scripts\activate
    # Activate on Mac/Linux:
    source myenv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## ▶️ Usage Guide

This application requires both the **Backend** (API) and **Frontend** (UI) to be running simultaneously.

### Step 1: Start the Backend Server (FastAPI)
Open a terminal and run the following command to start the API:

```bash
python -m uvicorn app:app --reload
```
- The API will start at: `http://localhost:8000`
- API Documentation (Swagger UI): `http://localhost:8000/docs`

### Step 2: Start the Frontend App (Streamlit)
Open a **new terminal window**, activate your environment, and run:

```bash
python -m streamlit run frontend.py
```
- The interactive app will open in your browser at: `http://localhost:8501`

---

## 🧠 Model Information

The core of this project is a machine learning pipeline trained using `Flight_data.ipynb`. 
- **Algorithm:** XGBoost Regressor
- **Metrics:** Selected based on RMSE/R2 Score (details in `model_comparison_results...csv`).
- **Input Features:**
  - Airline
  - Date of Journey
  - Source & Destination
  - Route
  - Departure & Arrival Time
  - Duration
  - Total Stops
  - Additional Info

---

## 📝 API Endpoints

- **`GET /`**: API Health check and status.
- **`GET /health`**: Returns model loading status.
- **`POST /predict`**: Takes flight details as JSON input and returns the predicted price.

Example Request Body:
```json
{
  "Airline": "IndiGo",
  "Date_of_Journey": "24/03/2019",
  "Source": "Banglore",
  "Destination": "New Delhi",
  "Route": "BLR → DEL",
  "Dep_Time": "22:20",
  "Arrival_Time": "01:10 22 Mar",
  "Duration": "2h 50m",
  "Total_Stops": "non-stop",
  "Additional_Info": "No info"
}
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.
