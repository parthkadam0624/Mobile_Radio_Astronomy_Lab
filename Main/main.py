# main.py
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from .plotting import setup_figure, make_updater
from .controls import on_key
from .config import state

def main():
    print("Running 21-cm HI Spectrum Simulator (modular build)")
    print(f"Seed: {state['seed']}\n")
    print("Controls:\n  space: pause/resume\n  n/m: noise ±\n  a: toggle 2nd component\n"
          "  v: toggle x-mode\n  ↑↓: amplitude ±\n  ←→: doppler shift\n  q/esc: quit\n")

    fig, axes, lines, param_text = setup_figure()
    update = make_updater(fig, axes, lines, param_text)
    anim = FuncAnimation(fig, update, interval=40, blit=True)

    fig.canvas.mpl_connect("key_press_event", on_key)
    plt.show(block=False)

    while plt.fignum_exists(fig.number):
        plt.pause(0.01)

if __name__ == "__main__":
    main()