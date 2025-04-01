# eyetracking-benchmarking
Analyzing experimental data comparing the performance of professional eyetrackers and webcam-based eyetrackers.

## Authors
Publication Name: WIP
Journal: WIP
DOI: WIP

- [Manuel García-Romero](https://scholar.google.com/citations?hl=es&user=eu0urvcAAAAJ)
- [Antonio Martínez-Rojas](https://scholar.google.com/citations?user=qhMxtwMAAAAJ&hl=es&oi=ao)
- [Andrés Jiménez Ramírez](https://scholar.google.com/citations?user=qxRi-4gAAAAJ&hl=es&oi=ao)
- [José González Enríquez](https://scholar.google.com/citations?user=uMfdKyEAAAAJ&hl=es&oi=ao)

The data is located in the tests folder after the execution is done.

To execute this, you can create a virtual environment:

Create a virtual environment in the current folder:

```bash
python -m venv .venv
```

3. Activate the virtual environment:
    - On Windows:
        
```bash
.venv\Scripts\activate
```
    - On macOS/Linux:
        
```bash
source .venv/bin/activate
```

4. Make sure the virtual environment is activated. You should see the name of the virtual environment in the terminal prompt.

5. Select the Python interpreter of the virtual environment in Visual Studio Code:
    - Open the command palette and run the command **Python: Select Interpreter**.

Run the following command to install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Project

To run the project, execute the `run.py` script:

```bash
python run.py
```
To run plots, you need to install latex, ghostscript and dvipng binaries packages to proceed

https://miktex.org/download
https://ghostscript.com/
https://www.nongnu.org/dvipng/

## Project Structure

- `configuration/`: Contains JSON configuration files for determined scenarios.
- `metrics.py`: Contains functions for processing and analyzing metrics.
- `results.py`: Handles the results of the analysis.
- `plots.py` : Plots are generated from the analysis.
- `run.py`: Main script to execute the project.
- `settings.py`: Configuration settings for the project.
- `tests/`: Contains test data and the results of the execution.

## License

This research was supported by the EQUAVEL project PID2022-137646OB-C31, funded
by MICIU/AEI/10.13039/501100011033 and by FEDER, UE; and the
grant FPU20/05984 funded by MICIU/AEI/10.13039/501100011033 and by FSE+.