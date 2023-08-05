from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *

def setup_menu(win):
    menu = win.menuBar()
    file_menu = menu.addMenu("&File")
    open_menuitem = file_menu.addAction("Open...")
    open_menuitem.setShortcut(QKeySequence.Open)
    open_menuitem.triggered.connect(win.on_open)
    win.mru_menu = file_menu.addMenu("Recent files")
    if len(win.mru):
        win.populate_mru_menu()
    else:
        win.mru_menu.setEnabled(False)
    exit_menuitem = file_menu.addAction("E&xit")
    exit_menuitem.setMenuRole(QAction.QuitRole)
    exit_menuitem.setShortcut(QKeySequence.Quit)
    exit_menuitem.triggered.connect(win.on_exit)
    #########
    view_menu = menu.addMenu("View")
    win.prefix_menuitem = view_menu.addAction("DWARF prefix")
    win.prefix_menuitem.setCheckable(True)
    win.prefix_menuitem.setChecked(win.prefix)
    win.prefix_menuitem.triggered.connect(win.on_view_prefix)
    win.lowlevel_menuitem = view_menu.addAction("Low level")
    win.lowlevel_menuitem.setCheckable(True)
    win.lowlevel_menuitem.setChecked(win.lowlevel)
    win.lowlevel_menuitem.triggered.connect(win.on_view_lowlevel)
    win.hex_menuitem = view_menu.addAction("Hexadecimal")
    win.hex_menuitem.setCheckable(True)
    win.hex_menuitem.setChecked(win.hex)
    win.hex_menuitem.triggered.connect(win.on_view_hex)
    win.regnames_menuitem = view_menu.addAction("DWARF register names")
    win.regnames_menuitem.setCheckable(True)
    win.regnames_menuitem.setChecked(win.dwarfregnames)
    win.regnames_menuitem.triggered.connect(win.on_view_regnames)
    view_menu.addSeparator()
    win.sortcus_menuitem = view_menu.addAction("Sort CUs")
    win.sortcus_menuitem.setCheckable(True)
    win.sortcus_menuitem.setChecked(win.sortcus)
    win.sortcus_menuitem.triggered.connect(win.on_sortcus)
    win.sortdies_menuitem = view_menu.addAction("Sort DIEs")
    win.sortdies_menuitem.setCheckable(True)
    win.sortdies_menuitem.setChecked(win.sortdies)
    win.sortdies_menuitem.triggered.connect(win.on_sortdies)
    view_menu.addSeparator()
    win.highlightcode_menuitem = view_menu.addAction("Highlight code")
    win.highlightcode_menuitem.setCheckable(True)
    win.highlightcode_menuitem.setEnabled(False)
    win.highlightcode_menuitem.triggered.connect(win.on_highlight_code)
    win.highlightnothing_menuitem = view_menu.addAction("Remove highlighting")
    win.highlightnothing_menuitem.setEnabled(False)
    win.highlightnothing_menuitem.triggered.connect(win.on_highlight_nothing)
    view_menu.addSeparator()
    win.cuproperties_menuitem = view_menu.addAction("CU properties...")
    win.cuproperties_menuitem.setEnabled(False)
    win.cuproperties_menuitem.triggered.connect(win.on_cuproperties)
    #########
    edit_menu = menu.addMenu("Edit")
    win.copy_menuitem = edit_menu.addAction("Copy value")
    win.copy_menuitem.setShortcut(QKeySequence.Copy)
    win.copy_menuitem.setEnabled(False)
    win.copy_menuitem.triggered.connect(win.on_copyvalue)
    win.copyline_menuitem = edit_menu.addAction("Copy line")
    win.copyline_menuitem.setEnabled(False)
    win.copyline_menuitem.triggered.connect(win.on_copyline)        
    win.copytable_menuitem = edit_menu.addAction("Copy table")
    win.copytable_menuitem.setEnabled(False)
    win.copytable_menuitem.triggered.connect(win.on_copytable)  
    #########
    nav_menu = menu.addMenu("Navigate")
    win.back_menuitem = nav_menu.addAction("Back")
    win.back_menuitem.setShortcut(QKeySequence.Back)
    win.back_menuitem.setEnabled(False);
    win.back_menuitem.triggered.connect(lambda: win.on_nav(1))
    win.forward_menuitem = nav_menu.addAction("Forward")
    win.forward_menuitem.setShortcut(QKeySequence.Forward)
    win.forward_menuitem.setEnabled(False);
    win.forward_menuitem.triggered.connect(lambda: win.on_nav(-1))
    win.followref_menuitem = nav_menu.addAction("Follow the ref")
    win.followref_menuitem.setEnabled(False);
    win.followref_menuitem.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Return))
    win.followref_menuitem.triggered.connect(win.on_followref)        
    nav_menu.addSeparator()
    win.find_menuitem = nav_menu.addAction("Find...")
    win.find_menuitem.setEnabled(False)
    win.find_menuitem.setShortcut(QKeySequence.Find)
    win.find_menuitem.triggered.connect(win.on_find)
    win.findip_menuitem = nav_menu.addAction("Find code offset...")
    win.findip_menuitem.setEnabled(False)
    win.findip_menuitem.triggered.connect(win.on_findip)
    win.findbycondition_menuitem = nav_menu.addAction("Find by condition...")
    win.findbycondition_menuitem.setEnabled(False)
    win.findbycondition_menuitem.triggered.connect(win.on_findbycondition)
    win.findnext_menuitem = nav_menu.addAction("Find next")
    win.findnext_menuitem.setEnabled(False)
    win.findnext_menuitem.setShortcut(QKeySequence.FindNext)
    win.findnext_menuitem.triggered.connect(win.on_findnext)
    ########
    help_menu = menu.addMenu("Help")
    about_menuitem = help_menu.addAction("About...")
    about_menuitem.setMenuRole(QAction.AboutRole)
    about_menuitem.triggered.connect(win.on_about) 
    help_menu.addAction('Check for updates...').triggered.connect(win.on_updatecheck)
    help_menu.addAction('Homepage').triggered.connect(win.on_homepage)

def setup_ui(win):
    setup_menu(win)
    # Set up the left pane and the right pane
    tree = win.the_tree = QTreeView()
    tree.header().hide()
    tree.setUniformRowHeights(True)
    
    rpane = QSplitter(Qt.Orientation.Vertical)
    die_table = win.die_table = QTableView()
    die_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    die_table.doubleClicked.connect(win.on_attribute_dclick)
    rpane.addWidget(die_table)

    details_table = win.details_table = QTableView()
    details_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    rpane.addWidget(details_table)
    # All the resizing goes into the bottom pane
    rpane.setStretchFactor(0, 0)
    rpane.setStretchFactor(1, 1)

    spl = QSplitter()
    spl.addWidget(win.the_tree)
    spl.addWidget(rpane)
    # All the resizing goes into the right pane by default
    spl.setStretchFactor(0, 0)
    spl.setStretchFactor(1, 1) 
    win.setCentralWidget(spl)

    win.setWindowTitle("DWARF Explorer")
    win.resize(win.font_metrics.averageCharWidth() * 250, win.font_metrics.height() * 60)
