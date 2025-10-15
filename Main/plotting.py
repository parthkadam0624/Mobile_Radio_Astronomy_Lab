# plotting.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
from .config import state, freqs, x_khz, REST_FREQ_HZ
from .spectrum import make_spectrum, smooth_spectrum, freq_to_v_kms

def setup_figure():
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=False)
    ax_spec, ax_filt, ax_fft = axes
    line_spec, = ax_spec.plot(x_khz, np.zeros_like(x_khz), lw=1.2, label="Raw Spectrum")
    line_filt, = ax_filt.plot(x_khz, np.zeros_like(x_khz), lw=1.2, color="tab:orange", label="Smoothed Spectrum")
    line_fft, = ax_fft.plot(x_khz, np.zeros_like(x_khz), lw=1.2, color="tab:green", label="FFT Power")

    for ax in axes:
        ax.grid(True, linestyle=':', linewidth=0.5)
    ax_spec.set_title(f"Simulated 21-cm HI spectrum — seed={state['seed']}")
    ax_spec.set_ylabel("Intensity (a.u.)")
    ax_filt.set_ylabel("Smoothed (a.u.)")
    ax_fft.set_ylabel("FFT Mag")
    ax_fft.set_xlabel("Frequency offset (kHz)")

    param_text = ax_spec.text(0.01, 0.98, "", transform=ax_spec.transAxes,
                              va="top", ha="left", fontsize=9,
                              bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.3))

    # Inset for velocity
    ax_vel = ax_spec.inset_axes([0.65, 0.7, 0.3, 0.25])
    vel_line, = ax_vel.plot([], [], 'r-')
    ax_vel.grid(True, linestyle=':', linewidth=0.4)
    ax_vel.set_xlim(-5, 5)
    ax_vel.set_ylim(-10, 10)
    ax_vel.set_title("Velocity (km/s)", fontsize=8)

    return fig, (ax_spec, ax_filt, ax_fft, ax_vel), (line_spec, line_filt, line_fft, vel_line), param_text

def update_param_text(param_text):
    info = (f"mode: {state['x_mode']}\n"
            f"noise σ: {state['noise_std']:.3f}\n"
            f"main amp: {state['main_amp']:.3f}\n"
            f"main σ(Hz): {state['main_sigma_hz']:.0f}\n"
            f"2nd comp: {'ON' if state['add_second'] else 'off'}")
    param_text.set_text(info)

def make_updater(fig, axes, lines, param_text):
    ax_spec, ax_filt, ax_fft, ax_vel = axes
    line_spec, line_filt, line_fft, vel_line = lines

    def update(frame):
        if state["paused"]:
            return (line_spec, line_filt, line_fft, vel_line)

        spec, jitter = make_spectrum()
        filtered = smooth_spectrum(spec)
        fft_vals = np.abs(np.fft.fftshift(np.fft.fft(spec - np.mean(spec))))
        fft_vals /= np.max(fft_vals)
        fft_x = (freqs - REST_FREQ_HZ) / 1e3

        # velocity
        v = freq_to_v_kms(state["main_center_hz"] + jitter)
        vel_line.set_data(np.linspace(-5, 5, 50), np.full(50, v))
        ax_vel.set_ylim(v - 10, v + 10)
        ax_vel.set_title(f"Velocity: {v:.3f} km/s", fontsize=8)

        # plot updates
        line_spec.set_data(fft_x, spec)
        line_filt.set_data(fft_x, filtered)
        line_fft.set_data(fft_x, fft_vals)

        for ax, y in zip((ax_spec, ax_filt, ax_fft), (spec, filtered, fft_vals)):
            ymin, ymax = ax.get_ylim()
            pad = 3 * state["noise_std"]
            target_ymin = max(0.0, np.min(y) - pad)
            target_ymax = np.max(y) + pad
            alpha = 0.15
            ax.set_ylim((1 - alpha)*ymin + alpha*target_ymin,
                        (1 - alpha)*ymax + alpha*target_ymax)

        ax_spec.set_title(f"Simulated 21-cm HI spectrum — seed={state['seed']} — {datetime.now().strftime('%H:%M:%S')}")
        update_param_text(param_text)
        return (line_spec, line_filt, line_fft, vel_line, param_text)

    return update