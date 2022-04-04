import tkinter as tk
import threading
import time

class Simulator:
    def __init__(self, bg = 'black', fg = 'white', cellSide = 10, activeAreaColor = 'blue', arraySize = (100,100)):
        self.bg = bg
        self.fg = fg
        self.activeAreaColor = activeAreaColor
        self.cellSide = cellSide
        self.simulationSpace:tk.Canvas = None
        self.arraySize = arraySize

        self.cellStateArray:list = []             # list of list with every element being either 0 or 1
        self._createCellStateArray()

        self._simulationThreadLock = threading.Lock()
        self._simulationState = 'paused'          # 'paused'|'running'
        self.simulationCycleDelay = 0.1           # delay in seconnds
        self._simulationThreadLock.acquire()      # it is acquired when paused
        self._simulationThread = threading.Thread(target =  self._simulationLoop, daemon = True)
        self._simulationThread.start()

    def getSimulationSpace(self, master):
        ''' - creates the simulation canvas in self.simulationSpace variable
            - then, returns the self.simulationSpace variable, i.e. the canvas
            - master represents the parent widget for the canvas '''

        self.simulationSpace = tk.Canvas(
            bg = self.bg,
            bd = 0,
            highlightthickness = 0,
            width = 500
        )

        self.simulationSpace.create_rectangle(0, 0, self.cellSide*self.arraySize[0], self.cellSide*self.arraySize[1],
            tags = 'activeArea', fill = self.activeAreaColor, outline = self.activeAreaColor)

        # mechanism to allow activating/deactivating cells through mouse clicks (left and right)
        self.simulationSpace.bind('<ButtonPress-1>', self._button1Binding)
        self.simulationSpace.bind('<ButtonRelease-1>', lambda x: self.simulationSpace.unbind('<Motion>'))
        self.simulationSpace.bind('<ButtonPress-3>', self._button3Binding)
        self.simulationSpace.bind('<ButtonRelease-3>', lambda x: self.simulationSpace.unbind('<Motion>'))
        self.simulationSpace.bind('<MouseWheel>', lambda x: self.simulateOneStep())

        return self.simulationSpace

    def _createCellStateArray(self):
        self.cellStateArray = []
        for y in range(self.arraySize[1] + 2):
            self.cellStateArray.append([0]*(self.arraySize[0]+2))

    def _button1Binding(self, event):
        self._activateCellWithCoordinates(event.x, event.y)
        self.simulationSpace.bind('<Motion>', lambda event: self._activateCellWithCoordinates(event.x, event.y))

    def _button3Binding(self, event):
        self._deactivateCellWithCoordinates(event.x, event.y)
        self.simulationSpace.bind('<Motion>', lambda event: self._deactivateCellWithCoordinates(event.x, event.y))

    def _activateCellWithCoordinates(self, x_coord, y_coord):
        ''' - function to activate a cell (i.e. make it live)
            - use this function for the events of activating the cell '''

        x,y = x_coord//self.cellSide + 1, y_coord//self.cellSide + 1
        if((1<=x<=self.arraySize[0]) and (1<=y<=self.arraySize[1])):
            self._activateCell(x-1,y-1)

    def _activateCell(self, x, y):
        ''' - funcition to activate the cell (x,y) (i.e. make it live) '''

        if((0<=x<=self.arraySize[0]) and (0<=y<=self.arraySize[1])):
            if(self.cellStateArray[y+1][x+1] == 0):
                self.cellStateArray[y+1][x+1] = 1
                self.simulationSpace.create_rectangle((x)*self.cellSide, (y)*self.cellSide, (x+1)*self.cellSide, (y+1)*self.cellSide, fill = self.fg, tags = 'Cell({}{})'.format(x+1,y+1))
        else:
            raise AssertionError('Cell ({},{}) out of range of the active array.'.format(x+1,y+1))

    def _deactivateCellWithCoordinates(self, x_coord, y_coord):
        ''' - function to deactivate a cell (i.e. make it live)
            - use this function for the events of deactivating the cell '''

        x,y = x_coord//self.cellSide + 1, y_coord//self.cellSide + 1
        if((1<=x<=self.arraySize[0]) and (1<=y<=self.arraySize[1])):
            self._deactivateCell(x-1,y-1)

    def _deactivateCell(self, x, y):
        ''' - funcition to deactivate the cell (x,y) (i.e. make it live) '''

        if((0<=x<=self.arraySize[0]) and (0<=y<=self.arraySize[1])):
            if(self.cellStateArray[y+1][x+1] == 1):
                self.cellStateArray[y+1][x+1] = 0
                self.simulationSpace.delete('Cell({}{})'.format(x+1,y+1))
        else:
            raise AssertionError('Cell ({},{}) out of range of the active array.'.format(x+1,y+1))

    def _simulationLoop(self):
        ''' - to be used inside simulation-thread '''

        while(True):                                                         # the thread running this is daemon, so, even in this infinite loop, it will end when main thread exits
            self._simulationThreadLock.acquire()
            self.simulationSpace.after_idle(func = self.simulateOneStep)     # this way, you ensure that simulateOneStep is executed only when it is not colliding with any other tkinter events
            self._simulationThreadLock.release()
            time.sleep(self.simulationCycleDelay)

    def simulateOneStep(self):
        ''' - call this function to simulate 1 step forward '''

        newcellStateArray = tuple(tuple(x) for x in self.cellStateArray)
        for y in range(0, self.arraySize[1]):
            for x in range(0, self.arraySize[0]):
                environment_value = newcellStateArray[y][x]+newcellStateArray[y][x+1] + newcellStateArray[y][x+2] +\
                    newcellStateArray[y+1][x] + newcellStateArray[y+1][x+2] +\
                    newcellStateArray[y+2][x] + newcellStateArray[y+2][x+1] + newcellStateArray[y+2][x+2]

                if((environment_value < 2) or (environment_value > 3)): self._deactivateCell(x,y)
                elif(environment_value == 3): self._activateCell(x,y)
                else: pass

    def reset(self):
        self.pause()
        for y in range(0, self.arraySize[1]):
            for x in range(0, self.arraySize[0]):
                self.cellStateArray[y+1][x+1] = 0
                self.simulationSpace.delete('Cell({}{})'.format(x+1,y+1))

    def pause(self):
        if(self._simulationState == 'running'): self._simulationThreadLock.acquire()
        self._simulationState = 'paused'

    def resume(self):
        if(self._simulationState == 'paused'): self._simulationThreadLock.release()
        self._simulationState = 'running'

    def customize(self, cellSide:int, arraySize:tuple, simulationCycleDelay:float):
        ''' - function to customize the properties of the simulator
            - call this only when the simulation is not running
            - note: the simulation will be reset while customizing
        '''
        self.reset()
        self.arraySize = arraySize
        self.cellSide = cellSide
        self.simulationCycleDelay = simulationCycleDelay
        self._createCellStateArray()

        # it is necessary to delete the older activeArea so that the bindings work on new arraySize
        # and since the older activeArea is removed, it is a good idea to create it again for the intended purpose (tell the user the active area)
        self.simulationSpace.delete('activeArea')
        self.simulationSpace.create_rectangle(0, 0, self.cellSide*self.arraySize[0], self.cellSide*self.arraySize[1],
            tags = 'activeArea', fill = self.activeAreaColor, outline = self.activeAreaColor)

    def showCellStates(self):
        ''' function for debugging purposes '''
        for row in self.cellStateArray:
            print(row)
