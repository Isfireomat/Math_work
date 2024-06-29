# import transmutation
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QLabel, QTableWidgetItem,QFileDialog, QDialog,QMessageBox, QAction,QPushButton,QShortcut
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from main_form import Ui_MainWindow
import create_form
import doptable_form 
from defs import *
import queue
from PyQt5.QtCore import pyqtSignal
from chart import chart

class dopt_form(QDialog, doptable_form.Ui_Dialog): 
    data_sent = pyqtSignal(dict)
    def __init__(self,params, parent=None):
        super().__init__(parent)
        self.setupUi(self)  

    def set_params_and_comments(self, params,comments):
        self.params=params
        self.comments=comments
    
class c_form(QDialog, create_form.Ui_Dialog): 
    data_sent = pyqtSignal(dict)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  
        self.pushButton.clicked.connect(self.send_data)
        
    def send_data(self):
        data={
            "day_count":18,
            "chiken_count":6,
            "work_count":3,
            "befor_days":2,
            "cycle_days":9,
            "start_cycle":5,
            "size_sum_masiv":2, 
            "normal":4,
            "file_name":"test"}
        try:
            data["file_name"]=str(self.lineEdit_8.text())
            data["day_count"]=int(self.lineEdit_4.text())
            data["chiken_count"]=int(self.lineEdit_2.text())
            data["befor_days"]=int(self.lineEdit_3.text())
            data["cycle_days"]=int(self.lineEdit_4.text())
            data["start_cycle"]=int(self.lineEdit_5.text())
            data["size_sum_masiv"]=int(self.lineEdit_6.text())
            data["normal"]=int(self.lineEdit_7.text())
            data['work_count']=int(self.lineEdit_9.text())
            self.data_sent.emit(data)
        except Exception as e: print(e)
        self.close()

class main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        self.setupUi(self)
        self.chart_forms=[]
        menubar = self.menuBar()
        self.saved_params={
        "number":None,
        "normal":None,
        "last values":None,
        "Related values":None,
        "v1":None,
        "v2":None,
        "v3":None,
        "v4":None,
        "bc":True
        }
        file_menu = menubar.addMenu('&Меню')
        menu={'&Открыть':self.open,
              '&Создать':self.open_c_form,
              '&Сохранить (Ctrl+S)':self.save,
              '&Сохранить как':self.save_file_as,
              '&Рассчёт (Ctrl+R)':self.update,
              '&Добавить строку (Ctrl++)':self.add_row,
              '&Убрать строку (Ctrl+-)':self.remove_row,
              '&Сокращённая таблица':self.open_doptable,
              '&Реконфигуратор':self.open_configurator,
              '&Графики':self.open_cahrt}
        for i in menu.keys():    
            save_action = QAction(i, self)
            save_action.triggered.connect(menu[i])
            file_menu.addAction(save_action)
        qshortcuts={'Ctrl+S':self.save,
                    'Ctrl+R':self.update,
                    'Ctrl++':self.add_row,
                    'Ctrl+=':self.add_row,
                    'Ctrl+-':self.remove_row}
        for i in qshortcuts.keys():
            shortcut = QShortcut(QKeySequence(i), self)
            shortcut.activated.connect(qshortcuts[i])
        self.params=None
        self.file_name=None
        self.comments=[]
        # self.file_name="masiv.math"
        # self.open()
        # self.open_cahrt()
        
    def open_cahrt(self):    
        if self.file_name:
            
            masiv=self.read()
            errors=isled(masiv,self.params['work_count'])
            solv_masiv=solver(masiv,self.params['day_count'],self.params['cycle_days'],self.params['start_cycle'],self.params['size_sum_masiv'],self.params['normal'],self.params['befor_days'],self.params['work_count'])
            repeat_masiv=find_all_repet(masiv)
            masiv=normolize_masiv(masiv,solv_masiv)
            
            self.chart=chart(self,masiv,self.read_comments(),self.params)
            self.chart_forms.append(self.chart)
            self.chart.show()
    
    def update_charts(self,masiv):
        for i in self.chart_forms:
            i.update_masiv(masiv,self.comments,self.params)    
    
    def open_doptable(self):
        if self.file_name:
            self.dopt_form = dopt_form(self)
            masiv=self.read()
            errors=isled(masiv,self.params['work_count'])
            solv_masiv=solver(masiv,self.params['day_count'],self.params['cycle_days'],self.params['start_cycle'],self.params['size_sum_masiv'],self.params['normal'],self.params['befor_days'],self.params['work_count'])
            repeat_masiv=find_all_repet(masiv)
            masiv=normolize_masiv(masiv,solv_masiv)
            self.dopt_form.set_params_and_comments(self.params,self.comments)
            masiv=abbreviation(masiv)
            render(self.dopt_form,masiv,repeat_masiv,errors=errors,vh_doptable=1)
            self.dopt_form.show()
            
    def closeEvent(self, event):
        self.save()    
    
    def open_configurator(self):
        self.c_form=c_form(self)
        self.c_form.lineEdit_8.setText(str(self.file_name.replace(".math","")))
        self.c_form.lineEdit_4.setText(str(self.params['cycle_days']))
        self.c_form.lineEdit_2.setText(str(self.params['chiken_count']))
        self.c_form.lineEdit_3.setText(str(self.params['befor_days']))
        self.c_form.lineEdit_5.setText(str(self.params['start_cycle']))
        self.c_form.lineEdit_6.setText(str(self.params['size_sum_masiv']))
        self.c_form.lineEdit_7.setText(str(self.params['normal']))
        self.c_form.lineEdit_9.setText(str(self.params['work_count']))
        self.c_form.data_sent.connect(self.reconfig)
        self.c_form.show()
        
    def open_c_form(self):
        self.c_form = c_form(self)
        self.c_form.data_sent.connect(self.create)  
        self.c_form.show()

    def reconfig(self,data):
        masiv=self.read()
        masiv=modify_masiv(masiv,data['chiken_count']-self.params['chiken_count'])
        data.pop('day_count')
        replace_common_keys(self.params,data)
        self.file_name=f"{data['file_name']}.math"
        self.solv_and_render(masiv)
        
    def create(self,data):
        self.params=data
        masiv=[[0 for _ in range(self.params['chiken_count'])]for _ in range(self.params['day_count'])]
        self.file_name=f"{self.params['file_name']}.math"
        self.solv_and_render(masiv)
        
    def add_row(self):
        masiv=self.read()
        masiv.append([0 for _ in range(self.params['chiken_count'])])
        comment=self.read_comments()[::-1][0]
        if comment.isdigit():
            self.comments.append(str(int(comment)+1))
        else: self.comments.append("1")    
        self.params["day_count"]+=1
        self.solv_and_render(masiv)
    
    def remove_row(self):
        try:
            masiv=self.read()
            masiv.pop()
            self.comments.pop()
            self.params["day_count"]-=1
            self.solv_and_render(masiv)
        except: pass
                
    def open(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Math files (*.math)")
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            with open(file_path, 'r') as f:    
                self.file_name=file_path
                params_and_masiv=eval(f.read())
                self.params=params_and_masiv[0]
                masiv=params_and_masiv[1]
                self.comments=params_and_masiv[2]
                errors=isled(masiv,self.params['work_count'])
                solv_masiv=solver(masiv,self.params['day_count'],self.params['cycle_days'],self.params['start_cycle'],self.params['size_sum_masiv'],self.params['normal'],self.params['befor_days'],self.params['work_count'])
                repeat_masiv=find_all_repet(masiv)
                masiv=normolize_masiv(masiv,solv_masiv)
                render(self,masiv,repeat_masiv,errors)    
    
    def save_file_as(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(self, "Сохранение", "", "Math files (*.math)")
        if file_path:
            self.file_name = file_path
            self.save()
            
    def save(self):
        self.solv_and_render(self.read())
        masiv=self.read()
        if len(self.comments)==0: return
        if self.file_name:
            with open(self.file_name,"w") as f:
                f.write(str([self.params,masiv,self.comments]))
        else: self.save_file_as()
    
    def solv_and_render(self,masiv):
        try:
            errors=isled(masiv,self.params['work_count'])
            solv_masiv=solver(masiv,self.params['day_count'],self.params['cycle_days'],self.params['start_cycle'],self.params['size_sum_masiv'],self.params['normal'],self.params['befor_days'],self.params['work_count'])
            repeat_masiv=find_all_repet(masiv)
            masiv=normolize_masiv(masiv,solv_masiv)
            self.update_charts(masiv)
            render(self,masiv,repeat_masiv,errors=errors)
        except Exception as e: print(e)
            
    def update(self):
        self.solv_and_render(self.read())
    
    def read_comments(self):
        right=1
        row_count=self.tableWidget.rowCount()
        comments=[]        
        vertical_headers = []
        for row in range(row_count):
            item = self.tableWidget.verticalHeaderItem(row)
            if item is not None:
                vertical_headers.append(item.text())
                
        for y in range(row_count):
            if vertical_headers[y].isdigit() and not (int(vertical_headers[y])==self.params['cycle_days']-self.params['start_cycle'] and not vertical_headers[y+1].isdigit()):
                comments.append( str(self.tableWidget.item(y, self.tableWidget.columnCount()-2).text()) if self.tableWidget.item(y, self.tableWidget.columnCount()-2) else " ")
        return comments[::-1]
        
    def read(self):
        y=0
        regular=1
        right=1
        row_count=self.tableWidget.rowCount()
        column_count=self.tableWidget.columnCount()-right-2
        masiv=[]
        vertical_headers = []
        for row in range(row_count):
            item = self.tableWidget.verticalHeaderItem(row)
            if item is not None:
                vertical_headers.append(item.text())
        
        self.comments=[]    
        for y in range(row_count):
            if vertical_headers[y].isdigit() and not (int(vertical_headers[y])==self.params['cycle_days']-self.params['start_cycle'] and not vertical_headers[y+1].isdigit()):
                masiv.append([int(1 if self.tableWidget.item(y, x).text()=="1" else 0) for x in range(regular,column_count)])
        self.params['day_count']=len(masiv)
        self.comments=self.read_comments()
        return masiv[::-1] 
    
def create_JSON(self):
    button = self.sender()
    if button:
        values = button.property('values')
        nazva=""
        l=self.read_comments()[::-1]
        l.remove(' ')
        if len(l): nazva=l[0]
        
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(self, "Сохранение", nazva, "JSON (*.json)")
        if file_path:
            grouped_on_dict(values,self.params['size_sum_masiv'],file_path)         
def set_button(self,values):
    buttton = QPushButton('JSON')
    buttton.clicked.connect(lambda:create_JSON(self))
    buttton.setProperty('values', values)
    self.tableWidget.setCellWidget(self.tableWidget.rowCount()-1, self.tableWidget.columnCount()-1, buttton)
        
def render(self,masiv,repeat_masiv,errors,vh_doptable=0,comments=[]):
    self.tableWidget.setUpdatesEnabled(False)
    self.tableWidget.setSortingEnabled(False)
    header = self.tableWidget.horizontalHeader()
    header.setMinimumSectionSize(20)
    self.tableWidget.clearContents()
    self.tableWidget.setRowCount(0) 
    self.tableWidget.setColumnCount(0) 
    horizontal_headers = [str(i) if i else " " for i in range(self.params['chiken_count']+1)] + [" ","Комментарии","JSON"]
    vertical_headers = [] 

    Boldfont = QFont()
    Boldfont.setBold(True)
    regular=1 
    right=1
    columns_count=self.params['chiken_count']
    days=[]
    days_2=[]
    day=return_days(masiv)
    if vh_doptable: day+=self.params['cycle_days']-self.params['befor_days']
    self.tableWidget.setColumnCount(columns_count+4)
    horizontal_headers.append(" ")
    colors=color_generat(columns_count,self.params["size_sum_masiv"])
    q_3=queue.LifoQueue()
    for i in self.comments:
        q_3.put(i)
        
    for i in masiv[::-1]:
        
        if type(i)==dict:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            if i["type"]=="analitika":
                for _ in range(2): vertical_headers.append(" ")
                self.tableWidget.setSpan(self.tableWidget.rowCount()-1, 0+regular, 1, columns_count)
                label = QLabel()
                label.setAlignment(Qt.AlignmentFlag.AlignLeft)

                text = f'''
                <span style="color: red;">{i["sum_even"]}</span>&nbsp;
                <span style="color: green;">{i["sum_odd"]}</span>&nbsp;&nbsp;
                <span style="color: green;">{i["above_normal"]}/</span>
                <span style="color: red;">{i["below_normal"]}</span>&nbsp;&nbsp;
                <span style="color: green;">{i["sum_above_normal"]}</span>&nbsp;
                <span style="color: red;">{i["sum_below_normal"]}</span>&nbsp;
                <span>Повторы {i["repetitions_day"]} ({i["repetitions_all"]})</span>
                '''
                font = QFont()
                font.setPointSize(14) 
                label.setFont(font)
                label.setText(text)
                self.tableWidget.setCellWidget(self.tableWidget.rowCount()-1, 0 + regular, label)
        
                self.tableWidget.insertRow(self.tableWidget.rowCount())
                
                for x,j in enumerate(i["size_sum_masiv"]):
                    self.tableWidget.setSpan(self.tableWidget.rowCount()-1, x*self.params["size_sum_masiv"]+regular, 1, self.params["size_sum_masiv"] if columns_count-(x+1)*self.params["size_sum_masiv"]-regular>0 else columns_count-x*self.params["size_sum_masiv"])
                    self.tableWidget.setItem(self.tableWidget.rowCount()-1, x*self.params["size_sum_masiv"]+regular, QTableWidgetItem(str(f"{i['size_sum_masiv'][x]}  ({'+' if i['otstup_masiv'][x]>0 else ''}{i['otstup_masiv'][x]})" )))
                    
                    self.tableWidget.item    (self.tableWidget.rowCount()-1, x*self.params["size_sum_masiv"]+regular).setBackground(colors[x*self.params["size_sum_masiv"]+regular])
                    self.tableWidget.item(self.tableWidget.rowCount()-1, x*self.params["size_sum_masiv"]+regular).setForeground(QColor(0, 0, 0))
                    self.tableWidget.item(self.tableWidget.rowCount()-1, x*self.params["size_sum_masiv"]+regular).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                
                
                
                q,q_2 = queue.LifoQueue(),queue.LifoQueue()
                try:
                    for bd,pred,sumator in zip(i['before_days'],i['prediction'],i['sumator_before_days']): 
                        q.put(f'''
                                <span style="color: red;">{pred["sum_even"]}</span>&nbsp;
                                <span style="color: green;">{pred["sum_odd"]}</span>&nbsp;&nbsp;<br>
                                <span style="color: green;">{pred["above_normal"]}/</span>
                                <span style="color: red;">{pred["below_normal"]}</span>&nbsp;&nbsp;
                                <span style="color: green;">{pred["sum_above_normal"]}</span>&nbsp;
                                <span style="color: red;">{pred["sum_below_normal"]}</span>&nbsp;<br>
                                <span>({bd})</span>&nbsp;<span style="color: blue;">{sumator}</span>
                                ''')
                except: pass
                for sc in i['sum_columns']:
                    q_2.put(f"({sc})")
                days.append(q)
                days_2.append(q_2)
                self.tableWidget.insertRow(self.tableWidget.rowCount())
            normal=normal_generate(self.params["normal"])
            for x,j in enumerate(i['column_sums']):
                self.tableWidget.setItem(self.tableWidget.rowCount()-1, x + regular, QTableWidgetItem(str(j)))
                if j in normal:               self.tableWidget.item(self.tableWidget.rowCount()-1, x+regular).setBackground(QColor(255, 255, 0))
                elif j>self.params["normal"]: self.tableWidget.item(self.tableWidget.rowCount()-1, x+regular).setBackground(QColor(0, 255, 0))
                else:                         self.tableWidget.item(self.tableWidget.rowCount()-1, x+regular).setBackground(QColor(255, 0, 0))
                self.tableWidget.item(self.tableWidget.rowCount()-1, x+regular).setTextAlignment(Qt.AlignmentFlag.AlignCenter)    
                self.tableWidget.item(self.tableWidget.rowCount()-1, x+regular).setForeground(QColor(0, 0, 0))
                self.tableWidget.setColumnWidth(x+regular, 1)
            
            if i['type']=="analitika": 
                self.tableWidget.setItem(self.tableWidget.rowCount()-1, len(i['column_sums']) + regular + 1, QTableWidgetItem(str(i["number"])))
                
            set_button(self,i['column_sums']) 
                
            vertical_headers.append(f"|{i['dop_date']}" if 'dop_date' in i else " ")
            if i["type"]=="analitika" and not ('dop_date' in i):
                self.tableWidget.setItem(self.tableWidget.rowCount()-1, 0, QTableWidgetItem(f"({i['before_days_sum']})"))
                
            
            
        else:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            if q and not q.empty():
                label = QLabel()
                label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                text=q.get()
                label.setText(text)
                self.tableWidget.setCellWidget(self.tableWidget.rowCount()-1, 0 + 0, label)
                
            text=' '.join([d.get() for d in days_2[::-1] if not d.empty()])  
            self.tableWidget.setItem(self.tableWidget.rowCount()-1, self.tableWidget.columnCount()-3, QTableWidgetItem(f"{text}"))
            
            if not q_3.empty(): self.tableWidget.setItem(self.tableWidget.rowCount()-1, self.tableWidget.columnCount()-2, QTableWidgetItem(str(q_3.get())))
            
            vertical_headers.append(str((day-1)%self.params['cycle_days']%self.params['start_cycle']+(self.params['cycle_days']-self.params['start_cycle']+1) if day>self.params['cycle_days'] else day))
            k=repeat_masiv.get()
            error=errors.get()
            
            for x,j in enumerate(i):
                self.tableWidget.setItem(self.tableWidget.rowCount()-1, x + regular, QTableWidgetItem(str(j) if j else " "))
                self.tableWidget.item(self.tableWidget.rowCount()-1, x + regular).setFont(Boldfont)
                
                self.tableWidget.item(self.tableWidget.rowCount()-1, x+regular).setBackground(colors[x])    
                self.tableWidget.item(self.tableWidget.rowCount()-1, x+regular).setForeground(QColor(0, 0, 0))
                self.tableWidget.setColumnWidth(x+regular, 1)
                if k[x]: self.tableWidget.item(self.tableWidget.rowCount()-1, x+regular).setBackground(QColor(0, 255, 0)) 
                elif error: self.tableWidget.item(self.tableWidget.rowCount()-1, x+regular).setBackground(QColor(255, 0, 0))
                else:    self.tableWidget.item(self.tableWidget.rowCount()-1, x+regular).setBackground(colors[x])

                self.tableWidget.item(self.tableWidget.rowCount()-1, x+regular).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
              
            day-=1
    
    self.tableWidget.resizeRowsToContents()  
    self.tableWidget.setHorizontalHeaderLabels(horizontal_headers)
    self.tableWidget.setVerticalHeaderLabels(vertical_headers)
    self.tableWidget.setUpdatesEnabled(True)
    self.tableWidget.setSortingEnabled(True)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    player = main()
    player.show()
    sys.exit(app.exec())