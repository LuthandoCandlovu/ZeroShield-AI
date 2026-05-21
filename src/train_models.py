import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.callbacks import EarlyStopping
import joblib
import os

os.makedirs('models', exist_ok=True)

# Load data
df = pd.read_csv('data/network_traffic.csv')
X = df.drop('label', axis=1)
y = df['label']

# Load only normal data for training
X_normal = pd.read_csv('data/normal_only.csv').drop('label', axis=1)

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_normal)
X_full_scaled = scaler.transform(X)

# ---------- Isolation Forest ----------
iso_forest = IsolationForest(contamination=0.05, random_state=42)
iso_forest.fit(X_scaled)
joblib.dump(iso_forest, 'models/iso_forest.pkl')

# ---------- Autoencoder ----------
input_dim = X_scaled.shape[1]
input_layer = Input(shape=(input_dim,))
encoded = Dense(8, activation='relu')(input_layer)
encoded = Dense(4, activation='relu')(encoded)
decoded = Dense(8, activation='relu')(encoded)
decoded = Dense(input_dim, activation='linear')(decoded)

autoencoder = Model(input_layer, decoded)
autoencoder.compile(optimizer='adam', loss='mse')

early_stop = EarlyStopping(monitor='loss', patience=5)
autoencoder.fit(X_scaled, X_scaled, epochs=50, batch_size=32, callbacks=[early_stop], verbose=1)
autoencoder.save('models/autoencoder.h5')

# Compute reconstruction error threshold (95th percentile of normal data)
reconstructed = autoencoder.predict(X_scaled, verbose=0)
mse_train = np.mean((X_scaled - reconstructed)**2, axis=1)
threshold = np.percentile(mse_train, 95)
with open('models/ae_threshold.txt', 'w') as f:
    f.write(str(threshold))

# Save scaler
joblib.dump(scaler, 'models/scaler.pkl')

print(f"✅ Models trained and saved. Autoencoder threshold = {threshold:.4f}")
