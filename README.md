# Industrial IoT Anomaly Detection Dashboard

Detects anomalies in industrial pump sensor data using unsupervised machine learning.

## Business Problem
Unexpected machine failures are costly. This system flags abnormal sensor
behaviour so maintenance teams can act before a breakdown.

## Dataset
Pump sensor dataset (Kaggle) — 220,320 readings from 52 sensors, with a
machine_status label (NORMAL / RECOVERING / BROKEN). Only 7 readings are BROKEN.
DATASET LINK : https://www.kaggle.com/datasets/nphantawee/pump-sensor-data


## Approach
- Cleaning: removed empty sensors (15, 50), filled gaps, scaled all sensors.
- Model: Isolation Forest (unsupervised, contamination 0.05) — labels never used in training.
- Flagged 11,016 readings (5%) as anomalous.

## Results
- Anomaly rate: NORMAL 2.8%, BROKEN 14.3%, RECOVERING 36.6%.
- 5 of 7 real breakdowns detected within a 6-hour window.

## Key Finding
The system reliably DETECTS abnormal conditions in real time, but does not
reliably PREDICT failures in advance — most failures occur abruptly. Real-time
detection is achievable; early failure prediction remains an open research problem.

## Live App
https://iot-anomaly-dashboard-aznr4k8ensc8fmmghuswu7.streamlit.app/

## Demo Video
[Video link — add after recording]

## How to Run
1. `pip install -r requirements.txt`
2. `streamlit run streamlit_app.py`
