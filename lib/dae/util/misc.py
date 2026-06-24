import sys
import math
from os import path
from ctypes import cdll
from typing import Iterable
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import QFileDialog, QDialog

# def getPath(relativePath:str):
# 	return path.abspath(path.join(path.dirname(__file__), relativePath))

def getParentDir(filePath:str, level:int = 1):
	if level <= 0:
		return filePath
	else:
		return getParentDir(path.dirname(filePath), level - 1)

if getattr(sys, "frozen", False):
	ROOT_FOLDER = getattr(sys, "_MEIPASS", path.dirname(sys.executable))
else:
	ROOT_FOLDER = getParentDir(path.abspath(__file__), 4)

RES_FOLDER = path.join(ROOT_FOLDER, "res")
LIB_FOLDER = path.join(ROOT_FOLDER, "lib")
UI_FOLDER = path.join(ROOT_FOLDER, "ui")

def getResPath(fileName:str):
	return path.join(RES_FOLDER, fileName)

def loadDLL(name:str):
	dllPath = path.join(LIB_FOLDER, name)
	
	if not path.exists(dllPath):
		try:
			with open("WT_3D_Exports/dll_debug.log", "w") as f:
				f.write(f"DLL NOT FOUND!\nName: {name}\ndllPath: {dllPath}\nROOT_FOLDER: {ROOT_FOLDER}\nLIB_FOLDER: {LIB_FOLDER}\n")
				f.write(f"frozen: {getattr(sys, 'frozen', False)}\n")
				if getattr(sys, "frozen", False):
					f.write(f"_MEIPASS: {getattr(sys, '_MEIPASS', 'MISSING')}\n")
					try:
						import os
						f.write("Root files:\n" + str(os.listdir(getattr(sys, '_MEIPASS', '.'))) + "\n")
						f.write("Lib files:\n" + str(os.listdir(path.join(getattr(sys, '_MEIPASS', '.'), 'lib'))) + "\n")
					except Exception as e:
						f.write(f"Error listing dirs: {e}\n")
		except Exception:
			pass
		return None
	else:
		import os
		cookie = None
		if hasattr(os, "add_dll_directory"):
			try:
				cookie = os.add_dll_directory(LIB_FOLDER)
			except Exception:
				pass
		try:
			return cdll.LoadLibrary(dllPath)
		except Exception as e:
			try:
				with open("WT_3D_Exports/dll_debug.log", "w") as f:
					f.write(f"DLL LOAD FAILED!\nName: {name}\ndllPath: {dllPath}\nException: {e}\n")
			except Exception:
				pass
		finally:
			if cookie:
				try:
					cookie.close()
				except Exception:
					pass

def getUIPath(fileName:str):
	return path.join(UI_FOLDER, fileName)


def matrixMul(A, B):
	if len(A[0]) != len(B):
		raise ValueError("Matrix dimensions do not match")
	
	result = [[0] * len(B[0]) for _ in range(len(A))]
	
	for i in range(len(A)):
		for j in range(len(B[0])):
			for k in range(len(B)):
				result[i][j] += A[i][k] * B[k][j]
	
	return result

def vectorTransform(matrix, vector):
	result = [0] * 3

	for i in range(3):
		for j in range(3):
			result[i] += matrix[i][j] * vector[j]
	
	result[0] += matrix[0][3]
	result[1] += matrix[1][3]
	result[2] += matrix[2][3]

	return result

def matrixToEuler(matrix):
	r11, r12, r13 = matrix[0][:3]
	r21, r22, r23 = matrix[1][:3]

	yaw = math.atan2(r13, math.sqrt(r11**2 + r12**2))

	pitch = math.atan2(-r23, math.sqrt(r21**2 + r22**2))

	roll = math.atan2(r21, r22)

	return pitch, roll, yaw



def openFile(window = None, title:str = "", nameFilters:Iterable = None, shouldAccept = lambda x: True, fileMode:int = QFileDialog.ExistingFiles):
	selectedFolderValid = False

	while not selectedFolderValid:
		dialog = QFileDialog()
		dialog.setWindowTitle(title)
		dialog.setDirectory(QDir.currentPath())
		dialog.setFileMode(fileMode)
		
		# dialog.setOption(QFileDialog.Option.DontUseNativeDialog,True)

		# listView = dialog.findChild(QListView,name = "listView")
		
		# if listView != None:
		#     listView.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
		
		# treeView = dialog.findChild(QTreeView)

		# if treeView != None:
		#     treeView.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
		
		if nameFilters != None:
			dialog.setNameFilters(nameFilters)

		if dialog.exec_() == QDialog.Accepted:
			selectedFolderValid = shouldAccept(dialog)
		else:
			return None
	
	if window != None:
		window.setWindowState(window.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
		window.activateWindow()
	
	return dialog


powerLabels = (
	" B",
	" KB",
	" MB"
)
powerLabelCnt = len(powerLabels)
power = 2**10

def formatBytes(size):
	n = 0

	while size > power and n < powerLabelCnt:
		size /= power
		n += 1
	
	return str(round(size)) + powerLabels[n]