# config.py
import time
import numpy as np

# --- Physical constants ---
REST_FREQ_HZ = 1420.405751e6
SPAN_HZ = 400e3
CHANNELS = 2048
C = 299792.458  # km/s

# Frequency axis
freqs = np.linspace(REST_FREQ_HZ - SPAN_HZ/2,
                    REST_FREQ_HZ + SPAN_HZ/2,
                    CHANNELS)
x_khz = (freqs - REST_FREQ_HZ) / 1e3

# Random number generator
seed = int(time.time())
rng = np.random.default_rng(seed)

# Default parameters
BASELINE = 1.0
main_amp = 0.9 + 0.2 * rng.random()
main_sigma_hz = 8e3 + 3e3 * rng.random()
main_center_offset_hz = rng.normal(0, 1500.0)
add_second = False
second_amp = 0.4 * (0.6 + 0.8 * rng.random())
second_sigma_hz = 5e3 + 2e3 * rng.random()
second_center_offset_hz = -6000.0 + 2000.0 * rng.random()
noise_std = 0.08

# Runtime state
state = {
    "paused": False,
    "noise_std": noise_std,
    "add_second": add_second,
    "main_amp": main_amp,
    "main_sigma_hz": main_sigma_hz,
    "main_center_hz": REST_FREQ_HZ + main_center_offset_hz,
    "second_amp": second_amp,
    "second_sigma_hz": second_sigma_hz,
    "second_center_hz": REST_FREQ_HZ + second_center_offset_hz,
    "x_mode": "khz",
    "seed": seed,
    "start_time": time.time(),
}