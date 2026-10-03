import random

import numpy as np
from stable_baselines3 import PPO

from simulation.intersection import Intersection
from simulation.traffic_light import TrafficLight

from controllers.fixed_time import FixedTimeController
from controllers.adaptive import AdaptiveController


# ==========================================
# SETTINGS
# ==========================================

TOTAL_FRAMES = 60000

SEEDS = [
    42,
    43,
    44,
    45,
    46,
    47,
    48,
    49,
    50,
    51
]


# ==========================================
# RUN FIXED-TIME
# ==========================================

def run_fixed(seed):

    random.seed(seed)
    np.random.seed(seed)

    intersection = Intersection(
        width=1000,
        height=700
    )

    traffic_light = TrafficLight()

    intersection.traffic_light = traffic_light

    controller = FixedTimeController(
        traffic_light
    )

    for _ in range(TOTAL_FRAMES):

        controller.update()

        traffic_light.update()

        intersection.update()

    return intersection.get_metrics()


# ==========================================
# RUN ADAPTIVE
# ==========================================

def run_adaptive(seed):

    random.seed(seed)
    np.random.seed(seed)

    intersection = Intersection(
        width=1000,
        height=700
    )

    traffic_light = TrafficLight()

    intersection.traffic_light = traffic_light

    controller = AdaptiveController(
        traffic_light,
        intersection
    )

    for _ in range(TOTAL_FRAMES):

        controller.update()

        traffic_light.update()

        intersection.update()

    return intersection.get_metrics()


# ==========================================
# RUN RL
# ==========================================

def run_rl(model, seed):

    env = __import__(
        "environment.traffic_env",
        fromlist=["TrafficEnv"]
    ).TrafficEnv()

    observation, _ = env.reset(seed=seed)

    total_reward = 0

    for _ in range(1000):

        action, _ = model.predict(
            observation,
            deterministic=True
        )

        observation, reward, terminated, truncated, info = (
            env.step(action)
        )

        total_reward += reward

        if terminated or truncated:
            break

    metrics = env.intersection.get_metrics()

    metrics["total_reward"] = total_reward

    return metrics


# ==========================================
# LOAD RL MODEL
# ==========================================

print()
print("Loading PPO model...")

model = PPO.load(
    "models/traffic_ppo"
)


# ==========================================
# RUN EXPERIMENT
# ==========================================

results = []


print()
print("==========================================")
print("       STARTING TRAFFIC EXPERIMENT")
print("==========================================")
print()


for seed in SEEDS:

    print(
        f"Running seed {seed}..."
    )

    # --------------------------------------
    # Fixed-Time
    # --------------------------------------

    fixed = run_fixed(seed)

    results.append({
        "seed": seed,
        "controller": "Fixed-Time",
        **fixed
    })

    # --------------------------------------
    # Adaptive
    # --------------------------------------

    adaptive = run_adaptive(seed)

    results.append({
        "seed": seed,
        "controller": "Adaptive",
        **adaptive
    })

    # --------------------------------------
    # RL
    # --------------------------------------

    rl = run_rl(
        model,
        seed
    )

    results.append({
        "seed": seed,
        "controller": "RL-PPO",
        **rl
    })


# ==========================================
# SAVE RESULTS
# ==========================================

import pandas as pd


df = pd.DataFrame(results)


df.to_csv(
    "analysis/results.csv",
    index=False
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print()
print("==========================================")
print("          EXPERIMENT COMPLETED")
print("==========================================")

print()

print(df.to_string(index=False))

print()

print(
    "Results saved to:"
)

print(
    "analysis/results.csv"
)

print()