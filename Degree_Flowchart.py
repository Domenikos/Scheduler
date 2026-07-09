""" Degree Flowchart Generator """
import graphviz


# Dictionary Format: 'COURSE_CODE': (Credit_Hours, Term_Restriction, [Prereqs], [Co-reqs])
# Term Restrictions: 'Fall', 'Spring', or 'Both|Any'


def create_course_flowchart(courses_dict):
    # Generate a flowchart of courses with prerequisites and corequisites using Graphviz
    # Initialize a directed graph
    dot = graphviz.Digraph(comment="Course Flowchart", format="svg")
    dot.attr(rankdir="LR", size="12,8")  # Left to Right layout

    # Track created corequisite clusters to avoid duplicate nodes
    coreq_clusters = set()

    # 1. Create Nodes and Term/Coreq Groupings
    for course, (credits, term, prereqs, coreqs) in courses_dict.items():
        # Node styling based on term restriction
        color = (
            "pink"
            if term == "Fall"
            else "lightgreen" if term == "Spring" else "lightgrey"
        )

        # Format Node Label
        label = f"{course}\\n({credits} Credits)\\n({term})"

        # Handle Corequisites as subgraphs (clusters) if they exist
        if coreqs:
            cluster_name = f"cluster_{'_'.join(sorted([course] + coreqs))}"
            if cluster_name not in coreq_clusters:
                coreq_clusters.add(cluster_name)
                # Create visual box grouping for corequisites
                with dot.subgraph(name=cluster_name) as c:
                    c.attr(label="Corequisites", style="filled", color="lightyellow")
                    c.node(course, label=label, style="filled", fillcolor=color)
                    for req in coreqs:
                        c.node(req, label=req, style="filled", fillcolor="lightgrey")
            else:
                # Node already placed inside cluster
                dot.node(course, label=label, style="filled", fillcolor=color)
        else:
            # Standalone node
            dot.node(course, label=label, style="filled", fillcolor=color)

    # 2. Draw Edges for Prerequisites and Corequisites
    for course, (_, _, prereqs, coreqs) in courses_dict.items():
        # Prerequisites: directed edge from prereq to course (solid line)
        for prereq in prereqs:
            dot.edge(prereq, course, style="solid")

        # Corequisites: undirected or double-directed edge (dotted line)
        for coreq in coreqs:
            dot.edge(course, coreq, style="dotted", dir="none")

    # 3. Render the Flowchart
    dot.render("course_flowchart", view=True)


# Run the function
if __name__ == "__main__":
    from EE_COURSE_DB import EE_COURSE_DB

    courses = EE_COURSE_DB  # Use the imported course database
    create_course_flowchart(courses)
