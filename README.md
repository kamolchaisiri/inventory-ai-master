# 💎 Inventory AI Master: Dead Stock Detective & Demand Forecasting

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-FF4B4B)
![Scikit-Learn](https://img.shields.io/badge/ML-KMeans-orange)

**An intelligent dashboard that helps retailers optimize inventory, reduce dead stock, and prevent stockouts using Machine Learning.**

---

## 🚀 Overview

Managing inventory is a balancing act. Retailers face two major problems:
1.  **Dead Stock:** Capital tied up in unsold items.
2.  **Stockouts:** Lost revenue due to running out of popular items.

**Inventory AI Master** solves this by using:
* **Unsupervised Learning (K-Means Clustering)** to automatically segment products and identify "Dead Stock".
* **Time-Series Logic** to calculate "Stock Runway" and predict when items will run out based on lead times.

## ✨ Key Features

### 1. 💀 Dead Stock Manager (Cash Flow Optimization)
* **AI-Powered Detection:** Uses K-Means clustering to group items based on stock levels and days unsold.
* **Visual Analysis:** Interactive Bubble Chart (Scatter Plot) to spot expensive, aging inventory instantly.
* **Actionable Insights:** Generates a list of candidates for clearance campaigns.

### 2. 📉 Demand Forecasting (Revenue Protection)
* **Stock Runway Calculation:** Predicts how many days of stock remain based on average daily sales.
* **Smart Alerts:** Compares remaining stock days vs. Supplier Lead Time.
    * 🚨 **Critical Low:** Restock immediately to avoid stockout.
    * ⚠️ **Warning:** Plan restock soon.
* **Budget Estimation:** Estimates the capital required to replenish safe stock levels.

## 🛠 Tech Stack

* **Frontend:** Streamlit (Python)
* **Data Manipulation:** Pandas, NumPy
* **Machine Learning:** Scikit-learn (K-Means)
* **Visualization:** Plotly Express

## 💻 How to Run Locally

1.  **Clone the repository**
    ```bash
    git clone https://github.com/kamolchaisiri/inventory-ai-master.git
    cd inventory-ai-master
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Generate Mock Data**
    Run the script to create a realistic dataset (`inventory_data.csv`) with advanced metrics.
    ```bash
    python generate_csv.py
    ```

4.  **Start the Dashboard**
    ```bash
    streamlit run app.py
    ```

## 📸 Screenshots

<img width="1899" height="1687" alt="image" src="https://github.com/user-attachments/assets/5877157c-4d22-451f-a681-d162c9284a08" />


## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
