from PythUnity import Variables
from PythUnity import Functions
import copy
import pygame
import types
class Object:
  def __init__(self, rect, image, onClick = None, onDrag = None, onClickOff = None, onScroll = None, enableDragOff = False, clickGroup = 0):
    self.__destroyed = False
    self.__parent = None
    self.__children = []
    self.__variables = {}
    self.__image = None
    self.__text = None
    self.__color = None
    self.__components = []
    self.__clickGroup = clickGroup#not implemented yet
    self.__velocity = (0, 0)
    self.__index = None
    if(type(image) is tuple):
      self.color = image
    elif(type(image) is String):
      self.text = copy.deepcopy(image)
    else:
      self.image = image
    self.rect = rect
    if onClick != None or onDrag != None or onScroll != None:
      self.__button = Button(onClick, onDrag, onClickOff, onScroll, enableDragOff)
    else:
      self.__button = None
    Functions.AddObject(self)
    #for att in dir(self):
    #    print(att)
    #print("////////////")
  #####
  @property
  def image(self):
    return self.__image
  @image.setter
  def image(self, value):
    Functions.TypeCheck(value, pygame.Surface, "image")
    self.__image = value
    ratio = self.__image.get_size()
    max = ratio[0]
    if(max < ratio[1]):
        max = ratio[1]
    ratio = (int(1000.0 * ratio[0] / max), int(1000.0 * ratio[1] / max))
    self.__image = pygame.transform.scale(self.__image, ratio)
  @property
  def destroyed(self):
    return self.__destroyed
  @destroyed.setter
  def destroyed(self, value):
    Functions.Err("Cant set Object.destroyed")
  @property
  def index(self):
    return self.__index
  @index.setter
  def index(self, value):
    Functions.Err("Cant set Object.index")
  @property
  def parent(self):
    return self.__parent
  @parent.setter
  def parent(self, value):
    Functions.Err("Cant set Object.parent")
  @property
  def children(self):
    return self.__children
  @children.setter
  def children(self, value):
    Functions.Err("Cant set Object.children")
  @property
  def components(self):
    return self.__components
  @components.setter
  def components(self, value):
    Functions.Err("Cant set Object.components, use Object.AddComp or Object.DelComp")
  @property
  def variables(self):
    return self.__variables
  @variables.setter
  def variables(self, value):
    Functions.Err("Cant set Object.variables, add each variable individualy")
  ##
  @property
  def text(self):
      return self.__text
  @text.setter
  def text(self, value):
    Functions.TypeCheck(value, [String, type(None)], "text")
    self.__text = value
  @property
  def color(self):
      return self.__color
  @color.setter
  def color(self, value):
    Functions.TypeCheck(value, [tuple, type(None)], "color")
    self.__color = value
  @property
  def clickGroup(self):
      return self.__clickGroup
  @clickGroup.setter
  def clickGroup(self, value):
    Functions.TypeCheck(value, int, "clickGroup")
    self.__clickGroup = value
  @property
  def velocity(self):
      return self.__velocity
  @velocity.setter
  def velocity(self, value):
    Functions.TypeCheck(value, tuple, "velocity")
    self.__velocity = value
  @property
  def button(self):
      return self.__button
  @button.setter
  def button(self, value):
    Functions.TypeCheck(value, [Button, type(None)], "button")
    self.__button = value
  #####
  def __getitem__(self, i):
    self.__Throw("children.getitem")
    return self.__children[i]
  def __len__(self):
    self.__Throw("children.len")
    return len(self.__children)
  #####
  def Decendants(self):
    self.__Throw("Object.Decendants")
    indexes = []
    for i in self.__children:
      indexes.append(i)
      indexes.extend(Variables.var.parts[i].Decendants())
    return indexes
  def Move(self, newIndex):#components can have their update function skipped on accident if ran in another comp.update
    self.__Throw("Object.Move")
    children = self.GetParentChildren()
    if(newIndex < 0):
        Functions.Err("Object.Move failed, index less than 0")
    elif(newIndex > len(children)):
        Functions.Warn("Object.Move incorrect, index is greater than parent.children count")
    oldIndex = self.index
    self.__index = newIndex
    del children[oldIndex]
    children.insert(newIndex, self)
    i = oldIndex
    if(newIndex > oldIndex):
      while(i < newIndex):
        children[i]._Object__index = i
        i = i + 1
    elif(newIndex < oldIndex):
      while(i >= newIndex):
        children[i]._Object__index = i
        i = i - 1
  def SetParent(self, newParent):
    self.__Throw("Object.SetParent")
    children = self.GetParentChildren()
    self.Move(len(children))#make it so other children have their indexes fixed
    del children[self.index]
    self.__parent = newParent
    self.__parent.children.append(self)
    self.__index = len(self.__parent.children) - 1
  def GetParentChildren(self):
    self.__Throw("Object.GetParentChildren")
    children = None
    if(self.__parent != None):
      children = self.__parent.children
    else:
      children = Variables.var.parts
    return children
  def Copy(self):
    self.__Throw("Object.Copy")
    CopyHelp(self)
    parChildren = self.GetParentChildren()
    copied = copy.deepcopy(self)
    copied._Object__index = len(parChildren)
    parChildren.append(copied)
    copied.__parent = self.__parent
    copied.Move(self.index + 1)
    CopyUnHelp(self)
    CopyUnHelp(copied)
    CopyHelp2(copied)
    return copied
  def Destroy(self):
    self.__Throw("Object.Destroy")
    children = self.GetParentChildren()
    self.Move(len(children))
    del children[self.index]
    self.__index = -1 #will cause Functions.Error if used incorrectly, did this on purpous
    self.__destroyed = True
    for i in self.__children:
      i.Destroy()
  def AddComp(self, comp):
    self.__Throw("Object.AddComp")
    self.__components.append(comp)
    if(comp[0] != None):
        comp[0](self)
  def DelComp(self, index):
      self.__Throw("Object.DelComp")
      if(len(self.__components) > index):
          del self.__components[index]
      else:
          Functions.Err("Object.DelComp failed, index greater than comp index")
  def __Throw(self, action = ""):
    if(self.__destroyed):
      if(action == ""):
        Functions.Err("Object was destroyed")
      else:
        Functions.Err("Object was destroyed while " + action + "() was happening")
class Button:
  def __init__(self, onClick, onDrag, onClickOff, onScroll, enableDragOff):
    self.__onClick = None
    self.__onClickOff = None
    self.__onDrag = None
    self.__onScroll = None
    self.__dragging = False
    self.__enableDragOff = False
    self.onClick = onClick
    self.onClickOff = onClickOff
    self.onDrag = onDrag
    self.onScroll = onScroll
  @property
  def dragging(self):
      return self.__dragging
  @dragging.setter
  def dragging(self, value):
      Functions.Err("You cant set PythUnity.Button.dragging, you can only get it")
  ##
  @property
  def enableDragOff(self):
      return self.__enableDragOff
  @enableDragOff.setter
  def enableDragOff(self, value):
      Functions.TypeCheck(value, bool, "enableDragOff", "Button")
      self.__enableDragOff = value
  @property
  def onClick(self):
      return self.__onClick
  @onClick.setter
  def onClick(self, value):
      Functions.TypeCheck(value, [types.FunctionType, type(None)], "onClick", "Button")
      self.__onClick = value
  @property
  def onClickOff(self):
      return self.__onClickOff
  @onClickOff.setter
  def onClickOff(self, value):
      Functions.TypeCheck(value, [types.FunctionType, type(None)], "onClickOff", "Button")
      self.__onClickOff = value
  @property
  def onDrag(self):
      return self.__onDrag
  @onDrag.setter
  def onDrag(self, value):
      Functions.TypeCheck(value, [types.FunctionType, type(None)], "onDrag", "Button")
      self.__onDrag = value
  @property
  def onScroll(self):
      return self.__onScroll
  @onScroll.setter
  def onScroll(self, value):
      Functions.TypeCheck(value, [types.FunctionType, type(None)], "onScroll", "Button")
      self.__onScroll = value
class String:
  def __init__(self, text, fontSize, font, fontColor, backgroundColor):
    self.__fontSize = None
    self.__text = None
    self.__font = None
    self.__fontColor = None
    self.__backgroundColor = None
    self.fontSize = fontSize
    self.text = text
    self.font = font
    self.fontColor = fontColor
    self.backgroundColor = backgroundColor
  @property
  def fontSize(self):
    return self.__fontSize
  @fontSize.setter
  def fontSize(self, value):
    Functions.TypeCheck(value, int, "fontSize", "String")
    self.__fontSize = value
  @property
  def text(self):
    return self.__text
  @text.setter
  def text(self, value):
    Functions.TypeCheck(value, str, "text", "String")
    self.__text = value
  @property
  def font(self):
    return self.__font
  @font.setter
  def font(self, value):
    Functions.TypeCheck(value, str, "font", "String")
    self.__font = value
  @property
  def fontColor(self):
    return self.__fontColor
  @fontColor.setter
  def fontColor(self, value):
    Functions.TypeCheck(value, [tuple, type(None)], "fontColor", "String")
    self.__fontColor = value
  @property
  def backgroundColor(self):
    return self.__backgroundColor
  @backgroundColor.setter
  def backgroundColor(self, value):
    Functions.TypeCheck(value, [tuple, type(None)], "backgroundColor", "String")
    self.__backgroundColor = value
def CopyHelp(self):
  if(self.image != None):
    self._Object__image = (pygame.image.tostring(self._Object__image, 'RGBA'), self._Object__image.get_size())
  for i in self.children:
    CopyHelp(i)

def CopyUnHelp(self):
  if(self._Object__image != None):
    self._Object__image = pygame.image.fromstring(self._Object__image[0], self._Object__image[1], 'RGBA')
  for i in self.children:
    CopyUnHelp(i)
def CopyHelp2(self):
  for att in dir(self):
    attObj = getattr(self, att)
    if(att[0] != "_" or att[1] == "O"):#if its a _Object__ atribute still copy
        attType = type(attObj)
        if(attType is not types.MethodType and attType is not list and attType is not type(None) and attType is not Object and attType is not pygame.Surface):
            attObj = copy.deepcopy(attObj)
  for i in self.children:
    CopyHelp2(i)

