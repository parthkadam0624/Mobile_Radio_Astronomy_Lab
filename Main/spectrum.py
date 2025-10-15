# spectrum.py
import numpy as np
from scipy.signal import savgol_filter
import time
from .config import REST_FREQ_HZ, freqs, C, rng, BASELINE, state

def gaussian(freqs_hz, center_hz, sigma_hz, amp):
    return amp * np.exp(-0.5 * ((freqs_hz - center_hz) / sigma_hz) ** 2)

def freq_to_v_kms(freqs_hz):
    return C * (freqs_hz - REST_FREQ_HZ) / REST_FREQ_HZ

def smooth_spectrum(data, window=51, poly=3):
    if window >= len(data):
        window = len(data) - (1 - len(data) % 2)
    return savgol_filter(data, window_length=window, polyorder=poly)

def make_spectrum():
    """Generate simulated noisy HI spectrum and instantaneous velocity jitter."""
    t = time.time() - state["start_time"]
    amp_mod = 1.0 + 0.12 * np.sin(2*np.pi*(0.1*t))
    center_jitter = 300.0 * np.sin(2*np.pi*(0.07*t))

    main = gaussian(freqs,
                    state["main_center_hz"] + center_jitter,
                    state["main_sigma_hz"],
                    state["main_amp"] * amp_mod)
    spec = BASELINE + main

    if state["add_second"]:
        s_jitter = 200.0 * np.cos(2*np.pi*(0.05*t + 0.3))
        second = gaussian(freqs,
                          state["second_center_hz"] + s_jitter,
                          state["second_sigma_hz"],
                          state["second_amp"])
        spec += second

    noise = rng.normal(scale=state["noise_std"], size=len(freqs))
    return spec + noise, center_jitter