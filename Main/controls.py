# controls.py
import matplotlib.pyplot as plt
from .config import state, REST_FREQ_HZ
from .spectrum import freq_to_v_kms

def on_key(event):
    key = event.key.lower()
    if key == " ":
        state["paused"] = not state["paused"]
        print("[paused]" if state["paused"] else "[resumed]")
    elif key == "n":
        state["noise_std"] *= 1.25
    elif key == "m":
        state["noise_std"] /= 1.25
    elif key == "a":
        state["add_second"] = not state["add_second"]
    elif key == "v":
        state["x_mode"] = "kms" if state["x_mode"] == "khz" else "khz"
    elif key == "up":
        state["main_amp"] *= 1.1
        print(f"↑ amplitude → {state['main_amp']:.3f}")
    elif key == "down":
        state["main_amp"] /= 1.1
        print(f"↓ amplitude → {state['main_amp']:.3f}")
    elif key == "right":
        state["main_center_hz"] += 500.0
        print(f"→ redshift +500 Hz ({freq_to_v_kms(state['main_center_hz']) - freq_to_v_kms(REST_FREQ_HZ):.4f} km/s)")
    elif key == "left":
        state["main_center_hz"] -= 500.0
        print(f"← blueshift -500 Hz ({freq_to_v_kms(state['main_center_hz']) - freq_to_v_kms(REST_FREQ_HZ):.4f} km/s)")
    elif key in ("q", "escape"):
        plt.close(event.canvas.figure)