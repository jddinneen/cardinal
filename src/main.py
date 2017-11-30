#!/usr/bin/env python
# coding:utf-8
"""
Main script calling all others.
"""

from config import CONSENT_TEXT, CONSENT_FILE_DIR, SUMMARY_FILE_DIR
import sys
import platform
import os
from PyQt5 import QtWidgets, QtCore
from wizardUI import Ui_Wizard
from disklook import get_hardware_data
from walk import scan
from classes import Results
from review import summarize
import urllib.request
from datetime import datetime
from time import sleep
from operator import attrgetter
from upload import send_encrypted_to_dropbox
import json


__author__ = "Jesse David Dinneen, Fabian Odoni"
__copyright__ = "Copyright 2015, JDD"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Jesse David Dinneen"
__email__ = "jesse.dinneen@vuw.ac.nz"
__status__ = "Beta"


# Global variables
THE_RESULTS = Results()  # Everything saved goes in here. This is defined in advance so that it can later be serialized into JSON format
LOCATIONS = []  # Places to be scanned
IGNORES = []  # Places to be ignored
home = os.path.expanduser("~")
SCANNED = False
SUMMARIZED = False
SUBMITTED = False
PAGE_TURN_COUNTER = 0
SUMMARY = ""
OS_NEXT_TEXT = "Next >"

# Done so consent form saving happens in obvious place (and doesn't fail)
os.chdir(home)


# Custom QRunnables (each for a long-running process, sent to a separate thread to keep GUI reseponsive)
class SubmitRunnable(QtCore.QRunnable):
    """ the process for submitting data """

    def run(self):
        global SUBMITTED
        print("Trying to submit")

        json_to_transmit = json.dumps(THE_RESULTS, default=lambda o: o.__dict__, sort_keys=True,  indent=None,  separators=(',', ':'))

        if send_encrypted_to_dropbox(json_to_transmit):
            # if send_to_dropbox(json_to_transmit):
            SUBMITTED = True
            # test if file was upladed
        else:
            SUBMITTED = False
            temp_text = "Error submitting; please click here to try again"
            main.ui.pushButton_4.setText(temp_text)
            main.ui.pushButton_4.setEnabled(True)


class ScanRunnable(QtCore.QRunnable):
    """ initiates the file scan """

    def run(self):
        global SCANNED
        THE_RESULTS.node_lists = scan(LOCATIONS,  IGNORES)
        SCANNED = True


class SummaryRunnable(QtCore.QRunnable):
    """ initiates summarizing the results """

    def run(self):
        global SUMMARY
        global SUMMARIZED

        SUMMARY = summarize(THE_RESULTS)

        if SUMMARY:
            SUMMARIZED = True
        else:
            SUMMARIZED = False
            temp_text = "Error summarizing results; perhaps you have no files?"
            main.ui.label_8.setText(temp_text)
            main.ui.pushButton_4.setEnabled(False)


# Custom functions called by each other or connected below via signals/slots
def user_data_saved():
    """ save demographic and computer information """
    demographic_answers = {}
    computer_answers = {}

    demographic_answers['age'] = main.ui.ageBox.text()
    demographic_answers['gender'] = main.ui.genderBox.currentText()
    demographic_answers['occupation'] = main.ui.occupationBox.text()
    demographic_answers['education'] = main.ui.educationBox.currentText()

    computer_answers['form'] = main.ui.formFactorBox.currentText()
    computer_answers['use'] = main.ui.useBox.currentText()

    THE_RESULTS.demographics = demographic_answers
    THE_RESULTS.computer_description = computer_answers

    # distro and version collecting based on sys.platform answer
    THE_RESULTS.operating_system = sys.platform

    # linux distro and version
    if ('linux' in THE_RESULTS.operating_system) or ('Linux' in THE_RESULTS.operating_system):
        THE_RESULTS.computer_description['distro'] = platform.dist()[0]
        THE_RESULTS.computer_description['version'] = platform.dist()[1]

        if len(platform.dist()[0]) < 1:
            THE_RESULTS.computer_description['distro'] = platform.platform()

    # darwin means mac
    if ('darwin' in THE_RESULTS.operating_system) or ('Darwin' in THE_RESULTS.operating_system):
        def mac_version():
            try:
                return platform.mac_ver()[0]
            except:
                return "unknown"
        THE_RESULTS.computer_description['version'] = mac_version()

    # windows version
    if ('win32' in THE_RESULTS.operating_system) or ('windows' in THE_RESULTS.operating_system):
        THE_RESULTS.computer_description['version'] = platform.platform()


def installed_software_data_saved():
    """ save user's software entries """
    file_manager_answers = {}
    cloud_answers = {}
    file_manager_answers['FM1'] = main.ui.lineEdit_2.text()
    file_manager_answers['FM2'] = main.ui.lineEdit_3.text()
    file_manager_answers['FM3'] = main.ui.lineEdit_4.text()
    file_manager_answers['FM4'] = main.ui.lineEdit_5.text()
    cloud_answers['cloud1'] = main.ui.lineEdit_7.text()
    cloud_answers['cloud2'] = main.ui.lineEdit_6.text()
    cloud_answers['cloud3'] = main.ui.lineEdit_8.text()
    cloud_answers['cloud4'] = main.ui.lineEdit_13.text()
    THE_RESULTS.installed_file_managers = file_manager_answers
    THE_RESULTS.cloud_services = cloud_answers


def choose_spot_requested(lineedit):
    """ launch a folder-selecting dialog """
    lineedit.setText(QtWidgets.QFileDialog.getExistingDirectory())


def save_locations_requested():
    """ save any 'managed location' entered """
    if not SCANNED:
        if((len(LOCATIONS)) > 0):
            del LOCATIONS[:]
        possible_locations = [main.ui.lineEdit_9,  main.ui.lineEdit_10, main.ui.lineEdit_11, main.ui.lineEdit_12]
        for answer in possible_locations:
            if (len(answer.text()) > 0):
                LOCATIONS.append(answer.text())
    else:
        main.ui.pushButton_9.setEnabled(False)
        main.ui.pushButton_10.setEnabled(False)
        main.ui.pushButton_11.setEnabled(False)
        main.ui.pushButton_12.setEnabled(False)


def save_ignores_requested():
    """ save any 'ignore location' entered """
    if not SCANNED:
        if((len(IGNORES)) > 0):
            del IGNORES[:]
        possible_ignores = [main.ui.lineEdit_23,  main.ui.lineEdit_24, main.ui.lineEdit_25, main.ui.lineEdit_26]
        for answer in possible_ignores:
            if (len(answer.text()) > 0):
                IGNORES.append(answer.text())
    else:
        main.ui.pushButton_23.setEnabled(False)
        main.ui.pushButton_24.setEnabled(False)
        main.ui.pushButton_25.setEnabled(False)
        main.ui.pushButton_26.setEnabled(False)


def file_scan_requested():
    """ prepare for scan and then initiate it """
    labelstring = " "
    main.ui.label_9.setText(labelstring)

    if (len(THE_RESULTS.drives) > 0):
        del THE_RESULTS.drives[:]
    THE_RESULTS.drives = get_hardware_data()

    if (len(LOCATIONS) < 1):
        warningstring = "<p align=\"center\">Can't collect data about 0 locations.\nPlease add locations to be included in data collection.</p>"
        main.ui.label_9.setText(warningstring)
    else:
        main.ui.label_9.clear()
        if (len(LOCATIONS) > 1):  # make sure descendant folders don't end up getting SCANNED twice
            locations2 = list(LOCATIONS)
            for entry2 in locations2:
                for entry in LOCATIONS:
                    if ((entry2 in entry) and not ((entry2 in entry) and (entry in entry2))):
                        LOCATIONS.remove(entry)
        main.ui.pushButton_2.setEnabled(False)
        # disable all the previously interactive buttons and fields
        main.ui.consentBox.setEnabled(False)
        main.ui.ageBox.setEnabled(False)
        main.ui.genderBox.setEnabled(False)
        main.ui.educationBox.setEnabled(False)
        main.ui.occupationBox.setEnabled(False)
        main.ui.formFactorBox.setEnabled(False)
        main.ui.useBox.setEnabled(False)
        main.ui.useBox.setEnabled(False)
        main.ui.lineEdit_2.setEnabled(False)
        main.ui.lineEdit_3.setEnabled(False)
        main.ui.lineEdit_4.setEnabled(False)
        main.ui.lineEdit_5.setEnabled(False)
        main.ui.lineEdit_6.setEnabled(False)
        main.ui.lineEdit_7.setEnabled(False)
        main.ui.lineEdit_8.setEnabled(False)
        main.ui.lineEdit_13.setEnabled(False)
        main.ui.pushButton_9.setEnabled(False)
        main.ui.pushButton_10.setEnabled(False)
        main.ui.pushButton_11.setEnabled(False)
        main.ui.pushButton_12.setEnabled(False)
        main.ui.pushButton_23.setEnabled(False)
        main.ui.pushButton_24.setEnabled(False)
        main.ui.pushButton_25.setEnabled(False)
        main.ui.pushButton_26.setEnabled(False)
        app.processEvents()  # does the above before moving on
        runnable = ScanRunnable()
        QtCore.QThreadPool.globalInstance().start(runnable)
        global SCANNED
        buttonstring = "Collecting data..."
        while not SCANNED:
            app.processEvents()
            if len(buttonstring) > 20:
                buttonstring = "Collecting data..."
                main.ui.pushButton_2.setText(buttonstring)
            else:
                sleep(0.25)
                buttonstring += "."
                main.ui.pushButton_2.setText(buttonstring)
        else:
            buttonstring = "Done"
            main.ui.pushButton_2.setText(buttonstring)
            warningstring = "<html><head/><body><p align=\"center\"><span style=\"font-size:16pt; color:#00c800;\">Done!</span></p><p align=\"center\"></p><p align=\"center\"><span style=\"font-size:14pt; color:#000000;\">Let's continue.</span></p><p align=\"center\"></p></body></html>"
            main.ui.label_9.setText(warningstring)
            if not main.ui.scanCheckBox.isChecked():
                main.ui.scanCheckBox.toggle()
            main.next()  # advance the page


def savePersonalityRequested():
    """ save the raw responses of the personality style questionnaire """

    personality_responses = {}
    for question in range(1, 11):
        question_name = "q{}".format(question)
        for button in range(1, 8):
            radio_button = "radioButton_{}".format(button + ((question - 1) * 7))
            if attrgetter(radio_button)(main.ui).isChecked():
                personality_responses[question_name] = str(button)

    THE_RESULTS.personality_results = personality_responses


def saveSODRequested():
    """ save the raw responses to the sense of direction questionnaire """

    sod_responses = {}
    button_offset = 70

    for question in range(1, 16):
        question_name = "q{}".format(question)
        for button in range(1, 8):
            radio_button = "radioButton_{}".format((button + ((question - 1) * 7) + button_offset))
            if attrgetter(radio_button)(main.ui).isChecked():
                sod_responses[question_name] = str(button)

    THE_RESULTS.sod_results = sod_responses


def check_connectivity(reference):
    """ check internet connectivity (done at app start) """
    try:
        urllib.request.urlopen(reference, timeout=5)
        return True
    except urllib.request.URLError:
        return False


def button_checks():
    global OS_NEXT_TEXT
    """ check on buttons that validate to enable 'next' buttons """

    if (len(THE_RESULTS.node_lists) > 0):
        if (main.currentId() == 7):
            if not main.ui.scanCheckBox.isChecked():
                main.ui.scanCheckBox.toggle()

    if (main.currentId() == 6):
        if (len(LOCATIONS) < 1):
            warningstring = "<p align=\"center\">Please add locations to be included in data collection.</p>"
            main.ui.label_9.setText(warningstring)
        else:
            main.ui.label_9.clear()

    if (main.currentId() == 12):
        main.setButtonText(main.NextButton, OS_NEXT_TEXT)

    if (main.currentId() == 13):
        savePersonalityRequested()
        saveSODRequested()
        if ((len(THE_RESULTS.sod_results) > 14) and (len(THE_RESULTS.personality_results) > 9)):
            main.setButtonText(main.NextButton, OS_NEXT_TEXT)
            if not main.ui.questionnaireBox.isChecked():
                main.ui.questionnaireBox.toggle()
        else:
            if not ((len(THE_RESULTS.personality_results) > 9) and (len(THE_RESULTS.sod_results) > 9)):
                main.setButtonText(main.NextButton, "Please complete both questionnaires to proceed.")

    if SUMMARIZED:
        if (main.currentId() == 14):
            if not main.ui.summaryBox.isChecked():
                main.ui.summaryBox.toggle()

    if SUBMITTED:
        if (main.currentId() == 15):
            main.ui.pushButton_4.setEnabled(False)
            if not main.ui.submitCheckBox.isChecked():
                main.ui.submitCheckBox.toggle()


def summary_requested():
    """ prepare and display a summary of the results """
    global SUMMARIZED
    if not SUMMARIZED:
        if (len(THE_RESULTS.sod_results) < 15) or (len(THE_RESULTS.personality_results) < 10 or len(THE_RESULTS.node_lists) < 1):
            main.ui.pushButton_4.setEnabled(False)
        else:
            textA = "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Summarizing results..."
            textB = ""
            textC = "</span></p></body></html>"
            summarizable = SummaryRunnable()  # start a qrunnable for the summarizer
            QtCore.QThreadPool.globalInstance().start(summarizable)
            while not SUMMARIZED:  # check on global 'SUMMARIZED'
                app.processEvents()
                if len(textB) > 2:
                    sleep(0.25)
                    textB = ""
                    summarizingText = textA + textB + textC
                    main.ui.summarizingLabel.setText(summarizingText)
                else:
                    sleep(0.25)
                    textB += "."
                    summarizingText = textA + textB + textC
                    main.ui.summarizingLabel.setText(summarizingText)
            else:
                textA = "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Done preparing summary.\n "
                summarizingText = textA + textC
                main.ui.summarizingLabel.setText(summarizingText)
                if not main.ui.summaryBox.isChecked():
                    main.ui.summaryBox.toggle()
                main.ui.pushButton_4.setEnabled(True)
                main.ui.label_6.setText(SUMMARY)


def submit_file_requested():
    """ prepare to submit, initiate """
    main.ui.pushButton_4.setEnabled(False)
    if check_connectivity("http://www.google.com/"):
        app.processEvents()
        runnable = SubmitRunnable()
        QtCore.QThreadPool.globalInstance().start(runnable)
        global SUBMITTED
        buttonstring = "Submitting results..."
        while not SUBMITTED:
            app.processEvents()
            if len(buttonstring) > 23:
                buttonstring = "Submitting results..."
                main.ui.pushButton_4.setText(buttonstring)
            else:
                sleep(0.25)
                buttonstring += "."
                main.ui.pushButton_4.setText(buttonstring)
        else:
            buttonstring = "Done"
            main.ui.pushButton_4.setText(buttonstring)
            if not main.ui.submitCheckBox.isChecked():
                main.ui.submitCheckBox.toggle()
            main.next()
    else:
        main.ui.pushButton_4.setText("Please connect to the Internet and try again.")
        main.ui.pushButton_4.setEnabled(True)


def save_consent_requested():
    """ save the consent form to a text file """
    os.chdir(home)
    consent_file = open(CONSENT_FILE_DIR,  'w')
    consent_file.write(CONSENT_TEXT)
    consent_file.close()
    button_string = "Saved {} to home folder".format(CONSENT_FILE_DIR)
    main.ui.consentSaveButton.setText(button_string)
    main.ui.consentSaveButton.setEnabled(False)


def save_results_requested():
    """ save the results summary to a text file """
    os.chdir(home)
    summary_file = open(SUMMARY_FILE_DIR,  'w')
    summary_file.write(SUMMARY)
    summary_file.close()
    button_string = "Saved {} to home folder".format(SUMMARY_FILE_DIR)
    main.ui.resultsSaveButton.setText(button_string)
    main.ui.resultsSaveButton.setEnabled(False)


def age_box_handling():
    """
    put the cursor in the right starting position in the age box
    (input mask + text validation seem to cause strange behavior otherwise)
    """
    if (len(main.ui.ageBox.text()) < 1):
        main.ui.ageBox.setCursorPosition(0)
    elif (len(main.ui.ageBox.text()) < 2):
        main.ui.ageBox.setCursorPosition(1)


def rb_actions():
    """
    save results of questionnaires every time one of the questionnaire
    radio button 'groups' is clicked
    """
    global OS_NEXT_TEXT
    savePersonalityRequested()
    saveSODRequested()
    if ((len(THE_RESULTS.sod_results) > 14) and (len(THE_RESULTS.personality_results) > 9)):
        if not main.ui.questionnaireBox.isChecked():
            main.ui.questionnaireBox.toggle()
            main.setButtonText(main.NextButton, OS_NEXT_TEXT)


def take_time_stamps():
    """ make page+timestamp """
    global PAGE_TURN_COUNTER
    PAGE_TURN_COUNTER += 1
    THE_RESULTS.time_stamps[PAGE_TURN_COUNTER] = (main.currentId(), datetime.strftime(datetime.utcnow(), '%H:%M:%S'))


class Main(QtWidgets.QWizard):
    """ The QT GUI """

    def __init__(self):
        super(Main, self).__init__()

        # build ui
        self.ui = Ui_Wizard()
        self.ui.setupUi(self)

        # connect signals
        self.currentIdChanged.connect(lambda: take_time_stamps())
        self.currentIdChanged.connect(lambda: user_data_saved())
        self.currentIdChanged.connect(lambda: installed_software_data_saved())
        self.currentIdChanged.connect(lambda: save_locations_requested())
        self.currentIdChanged.connect(lambda: save_ignores_requested())
        self.currentIdChanged.connect(lambda: button_checks())
        self.currentIdChanged.connect(lambda: summary_requested())
        self.ui.pushButton_2.clicked.connect(lambda: file_scan_requested())
        self.ui.pushButton_4.clicked.connect(lambda: submit_file_requested())
        self.ui.pushButton_9.clicked.connect(lambda: choose_spot_requested(self.ui.lineEdit_9))
        self.ui.pushButton_10.clicked.connect(lambda: choose_spot_requested(self.ui.lineEdit_10))
        self.ui.pushButton_11.clicked.connect(lambda: choose_spot_requested(self.ui.lineEdit_11))
        self.ui.pushButton_12.clicked.connect(lambda: choose_spot_requested(self.ui.lineEdit_12))
        self.ui.pushButton_23.clicked.connect(lambda: choose_spot_requested(self.ui.lineEdit_23))
        self.ui.pushButton_24.clicked.connect(lambda: choose_spot_requested(self.ui.lineEdit_24))
        self.ui.pushButton_25.clicked.connect(lambda: choose_spot_requested(self.ui.lineEdit_25))
        self.ui.pushButton_26.clicked.connect(lambda: choose_spot_requested(self.ui.lineEdit_26))
        self.ui.consentSaveButton.clicked.connect(lambda: save_consent_requested())
        self.ui.resultsSaveButton.clicked.connect(lambda: save_results_requested())
        self.ui.ageBox.cursorPositionChanged.connect(lambda: age_box_handling())
        self.ui.buttonGroup.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_2.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_3.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_4.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_5.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_6.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_7.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_8.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_9.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_10.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_11.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_12.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_13.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_14.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_15.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_16.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_17.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_18.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_19.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_20.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_21.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_22.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_23.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_24.buttonClicked.connect(lambda: rb_actions())
        self.ui.buttonGroup_25.buttonClicked.connect(lambda: rb_actions())

        # default values for sw data page
        suggested_filemanager = ""
        if sys.platform in ('Windows',  'win32',  'cygwin'):
            suggested_filemanager = "File Explorer"
        elif sys.platform in ('darwin'):
            suggested_filemanager = "Finder"
        self.ui.lineEdit_2.setText(suggested_filemanager)

        # default value for first scan location (user home)
        self.ui.lineEdit_9.setText(home)

        # make some check boxes mandatory for progressing in app
        self.ui.questionnaireBox.setVisible(False)
        self.ui.wizardPage8c.registerField("questionnaireBox*", self.ui.questionnaireBox)
        self.ui.summaryBox.setVisible(False)
        self.ui.signpostPage4.registerField("summaryBox*", self.ui.summaryBox)
        self.ui.internetBox.setVisible(False)
        self.ui.wizardPage1.registerField("internetBox*", self.ui.internetBox)
        self.ui.scanCheckBox.setVisible(False)
        self.ui.wizardPage6.registerField("scanCheckBox*", self.ui.scanCheckBox)
        self.ui.submitCheckBox.setVisible(False)
        self.ui.wizardPage9.registerField("submitCheckBox*", self.ui.submitCheckBox)
        self.ui.wizardPage1.registerField("consentBox*", self.ui.consentBox)  # this one needs to be visible as user clicks it

        # check internet connection at start
        if check_connectivity("http://www.google.com/"):
            self.ui.internetBox.toggle()
        else:
            self.setButtonText(self.NextButton, "Please connect to the Internet and restart the application.")

# the whole app
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    main = Main()
    main.show()
    sys.exit(app.exec_())
