from pathlib import Path

import imagesize
import matplotlib.pyplot as plt
import numpy as np
# Import Packages
import pandas as pd
from PIL import Image
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.path import Path as mplPath
# Import libraries
from matplotlib.widgets import LassoSelector


class MatplotlibWidget(QWidget):
    selected = pyqtSignal(list)
    
    def __init__(self, dirname_arr):
        super(MatplotlibWidget, self).__init__()
        self.__initUi(dirname_arr)
        
    def __initUi(self, dirname_arr):
        self.__wrapper = MatplotlibWrapper(dirname_arr)

        self.__figure = self.__wrapper.get_figure()
        self.__ax = self.__wrapper.get_ax()

        self.__collection = self.__wrapper.get_points()

        self.__canvas = FigureCanvas(self.__figure)

        self.__xys = self.__collection.get_offsets()
        self.__lasso = LassoSelector(self.__ax, onselect=self.onselect)
        self.__ind = []

        self.__toolbar = NavigationToolbar(self.__canvas, self)
        
        lay = QVBoxLayout()

        lay.addWidget(self.__toolbar)
        lay.addWidget(self.__canvas)
        lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout(lay)

    def onselect(self, verts):
        path = mplPath(verts)
        self.__ind = np.nonzero(path.contains_points(self.__xys))[0]
        self.__canvas.draw_idle()

        self.__collection = self.__wrapper.get_points()
        self.__img_meta_df = self.__wrapper.get_img_meta_df()

        filenames = []
        for _ in self.__ind:
            w, h = self.__collection.get_offsets().data[_]
            img_file = self.__img_meta_df.iloc[_, 0]
            filenames.append(img_file)
        
        self.selected.emit(filenames)

    def refresh(self):
        pass
        # self.__wrapper.set_img_meta_df()
        # print(len(self.__wrapper.get_img_meta_df().FileName.to_list()))
        # self.__canvas.draw()

    def get_canvas(self):
        return self.__canvas


class MatplotlibWrapper:
    def __init__(self, dirname_arr):
        super(MatplotlibWrapper, self).__init__()
        self.__initVal(dirname_arr)
        self.initGraph()

    def __initVal(self, dirname_arr):
        self.__figure = plt.figure(figsize=(8, 8))
        self.__ax = self.__figure.add_subplot(111)
        self.__dirname_arr = dirname_arr
        self.__img_meta_df = None
        self.__points = None

    def initGraph(self):
        self.set_img_meta_df()

        # self.__img_meta_df.head()

        self.__ax.set_title("Image Resolution")
        self.__ax.set_xlabel("Width", size=14)
        self.__ax.set_ylabel("Height", size=14)

        # event
        # self.__figure.canvas.mpl_connect('key_press_event', self.accept)

        # selector
        # Add interaction

        self.__figure.canvas.mpl_connect('pick_event', self.on_pick)

    def set_img_meta_df(self):
        img_meta = {}
        for dirname in self.__dirname_arr:
            imgs = []
            imgs.extend([img.name for img in Path(dirname).iterdir() if img.suffix == ".jpg" or img.suffix == '.png'])
            for f in imgs:
                relpath_name = dirname + '/' + f
                img_meta[relpath_name] = imagesize.get(relpath_name)

        # Convert it to Dataframe and compute aspect ratio
        self.__img_meta_df = pd.DataFrame.from_dict([img_meta]).T.reset_index().set_axis(['FileName', 'Size'],
                                                                                         axis='columns')
        self.__img_meta_df[["Width", "Height"]] = pd.DataFrame(self.__img_meta_df["Size"].tolist(),
                                                               index=self.__img_meta_df.index)
        self.__img_meta_df["Aspect Ratio"] = round(self.__img_meta_df["Width"] / self.__img_meta_df["Height"], 2)

        self.__ax.clear()

        self.__points = self.__ax.scatter(self.__img_meta_df.Width, self.__img_meta_df.Height, color='blue', alpha=0.5,
                                 s=self.__img_meta_df["Aspect Ratio"] * 100, picker=True)
    # def accept(self, event):
    #     if event.key == "enter":
    #         print('enter')
    #     elif event.key == 'escape':
    #         print('escape')
    #     else:
    #         print(event.key)

    # Show the original image upon picking the point
    def on_pick(self, event):
        ind = event.ind[0]
        w, h = self.__points.get_offsets().data[ind]
        img_file = Path(self.__img_meta_df.iloc[ind, 0])
        if Path(img_file).is_file():
            img = Image.open(Path(img_file))
            figs = plt.figure(figsize=(5, 5))
            axs = figs.add_subplot(111)
            axs.set_title(Path(img_file).name, size=14)
            axs.set_xticks([])
            axs.set_yticks([])
            axs.set_xlabel(f'Dim: {round(w)} x {round(h)}', size=14)
            axs.imshow(img)
            figs.tight_layout()
            figs.show()
            
    def get_figure(self):
        return self.__figure
    
    def get_ax(self):
        return self.__ax

    def get_points(self):
        return self.__points

    def get_img_meta_df(self):
        return self.__img_meta_df