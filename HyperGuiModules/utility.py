from tkinter import *
from tkinter.ttk import Notebook, Style
from tkinter.ttk import Button as TButton
from HyperGuiModules.constants import *
import numpy as np
from matplotlib import cm
import imageio
from math import atan, pi
import matplotlib.colors
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2
from matplotlib.figure import Figure

matplotlib.use("TkAgg")


def init():
    """
    Creates a root window which contains a notebook 'notebook' with four frames: 'introduction', 'input_output',
    'image_diagram', and 'Prediciton'. Returns the root window along with the four frames.
    """
    root = Tk()
    root.resizable(width=False, height=False)
    root.title(WINDOW_TITLE)
    root.geometry("+0+0")

    notebook = Notebook(root)

    introduction = Frame(notebook, bg=tkcolour_from_rgb(WHITE))
    introduction.pack()
    notebook.add(introduction, text="Introduction")

    input_output = Frame(notebook)
    input_output.pack()
    notebook.add(input_output, text="Input and Output")
    

    image_diagram = Frame(notebook)
    image_diagram.pack()
    notebook.add(image_diagram, text="Images and Diagrams")

    hist_calculation = Frame(notebook, bg=tkcolour_from_rgb(BACKGROUND))
    hist_calculation.pack()
    notebook.add(hist_calculation, text="Histogram Calculation")

    spec_calculation = Frame(notebook, bg=tkcolour_from_rgb(BACKGROUND))
    spec_calculation.pack()
    notebook.add(spec_calculation, text="Optical Spectrum Calculation")
    
    BP = Frame(notebook, bg=tkcolour_from_rgb(WHITE))
    BP.pack()
    notebook.add(BP, text="bp (free hand)")
    
    circle = Frame(notebook, bg=tkcolour_from_rgb(WHITE))
    circle.pack()
    notebook.add(circle, text="bp (circular)")
    
    rectangle = Frame(notebook, bg=tkcolour_from_rgb(WHITE))
    rectangle.pack()
    notebook.add(rectangle, text="bp (rectangular)")
    
    crops = Frame(notebook, bg=tkcolour_from_rgb(WHITE))
    crops.pack()
    notebook.add(crops, text="Crops")
    
    BS = Frame(notebook, bg=tkcolour_from_rgb(WHITE))
    BS.pack()
    notebook.add(BS, text="Baseline subtracion")
    
    measure = Frame(notebook, bg=tkcolour_from_rgb(WHITE))
    measure.pack()
    notebook.add(measure, text="Measure Tool")
    
    mda = Frame(notebook, bg=tkcolour_from_rgb(WHITE))
    mda.pack()
    notebook.add(mda, text="Meta-Data Anotation")
    
    mda2 = Frame(notebook, bg=tkcolour_from_rgb(WHITE))
    mda2.pack()
    notebook.add(mda2, text="Meta-Data Anotation 2")
    
    specInvest = Frame(notebook, bg=tkcolour_from_rgb(WHITE))
    specInvest.pack()
    notebook.add(specInvest, text="Spectrum Investigation")
    
    progressions = Frame(notebook, bg=tkcolour_from_rgb(WHITE))
    progressions.pack()
    notebook.add(progressions, text="Progressions")
    
    prediction = Frame(notebook, bg=tkcolour_from_rgb(WHITE))
    prediction.pack()
    notebook.add(prediction, text="Prediction")
    
    notebook.pack()

    return root, introduction, input_output, image_diagram, hist_calculation, spec_calculation, BP, crops, BS, measure, mda, mda2, circle, rectangle, specInvest, progressions, prediction


def tkcolour_from_rgb(rgb):
    """
    Translates an rgb tuple of ints to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb


def frame(window, colour, row, column, rowspan, columnspan, wraplength=140):
    """
    Creates a frame, grids it, and returns it based on the input parameters with 2px thick 
    borders in the colour BORDER.
    window : tk.Frame
    colour : hexadecimal colour
    row : int
    column : int
    rowspan : int
    columnspan : int
    wraplength : int (default 140)
    """
    frame_widget = Frame(window, bg=tkcolour_from_rgb(colour), highlightbackground=tkcolour_from_rgb(BORDER),
                         highlightcolor=tkcolour_from_rgb(BORDER), highlightthickness=2)
    frame_widget.grid(row=row, rowspan=rowspan, column=column, columnspan=columnspan, sticky=W + E + N + S)
    return frame_widget


def make_button(window, text, command, row, column, height=1, width=10,
                inner_padx=10, inner_pady=10, outer_padx=0, outer_pady=0, columnspan=1, rowspan=1, highlightthickness=1,
                wraplength=0, button = None):
    """
    Creates a button, grids it, and returns it based on the input parameters.
    window : tk.Frame
    text : str
    command : function
    row : int
    column : int
    height : int (default 1, text units)
    width : int (default 10, text units)
    inner_padx : int (default 10, x padding inside button)
    inner_pady : int (default 10, y padding inside button)
    outer_padx : int or tuple of two ints (default 0, x padding outside button)
    outer_pady : int or tuple of two ints (default 0, y padding outside button)
    columnspan : int (default 1)
    rowspan : int (default 1)
    highlightthickness : int (default 1, button border thickness)
    wraplength : int (default 0)
    """
    if button is None:
        button = Button(window, text=text, command=command, padx=inner_padx, pady=inner_pady, height=height, width=width,
                        highlightthickness=highlightthickness, wraplength=wraplength)#
    button.grid(row=row, column=column, padx=outer_padx, pady=outer_pady, columnspan=columnspan, rowspan=rowspan)
    return button

def make_slider(window, label, command, row, column, width=10, #Jan Odenthal, University of Heidelberg
               outer_padx=0, outer_pady=0, columnspan=1, rowspan=1, highlightthickness=1, orient="vertical", from_=0, to = 100, resolution=1):
    """
    Creates a button, grids it, and returns it based on the input parameters.
    window : tk.Frame
    label : str
    command : function
    row : int
    column : int
    height : int (default 1, text units)
    width : int (default 10, text units)
    outer_padx : int or tuple of two ints (default 0, x padding outside button)
    outer_pady : int or tuple of two ints (default 0, y padding outside button)
    columnspan : int (default 1)
    rowspan : int (default 1)
    highlightthickness : int (default 1, button border thickness)
    wraplength : int (default 0)
    """
    slider = Scale(window, label=label, command=command, width=width,
                    highlightthickness=highlightthickness, orient = orient, from_=from_, to=to, resolution=resolution)
    slider.grid(row=row, column=column, padx=outer_padx, pady=outer_pady, columnspan=columnspan, rowspan=rowspan)
    return slider

def make_label_button(window, text, command, width):
    """
    Creates a button to be used as a widget label, grids it, and returns it 
    based on the input parameters. The button is given solid relief, coloured white, and given a 2px thick black border.
    The button is padded 15px from the left and 15px above and below.
    window : tk.Frame
    command : function
    width : int (text units)
    """
    button = TButton(window, text=text, width=width, command=command)
    Style().configure("TButton", relief="solid", background=tkcolour_from_rgb((255, 255, 255)),
                      bordercolor=tkcolour_from_rgb((0, 0, 0)), borderwidth=2)
    Style().theme_use('default')
    button.grid(row=0, column=0, padx=(15, 0), pady=15)
    return button


def make_label(window, text, row, column, borderwidth=2, inner_padx=1, inner_pady=1, outer_padx=0, outer_pady=15,
               relief="solid", rowspan=1, columnspan=1, wraplength=140):
    """
    Creates a label, grids it, and returns it based on the input parameters.
    window : tk.Frame
    text : str
    row : int
    column : int
    borderwidth : int (default 2)
    inner_padx : int (default 1, x padding inside button)
    inner_pady : int (default 1, y padding inside button)
    outer_padx : int or tuple of two ints (default 0, x padding outside button)
    outer_pady : int or tuple of two ints (default 15, y padding outside button)
    relief : str (default "solid", label design option)
    rowspan : int (default 1)
    columnspan : int (default 1)
    wraplength : int (default 140)
    """
    label = Label(window, text=text, borderwidth=borderwidth, relief=relief,
                  padx=inner_padx, pady=inner_pady, wraplength=wraplength)
    label.grid(row=row, column=column, padx=outer_padx, pady=outer_pady, columnspan=columnspan, rowspan=rowspan)
    return label


def make_text(window, content, row, column, padx=0, pady=0, height=1, width=2, highlightthickness=0, bg="white",
              columnspan=1, rowspan=1, state=DISABLED, text = None):
    """
    Creates text, grids it, and returns it based on the input parameters.
    window : tk.Frame
    content : str
    row : int
    column : int
    padx : int or tuple of two ints (default 0, x padding outside button)
    pady : int or tuple of two ints (default 0, y padding outside button)
    height : int (default 1, text units)
    width : int (default 2, text units)
    highlightthickness : int (default 0)
    bg : hexadecimal colour or str (defult "white", background colour)
    columsnpan : int (default 1)
    rowspan : int (default 1)
    state : DISABLED or NORMAL (default DISABLED, NORMAL allows the text to be selected/edited while DISABLED does not)
    """
    if text is None:
        text = Text(window, bg=bg, height=height, width=width, highlightthickness=highlightthickness)
        text.insert(END, content)
        text.config(state=state)
        text.grid(row=row, column=column, padx=padx, pady=pady, columnspan=columnspan, rowspan=rowspan)
    else:
        text.delete(1.0, END)
        text.insert(END, content)
        text.config(state=state)
        text.grid(row=row, column=column, padx=padx, pady=pady, columnspan=columnspan, rowspan=rowspan)
    return text


def make_listbox(window, row, column, padx=0, pady=0, highlightthickness=0, columnspan=1, rowspan=1, height = 10, width=18, selectmode = "EXTENDED"):
    """
    Creates a listbox, grids it, and returns it based on the input parameters.
    window : tk.Frame
    row : int
    column : int
    padx : int or tuple of two ints (default 0, x padding outside button)
    pady : int or tuple of two ints (default 0, y padding outside button)
    highlightthickness : int (default 0)
    columnspan : int (default 1)
    rowspan : int (default 1)
    """
    listbox = Listbox(window, width=width, highlightthickness=highlightthickness, selectmode=selectmode, height=height, exportselection=0)
    listbox.grid(row=row, column=column, padx=padx, pady=pady, rowspan=rowspan, columnspan=columnspan)
    return listbox


def make_entry(window, row, column, width, columnspan=1, pady=0, padx=0, highlightthickness=0, entry = None):
    """
    Creates an Entry widget, grids it, and returns it based on the input parameters.
    window : tk.Frame
    row : int
    column : int
    width : int (text units)
    columnspan : int (default 1)
    pady : int or tuple of two ints (default 0, y padding outside button)
    padx : int or tuple of two ints (default 0, x padding outside button)
    highlightthickness : int (default 0)
    """
    if entry is None:
        entry = Entry(window, width=width, highlightthickness=highlightthickness, textvariable=StringVar())
    entry.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady)
    return entry


def make_checkbox(window, text, row, column, var, columnspan=1, inner_padx=1, inner_pady=1, outer_padx=0, outer_pady=0,
                  bg=tkcolour_from_rgb(CHECKBOX), sticky=W + N + S + E, checkbox = None):
    """
    Creates a checkbox of width 2, grids it, and returns it based on the input parameters. 
    window : tk.Frame
    text : str
    row : int
    column : int
    var : variable containing bool (True if selected, False if deselected)
    columspan : int (default 1)
    inner_padx : int (default 1, x padding inside button)
    inner_pady : int (default 1, y padding inside button)
    outer_padx : int or tuple of two ints (default 0, x padding outside button)
    outer_pady : int or tuple of two ints (default 0, y padding outside button)
    bg : hexadecimal colour or str (defult CHECKBOX, checkbox colour)
    sticky : combination of N, S, W, E (default W+N+S+E, position of checkbox in gridcell)
    """
    if checkbox is None:
        checkbox = Checkbutton(window, text=text, variable=var, padx=inner_padx, pady=inner_pady, bg=bg, width=2)
    checkbox.grid(row=row, column=column, padx=outer_padx, pady=outer_pady, sticky=sticky, columnspan=columnspan)
    return checkbox


def make_image(window, image_data, row, column, columnspan, rowspan, lower_scale_value, upper_scale_value, color_rgb,
               figwidth=2.5, figheight=2, original=False, gs=False, img = None, axs = None, figu = None):
    """
    Plots an image and grids it based on the input parameters. Image is plotted with origin="lower" and cmap="jet".
    Returns the Figure object (fig) that the image is plotted on, as well as the image itself.
    window : tk.Frame
    image_data : 2D array
    row : int
    column : int
    columnspan : int
    rowspan : int
    lower_scale_value : int or float (used as vmin when plotting)
    lower_scale_value : int or float (used as vmax when plotting)
    color_rgb : hexadecimal colour (colour surrounding image)
    figwidth : int or float (default 3, inches)
    figheight : int or float (default 2, inches)
    original : bool (default False, will not plot vmin, vmax, or axes if True)
    gs : bool (default False, True would plot in greyscale)
    """
    
    # create figure
    if figu is None:
        fig = Figure(figsize=(figwidth, figheight))
    else:
        fig = figu
    # add axes
    if axs is None:
        axes = fig.add_subplot(111)
    else:
        axes = axs.gca()
        axes.clear()
    # determine cmap
    norm = None
    if gs:
        cmap = 'gray'
    else:
        
        
        #colors = [(0, 0, 100/256), (0, 0, 255/256), (0, 255/256, 0), (255/256, 255/256, 0), (255/256, 0, 0),  (100/256, 0, 0)]  # R -> G -> B
        #n_bin = 100  # Discretizes the interpolation into bins
        #cmap_name = 'my_list'
        #color_scale = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bin)
        #boundaries = [0,0.2,0.4,0.6,0.8,1]
        #if lower_scale_value is not None and upper_scale_value is not None:
        #    boundaries = [val*(upper_scale_value - lower_scale_value) + lower_scale_value for val in boundaries]
        #norm = matplotlib.colors.BoundaryNorm(boundaries, color_scale.N, clip=True)
        #cmap = color_scale
        
        R1 = np.linspace(0,0,20)
        B1 = np.linspace(0,0,20)
        G1 = np.linspace(100/256,255/256,20) 
        R2 = np.linspace(0,0,20)
        B2 = np.linspace(0,255/256,20)
        G2 = np.linspace(255/256,0,20) 
        R3 = np.linspace(0,255/256,20)
        B3 = np.linspace(255/256,255/256,20)
        G3 = np.linspace(0,0,20) 
        R4 = np.linspace(255/256,255/256,20)
        B4 = np.linspace(255/256,0,20)
        G4 = np.linspace(0,0,20) 
        R5 = np.linspace(255/256,100/256,20)
        B5 = np.linspace(0,0,20)
        G5 = np.linspace(0,0,20) 
        R = np.hstack([R1, R2, R3, R4, R5])
        B = np.hstack([B1, B2, B3, B4, B5])
        G = np.hstack([G1, G2, G3, G4, G5])
        colors = [(R[idx], B[idx], G[idx]) for idx in range(100)]
        n_bin = 100  # Discretizes the interpolation into bins
        cmap_name = 'my_list'
        color_scale = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bin)
        boundaries = np.arange(0,1,0.01)
        if lower_scale_value is not None and upper_scale_value is not None:
            boundaries = [val*(upper_scale_value - lower_scale_value) + lower_scale_value for val in boundaries]
        norm = matplotlib.colors.BoundaryNorm(boundaries, color_scale.N, clip=True)
        cmap = color_scale

        
        #scale = np.loadtxt('scale.txt', delimiter = ",")
        #c_scale = [list(li/255)[0:3] for li in scale]
        #c_scale.reverse()
        #boundaries = [li[3]/100 for li in scale]
        #boundaries.reverse()
        #if lower_scale_value is not None and upper_scale_value is not None:
        #    boundaries = [val*(upper_scale_value - lower_scale_value) + lower_scale_value for val in boundaries]
        #color_scale = matplotlib.colors.ListedColormap(c_scale)
        #norm = matplotlib.colors.BoundaryNorm(boundaries, color_scale.N, clip=True)
        #cmap = color_scale
        
        #cmap = 'jet'
        
        
        
    # plot image
    if original:
        # plot image array without showing axes
        if norm is None:
            image = axes.imshow(np.flipud(image_data), origin='lower', cmap=cmap)
        else:
            image = axes.imshow(np.flipud(image_data), origin='lower', cmap=cmap, norm = norm)
        axes.axis('off')
        image_array = image.get_array().flatten()
    else:
        # plot image array with vmin and vmax 
        if norm is None:
            image = axes.imshow(image_data[:, :].T, origin='lower', cmap=cmap,
                                vmin=float(lower_scale_value),
                                vmax=float(upper_scale_value))
        else:
            image = axes.imshow(image_data[:, :].T, origin='lower', cmap=cmap, norm = norm,
                                vmin=float(lower_scale_value),
                                vmax=float(upper_scale_value))
        image_array = image.get_array().flatten()

    # set colour around image 
    fig.patch.set_facecolor(rgb_to_rgba(color_rgb))
    # set tight layout 
    fig.set_tight_layout('True')
    # place image in window and draw

    if img == None or isinstance(img, Label):
        image = FigureCanvasTkAgg(fig, master=window)
    else:
        image = img
    image.draw()
    if figu is not None:
        fig.canvas.draw_idle()
    image.get_tk_widget().grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)
    return fig, image, image_array


def make_popup_image(graph, graphsize=(8, 8), interactive=False):
    """
    Creates a pop-up TopLevel() window in the top left screen corner containing an image based on the input parameters.
    graph : matplotlib Figure() object
    graphsize : tuple of two ints (default (8, 8), inches)
    interactive : bool (default False, will return a tuple containing window and image if True)
    """

    # create the toplevel window and place it at top left of screen
    window = Toplevel()
    window.geometry("+0+0")
    # set graph size to that defined in parameters
    graph.set_size_inches(graphsize[0], graphsize[1])
    # create image, draw, and grid
    image = FigureCanvasTkAgg(graph, master=window)
    image.draw()
    image.get_tk_widget().grid(column=0, row=0)
    # return window and image as a tuple
    if interactive:
        return window, image
    
def make_popup_image_external(graph, graphsize=(8, 8)):
    """
    Creates a pop-up TopLevel() window in the top left screen corner containing an image based on the input parameters.
    graph : matplotlib Figure() object
    graphsize : tuple of two ints (default (8, 8), inches)
    interactive : bool (default False, will return a tuple containing window and image if True)
    """

    # create the toplevel window and place it at top left of screen
    window = Toplevel()
    window.geometry("+0+0")
    # set graph size to that defined in parameters
    graph.set_size_inches(graphsize[0], graphsize[1])
    # create image, draw, and grid
    image = FigureCanvasTkAgg(graph, master=window)
    image.draw()
    image.get_tk_widget().grid(column=0, row=0)
    # return window and image as a tuple
    return window, image, graph.axes[0]


def image_to_array(filename):
    """
    Converts an image to an array using imageio and returns array.
    filename : str
    """
    return imageio.imread(filename)


def make_info(title, info):
    """
    Creates a pop-up TopLevel() window in the top=left screen corner containing information about the widget. Default
    size is 50 characters wide by 20 characters high, with wrapping by word, disabled text, 5px padding around the text
    box, and resizable=False.
    title : str (title of pop-up window)
    info : str (content of pop-up window)
    """

    # create the toplevel window with title and place in top left of screen
    window = Toplevel()
    window.title(title)
    window.geometry("+0+0")
    # create textbox and insert info
    text = Text(window, height=24, width=70, wrap=WORD, highlightthickness=0, foreground=tkcolour_from_rgb(GREY))
    text.insert(END, title, ('title', str(0)))
    text.insert(END, '\n\n' + info)
    text.tag_config('title', foreground='black', underline=True)
    # disable text, add padding and make resizable False
    text.config(state="disabled")
    text.grid(padx=5, pady=5)
    window.resizable(width=False, height=False)


def specs(choice):
    if choice == '1.':
        specs_tup = (False, True, False)
    elif choice == '2.':
        specs_tup = (False, True, True)
    elif choice == '3.':
        specs_tup = (False, False, False)
    elif choice == '4.':
        specs_tup = (False, False, True)
    elif choice == '5.':
        specs_tup = (True, True, False)
    elif choice == '6.':
        specs_tup = (True, True, True)
    elif choice == '7.':
        specs_tup = (True, False, False)
    elif choice == '8.':
        specs_tup = (True, False, True)
    spec_number = int(choice[0])
    return specs_tup, spec_number


def rgb_to_rgba(rgb):
    """
    Convert a tuple or list containing an rgb value to a tuple containing an rgba value.
    rgb : tuple or list of ints or floats ([r, g, b])
    """
    r = rgb[0] / 255
    g = rgb[1] / 255
    b = rgb[2] / 255
    return r, g, b


def progress(val, total):
    update = ['-', '\\', '|', '/']
    if val != total - 1:
        print(update[val % 4] + ' ' + str(round((val + 1) / total * 100, 2)) + '%', end="\r", flush=True)
    else:
        print(update[val % 4] + ' ' + str(round((val + 1) / total * 100, 2)) + '%')


def find_nearest(array, value):
    """
    Returns the index of the element in the input array closest to the input value.
    array : array of ints or floats
    value : int or float
    """
    # convert array to numpy array
    array = np.asarray(array)
    # take the absolute value of the difference between each value in the input array and the input value, and return
    # the index of the minimum value
    return (np.abs(array - value)).argmin()


def rgb_to_angle(rgb):
    """
    Converts an rgb tuple or list to an angle and returns the angle. Conversion is done by flattening the rgb colour
    space along axis 2 and determining the angle of the flattened rgb point (red). This process is repeated with axis 0
    as the flattened axis (blue). If red is 0, we return blue as the angle. Similarly if blue is 315, we return red as
    the angle. Otherwise, we return the average of the two angles.
    rgb : tuple or list of floats or ints ([r, g, b])
    """
    if rgb[0] == rgb[1] == rgb[2] == 0 or rgb[0] == rgb[1] == rgb[2] == 255:
        return 0

    a = rgb[0] - 0.5
    b = 0.5 - rgb[1]

    if a < 0:
        if b > 0:
            if atan(a / b) * 180 / pi >= 45:
                red = 0
            else:
                red = atan(a / b) * 180 / pi
        elif b == 0:
            red = 360 - 270
        else:
            red = 360 - (atan(a / b) * 180 / pi + 180)
    else:
        if b > 0:
            red = 360 - atan(a / b) * 180 / pi
        elif b == 0:
            red = 360 - 90
        else:
            red = 360 - (atan(a / b) * 180 / pi + 180)

    c = rgb[2] - 0.5
    d = rgb[1] - 0.5

    if c < 0:
        if d > 0:
            blue = 180 - atan(c / d) * 180 / pi
        elif d == 0:
            blue = 270
        else:
            blue = 360 - atan(c / d) * 180 / pi
    else:
        if d > 0:
            blue = 180 - atan(c / d) * 180 / pi
        elif d == 0:
            blue = 90
        else:
            blue = atan(-c / d) * 180 / pi

    if red == 0:
        return blue
    elif blue == 315:
        return red
    else:
        return (red + blue) / 2


boi = cm.jet(np.arange(100))
jet_angles = [rgb_to_angle(i) for i in boi]


def angle_to_jet(angle):
    """
    Returns the index of the jet angle array nearest to the input angle, giving the index of the jet colour scale that
    most closely matches the rgb value that formed the input angle.
    angle : int or float
    """
    return int(find_nearest(jet_angles, angle))


def rgb_image_to_jet_array(img_array):
    """
    Converts a 2D array of rgb values to a 2D array of ints between 0 and 100 based on the jet colour scale.
    img_array : 2D array of length-3 tuples or lists of ints or floats
    """

    # initialise array
    array = []
    # iterate over pixels in image
    for i in range(len(img_array)):
        progress(i, len(img_array))
        for j in range(len(img_array[i])):
            # normalise rgb values
            zero = img_array[i][j][0] / 255
            one = img_array[i][j][1] / 255
            two = img_array[i][j][2] / 255
            # convert rgb to jet value using rgb_to_angle and angle_to_jet and append to the array to form the
            # 2D matrix or jet values
            array.append(angle_to_jet(rgb_to_angle((zero, one, two))))
    return array


text_file = './scale.txt'
file = open(text_file, 'r')
NDIM = 3
rgb_list = []
scale_list = []
for line in file:
    nums = line[:-1].split(',')
    rgb_list.append((int(nums[0]), int(nums[1]), int(nums[2])))
    scale_list.append(int(nums[3]))

a = np.asarray(rgb_list)
a.shape = int(a.size / NDIM), NDIM


def find_closest_3d(point):
    d = ((a - point) ** 2).sum(axis=1)
    ndx = d.argsort()
    return scale_list[ndx[0]]


def rgb_image_to_hsi_array(img_array):
    array = []
    truth = isinstance(img_array, np.ma.MaskedArray)
    if truth:
        mask = img_array.mask[:, :, 0]
    # iterate over pixels in image
    for i in range(len(img_array)):
        progress(i, len(img_array))
        for j in range(len(img_array[i])):
            # normalise rgb values
            zero = img_array[i][j][0]
            one = img_array[i][j][1]
            two = img_array[i][j][2]
            if truth:
                if not mask[i][j]:
                    closest = find_closest_3d((zero, one, two))
                    array.append(closest+CORRECTION_VALUE)
                else:
                    array.append(str('NaN'))
            else:
                array.append(find_closest_3d((zero, one, two))+CORRECTION_VALUE)
    return np.asarray(array).reshape((480, 640))


