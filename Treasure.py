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
        self.vy = 5.0
        self.rXPos = 0
        self.rYPos = 0        
        self.x1 = 0.0
        self.y1 = 0.0
        self.x2 = 0.0
        self.y2 = 0.0
        self.status = "" #String to display status of robot
        self.points = 0 #Integer to display points of robot
        self.run = False #Used for when robot should run
        self.done = False #Used for when robot is done i.e. got all treasures
        

    def robotSpawn(self):
        # Create a rect object for robot.
        self.rXPos = random.randint(20, 854)
        self.rYPos = random.randint(20, 500)
        self.robot = canvas.create_rectangle(self.rXPos, self.rYPos, self.rXPos + 10, self.rYPos + 10, fill = "cyan", outline = "blue", tag = "robotTag")
        self.run = True

    def robotDraw(self):
        self.robot = canvas.create_rectangle(self.rXPos, self.rYPos, self.rXPos + 10, self.rYPos + 10, fill = "cyan", outline = "blue", tag = "robotTag")        

    def robotMove(self, treasures):
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
                self.updateInfo()
                
    def robotStop(self): #Function to stop robot by changing values
        self.run = False #Run changes to false to stop
        self.done = False #Done changes back to default
        canvas.delete("robotTag") #Deletes robot from canvas
            
    def updateInfo(self): #Function to update info about robot in GUI
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
            ResetLabels() #Run function to reset labels to default if robot not running anymore
            
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



class treasureDrag:
    def __init__(self):
        #Frame(canvas) 
        #self.window = Tk()
        #self.draw = window.geometry
        self.draw = canvas 
        
        self.draw.pack()#(expand = YES, fill = BOTH)
        self.widgets()
        #mainloop()
        
    def down(self, event):
        self.xLast = event.x # coords of where the mouse went down
        self.yLast = event.y

    def move(self, event):
        # whatever the mouse is over it will be tagged as current 
        self.draw.move(CURRENT, event.x - self.xLast, event.y - self.yLast)
        self.xLast = event.x
        self.yLast = event.y

# callback for items on canvas

    #def enter(self,event):
        #self.draw.itemconfig(CURRENT) 
    def Coin(self):
        self.coinimg = PhotoImage(file = "coin.gif")
        self.draw.create_image(700,130, image = self.coinimg, anchor = NW)

    def Green(self):
        self.greenimg = PhotoImage(file = 'greenjewel.gif')
        self.draw.create_image(700,168, image = self.greenimg, anchor = NW)

    def Red(self):
        self.redimg = PhotoImage(file = 'redjewel.gif')
        self.draw.create_image(700,208, image = self.redimg, anchor = NW)

    def Chest(self):
        self.chestimg = PhotoImage(file='chest.gif')
        self.draw.create_image(700,247, image = self.chestimg, anchor = NW)
        
        
    def widgets(self):   
        Widget.bind(self.draw,"<1>", self.down) # 1 indicates the left click on the mouse, 2 is middle and 3 is right
        Widget.bind(self.draw,"<B1-Motion>", self.move) # movement of mouse when click is held down            
              
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

class Trap:
    def __init__(self):
        self.draw = canvas 
        self.draw.pack()
        self.xpos = 0
        self.ypos = 0
        self.hit = False
        self.points = 0
        
    def spawn(self):
        self.xpos = random.randrange(20,800)
        self.ypos = random.randrange(200,400)
        
    def hit(self):
        #first check if hit is false
        #take away points from robot total points
        #show image
        self.trapImage = PhotoImage(file = "trap.gif")
        self.draw.create_image(self.xpos,self.ypos, image = self.trapImage)
        #make last treasure grey
        #flash canvas red
            
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
            
        R1 = Robot() # Create instance of robot class (R1)
        #R2 = Robot() # Create instance of robot class (R1)
        R1.robotSpawn() # Draw R1 onto screen
        #R2.robotSpawn() # Draw R1 onto screen
        
        R1.robotMove(obstacles)  # Deploy R1 movement behaviour
        #R2.robotMove(obstacles) # Deploy R1 movement behaviour  		 

MapOneLandMarks()
                     
#Creating frames to seperate controls
robotSection = Frame(bd=1, relief=SUNKEN, height=158, width=854)
robotSection.place(x=11, y=500)
collectedSection = Frame(bd=1, relief=SUNKEN, height=85, width=180)
collectedSection.place(x=275, y=565)
thoughtsSection = Frame(bd=1, relief=SUNKEN, height=85, width=220)
thoughtsSection.place(x=476, y=565)
settingSection = Frame(bd=1, relief=SUNKEN, height=480, width=175)
settingSection.place(x=872, y=11)
treasureSection = Frame(bd=1, relief=SUNKEN, height=165, width=160)
treasureSection.place(x=880, y=128)
wishlistSection = Frame(bd=1, relief=SUNKEN, height=140, width=160)
wishlistSection.place(x=880, y=344)
countdownSection = Frame(bd=1, relief=SUNKEN, height=158, width=175)
countdownSection.place(x=872, y=500) 

# creating instances of class for each treasure item. this will be called through as a command on the buttons 
treasureCoin = treasureDrag()
treasureGreen = treasureDrag()
treasureRed = treasureDrag()
treasureChest = treasureDrag()

trap1 = Trap()

# import images into a variable 
coinImage = PhotoImage(file="coin.gif")
greenImage = PhotoImage(file="greenjewel.gif")
redImage = PhotoImage(file="redjewel.gif")
chestImage = PhotoImage(file="chest.gif")

#buttons for each treasure, command calls the treasure variable and functin to draw
btnCoin = Button(window, image = coinImage, command = treasureCoin.Coin)
btnGreen = Button(window, image = greenImage, command=treasureGreen.Green)
btnRed = Button(window, image = redImage, command=treasureRed.Red)
btnChest = Button(window,image = chestImage,command= treasureChest.Chest)

#place treasure buttons in correct place outside canvas 
btnCoin.place(x=884,y=130)
btnGreen.place(x=884,y=168)
btnRed.place(x=884,y=208)
btnChest.place(x=884,y=247)

#Creating Buttons
btnStart=Button(window, text='Start', height=1, width=22, command=Start)
btnPoint1=Button(window, text='1', height=1, width=2)
btnPoint2=Button(window, text='2', height=1, width=2)
btnPoint3=Button(window, text='3', height=1, width=2)
btnPoint4=Button(window, text='4', height=1, width=2)
btnPoint5=Button(window, text='5', height=1, width=2)
btnPoint6=Button(window, text='6', height=1, width=2)

#Places buttons in correct positions
btnStart.place(x=878, y=505)
btnPoint1.place(x=877, y=77)
btnPoint2.place(x=902, y=77)
btnPoint3.place(x=927, y=77)
btnPoint4.place(x=952, y=77)
btnPoint5.place(x=977, y=77)
btnPoint6.place(x=1002, y=77)

#Creating robot1 labels
rbName=Label(font=('Helvetica', 18, 'underline'), text='Virtual Robot Pirate')
rbPosition=Label(font=('Helvetica', 12), text='Position:')
rbStatus=Label(font=('Helvetica', 12), text='Status:')
rbPoints=Label(font=('Helvetica', 12), text='Points:')
rbLookingFor=Label(font=('Helvetica', 12), text='Currently Looking For:')
rbCollected=Label(font=('Helvetica', 12), text='Collected Treasure:')
rbThoughts=Label(font=('Helvetica', 12), text='Thoughts:')

#Places robot1 labels in correct positions
rbName.place(x=15, y=505)
rbPosition.place(x=15, y=540)
rbStatus.place(x=15, y=570)
rbPoints.place(x=15, y=600)
rbLookingFor.place(x=15, y=630)
rbCollected.place(x=270, y=540)
rbThoughts.place(x=470, y=540)

#Pirate Image
pirateImage = PhotoImage(file="pirate.gif")
pirateImageLabel=Label(image=pirateImage)
pirateImageLabel.place(x=720, y=530)

#Creating Settings labels
settings=Label(font=('Helvetica', 12, 'underline'), text='Settings')
timelimit=Label(font=('Helvetica', 10), text='Time Limit:')
starting=Label(font=('Helvetica', 10), text='Starting Point:')
treasureselection=Label(font=('Helvetica', 10), text='Treasure Selection:')
coin=Label(font=('Helvetica', 10), text='Coin - 10 Points')
greenjewel=Label(font=('Helvetica', 10), text='Jewel - 20 Points')
redjewel=Label(font=('Helvetica', 10), text='Ruby - 30 Points')
chest=Label(font=('Helvetica', 10), text='Chest - 50 Points')
instruction=Label(font=('Helvetica', 10), text='Drag and drop on landmarks')
wishlist=Label(font=('Helvetica', 10), text='Wishlist:')

#Places settings labels in correct positions
settings.place(x=877, y=13)
timelimit.place(x=877, y=35)
starting.place(x=877, y=55)
treasureselection.place(x=877, y=106)
coin.place(x=930, y=137)
greenjewel.place(x=925, y=175)
redjewel.place(x=927, y=215)
chest.place(x=927, y=255)
instruction.place(x=876, y=293)
wishlist.place(x=877, y=320)

#Placement of canvas
canvas.place(x=10, y=10)

#Creating light objects
light1 = Light(1)
light2 = Light(2)
light3 = Light(3)
light4 = Light(4)

#Drawing lights onto canvas using function in light class
light1.CreateLight()
light2.CreateLight()
light3.CreateLight()
light4.CreateLight()

#Drawing line around canvas
whole=canvas.create_rectangle(2, 481, 855, 2)

window.mainloop()
