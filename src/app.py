import streamlit as st
from rrt import RRT

st.title("Rapidly Exploring Random Forests")

with st.form("form1"):
    st.write("Select Environment Size: ")
    col1, col2 = st.beta_columns(2)
    with col1:
        env_x = st.slider(
            label="x", min_value=100, max_value=500, value=300, step=100, key="envx"
        )
    with col2:
        env_y = st.slider(
            label="y", min_value=100, max_value=500, value=300, step=100, key="envy"
        )

    st.write("Select Starting Point: ")
    col1, col2 = st.beta_columns(2)
    with col1:
        start_x = st.number_input(
            label="x", min_value=1, max_value=500, step=1, value=100, key="startx"
        )
    with col2:
        start_y = st.number_input(
            label="y", min_value=1, max_value=500, step=1, value=100, key="starty"
        )

    st.write("Select Ending Point: ")
    col1, col2 = st.beta_columns(2)
    with col1:
        end_x = st.number_input(
            label="x", min_value=1, max_value=500, step=1, value=250, key="endx"
        )
    with col2:
        end_y = st.number_input(
            label="y", min_value=1, max_value=500, step=1, value=200, key="endy"
        )

    st.write("Select Goal Radius")
    goal_radius = st.number_input(
        label="radius",
        min_value=0.5,
        max_value=500.0,
        value=5.0,
        step=0.5,
        key="goalrad",
    )

    st.write("Select Step Size")
    step_size = st.number_input(
        label="step",
        min_value=1,
        max_value=500,
        value=10,
        step=1,
        key="stepsize",
    )

    st.write("Select Maximum Iterations")
    max_iter = st.number_input(
        label="iterations",
        min_value=1000,
        max_value=500_000,
        value=10_000,
        step=500,
        key="goalrad",
    )

    st.write("Write down obstacles")
    obstacles = st.text_area(
        label="obstacles",
        value="""\
[
    # Follows the format - [x, y, radius]
    [150, 150, 4],
    [180, 180, 2],
    [200, 200, 10],
    [10, 100, 5],
]
        """,
        height=300,
        help="Enter a Python 2D list where each element is an array of the following format: [x, y, radius]",
        key="obstacles",
    )

    submit = st.form_submit_button("Run")

    # Validate Input
    temp = eval(obstacles.strip())
    if not isinstance(temp, list) or not isinstance(temp[0], list):
        raise ValueError(
            "Invalid Entries. Please ensure you enter a valid 2D Python List"
        )

    if submit:
        rrt = RRT(
            env_size=(env_x, env_y),
            start_pt=(start_x, start_y),
            end_pt=(end_x, end_y),
            goal_radius=goal_radius,
            step_size=step_size,
            max_iter=max_iter,
            obstacles=eval(obstacles.strip()),
        )
        with st.spinner("Running..."):
            msg, fig, iterations = rrt.run()

        st.write(f"Operation took {iterations} iterations.")

        if not msg == "No Path":
            s = ""
            for i in range(len(msg)):
                x, y = msg[i]
                if i != len(msg) - 1:
                    s += f"({x}, {y}) ➡ "
                else:
                    s += f"({x}, {y})"
            st.write("Path Taken:")
            st.markdown(f"```text\n{s}\n```")
            st.pyplot(fig)
        else:
            st.write(msg)
