# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\PythonProjects\game_scripts\COC\ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(547, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
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
        self.verticalLayout_3.addWidget(self.widget_3)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_night = QtWidgets.QWidget()
        self.tab_night.setObjectName("tab_night")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_night)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_4 = QtWidgets.QWidget(self.tab_night)
        self.widget_4.setStyleSheet("")
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_2.setContentsMargins(11, 15, 11, 9)
        self.verticalLayout_2.setSpacing(7)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget_4)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 50))
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
        self.night_execute_time = QtWidgets.QSpinBox(self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.night_execute_time.sizePolicy().hasHeightForWidth())
        self.night_execute_time.setSizePolicy(sizePolicy)
        self.night_execute_time.setMinimumSize(QtCore.QSize(60, 0))
        self.night_execute_time.setMaximumSize(QtCore.QSize(80, 16777215))
        self.night_execute_time.setAlignment(QtCore.Qt.AlignCenter)
        self.night_execute_time.setProperty("value", 3)
        self.night_execute_time.setObjectName("night_execute_time")
        self.horizontalLayout_5.addWidget(self.night_execute_time)
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
        self.collect_interval_1 = QtWidgets.QLineEdit(self.widget_5)
        self.collect_interval_1.setMinimumSize(QtCore.QSize(60, 0))
        self.collect_interval_1.setMaximumSize(QtCore.QSize(80, 16777215))
        self.collect_interval_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.collect_interval_1.setAlignment(QtCore.Qt.AlignCenter)
        self.collect_interval_1.setObjectName("collect_interval_1")
        self.horizontalLayout_4.addWidget(self.collect_interval_1)
        self.label_6 = QtWidgets.QLabel(self.widget_5)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.collect_interval_2 = QtWidgets.QLineEdit(self.widget_5)
        self.collect_interval_2.setMinimumSize(QtCore.QSize(60, 0))
        self.collect_interval_2.setMaximumSize(QtCore.QSize(80, 16777215))
        self.collect_interval_2.setAlignment(QtCore.Qt.AlignCenter)
        self.collect_interval_2.setObjectName("collect_interval_2")
        self.horizontalLayout_4.addWidget(self.collect_interval_2)
        self.label_9 = QtWidgets.QLabel(self.widget_5)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_4.addWidget(self.label_9)
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
        self.unit = QtWidgets.QComboBox(self.widget_2)
        self.unit.setMinimumSize(QtCore.QSize(80, 0))
        self.unit.setMaximumSize(QtCore.QSize(800, 16777215))
        self.unit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.unit.setObjectName("unit")
        self.unit.addItem("")
        self.unit.addItem("")
        self.unit.addItem("")
        self.horizontalLayout_2.addWidget(self.unit)
        spacerItem7 = QtWidgets.QSpacerItem(132, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem7)
        self.label_4 = QtWidgets.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.night_number = QtWidgets.QSpinBox(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.night_number.sizePolicy().hasHeightForWidth())
        self.night_number.setSizePolicy(sizePolicy)
        self.night_number.setMinimumSize(QtCore.QSize(60, 0))
        self.night_number.setMaximumSize(QtCore.QSize(80, 16777215))
        self.night_number.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.night_number.setAlignment(QtCore.Qt.AlignCenter)
        self.night_number.setProperty("value", 8)
        self.night_number.setObjectName("night_number")
        self.horizontalLayout_2.addWidget(self.night_number)
        spacerItem8 = QtWidgets.QSpacerItem(133, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem8)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.widget = QtWidgets.QWidget(self.widget_4)
        self.widget.setObjectName("widget")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem9 = QtWidgets.QSpacerItem(90, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem9)
        self.night_btn = QtWidgets.QPushButton(self.widget)
        self.night_btn.setObjectName("night_btn")
        self.horizontalLayout_6.addWidget(self.night_btn)
        spacerItem10 = QtWidgets.QSpacerItem(90, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem10)
        self.verticalLayout_2.addWidget(self.widget)
        self.verticalLayout.addWidget(self.widget_4)
        self.tabWidget.addTab(self.tab_night, "")
        self.tab_day = QtWidgets.QWidget()
        self.tab_day.setObjectName("tab_day")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_day)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget_7 = QtWidgets.QWidget(self.tab_day)
        self.widget_7.setStyleSheet("")
        self.widget_7.setObjectName("widget_7")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_7)
        self.verticalLayout_4.setContentsMargins(-1, 15, -1, 9)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_10 = QtWidgets.QLabel(self.widget_7)
        self.label_10.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_4.addWidget(self.label_10)
        self.widget_8 = QtWidgets.QWidget(self.widget_7)
        self.widget_8.setObjectName("widget_8")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget_8)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem11 = QtWidgets.QSpacerItem(244, 19, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem11)
        self.label_11 = QtWidgets.QLabel(self.widget_8)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_7.addWidget(self.label_11)
        self.day_execute_time = QtWidgets.QSpinBox(self.widget_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.day_execute_time.sizePolicy().hasHeightForWidth())
        self.day_execute_time.setSizePolicy(sizePolicy)
        self.day_execute_time.setMinimumSize(QtCore.QSize(100, 0))
        self.day_execute_time.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.day_execute_time.setAlignment(QtCore.Qt.AlignCenter)
        self.day_execute_time.setMaximum(180)
        self.day_execute_time.setSingleStep(10)
        self.day_execute_time.setProperty("value", 30)
        self.day_execute_time.setObjectName("day_execute_time")
        self.horizontalLayout_7.addWidget(self.day_execute_time)
        self.label_12 = QtWidgets.QLabel(self.widget_8)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_7.addWidget(self.label_12)
        self.widget_9 = QtWidgets.QWidget(self.widget_8)
        self.widget_9.setObjectName("widget_9")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_9)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem12 = QtWidgets.QSpacerItem(135, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem12)
        self.label_13 = QtWidgets.QLabel(self.widget_9)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout.addWidget(self.label_13)
        self.day_number = QtWidgets.QLineEdit(self.widget_9)
        self.day_number.setMinimumSize(QtCore.QSize(100, 0))
        self.day_number.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.day_number.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.day_number.setObjectName("day_number")
        self.horizontalLayout.addWidget(self.day_number)
        spacerItem13 = QtWidgets.QSpacerItem(134, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem13)
        self.horizontalLayout_7.addWidget(self.widget_9)
        self.verticalLayout_4.addWidget(self.widget_8)
        self.widget_10 = QtWidgets.QWidget(self.widget_7)
        self.widget_10.setObjectName("widget_10")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_10)
        self.verticalLayout_6.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_14 = QtWidgets.QLabel(self.widget_10)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_6.addWidget(self.label_14)
        self.widget_13 = QtWidgets.QWidget(self.widget_10)
        self.widget_13.setObjectName("widget_13")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_13)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.widget_12 = QtWidgets.QWidget(self.widget_13)
        self.widget_12.setObjectName("widget_12")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget_12)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem14)
        self.label_15 = QtWidgets.QLabel(self.widget_12)
        self.label_15.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_8.addWidget(self.label_15)
        self.gold = QtWidgets.QLineEdit(self.widget_12)
        self.gold.setMinimumSize(QtCore.QSize(120, 0))
        self.gold.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.gold.setAlignment(QtCore.Qt.AlignCenter)
        self.gold.setObjectName("gold")
        self.horizontalLayout_8.addWidget(self.gold)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem15)
        self.label_16 = QtWidgets.QLabel(self.widget_12)
        self.label_16.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_8.addWidget(self.label_16)
        self.elixir = QtWidgets.QLineEdit(self.widget_12)
        self.elixir.setMinimumSize(QtCore.QSize(120, 0))
        self.elixir.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.elixir.setAlignment(QtCore.Qt.AlignCenter)
        self.elixir.setObjectName("elixir")
        self.horizontalLayout_8.addWidget(self.elixir)
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem16)
        self.verticalLayout_7.addWidget(self.widget_12)
        self.widget_14 = QtWidgets.QWidget(self.widget_13)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.widget_14.setFont(font)
        self.widget_14.setObjectName("widget_14")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.widget_14)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem17)
        self.label_17 = QtWidgets.QLabel(self.widget_14)
        self.label_17.setMinimumSize(QtCore.QSize(0, 0))
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_11.addWidget(self.label_17)
        self.oil = QtWidgets.QLineEdit(self.widget_14)
        self.oil.setMinimumSize(QtCore.QSize(120, 0))
        self.oil.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.oil.setFont(font)
        self.oil.setAlignment(QtCore.Qt.AlignCenter)
        self.oil.setObjectName("oil")
        self.horizontalLayout_11.addWidget(self.oil)
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem18)
        self.verticalLayout_7.addWidget(self.widget_14)
        self.verticalLayout_6.addWidget(self.widget_13)
        self.verticalLayout_4.addWidget(self.widget_10)
        self.widget_11 = QtWidgets.QWidget(self.widget_7)
        self.widget_11.setObjectName("widget_11")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.widget_11)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem19 = QtWidgets.QSpacerItem(90, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem19)
        self.day_btn = QtWidgets.QPushButton(self.widget_11)
        self.day_btn.setObjectName("day_btn")
        self.horizontalLayout_10.addWidget(self.day_btn)
        spacerItem20 = QtWidgets.QSpacerItem(90, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem20)
        self.verticalLayout_4.addWidget(self.widget_11)
        self.verticalLayout_5.addWidget(self.widget_7)
        self.tabWidget.addTab(self.tab_day, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 547, 26))
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
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "输入窗口名称："))
        self.window_name_label.setText(_translate("MainWindow", "MuMu模拟器12"))
        self.label_2.setText(_translate("MainWindow", "脚本配置"))
        self.label_7.setText(_translate("MainWindow", "运行时间："))
        self.label_8.setText(_translate("MainWindow", "小时"))
        self.label_5.setText(_translate("MainWindow", "每进行"))
        self.collect_interval_1.setText(_translate("MainWindow", "4"))
        self.label_6.setText(_translate("MainWindow", "场战斗 + "))
        self.collect_interval_2.setText(_translate("MainWindow", "0"))
        self.label_9.setText(_translate("MainWindow", "场送分，收集一次圣水"))
        self.label_3.setText(_translate("MainWindow", "兵种："))
        self.unit.setItemText(0, _translate("MainWindow", "女巫"))
        self.unit.setItemText(1, _translate("MainWindow", "龙"))
        self.unit.setItemText(2, _translate("MainWindow", "变异亡灵"))
        self.label_4.setText(_translate("MainWindow", "总数量："))
        self.night_btn.setText(_translate("MainWindow", "开始"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_night), _translate("MainWindow", "夜世界"))
        self.label_10.setText(_translate("MainWindow", "脚本配置"))
        self.label_11.setText(_translate("MainWindow", "运行时间："))
        self.label_12.setText(_translate("MainWindow", "分钟"))
        self.label_13.setText(_translate("MainWindow", "兵营大小："))
        self.day_number.setText(_translate("MainWindow", "300"))
        self.label_14.setText(_translate("MainWindow", "跳过资源低于如下阈值的敌人："))
        self.label_15.setText(_translate("MainWindow", "金币："))
        self.gold.setText(_translate("MainWindow", "1 000 000"))
        self.label_16.setText(_translate("MainWindow", "圣水："))
        self.elixir.setText(_translate("MainWindow", "1 000 000"))
        self.label_17.setText(_translate("MainWindow", "黑油："))
        self.oil.setText(_translate("MainWindow", "10 000"))
        self.day_btn.setText(_translate("MainWindow", "开始"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_day), _translate("MainWindow", "主世界"))
