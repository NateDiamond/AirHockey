#airHockey.py
#Nathaniel Diamond
#Started 12/14/16

from game2d import *
from kivy.core.audio import SoundLoader
import random

GAME_WIDTH = 1000
GAME_HEIGHT = 500

A_INC = 3

STARTING_ANIMATION_SPEED = .075
STARTING_ANIMATION_COLORS = [colormodel.RED,colormodel.ORANGE,colormodel.YELLOW,colormodel.GREEN,colormodel.BLUE,colormodel.MAGENTA]
STARTING_ANIMATION_NUMBER = len(STARTING_ANIMATION_COLORS)

STATE_INACTIVE = 0
STATE_COUNTDOWN = 1
STATE_SELECT = 2
STATE_FADE = 3

PUCK_DIM = 50

SOUND_NAME_LIST = ["Boom.wav","Cycles.wav","Namaste.wav","Nip.wav",
                   "RubixCube.wav","SeductressDubstep.wav","Sk8board.wav",
                   "TechTalk.wav", "U-ah.wav"]
SOUND_LIST = []
for name in SOUND_NAME_LIST:
     SOUND_LIST.append(SoundLoader.load(name))
     
SELECT_SOUND = SoundLoader.load("button-3.wav")
GAME_START_SOUND = SoundLoader.load("Cheering 3-SoundBible.com-1680253418.wav")
     
class AirHockey(GameApp):
     """ Primary controller for the AirHockey App
     
     Attributes:
     **view
     **input
     _startingClock
     _state
     _songsPlayed
     _song
     _alpha
     _inc
     _keyPressed
     _mousePressed
     _puckSelected
     _selectLabels
     _selectSound
     _selectBack
     _game
     _fadeClock
     _aStart
     _countdownClock"""
     
     
     def start(self):
          self._song = SOUND_LIST[0]
          self._song.play()
          self._songsPlayed = []
          state = STATE_INACTIVE
          keyPressed = False
          mousePressed = False
          self._startingClock = 0
          self._state = STATE_INACTIVE
          self._alpha = 255
          A_INC = 3
          self._inc = False
          
          self._label1 = GLabel(x = GAME_WIDTH/2.0 + 5,y = 2*GAME_HEIGHT/3.0 - 5,text = "Air Hockey", font_size = 170, font_name = "Justo St.ttf",
                      linecolor = colormodel.RGB(255,215,0),fillcolor = colormodel.RGB(0,0,0,0))
          self._label2 = GLabel(x = GAME_WIDTH/2.0,y = 2*GAME_HEIGHT/3.0,text = "Air Hockey", font_size = 170,
                      font_name = "Justo St.ttf", linecolor = colormodel.WHITE,fillcolor = colormodel.RGB(0,0,0,0))
          self._label3 = GLabel(x = GAME_WIDTH/2.0,y = GAME_HEIGHT/3.0 + 10,text = "Press anywhere to play", font_size = 40, font_name = "ComicSans.ttf",
                      linecolor = colormodel.RGB(255,255,255),fillcolor = colormodel.RGB(0,0,0,0))
          self._label4 = GLabel(x = GAME_WIDTH/2.0 + 2,y = GAME_HEIGHT/3.0 + 12,text = "Press anywhere to play", font_size = 40, font_name = "ComicSans.ttf",
                    linecolor = colormodel.RGB(255,215,0),fillcolor = colormodel.RGB(0,0,0,0))
          

          
          self._keyPressed = False
          self._mousePressed = False
          
     def update(self, dt):
          self._updateSound()
          self._determineState()
          
          if self._state == STATE_INACTIVE or self._state == STATE_SELECT:
               self._updateStartingClock(dt)
          
          if self._state == STATE_SELECT:
               if self.input.is_key_down('right') and not self._keyPressed:
                    self._puckSelected = (self._puckSelected + 1) % 3
                    SELECT_SOUND.play()
                    
               elif self.input.is_key_down('left') and not self._keyPressed:
                    self._puckSelected = (self._puckSelected + 2) % 3
                    SELECT_SOUND.play()
          
          if self._state == STATE_FADE:
               self._fadeClock += dt
                    
          #if self._state == STATE_COUNTDOWN:
               
          self._keyPressed = self.input.key_count > 0
          self._mousePressed = self.input.touch is not None
               
     def draw(self):
          if self._state == STATE_INACTIVE:
               self._startingAnimation()
               
          if self._state == STATE_SELECT:
               self._selectScreen(1)
               
          if self._state == STATE_FADE:
               self._drawTable()
               background = GRectangle(x = GAME_WIDTH/2.0, y = GAME_HEIGHT/2.0, width = GAME_WIDTH,
                          height = GAME_HEIGHT, fillcolor = colormodel.RGB(255,255,255,int((1 - self._fadeClock/5.0)*255)))
               background.draw(self.view)
               self._selectScreen(1 - self._fadeClock/5.0)
               
          if self._state == STATE_COUNTDOWN:
               self._drawTable()
                      
     def _updateStartingClock(self, dt):
          self._startingClock += dt
          
     def _startingAnimation(self):
          GRectangle(x = GAME_WIDTH/2.0, y = GAME_HEIGHT/2.0, width = GAME_WIDTH,
                          height = GAME_HEIGHT, fillcolor = colormodel.RGB(10,10,10,230)).draw(self.view)
          phase = int(self._startingClock*1/STARTING_ANIMATION_SPEED)
          columns = 2 * STARTING_ANIMATION_NUMBER
          rows = STARTING_ANIMATION_NUMBER
          
          for r in range(rows):
               for c in range(columns):
                    x = 3*PUCK_DIM/4.0 + (1.0*(GAME_WIDTH))/columns * c
                    y = GAME_HEIGHT - (3*PUCK_DIM/4.0 + (1.0 * (GAME_HEIGHT))/rows * r)
                    GEllipse(x = x, y = y, width = PUCK_DIM, height = PUCK_DIM,
                             fillcolor = STARTING_ANIMATION_COLORS[(r - phase)%STARTING_ANIMATION_NUMBER]).draw(self.view)
                    
          if self._inc:
               self._alpha += A_INC
               if self._alpha >= 255 - A_INC:
                    self._inc = False
          else:
               self._alpha -= A_INC
               if self._alpha <= A_INC:
                    self._inc = True
               
          self._label3.linecolor = colormodel.RGB(255,255,255,self._alpha)
          self._label4.linecolor = colormodel.RGB(255,215,0,self._alpha)
          
          self._label1.draw(self.view); self._label2.draw(self.view)
          self._label4.draw(self.view); self._label3.draw(self.view)
          
     def _initSelect(self):
          self._puckSelected = 0
          self._selectLabels = []
          
          self._startingClock = 0
          self._alpha = 255
          A_INC = 1
          self._inc = False
          
          for i in range(3):
               red = 1
               green = 1
               if i == 2:
                    green = 0
               if i == 0:
                    red = 0
               #self._selectPucks.append...
               #GEllipse(x = GAME_WIDTH/4.0 * (i+1), y = GAME_HEIGHT/2.0, width = PUCK_DIM,
                                 #height = PUCK_DIM, fillcolor = colormodel.RGB(red*190,green*190,0))
               #circle.draw(self.view)
               #circle = GEllipse(x = GAME_WIDTH/4.0 * (i+1), y = GAME_HEIGHT/2.0, width = PUCK_DIM - 10,
                                 #height = PUCK_DIM - 10, fillcolor = colormodel.RGB(red*210,green*210,0))
               #circle.draw(self.view)
               size = 60
               if i == 0:
                    text = "EASY"
               elif i == 1:
                    text = "MEDIUM"
               else:
                    text = "HARD"
               self._selectLabels.append(GLabel(x= GAME_WIDTH/4.0 * (i+1), y = GAME_HEIGHT/2.0 + 1.5*size, text = text,
                              font_size = size, font_name = 'Justo St.ttf',linecolor = colormodel.RGB(red*255,green*205,0),
                              fillcolor = colormodel.RGB(255,255,255,0)))
               
          self._selectLabels.append(GLabel(x = GAME_WIDTH/2.0 + 3, y = 3*GAME_HEIGHT/16.0, text = "Select Difficulty",
                                           font_size = 40, font_name = "ComicSansBold.ttf", linecolor = colormodel.RGB(30,90,220),
                                           fillcolor = colormodel.RGB(0,0,0,0)))
          self._selectLabels.append(GEllipse(x = 3*GAME_WIDTH/16.0 + 15,y=3*GAME_HEIGHT/16.0 + 1.5,width = GAME_WIDTH/4.0, height = 5,
                                             fillcolor = colormodel.RGB(30,90,220)))
          self._selectLabels.append(GEllipse(x = 3*GAME_WIDTH/16.0,y=3*GAME_HEIGHT/16.0,width = GAME_WIDTH/4.0, height = 5,
                                             fillcolor = colormodel.RGB(40,120,255)))
          self._selectLabels.append(GEllipse(x = 13*GAME_WIDTH/16.0 + 15,y=3*GAME_HEIGHT/16.0 + 1.5,width = GAME_WIDTH/4.0, height = 5,
                                             fillcolor = colormodel.RGB(30,90,220)))
          self._selectLabels.append(GEllipse(x = 13*GAME_WIDTH/16.0,y=3*GAME_HEIGHT/16.0,width = GAME_WIDTH/4.0, height = 5,
                                             fillcolor = colormodel.RGB(40,120,255)))
          self._selectLabels.append(GLabel(x = GAME_WIDTH/2.0, y = 3*GAME_HEIGHT/16.0, text = "Select Difficulty",
                                           font_size = 40, font_name = 'ComicSansBold.ttf', linecolor = colormodel.RGB(40,120,255),
                                           fillcolor = colormodel.RGB(255,255,255,0)))
          
          self._selectBack = GImage(source = 'arena1.jpg', x = GAME_WIDTH/2.0,y = GAME_HEIGHT/2.0,width = GAME_WIDTH,height = GAME_HEIGHT)
          
     def _initFade(self):
          GAME_START_SOUND.play()
          self._fadeClock = 0
          self._aStart = self._alpha
           
     def _initCountdown(self):
          pass
     
     def _selectScreen(self,brightness):
          if not self._state == STATE_FADE:
               if self._inc:
                    self._alpha += A_INC
                    if self._alpha >= 255 - A_INC:
                         self._inc = False
               else:
                    self._alpha -= A_INC
                    if self._alpha <= A_INC + 140:
                         self._inc = True
          else:
               self._alpha = self._aStart * brightness
               self._alpha = int(self._alpha)
          
          self._selectBack.fillcolor = colormodel.RGB(255,255,255,self._alpha)
          self._selectBack.draw(self.view)
          #self._drawTable()
          for l in self._selectLabels:
               color = l.linecolor
               l.linecolor = colormodel.RGB(int(255*color[0]),int(255*color[1]),int(255*color[2]),int(brightness*255))
               color = l.fillcolor
               if color[3] != 0:
                    l.fillcolor = colormodel.RGB(int(255*color[0]),int(255*color[1]),int(255*color[2]),int(brightness*255))
               l.draw(self.view)    
          red = 1
          green = 1
          if self._puckSelected == 2:
               green = 0
          if self._puckSelected == 0:
               red = 0
          puck = Game.Puck(GAME_WIDTH/4.0*(self._puckSelected + 1),GAME_HEIGHT/2.0, red*255,green*205,0,int(brightness*255))
          puck.draw(self.view)
               
     def _updateSound(self):
          if self._song.state == 'stop':
               self._songsPlayed.append(self._song)
               if len(self._songsPlayed) == len(SOUND_LIST):
                    self._songsPlayed = [self._song]
               a = True
               while a:
                    b = random.randrange(0,len(SOUND_LIST))
                    if not SOUND_LIST[b] in self._songsPlayed:
                         a = False
                         self._song = SOUND_LIST[b]
                         self._song.play()
     
     def _keyClicked(self):
          """Returns: True if a key is clicked"""
          return self._keyPressed and self.input.key_count == 0
     
     def _mouseClicked(self):
          """Returns: True if the mouse is clicked"""
          return self._mousePressed and self.input.touch is None
     
     def _determineState(self):
          if self._state == STATE_INACTIVE:
               if self._keyClicked() or self._mouseClicked():
                    self._state = STATE_SELECT
                    self._initSelect()
          if self._state == STATE_SELECT:
               if self.input.is_key_down('enter') and not self._keyPressed:
                    self._state = STATE_FADE
                    self._game = Game(self._puckSelected)
                    self._initFade()
          if self._state == STATE_FADE:
               if self._fadeClock >= 5:
                    self._state = STATE_COUNTDOWN
                    self._initCountdown()
          if self._state == STATE_COUNTDOWN:
               pass
     
     def _drawTable(self):
          background = GRectangle(x = GAME_WIDTH/2.0, y = GAME_HEIGHT/2.0, width = GAME_WIDTH,
                          height = GAME_HEIGHT, fillcolor = colormodel.RGB(255,255,255))
          background.draw(self.view)
          
          for i in range(3):
               circle = GEllipse(x = GAME_WIDTH/2.0 * i, y = GAME_HEIGHT/2.0, width = GAME_HEIGHT/3.0,
                                 height = GAME_HEIGHT/3.0, fillcolor = colormodel.RGB(57,249,255))
               circle.draw(self.view)
               circle = GEllipse(x = GAME_WIDTH/2.0 * i, y = GAME_HEIGHT/2.0, width = GAME_HEIGHT/3.0 - 10,
                                 height = GAME_HEIGHT/3.0 - 10, fillcolor = colormodel.RGB(255,255,255))
               circle.draw(self.view)
               
          half = GRectangle(x = GAME_WIDTH/2.0, y = GAME_HEIGHT/2.0, width = 5,
                            height = GAME_HEIGHT, fillcolor = colormodel.RGB(57,249,255))
          half.draw(self.view)
     
     
class Game(object):
     """Runs the game
     
     Attributes:
          _difficulty"""
     def __init__(self,difficulty):
          """Difficulty 0 is easy, 1 is medium, and 2 is hard"""
          self._difficulty = difficulty
          
     
     class Puck(object):
          """A puck for the game
          #Note:  For collisions, treat the collision as completely
          elastic and with the paddle having infinitely more  mass
          than the puck.  This will make the method a simple
          'bounce' and the impulse-momentum theorem can be used.
          
          Attributes:
          _graphics --> list of gobjects that can be drawn calling the draw method"""
          
          def __init__(self,x,y,r,g,b,a=1,dim=PUCK_DIM):
               self._x = x
               self._y = y
               self._dim = dim
               self._r = int(r)
               self._g = int(g)
               self._b = int(b)
               self._a = int(a)
               self._graphics = []
               self._graphics.append(GEllipse(x=x,y=y,width=dim,height=dim,fillcolor=self.scaledColor(.8)))
               self._graphics.append(GEllipse(x=x,y=y,width=dim*.8,height=dim*.8,fillcolor=self.color()))
          
          def color(self):
               return colormodel.RGB(self._r,self._g,self._b,self._a)
          
          def scaledColor(self,scale):
               return colormodel.RGB(int(self._r*scale),int(self._g*scale),int(self._b*scale),self._a)
          
          def draw(self,view):
               for g in self._graphics:
                    g.draw(view)
          
          
          
          
if __name__ == '__main__':
     AirHockey(width = GAME_WIDTH, height = GAME_HEIGHT).run()