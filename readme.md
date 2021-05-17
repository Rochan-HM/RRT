# Readme

## Usage

This app comes with a **GUI** and a **CLI**.

### Using Docker

To run the GUI, run,

```sh
docker-compose run -p 80:8501 gui
```

from the root directory and navigate to `localhost` on your browser. The GUI shows the path taken and the plot.

Likewise, to run the CLI, run,

```sh
docker-compose run cli
```

and the list of points will be logged to the terminal.

### Without Docker

To run the GUI, install all the requirements via `pip install -r requirements.txt` and run

```sh
streamlit run ./src/app.py
```

from the root directory.

To run the CLI, install all the requirements via `pip install -r requirements.txt` and run

```sh
python ./src/rrt.py
```

from the root directory.

## Configuration

### GUI

All the parameters can be configured in the form in the GUI.

### CLI

All the parameters can be configured under the `# Constants` comment header inside `rrt.py`. In addition, all the parameters can also be passed in as arguments to the constructor of the `RRT` class.

#### Note

Due to the random number generation, sometimes, the algorithm may fail to find a route. Rerunning might help in such cases.
