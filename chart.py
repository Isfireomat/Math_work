
from PyQt5.QtWidgets import QApplication, QMainWindow,QLabel, QTableWidgetItem,QFileDialog, QDialog,QMessageBox, QAction,QPushButton,QShortcut
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from chart_form import Ui_Dialog
import sys
import random
from chart_defs import *
import matplotlib.ticker as ticker 
import math

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        
class chart(QDialog, Ui_Dialog): 
    def __init__(self,osn,masiv,comments,params, parent=None):
        super().__init__(parent)
        self.setupUi(self) 
        self.sc = MplCanvas(self, width=100, height=100, dpi=100)  
        self.First=True
        self.sp=osn.saved_params 
        self.number,self.days,self.medium=1,5,0
        self.horizontalLayout.addWidget(self.sc)
        self.comboBox.addItems(['Первый график','Второй график','Третий график'])
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.update_masiv(masiv,comments,params)
        self.spinBox.valueChanged.connect(self.spinBox_valueChanged)
        self.spinBox_2.valueChanged.connect(lambda:self.spinBox_valueChanged(value=0,combo=1))
        self.spinBox_3.valueChanged.connect(self.sp3ch)
        self.verticalSlider.valueChanged.connect(lambda:self.on_value_changed(0,1))
        self.verticalSlider_2.valueChanged.connect(lambda:self.on_value_changed(0,2))
        self.horizontalSlider.valueChanged.connect(lambda:self.on_value_changed(1,1))
        self.horizontalSlider_2.valueChanged.connect(lambda:self.on_value_changed(1,2))
        
        
    def update_masiv(self,masiv,comments,params):    
        
        self.masiv=get_analytics_list(masiv)
        self.first_titles,self.second_titles=get_title(self.masiv,comments,params)
        self.generate_chart(self.number,combo=0)
        
    def sp3ch(self): 
        self.sp["Related values"]=self.spinBox_3.value()
        self.definition()

        
    def save_saved_params(self):
        self.sp["number"]=self.number
        self.sp["normal"]=self.normal
        self.sp["last values"]=self.days
        self.sp["Related values"]=self.spinBox_3.value()
        self.sp["v1"]=self.v1
        self.sp["v2"]=self.v2
        self.sp["v3"]=self.v3
        self.sp["v4"]=self.v4
        
    def set_saved_params(self):
        if self.First: self.First=False
        else: return
        try:
            if not self.sp["number"]: return False 
            
            components=[self.comboBox,self.spinBox,self.spinBox_2,self.spinBox_3,self.verticalSlider,self.verticalSlider_2,self.horizontalSlider,self.horizontalSlider_2]
            for i in range(len(components)):
                components[i].blockSignals(True)
                
            self.number=self.sp["number"]
            self.comboBox.setCurrentIndex(self.number-1)
            self.normal=self.sp["normal"]
            self.spinBox.setValue(self.normal)
            self.days=self.sp["last values"]
            self.spinBox_2.setValue(self.days)
            self.spinBox_3.setValue(self.sp["Related values"])
            self.v1=self.sp["v1"]
            self.verticalSlider.setValue(self.v1)
            self.v2=self.sp["v2"]
            self.verticalSlider_2.setValue(self.v2)
            self.v3=self.sp["v3"]
            self.v4=self.sp["v4"]
            self.horizontalSlider.setValue(self.v4)
            self.horizontalSlider_2.setValue(self.v3)
            
            for i in range(len(components)):
                components[i].blockSignals(False)
            
        except:
            return False
        return True
    
    def definition(self,change=0):
        try:
            self.tableWidget_3.clearContents() 
            points,gaps=get_group_point(self.y,self.spinBox_3.value() if not change else change)
            self.generate_table_3(points,gaps)
            self.sp["bc"]=True
        except:
            pass    

    def on_value_changed(self,v,n):
        if v==0:
            self.v1=self.verticalSlider.value()
            self.v2=self.verticalSlider_2.value()
            if self.v2>self.v1:
                if n==1: self.verticalSlider_2.setValue(self.v1)
                if n==2: self.verticalSlider.setValue(self.v2)                    
        if v==1:
            self.v4=self.horizontalSlider.value()
            self.v3=self.horizontalSlider_2.value()
            if self.v3>self.v4:
                if n==1: self.horizontalSlider_2.setValue(self.v4)
                if n==2: self.horizontalSlider.setValue(self.v3)    
        self.medium=get_medium_nubmer(self.y[self.v3-self.h_min:self.v4-self.h_min+1])
        self.generate_table_2()
        self.generate_table_1()
        self.update_plot()
        
    def on_combobox_changed(self, index):
        self.number=index+1
        self.tableWidget_3.clearContents() 
        self.generate_chart(self.number,combo=1)
        
    def spinBox_valueChanged(self,value, combo=0):
        self.generate_chart(self.number,combo=combo)
        
    def get_normal(self):
        if self.First and self.sp["normal"]:
            self.normal=self.sp["normal"]
        else:
            self.normal=self.spinBox.value()
        return self.normal
    
    def get_days(self):
        if self.First and self.sp["last values"]:
            self.days=self.sp["last values"]
        else:
            self.days=self.spinBox_2.value()
        return self.days
    
    def set_standart_significance(self,):
        self.verticalSlider.setMinimum(int(min(self.y)))
        self.verticalSlider.setMaximum(math.ceil(max(self.y)))    
        self.verticalSlider_2.setMinimum(int(min(self.y)))
        self.verticalSlider_2.setMaximum(math.ceil(max(self.y)))
        self.horizontalSlider.setMinimum(int(min(self.x)))
        self.horizontalSlider.setMaximum(math.ceil(max(self.x)))    
        self.h_min=int(min(self.x))
        self.horizontalSlider_2.setMinimum(int(min(self.x)))
        self.horizontalSlider_2.setMaximum(math.ceil(max(self.x)))
        try:
            self.v4
        except:    
            self.horizontalSlider.setValue(math.ceil(max(self.x)))
            self.horizontalSlider_2.setValue(int(min(self.x)))
            self.v4=math.ceil(max(self.x))
            self.v3=int(min(self.x))
        try:
            self.v1
        except:    
            self.verticalSlider.setValue(math.ceil(max(self.y)))
            self.verticalSlider_2.setValue(int(min(self.y)))
            self.v1=math.ceil(max(self.y))
            self.v2=int(min(self.y))
        
    
    def generate_chart(self,number,combo=0):
        function=[get_before_days_sum_list,get_before_days_list,get_sum_columns_list]
        masiv=function[(self.number if self.set_saved_params() else number)-1](self.masiv)    
        self.spinBox_2.setMaximum(len(masiv))
        self.y,self.x=pruning(masiv,list(range(1,len(masiv)+1)),self.get_days())
        if self.sp["bc"]: self.definition()
        self.set_standart_significance()  
        self.spinBox.setMaximum(max(self.y))
        self.medium=get_medium_nubmer(self.y[self.v3-self.h_min:self.v4-self.h_min+1])
        self.generate_table_2()
        self.generate_table_1()
        self.update_plot()  
        
    def update_plot(self):
        self.sc.axes.clear()
        self.sc.axes.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        self.sc.axes.xaxis.set_major_locator(ticker.MultipleLocator(1))
        self.sc.axes.set_xlabel('Номер значения')
        self.sc.axes.set_ylabel('Значение') 
        self.sc.axes.plot(self.x, self.y,color='blue', linewidth=4, markersize=10,linestyle='-', marker='p')
        self.sc.axes.set_xticks(self.x)
        if self.number>1:
            self.sc.axes.set_xticklabels(self.first_titles[min(self.x)-1:max(self.x)])
        else:
            self.sc.axes.set_xticklabels(self.second_titles[min(self.x)-1:max(self.x)])
        self.sc.axes.plot([self.v3,self.v4], [self.medium,self.medium],color='black', linewidth=2,linestyle='-')
        self.sc.axes.plot([min(self.x),max(self.x)], [self.get_normal(),self.get_normal()],color='red', linewidth=2,linestyle='-')
        self.sc.axes.fill_between([self.v3,self.v4], min(min(self.y),self.normal), max(max(self.y),self.normal), color='yellow', alpha=0.25, label='Зона 2') 
        self.sc.axes.fill_between(self.x, self.v1, self.v2, color='green', alpha=0.25, label='Зона 1') 
        self.sc.draw()
        self.save_saved_params()

    def clear_plot(self):
        self.sc.axes.clear()
        self.sc.draw()
    
    def generate_table_1(self):
        masiv=get_points_significance_dict([v for v,i in zip(self.y,self.x) if v>=self.v2 and v<=self.v1 and i>=self.v3 and i<=self.v4])
        self.tableWidget.clearContents() 
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(len(masiv)+1)
        self.tableWidget.setItem(0,0,QTableWidgetItem("значение"))
        self.tableWidget.setItem(0,1,QTableWidgetItem("количество"))
        for i,v in enumerate(masiv.keys()):
            self.tableWidget.setItem(i+1,0,QTableWidgetItem(str(v)))
            self.tableWidget.setItem(i+1,1,QTableWidgetItem(str(masiv[v])))
        self.tableWidget.resizeRowsToContents()  
        
    def generate_table_2(self): 
        dictionary=get_deviation_dict(self.y[self.v3-self.h_min:self.v4-self.h_min+1],self.get_normal())
        self.tableWidget_2.clearContents() 
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setRowCount(6)
        self.tableWidget_2.setItem(0,0,QTableWidgetItem("Меньше нормы"))
        self.tableWidget_2.setItem(0,1,QTableWidgetItem("Выше нормы"))
        self.tableWidget_2.setItem(1,0,QTableWidgetItem(str(dictionary["less"])))
        self.tableWidget_2.setItem(1,1,QTableWidgetItem(str(dictionary["more"])))
        self.tableWidget_2.setItem(3,0,QTableWidgetItem("Сумма отклонения:"))
        self.tableWidget_2.setItem(3,1,QTableWidgetItem(str(dictionary["deviation"])))
        self.tableWidget_2.setItem(5,0,QTableWidgetItem("Среднее значение:"))
        self.tableWidget_2.setItem(5,1,QTableWidgetItem(str(self.medium)))
        self.tableWidget_2.resizeRowsToContents()  

    def generate_table_3(self,points,gaps):
        self.tableWidget_3.setColumnCount(max(2,len(gaps)+1))
        self.tableWidget_3.setRowCount(2)
        self.tableWidget_3.setItem(0,0,QTableWidgetItem(f"Количество точек: {points}"))
        self.tableWidget_3.setItem(1,0,QTableWidgetItem("Промежутки значений:"))
        for i in range(len(gaps)):
            self.tableWidget_3.setItem(1,i+1,QTableWidgetItem(gaps[i]))
        self.tableWidget_3.resizeRowsToContents()
        self.tableWidget_3.resizeColumnsToContents()
        
if __name__=="__main__":
    app = QApplication(sys.argv)
    main = chart([])
    main.show()
    sys.exit(app.exec_())