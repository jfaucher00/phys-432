from tkinter import *
import numpy as np
import pydicom
import os
from PIL import ImageTk, Image

### Setup Display and Slider Positions ###

interf_res = "1900x1000"
interf_color = "gray25"
button_color = "gray35"
display_res = (624, 480)

display1_pos = (40, 60)
display2_pos = (654, 60)
display3_pos = (1268, 60)
slide1 = (540,82)
slide2 = (561,82)
slide3 = (1150,82)
slide4 = (1171,82)
slide5 = (1768,82)
slide6 = (1789,82)

### Define Mammogram Class ###

class mammogram:
    def __init__(self, blank = False):
        self.blank = blank
        self.level_max = None
        self.level_min = None
        self.rows = None
        self.cols = None
        self.DICOMheader = None
        self.image = None
        self.windowedImage = None
        self.exposure = None
        self.HVL = None
        self.kvp = None
        self.checks_title = ["KVP", "Grid Status","Breast Thickness",
                             "Filter Material", "Filter Thickness", 
                             "Magnification", "HVL [mm]", 
                             "Exposure [mAs]"]
        self.checks = []
        
    def load(self):
        
        if self.blank:
            path = filedialog.askopenfilename(initialdir=os.getcwd(), 
                                          title="Select Blank Scan")
        else:
            path = filedialog.askopenfilename(initialdir=os.getcwd(), 
                                          title="Select Patient Image")
        
        if len(path) > 0:
        
            ds = pydicom.dcmread(path)
            img = ds.pixel_array
            
            window_center = float(ds.WindowCenter)
            window_width = float(ds.WindowWidth)
            
            # img_type = ds.ImageType
            kvp = ds.KVP
            grid_state = ds.Grid
            breast_thick = ds.BodyPartThickness
            filter_mat = ds.FilterMaterial
            filter_thi = ds.FilterThicknessMinimum
            magnif = str(ds[0x0018, 0x1114])[54:-1]
            hvl = ds.HalfValueLayer
            expo = ds.Exposure
            
            self.checks = [kvp, grid_state, breast_thick,
                           filter_mat, filter_thi, magnif, hvl, expo]
            
            self.exposure = float(expo)
            self.HVL = float(hvl)
            self.DICOMheader = ds
            self.kvp = int(kvp)
            if img.shape == (3328, 2560):
                self.image = img
            else:
                self.image = img[384:3712, 768:]
                
            self.rows, self.cols = img.shape
            self.level_max = int(window_center + window_width)
            self.level_min = int(window_center - window_width)
            
            self.update_img()
            self.send_img()
    
    def update_img(self):
        tempo = self.image.copy()
        tempo[tempo<self.level_min] = self.level_min
        tempo[tempo>self.level_max] = self.level_max
        tempo = tempo - self.level_min
        tempo = tempo*255.0/(self.level_max - self.level_min)
        self.windowedImage = tempo.astype(np.uint8)
        
    def send_img(self):
        # opens the image
        if self.blank:
            img_blank = Image.fromarray(self.windowedImage)
            img_blank = img_blank.resize(display_res[::-1])
            img_blank = ImageTk.PhotoImage(img_blank)
            panel_blank = Label(root, image = img_blank)
            panel_blank.image = img_blank
            panel_blank.place(x = display2_pos[0], y = display2_pos[1])
            
            win_max_slide_blank.set(self.level_max)
            win_min_slide_blank.set(self.level_min)
            
            listbox_blank.delete(0, END)
            for i in range(len(self.checks)):
                listbox_blank.insert(END, self.checks_title[i] + ": " + self.checks[i])
            
        else:
            img_real = Image.fromarray(self.windowedImage)
            img_real = img_real.resize(display_res[::-1])
            img_real = ImageTk.PhotoImage(img_real)
            panel_real = Label(root, image = img_real)
            panel_real.image = img_real
            panel_real.place(x = display1_pos[0], y = display1_pos[1])
            win_max_slide_real.set(self.level_max)
            win_min_slide_real.set(self.level_min)
            
            listbox_real.delete(0, END)
            for i in range(len(self.checks)):
                listbox_real.insert(END, self.checks_title[i] + ": " + self.checks[i])
            
    
    def change_level_max(self, new_val):
        
        self.level_max = float(new_val)
        self.update_img()
        self.send_img()
        
    def change_level_min(self, new_val):
        
        self.level_min = float(new_val)
        self.update_img()
        self.send_img()
        
class mu_map:
    def __init__(self):
        self.map = None
        self.elem1_lvl = None
        self.elem2_lvl = None
        self.elem3_lvl = None
    
    def create(real, blank):
        self.map = np.zeros(real.image.shape)

### Initiate mammogram objects ###

blank_scan = mammogram(blank = True)
real_scan = mammogram()
mat_map = mu_map()

### Interface General Appearence ###

root = Tk()
root.title("MammoPhantom")
root.geometry(interf_res)

lb_font = font.Font(family='Helvetica', size=12)

### Loading Buttons ###

real_button = Button(root, text ='Patient Image', bg = "gray35", fg ='white',
                     font = lb_font, command=real_scan.load)
real_button.place(x = display1_pos[0], y = 10)

blank_button = Button(root, text ='Blank Scan', bg = "gray35", fg ='white',
                      font = lb_font, command=blank_scan.load)
blank_button.place(x = display2_pos[0], y = 10)

### Phantom Specs Input ###



### Real Image Display ### 

win_min_slide_real = Scale(root, from_=3000, tickinterval = 100, 
                      to=0, orient = "vertical",
                      command = real_scan.change_level_min,
                      cursor = "arrow", length = 600,
                      showvalue = 0, background='gray25')
win_max_slide_real = Scale(root, from_=3000, tickinterval = 100, 
                      to=0, orient = "vertical",
                      command = real_scan.change_level_max,
                      cursor = "arrow", length = 600,
                      showvalue = 0, background='gray25')

img_real = Image.fromarray(np.zeros(display_res, dtype = np.int8))

img_real = ImageTk.PhotoImage(img_real)

panel_real = Label(root, image = img_real)
      
panel_real.image = img_real
panel_real.place(x = display1_pos[0], y = display1_pos[1])

win_max_slide_real.place(x = slide1[0], y = slide1[1])
win_min_slide_real.place(x = slide2[0], y = slide2[1])

### Add Descriptive Text ###

# text_real = Text(root, height = 1, width = 36, font = lb_font,
#                  background = interf_color, bd = 0, foreground = 'white')
# text_real.place(x = display1_pos[0], y = 10)
# text_real.insert(END, "Patient Image")

text_window_real = Text(root, height = 1, width = 7, font = lb_font,
                 background = interf_color, bd = 0, foreground = 'white')
text_window_real.place(x = slide1[0], y = 15)
text_window_real.insert(END, "Window")

text_max_real = Text(root, height = 1, width = 4,
                 background = interf_color, bd = 0, foreground = 'white')
text_max_real.place(x = slide1[0], y = 42)
text_max_real.insert(END, "MAX")

text_min_real = Text(root, height = 1, width = 4,
                 background = interf_color, bd = 0, foreground = 'white')
text_min_real.place(x = slide2[0]+34, y = 42)
text_min_real.insert(END, "MIN")

### Real Image Listbox ###

listbox_real = Listbox(root, width = 44, height = 10, font = lb_font,
                       background = 'black', foreground = "white")
listbox_real.place(x=display1_pos[0],y=display1_pos[1]+display_res[0]+20)

listbox_real.insert(END, 'Select a patient scan in the "File" menu.')

### Blank Scan Display ###

win_min_slide_blank = Scale(root, from_=16400, tickinterval = 400, 
                      to=0, orient = "vertical",
                      command = blank_scan.change_level_min,
                      cursor = "arrow", length = 600,
                      showvalue = 0, background='gray25')
win_max_slide_blank = Scale(root, from_=16400, tickinterval = 400, 
                      to=0, orient = "vertical",
                      command = blank_scan.change_level_max,
                      cursor = "arrow", length = 600,
                      showvalue = 0, background='gray25')

img_blank = Image.fromarray(np.zeros(display_res, dtype = np.int8))

img_blank = ImageTk.PhotoImage(img_blank)

panel_blank = Label(root, image = img_blank)

panel_blank.image = img_blank
panel_blank.place(x = display2_pos[0], y = display2_pos[1])

win_max_slide_blank.place(x = slide3[0], y = slide3[1])
win_min_slide_blank.place(x = slide4[0], y = slide4[1])

### Add Descriptive Text ###

# text_blank = Text(root, height = 1, width = 36, font = lb_font,
#                  background = interf_color, bd = 0, foreground = 'white')
# text_blank.place(x = display2_pos[0], y = 10)
# text_blank.insert(END, "Blank Scan")

text_window_blank = Text(root, height = 1, width = 7, font = lb_font,
                 background = interf_color, bd = 0, foreground = 'white')
text_window_blank.place(x = slide3[0], y = 15)
text_window_blank.insert(END, "Window")

text_max_blank = Text(root, height = 1, width = 4,
                 background = interf_color, bd = 0, foreground = 'white')
text_max_blank.place(x = slide3[0], y = 42)
text_max_blank.insert(END, "MAX")

text_min_blank = Text(root, height = 1, width = 4,
                 background = interf_color, bd = 0, foreground = 'white')
text_min_blank.place(x = slide4[0] + 40, y = 42)
text_min_blank.insert(END, "MIN")

### Blank Image Listbox ###

listbox_blank = Listbox(root, width = 44, height = 10, font = lb_font,
                       background = 'black', foreground = "white")
listbox_blank.place(x=display2_pos[0],y=display2_pos[1]+display_res[0]+20)

listbox_blank.insert(END, 'Select a blank scan in the "File" menu if available.')


### Material Map ###

# mat2_slide = Scale(root, from_=16400, tickinterval = 400, 
#                    to=0, orient = "vertical",
#                    command = blank_scan.change_level_max,
#                    cursor = "arrow", length = 600,
#                    showvalue = 0, background='gray25')
# mat1_slide = Scale(root, from_=16400, tickinterval = 400, 
#                    to=0, orient = "vertical",
#                    command = blank_scan.change_level_min,
#                    cursor = "arrow", length = 600,
#                    showvalue = 0, background='gray25')


img_mat = Image.fromarray(np.zeros(display_res, dtype = np.int8))

img_mat = ImageTk.PhotoImage(img_mat)

panel_mat = Label(root, image = img_mat)

panel_mat.image = img_mat
panel_mat.place(x = display3_pos[0], y = display3_pos[1])

# mat1_slide.place(x = slide5[0], y = slide5[1])
# mat2_slide.place(x = slide6[0], y = slide6[1])

### Add Descriptive Text ###

text_mat = Text(root, height = 1, width = 36, font = lb_font,
                 background = interf_color, bd = 0, foreground = 'white')
text_mat.place(x = display3_pos[0], y = 15)
text_mat.insert(END, "Material Map")

# text_window_mat = Text(root, height = 1, width = 7, font = lb_font,
#                  background = interf_color, bd = 0, foreground = 'white')
# text_window_mat.place(x = slide5[0], y = 10)
# text_window_mat.insert(END, "Window")

# text_max_mat = Text(root, height = 1, width = 4,
#                  background = interf_color, bd = 0, foreground = 'white')
# text_max_mat.place(x = slide5[0], y = 37)
# text_max_mat.insert(END, "MAX")

# text_min_mat = Text(root, height = 1, width = 4,
#                  background = interf_color, bd = 0, foreground = 'white')
# text_min_mat.place(x = slide6[0] + 40, y = 37)
# text_min_mat.insert(END, "MIN")


### Run Main Loop ###

root.configure(bg = interf_color)
root.mainloop()