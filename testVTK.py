import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget
from PyQt5.QtWidgets import QFrame, QVBoxLayout

import vtk
from vtk.util.colors import tomato # type: ignore
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor # type: ignore


class MouseInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, parent=None):
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        # self.AddObserver("MouseMoveEvent", self.OnMouseMove)
        self.AddObserver('LeftButtonReleaseEvent', self.left_button_release_event)
        # self.__obsIDMouseMoveTag = iren.AddObserver("MouseMoveEvent", self.MouseMoveCallback)        
        
    def leftButtonPressEvent(self, obj, event):
        self.OnLeftButtonDown()
    def left_button_release_event(self, obj, event):
        return
    def mouseMoveEvent(self, obj, event):
        return
        self.OnMouseMove()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        # source
        cylinder = vtk.vtkCylinderSource()
        cylinder.SetResolution(200)

        # mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(cylinder.GetOutputPort())

        # actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(tomato)
        actor.RotateX(30.)
        actor.RotateY(-45.)

        # renderer
        ren = vtk.vtkRenderer()
        ren.AddActor(actor)
        ren.SetBackground(0.1, 0.2, 0.4)

        # interactor
        frame = QFrame()
        inter = QVTKRenderWindowInteractor(frame)
        inter.SetInteractorStyle(MouseInteractorStyle())

        ren_win = inter.GetRenderWindow()
        ren_win.AddRenderer(ren)

        ren.ResetCamera()
        ren.GetActiveCamera().Zoom(1.5)

        ren_win.Render()
        inter.Initialize()

        layout = QVBoxLayout()
        layout.addWidget(inter)
        frame.setLayout(layout)
        self.setCentralWidget(frame)

        self.setWindowTitle("Qt VTK")
        self.resize(320, 240)
        self.centerOnScreen()
        self.show()

    def centerOnScreen(self):
        res = QDesktopWidget().screenGeometry()
        self.move((res.width()/2) - (self.frameSize().width()/2),
                  (res.height()/2) - (self.frameSize().height()/2))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Main()
    sys.exit(app.exec_())