import numpy as np
import joblib
from tensorflow.keras.models import load_model

class ZeroShieldDetector:
    def __init__(self):
        self.iso_forest = joblib.load('models/iso_forest.pkl')
        self.autoencoder = load_model('models/autoencoder.h5')
        self.scaler = joblib.load('models/scaler.pkl')
        with open('models/ae_threshold.txt', 'r') as f:
            self.ae_threshold = float(f.read())

    def predict(self, features_array):
        # features_array: shape (n_samples, n_features)
        scaled = self.scaler.transform(features_array)

        # Isolation Forest: -1 = anomaly, 1 = normal
        iso_pred = self.iso_forest.predict(scaled)
        iso_score = np.where(iso_pred == -1, 1, 0)

        # Autoencoder reconstruction error
        reconstructed = self.autoencoder.predict(scaled, verbose=0)
        mse = np.mean((scaled - reconstructed)**2, axis=1)
        ae_anomaly = (mse > self.ae_threshold).astype(int)

        # Ensemble: anomaly if either model detects
        ensemble = (iso_score + ae_anomaly) >= 1
        return ensemble.astype(int), mse, iso_score
