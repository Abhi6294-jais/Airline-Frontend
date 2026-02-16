# ✈️ Flight Price Prediction App

A powerful machine learning application that predicts flight ticket prices in India based on various parameters like airline, source, destination, departure time, and more. This project features a robust **FastAPI** backend that is **Dockerized and deployed on AWS EC2**, coupled with an interactive **Streamlit** frontend.

---

## 🌟 Key Features

- **Cloud-Native Backend:** The API is containerized using **Docker** and deployed on **AWS EC2** for scalability and reliability.
- **Accurate Predictions:** Uses an optimized **XGBoost Regressor** trained on historical flight data.
- **Interactive UI:** Built with **Streamlit** for a seamless user experience.
- **Real-Time API:** Powered by **FastAPI** for fast inference.
- **Confidence Intervals:** Provides a price range (lower and upper bound) along with the predicted price.
- **Visualizations:** Displays feature importance and confidence scores using **Plotly**.
- **Comprehensive Inputs:** Supports selection of Airline, Source, Destination, Route, Total Stops, and more.

---

## 🛠️ Technology Stack

- **Frontend:** [Streamlit](https://streamlit.io/), [Plotly](https://plotly.com/)
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/)
- **Deployment:** [Docker](https://www.docker.com/), [AWS EC2](https://aws.amazon.com/ec2/)
- **Machine Learning:** [XGBoost](https://xgboost.readthedocs.io/), [Scikit-Learn](https://scikit-learn.org/), [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Data Format:** Excel (`.xlsx`), Pickle (`.pkl`) for model serialization.

---

## 📂 Project Structure

```
Airline_final_proj/
├── app.py                                              # FastAPI Backend application
├── frontend.py                                         # Streamlit Frontend application (Connected to AWS Backend)
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

The application consists of a **Frontend** running locally and a **Backend** deployed on AWS.

### Start the Frontend App (Streamlit)
Since the backend is already actively running on AWS, you only need to start the frontend interface:

1.  Open a terminal in the project directory.
2.  Run the following command:

    ```bash
    python -m streamlit run frontend.py
    ```

3.  The interactive app will open in your browser at: `http://localhost:8501`. It will automatically connect to the live backend API.

**(Optional) Running Backend Locally:**
If you wish to develop or run the backend locally instead of using the AWS deployment:
1.  Open `frontend.py` and update the `API_URL` to `http://localhost:8000`.
2.  Start the backend server: `python -m uvicorn app:app --reload`

---

## 🧠 Model Information

The core of this project is a machine learning pipeline trained using `Flight_data.ipynb`. 
- **Algorithm:** XGBoost Regressor
- **Metrics:** Selected based on RMSE/R2 Score.
- **Input Features:** various flight parameters (Airline, Date, Source, Destination, etc.).

---

## 📝 API Endpoints

The backend API is deployed on AWS at: `http://100.53.9.152:8000`

It exposes the following endpoints:

- **`GET /`**: API Health check and status.
- **`GET /health`**: Returns model loading status.
- **`POST /predict`**: Takes flight details as JSON input and returns the predicted price.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.
