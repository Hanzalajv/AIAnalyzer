import streamlit as st
from collections import deque
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Airport Check-in Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title
st.title("✈️ Smart Airport Check-in Planning Agent")
st.markdown("---")

# Problem Formulation
st.header("📋 Problem Formulation")

# Initial and Goal States
initial_state = "Airport Entrance"
goal_state = "Boarded"

# Airport checkpoints graph (adjacency list with processing times)
airport_graph = {
    "Airport Entrance": [("Identity Verification", 5)],
    "Identity Verification": [("Baggage Check-in", 10), ("Security Screening", 8)],
    "Baggage Check-in": [("Security Screening", 7)],
    "Security Screening": [("Immigration", 15), ("Boarding Gate", 10)],
    "Immigration": [("Boarding Gate", 5)],
    "Boarding Gate": [("Boarded", 2)],
    "Boarded": []
}

# Possible Actions (all checkpoints)
possible_actions = [
    "Verify Identity",
    "Check-in Baggage",
    "Pass Security Screening",
    "Complete Immigration",
    "Reach Boarding Gate",
    "Board Aircraft"
]

# Display Problem Definition
col1, col2 = st.columns(2)

with col1:
    st.subheader("States Definition")
    st.write(f"**Initial State:** {initial_state}")
    st.write(f"**Goal State:** {goal_state}")
    st.write("**Possible Actions:**")
    for i, action in enumerate(possible_actions, 1):
        st.write(f"{i}. {action}")

with col2:
    st.subheader("Transition Model")
    st.write("**Checkpoint Connections (with processing times):**")
    for state, neighbors in airport_graph.items():
        if neighbors:
            for next_state, cost in neighbors:
                st.write(f"• {state} → {next_state} ({cost} min)")

# Functions for Agent
def transition_model(state, action):
    """Apply action to move to next state"""
    for next_state, cost in airport_graph.get(state, []):
        if next_state == action:
            return next_state, cost
    return state, 0

def goal_test(state):
    """Check if goal reached"""
    return state == goal_state

def path_cost(path):
    """Calculate total processing time"""
    total = 0
    for i in range(len(path) - 1):
        for next_state, cost in airport_graph.get(path[i], []):
            if next_state == path[i + 1]:
                total += cost
                break
    return total

def generate_state_space(start_state):
    """Generate all reachable states using BFS"""
    visited = set()
    queue = deque([start_state])
    reachable = []
    
    while queue:
        current = queue.popleft()
        if current not in visited:
            visited.add(current)
            reachable.append(current)
            for next_state, _ in airport_graph.get(current, []):
                if next_state not in visited:
                    queue.append(next_state)
    return reachable

def find_plan(start, goal):
    """Find sequence of checkpoints from start to goal using BFS"""
    visited = set()
    queue = deque([[start]])
    
    while queue:
        path = queue.popleft()
        current = path[-1]
        
        if current == goal:
            return path
        
        if current not in visited:
            visited.add(current)
            for next_state, _ in airport_graph.get(current, []):
                if next_state not in visited:
                    new_path = list(path)
                    new_path.append(next_state)
                    queue.append(new_path)
    return None

# Generate State Space
st.markdown("---")
st.header("🗺️ State Space Generation")

reachable_states = generate_state_space(initial_state)

# Display as graph-like structure
st.write(f"**Total Reachable States:** {len(reachable_states)}")
st.write("**Reachable States from Initial State:**")

# Create columns for state display
cols = st.columns(3)
for i, state in enumerate(reachable_states):
    with cols[i % 3]:
        if state == initial_state:
            st.info(f"🔵 **{state}** (Start)")
        elif state == goal_state:
            st.success(f"✅ **{state}** (Goal)")
        else:
            st.write(f"⚪ {state}")

# Generate Plan
st.markdown("---")
st.header("🛤️ Solution Execution")

if st.button("Generate Check-in Plan", type="primary"):
    plan = find_plan(initial_state, goal_state)
    
    if plan:
        st.success("✅ Optimal check-in plan generated successfully!")
        
        # Display plan sequence
        st.subheader("Planned Checkpoint Sequence")
        
        # Create a dataframe for the plan
        plan_data = []
        for i in range(len(plan) - 1):
            current = plan[i]
            next_state = plan[i + 1]
            cost = 0
            for ns, c in airport_graph.get(current, []):
                if ns == next_state:
                    cost = c
                    break
            
            plan_data.append({
                "Step": i + 1,
                "From": current,
                "To": next_state,
                "Processing Time (min)": cost,
                "Status": "Pending"
            })
        
        plan_df = pd.DataFrame(plan_data)
        st.dataframe(plan_df, width='stretch')
        
        # Visualize the path
        st.subheader("Visual Path")
        path_str = " → ".join(plan)
        st.markdown(f"**{path_str}**")
        
        # Calculate and display metrics
        total_time = path_cost(plan)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Checkpoints", len(plan))
        with col2:
            st.metric("Total Processing Time", f"{total_time} min")
        with col3:
            st.metric("Reachable States", len(reachable_states))
        with col4:
            efficiency = (len(plan) / len(reachable_states)) * 100
            st.metric("Path Efficiency", f"{efficiency:.1f}%")
        
        # Display cycle avoidance
        st.subheader("Cycle Avoidance")
        st.write(f"✅ Visited {len(plan)} states without revisiting any checkpoint")
        st.write(f"✅ Avoided {len(reachable_states) - len(plan)} unnecessary states")
        
    else:
        st.error("❌ No valid plan found!")

# Sidebar Information
with st.sidebar:
    st.header("ℹ️ Agent Information")
    st.write("**Agent Type:** Problem-Solving Agent")
    st.write("**Environment:** Static (Airport)")
    st.write("**Search Strategy:** Breadth-First Search")
    
    st.markdown("---")
    st.subheader("Performance Measures")
    st.write("• Minimize total processing time")
    st.write("• Avoid unnecessary checkpoints")
    st.write("• No revisiting completed checkpoints")
    
    st.markdown("---")
    st.subheader("Constraints")
    st.write("• Minimum 6 checkpoints ✓")
    st.write("• Static environment ✓")
    st.write("• No revisiting states ✓")
    st.write("• Cycle avoidance ✓")

# Footer
st.markdown("---")
st.markdown("Built with  | Airport Check-in Problem-Solving Agent")