import streamlit as st
import random
import time
import pandas as pd

st.set_page_config(page_title="CloudSched-X", layout="wide")

st.title("☁️ CloudSched-X: Real-Time Cloud Scheduling Simulator")

st.sidebar.header("Simulation Controls")

num_tasks = st.sidebar.slider("Number of Cloud Tasks", 5, 50, 15)
num_vms = st.sidebar.slider("Number of Virtual Machines", 1, 10, 3)
algorithm = st.sidebar.selectbox(
    "Select Scheduling Algorithm",
    ["FCFS", "Round Robin", "Priority", "EDF", "Random Load Balancing"]
)

time_quantum = st.sidebar.slider("Time Quantum (RR)", 1, 10, 3)

st.markdown("### 🔄 Live Task Generation")

tasks = []
for i in range(num_tasks):
    tasks.append({
        "Task ID": f"T{i+1}",
        "Arrival Time": random.randint(0, 10),
        "Burst Time": random.randint(1, 10),
        "Priority": random.randint(1, 5),
        "Deadline": random.randint(5, 20)
    })

df = pd.DataFrame(tasks).sort_values("Arrival Time")
st.dataframe(df, use_container_width=True)

st.markdown("### ⚙️ Scheduling Execution")

results = []
current_time = 0
vm_load = [0] * num_vms

for _, task in df.iterrows():
    start_time = max(current_time, task["Arrival Time"])
    finish_time = start_time + task["Burst Time"]

    if algorithm == "FCFS":
        pass

    elif algorithm == "Priority":
        df = df.sort_values("Priority")

    elif algorithm == "EDF":
        df = df.sort_values("Deadline")

    elif algorithm == "Random Load Balancing":
        selected_vm = random.randint(0, num_vms - 1)
        vm_load[selected_vm] += task["Burst Time"]

    elif algorithm == "Round Robin":
        finish_time = start_time + min(task["Burst Time"], time_quantum)

    waiting_time = start_time - task["Arrival Time"]
    turnaround_time = finish_time - task["Arrival Time"]

    results.append({
        "Task ID": task["Task ID"],
        "Start Time": start_time,
        "Finish Time": finish_time,
        "Waiting Time": waiting_time,
        "Turnaround Time": turnaround_time
    })

    current_time = finish_time

result_df = pd.DataFrame(results)
st.dataframe(result_df, use_container_width=True)

st.markdown("### 📊 Performance Metrics")

avg_wait = result_df["Waiting Time"].mean()
avg_turnaround = result_df["Turnaround Time"].mean()

st.metric("Average Waiting Time", round(avg_wait, 2))
st.metric("Average Turnaround Time", round(avg_turnaround, 2))

st.markdown("### 🖥 VM Load Distribution")
vm_df = pd.DataFrame({
    "VM": [f"VM{i+1}" for i in range(num_vms)],
    "Load": vm_load
})

st.bar_chart(vm_df.set_index("VM"))

st.success("Simulation Completed Successfully!")
