from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from threading import Thread
from datetime import datetime
import pandas as pd
import pickle
import random
import sys
import time
from recommendation import main_function


class Application(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize class variables
        self.options = {}
        self.font = 'Ariel'
        self.data = pd.read_csv('./crawling_data/cleaned_disease_content.csv')
        self.elements = None
        self.modified_elements = None
        self.fsm_conditions = None

        # Initialize Qt-Objects
        self.fsm0_lbl_title = QLabel(self)
        self.fsm0_lbl_le_notice = QLabel(self)
        self.fsm0_lbl_result_notice = QLabel(self)
        self.fsm0_lbl_eraser_notice = QLabel(self)
        self.fsm0_lbl_options_notice = QLabel(self)
        self.fsm0_lbl_exit_notice = QLabel(self)
        self.fsm1_lbl_reset_notice = QLabel(self)
        self.fsm1_lbl_cancel_notice = QLabel(self)
        self.fsm1_lbl_allow_notice = QLabel(self)
        self.fsm1_lbl_question = QLabel(self)
        self.fsm1_lbl_question_allow_deny = [QLabel(self), QLabel(self)]
        self.fsm1_lbl_elements_notice = QLabel(self)
        self.fsm0_line_edit = QLineEdit(self)
        self.fsm0_btn_search = QPushButton(self)
        self.fsm0_btn_eraser = QPushButton(self)
        self.fsm0_btn_options = QPushButton(self)
        self.fsm0_btn_exit = QPushButton(self)
        self.fsm1_btn_reset = QPushButton(self)
        self.fsm1_btn_cancel = QPushButton(self)
        self.fsm1_btn_allow = QPushButton(self)
        self.fsm1_btn_question_allow_deny = [QPushButton(self), QPushButton(self)]
        self.fsm1_line_edit = [QLineEdit(self)]
        self.fsm1_lbl_line_edit_notice = [QLabel(self)]
        self.fsm0_tb_result = QTextBrowser(self)

        # Setup GUI(Graphic User Interface) environments
        current_time = f'{datetime.now().strftime("%Y")}/{datetime.now().strftime("%m")}/{datetime.now().strftime("%d")}'
        self.initializeWindow(name=f'DDA(Disease Detected Agency) Client - {current_time}', rgb=(0, 0, 0), w=1080, h=860)
        self.initializeVariables()
        self.initializeStaticObjects()
        self.initializeObject()

        # Connected signal function
        self.fsm0_line_edit.textChanged.connect(self.signal_detected_word_length)
        self.fsm0_line_edit.returnPressed.connect(self.signal_btn_search_clicked)
        self.fsm0_btn_search.clicked.connect(self.signal_btn_search_clicked)
        self.fsm0_btn_eraser.clicked.connect(self.signal_btn_eraser_clicked)
        self.fsm0_btn_options.clicked.connect(self.signal_btn_options_clicked)
        self.fsm0_btn_exit.clicked.connect(self.signal_btn_exit_clicked)
        self.fsm1_btn_reset.clicked.connect(self.signal_btn_reset_clicked)
        self.fsm1_btn_cancel.clicked.connect(self.signal_btn_cancel_clicked)
        self.fsm1_btn_allow.clicked.connect(self.signal_btn_allow_clicked)
        self.fsm1_btn_question_allow_deny[0].clicked.connect(self.signal_btn_question_allow_clicked)
        self.fsm1_btn_question_allow_deny[1].clicked.connect(self.signal_btn_question_deny_clicked)
        self.fsm1_line_edit[0].textChanged.connect(self.signal_fsm1_lineedit0_text_changed)

        # Execute thread modules
        while True:
            try:
                thread_title = Thread(target=self.launchThread, name='thread_title')
                thread_title.daemon = True
                thread_title.start()
            except Exception as E:
                print(f'{thread_title.name} error occurred.. {E}')
                continue
            else:
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

    def initializeVariables(self):
        self.elements = 10
        self.modified_elements = self.elements
        self.fsm_conditions = [True, {'main': False, 'reset': False, 'cancel': False, 'allow': False}]

    def initializeStaticObjects(self):
        font = self.fsm0_lbl_title.font()
        font.setFamily(self.font)
        font.setBold(True)
        font.setPointSize(20)
        self.fsm0_lbl_title.setText('Disease Detected Agency')
        self.fsm0_lbl_title.setGeometry((self.options['width'] / 2) - (350 / 2), 20, 350, 30)
        self.fsm0_lbl_title.setAlignment(Qt.AlignCenter)
        self.fsm0_lbl_title.setFont(font)
        font.setBold(False)
        font.setPointSize(18)
        self.fsm0_line_edit.setGeometry(50, 80, self.options['width'] - 100 - 100 - 50, 50)
        self.fsm0_line_edit.setStyleSheet('color: rgb(255, 255, 255)')
        self.fsm0_line_edit.setAlignment(Qt.AlignLeft)
        self.fsm0_line_edit.setFont(font)
        font.setPointSize(13)
        self.fsm0_lbl_le_notice.setText('Please enter a keyword in line-edit')
        self.fsm0_lbl_le_notice.setGeometry(50, 140, 280, 30)
        self.fsm0_lbl_le_notice.setStyleSheet('color: rgb(255, 0, 0)')
        self.fsm0_lbl_le_notice.setAlignment(Qt.AlignLeft)
        self.fsm0_lbl_le_notice.setFont(font)
        font.setBold(True)
        font.setPointSize(13)
        self.fsm0_btn_search.setGeometry(self.options['width'] - 100 - 50, 80, 100, 50)
        self.fsm0_btn_search.setStyleSheet('background: rgb(30, 30, 30)')
        self.fsm0_btn_search.setIcon(QtGui.QIcon('./app_icon/icon_magnifier.png'))
        self.fsm0_btn_search.setIconSize(QSize(40, 40))
        font.setPointSize(20)
        self.fsm0_lbl_result_notice.setText('진단 결과')
        self.fsm0_lbl_result_notice.setGeometry(50, 200, self.options['width'] - 100, 50)
        self.fsm0_lbl_result_notice.setStyleSheet('color: rgb(255, 255, 255)')
        self.fsm0_lbl_result_notice.setAlignment(Qt.AlignCenter)
        self.fsm0_lbl_result_notice.setFont(font)
        font.setPointSize(15)
        self.fsm0_tb_result.setText('')
        self.fsm0_tb_result.setGeometry(50, 250, self.options['width'] - 100, self.options['height'] - 480)
        # self.fsm0_tb_result.setGeometry(50, 250, self.options['width'] - 100, 100)
        self.fsm0_tb_result.setStyleSheet('color: rgb(255, 255, 255)')
        self.fsm0_tb_result.setFont(font)
        # FSM-0 Eraser 버튼 및 텍스트
        font.setPointSize(10)
        self.fsm0_lbl_eraser_notice.setText('Erase')
        self.fsm0_lbl_eraser_notice.setGeometry(self.options['width'] - 250, self.options['height'] - 140, 60, 30)
        self.fsm0_lbl_eraser_notice.setStyleSheet('color: rgb(255, 255, 255)')
        self.fsm0_lbl_eraser_notice.setAlignment(Qt.AlignCenter)
        self.fsm0_lbl_eraser_notice.setFont(font)
        self.fsm0_btn_eraser.setGeometry(self.options['width'] - 250, self.options['height'] - 110, 60, 60)
        self.fsm0_btn_eraser.setStyleSheet('background: rgb(150, 150, 150)')
        self.fsm0_btn_eraser.setIcon(QtGui.QIcon('./app_icon/icon_eraser.png'))
        self.fsm0_btn_eraser.setIconSize(QSize(30, 30))
        self.fsm0_btn_eraser.setToolTip('진단 결과 기록을 삭제합니다.')
        # FSM-0 Options 버튼 및 텍스트
        self.fsm0_lbl_options_notice.setText('Options')
        self.fsm0_lbl_options_notice.setGeometry(self.options['width'] - 180, self.options['height'] - 140, 60, 30)
        self.fsm0_lbl_options_notice.setStyleSheet('color: rgb(255, 255, 255)')
        self.fsm0_lbl_options_notice.setAlignment(Qt.AlignCenter)
        self.fsm0_lbl_options_notice.setFont(font)
        self.fsm0_btn_options.setGeometry(self.options['width'] - 180, self.options['height'] - 110, 60, 60)
        self.fsm0_btn_options.setStyleSheet('background: rgb(150, 150, 150)')
        self.fsm0_btn_options.setIcon(QtGui.QIcon('./app_icon/icon_options.png'))
        self.fsm0_btn_options.setIconSize(QSize(30, 30))
        # FSM-0 Exit 버튼 및 텍스트
        self.fsm0_lbl_exit_notice.setText('Exit')
        self.fsm0_lbl_exit_notice.setGeometry(self.options['width'] - 110, self.options['height'] - 140, 60, 30)
        self.fsm0_lbl_exit_notice.setStyleSheet('color: rgb(255, 255, 255)')
        self.fsm0_lbl_exit_notice.setAlignment(Qt.AlignCenter)
        self.fsm0_lbl_exit_notice.setFont(font)
        self.fsm0_btn_exit.setGeometry(self.options['width'] - 110, self.options['height'] - 110, 60, 60)
        self.fsm0_btn_exit.setStyleSheet('background: rgb(150, 150, 150)')
        self.fsm0_btn_exit.setIcon(QtGui.QIcon('./app_icon/icon_exit.png'))
        self.fsm0_btn_exit.setIconSize(QSize(30, 30))
        # FSM-1 elements 라벨 및 라인에디트
        font.setPointSize(15)
        self.fsm1_lbl_elements_notice.setText('최대 검색 결과 수')
        self.fsm1_lbl_elements_notice.setGeometry(50, 100, 200, 30)
        self.fsm1_lbl_elements_notice.setStyleSheet('color: rgb(255, 255, 255)')
        self.fsm1_lbl_elements_notice.setAlignment(Qt.AlignLeft)
        self.fsm1_lbl_elements_notice.setFont(font)
        self.fsm1_line_edit[0].setText(str(self.elements))
        self.fsm1_line_edit[0].setGeometry((self.options['width'] / 2), 100, 100, 30)
        self.fsm1_line_edit[0].setStyleSheet('color: rgb(255, 255, 255)')
        self.fsm1_line_edit[0].setAlignment(Qt.AlignLeft)
        self.fsm1_line_edit[0].setFont(font)
        self.fsm1_lbl_line_edit_notice[0].setText('')
        self.fsm1_lbl_line_edit_notice[0].setGeometry((self.options['width'] / 2), 140, 200, 30)
        self.fsm1_lbl_line_edit_notice[0].setStyleSheet('color: rgb(255, 0, 0)')
        self.fsm1_lbl_line_edit_notice[0].setAlignment(Qt.AlignLeft)
        font.setPointSize(13)
        self.fsm1_lbl_line_edit_notice[0].setFont(font)

        # FSM-1 Reset 버튼 및 테스트
        font.setPointSize(10)
        self.fsm1_lbl_reset_notice.setText('Reset')
        self.fsm1_lbl_reset_notice.setGeometry(self.options['width'] - 250, self.options['height'] - 140, 60, 30)
        self.fsm1_lbl_reset_notice.setStyleSheet('color: rgb(255, 255, 255)')
        self.fsm1_lbl_reset_notice.setAlignment(Qt.AlignCenter)
        self.fsm1_lbl_reset_notice.setFont(font)
        self.fsm1_btn_reset.setGeometry(self.options['width'] - 250, self.options['height'] - 110, 60, 60)
        self.fsm1_btn_reset.setStyleSheet('background: rgb(150, 150, 150)')
        self.fsm1_btn_reset.setIcon(QtGui.QIcon('./app_icon/icon_reset.png'))
        self.fsm1_btn_reset.setIconSize(QSize(30, 30))
        # FSM-1 Cancel 버튼 및 텍스트
        self.fsm1_lbl_cancel_notice.setText('Cancel')
        self.fsm1_lbl_cancel_notice.setGeometry(self.options['width'] - 180, self.options['height'] - 140, 60, 30)
        self.fsm1_lbl_cancel_notice.setStyleSheet('color: rgb(255, 255, 255)')
        self.fsm1_lbl_cancel_notice.setAlignment(Qt.AlignCenter)
        self.fsm1_lbl_cancel_notice.setFont(font)
        self.fsm1_btn_cancel.setGeometry(self.options['width'] - 180, self.options['height'] - 110, 60, 60)
        self.fsm1_btn_cancel.setStyleSheet('background: rgb(150, 150, 150)')
        self.fsm1_btn_cancel.setIcon(QtGui.QIcon('./app_icon/icon_cancel.png'))
        self.fsm1_btn_cancel.setIconSize(QSize(30, 30))
        # FSM-1 Allow 버튼 및 텍스트
        self.fsm1_lbl_allow_notice.setText('Allow')
        self.fsm1_lbl_allow_notice.setGeometry(self.options['width'] - 110, self.options['height'] - 140, 60, 30)
        self.fsm1_lbl_allow_notice.setStyleSheet('color: rgb(255, 255, 255)')
        self.fsm1_lbl_allow_notice.setAlignment(Qt.AlignCenter)
        self.fsm1_lbl_allow_notice.setFont(font)
        self.fsm1_btn_allow.setGeometry(self.options['width'] - 110, self.options['height'] - 110, 60, 60)
        self.fsm1_btn_allow.setStyleSheet('background: rgb(150, 150, 150)')
        self.fsm1_btn_allow.setIcon(QtGui.QIcon('./app_icon/icon_allow.png'))
        self.fsm1_btn_allow.setIconSize(QSize(30, 30))
        font.setPointSize(20)
        self.fsm1_lbl_question.setGeometry((self.options['width'] / 2) - 250, (self.options['height'] / 2) - 100, 500, 30)
        self.fsm1_lbl_question.setStyleSheet('color: rgb(255, 255, 255)')
        self.fsm1_lbl_question.setAlignment(Qt.AlignCenter)
        self.fsm1_lbl_question.setFont(font)
        font.setPointSize(12)
        self.fsm1_lbl_question_allow_deny[0].setText('네')
        self.fsm1_lbl_question_allow_deny[0].setGeometry((self.options['width'] / 2) - 150, (self.options['height'] / 2) - 50, 60, 30)
        self.fsm1_lbl_question_allow_deny[0].setStyleSheet('color: rgb(0, 255, 0)')
        self.fsm1_lbl_question_allow_deny[0].setAlignment(Qt.AlignCenter)
        self.fsm1_lbl_question_allow_deny[0].setFont(font)
        self.fsm1_btn_question_allow_deny[0].setGeometry((self.options['width'] / 2) - 150, (self.options['height'] / 2) - 15, 60, 60)
        self.fsm1_btn_question_allow_deny[0].setStyleSheet('background: rgb(150, 150, 150)')
        self.fsm1_btn_question_allow_deny[0].setIconSize(QSize(30, 30))
        self.fsm1_btn_question_allow_deny[0].setIcon(QtGui.QIcon('./app_icon/icon_allow.png'))
        self.fsm1_lbl_question_allow_deny[1].setText('아니오')
        self.fsm1_lbl_question_allow_deny[1].setGeometry((self.options['width'] / 2) + 100, (self.options['height'] / 2) - 50, 60, 30)
        self.fsm1_lbl_question_allow_deny[1].setStyleSheet('color: rgb(255, 0, 0)')
        self.fsm1_lbl_question_allow_deny[1].setAlignment(Qt.AlignCenter)
        self.fsm1_lbl_question_allow_deny[1].setFont(font)
        self.fsm1_btn_question_allow_deny[1].setGeometry((self.options['width'] / 2) + 100, (self.options['height'] / 2) - 15, 60, 60)
        self.fsm1_btn_question_allow_deny[1].setStyleSheet('background: rgb(150, 150, 150)')
        self.fsm1_btn_question_allow_deny[1].setIconSize(QSize(30, 30))
        self.fsm1_btn_question_allow_deny[1].setIcon(QtGui.QIcon('./app_icon/icon_cancel.png'))

    def initializeObject(self):
        # FSM-0 라인 에디트
        self.fsm0_line_edit.setVisible(self.fsm_conditions[0])
        self.fsm0_line_edit.setVisible(self.fsm_conditions[0])
        self.fsm0_lbl_le_notice.setVisible(self.fsm_conditions[0])
        self.fsm0_lbl_le_notice.setEnabled(self.fsm_conditions[0])
        # FSM-0 검색 버튼
        self.fsm0_btn_search.setVisible(self.fsm_conditions[0])
        self.fsm0_btn_search.setEnabled(False)
        # FSM-0 검색 결과
        # self.fsm0_lbl_result_notice.setGeometry((self.options['width'] / 2) - (100 / 2), 200, 100, 50)
        self.fsm0_lbl_result_notice.setVisible(self.fsm_conditions[0])
        self.fsm0_lbl_result_notice.setEnabled(self.fsm_conditions[0])
        self.fsm0_tb_result.setVisible(self.fsm_conditions[0])
        self.fsm0_tb_result.setEnabled(self.fsm_conditions[0])
        # FSM-0 Eraser 버튼 및 텍스트
        self.fsm0_lbl_eraser_notice.setVisible(self.fsm_conditions[0])
        self.fsm0_lbl_eraser_notice.setEnabled(self.fsm_conditions[0])
        self.fsm0_btn_eraser.setVisible(self.fsm_conditions[0])
        self.fsm0_btn_eraser.setEnabled(self.fsm_conditions[0])
        # FSM-0 Options 버튼 및 텍스트
        self.fsm0_lbl_options_notice.setVisible(self.fsm_conditions[0])
        self.fsm0_lbl_options_notice.setEnabled(self.fsm_conditions[0])
        self.fsm0_btn_options.setVisible(self.fsm_conditions[0])
        self.fsm0_btn_options.setEnabled(self.fsm_conditions[0])
        # FSM-0 Exit 버튼 및 텍스트
        self.fsm0_lbl_exit_notice.setVisible(self.fsm_conditions[0])
        self.fsm0_lbl_exit_notice.setEnabled(self.fsm_conditions[0])
        self.fsm0_btn_exit.setVisible(self.fsm_conditions[0])
        self.fsm0_btn_exit.setEnabled(self.fsm_conditions[0])

        # FSM-1 elements 라벨 및 라인 에디트
        self.fsm1_lbl_elements_notice.setVisible(self.fsm_conditions[1]['main'])
        self.fsm1_lbl_elements_notice.setEnabled(self.fsm_conditions[1]['main'])
        self.fsm1_line_edit[0].setVisible(self.fsm_conditions[1]['main'])
        self.fsm1_line_edit[0].setEnabled(self.fsm_conditions[1]['main'])
        self.fsm1_lbl_line_edit_notice[0].setVisible(self.fsm_conditions[1]['main'])
        self.fsm1_lbl_line_edit_notice[0].setEnabled(self.fsm_conditions[1]['main'])
        # FSM-1 Reset 버튼 및 텍스트
        self.fsm1_lbl_reset_notice.setVisible(self.fsm_conditions[1]['main'])
        self.fsm1_lbl_reset_notice.setEnabled(self.fsm_conditions[1]['main'])
        self.fsm1_btn_reset.setVisible(self.fsm_conditions[1]['main'])
        self.fsm1_btn_reset.setEnabled(self.fsm_conditions[1]['main'])
        # FSM-1 Cancel 버튼 및 텍스트
        self.fsm1_lbl_cancel_notice.setVisible(self.fsm_conditions[1]['main'])
        self.fsm1_lbl_cancel_notice.setEnabled(self.fsm_conditions[1]['main'])
        self.fsm1_btn_cancel.setVisible(self.fsm_conditions[1]['main'])
        self.fsm1_btn_cancel.setEnabled(self.fsm_conditions[1]['main'])
        # FSM-1 Allow 버튼 및 텍스트
        self.fsm1_lbl_allow_notice.setVisible(self.fsm_conditions[1]['main'])
        self.fsm1_lbl_allow_notice.setEnabled(self.fsm_conditions[1]['main'])
        self.fsm1_btn_allow.setVisible(self.fsm_conditions[1]['main'])
        self.fsm1_btn_allow.setEnabled(self.fsm_conditions[1]['main'])

        # FSM1 - Question
        if self.fsm_conditions[1]['reset']:
            self.fsm1_lbl_question.setText('설정을 초기화하시겠습니까?')
        elif self.fsm_conditions[1]['allow']:
            self.fsm1_lbl_question.setText('변경된 설정을 적용하시겠습니까?')
        self.fsm1_lbl_question.setVisible(self.fsm_conditions[1]['reset'] or self.fsm_conditions[1]['allow'])
        self.fsm1_lbl_question.setEnabled(self.fsm_conditions[1]['reset'] or self.fsm_conditions[1]['allow'])

        for i in range(2):
            self.fsm1_lbl_question_allow_deny[i].setVisible(self.fsm_conditions[1]['reset'] or self.fsm_conditions[1]['allow'])
            self.fsm1_lbl_question_allow_deny[i].setEnabled(self.fsm_conditions[1]['reset'] or self.fsm_conditions[1]['allow'])
            self.fsm1_btn_question_allow_deny[i].setVisible(self.fsm_conditions[1]['reset'] or self.fsm_conditions[1]['allow'])
            self.fsm1_btn_question_allow_deny[i].setEnabled(self.fsm_conditions[1]['reset'] or self.fsm_conditions[1]['allow'])

    # Signal-function: Line-Edit 단어 입력 감지
    def signal_detected_word_length(self):
        # 특수문자가 입력된 경우 지움.
        word = self.fsm0_line_edit.text()
        for i in range(len(word)):
            if ord(word[i]) in range(33, 44) or ord(word[i]) in range(45, 48) or ord(word[i]) in range(58, 65) or ord(word[i]) in range(91, 97) or ord(word[i]) in range(123, 128):
                self.fsm0_line_edit.setText(word[:-1])

        word_length = len(self.fsm0_line_edit.text())
        if word_length > 0:
            self.fsm0_lbl_le_notice.setVisible(False)
            self.fsm0_btn_search.setEnabled(True)
            self.fsm0_btn_search.setStyleSheet('background: rgb(150, 150, 150)')
        else:
            self.fsm0_lbl_le_notice.setVisible(True)
            self.fsm0_btn_search.setEnabled(False)
            self.fsm0_btn_search.setStyleSheet('background: rgb(30, 30, 30)')

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
            # renewed_word = renewed_word[1:].split('\n')
            # # 영문을 제거하고 남은 병명들 중 중복인 병명을 제거한다.
            # return_list = []
            # for disease in renewed_word:
            #     if disease not in return_list:
            #         return_list.append(disease)
            #
            # return_words = ''
            # for i in range(len(return_list)):
            #     return_words = '\n'.join([return_words, return_list[i]])
            #
            # return return_words[1:]

        if len(self.fsm0_line_edit.text()):
            org_symptom = self.fsm0_line_edit.text()
            symptom = org_symptom.replace(',', ' ').split()
            print(f'keywords: {len(symptom)}{symptom}')
            self.fsm0_line_edit.setText('')
            self.fsm0_lbl_le_notice.setVisible(True)
            self.fsm0_btn_search.setEnabled(False)
            self.fsm0_btn_search.setStyleSheet('color: rgb(0, 0, 0); background: rgb(30, 30, 30)')
            self.fsm0_lbl_result_notice.setVisible(True)
            self.fsm0_lbl_result_notice.setStyleSheet(f'color: rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})')
            try:
                ret_val = self.create_duplication_data(data=symptom)
            except Exception as E:
                print(f'Error--')
                self.fsm0_lbl_result_notice.setText(f'"{org_symptom}"에 대한 진단 결과 "0"건')
                self.fsm0_tb_result.setText('데이터가 없습니다.')
                self.fsm0_tb_result.setStyleSheet('color: rgb(255, 0, 0)')
            else:
                words_length = ret_val.split('\n')
                print(f'words_length: {len(words_length)}: {words_length}')
                # 학명 제거를 위한 n개 이상의 연속적인 영문 제거
                # threshold=n 은 n개 이상 등장시 학명으로 간주하고 지우겠다는 의미
                ret_val = remove_continuous_english(data=ret_val, threshold=5)
                items = len(ret_val.split('\n'))
                self.fsm0_lbl_result_notice.setText(f'"{org_symptom}"에 대한 진단 결과 "{items}"건')
                if len(words_length) > 1:
                    self.fsm0_tb_result.setText(ret_val)
                    self.fsm0_tb_result.setStyleSheet('color: rgb(255, 255, 255)')
                elif len(words_length[0]):
                    self.fsm0_tb_result.setText(ret_val)
                    self.fsm0_tb_result.setStyleSheet('color: rgb(255, 255, 255)')
                else:
                    self.fsm0_tb_result.setText('데이터가 없습니다.')
                    self.fsm0_tb_result.setStyleSheet('color: rgb(255, 0, 0)')

    def signal_btn_eraser_clicked(self):
        self.fsm0_lbl_result_notice.setText('진단 결과')
        self.fsm0_lbl_result_notice.setStyleSheet('color: rgb(255, 255, 255)')
        self.fsm0_tb_result.setText('')
        self.initializeObject()

    def signal_btn_options_clicked(self):
        self.fsm_conditions = [False, {'main': True, 'reset': False, 'cancel': False, 'allow': False}]
        self.fsm1_line_edit[0].setText(str(self.elements))
        self.initializeObject()

    def signal_btn_exit_clicked(self):
        self.close()

    def signal_btn_reset_clicked(self):
        self.fsm_conditions = [False, {'main': False, 'reset': True, 'cancel': False, 'allow': False}]
        self.initializeObject()

    def signal_btn_cancel_clicked(self):
        self.fsm_conditions = [True, {'main': False, 'reset': False, 'cancel': False, 'allow': False}]
        self.initializeObject()

    def signal_btn_allow_clicked(self):
        self.fsm_conditions = [False, {'main': False, 'reset': False, 'cancel': False, 'allow': True}]
        self.initializeObject()

    def signal_btn_question_allow_clicked(self):
        # Reset 버튼을 클릭했을 때
        if self.fsm_conditions[1]['reset']:
            self.fsm_conditions = [True, {'main': False, 'reset': False, 'cancel': False, 'allow': False}]
            self.initializeStaticObjects()
            self.initializeVariables()
            self.close()
            self.show()
            print('설정 초기화 완료.')
        # Allow 버튼을 클릭했을 때
        elif self.fsm_conditions[1]['allow']:
            self.fsm_conditions = [True, {'main': False, 'reset': False, 'cancel': False, 'allow': False}]
            # 각종 변수값을 리턴해야함.
            print(f'elements: {self.elements} -> {self.modified_elements}')
            self.elements = self.modified_elements
            print('설정 변경 완료.')

        self.initializeObject()

    def signal_btn_question_deny_clicked(self):
        self.fsm_conditions = [False, {'main': True, 'reset': False, 'cancel': False, 'allow': False}]
        self.initializeObject()
        print('취소 버튼을 클릭')

    def signal_fsm1_lineedit0_text_changed(self):
        word = self.fsm1_line_edit[0].text()
        self.fsm1_lbl_line_edit_notice[0].setVisible(False)
        if len(word):
            try:
                if not 48 <= ord(word[-1]) <= 57:
                    word = word[:-1]
                    self.fsm1_line_edit[0].setText(word)
                    self.fsm1_lbl_line_edit_notice[0].setText('정수만 입력 가능합니다.')
                    self.fsm1_lbl_line_edit_notice[0].setVisible(True)
                    self.fsm1_btn_allow.setEnabled(False)
                else:
                    word = int(word)
                    word = str(word)
                    self.fsm1_line_edit[0].setText(word)
                    self.fsm1_btn_allow.setEnabled(True)
                if not 1 <= int(word) <= 99:
                # if len(word) > 2:
                    self.fsm1_lbl_line_edit_notice[0].setText('1~99 까지만 가능합니다.')
                    self.fsm1_lbl_line_edit_notice[0].setVisible(True)
                    self.fsm1_btn_allow.setEnabled(False)
                else:
                    word = int(word)
                    word = str(word)
                    self.fsm1_line_edit[0].setText(word)
                    self.fsm1_btn_allow.setEnabled(True)
                self.modified_elements = int(word)
            except Exception as E:
                print(f'Error: {E}')
                self.fsm1_line_edit[0].setText(str(self.elements))
        else:
            self.fsm1_lbl_line_edit_notice[0].setText('정수를 입력해주세요.')
            self.fsm1_lbl_line_edit_notice[0].setVisible(True)
            self.fsm1_btn_allow.setEnabled(False)



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
            print(f'symptom_index: {symptom_index}')

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
                diseases = '\n'.join([diseases, self.data['Disease'].iloc[ret_val.index[i]].replace('\n', ' ')])

            return diseases[1:]
        else:
            ret_val = main_function(keyword_flag=True, keywords=data[0], elements=self.elements)
            diseases = ''
            for i in range(len(ret_val)):
                diseases = '\n'.join([diseases, self.data['Disease'].iloc[ret_val.index[i]].replace('\n', ' ')])

            return diseases[1:]

    def launchThread(self):
        while True:
            self.fsm0_lbl_title.setStyleSheet(f'color: rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})')
            time.sleep(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Application()
    mainWindow.show()
    sys.exit(app.exec_())
