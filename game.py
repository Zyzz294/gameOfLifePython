import tkinter as tk
from tkinter import messagebox
import main
import webbrowser


class GUI:
    def __init__(self):

        # variables for widgets
        self.mainwindow: tk.Tk = None
        self.controlsFrame: tk.LabelFrame = None
        self.rowEntry: tk.Entry = None
        self.columnEntry: tk.Entry = None
        self.cellSideEntry: tk.Entry = None
        self.simulationDelayEntry: tk.Entry = None
        self.startButton: tk.Button = None
        self.applyButton: tk.Button = None

        # variables for theme properties
        self.backgroundColor = '#000000'
        self.foregroundColor = '#1f7db7'
        self.textColor = '#ccb200'
        self.font = ('Consolas', 12)
        self.buttonColor = '#181818'
        self.buttonTextColor = '#f0f0f0'
        self.simulationCanvasColor = '#010101'
        self.livecellColor = '#00b2ff'
        self.activeAreaColor = '#101010'

        # unclassified variables
        self.simulationState = 'paused'  # 'paused'|'running'
        self.Simulator = main.Simulator(
            bg=self.simulationCanvasColor,
            fg=self.livecellColor,
            activeAreaColor=self.activeAreaColor,
            cellSide=10,
            arraySize=(190, 80))

    def initiate(self):
        ''' - function initiate the GUI
            - it invokes the GUI mainloop too '''

        # creating the main window and setting its basic properties
        self.mainwindow = tk.Tk()
        self.mainwindow.geometry('1600x800')
        self.mainwindow.configure(background=self.backgroundColor, highlightcolor=self.foregroundColor)
        self.mainwindow.minsize(width=1000, height=500)
        self.mainwindow.title('Game of Life Simulation')
        self.mainwindow.wm_protocol('WM_DELETE_WINDOW', self._exitAction)

        # creating and mounting controls frame in GUI
        self._createControls()
        self.controlsFrame.pack(side='bottom', padx=5, pady=5)

        # creating and mounting siumlation canvas in GUI
        self.Simulator.getSimulationSpace(self.mainwindow).pack(side='top', fill='both', expand=True, padx=5, pady=5)

        # self.mainwindow.bind("<Configure>", lambda event: self.Simulator.resizeCanvas(self.mainwindow))
        self.mainwindow.mainloop()

    def _createControls(self):
        ''' - function to create controls in the mainwindow
            - saves frame in self.controlFrame
            - to be called after the window is created '''

        self.controlsFrame = tk.LabelFrame(
            master=self.mainwindow,
            bg=self.backgroundColor,
            fg=self.foregroundColor,
            text='Controls',
            font=self.font
        )

        padx, pady = 5, 5

        tk.Label(
            master=self.controlsFrame,
            font=self.font,
            bg=self.backgroundColor,
            fg=self.foregroundColor,
            text='No. of Rows (integer)'
        ).grid(row=0, column=0, padx=padx, pady=pady, sticky=tk.E)

        self.rowEntry = tk.Entry(
            master=self.controlsFrame,
            font=self.font,
            width=3,
            bg=self.buttonColor,
            fg=self.buttonTextColor
        )
        self.rowEntry.grid(row=0, column=1, padx=padx, pady=pady)

        tk.Label(
            master=self.controlsFrame,
            font=self.font,
            bg=self.backgroundColor,
            fg=self.foregroundColor,
            text='No. of Columns (integer)'
        ).grid(row=1, column=0, padx=padx, pady=pady, sticky=tk.E)

        self.columnEntry = tk.Entry(
            master=self.controlsFrame,
            font=self.font,
            width=3,
            bg=self.buttonColor,
            fg=self.buttonTextColor,
        )
        self.columnEntry.grid(row=1, column=1, padx=padx, pady=pady)

        tk.Label(
            master=self.controlsFrame,
            font=self.font,
            bg=self.backgroundColor,
            fg=self.foregroundColor,
            text='Cell-side-length (px)'
        ).grid(row=0, column=2, padx=padx, pady=pady, sticky=tk.E)

        self.cellSideEntry = tk.Entry(
            master=self.controlsFrame,
            font=self.font,
            width=3,
            bg=self.buttonColor,
            fg=self.buttonTextColor,
        )
        self.cellSideEntry.grid(row=0, column=3, padx=padx, pady=pady)

        tk.Label(
            master=self.controlsFrame,
            font=self.font,
            bg=self.backgroundColor,
            fg=self.foregroundColor,
            text='Delay-per-cycle (sec)'
        ).grid(row=1, column=2, padx=padx, pady=pady, sticky=tk.E)

        self.simulationDelayEntry = tk.Entry(
            master=self.controlsFrame,
            font=self.font,
            width=3,
            bg=self.buttonColor,
            fg=self.buttonTextColor,
        )
        self.simulationDelayEntry.grid(row=1, column=3, padx=padx, pady=pady)

        self.applyButton = tk.Button(
            master=self.controlsFrame,
            bg=self.buttonColor,
            fg=self.buttonTextColor,
            font=self.font,
            text=' Apply ',
            command=self._applyButtonAction
        )
        self.applyButton.grid(padx=padx, pady=pady, row=2, column=0, columnspan=4, sticky=(tk.E, tk.W))

        tk.Button(
            master=self.controlsFrame,
            bg=self.buttonColor,
            fg=self.buttonTextColor,
            font=self.font,
            text=' Reset ',
            command=self._resetButtonAction
        ).grid(padx=padx, pady=pady, row=2, column=4, sticky=(tk.E, tk.W))

        self.startButton = tk.Button(
            master=self.controlsFrame,
            bg=self.buttonColor,
            fg=self.buttonTextColor,
            font=("Courier", 25, 'bold'),
            text='\u23F5',
            command=self._startButtonAction
        )
        self.startButton.grid(padx=padx, pady=pady, row=0, column=4, sticky=(tk.E, tk.W, tk.N, tk.S), rowspan=2)

        tk.Button(
            master=self.controlsFrame,
            bg=self.buttonColor,
            fg=self.buttonTextColor,
            font=self.font,
            text=' Exit ',
            command=self._exitAction
        ).grid(padx=padx, pady=pady, row=2, column=5, sticky=(tk.E, tk.W))

        tk.Button(
            master=self.controlsFrame,
            bg=self.buttonColor,
            fg=self.buttonTextColor,
            font=self.font,
            text=' Help ',
            command=self._showHelp
        ).grid(padx=padx, pady=pady, row=0, column=5, sticky=(tk.E, tk.W))

        tk.Button(
            master=self.controlsFrame,
            bg=self.buttonColor,
            fg=self.buttonTextColor,
            font=self.font,
            text=' About ',
            command=self._showAbout
        ).grid(padx=padx, pady=pady, row=1, column=5, sticky=(tk.E, tk.W))

        # placing default entries
        self.columnEntry.insert(0, '190')
        self.rowEntry.insert(0, '80')
        self.cellSideEntry.insert(0, '10')
        self.simulationDelayEntry.insert(0, '0.1')

    def _exitAction(self):
        ''' - call this function when an attempt to close the GUI is made
            - if confirms exit from user and if yes, performs any required exit actions '''

        if (messagebox.askyesno(title='Exit', message='Are you sure to exit?')):
            self.mainwindow.destroy()

    def _startButtonAction(self):
        ''' action for the start (start/resume/pause) button '''

        if (self.simulationState == 'paused'):
            self.simulationState = 'running'
            self.startButton.configure(text='\u23F8', font=("Courier", 25, 'bold'))
            self.applyButton.configure(state='disabled')
            self.Simulator.resume()
        else:  # simulationState == 'running'
            self.simulationState = 'paused'
            self.startButton.configure(text='\u23F5', font=("Courier", 25, 'bold'))
            self.applyButton.configure(state='normal')
            self.Simulator.pause()

    def _resetButtonAction(self):
        ''' action for the reset button '''

        self.simulationState = 'paused'
        self.startButton.configure(text='\u23F5')
        self.applyButton.configure(state='normal')
        self.Simulator.reset()

    def _showHelp(self):
        ''' call this function to show help information '''
        window = tk.Toplevel(master=self.mainwindow)
        window.title('Help JC_GameOfLife')
        window.resizable(False, False)
        padx, pady = 10, 5

        tk.Label(
            master=window,
            text='This software can be used to play/carrout-out different\ntests of the shapes in the game-of-life space and constraints.',
            font=self.font,
            justify=tk.LEFT
        ).grid(row=0, column=0, padx=padx, pady=pady, sticky=tk.W)

        tk.Label(
            master=window,
            text='CONTROLS -\n 1. Press left-mouse-button and move over dead cell (in active area) to make them living.\n 2. Similarly, move pointer with right-mouse-button pressed over live cells to kill them.',
            font=self.font,
            justify=tk.LEFT
        ).grid(row=1, column=0, padx=padx, pady=pady, sticky=tk.W)

        tk.Label(
            master=window,
            text=' 3. Use mouse-scroll to run the simulation manually. \n 4. Use play-pause button (given in controls) to run the simulation automatically.\n 5. Reset button (given in controls) to reset the simulation.\n 6. You can use mouse to change the cells in both paused and running mode.',
            font=self.font,
            justify=tk.LEFT
        ).grid(row=2, column=0, padx=padx, pady=0, sticky=tk.W)

        tk.Label(
            master=window,
            text='RECOMMENDATIONS -\n 1. Draw in paused mode if you need to draw and observe seriously. \n 2. Try adjusting the parameters as per your needs.\n 3. May use scrolling for serious observations.',
            font=self.font,
            justify=tk.LEFT
        ).grid(row=3, column=0, padx=padx, pady=pady, sticky=tk.W)

        window.mainloop()

    def _showAbout(self):
        ''' call this function to show about information '''
        window = tk.Toplevel(master=self.mainwindow)
        window.title('About JC_GameOfLife')
        window.resizable(False, False)
        padx, pady = 10, 5

        tk.Label(
            master=window,
            text="The simulation is based on mathematician John Horton Conway's\n'Game of Life' cellular automaton from 1970.",
            font=self.font,
            justify=tk.LEFT
        ).grid(row=2, column=0, padx=padx, pady=pady)

        tk.Button(
            master=window,
            text=" Conway's Game of Life ",
            font=self.font,
            command=lambda: webbrowser.open(url='https://en.m.wikipedia.org/wiki/Conway%27s_Game_of_Life')
        ).grid(row=3, column=0, padx=padx, pady=pady, sticky=tk.W)

        window.mainloop()

    def _applyButtonAction(self):
        ''' handler for apply button '''

        rows = self.rowEntry.get().strip()
        cols = self.columnEntry.get().strip()
        cellSide = self.cellSideEntry.get().strip()
        delay = self.simulationDelayEntry.get().strip()

        try:
            rows, cols, cellSide, delay = int(rows), int(cols), int(cellSide), float(delay)
        except:
            messagebox.showerror(title='Apply', message='Enter valid values for customizing the simulator.')
        else:
            if (
            messagebox.askyesno(title='Apply', message='The simulator will be reset. Are you sure to apply changes?')):
                if (delay <= 0): delay = 0.05  # this is necessary to avoid thread hangs
                self.Simulator.customize(cellSide=cellSide, arraySize=(cols, rows), simulationCycleDelay=delay)


if __name__ == '__main__':
    GUI().initiate()