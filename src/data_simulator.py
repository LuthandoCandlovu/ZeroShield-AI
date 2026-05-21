import numpy as np
import pandas as pd
import os

os.makedirs('data', exist_ok=True)

np.random.seed(42)
n_normal = 20000
n_attack = 2000

# Normal traffic features
normal = {
    'duration': np.random.exponential(0.05, n_normal),
    'src_bytes': np.random.normal(200, 50, n_normal),
    'dst_bytes': np.random.normal(300, 80, n_normal),
    'packet_rate': np.random.normal(50, 10, n_normal),
    'syn_flag': np.random.binomial(1, 0.3, n_normal),
    'ack_flag': np.random.binomial(1, 0.7, n_normal)
}

# Attack traffic (anomalous)
attack = {
    'duration': np.random.exponential(2, n_attack),
    'src_bytes': np.random.normal(5000, 1000, n_attack),
    'dst_bytes': np.random.normal(10, 20, n_attack),
    'packet_rate': np.random.normal(200, 50, n_attack),
    'syn_flag': np.random.binomial(1, 0.9, n_attack),
    'ack_flag': np.random.binomial(1, 0.1, n_attack)
}

df_normal = pd.DataFrame(normal)
df_normal['label'] = 0
df_attack = pd.DataFrame(attack)
df_attack['label'] = 1

df = pd.concat([df_normal, df_attack], ignore_index=True)
df.to_csv('data/network_traffic.csv', index=False)

# Also save normal-only for training
df_normal.to_csv('data/normal_only.csv', index=False)
print("✅ Synthetic dataset created (22000 samples)")
