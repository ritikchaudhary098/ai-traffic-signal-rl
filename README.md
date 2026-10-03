# 🚦 AI Traffic Signal Optimization using Reinforcement Learning

An AI-based traffic signal optimization project that uses **Reinforcement Learning (PPO)** to dynamically control traffic signals at a simulated 4-way intersection.

The project compares a trained **PPO Reinforcement Learning controller** with two traditional approaches:

* **Fixed-Time Controller**
* **Adaptive Rule-Based Controller**
* **RL-PPO Controller**

The traffic environment is simulated using **Pygame**, while **Streamlit** is used to visualize and analyze the experimental results.

---

## 🎯 Project Objective

Traditional traffic signals generally operate using fixed timing or manually designed rules.

This project explores whether a **Reinforcement Learning agent** can dynamically decide when to switch traffic signal phases based on the current traffic conditions.

The RL agent observes:

* Number of vehicles from each direction
* Number of waiting vehicles
* Current traffic signal phase
* Signal state
* Signal timer
* Whether switching is currently allowed

Based on these observations, the PPO agent chooses between:

```text
0 → KEEP CURRENT PHASE
1 → REQUEST SIGNAL SWITCH
```

The objective is to reduce:

* 🚗 Vehicle waiting time
* 🚧 Queue length
* 🚦 Traffic congestion

while maintaining good traffic flow.

---

## 🧠 Reinforcement Learning Algorithm

The project uses **Proximal Policy Optimization (PPO)**, a policy-gradient reinforcement learning algorithm.

PPO is implemented using:

* Python
* Gymnasium
* Stable-Baselines3
* PyTorch

### RL Workflow

```text
Traffic Environment
        ↓
Observe Traffic State
        ↓
PPO Agent
        ↓
Choose Action
        ↓
KEEP / SWITCH
        ↓
Traffic Signal Changes
        ↓
Vehicles Move
        ↓
Calculate Reward
        ↓
Agent Learns
```

---

## 🚦 Traffic Simulation

The traffic environment represents a four-way intersection:

```text
                    NORTH
                      ↓
                      🚗
                      │
                      │
        WEST ← 🚗 ────┼──── 🚗 → EAST
                      │
                      │
                      🚗
                      ↑
                    SOUTH
```

Vehicles are randomly generated from four directions.

The simulation includes:

* Four traffic directions
* Traffic lights
* Vehicle movement
* Vehicle queues
* Waiting time
* Signal phases
* Green, yellow and all-red states
* Traffic generation
* Performance metrics

The visual simulation is built using **Pygame**.

---

## 🔬 Controllers

The project evaluates three traffic signal control strategies.

### 1. Fixed-Time Controller

The signal changes according to a predefined timing schedule.

```text
NS Green
   ↓
Yellow
   ↓
EW Green
   ↓
Yellow
   ↓
Repeat
```

It does not consider the current traffic conditions.

---

### 2. Adaptive Controller

The adaptive controller uses traffic queue lengths.

For example:

```text
If EW queue > NS queue + threshold
        ↓
Switch from NS → EW
```

It reacts to the current traffic situation using predefined rules.

---

### 3. RL-PPO Controller

The PPO agent learns a traffic signal policy through reinforcement learning.

The agent observes the environment and chooses whether to:

```text
KEEP PHASE
     or
REQUEST SWITCH
```

The reward function considers:

* Queue size
* Queue improvement
* Vehicles passing through the intersection
* Cost of switching
* Invalid switch attempts

---

## 📊 Performance Metrics

The controllers are compared using:

| Metric               | Description                       |
| -------------------- | --------------------------------- |
| Average Waiting Time | Average vehicle waiting time      |
| Average Queue        | Average number of queued vehicles |
| Maximum Queue        | Largest queue observed            |
| Vehicles Passed      | Vehicles that successfully passed |
| Traffic Volume       | Number of vehicles generated      |

The experiment uses **10 different random traffic scenarios (seeds)** to evaluate controller behavior under different traffic patterns.

---

## 📈 Experimental Results

Results from the 10-scenario experiment:

| Controller | Avg Waiting Time (sec) | Avg Queue | Max Queue | Vehicles Passed |
| ---------- | ---------------------: | --------: | --------: | --------------: |
| Fixed-Time |                   9.92 |      8.50 |      25.8 |           847.5 |
| Adaptive   |                   4.66 |      4.00 |      12.3 |           846.3 |
| RL-PPO     |                   4.69 |      4.02 |      12.1 |           846.6 |

### Observations

The experiment shows that:

* Fixed-Time control produces substantially higher waiting time and queue lengths in this simulated traffic environment.
* Adaptive and RL-PPO controllers produce similar average waiting times and queue lengths.
* RL-PPO achieves performance comparable to the adaptive controller while learning its switching policy from the environment.
* Results are based on a simulated environment and should not be interpreted as real-world traffic performance.

---

## 🖥️ Project Visualization

### Pygame Simulation

The Pygame application provides a visual representation of the traffic intersection.

It displays:

* 🚗 Moving vehicles
* 🚦 Traffic signals
* 🧠 PPO actions
* 📊 Traffic counts
* 📈 Queue statistics
* ⏱️ Waiting time

Run the visual simulation using:

```bash
uv run python main.py
```

---

## 📊 Streamlit Dashboard

The project also includes an interactive dashboard for analyzing experimental results.

The dashboard displays:

* Average waiting time
* Average queue length
* Maximum queue
* Vehicles passed
* Traffic volume
* PPO reward
* Detailed experiment results

Run the dashboard:

```bash
uv run streamlit run dashboard/app.py
```

---

## 📁 Project Structure

```text
ai-traffic-signal-rl/
│
├── simulation/
│   ├── __init__.py
│   ├── vehicle.py
│   ├── traffic_light.py
│   ├── intersection.py
│   └── runner.py
│
├── environment/
│   ├── __init__.py
│   └── traffic_env.py
│
├── agent/
│   ├── __init__.py
│   ├── train.py
│   └── evaluate.py
│
├── controllers/
│   ├── __init__.py
│   ├── fixed_time.py
│   └── adaptive.py
│
├── models/
│   └── traffic_ppo.zip
│
├── analysis/
│   ├── experiment.py
│   ├── analyze_results.py
│   └── results.csv
│
├── dashboard/
│   └── app.py
│
├── main.py
├── README.md
├── requirements.txt
├── pyproject.toml
└── uv.lock
```

---

## ⚙️ Technologies Used

### Programming

* Python

### Reinforcement Learning

* PPO
* Stable-Baselines3
* Gymnasium
* PyTorch

### Simulation

* Pygame

### Data Analysis

* NumPy
* Pandas
* Matplotlib

### Dashboard

* Streamlit

### Development

* uv
* Git
* GitHub

---

## 🚀 Installation

Clone the repository:

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
```

Move into the project directory:

```bash
cd ai-traffic-signal-rl
```

Create the virtual environment:

```bash
uv venv
```

Activate it:

### macOS / Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
uv sync
```

Or using `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

### 1. Train the PPO Agent

```bash
uv run python -m agent.train
```

The trained model will be saved in:

```text
models/traffic_ppo.zip
```

---

### 2. Evaluate the PPO Agent

```bash
uv run python -m agent.evaluate
```

---

### 3. Run the Visual Simulation

```bash
uv run python main.py
```

---

### 4. Run the Experiment

The experiment compares all three controllers across multiple traffic scenarios.

```bash
uv run python -m analysis.experiment
```

Results are saved to:

```text
analysis/results.csv
```

---

### 5. Analyze Results

```bash
uv run python -m analysis.analyze_results
```

---

### 6. Launch Dashboard

```bash
uv run streamlit run dashboard/app.py
```

---

## 🔄 Complete Project Pipeline

```text
                TRAFFIC SIMULATION
                       │
                       ↓
              Generate Vehicles
                       │
                       ↓
               Observe Traffic
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
      Fixed-Time    Adaptive      RL-PPO
          │            │            │
          └────────────┼────────────┘
                       ↓
                Collect Metrics
                       ↓
                 results.csv
                       ↓
              Streamlit Dashboard
```

---

## 🎓 Key Learning Outcomes

This project demonstrates practical experience with:

* Reinforcement Learning
* PPO
* Custom Gymnasium environments
* Reward function design
* State and action space design
* Simulation development
* Traffic signal optimization
* Experimental evaluation
* Data analysis
* Visualization
* Streamlit dashboards
* Python project structure

---

## 🔮 Future Improvements

Possible improvements include:

* Multiple lanes per direction
* Turning vehicles
* Pedestrian crossings
* Emergency vehicle priority
* More realistic traffic generation
* Larger intersections
* Deep Q-Learning comparison
* A2C/SAC algorithm comparison
* Real-world traffic datasets
* SUMO integration
* Real-time RL monitoring
* Cloud deployment of the dashboard

---

## 👨‍💻 Author

**Ritik Chaudhary**

B.Tech Computer Science Engineering
Artificial Intelligence & Machine Learning

GitHub: **[https://github.com/ritikchaudhary098]**

LinkedIn: **[https://www.linkedin.com/in/ritik-chaudhary-6712b0289/?isSelfProfile=true]**
