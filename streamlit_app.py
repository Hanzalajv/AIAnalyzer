# streamlit_app.py
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from searchAlgos import hospital_graph, locations, gbfs, a_star, heuristic

st.set_page_config(page_title="Informed Search Visualizer", layout="wide")

st.title("🏥 Hospital Emergency Supply Robot")
st.markdown("""
Compare **Greedy Best-First Search (GBFS)** and **A\\* Search** on a hospital corridor network.
The robot delivers emergency supplies from **Pharmacy** to **Emergency_Ward**.
""")

st.sidebar.header("Configuration")
nodes = list(hospital_graph.keys())

start = st.sidebar.selectbox("Select Initial Node", nodes,
                             index=nodes.index("Pharmacy"))
goal = st.sidebar.selectbox("Select Goal Node", nodes,
                            index=nodes.index("Emergency_Ward"))
algorithm = st.sidebar.selectbox("Select Search Algorithm", ["GBFS", "A*"])

st.sidebar.subheader("Heuristic Values h(n)")
for n in nodes:
    st.sidebar.write(f"h({n}) = {heuristic(n, goal):.2f}")

if st.button("🚀 Run Search", type="primary"):
    if algorithm == "GBFS":
        path, cost, expanded = gbfs(start, goal)
    else:
        path, cost, expanded = a_star(start, goal)

    if path is None:
        st.error(f"❌ No path found from {start} to {goal}.")
    else:
        st.subheader("Search Result")
        c1, c2, c3 = st.columns(3)
        c1.metric("Algorithm", algorithm)
        c2.metric("Total Path Cost", f"{cost:.2f}")
        c3.metric("Nodes Expanded", len(expanded))

        st.write(f"**Solution Path:** {' → '.join(path)}")
        st.write(f"**Expansion Order:** {' → '.join(expanded)}")

        G = nx.DiGraph()
        for node, neighbors in hospital_graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)

        pos = locations
        fig, ax = plt.subplots(figsize=(12, 7))

        nx.draw_networkx_edges(G, pos, ax=ax, edge_color="lightgray",
                               arrows=True, arrowsize=15, width=2,
                               connectionstyle="arc3,rad=0.05")
        edge_labels = {k: f"{v:.1f}" for k, v in
                       nx.get_edge_attributes(G, "weight").items()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=9)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color="lightblue",
                               node_size=1800, edgecolors="black")

        if path and len(path) > 1:
            pe = list(zip(path[:-1], path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=pe, ax=ax,
                                   edge_color="red", width=4,
                                   arrows=True, arrowsize=20,
                                   connectionstyle="arc3,rad=0.05")
            nx.draw_networkx_nodes(G, pos, nodelist=path, ax=ax,
                                   node_color="salmon", node_size=1800,
                                   edgecolors="black")

        nx.draw_networkx_nodes(G, pos, nodelist=[start], ax=ax,
                               node_color="green", node_size=2000, edgecolors="black")
        nx.draw_networkx_nodes(G, pos, nodelist=[goal], ax=ax,
                               node_color="gold", node_size=2000, edgecolors="black")
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=9, font_weight="bold")

        ax.set_title(f"{algorithm} Solution Path: {' → '.join(path)}", fontsize=12)
        ax.axis("off")
        plt.tight_layout()
        st.pyplot(fig)

        st.subheader("Path Cost Breakdown")
        breakdown = []
        for i in range(len(path) - 1):
            breakdown.append({
                "From": path[i],
                "To": path[i + 1],
                "Edge Cost": hospital_graph[path[i]][path[i + 1]]
            })
        st.table(breakdown)