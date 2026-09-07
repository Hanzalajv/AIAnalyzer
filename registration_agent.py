import streamlit as st
from collections import deque
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Course Registration Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title
st.title("🎓 University Course Registration Planning Agent")
st.markdown("---")

# Problem Formulation
st.header("📋 Problem Formulation")

# Initial and Goal States
initial_state = "Student Login"
goal_state = "Registration Completed"

# Registration workflow graph (each step has cost = 1 unit)
registration_graph = {
    "Student Login": [("Authenticate Student", 1)],
    "Authenticate Student": [("Verify Prerequisites", 1)],
    "Verify Prerequisites": [("Select Courses", 1)],
    "Select Courses": [("Verify Fee Status", 1)],
    "Verify Fee Status": [("Confirm Enrollment", 1)],
    "Confirm Enrollment": [("Registration Completed", 1)],
    "Registration Completed": []
}

# Possible Actions
possible_actions = [
    "Authenticate Student",
    "Verify Prerequisites",
    "Select Courses",
    "Verify Fee Status",
    "Confirm Enrollment"
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
    st.write("**Registration Workflow:**")
    for state, transitions in registration_graph.items():
        if transitions:
            for next_state, cost in transitions:
                st.write(f"• {state} → {next_state} (Cost: {cost})")

# Agent Functions
def transition_model(state, action):
    """Apply action to move to next state"""
    for next_state, cost in registration_graph.get(state, []):
        if next_state == action:
            return next_state, cost
    return state, 0

def goal_test(state):
    """Check if registration is complete"""
    return state == goal_state

def path_cost(path):
    """Calculate total cost (each step = 1 unit)"""
    return len(path) - 1  # Each transition costs 1 unit

def generate_state_space(start_state):
    """Generate all reachable states"""
    visited = set()
    queue = deque([start_state])
    reachable = []
    
    while queue:
        current = queue.popleft()
        if current not in visited:
            visited.add(current)
            reachable.append(current)
            for next_state, _ in registration_graph.get(current, []):
                if next_state not in visited:
                    queue.append(next_state)
    return reachable

def find_plan(start, goal):
    """Find sequence of registration steps"""
    visited = set()
    queue = deque([[start]])
    
    while queue:
        path = queue.popleft()
        current = path[-1]
        
        if current == goal:
            return path
        
        if current not in visited:
            visited.add(current)
            for next_state, _ in registration_graph.get(current, []):
                if next_state not in visited:
                    new_path = list(path)
                    new_path.append(next_state)
                    queue.append(new_path)
    return None

# Generate State Space
st.markdown("---")
st.header("🗺️ Registration State Space")

reachable_states = generate_state_space(initial_state)

st.write(f"**Total Reachable States:** {len(reachable_states)}")

# Display states as a flow
st.write("**Registration Workflow States:**")
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
st.header("📝 Registration Plan Execution")

if st.button("Generate Registration Plan", type="primary"):
    plan = find_plan(initial_state, goal_state)
    
    if plan:
        st.success("✅ Registration plan generated successfully!")
        
        # Display plan sequence
        st.subheader("Execution Sequence")
        
        # Create dataframe for plan
        plan_data = []
        for i in range(len(plan) - 1):
            plan_data.append({
                "Step": i + 1,
                "Action": f"{plan[i]} → {plan[i+1]}",
                "From State": plan[i],
                "To State": plan[i + 1],
                "Cost": 1,
                "Status": "✓"
            })
        
        plan_df = pd.DataFrame(plan_data)
        st.dataframe(plan_df, width='stretch')
        
        # Visual path
        st.subheader("Registration Path")
        path_str = " → ".join(plan)
        st.markdown(f"**{path_str}**")
        
        # Calculate metrics
        total_cost = path_cost(plan)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Steps", total_cost)
        with col2:
            st.metric("Total Path Cost", f"{total_cost} unit(s)")
        with col3:
            st.metric("Reachable States", len(reachable_states))
        with col4:
            completion = (total_cost / (len(reachable_states) - 1)) * 100
            st.metric("Completion", f"{completion:.0f}%")
        
        # Display requirements met
        st.subheader("Requirements Verification")
        requirements = {
            "Authentication": "✓ Completed",
            "Prerequisites Verified": "✓ Completed",
            "Courses Selected": "✓ Completed",
            "Fee Status Verified": "✓ Completed",
            "Enrollment Confirmed": "✓ Completed"
        }
        
        for req, status in requirements.items():
            st.write(f"• {req}: {status}")
        
        # Cycle avoidance
        st.subheader("Cycle Avoidance")
        st.write(f"✅ Visited {len(plan)} states without revisiting any step")
        st.write(f"✅ No cycles detected in registration process")
        
    else:
        st.error("❌ No valid registration plan found!")

# Sidebar Information
with st.sidebar:
    st.header("ℹ️ Agent Information")
    st.write("**Agent Type:** Problem-Solving Agent")
    st.write("**Environment:** Static (University System)")
    st.write("**Search Strategy:** Breadth-First Search")
    
    st.markdown("---")
    st.subheader("Performance Measures")
    st.write("• Minimize registration steps")
    st.write("• Ensure all academic requirements satisfied")
    st.write("• No revisiting completed steps")
    
    st.markdown("---")
    st.subheader("Path Cost")
    st.write("Each registration step has a processing cost of 1 unit")
    
    st.markdown("---")
    st.subheader("Constraints")
    st.write("• Sequential workflow ✓")
    st.write("• Static environment ✓")
    st.write("• No step revisiting ✓")
    st.write("• Mandatory steps only ✓")

# Footer
st.markdown("---")
st.markdown("Built with  | Course Registration Problem-Solving Agent")