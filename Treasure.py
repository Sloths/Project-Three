from Tkinter import *
import ttk
import random
import time

window = Tk()
canvas = Canvas(window, width=854, height=480, bg="#3796da")
canvas.pack()

#Creates window and centers to any screen
window.geometry('{}x{}'. format(1060, 670)) #Setting size of window
window.withdraw() #Hide window to stop showing in wrong position
window.update_idletasks() #Request screen size from sstem
x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / 2 #Calculate screen width
y = ((window.winfo_screenheight() - window.winfo_reqheight()) / 2) - 70 #Calculate screen height
window.geometry("+%d+%d" % (x, y)) #Change position of window
window.title('Sloths - Virtual Robot Treasure Hunt') #Adds name to window
window.resizable(width=FALSE, height=FALSE) #Disabled resizable function of window
window.deiconify() #Redraw window in correct position

intPlay = 0
SelectedMap = 1

coinImage = PhotoImage(file="coin.gif")
greenImage = PhotoImage(file="greenjewel.gif")
redImage = PhotoImage(file="redjewel.gif")
chestImage = PhotoImage(file="chest.gif")
pirateImage = PhotoImage(file="pirate.gif")

class landmark:                                   # Landmark class being created
    def __init__(self, x1, y1, x2, y2):             # this sets out the layout of how all future objects will be set in order to be created
        self.x1 = x1                                # whatever the objects name.x1 or x2 or y1 or y2, store the value in x1, which then places it in the user interface
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.colour  = "#e7df63"                      # the background colour for all landmarks is set here to green in the user interface
        self.outline = "black"                      # the outline colour of all landmarks is set to black in the user interface
        self.treasure = False                       #  setting the variable with the value of 'false'
        self.treasureID = ""                        #creating treasure ID for robot 
        
        self.lndmrk = canvas.create_rectangle(self.x1,self.y1,self.x2,self.y2, fill=self.colour, outline = self.outline, tag="Landmark") # creates the landmark with the given coordinates and colours, but they're pre-set.
        
def MapOneLandMarks():                              #creating a new function which will store all the landmarks in the first map
    global obstacles 
    obstacles = [
        # this code within the array creates the first landmark                        
        landmark(30,50,180,120),                 
        landmark(670,50,825,120), 
        landmark(30,460,180,330), 
        landmark(670,460,825,330),                              
        landmark(270,370,590,430),
        landmark(160,160,690,230)]
        
class Robot:
    def __init__(self):
        self.vx = 10.0
        self.vy = 0.0
        self.rXPos = 0
        self.rYPos = 0   
        self.status = "" #String to display status of robot
        self.points = 100 #Integer to display points of robot
        self.run = False #Used for when robot should run
        self.done = False #Used for when robot is done i.e. got all treasures
        self.shipSprite = PhotoImage(file="ship.gif")
        

    def robotLoad(self):
        self.rXPos = random.randint(20, 854)
        self.rYPos = random.randint(30, 400)
        
        for o in obstacles:            
            ox1, oy1, ox2, oy2 = canvas.coords(o.lndmrk)

            if (self.rXPos > ox1 - 10.0 and self.rXPos < ox2 + 10.0) and (self.rYPos > oy1 - 10.0 and self.rYPos < oy2 + 10.0):
                self.robotLoad()

            else:
                self.robot = canvas.create_rectangle(self.rXPos, self.rYPos, self.rXPos + 10.0, self.rYPos + 10.0, fill = "blue")
                self.run = True

    def robotMove(self):        
        while True:            
            x1, y1, x2, y2 = canvas.coords(self.robot)
            self.bypassLandmark(x1, y1, x2, y2)
            self.trapCollision(x1, y1, x2, y2, traps[0])
            self.trapCollision(x1, y1, x2, y2, traps[1])

            # Boundary Response            
            if x2 > 840.0:
                self.vx = -10.0
                self.vy = 0.0

            if x1 < 20.0:
                self.vx = 10.0
                self.vy = 0.0

            if y2 > 470.0:
                self.vx = 0.0
                self.vy = -5.0
                '''if x2 > 840.0:
                    self.vx = 0.0
                    self.vy = -5.0
                elif x2 < 850.0:
                    self.vx = 10.0
                    self.vy = 0.0'''
            
            if y1 < 30.0:
                self.vx = 0.0
                self.vy = 5.0
                '''if x1 < 10.0:
                    self.vx = 0.0
                    self.vy = 5.0
                elif x1 > 10.0:                    
                    self.vx = -10.0
                    self.vy = 0.0'''

            # Add velocity value to Robot position
            self.rXPos += self.vx
            self.rYPos += self.vy            

            canvas.coords(self.robot, x1 + self.vx, y1 + self.vy, x2 + self.vx, y2 + self.vy)

            canvas.update()                
            time.sleep(0.1)

    def trapCollision(self, x1, y1, x2, y2, trap):
        print self.points
        if (x2 > trap.xpos and x1 < trap.xpos + 30.0) and (y2 > trap.ypos and y1 < trap.ypos + 30.0):
            self.points -= 10
            print self.points

    def bypassLandmark(self, x1, y1, x2, y2):
        for o in obstacles:
            ox1, oy1, ox2, oy2 = canvas.coords(o.lndmrk)
            
            if (x2 > ox1 - 10.0 and x2 < ox1 + 10.0) and y2 > oy1 and y1 < oy2: # APPROACH FROM LEFT
                if self.vy == -5.0 or self.vy == 0.0:
                    self.vx = 0.0
                    self.vy = -5.0
                elif self.vy == 5.0:
                    self.vx = 0.0
                    self.vy = 5.0
                else:
                    continue
            
            if (x1 < ox2 + 10.0 and x1 > ox2 - 10.0) and y2 > oy1 and y1 < oy2: # APPROACH FROM RIGHT
                if self.vy == -5.0 or self.vy == 0.0:
                    self.vx = 0.0
                    self.vy = -5.0
                elif self.vy == -5.0:
                    self.vx = 0.0
                    self.vy = 5.0
                else:
                    continue

            if (y2 > oy1 - 10.0 and y2 < oy1 + 10.0) and x2 > ox1 and x1 < ox2: # APPROACH FROM TOP
                if self.vx == -10.0 or self.vx == 0.0:
                    self.vx = -10.0
                    self.vy = 0.0
                elif self.vx == 10.0:                
                    self.vx = 10.0
                    self.vy = 0.0
                else:
                    continue

            if (y1 < oy2 + 10.0 and y1 > oy2 - 10.0) and x1 > ox1 and x2 < ox2: # APPROACH FROM BOTTOM
                if self.vx == -10.0 or self.vx == 0.0:
                    self.vx = -10.0
                    self.vy = 0.0
                elif self.vx == 10.0:
                    self.vx = 10.0
                    self.vy = 0.0
                else:
                    continue

    # def lightResponse(self):                  

    '''def robotMove(self, treasures):
        if self.run == True:
            if self.done == False:
                for o in obstacles: # Iterate through obstacle list
                    ox1, oy1, ox2, oy2 = canvas.coords(o.lndmrk) # Creating coordinates for landmark object
                    while o.treasure == True:
                        
                        self.x1, self.y1, self.x2, self.y2 = canvas.coords(self.robot) # Creating coordinates for robot object

                        # GENERAL ROBOT MOVEMENT
                        if self.x1 > 0.0 and self.x2 < (213.5 - 10.0): # Is robot in section 1?
                            tag = str(canvas.gettags(section1))
                            tag = tag.replace("('", "")
                            tag = tag.replace("',)", "")
                            self.status = tag
                            
                            if tag == "Red": # If section 1 is red, stop robot movement.
                                self.vx = 0.0
                                self.vy = 0.0
                                                
                            elif tag == "Amber": # If section 1 is amber, decrease movement speed by half.
                                if self.x2 < ox1:
                                    self.vx = 5.0
                                    self.vy = 0.0
                                if self.x1 > ox2:
                                    self.vx = -5.0
                                    self.vy = 0.0
                                if self.y2 < oy1:
                                    self.vy = 5.0
                                    self.vx = 0.0
                                if self.y1 > oy2:
                                    self.vy = -5.0
                                    self.vx = 0.0
                                                        
                            elif tag == "Green": # If section 1 is green, movement speed is normal.
                                if self.x2 < ox1:
                                    self.vx = 10.0
                                    self.vy = 0.0
                                if self.x1 > ox2:
                                    self.vx = -10.0
                                    self.vy = 0.0
                                if self.y2 < oy1:
                                    self.vy = 10.0                        
                                    self.vx = 0.0
                                if self.y1 > oy2:
                                    self.vy = -10.0
                                    self.vx = 0.0

                        if self.x1 > (213.5 + 10.0) and self.x2 < (427.0 - 10.0): # Is robot in section 2?
                            tag = str(canvas.gettags(section2))
                            tag = tag.replace("('", "")
                            tag = tag.replace("',)", "")
                            self.status = tag
                            
                            if tag == "Red": # If section 2 is red, stop robot movement.
                                self.vx = 0.0
                                self.vy = 0.0
                                
                            elif tag == "Amber": # If section 2 is amber, decrease movement speed by half.
                                if self.x2 < ox1:
                                    self.vx = 5.0
                                    self.vy = 0.0
                                if self.x1 > ox2:
                                    self.vx = -5.0
                                    self.vy = 0.0
                                if self.y2 < oy1:
                                    self.vy = 5.0
                                    self.vx = 0.0
                                if self.y1 > oy2:
                                    self.vy = -5.0
                                    self.vx = 0.0
                                                        
                            elif tag == "Green": # If section 2 is green, movement speed is normal.
                                if self.x2 < ox1:
                                    self.vx = 10.0
                                    self.vy = 0.0
                                if self.x1 > ox2:
                                    self.vx = -10.0
                                    self.vy = 0.0
                                if self.y2 < oy1:
                                    self.vy = 10.0
                                    self.vx = 0.0
                                if self.y1 > oy2:
                                    self.vy = -10.0
                                    self.vx = 0.0

                        if self.x1 > (427.0 + 10.0) and self.x2 < (640.5 - 10.0): # Is robot in section 3?
                            tag = str(canvas.gettags(section3))
                            tag = tag.replace("('", "")
                            tag = tag.replace("',)", "")
                            self.status = tag
                            
                            if tag == "Red": # If section 3 is red, stop robot movement.
                                self.vx = 0.0
                                self.vy = 0.0               
                            elif tag == "Amber": # If section 3 is amber, decrease movement speed by half.
                                if self.x2 < ox1:
                                    self.vx = 5.0
                                    self.vy = 0.0
                                if self.x1 > ox2:
                                    self.vx = -5.0
                                    self.vy = 0.0
                                if self.y2 < oy1:
                                    self.vy = 5.0
                                    self.vx = 0.0
                                if self.y1 > oy2:
                                    self.vy = -5.0
                                    self.vx = 0.0
                                                        
                            elif tag == "Green": # If section 3 is green, movement speed is normal.
                                if self.x2 < ox1:
                                    self.vx = 10.0
                                    self.vy = 0.0
                                if self.x1 > ox2:
                                    self.vx = -10.0
                                    self.vy = 0.0
                                if self.y2 < oy1:
                                    self.vy = 10.0
                                    self.vx = 0.0
                                if self.y1 > oy2:
                                    self.vy = -10.0
                                    self.vx = 0.0

                        if self.x1 > (640.5 + 10.0) and self.x2 < (854.0 - 10.0): # Is robot in section 4?
                            tag = str(canvas.gettags(section4))
                            tag = tag.replace("('", "")
                            tag = tag.replace("',)", "")
                            self.status = tag
                            
                            if tag == "Red": # If section 4 is red, stop robot movement.
                                self.vx = 0.0
                                self.vy = 0.0
                                
                            elif tag == "Amber": # If section 4 is amber, decrease movement speed by half.
                                if self.x2 < ox1:
                                    self.vx = 5.0
                                    self.vy = 0.0
                                if self.x1 > ox2:
                                    self.vx = -5.0
                                    self.vy = 0.0
                                if self.y2 < oy1:
                                    self.vy = 5.0
                                    self.vx = 0.0
                                if self.y1 > oy2:
                                    self.vy = -5.0
                                    self.vx = 0.0
                                                        
                            elif tag == "Green": # If section 4 is green, movement speed is normal.
                                if self.x2 < ox1:
                                    self.vx = 10.0
                                    self.vy = 0.0
                                if self.x1 > ox2:
                                    self.vx = -10.0
                                    self.vy = 0.0
                                if self.y2 < oy1:
                                    self.vy = 10.0
                                    self.vx = 0.0
                                if self.y1 > oy2:
                                    self.vy = -10.0
                                    self.vx = 0.0			

                        # LOCATION CHECK
                        if self.x2 > ox1 - 20.0 and self.x2 < ox2 + 20.0 and self.y1 > oy1 - 20.0 and self.y2 < oy2 + 20.0:
                            o.treasure = False # If robot contacts landmark with treasure
                            ID = o.treasureID 
                            canvas.delete(ID) # Delete treasure object from list
                            o.treasureID = ""
                            self.points += 100 #Add 100 to points as treasure has been found
                            
                        self.rXPos += self.vx                
                        self.rYPos += self.vy
                        
                        canvas.delete(self.robot)
                        self.robotDraw()                
                        canvas.update()
                        self.updateInfo()
                        time.sleep(0.1)
                self.done = True
                self.updateInfo()'''
                
    '''def robotStop(self): #Function to stop robot by changing values
        self.run = False #Run changes to false to stop
        self.done = False #Done changes back to default
        canvas.delete("robotTag") #Deletes robot from canvas'''
            
    '''def updateInfo(self): #Function to update info about robot in GUI
        if self.done == True: #If robot is done
            self.run = False
            rb1Status.config(text='Status: Done') #Change status to done
            global rb1T
            rb1T.Done() #Stop timer but still display time
        elif self.run == True: #Constantly update info if robot is running
            rb1Position.config(text='Position: x:' + str(int(self.x1)) + " y:" + str(int(self.y1))) #Change x/y position info
            rb1Status.config(text='Status: ' + self.status) #Chnage status
            #Yet to add other labels yet
            rb1Points.config(text='Points: ' + str(self.points)) #Update points
        else:
            ResetLabels() #Run function to reset labels to default if robot not running anymore'''
            
class Treasure:
   #create random spawn location of treasure, coordinates need adjusting with landmarks 
    def __init__(self, n, x=0,y=0,size = 12,colour='#ffd700'):
        
        self.colour = colour
        self.size = size
        self.n = n # the given number of treasures to give IDs
        self.id = "Treasure" + str(n)  # giving the treasure different IDs, easier for robot to detect 
        #print self.id - put in place to test Treasure IDs
        
    def checkLandmark(self):
        global intPlay 
        if intPlay <=1:  # if intial play is less than or equal to one, create random search of objects for treasure 
            n = random.randint(0,len(obstacles)-1) # chooses random object within obstacle array. index 0 - 8 but -1, because 7 landmarks 
            
            if obstacles[n].treasure == False: # if no treasure in landmark 
                x1,y1,x2,y2=canvas.coords(obstacles[n].lndmrk) # place within middle of random object chosen.
                self.x = (x1+x2)/2 # average of the x axis for object
                self.y = (y1+y2)/2 # average of the y axis for object to get centre
                obstacles[n].treasure = True # random obstacle has treasure inside it
                obstacles[n].treasureID = self.id #each treasure in landmark is given an ID 
            else:
                self.checkLandmark() # checks landmarks if there is a treasure present, if so choose another. 
        
    def DrawTreasure(self,canvas): #creating the attributes for the treasure
        self.checkLandmark() # call checkLandmark to make sure no treasure is present before creating 
        self.shape = canvas.create_oval(self.x,self.y,self.x + self.size, self.y + self.size,outline = self.colour, fill=self.colour,tag=self.id)
        # creating object, size goes against each x and y coordinates. tag inplace to call for deletion


              
class Timer:
    def __init__(self, label):
        self.second = 0
        self.minute = 0
        self.hour = 0
        self.time = ""
        self.stop = False
        self.done = False
        self.label = label
        self.sections = {}

    def Stop(self):
        #used to stop timer and get rid of time i.e. when game is done
        global intPlay
        intPlay = 0
        # used so the timer stops
        self.stop = True
        # used as the robot has not found the treasure
        self.done = False
        
    def Done(self): #Change to done if robot is done
        #used so that timer stops but still displays time
        self.stop = True
        self.done = True
        
    def Count(self):
        # condition - if the program is running
        if self.stop == False:
             # second increments by 1
            self.second = self.second + 1
            if self.second == 60:
                # once the timer reaches 60 seconds, a minute is reached and the seconds are set back to 0 to repeat process
                self.minute = self.minute + 1
                self.second = 0
            if self.minute == 60:
                # once the timer reaches 60 minutes, an hour is reached and the minutes are set to 0 to repeat the process
                self.hour = self.hour + 1
                self.minute = 0

            #Generate 4 random numbers between 1 - 3 for lights
            # lights change every 5 seconds
            if self.second % 5 == 0:
                light1.ChangeLight()
                light2.ChangeLight()
                light3.ChangeLight()
                light4.ChangeLight()

            # formatting of timer display hh:mm:ss
            if self.hour < 10:
                if self.minute < 10:
                    if self.second < 10:
                        # e.g. 01:02:03
                        self.time = "0" + str(self.hour) + ":0" + str(self.minute) + ":0" + str(self.second)
                    else:
                        # e.g. 01:02:34
                        self.time = "0" + str(self.hour) + ":0" + str(self.minute) + ":" + str(self.second)
                else:
                    if self.second < 10:
                        # e.g. 01:23:04
                        self.time = "0" + str(self.hour) + ":" + str(self.minute) + ":0" + str(self.second)
                    else:
                        # e.g. 01:23:45
                        self.time = "0" + str(self.hour) + ":" + str(self.minute) + ":" + str(self.second)
            else:
                if self.minute < 10:
                    if self.second < 10:
                        # e.g. 12:03:04
                        self.time = str(self.hour) + ":0" + str(self.minute) + ":0" + str(self.second)
                    else:
                        # e.g. 12:03:45
                        self.time = str(self.hour) + ":0" + str(self.minute) + ":" + str(self.second)
                else:
                    if self.second < 10:
                        # e.g. 12:34:05
                        self.time = str(self.hour) + ":" + str(self.minute) + ":0" + str(self.second)
                    else:
                        #12:34:56
                        self.time = str(self.hour) + ":" + str(self.minute) + ":" + str(self.second)
            # executing the timer display as a string so it can display as a label
            exec str(self.label.config(text=(self.time)))
            # 1000 ticks == 1 second delay and continues the Count function
            self.label.after(1000, self.Count)
        else:
            # when the robot has found the treasures the timer is stopped, and the time the robot found the treasures in is displayed
            if self.done == True:
                exec str(self.label.config(text=(self.time)))
            else:
                # display of timer when Stop is pressed
                exec str(self.label.config(text="00:00:00"))

#Class for lights
class Light():
    def __init__(self, number):
        self.width = 854 #width of canvas
        self.height = 480 #height of canvas
        self.sectionWidth = 213.5 #width of one section (1/4 of whole width)
        self.number = number #number of section
        self.colour = "" #string to hold colour of section

    def CreateLight(self): #Function to create the lights for GUI
        #globalising objects to be made
        global lightcolour1
        global lightcolour2
        global lightcolour3
        global lightcolour4
        global section1
        global section2
        global section3
        global section4
        global light1Text
        global light2Text
        global light3Text
        global light4Text
        
        if self.number == 1: #if section 1, place in left most position
            lightcolour1=canvas.create_rectangle(2, 2, self.sectionWidth, 23, fill="#2ecc71", tag="1") #Create light block and tag number
            section1=canvas.create_rectangle(0, self.height + 1, self.sectionWidth, 23, dash=(10,10), tag="Green") #Create dashed section and tag colour
            light1Text=Label(font=('Helvetica', 8), text='Green', bg="#2ecc71") #Create label to match colour of section
            light1Text.place(x=100, y=13) #Place label in correct position
            self.colour = "Green" #Change string to hold value of light
        elif self.number == 2: #If section 2, place in left mid position
            lightcolour2=canvas.create_rectangle(self.sectionWidth, 2, self.sectionWidth * self.number, 23, fill="#f39c12", tag="2") #Create light block and tag number
            section2=canvas.create_rectangle(self.sectionWidth, self.height + 1, self.sectionWidth * 2, 23, dash=(10,10), tag="Amber") #Create dashed section and tag colour
            light2Text=Label(font=('Helvetica', 8), text='Amber', bg="#f39c12") #Create label to match colour of section
            light2Text.place(x=310, y=13) #Place label in correct position
            self.colour = "Amber" #Change string to hold value of light
        elif self.number == 3: #If section 3, place in right mid position
            lightcolour3=canvas.create_rectangle(self.sectionWidth * (self.number - 1), 2, self.sectionWidth * self.number, 23, fill="#e74c3c", tag="3") #Create light block and tag number
            section3=canvas.create_rectangle(self.sectionWidth * 2, self.height + 1, self.sectionWidth * 3, 23, dash=(10,10), tag="Red") #Create dashed section and tag colour
            light3Text=Label(font=('Helvetica', 8), text='Red', bg="#e74c3c")  #Create label to match colour of section
            light3Text.place(x=530, y=13) #Place label in correct position
            self.colour = "Red" #Change string to hold value of light
        elif self.number == 4: #If section 4, place in right most position
            lightcolour4=canvas.create_rectangle(self.sectionWidth * (self.number - 1), 2, ((self.sectionWidth * self.number) + 1), 23, fill="#2ecc71", tag="4") #Create light block and tag number
            section4=canvas.create_rectangle(self.sectionWidth * 3, self.height + 1, ((self.sectionWidth * 4) + 1), 23, dash=(10,10), tag="Green") #Create dashed section and tag colour
            light4Text=Label(font=('Helvetica', 8), text='Green', bg="#2ecc71") #Create label to match colour of section
            light4Text.place(x=740, y=13) #Place label in correct position
            self.colour = "Green" #Change string to hold value of light
        
    def ChangeLight(self): #Function to change lights, called in timer class count function
        intColour = random.randrange(1,4) # Random selection of traffic lights ranging from 1 - 3
        
        global canvas
        
        if intColour == 1: #If random number = 1 (Green)
            self.colour = "Green" #Change value of colour string
            if self.number == 1: #Check for section to change
                light1Text.config(text='Green', bg="#2ecc71") #Change label text to correct value
                canvas.itemconfig(lightcolour1, fill="#2ecc71") #Change light to correct colour
                canvas.itemconfig(section1, tag="Green") #Change section tag to correct value
            elif self.number == 2:
                light2Text.config(text='Green', bg="#2ecc71") #Change label text to correct value
                canvas.itemconfig(lightcolour2, fill="#2ecc71") #Change light to correct colour
                canvas.itemconfig(section2, tag="Green")  #Change section tag to correct value
            elif self.number == 3:
                light3Text.config(text='Green', bg="#2ecc71") #Change label text to correct value
                canvas.itemconfig(lightcolour3, fill="#2ecc71") #Change light to correct colour
                canvas.itemconfig(section3, tag="Green") #Change section tag to correct value
            elif self.number == 4:
                light4Text.config(text='Green', bg="#2ecc71") #Change label text to correct value
                canvas.itemconfig(lightcolour4, fill="#2ecc71") #Change light to correct colour
                canvas.itemconfig(section4, tag="Green")
        elif intColour == 2: #If random number = 2 (Amber)
            self.colour = "Amber" #Change value of colour string
            if self.number == 1: #Check for section to change
                light1Text.config(text='Amber', bg="#f39c12") #Change label text to correct value
                canvas.itemconfig(lightcolour1, fill="#f39c12") #Change light to correct colour
                canvas.itemconfig(section1, tag="Amber") #Change section tag to correct value
            elif self.number == 2:
                light2Text.config(text='Amber', bg="#f39c12") #Change label text to correct value
                canvas.itemconfig(lightcolour2, fill="#f39c12") #Change light to correct colour
                canvas.itemconfig(section2, tag="Amber") #Change section tag to correct value
            elif self.number == 3:
                light3Text.config(text='Amber', bg="#f39c12") #Change label text to correct value
                canvas.itemconfig(lightcolour3, fill="#f39c12") #Change light to correct colour
                canvas.itemconfig(section3, tag="Amber") #Change section tag to correct value
            elif self.number == 4:
                light4Text.config(text='Amber', bg="#f39c12") #Change label text to correct value
                canvas.itemconfig(lightcolour4, fill="#f39c12") #Change light to correct colour
                canvas.itemconfig(section4, tag="Amber")
        elif intColour == 3: #If random number = 3 (Red)
            self.colour = "Red" #Change value of colour string
            if self.number == 1: #Check for section to change
                light1Text.config(text='Red', bg="#e74c3c") #Change label text to correct value
                canvas.itemconfig(lightcolour1, fill="#e74c3c") #Change light to correct colour
                canvas.itemconfig(section1, tag="Red") #Change section tag to correct value
            elif self.number == 2:
                light2Text.config(text='Red', bg="#e74c3c") #Change label text to correct value
                canvas.itemconfig(lightcolour2, fill="#e74c3c") #Change light to correct colour
                canvas.itemconfig(section2, tag="Red") #Change section tag to correct value
            elif self.number == 3:
                light3Text.config(text='Red', bg="#e74c3c") #Change label text to correct value
                canvas.itemconfig(lightcolour3, fill="#e74c3c") #Change light to correct colour
                canvas.itemconfig(section3, tag="Red") #Change section tag to correct value
            elif self.number == 4:
                light4Text.config(text='Red', bg="#e74c3c") #Change label text to correct value
                canvas.itemconfig(lightcolour4, fill="#e74c3c") #Change light to correct colour
                canvas.itemconfig(section4, tag="Red") #Change section tag to correct value
        
class image(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.location = ""
        self.draw = canvas
        self.draw.pack()
        self.widgets() 
    def down(self, event):
        self.xLast = event.x # coords of where the mouse went down
        self.yLast = event.y

    def move(self, event):
        # whatever the mouse is over it will be tagged as current 
        self.draw.move(CURRENT, event.x - self.xLast, event.y - self.yLast)
        self.xLast = event.x
        self.yLast = event.y
        
    def widgets(self):   
        self.draw.tag_bind(test,"<1>", self.down) # 1 indicates the left click on the mouse, 2 is middle and 3 is right
        self.draw.tag_bind('test',"<B1-Motion>", self.move) # movement of mouse when click is held down  
        
    def spawn(self, x, y, image):
        self.image = PhotoImage(file=image)
        self.x = x
        self.y = y
        self.draw.create_image(self.x, self.y,image = self.image , anchor = NW,tag ='test')
        if image == "coin.gif":
            TreasureButtons[0].config(state="disabled")
        elif image == "greenjewel.gif":
            TreasureButtons[1].config(state="disabled")
        elif image == "redjewel.gif":
            TreasureButtons[2].config(state="disabled")
        elif image == "chest.gif":
            TreasureButtons[3].config(state="disabled")

class treasure(image):
    def __init__(self):
        image.__init__(self) # use the init from image class to create images, inheritance 
        self.points = 0

class Trap(image):
    def __init__(self):
        image.__init__(self)
        self.xpos = 0
        self.ypos = 0
        self.hit = False
        self.points = 0

    #def points(self):
        #get points from last collected treasure
        
    def create(self): #Creates the x,y position of trap to check in 
        self.xpos = random.randint(20,800)
        self.ypos = random.randint(200,400)
        for o in obstacles:            
            ox1, oy1, ox2, oy2 = canvas.coords(o.lndmrk)
            if (self.xpos > ox1 - 25.0 and self.xpos < ox2 + 25.0) and (self.ypos > oy1 - 25.0 and self.ypos < oy2 + 25.0):
                self.create()
            else:
                self.spawn(self.xpos, self.ypos, "trap.gif")
                     
    #def hit(self):
        #show image of trap
        #deduct points from score
        #change pirate thought
        #
                
                
def Start():
    global intPlay
    intPlay += 1
    if intPlay <= 1:
        global main
        global rb1T
        global rb2T
        global m
        #global spawnTreasure # no need for this global variable 
        global R1
        global R2
        main = Timer(timer)
        rb1T = Timer(rb1Timer)
        rb2T = Timer(rb2Timer)
        main.Count()
        rb1T.Count()
        rb2T.Count()
        spawnTreasure= [] # creating an empty array for number of treasures using for loop
        
        for n in range (4): #giving a range between index 0 - 3 
            spawnTreasure.append(Treasure(n)) #update empty array with given argument 
            spawnTreasure[n].DrawTreasure(canvas)# draw treasure onto canvas           
  		 

MapOneLandMarks()
        
traps = []
for n in range(0,2):
    traps.append(Trap())
    traps[n].create()

treasureitems = [] # empty list to populate with treasure 
treasurex = [830,820] # create a fixed x position for treasure 
treasurey = [123, 160, 200, 240] # give different y position for treasure 

#iterate through loop and use treasure class to populate 
for n in range(0,4):
    treasureitems.append(treasure())

frames = []
FrameHeight = [158, 85, 85, 480, 165, 140, 158]
FrameWidth = [854, 180, 220, 175, 160, 160, 175]
FramePlacementx = [11, 275, 476, 872, 880, 880, 872]
FramePlacementy = [500, 565, 565, 11, 128, 344, 500]
for n in range(0,7):
    frames.append(Frame(bd=1, relief=SUNKEN, height=FrameHeight[n], width=FrameWidth[n]))
    frames[n].place(x=FramePlacementx[n], y=FramePlacementy[n])

TreasureButtons = []
TreasureButtonImage = [coinImage, greenImage, redImage, chestImage]
TreasureButtonCommand = [lambda: treasureitems[0].spawn(treasurex[0], treasurey[0], "coin.gif"), lambda: treasureitems[1].spawn(treasurex[0], treasurey[1], "greenjewel.gif"),
                         lambda: treasureitems[2].spawn(treasurex[0], treasurey[2], "redjewel.gif"), lambda: treasureitems[3].spawn(treasurex[1], treasurey[3], "chest.gif")]
TreasureButtonPlacementy = [130, 168, 208, 247]
for n in range(0,4):
    TreasureButtons.append(Button(window, image =TreasureButtonImage[n], command=TreasureButtonCommand[n]))
    TreasureButtons[n].place(x=884, y=TreasureButtonPlacementy[n])

def test1():
    print "works"

ButtonList = []
ButtonString = ["Start", "1", "2", "3", "4", "5", "6"]
ButtonPlacementx = [878, 877, 902, 927, 952, 977, 1002]
ButtonPlacementy = [505, 77, 77, 77, 77, 77, 77]
ButtonWidth = [22, 2, 2, 2, 2, 2, 2]
ButtonCommand = [Start, test1, test1, test1, test1, test1, test1]
for n in range (0,7):
    ButtonList.append(Button(window, text=ButtonString[n], height=1, width=ButtonWidth[n], command=ButtonCommand[n]))
    ButtonList[n].place(x=ButtonPlacementx[n], y=ButtonPlacementy[n])

#Creating labels
LabelList = []
LabelStrings = ["Position:", "Status:", "Points:", "Currently Looking For:", "Collected Treasure:", "Thoughts:", "Time Limit:", "Starting Point:", "Treasure Selection:", "Coin - 10 Points",
                "Jewel - 20 Points", "Ruby - 30 Points", "Chest - 50 Points", "Drag and drop on landmarks", "Wishlist:"]
LabelPlacementx = [15, 15, 15, 15, 270, 470, 877, 877, 877, 930, 925, 927, 927, 876, 877]
LabelPlacementy = [540, 570, 600, 630, 540, 540, 35, 55, 106, 137, 175, 215, 255, 293, 320]
LabelSize = [12, 12, 12, 12, 12, 12, 10, 10, 10, 10, 10, 10, 10, 10, 10]
for n in range (0,15):
    LabelList.append(Label(font=('Helvetica', LabelSize[n]), text=LabelStrings[n]))
    LabelList[n].place(x=LabelPlacementx[n], y=LabelPlacementy[n])        

Images = []
ImageList = [pirateImage, coinImage, greenImage, redImage, chestImage]
ImagePlacementx = [720, 280, 310, 340, 370]
ImagePlacementy = [530, 576, 575, 575, 580]
for n in range(0,5):
    Images.append(Label(image=ImageList[n]))
    Images[n].place(x=ImagePlacementx[n], y=ImagePlacementy[n])

rbName=Label(font=('Helvetica', 18, 'underline'), text='Virtual Robot Pirate')
settings=Label(font=('Helvetica', 12, 'underline'), text='Settings')
rbName.place(x=15, y=505)
settings.place(x=877, y=13)

#Placement of canvas
canvas.place(x=10, y=10)

lightlist = []
for n in range(1,5):
    lightlist.append(Light(n))
    lightlist[n-1].CreateLight()

#Drawing line around canvas
whole=canvas.create_rectangle(2, 481, 855, 2)

R1 = Robot() # Create instance of robot class (R1)
R1.robotLoad() # Draw R1 onto screen
R1.robotMove()
R1.trapCollision(r1.x1, r1.y1, r1.x2, r1.y2, trap1)
R1.trapCollision(r1.x1, r1.y1, r1.x2, r1.y2, trap2)

window.mainloop()
