# version 1.2
# 윈도우 타이틀 및 어플리케이션 상단 노출 문구 변경(Disease Detected Agency -> Disease Diagnosis Agency)
# 노출 문구 변경에 따른 self.fsm0_label['title']의 frame_width 수정
# self.fsm0_line_edit['search']에 PlaceholderText(기본 텍스트) 기능 추가
# 디버그 스크립트 수정

from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from threading import Thread
from datetime import datetime
import pandas as pd
import random
import sys
import time
from recommendation import main_function


class Application(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize class constants
        self.DATA = pd.read_csv('./crawling_data/cleaned_disease_content.csv')
        self.font = 'Ariel'
        self.options = {}
        # Initialize class variables
        self.current_time = datetime.now()
        self.elements = None
        self.modified_elements = None
        self.fsm_conditions = None

        # Initialize Qt-Objects
        self.fsm0_label = {'title': QLabel(self), 'line-edit_notice': QLabel(self), 'result_notice': QLabel(self),
                           'eraser_notice': QLabel(self), 'options_notice': QLabel(self), 'exit_notice': QLabel(self)}
        self.fsm1_label = {'reset_notice': QLabel(self), 'cancel_notice': QLabel(self), 'allow_notice': QLabel(self),
                           'line-edit-0_notice': QLabel(self), 'elements_notice': QLabel(self),
                           'question': QLabel(self), 'question_allow': QLabel(self), 'question_deny': QLabel(self)}
        self.fsm0_button = {'search': QPushButton(self), 'eraser': QPushButton(self), 'options': QPushButton(self),
                            'exit': QPushButton(self)}
        self.fsm1_button = {'reset': QPushButton(self), 'cancel': QPushButton(self), 'allow': QPushButton(self), 
                            'question_allow': QPushButton(self), 'question_deny': QPushButton(self)}
        self.fsm0_line_edit = {'search': QLineEdit(self)}
        self.fsm1_line_edit = {'elements': QLineEdit(self)}
        self.fsm0_text_browser = QTextBrowser(self)

        # Setup GUI(Graphic User Interface) environments
        window_name = f'DDA(Disease Diagnosis Agency) Client - {datetime.now().strftime("%Y")}/{datetime.now().strftime("%m")}/{datetime.now().strftime("%d")}'
        self.initializeWindow(name=f'{window_name}', rgb=(0, 0, 0), w=1080, h=860)
        self.initializeVariables()
        self.initializeStaticObjects()
        self.initializeObject()

        # Connected signal function
        self.fsm0_line_edit['search'].textChanged.connect(self.signal_detected_word_length)
        self.fsm0_line_edit['search'].returnPressed.connect(self.signal_btn_search_clicked)
        self.fsm0_button['search'].clicked.connect(self.signal_btn_search_clicked)
        self.fsm0_button['eraser'].clicked.connect(self.signal_btn_eraser_clicked)
        self.fsm0_button['options'].clicked.connect(self.signal_btn_options_clicked)
        self.fsm0_button['exit'].clicked.connect(self.signal_btn_exit_clicked)
        self.fsm1_button['reset'].clicked.connect(self.signal_btn_reset_clicked)
        self.fsm1_button['cancel'].clicked.connect(self.signal_btn_cancel_clicked)
        self.fsm1_button['allow'].clicked.connect(self.signal_btn_allow_clicked)
        self.fsm1_button['question_allow'].clicked.connect(self.signal_btn_question_allow_clicked)
        self.fsm1_button['question_deny'].clicked.connect(self.signal_btn_question_deny_clicked)
        self.fsm1_line_edit['elements'].textChanged.connect(self.signal_fsm1_lineedit0_text_changed)

        # Execute thread modules
        while True:
            try:
                thread_title = Thread(target=self.launchThread, name='thread_title')
                thread_title.daemon = True
                thread_title.start()
            except Exception as E:
                print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Failed to launched the "{thread_title.name}".. restart after 5 seconds.\nError: {E}')
                time.sleep(5)
            else:
                print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Success to launched the "{thread_title.name}".')
                break

    def initializeWindow(self, **kwargs):
        """
        name: window 이름 설정  (default: Window) (type: str)
        rgb: window 배경 색상 설정    (default: (255, 255, 255)) (type: tuple)
        w: window 가로 길이 설정  (default: 640) (type: int)
        h: window 세로 길이 설정  (default: 480) (type: int)
        m: window 시작 좌표 설정  (default: False) (type: bool)
        mx: window 시작 x좌표 설정    (default: 0) (type: int)
        my: window 시작 y좌표 설정    (default: 0) (type: int)
        """
        try:
            self.options['name'] = kwargs['name'] if 'name' in kwargs else 'Window'
            self.options['rgb'] = kwargs['rgb'] if 'rgb' in kwargs else (255, 255, 255)
            self.options['width'] = kwargs['w'] if 'w' in kwargs else 640
            self.options['width'] = 640 if self.options['width'] < 640 else self.options['width']
            self.options['height'] = kwargs['h'] if 'h' in kwargs else 480
            self.options['height'] = 480 if self.options['height'] < 480 else self.options['height']
            self.options['move'] = kwargs['m'] if 'm' in kwargs else False
            self.options['move_x'] = kwargs['mx'] if 'mx' in kwargs else 0
            self.options['move_y'] = kwargs['my'] if 'my' in kwargs else 0

            self.setWindowTitle(self.options['name'])
            if self.options['move']:
                self.move(self.options['move_x'], self.options['move_y'])
            self.resize(self.options['width'], self.options['height'])
            self.setStyleSheet(f'background-color: rgb{self.options["rgb"]}')
            # 사용자가 Window 크기를 조절하지 못하도록 막는다.
            self.setFixedSize(self.options['width'], self.options['height'])
            # APP Icon 설정
            self.setWindowIcon(QtGui.QIcon('./app_icon/icon_stethoscope.png'))
        except Exception as E:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Unknown error occurred in "{sys._getframe().f_code.co_name}()"\n\t\t\t\t\t  {E}')
            self.close()
        else:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Success to initialize window settings.')

    def initializeVariables(self):
        try:
            self.elements = 10
            self.modified_elements = self.elements
            self.fsm_conditions = [True, {'main': False, 'reset': False, 'cancel': False, 'allow': False}]
        except Exception as E:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Unknown error occurred in "{sys._getframe().f_code.co_name}()"\n\t\t\t\t\t  {E}')
        else:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Success to initialize variables.')

    def initializeStaticObjects(self):
        try:
            font = self.fsm0_label['title'].font()
            font.setFamily(self.font)
            font.setBold(True)
            font.setPointSize(20)
            self.fsm0_label['title'].setText('Disease Diagnosis Agency')
            self.fsm0_label['title'].setGeometry((self.options['width'] / 2) - (400 / 2), 20, 400, 30)
            self.fsm0_label['title'].setStyleSheet('color: rgb(255, 255, 255)')
            self.fsm0_label['title'].setAlignment(Qt.AlignCenter)
            self.fsm0_label['title'].setFont(font)
            font.setBold(False)
            font.setPointSize(18)
            self.fsm0_line_edit['search'].setPlaceholderText('증상을 입력해주세요')
            self.fsm0_line_edit['search'].setGeometry(50, 80, self.options['width'] - 100 - 100 - 50, 50)
            self.fsm0_line_edit['search'].setStyleSheet('color: rgb(255, 255, 255)')
            self.fsm0_line_edit['search'].setAlignment(Qt.AlignLeft)
            self.fsm0_line_edit['search'].setFont(font)
            font.setPointSize(13)
            self.fsm0_label['line-edit_notice'].setText('Please enter a keyword in line-edit')
            self.fsm0_label['line-edit_notice'].setGeometry(50, 140, 280, 30)
            self.fsm0_label['line-edit_notice'].setStyleSheet('color: rgb(255, 0, 0)')
            self.fsm0_label['line-edit_notice'].setAlignment(Qt.AlignLeft)
            self.fsm0_label['line-edit_notice'].setFont(font)
            font.setBold(True)
            font.setPointSize(13)
            self.fsm0_button['search'].setGeometry(self.options['width'] - 100 - 50, 80, 100, 50)
            self.fsm0_button['search'].setStyleSheet('background: rgb(30, 30, 30)')
            self.fsm0_button['search'].setIcon(QtGui.QIcon('./app_icon/icon_magnifier.png'))
            self.fsm0_button['search'].setIconSize(QSize(40, 40))
            self.fsm0_button['search'].setToolTip('입력한 증상을 수반하는 질병을 검색합니다.')
            font.setPointSize(20)
            self.fsm0_label['result_notice'].setText('진단 결과')
            self.fsm0_label['result_notice'].setGeometry(50, 200, self.options['width'] - 100, 50)
            self.fsm0_label['result_notice'].setStyleSheet('color: rgb(255, 255, 255)')
            self.fsm0_label['result_notice'].setAlignment(Qt.AlignCenter)
            self.fsm0_label['result_notice'].setFont(font)
            font.setPointSize(15)
            self.fsm0_text_browser.setText('')
            self.fsm0_text_browser.setGeometry(50, 250, self.options['width'] - 100, self.options['height'] - 480)
            # self.fsm0_text_browser.setGeometry(50, 250, self.options['width'] - 100, 100)
            self.fsm0_text_browser.setStyleSheet('color: rgb(255, 255, 255)')
            self.fsm0_text_browser.setFont(font)
            # FSM-0 Eraser 버튼 및 텍스트
            font.setPointSize(10)
            self.fsm0_label['eraser_notice'].setText('Erase')
            self.fsm0_label['eraser_notice'].setGeometry(self.options['width'] - 250, self.options['height'] - 140, 60, 30)
            self.fsm0_label['eraser_notice'].setStyleSheet('color: rgb(255, 255, 255)')
            self.fsm0_label['eraser_notice'].setAlignment(Qt.AlignCenter)
            self.fsm0_label['eraser_notice'].setFont(font)
            self.fsm0_label['eraser_notice'].setStyleSheet('color: rgb(255, 255, 255)')
            self.fsm0_button['eraser'].setGeometry(self.options['width'] - 250, self.options['height'] - 110, 60, 60)
            self.fsm0_button['eraser'].setStyleSheet('background: rgb(150, 150, 150)')
            self.fsm0_button['eraser'].setIcon(QtGui.QIcon('./app_icon/icon_eraser.png'))
            self.fsm0_button['eraser'].setIconSize(QSize(30, 30))
            self.fsm0_button['eraser'].setToolTip('진단 결과 기록을 삭제합니다.')
            # FSM-0 Options 버튼 및 텍스트
            self.fsm0_label['options_notice'].setText('Options')
            self.fsm0_label['options_notice'].setGeometry(self.options['width'] - 180, self.options['height'] - 140, 60, 30)
            self.fsm0_label['options_notice'].setStyleSheet('color: rgb(255, 255, 255)')
            self.fsm0_label['options_notice'].setAlignment(Qt.AlignCenter)
            self.fsm0_label['options_notice'].setFont(font)
            self.fsm0_button['options'].setGeometry(self.options['width'] - 180, self.options['height'] - 110, 60, 60)
            self.fsm0_button['options'].setStyleSheet('background: rgb(150, 150, 150)')
            self.fsm0_button['options'].setIcon(QtGui.QIcon('./app_icon/icon_options.png'))
            self.fsm0_button['options'].setIconSize(QSize(30, 30))
            self.fsm0_button['options'].setToolTip('어플리케이션과 관련된 설정을 할 수 있습니다.')
            # FSM-0 Exit 버튼 및 텍스트
            self.fsm0_label['exit_notice'].setText('Exit')
            self.fsm0_label['exit_notice'].setGeometry(self.options['width'] - 110, self.options['height'] - 140, 60, 30)
            self.fsm0_label['exit_notice'].setStyleSheet('color: rgb(255, 255, 255)')
            self.fsm0_label['exit_notice'].setAlignment(Qt.AlignCenter)
            self.fsm0_label['exit_notice'].setFont(font)
            self.fsm0_button['exit'].setGeometry(self.options['width'] - 110, self.options['height'] - 110, 60, 60)
            self.fsm0_button['exit'].setStyleSheet('background: rgb(150, 150, 150)')
            self.fsm0_button['exit'].setIcon(QtGui.QIcon('./app_icon/icon_exit.png'))
            self.fsm0_button['exit'].setIconSize(QSize(30, 30))
            self.fsm0_button['exit'].setToolTip('어플리케이션을 종료합니다.')
            # FSM-1 elements 라벨 및 라인에디트
            font.setPointSize(15)
            self.fsm1_label['elements_notice'].setText('최대 검색 결과 수')
            self.fsm1_label['elements_notice'].setGeometry(50, 100, 200, 30)
            self.fsm1_label['elements_notice'].setStyleSheet('color: rgb(255, 255, 255)')
            self.fsm1_label['elements_notice'].setAlignment(Qt.AlignLeft)
            self.fsm1_label['elements_notice'].setFont(font)
            self.fsm1_line_edit['elements'].setText(str(self.elements))
            self.fsm1_line_edit['elements'].setGeometry((self.options['width'] / 2), 100, 100, 30)
            self.fsm1_line_edit['elements'].setStyleSheet('color: rgb(255, 255, 255)')
            self.fsm1_line_edit['elements'].setAlignment(Qt.AlignLeft)
            self.fsm1_line_edit['elements'].setFont(font)
            self.fsm1_label['line-edit-0_notice'].setText('')
            self.fsm1_label['line-edit-0_notice'].setGeometry((self.options['width'] / 2), 140, 200, 30)
            self.fsm1_label['line-edit-0_notice'].setStyleSheet('color: rgb(255, 0, 0)')
            self.fsm1_label['line-edit-0_notice'].setAlignment(Qt.AlignLeft)
            font.setPointSize(13)
            self.fsm1_label['line-edit-0_notice'].setFont(font)

            # FSM-1 Reset 버튼 및 테스트
            font.setPointSize(10)
            self.fsm1_label['reset_notice'].setText('Reset')
            self.fsm1_label['reset_notice'].setGeometry(self.options['width'] - 250, self.options['height'] - 140, 60, 30)
            self.fsm1_label['reset_notice'].setStyleSheet('color: rgb(255, 255, 255)')
            self.fsm1_label['reset_notice'].setAlignment(Qt.AlignCenter)
            self.fsm1_label['reset_notice'].setFont(font)
            self.fsm1_button['reset'].setGeometry(self.options['width'] - 250, self.options['height'] - 110, 60, 60)
            self.fsm1_button['reset'].setStyleSheet('background: rgb(150, 150, 150)')
            self.fsm1_button['reset'].setIcon(QtGui.QIcon('./app_icon/icon_reset.png'))
            self.fsm1_button['reset'].setIconSize(QSize(30, 30))
            self.fsm1_button['reset'].setToolTip('모든 설정을 초기화합니다.')
            # FSM-1 Cancel 버튼 및 텍스트
            self.fsm1_label['cancel_notice'].setText('Cancel')
            self.fsm1_label['cancel_notice'].setGeometry(self.options['width'] - 180, self.options['height'] - 140, 60, 30)
            self.fsm1_label['cancel_notice'].setStyleSheet('color: rgb(255, 255, 255)')
            self.fsm1_label['cancel_notice'].setAlignment(Qt.AlignCenter)
            self.fsm1_label['cancel_notice'].setFont(font)
            self.fsm1_button['cancel'].setGeometry(self.options['width'] - 180, self.options['height'] - 110, 60, 60)
            self.fsm1_button['cancel'].setStyleSheet('background: rgb(150, 150, 150)')
            self.fsm1_button['cancel'].setIcon(QtGui.QIcon('./app_icon/icon_cancel.png'))
            self.fsm1_button['cancel'].setIconSize(QSize(30, 30))
            self.fsm1_button['cancel'].setToolTip('검색 화면으로 돌아갑니다.')
            # FSM-1 Allow 버튼 및 텍스트
            self.fsm1_label['allow_notice'].setText('Allow')
            self.fsm1_label['allow_notice'].setGeometry(self.options['width'] - 110, self.options['height'] - 140, 60, 30)
            self.fsm1_label['allow_notice'].setStyleSheet('color: rgb(255, 255, 255)')
            self.fsm1_label['allow_notice'].setAlignment(Qt.AlignCenter)
            self.fsm1_label['allow_notice'].setFont(font)
            self.fsm1_button['allow'].setGeometry(self.options['width'] - 110, self.options['height'] - 110, 60, 60)
            self.fsm1_button['allow'].setStyleSheet('background: rgb(150, 150, 150)')
            self.fsm1_button['allow'].setIcon(QtGui.QIcon('./app_icon/icon_allow.png'))
            self.fsm1_button['allow'].setIconSize(QSize(30, 30))
            self.fsm1_button['allow'].setToolTip('설정을 변경합니다.')
            font.setPointSize(20)
            self.fsm1_label['question'].setGeometry((self.options['width'] / 2) - 250, (self.options['height'] / 2) - 200, 500, 30)
            self.fsm1_label['question'].setStyleSheet('color: rgb(255, 255, 255)')
            self.fsm1_label['question'].setAlignment(Qt.AlignCenter)
            self.fsm1_label['question'].setFont(font)
            font.setPointSize(12)
            self.fsm1_label['question_allow'].setText('네')
            self.fsm1_label['question_allow'].setGeometry((self.options['width'] / 2) - 150, (self.options['height'] / 2) - 150, 60, 30)
            self.fsm1_label['question_allow'].setStyleSheet('color: rgb(0, 255, 0)')
            self.fsm1_label['question_allow'].setAlignment(Qt.AlignCenter)
            self.fsm1_label['question_allow'].setFont(font)
            self.fsm1_button['question_allow'].setGeometry((self.options['width'] / 2) - 150, (self.options['height'] / 2) - 115, 60, 60)
            self.fsm1_button['question_allow'].setStyleSheet('background: rgb(150, 150, 150)')
            self.fsm1_button['question_allow'].setIconSize(QSize(30, 30))
            self.fsm1_button['question_allow'].setIcon(QtGui.QIcon('./app_icon/icon_allow.png'))
            self.fsm1_label['question_deny'].setText('아니오')
            self.fsm1_label['question_deny'].setGeometry((self.options['width'] / 2) + 100, (self.options['height'] / 2) - 150, 60, 30)
            self.fsm1_label['question_deny'].setStyleSheet('color: rgb(255, 0, 0)')
            self.fsm1_label['question_deny'].setAlignment(Qt.AlignCenter)
            self.fsm1_label['question_deny'].setFont(font)
            self.fsm1_button['question_deny'].setGeometry((self.options['width'] / 2) + 100, (self.options['height'] / 2) - 115, 60, 60)
            self.fsm1_button['question_deny'].setStyleSheet('background: rgb(150, 150, 150)')
            self.fsm1_button['question_deny'].setIconSize(QSize(30, 30))
            self.fsm1_button['question_deny'].setIcon(QtGui.QIcon('./app_icon/icon_cancel.png'))
        except Exception as E:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Unknown error occurred in "{sys._getframe().f_code.co_name}()"\n\t\t\t\t\t  {E}')
            self.close()
        else:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Success to initialize static objects.')

    def initializeObject(self):
        try:
            # FSM-0 라인 에디트
            self.fsm0_line_edit['search'].setText('')
            self.fsm0_line_edit['search'].setVisible(self.fsm_conditions[0])
            self.fsm0_line_edit['search'].setVisible(self.fsm_conditions[0])
            self.fsm0_label['line-edit_notice'].setVisible(self.fsm_conditions[0])
            self.fsm0_label['line-edit_notice'].setEnabled(self.fsm_conditions[0])
            # FSM-0 검색 버튼
            self.fsm0_button['search'].setVisible(self.fsm_conditions[0])
            self.fsm0_button['search'].setEnabled(False)
            # FSM-0 검색 결과
            self.fsm0_label['result_notice'].setVisible(self.fsm_conditions[0])
            self.fsm0_label['result_notice'].setEnabled(self.fsm_conditions[0])
            self.fsm0_text_browser.setVisible(self.fsm_conditions[0])
            self.fsm0_text_browser.setEnabled(self.fsm_conditions[0])
            # FSM-0 Eraser 버튼 및 텍스트
            self.fsm0_label['eraser_notice'].setVisible(self.fsm_conditions[0])
            self.fsm0_label['eraser_notice'].setEnabled(self.fsm_conditions[0])
            self.fsm0_button['eraser'].setVisible(self.fsm_conditions[0])
            self.fsm0_button['eraser'].setEnabled(self.fsm_conditions[0])
            # FSM-0 Options 버튼 및 텍스트
            self.fsm0_label['options_notice'].setVisible(self.fsm_conditions[0])
            self.fsm0_label['options_notice'].setEnabled(self.fsm_conditions[0])
            self.fsm0_button['options'].setVisible(self.fsm_conditions[0])
            self.fsm0_button['options'].setEnabled(self.fsm_conditions[0])
            # FSM-0 Exit 버튼 및 텍스트
            self.fsm0_label['exit_notice'].setVisible(self.fsm_conditions[0])
            self.fsm0_label['exit_notice'].setEnabled(self.fsm_conditions[0])
            self.fsm0_button['exit'].setVisible(self.fsm_conditions[0])
            self.fsm0_button['exit'].setEnabled(self.fsm_conditions[0])

            # FSM-1 elements 라벨 및 라인 에디트
            self.fsm1_label['elements_notice'].setVisible(self.fsm_conditions[1]['main'])
            self.fsm1_label['elements_notice'].setEnabled(self.fsm_conditions[1]['main'])
            self.fsm1_line_edit['elements'].setVisible(self.fsm_conditions[1]['main'])
            self.fsm1_line_edit['elements'].setEnabled(self.fsm_conditions[1]['main'])
            self.fsm1_label['line-edit-0_notice'].setText('')
            self.fsm1_label['line-edit-0_notice'].setVisible(self.fsm_conditions[1]['main'])
            self.fsm1_label['line-edit-0_notice'].setEnabled(self.fsm_conditions[1]['main'])
            # FSM-1 Reset 버튼 및 텍스트
            self.fsm1_label['reset_notice'].setVisible(self.fsm_conditions[1]['main'])
            self.fsm1_label['reset_notice'].setEnabled(self.fsm_conditions[1]['main'])
            self.fsm1_button['reset'].setVisible(self.fsm_conditions[1]['main'])
            self.fsm1_button['reset'].setEnabled(self.fsm_conditions[1]['main'])
            # FSM-1 Cancel 버튼 및 텍스트
            self.fsm1_label['cancel_notice'].setVisible(self.fsm_conditions[1]['main'])
            self.fsm1_label['cancel_notice'].setEnabled(self.fsm_conditions[1]['main'])
            self.fsm1_button['cancel'].setVisible(self.fsm_conditions[1]['main'])
            self.fsm1_button['cancel'].setEnabled(self.fsm_conditions[1]['main'])
            # FSM-1 Allow 버튼 및 텍스트
            self.fsm1_label['allow_notice'].setVisible(self.fsm_conditions[1]['main'])
            self.fsm1_label['allow_notice'].setEnabled(self.fsm_conditions[1]['main'])
            self.fsm1_button['allow'].setVisible(self.fsm_conditions[1]['main'])
            self.fsm1_button['allow'].setEnabled(self.fsm_conditions[1]['main'])

            # FSM1 - Question
            if self.fsm_conditions[1]['reset']:
                self.fsm1_label['question'].setText('설정을 초기화하시겠습니까?')
            elif self.fsm_conditions[1]['allow']:
                self.fsm1_label['question'].setText('변경된 설정을 적용하시겠습니까?')
            self.fsm1_label['question'].setVisible(self.fsm_conditions[1]['reset'] or self.fsm_conditions[1]['allow'])
            self.fsm1_label['question'].setEnabled(self.fsm_conditions[1]['reset'] or self.fsm_conditions[1]['allow'])

            self.fsm1_label['question_allow'].setVisible(self.fsm_conditions[1]['reset'] or self.fsm_conditions[1]['allow'])
            self.fsm1_label['question_allow'].setEnabled(self.fsm_conditions[1]['reset'] or self.fsm_conditions[1]['allow'])
            self.fsm1_label['question_deny'].setVisible(self.fsm_conditions[1]['reset'] or self.fsm_conditions[1]['allow'])
            self.fsm1_label['question_deny'].setEnabled(self.fsm_conditions[1]['reset'] or self.fsm_conditions[1]['allow'])
            self.fsm1_button['question_allow'].setVisible(self.fsm_conditions[1]['reset'] or self.fsm_conditions[1]['allow'])
            self.fsm1_button['question_allow'].setEnabled(self.fsm_conditions[1]['reset'] or self.fsm_conditions[1]['allow'])
            self.fsm1_button['question_deny'].setVisible(self.fsm_conditions[1]['reset'] or self.fsm_conditions[1]['allow'])
            self.fsm1_button['question_deny'].setEnabled(self.fsm_conditions[1]['reset'] or self.fsm_conditions[1]['allow'])
        except Exception as E:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Unknown error occurred in "{sys._getframe().f_code.co_name}()"\n\t\t\t\t\t  {E}')
            self.initializeVariables()
            self.initializeStaticObjects()
        else:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Success to initialize objects.')

    # Signal-function: Line-Edit 단어 입력 감지
    def signal_detected_word_length(self):
        try:
            # 특수문자가 입력된 경우 지움.
            word = self.fsm0_line_edit['search'].text()
            for i in range(len(word)):
                if ord(word[i]) in range(33, 44) or ord(word[i]) in range(45, 48) or ord(word[i]) in range(58, 65) or ord(word[i]) in range(91, 97) or ord(word[i]) in range(123, 128):
                    self.fsm0_line_edit['search'].setText(word[:-1])

            word_length = len(self.fsm0_line_edit['search'].text())
            if word_length > 0:
                self.fsm0_label['line-edit_notice'].setVisible(False)
                self.fsm0_button['search'].setEnabled(True)
                self.fsm0_button['search'].setStyleSheet('background: rgb(150, 150, 150)')
            else:
                self.fsm0_label['line-edit_notice'].setVisible(True)
                self.fsm0_button['search'].setEnabled(False)
                self.fsm0_button['search'].setStyleSheet('background: rgb(30, 30, 30)')
        except Exception as E:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Unknown error occurred in "{sys._getframe().f_code.co_name}()"\n\t\t\t\t\t  {E}')

    # "Search" 버튼 클릭시 이하 이벤트 실행
    def signal_btn_search_clicked(self):
        def remove_continuous_english(data, threshold):
            data = data.split('\n')
            for i in range(len(data)):
                for j in range(len(data[i]) - threshold):
                    if 65 <= ord(data[i][j]) <= 122:
                        count = 0
                        for k in range(j, j + threshold):
                            if 65 <= ord(data[i][k]) <= 122:
                                count += 1
                            else:
                                break
                        if count >= 5:
                            data[i] = data[i][:j]
                            break
                    else:
                        continue
            renewed_word = ''
            for i in range(len(data)):
                renewed_word = '\n'.join([renewed_word, data[i]])

            return renewed_word[1:]

        if len(self.fsm0_line_edit['search'].text()):
            org_symptom = self.fsm0_line_edit['search'].text()
            symptom = org_symptom.replace(',', ' ').split()
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Debug # keywords: {len(symptom)}{symptom}')
            self.fsm0_line_edit['search'].setText('')
            self.fsm0_label['line-edit_notice'].setVisible(True)
            self.fsm0_button['search'].setEnabled(False)
            self.fsm0_button['search'].setStyleSheet('color: rgb(0, 0, 0); background: rgb(30, 30, 30)')
            self.fsm0_label['result_notice'].setVisible(True)
            self.fsm0_label['result_notice'].setStyleSheet(f'color: rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})')
            try:
                ret_val = self.create_duplication_data(data=symptom)
            except Exception as E:
                print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Unknown error occurred in "{sys._getframe().f_code.co_name}()"\n\t\t\t\t\t  {E}')
                self.fsm0_label['result_notice'].setText(f'"{org_symptom}"에 대한 진단 결과 "0"건')
                self.fsm0_text_browser.setText('데이터가 없습니다.')
                self.fsm0_text_browser.setStyleSheet('color: rgb(255, 0, 0)')
            else:
                words_length = ret_val.split('\n')
                print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Debug # words_length: {len(words_length)}{words_length}')
                # 학명 제거를 위한 n개 이상의 연속적인 영문 제거
                # threshold=n 은 n개 이상 등장시 학명으로 간주하고 지우겠다는 의미
                ret_val = remove_continuous_english(data=ret_val, threshold=5)
                items = len(ret_val.split('\n'))
                if len(words_length) > 1:
                    self.fsm0_label['result_notice'].setText(f'"{org_symptom}"에 대한 진단 결과 "{items}"건')
                    self.fsm0_text_browser.setText(ret_val)
                    self.fsm0_text_browser.setStyleSheet('color: rgb(255, 255, 255)')
                elif len(words_length[0]):
                    self.fsm0_label['result_notice'].setText(f'"{org_symptom}"에 대한 진단 결과 "{items}"건')
                    self.fsm0_text_browser.setText(ret_val)
                    self.fsm0_text_browser.setStyleSheet('color: rgb(255, 255, 255)')
                else:
                    self.fsm0_label['result_notice'].setText(f'"{org_symptom}"에 대한 진단 결과 "0"건')
                    self.fsm0_text_browser.setText('데이터가 없습니다.')
                    self.fsm0_text_browser.setStyleSheet('color: rgb(255, 0, 0)')

    # "Eraser" 버튼 클릭시 이하 이벤트 실행
    def signal_btn_eraser_clicked(self):
        try:
            self.fsm0_label['result_notice'].setText('진단 결과')
            self.fsm0_label['result_notice'].setStyleSheet('color: rgb(255, 255, 255)')
            self.fsm0_text_browser.setText('')
            self.initializeObject()
        except Exception as E:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Unknown error occurred in "{sys._getframe().f_code.co_name}()"\n\t\t\t\t\t  {E}')
        else:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - clicked "eraser" button.')

    # "Options" 버튼 클릭시 이하 이벤트 실행
    def signal_btn_options_clicked(self):
        try:
            self.fsm_conditions = [False, {'main': True, 'reset': False, 'cancel': False, 'allow': False}]
            self.fsm1_line_edit['elements'].setText(str(self.elements))
            self.initializeObject()
        except Exception as E:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Unknown error occurred in "{sys._getframe().f_code.co_name}()"\n\t\t\t\t\t  {E}')
        else:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - clicked "options" button.')

    # "Exit" 버튼 클릭시 이하 이벤트 실행
    def signal_btn_exit_clicked(self):
        try:
            self.close()
        except Exception as E:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Unknown error occurred in "{sys._getframe().f_code.co_name}()"\n\t\t\t\t\t  {E}')
        else:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - clicked "exit" button.')

    # "Reset" 버튼 클릭시 이하 이벤트 실행
    def signal_btn_reset_clicked(self):
        try:
            self.fsm_conditions = [False, {'main': False, 'reset': True, 'cancel': False, 'allow': False}]
            self.initializeObject()
        except Exception as E:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Unknown error occurred in "{sys._getframe().f_code.co_name}()"\n\t\t\t\t\t  {E}')
        else:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - clicked "reset" button.')

    # "Cancel" 버튼 클릭시 이하 이벤트 실행
    def signal_btn_cancel_clicked(self):
        try:
            self.fsm_conditions = [True, {'main': False, 'reset': False, 'cancel': False, 'allow': False}]
            self.initializeObject()
        except Exception as E:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Unknown error occurred in "{sys._getframe().f_code.co_name}()"\n\t\t\t\t\t  {E}')
        else:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - clicked "cancel" button.')

    # "Allow" 버튼 클릭시 이하 이벤트 실행
    def signal_btn_allow_clicked(self):
        try:
            self.fsm_conditions = [False, {'main': False, 'reset': False, 'cancel': False, 'allow': True}]
            self.initializeObject()
        except Exception as E:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Unknown error occurred in "{sys._getframe().f_code.co_name}()"\n\t\t\t\t\t  {E}')
        else:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - clicked "allow" button.')

    # FSM-1 에서 "Reset" 또는 "Allow" 버튼을 클릭한 뒤 "Allow" 버튼 클릭시 이하 이벤트 실행
    def signal_btn_question_allow_clicked(self):
        try:
            # Reset 버튼을 클릭했을 때
            if self.fsm_conditions[1]['reset']:
                self.fsm_conditions = [True, {'main': False, 'reset': False, 'cancel': False, 'allow': False}]
                self.initializeStaticObjects()
                self.initializeVariables()
                self.close()
                self.show()
            # Allow 버튼을 클릭했을 때
            elif self.fsm_conditions[1]['allow']:
                self.fsm_conditions = [True, {'main': False, 'reset': False, 'cancel': False, 'allow': False}]
                # 각종 변수값을 리턴해야함.
                print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - elements: {self.elements} -> {self.modified_elements}')
                self.elements = self.modified_elements

            self.initializeObject()
        except Exception as E:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Unknown error occurred in "{sys._getframe().f_code.co_name}()"\n\t\t\t\t\t  {E}')
        else:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - clicked "question_allow" button.')

    # FSM-1 에서 "Reset" 또는 "Allow" 버튼을 클릭한 뒤 "Deny" 버튼 클릭시 이하 이벤트 실행
    def signal_btn_question_deny_clicked(self):
        try:
            self.fsm_conditions = [False, {'main': True, 'reset': False, 'cancel': False, 'allow': False}]
            self.initializeObject()
        except Exception as E:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Unknown error occurred in "{sys._getframe().f_code.co_name}()"\n\t\t\t\t\t  {E}')
        else:
            print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - clicked "question_deny" button.')

    def signal_fsm1_lineedit0_text_changed(self):
        word = self.fsm1_line_edit['elements'].text()
        self.fsm1_label['line-edit-0_notice'].setVisible(False)
        if len(word):
            try:
                if not 48 <= ord(word[-1]) <= 57:
                    word = word[:-1]
                    self.fsm1_line_edit['elements'].setText(word)
                    self.fsm1_label['line-edit-0_notice'].setText('정수만 입력 가능합니다.')
                    self.fsm1_label['line-edit-0_notice'].setVisible(True)
                    self.fsm1_button['allow'].setEnabled(False)
                else:
                    word = int(word)
                    word = str(word)
                    self.fsm1_line_edit['elements'].setText(word)
                    self.fsm1_button['allow'].setEnabled(True)
                if not 1 <= int(word) <= 99:
                    self.fsm1_label['line-edit-0_notice'].setText('1~99 까지만 가능합니다.')
                    self.fsm1_label['line-edit-0_notice'].setVisible(True)
                    self.fsm1_button['allow'].setEnabled(False)
                else:
                    word = int(word)
                    word = str(word)
                    self.fsm1_line_edit['elements'].setText(word)
                    self.fsm1_button['allow'].setEnabled(True)
                self.modified_elements = int(word)
            except Exception as E:
                print(f'[{self.current_time.strftime("%y-%m-%d %H:%M:%S")}] - Unknown error occurred in "{sys._getframe().f_code.co_name}()"\n\t\t\t\t\t  {E}')
                self.fsm1_line_edit['elements'].setText(str(self.elements))
        else:
            self.fsm1_label['line-edit-0_notice'].setText('정수를 입력해주세요.')
            self.fsm1_label['line-edit-0_notice'].setVisible(True)
            self.fsm1_button['allow'].setEnabled(False)

    def create_duplication_data(self, data):
        if len(data) > 1:
            symptom_index = []
            symptom_list = []
            for i in range(len(data)):
                ret_val = main_function(keyword_flag=True, keywords=data[i], elements=self.elements)
                index_container = []
                for j in range(len(ret_val)):
                    index_container.append(ret_val.index[j])
                symptom_index.append(index_container)
                symptom_list.append(ret_val)
            # print(f'symptom_index: {symptom_index}')

            # 중복된 병명만 리스트에 노출시키기 위한 처리
            duplication_list = []
            for i in range(len(symptom_index) - 1):
                for j in range(len(symptom_index[i])):
                    for k in range(i + 1, len(symptom_index)):
                        if symptom_index[i][j] in symptom_index[k]:
                            duplication_list.append(symptom_index[i][j])
            # print(f'duplication_list: {duplication_list}')
            diseases = ''
            for i in range(len(duplication_list)):
                diseases = '\n'.join([diseases, self.DATA['Disease'].iloc[ret_val.index[i]].replace('\n', ' ')])

            return diseases[1:]
        else:
            ret_val = main_function(keyword_flag=True, keywords=data[0], elements=self.elements)
            diseases = ''
            for i in range(len(ret_val)):
                diseases = '\n'.join([diseases, self.DATA['Disease'].iloc[ret_val.index[i]].replace('\n', ' ')])

            return diseases[1:]

    # 스레드 모듈
    def launchThread(self):
        while True:
            self.current_time = datetime.now()
            self.fsm0_label['title'].setStyleSheet(f'color: rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})')
            time.sleep(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Application()
    mainWindow.show()
    sys.exit(app.exec_())
