#!/bin/bash


import pandas as pd
import numpy as np
import wx
import wx.xrc
import xlrd
import os

class MyFrame1 ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 487,218 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_button1 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.Point( -1,-1 ), wx.DefaultSize, 0 )

		self.m_button1.SetBitmapPosition( wx.TOP )
		bSizer1.Add( self.m_button1, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Upload File", wx.Point( 0,-1 ), wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer1.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_textCtrl1, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Bank Statement", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_textCtrl2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_textCtrl2, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button1.Bind( wx.EVT_BUTTON, self.merge )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def merge( self, event ):
		fName = os.path.dirname(os.path.abspath(self.m_textCtrl1.GetValue())) \
				+ '/' + self.m_textCtrl1.GetValue()
		#self.m_textCtrl1.GetValue()
		#/Users/sujeetyeramareddy/Desktop/Coast/Coast_Benefits/loanpaymentsBeg.csv
		wb = xlrd.open_workbook(fName)
		sheet = wb.sheet_by_index(0)

		fName2 = os.path.dirname(os.path.abspath(self.m_textCtrl2.GetValue())) \
				+ '/' + self.m_textCtrl2.GetValue()
		#self.m_textCtrl2.GetValue()
		#/Users/sujeetyeramareddy/Desktop/Coast/Coast_Benefits/loanpaymentsIK.csv
		wb2 = xlrd.open_workbook(fName2)
		sheet2 = wb2.sheet_by_index(0)
		paymentDue  = []
		paymentPaid = []

		for i in range(sheet2.nrows):
			paymentDue.append(sheet2.cell_value(i, 8))
			paymentPaid.append(sheet2.cell_value(i, 8))

		paymentPaid = [i for i in paymentPaid if i != '']
		paymentDue = [i for i in paymentDue if i != '']

		d2 = {'Payment Due': paymentDue, 'Payment Paid': paymentPaid}
		#endData = pd.DataFrame(d2)
		#endData['Payment Due'].replace('', np.nan, inplace=True)
		#endData['Payment Paid'].replace('', np.nan, inplace=True)
		#endData = endData.dropna(subset=['Payment Due', 'Payment Paid'])

		d = {}
		l = []
		for i in range(sheet.ncols):
			for j in range(1, sheet.nrows):
				l.append(sheet.cell_value(j,i))
			d.update({sheet.row_values(0)[i]: l})
			l = []

		d.update(d2)
		data = pd.DataFrame(d)
		data['SSN'] = data['SSN'].astype(int)
		data.to_excel('exported.xlsx', sheet_name='Sheet1', index=False)
		print('Successful!')

app = wx.App(False) 
frame = MyFrame1(None) 
frame.Show(True) 
app.MainLoop() 
