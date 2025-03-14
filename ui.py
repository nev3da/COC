# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1160, 375)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(91, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.window_name_label = QtWidgets.QLineEdit(self.widget_3)
        self.window_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.window_name_label.setObjectName("window_name_label")
        self.horizontalLayout_3.addWidget(self.window_name_label)
        spacerItem1 = QtWidgets.QSpacerItem(91, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.widget_3)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_7 = QtWidgets.QWidget(self.tab)
        self.widget_7.setObjectName("widget_7")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_7)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget_4 = QtWidgets.QWidget(self.widget_7)
        self.widget_4.setStyleSheet("")
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.widget_6 = QtWidgets.QWidget(self.widget_4)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem2 = QtWidgets.QSpacerItem(244, 19, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.label_7 = QtWidgets.QLabel(self.widget_6)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_5.addWidget(self.label_7)
        self.execute_time_1 = QtWidgets.QLineEdit(self.widget_6)
        self.execute_time_1.setMaximumSize(QtCore.QSize(40, 16777215))
        self.execute_time_1.setObjectName("execute_time_1")
        self.horizontalLayout_5.addWidget(self.execute_time_1)
        self.label_8 = QtWidgets.QLabel(self.widget_6)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_5.addWidget(self.label_8)
        spacerItem3 = QtWidgets.QSpacerItem(244, 19, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.verticalLayout_2.addWidget(self.widget_6)
        self.widget_5 = QtWidgets.QWidget(self.widget_4)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem4 = QtWidgets.QSpacerItem(205, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.label_5 = QtWidgets.QLabel(self.widget_5)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.collect_interval = QtWidgets.QLineEdit(self.widget_5)
        self.collect_interval.setMaximumSize(QtCore.QSize(40, 16777215))
        self.collect_interval.setObjectName("collect_interval")
        self.horizontalLayout_4.addWidget(self.collect_interval)
        self.label_6 = QtWidgets.QLabel(self.widget_5)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        spacerItem5 = QtWidgets.QSpacerItem(205, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.verticalLayout_2.addWidget(self.widget_5)
        self.widget_2 = QtWidgets.QWidget(self.widget_4)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem6 = QtWidgets.QSpacerItem(133, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.label_3 = QtWidgets.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.unit_1 = QtWidgets.QComboBox(self.widget_2)
        self.unit_1.setMaximumSize(QtCore.QSize(800, 16777215))
        self.unit_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.unit_1.setObjectName("unit_1")
        self.unit_1.addItem("")
        self.unit_1.addItem("")
        self.unit_1.addItem("")
        self.horizontalLayout_2.addWidget(self.unit_1)
        spacerItem7 = QtWidgets.QSpacerItem(132, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem7)
        self.label_4 = QtWidgets.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.number = QtWidgets.QLineEdit(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.number.sizePolicy().hasHeightForWidth())
        self.number.setSizePolicy(sizePolicy)
        self.number.setMaximumSize(QtCore.QSize(80, 16777215))
        self.number.setAlignment(QtCore.Qt.AlignCenter)
        self.number.setObjectName("number")
        self.horizontalLayout_2.addWidget(self.number)
        spacerItem8 = QtWidgets.QSpacerItem(133, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem8)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.widget = QtWidgets.QWidget(self.widget_4)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem9 = QtWidgets.QSpacerItem(90, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem9)
        self.btn_1 = QtWidgets.QPushButton(self.widget)
        self.btn_1.setObjectName("btn_1")
        self.horizontalLayout.addWidget(self.btn_1)
        spacerItem10 = QtWidgets.QSpacerItem(90, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem10)
        self.verticalLayout_2.addWidget(self.widget)
        self.verticalLayout_3.addWidget(self.widget_4)
        self.verticalLayout_4.addWidget(self.widget_7)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget_8 = QtWidgets.QWidget(self.tab_2)
        self.widget_8.setObjectName("widget_8")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_8)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_12 = QtWidgets.QLabel(self.widget_8)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_6.addWidget(self.label_12)
        self.widget_9 = QtWidgets.QWidget(self.widget_8)
        self.widget_9.setObjectName("widget_9")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_9)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem11 = QtWidgets.QSpacerItem(244, 19, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem11)
        self.label_9 = QtWidgets.QLabel(self.widget_9)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_6.addWidget(self.label_9)
        self.execute_time_2 = QtWidgets.QLineEdit(self.widget_9)
        self.execute_time_2.setMaximumSize(QtCore.QSize(40, 16777215))
        self.execute_time_2.setObjectName("execute_time_2")
        self.horizontalLayout_6.addWidget(self.execute_time_2)
        self.label_10 = QtWidgets.QLabel(self.widget_9)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_6.addWidget(self.label_10)
        spacerItem12 = QtWidgets.QSpacerItem(244, 19, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem12)
        self.verticalLayout_6.addWidget(self.widget_9)
        self.widget_11 = QtWidgets.QWidget(self.widget_8)
        self.widget_11.setObjectName("widget_11")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget_11)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem13 = QtWidgets.QSpacerItem(133, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem13)
        self.label_11 = QtWidgets.QLabel(self.widget_11)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_8.addWidget(self.label_11)
        self.unit_2 = QtWidgets.QComboBox(self.widget_11)
        self.unit_2.setMaximumSize(QtCore.QSize(800, 16777215))
        self.unit_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.unit_2.setObjectName("unit_2")
        self.unit_2.addItem("")
        self.unit_2.addItem("")
        self.unit_2.addItem("")
        self.horizontalLayout_8.addWidget(self.unit_2)
        spacerItem14 = QtWidgets.QSpacerItem(132, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem14)
        self.verticalLayout_6.addWidget(self.widget_11)
        self.widget_10 = QtWidgets.QWidget(self.widget_8)
        self.widget_10.setObjectName("widget_10")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget_10)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem15 = QtWidgets.QSpacerItem(90, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem15)
        self.btn_2 = QtWidgets.QPushButton(self.widget_10)
        self.btn_2.setObjectName("btn_2")
        self.horizontalLayout_7.addWidget(self.btn_2)
        spacerItem16 = QtWidgets.QSpacerItem(90, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem16)
        self.verticalLayout_6.addWidget(self.widget_10)
        self.verticalLayout_5.addWidget(self.widget_8)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1160, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "COC-Script"))
        self.label.setText(_translate("MainWindow", "输入窗口名称："))
        self.window_name_label.setText(_translate("MainWindow", "MuMu模拟器12"))
        self.label_2.setText(_translate("MainWindow", "脚本配置"))
        self.label_7.setText(_translate("MainWindow", "运行时间："))
        self.execute_time_1.setText(_translate("MainWindow", "3"))
        self.label_8.setText(_translate("MainWindow", "小时"))
        self.label_5.setText(_translate("MainWindow", "每进行"))
        self.collect_interval.setText(_translate("MainWindow", "4"))
        self.label_6.setText(_translate("MainWindow", "场战斗，收集一次圣水"))
        self.label_3.setText(_translate("MainWindow", "兵种："))
        self.unit_1.setItemText(0, _translate("MainWindow", "女巫"))
        self.unit_1.setItemText(1, _translate("MainWindow", "龙"))
        self.unit_1.setItemText(2, _translate("MainWindow", "变异亡灵"))
        self.label_4.setText(_translate("MainWindow", "总数量（算上预备营）："))
        self.number.setText(_translate("MainWindow", "7"))
        self.btn_1.setText(_translate("MainWindow", "开始"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "标准进攻"))
        self.label_12.setText(_translate("MainWindow", "脚本配置"))
        self.label_9.setText(_translate("MainWindow", "运行时间："))
        self.execute_time_2.setText(_translate("MainWindow", "1"))
        self.label_10.setText(_translate("MainWindow", "小时"))
        self.label_11.setText(_translate("MainWindow", "兵种："))
        self.unit_2.setItemText(0, _translate("MainWindow", "女巫"))
        self.unit_2.setItemText(1, _translate("MainWindow", "龙"))
        self.unit_2.setItemText(2, _translate("MainWindow", "变异亡灵"))
        self.btn_2.setText(_translate("MainWindow", "开始"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "掉杯刷圣水"))
