import os
import sys

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

import sys

from PyQt5.QtGui import QFont, QIcon

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget, QSpacerItem, \
    QHBoxLayout, QLabel, QSizePolicy, QSplitter, QFrame
from PyQt5.QtCore import Qt, QCoreApplication

from matplotlib_gui import MatplotlibWidget

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support

QApplication.setFont(QFont('Arial', 12))
QApplication.setWindowIcon(QIcon('ico/openai.svg'))


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        # Set window title and size
        self.setWindowTitle("PyQt5 & Matplotlib Example")
        self.setGeometry(100, 100, 800, 600)

        self.__removeFileList = QListWidget()
        self.__removeFileList.setStyleSheet('QListWidget { border: 0 }')

        self.__delBtn = QPushButton('Delete')
        self.__delBtn.clicked.connect(self.__delete)

        self.__clearBtn = QPushButton('Clear')
        self.__clearBtn.clicked.connect(self.__clear)

        lay = QHBoxLayout()
        lay.addWidget(QLabel('Images to Remove'))
        lay.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.MinimumExpanding))
        lay.addWidget(self.__delBtn)
        lay.addWidget(self.__clearBtn)
        lay.setContentsMargins(0, 0, 0, 0)

        menuWidget = QWidget()
        menuWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(menuWidget)
        lay.addWidget(self.__removeFileList)

        rightWidget = QWidget()
        rightWidget.setLayout(lay)

        # Create a vertical layout
        lay = QVBoxLayout()

        dirname_arr = []

        titleLbl = QLabel('Select the images to Remove')
        titleLbl.setFont(QFont('Arial', 14))
        titleLbl.setAlignment(Qt.AlignCenter)

        self.__matplotlibWidget = MatplotlibWidget(dirname_arr=dirname_arr)
        self.__matplotlibWidget.selected.connect(self.__added)
        self.__matplotlibWidget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)

        lay = QVBoxLayout()
        lay.addWidget(titleLbl)
        lay.addWidget(sep)
        lay.addWidget(self.__matplotlibWidget)
        lay.setAlignment(Qt.AlignTop)

        leftWidget = QWidget()
        leftWidget.setLayout(lay)

        mainSplitter = QSplitter()
        mainSplitter.addWidget(leftWidget)
        mainSplitter.addWidget(rightWidget)
        mainSplitter.setOrientation(Qt.Horizontal)
        mainSplitter.setSizes([700, 300])
        mainSplitter.setChildrenCollapsible(False)
        mainSplitter.setHandleWidth(2)
        mainSplitter.setStyleSheet(
            '''
            QSplitter::handle:horizontal
            {
                background: #CCC;
                height: 1px;
            }
            ''')

        # Set the layout to the central widget
        self.setCentralWidget(mainSplitter)

    def __added(self, filenames):
        self.__removeFileList.addItems(filenames)

    def __delete(self):
        filenames = [self.__removeFileList.item(i).text() for i in range(self.__removeFileList.count()) if self.__removeFileList.item(i)]
        for filename in filenames:
            os.remove(filename)
        self.__clear()
        self.__matplotlibWidget.refresh()

    def __clear(self):
        self.__removeFileList.clear()

    def update_plot(self):
        pass
        # Sample data
        # x = np.linspace(0, 10, 100)
        # y = np.sin(x)

        # Clear the old data from the plot and plot the new data
        # self.ax.clear()
        # self.ax.plot(x, y)
        # self.canvas.draw()


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = Window()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print('Fill the dirname_arr with directories containing images')