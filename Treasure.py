from Tkinter import *
#from PIL import Image, ImageTk
import ttk
import random
import time

window = Tk()
canvas = Canvas(window, width=854, height=480, bg="#3796da")
canvas.pack()

intPlay = 0

#Creates window and centers to any screen
window.geometry('{}x{}'. format(1060, 670)) #Setting size of window
window.withdraw() #Hide window to stop showing in wrong position
window.update_idletasks() #Request screen size from system
x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / 2 #Calculate screen width
y = ((window.winfo_screenheight() - window.winfo_reqheight()) / 2) - 70 #Calculate screen height
window.geometry("+%d+%d" % (x, y)) #Change position of window
window.title('Sloths - Virtual Robot Treasure Hunt') #Adds name to window
window.resizable(width=FALSE, height=FALSE) #Disabled resizable function of window
window.deiconify() #Redraw window in correct position

#Importing images to use through out program
coinImage = PhotoImage(file="coin.gif")
greenImage = PhotoImage(file="greenjewel.gif")
redImage = PhotoImage(file="redjewel.gif")
chestImage = PhotoImage(file="chest.gif")
pirateImage = PhotoImage(file="pirate.gif")
coinGImage = PhotoImage(file="coin-grey.gif")
jewelGImage = PhotoImage(file="jewel-grey.gif")
chestGImage = PhotoImage(file="chest-grey.gif")

ClockG = PhotoImage(file="clock-grey.gif")
Clock1 = PhotoImage(file="1.gif")
Clock15 = PhotoImage(file="1.5.gif")
Clock2 = PhotoImage(file="2.gif")
Clock25 = PhotoImage(file="2.5.gif")
Clock3 = PhotoImage(file="3.gif")
Clock35 = PhotoImage(file="3.5.gif")
Clock4 = PhotoImage(file="4.gif")
Clock45 = PhotoImage(file="4.5.gif")

#Importing png using PIL
#flash = Image.open("flash.png")
#flashImage = ImageTk.PhotoImage(flash)

class landmark:                                   # Landmark class being created
    def __init__(self, x1, y1, x2, y2):             # this sets out the layout of how all future objects will be set in order to be created
        self.x1 = x1                                # whatever the objects name.x1 or x2 or y1 or y2, store the value in x1, which then places it in the user interface
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.colour  = "#e7df63"                      # the background colour for all landmarks is set here to green in the user interface
        self.outline = "black"                      #   the outline colour of all landmarks is set to black in the user interface
        self.treasure = False                       #   setting the variable with the value of 'false'
        self.treasureID = ""                        #   creating treasure ID for robot 
        
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
        self.points = 0 #Integer to display points of robot
        self.run = False #Used for when robot should run
        self.done = False #Used for when robot is done i.e. got all treasures
        self.shipSprite = PhotoImage(file = "ship.gif")

    def setSpawn(self, xpos, ypos): #Function to set spawn variables
        self.rXPos = xpos #Setting xpos
        self.rYPos= ypos #Setting ypos
        
    def robotLoad(self):
        for o in obstacles:            
            ox1, oy1, ox2, oy2 = canvas.coords(o.lndmrk)

            if (self.rXPos > ox1 - 10.0 and self.rXPos < ox2 + 10.0) and (self.rYPos > oy1 - 10.0 and self.rYPos < oy2 + 10.0):
                self.robotLoad()

            else:
                self.robot = canvas.create_rectangle(self.rXPos, self.rYPos, self.rXPos + 10.0, self.rYPos + 10.0, fill = "blue")
                self.run = True    

    def trapCollision(self, x1, y1, x2, y2, trap):        
        if (x2 > trap.xpos and x1 < trap.xpos + 30.0) and (y2 > trap.ypos and y1 < trap.ypos + 30.0):
            if trap.hit == False:
                trap.collision()

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

    def treasureTrack(self):
        c = -1
        if self.run == True:
            if self.done == False:                

                for l in locationlist:

                    while l.treasure == True:

                        x1, y1, x2, y2 = canvas.coords(self.robot)
                        
                        self.bypassLandmark(x1, y1, x2, y2)
                        self.trapCollision(x1, y1, x2, y2, traps[0])
                        self.trapCollision(x1, y1, x2, y2, traps[1])

                        lx1, ly1, lx2, ly2 = canvas.coords(l.lndmrk)
                            
                        if (x2 < lx1 - 20.0) and (y2 < ly1 - 20.0): # Approaching from top left.
                            self.vx = 10.0
                            self.vy = 5.0
                        if (x2 < lx1 - 20.0) and (y1 > ly2 + 20.0): # Approaching from bottom left.
                            self.vx = 10.0
                            self.vy = -5.0
                        if (x1 > lx2 + 20.0) and (y2 < ly1 - 20.0): # Approaching from top right.
                            self.vx = -10.0
                            self.vy = 5.0
                        if (x1 > lx2 + 20.0) and (y1 > ly2 + 20.0): # Approaching from bottom right.
                            self.vx = -10.0
                            self.vy = -5.0

                        if (x2 < lx1 - 20.0) and ((y2 > ly1 - 20.0) and (y1 < ly2 + 20.0)):
                            self.vx = 10.0
                            self.vy = 0.0
                        if (x1 > lx2 + 20.0) and ((y2 > ly1 - 20.0) and (y1 < ly2 + 20.0)):
                            self.vx = -10.0
                            self.vy = 0.0
                        if (y2 < ly1 - 20.0) and ((x2 > lx1 - 20.0) and (x1 < lx2 + 20.0)):
                            self.vx = 0.0
                            self.vy = 5.0
                        if (y1 > ly2 + 20.0) and ((x2 > lx1 - 20.0) and (x1 < lx2 + 20.0)):
                            self.vx = 0.0
                            self.vy = -5.0

                        if ((x2 > lx1 - 20.0) and (x1 < lx2 + 20.0)) and ((y2 > ly1 - 20.0) and (y1 < ly2 + 20.0)):
                            print l
                            print "treasure collected"
                            l.treasure = False
                            c = c + 1
                            canvas.delete(treasurelist[c].location)
                            CollectedList.append(Label(image=l.treasureID))
                            CollectedList[c].place(x=CollectedImagex[c], y=CollectedImagey[c])
                            self.points = self.points + treasurelist[c].points
                            InfoLabels[2].config(text=self.points)
                            for n in range (0,2):
                                traps[n].points = treasurelist[c].points
                                traps[n].previous = l.treasureID
                                traps[n].colpos = c

                        self.rXPos += self.vx
                        self.rYPos += self.vy            

                        canvas.coords(self.robot, x1 + self.vx, y1 + self.vy, x2 + self.vx, y2 + self.vy)
                        
                        InfoLabels[0].config(text="x:" + str(int(x1)) + " y:" + str(int(y1)))
                        canvas.update()                
                        time.sleep(0.1)

    # def lightResponse(self):
         
class Countdown:
    def __init__(self, label):
        self.second = 0
        self.minute = 0
        self.time = ""
        self.totalTime = 0
        self.ticks = 0
        self.done = False
        self.label = label
         
    def getTime(self):
        time = E.get()
        #split the time string input
        #set the minutes as an int
        self.minute = int(time[0:2])
        #set the seconds as an int
        self.second = int(time[3:5])
        self.second = self.second + 1
        # for the clock countdown calculations
        self.ticks = (self.second + (self.minute * 60)) - 1
        self.totalTime = (self.second + (self.minute * 60)) - 1   
 
    def Done(self): #Change to done if robot is done
        #used so that the countdown still displays time
        self.done = True
         
    def Count(self):
        # when the countdown has seven eighths of the totalTime to go
        sevenEighths = self.totalTime * 0.875
        # when the countdown has three quarters of the totalTime left to go
        threeq = self.totalTime * 0.75
        # when the countdown has five eighths of the totalTime to go
        fiveEighths = self.totalTime * 0.625
        # when the countdown is halfway
        half = self.totalTime * 0.5
        # when the countdown has three eighths of the totalTime to go
        threeEighths = self.totalTime * 0.375
        # when the countdown has one quarter of the totalTime left to go
        oneq = self.totalTime * 0.25
        # when the countdown has one eighths of the totalTime to go
        oneEighth = self.totalTime * 0.125
        
        global intPlay
        if intPlay == 0:
            self.done = True
        # condition - if the program is running
        elif self.done == False:
            self.ticks = self.ticks - 1
            # seconds decrease by 1
            self.second = self.second - 1
            if self.second == 0:
                # once the countdown reaches 60 seconds, the minutes decreases and the seconds are set back to 0 to repeat process
                self.minute = self.minute - 1
                self.second = 59
                if self.minute < 0:
                    self.done = True
                    self.second = 0
                    self.minute = 0
                    ChangeThought(7) #Displays text from thoughts
            
            #Generate 4 random numbers between 1 - 3 for lights
            # lights change every 5 seconds
            if self.second % 5 == 0:
                lightlist[0].ChangeLight()
                lightlist[1].ChangeLight()
                lightlist[2].ChangeLight()
                lightlist[3].ChangeLight()
 
            # formatting of timer display mm:ss
            if self.minute >= 10:
                if self.second >= 10:
                    # e.g. 12:34
                    self.time = str(self.minute) + ":" + str(self.second)
                else:
                    # e.g. 12:03
                    self.time = str(self.minute) + ":0" + str(self.second)
            else:
                if self.minute < 10:
                    if self.second >= 10:
                        # e.g. 01:23
                        self.time = "0" + str(self.minute) + ":" + str(self.second)
                    else:
                        # e.g. 01:02
                        self.time = "0" + str(self.minute) + ":0" + str(self.second)
        # executing the timer display as a string so it can display as a label
        exec str(self.label.config(text=(self.time)))
        # 1000 ticks == 1 second delay and continues the Count function
        self.label.after(1000, self.Count)

        # when the robot has found the treasures the timer is stopped, and the time the robot found the treasures in is displayed
        if self.done == True:
            exec str(self.label.config(text=(self.time)))
            
        #countdown image change
        if (float(sevenEighths) < self.ticks <= self.totalTime):
            # display first clock image
            clock.config(image=Clock1)
        elif (float(threeq) < self.ticks <= float(sevenEighths)):
            # display second clock image
            clock.config(image=Clock45)
        elif (float(fiveEighths) < self.ticks <= float(threeq)):
            # display third clock image
            clock.config(image=Clock4)
        elif (float(half) < self.ticks <= float(fiveEighths)):
            # display fourth clock image
            clock.config(image=Clock35)
        elif (float(threeEighths) < self.ticks <= float(half)):
            # display fifth clock image
            clock.config(image=Clock3)
        elif (float(oneq) < self.ticks <= float(threeEighths)):
            # display sixth clock image
            clock.config(image=Clock25)
        elif (float(oneEighth) < self.ticks <= float(oneq)):
            # display seventh clock image
            clock.config(image=Clock2)
        elif (0 < self.ticks <= int(oneEighth)):
            # display eighth clock image
            clock.config(image=Clock15)
        else:
            # display greyed out clock
            clock.config(image=ClockG)
            
#Class for lights
class Light():
    def __init__(self, number):
        self.width = 854 #width of canvas
        self.height = 480 #height of canvas
        self.sectionWidth = 213.5 #width of one section (1/4 of whole width)
        self.number = number #number of section
        self.colour = "" #string to hold colour of section

    def CreateLight(self): #Function to create the lights for GUI
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
        
class image(object): # base class 
    def __init__(self):
        self.x = 0 # coords used for both treasure & trap once classed is called 
        self.y = 0
        self.location = "" # location set as empty string for trap to use
        self.draw = canvas
        self.draw.pack() # pack draw anywhere on canvas as coords will decide where to put it 
        self.widgets() # call mouse click and drag instantly 
        
    def down(self, event):
        self.xLast = event.x # coords of where the mouse went down
        self.yLast = event.y # event of each coords allows mouse to interact 

    def move(self, event):
        # CURRENT use to tag any object under the mouse, and only move one object at a time 
        self.draw.move(CURRENT, event.x - self.xLast, event.y - self.yLast) # use event of x and y on what object is present to keep it under the mouse once dragged 
        self.xLast = event.x # recall event coords when moving object with mouse 
        self.yLast = event.y
        
    def widgets(self):
        #tag will be binded with movement of mouse and click of mouse, so it is looking for 'treasure' tags and no other 
        self.draw.tag_bind('treasure',"<1>", self.down) # 1 indicates the left click on the mouse, 2 is middle and 3 is right
        self.draw.tag_bind('treasure',"<B1-Motion>", self.move) # movement of mouse when click is held down  
        
    def spawn(self, x, y, image, tag):
        self.image = PhotoImage(file=image) # allows images to be added once file given 
        self.x = x # coords for image once uploaded, both x & y 
        self.y = y
        self.tag= tag # tag in place to separate the treasure from trap when using mouse 
        self.location = self.draw.create_image(self.x, self.y,image = self.image,tag =self.tag) # able to create an image given the correct arugments  
        
wishlist = [] #Creating empty wishlist to be filled when selecting treasure
wishlistx = [885, 925, 965, 1005] #X position of images to be placed
wishlisty = [346, 346, 346, 346] #Y position of images to be placed
treasurelist = [] #Creating empty treasure list to be filled with sorted treasure items
locationlist = [] #Creating emtpy location list of landmarks that contain treasure in sorted order

def SortTreasure(treasurelist): #Function to sort treasure list (using bubble sort)
    for i in range(len(treasurelist)-1, 0, -1): #Loop counting down from last item in list
        for n in range(i): #Nested loop
            if treasurelist[n].points < treasurelist[n+1].points: #If current item is less then next item
                temp = treasurelist[n] #Put current item in temp
                treasurelist[n] = treasurelist[n+1] #Swap next item with current item
                treasurelist[n+1] = temp #Put current item at place of next item

class treasure(image):
    def __init__(self):
        image.__init__(self) # use the init from image class to create images, inheritance 
        self.points = 0 # set points to default '0', it will change once each treasure is populated in wishlist 

    def wishList(self, image):
        if image == "coin.gif":
            TreasureButtons[0].config(state="disabled") # disbale each treasure button once pressed, index indicates fist item'coin' 
            i = coinImage # used to iterate thrhough list so it can be sorted in order, highest to lowest, once collected 
            self.points = 10 # giving treasure a point value 
        elif image == "greenjewel.gif":
            TreasureButtons[1].config(state="disabled")# disbale each treasure button once pressed, index indicates fist item'green jewel' 
            i = greenImage# used to iterate thrhough list so it can be sorted in order, highest to lowest, once collected 
            self.points = 20 # giving treasure a point value
        elif image == "redjewel.gif":
            TreasureButtons[2].config(state="disabled")# disbale each treasure button once pressed, index indicates fist item'red jewel' 
            i = redImage# used to iterate thrhough list so it can be sorted in order, highest to lowest, once collected 
            self.points = 30 # giving treasure a point value
        elif image == "chest.gif":
            TreasureButtons[3].config(state="disabled")# disbale each treasure button once pressed, index indicates fist item'chest' 
            i = chestImage# used to iterate thrhough list so it can be sorted in order, highest to lowest, once collected 
            self.points = 50 # giving treasure a point value

        image.replace(".gif", "") # replace treasure in wishlist with correct sorted treasure, highest to lowest 
        wishlist.append(image) # append the wishlist with images of treasures, using the base class attributes 
        placement = wishlist.index(image) #Get index of wishlist item

        if placement == 0: #Check for placement of wishlist item 
            lbl1 = Label(image=i) #Create image label
            lbl1.place(x=wishlistx[0], y=wishlisty[0]) #Place image label in position 1
        elif placement == 1: #Check for placement of wishlist item 
            lbl2 = Label(image=i) #Create image label
            lbl2.place(x=wishlistx[1], y=wishlisty[1]) #Place image label in position 2
        elif placement == 2: #Check for placement of wishlist item 
            lbl3 = Label(image=i) #Create image label
            lbl3.place(x=wishlistx[2], y=wishlisty[2]) #Place image label in position 3
        elif placement == 3: #Check for placement of wishlist item 
            lbl4 = Label(image=i) #Create image label
            lbl4.place(x=wishlistx[3], y=wishlisty[3]) #Place image label in position 4

        treasurelist.append(self) #Add treasure object to list
        
    def create(self,x,y,image,tag): # call the base class to use its attributes 
        self.spawn(x,y,image,tag) # using spawn function from image class 
        self.wishList(image) # the wishlist will use the image class for its functions 

    def locate(self): #Function to get landmark treasure is in
        pos = canvas.coords(self.location) #Get coords of treasure object
        xpos = pos[0] #Seperate x coords
        ypos = pos[1] #Seperate y coords
        i = 0 #Start i at 0
        for o in obstacles: #Loop through landmark objects
            i = i + 1 #Increment i
            ox1, oy1, ox2, oy2 = canvas.coords(o.lndmrk) #Get coords of landmark object
            if (xpos > ox1 and xpos < ox2) and (ypos > oy1 and ypos < oy2): #Check if treasure object is within landmark object
                lnd = obstacles[i-1] #Get landmark object
                locationlist.append(lnd) #Add landmark object to list
                locationlist[-1].treasure = True #Landmakr has treasure item
                if self.points == 10: #Check what treasure the landmark has in it
                    locationlist[-1].treasureID = coinImage #Change treasureID to coin
                    #ChangeThought(4) #Displays text from thoughts nr.4
                elif self.points == 20: #Check what treasure the landmark has in it
                    locationlist[-1].treasureID = greenImage #Change treasureID to green jewel
                    #ChangeThought(5) #Displays text from thoughts nr.5
                elif self.points == 30: #Check what treasure the landmark has in it
                    locationlist[-1].treasureID = redImage #Change treasureID to red jewel
                    #ChangeThought(8) #Displays text from thoughts nr.8
                elif self.points == 50: #Check what treasure the landmark has in it
                    locationlist[-1].treasureID = chestImage #Change treasureID to chest
                    #ChangeThought(6) #Displays text from thoughts nr.6
          
class Trap(image): 
    def __init__(self):
        image.__init__(self) #Use the init from image class to create images, inheritance 
        self.xpos = 0 #Initilise xpos
        self.ypos = 0 #Initilise ypos
        self.hit = False #Initilise hit as false till trap has been hit
        self.points = 0 #Set points as zero
        self.previous = "" #Holds previous treasure collected
        self.colpos = 0 #Holds position of collected image picture
        
    def create(self): #Creates the x,y position of trap to check in 
        self.xpos = random.randint(25,829) #Random xpos within canvas
        self.ypos = random.randint(25,455) #Random ypos within canvas
        for o in obstacles: #Loop through landmarks        
            ox1, oy1, ox2, oy2 = canvas.coords(o.lndmrk) #Get landmark coords
            if (self.xpos > ox1 - 35.0 and self.xpos < ox2 + 35.0) and (self.ypos > oy1 - 35.0 and self.ypos < oy2 + 35.0): #Check if within landmark
                self.create() #Recurrsive function to retry spawn
            else: 
                self.spawn(self.xpos, self.ypos, "trap.gif",'trap') #Create trap, will not be in final program
                      
    def collision(self): #Function called when robot within xpos and ypos of trap
        ChangeThought(4) #Displays text from thoughts nr.4
        R1.points = R1.points - self.points #Deducts points of last collected treasure
        InfoLabels[2].config(text=R1.points) #Displays updated points to user
        if self.previous == coinImage:
            coinGreyImage = (Label(image=coinGImage))
            coinGreyImage.place(x=CollectedImagex[self.colpos], y=CollectedImagey[self.colpos])
        elif self.previous == chestImage:
            chestGreyImage = (Label(image=chestGImage))
            chestGreyImage.place(x=CollectedImagex[self.colpos], y=CollectedImagey[self.colpos])
        elif self.previous == greenImage:
            greenGreyImage =(Label(image=jewelGImage))
            greenGreyImage.place(x=CollectedImagex[self.colpos], y=CollectedImagey[self.colpos])
        elif self.previous == redImage:
            redGreyImage = (Label(image=jewelGImage))
            redGreyImage.place(x=CollectedImagex[self.colpos], y=CollectedImagey[self.colpos])
        self.spawn(self.xpos, self.ypos, "trap.gif",'trap') #Creates trap image (unhides)
        #f=canvas.create_image(429,263,image=flashImage, tag="flash")
        self.hit = True #Changes hit to true so robot will not hit again
                
def Start():
    Disable()
    ChangeThought(2) #Displays text from thoughts nr.2
    global intPlay
    intPlay += 1
    if intPlay <= 1:
        #global main
        main = Countdown(countdown)
        main.getTime()
        main.Count()
    SortTreasure(treasurelist)
    print treasurelist
    for n in range (0, len(treasurelist)):
        treasurelist[n].locate()
    print locationlist
    
    R1.robotLoad() # Draw R1 onto screen
    R1.treasureTrack()

def Disable():
    E.config(state=DISABLED)
    for n in range (0,7):
        ButtonList[n].config(state=DISABLED)
    for n in range (0,4):
        TreasureButtons[n].config(state=DISABLED)
    

MapOneLandMarks()
        
traps = []
for n in range(0,2):
    traps.append(Trap())
    traps[n].create()

treasureitems = [] # empty list to populate with treasure 
treasurex = [840,835] # create a fixed x position for treasure 
treasurey = [138, 178, 217, 254] # give different y position for treasure 

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

TreasureButtons = [] # creating empty list to be popualted by treasure image for buttons 
TreasureButtonImage = [coinImage, greenImage, redImage, chestImage] #  # images for each treasure button in a list

#lambda is an an anonymous function without defining specific attributes
# it will call the treasure index first [0] and then create it with the index for each treasure x and & y coords,
#once down, the image is loaded and tag is placed 
TreasureButtonCommand = [lambda: treasureitems[0].create(treasurex[0], treasurey[0], "coin.gif",'treasure'),
                         lambda: treasureitems[1].create(treasurex[0], treasurey[1], "greenjewel.gif",'treasure'),
                         lambda: treasureitems[2].create(treasurex[0], treasurey[2], "redjewel.gif",'treasure'),
                         lambda: treasureitems[3].create(treasurex[1], treasurey[3], "chest.gif",'treasure')]

TreasureButtonPlacementy = [130, 168, 208, 247] # placement for each buttons on window 
for n in range(0,4): # iterates through each treasure item 0-3 (4 objects)
    # update treasure button list with button function, called the window to place it, the image of the treasure, and the command to execute the button,
    #and then placement coords for each button
    TreasureButtons.append(Button(window, image =TreasureButtonImage[n], command=TreasureButtonCommand[n])) 
    TreasureButtons[n].place(x=884, y=TreasureButtonPlacementy[n])
    
#These functions below are linked to the buttons for starting position on the GUI, they load up different positions
# for the robot to spawn in.
def FirstButton():
    R1.setSpawn(300, 50)
    ChangeThought(1) #Displays text from thoughts nr.1
def SecondButton():
    R1.setSpawn(60, 130)
    ChangeThought(1) #Displays text from thoughts nr.1
def ThirdButton():
    R1.setSpawn(450, 130)
    ChangeThought(1) #Displays text from thoughts nr.1
def FourthButton():
    R1.setSpawn(200, 350)
    ChangeThought(1) #Displays text from thoughts nr.1
def FithButton():
    R1.setSpawn(700, 150)
    ChangeThought(1) #Displays text from thoughts nr.1
def SixthButton():
    R1.setSpawn(600, 410)
    ChangeThought(1) #Displays text from thoughts nr.1

ButtonList = []
ButtonString = ["Start", "1", "2", "3", "4", "5", "6"]
ButtonPlacementx = [878, 877, 902, 927, 952, 977, 1002]
ButtonPlacementy = [505, 77, 77, 77, 77, 77, 77]
ButtonWidth = [22, 2, 2, 2, 2, 2, 2]
ButtonCommand = [Start, FirstButton, SecondButton, ThirdButton, FourthButton, FithButton, SixthButton]
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

InfoLabels = []
InfoLabelString = ["", "", "0"]
InfoPlacementx = [80, 66, 66]
InfoPlacementy = [540, 570, 600]
for n in range (0, 3):
    InfoLabels.append(Label(font=('Helvetica', 12), text=InfoLabelString[n]))
    InfoLabels[n].place(x=InfoPlacementx[n], y=InfoPlacementy[n])

pirateLabel = Label(image=pirateImage)
pirateLabel.place(x=720, y=530)
clock=Label(image=ClockG)
clock.place(x=916, y=534)

CollectedList = []
CollectedImage = [coinImage, greenImage, redImage, chestImage]
CollectedImagex = [280, 315, 345, 375]
CollectedImagey = [575, 575, 575, 575]

rbName=Label(font=('Helvetica', 18, 'underline'), text='Virtual Robot Pirate')
settings=Label(font=('Helvetica', 12, 'underline'), text='Settings')
rbName.place(x=15, y=505)
settings.place(x=877, y=13)

#Placement of canvas
canvas.place(x=10, y=10)

#Creates countdown label
countdown=Label(font=('Helvetica', 20), text='00:00')
countdown.place(x=922, y=620)

#create entry for countdown
E = Entry(font=('Helvetica', 10), width = 12)
E.insert(0, "01:00")
#placement of entry
E.place(x= 947,y= 37)

lightlist = []
for n in range(1,5):
    lightlist.append(Light(n))
    lightlist[n-1].CreateLight()
    
#create thoughts label
thoughts = ("Change settings to start!", "Click Start!", "Ahoy, Matey!", "Batten down the hatches!",
            "Aaaarrrrgggghhhh", "Me Booty!", "Heave Ho!", "Avast ye, time up!", "Shiver me timbers!")
thoughtLabel = Label(font=("Helvetica", 12), text=thoughts[0]) #Displays text from thoughts nr.0

thoughtLabel.place(x=480, y=567)

def ChangeThought(number):
    thoughtLabel.config(text=thoughts[number])

#Drawing line around canvas
whole=canvas.create_rectangle(2, 481, 855, 2)

R1 = Robot() # Create instance of robot class (R1)
R1.setSpawn(300, 50)

window.mainloop()
