#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4.QtGui import QDialog
from ui.FilterLocationsDateDialog import Ui_FilterLocationsDateDialog


class FilterLocationsDateDialog(QDialog):
    """ Loads the Filter Locations by Date dialog from the ui and shows it """
    def __init__(self, parent=None):
        # Load the UI from the python file
        QDialog.__init__(self, parent)
        self.ui = Ui_FilterLocationsDateDialog()
        self.ui.setupUi(self)
