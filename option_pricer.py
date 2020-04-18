from tkinter import *
from tkinter import messagebox
from math import *
from scipy.stats import norm

##Notes to self
## ADJUST RISK-FREE RATE PARAMETER Option class
## Create final output for when user prices a structure
## Add another analytical option pricing formula
## Add quantity and buy/sell
## data validation = stil allows negative numbers


class Option(object):
	RiskFreeRate=0.03 #class attribute since the risk-free rate should be the same if we are only analyzing assets denominated in the same currency

	def __init__(self,Strike,Time,OptionType,Spot,Vol,Barrier=None):
		self.Strike=Strike
		self.Time=Time
		self.OptionType=OptionType
		self.Spot=Spot
		self.Vol=Vol
		self.Priced=False
		self.CreateDetails()

	def CreateDetails(self):
		self.Details="Option details\n"
		self.Details=self.Details+"Strike: {}\n".format(self.Strike)
		self.Details=self.Details+"Option Type: {}\n".format(self.OptionType)
		self.Details=self.Details+"Time to Expiration: {}\n".format(self.Time)
		self.Details=self.Details+"Underlying Price: {}\n".format(self.Spot)
		self.Details=self.Details+"Implied Volatility: {}\n".format(self.Vol)

	def __repr__(self):
		return self.Details

#Prices option with Black & Scholes model
def BlackScholes(Opt):
	d1=(log(Opt.Spot/Opt.Strike)+(Option.RiskFreeRate+pow(Opt.Vol,2)/2)*Opt.Time)/(Opt.Vol*sqrt(Opt.Time))
	d2=d1-Opt.Vol*sqrt(Opt.Time)
	
	if Opt.OptionType=="Call":
		Opt.Premium=round(Opt.Spot*norm.cdf(d1)-Opt.Strike*exp(-Option.RiskFreeRate*Opt.Time)*norm.cdf(d2),2)
	elif Opt.OptionType=="Put":
		Opt.Premium=round(-Opt.Spot*norm.cdf(-d1)+Opt.Strike*exp(-Option.RiskFreeRate*Opt.Time)*norm.cdf(-d2),2)
	else:
		messagebox.showerror("Option Type Error", "This is not a call or a put.")

	if not Opt.Priced: #Avoids updating details of an option object that was already priced before
		Opt.Details=Opt.Details+"Option Premium: {}\n".format(Opt.Premium)
		Opt.Priced=True

	print(Opt)

#Option pricer window
class OptionPricer(object):
	OptionTypeOptionMenu = ("Call", "Put")
	PricingMethodsOptionMenu= ("Black & Scholes",) #comma added to make it a tuple, otherwise its just a string
	NumberOfOptions=1
	LimitNumberOfOptions = 5 #sets the maximum number of legs the pricer will allow the user to add
	
	#Lists to have access to all elements
	AllFrames=[]
	AllLabels=[]
	AllStrikes=[]
	AllTimes=[]
	AllSpots=[]
	AllVols=[]
	AllTypes=[]
	AllOptions=[]

	#creates a structure with 1 leg
	def __init__(self):
		#Color palette
		self.window_color="gray10" #background color for toplevel, frames and labels
		self.elements_color="gray25" #background color for elements in buttons and frames
		self.entry_color="gray35" #background color for entries
		self.text_color="gray99" #color of displayed text

		#Creates a new window to define the details of the structure to be priced
		self.OptionPricerWindow = Toplevel()
		self.OptionPricerWindow.geometry("250x265")
		self.OptionPricerWindow.wm_title("Options Pricer")
		self.OptionPricerWindow.grab_set()
		self.OptionPricerWindow.config(bg=self.window_color)
		self.OptionPricerWindow.resizable(False, False)

		#adds the pricer's buttons
		self.Button_AddLeg = Button(self.OptionPricerWindow, text="Add Leg", command= self.AddLeg, bg=self.elements_color, fg=self.text_color)
		self.Button_RemoveLeg = Button(self.OptionPricerWindow, text="Remove Leg", command= self.RemoveLeg, bg=self.elements_color, fg=self.text_color)
		self.Button_PriceStructure = Button(self.OptionPricerWindow, text="Price Structure", command= self.CreateOption, bg=self.elements_color, fg=self.text_color)
		self.Button_PriceStructure.grid(column=0, row=0, columnspan=2, padx=5, pady=5)
		self.Button_AddLeg.grid(column=0, row=7, padx=4, pady=5)
		self.Button_RemoveLeg.grid(column=1, row=7, padx=2, pady=5)
		self.PricingMethod=StringVar(self.OptionPricerWindow)
		self.PricingMethod.set(OptionPricer.PricingMethodsOptionMenu[0])
		self.Menu_PricingMethod=OptionMenu(self.OptionPricerWindow,self.PricingMethod,*OptionPricer.PricingMethodsOptionMenu)
		self.Menu_PricingMethod.config(bg=self.elements_color, fg=self.text_color, activebackground=self.elements_color, activeforeground=self.text_color, width=16, highlightthickness=0)
		self.Menu_PricingMethod["menu"].configure(bg=self.elements_color, fg=self.text_color)
		self.Menu_PricingMethod.grid(column=0, row=8, columnspan=2, padx=2, pady=2)

		#Adds labels for the entries
		self.OptionPricerLabels=Frame(self.OptionPricerWindow, bg=self.window_color)
		self.OptionPricerLabels.grid(column=0, row=4, columnspan=2, padx=5, pady=5)
		self.Label_Leg=Label(self.OptionPricerLabels,text="", bg=self.window_color, fg=self.text_color).grid(column=0, row=0)
		self.Label_Strike=Label(self.OptionPricerLabels,text="Strike:", bg=self.window_color, fg=self.text_color, anchor="e", width=15, padx=2, pady=2).grid(column=0, row=1)
		self.Label_Time=Label(self.OptionPricerLabels,text="Expiry (in years): ", bg=self.window_color, fg=self.text_color, anchor="e", width=15, padx=2, pady=2).grid(column=0, row=2)
		self.Label_Spot=Label(self.OptionPricerLabels,text="Underlying Price: ", bg=self.window_color, fg=self.text_color, anchor="e", width=15, padx=2, pady=2).grid(column=0, row=3)
		self.Label_Vol=Label(self.OptionPricerLabels,text="Implied Volatility: ", bg=self.window_color, fg=self.text_color, anchor="e", width=15, padx=2, pady=2).grid(column=0, row=4)
		self.Label_OptionType=Label(self.OptionPricerLabels,text="Option Type", bg=self.window_color, fg=self.text_color, anchor="e", width=15, padx=2, pady=2).grid(column=0, row=5)

		#creates the frame and first entries
		OptionPricerFrame=Frame(self.OptionPricerWindow, bg=self.window_color)
		OptionPricerFrame.grid(column=2, row=4, columnspan=2, padx=5, pady=5)
		OptType=StringVar(OptionPricerFrame)
		OptType.set(OptionPricer.OptionTypeOptionMenu[0])


		Label_LegNumber=Label(OptionPricerFrame, text="Leg "+str(OptionPricer.NumberOfOptions), bg=self.window_color, fg=self.text_color)
		Entry_Strike=Entry(OptionPricerFrame, bg=self.entry_color, fg=self.text_color, width=10)
		Entry_Time=Entry(OptionPricerFrame, bg=self.entry_color, fg=self.text_color, width=10)
		Entry_Spot=Entry(OptionPricerFrame, bg=self.entry_color, fg=self.text_color, width=10)
		Entry_Vol=Entry(OptionPricerFrame, bg=self.entry_color, fg=self.text_color, width=10)
		Menu_OptionType=OptionMenu(OptionPricerFrame,OptType,*OptionPricer.OptionTypeOptionMenu)
		Menu_OptionType.config(bg=self.elements_color, fg=self.text_color, activebackground=self.elements_color, activeforeground=self.text_color, width=4, highlightthickness=0)
		Menu_OptionType["menu"].configure(bg=self.elements_color, fg=self.text_color)

		Label_LegNumber.grid(column=1, row=0)
		Entry_Strike.grid(column=1, row=1, padx=2, pady=2)
		Entry_Time.grid(column=1, row=2, padx=2, pady=2)
		Entry_Spot.grid(column=1, row=3, padx=2, pady=2)
		Entry_Vol.grid(column=1, row=4, padx=2, pady=2)
		Menu_OptionType.grid(column=1, row=5, padx=2, pady=2)

		#Sets up data validation
		self.Valid = self.OptionPricerWindow.register(self.ValidateEntries)
		Entry_Strike.config(validate="key", validatecommand=(self.Valid, '%P'))
		Entry_Time.config(validate="key", validatecommand=(self.Valid, '%P'))
		Entry_Spot.config(validate="key", validatecommand=(self.Valid, '%P'))
		Entry_Vol.config(validate="key", validatecommand=(self.Valid, '%P'))

		#Updates lists
		OptionPricer.AllFrames.append(OptionPricerFrame)
		OptionPricer.AllStrikes.append(Entry_Strike)
		OptionPricer.AllTimes.append(Entry_Time)
		OptionPricer.AllSpots.append(Entry_Spot)
		OptionPricer.AllVols.append(Entry_Vol)
		OptionPricer.AllTypes.append(OptType)
		OptionPricer.AllLabels.append(Label_LegNumber)

	#Adds another option leg to the structure
	def AddLeg(self):
		if OptionPricer.NumberOfOptions >= OptionPricer.LimitNumberOfOptions:
			messagebox.showerror("Limit of number of legs reached", "You have cannot add more than {} legs to the structure.".format(OptionPricer.LimitNumberOfOptions))
		else:
			OptionPricer.NumberOfOptions+=1
			self.Width = 250+((OptionPricer.NumberOfOptions-1)*79)
			self.OptionPricerWindow.geometry(str(self.Width)+"x265")
			OptionPricerFrame=Frame(self.OptionPricerWindow, bg=self.window_color)
			OptionPricerFrame.grid(column=2*OptionPricer.NumberOfOptions, row=4, columnspan=2, padx=5, pady=5)
			OptType=StringVar(OptionPricerFrame)
			OptType.set(OptionPricer.OptionTypeOptionMenu[0])
			
			Label_LegNumber=Label(OptionPricerFrame, text="Leg "+str(OptionPricer.NumberOfOptions), bg=self.window_color, fg=self.text_color)
			Entry_Strike=Entry(OptionPricerFrame, bg=self.entry_color, fg=self.text_color, width=10)
			Entry_Time=Entry(OptionPricerFrame, bg=self.entry_color, fg=self.text_color, width=10)
			Entry_Spot=Entry(OptionPricerFrame, bg=self.entry_color, fg=self.text_color, width=10)
			Entry_Vol=Entry(OptionPricerFrame, bg=self.entry_color, fg=self.text_color, width=10)
			Menu_OptionType=OptionMenu(OptionPricerFrame,OptType,*OptionPricer.OptionTypeOptionMenu)
			Menu_OptionType.config(bg=self.elements_color, fg=self.text_color, activebackground=self.elements_color, activeforeground=self.text_color, width=4, highlightthickness=0)
			Menu_OptionType["menu"].configure(bg=self.elements_color, fg=self.text_color)
			
			Label_LegNumber.grid(column=0, row=0)
			Entry_Strike.grid(column=0, row=1, padx=2, pady=2)
			Entry_Time.grid(column=0, row=2, padx=2, pady=2)
			Entry_Spot.grid(column=0, row=3, padx=2, pady=2)
			Entry_Vol.grid(column=0, row=4, padx=2, pady=2)
			Menu_OptionType.grid(column=0, row=5, padx=2, pady=2)

			#Data validation
			Entry_Strike.config(validate="key", validatecommand=(self.Valid, '%P'))
			Entry_Time.config(validate="key", validatecommand=(self.Valid, '%P'))
			Entry_Spot.config(validate="key", validatecommand=(self.Valid, '%P'))
			Entry_Vol.config(validate="key", validatecommand=(self.Valid, '%P'))

			#Updates lists
			OptionPricer.AllFrames.append(OptionPricerFrame)
			OptionPricer.AllStrikes.append(Entry_Strike)
			OptionPricer.AllTimes.append(Entry_Time)
			OptionPricer.AllSpots.append(Entry_Spot)
			OptionPricer.AllVols.append(Entry_Vol)
			OptionPricer.AllTypes.append(OptType)
			OptionPricer.AllLabels.append(Label_LegNumber)

	#Removes the last leg of the structure
	def RemoveLeg(self):
		if OptionPricer.NumberOfOptions == 1:
			messagebox.showerror("Cannot remove leg", "You have cannot remove the only remaining leg of the structure.")
		else:
			OptionPricer.NumberOfOptions-=1
			self.Width = 250+((OptionPricer.NumberOfOptions-1)*79)
			self.OptionPricerWindow.geometry(str(self.Width)+"x265")
			OptionPricer.AllFrames.pop().destroy()
			OptionPricer.AllStrikes.pop().destroy()
			OptionPricer.AllTimes.pop().destroy()
			OptionPricer.AllSpots.pop().destroy()
			OptionPricer.AllVols.pop().destroy()
			OptionPricer.AllLabels.pop().destroy()
			del OptionPricer.AllTypes[-1]

	#Validates inputs from user
	def ValidateEntries(self, User_Input):
		if User_Input:
			try:
				float(User_Input)
				return True
			except ValueError:
				return False
		if User_Input=="":
			return True
		else:
			return False

	#Creates the option objects for each leg of the structure
	def CreateOption(self):
		#cleans previous options list
		if len(OptionPricer.AllOptions)>0:
			for i in range(len(OptionPricer.AllOptions)):
				del OptionPricer.AllOptions[-1]

		#checks if all option fields are filled
		All_Entries_Valid=True
		for i in range(OptionPricer.NumberOfOptions):
			if (OptionPricer.AllStrikes[i].get()=="" or 
				OptionPricer.AllTimes[i].get()=="" or
				OptionPricer.AllSpots[i].get()=="" or
				OptionPricer.AllVols[i].get()==""):
				All_Entries_Valid=False
				messagebox.showerror("Option data missing", "Option data missing for one or more legs.\nPlease provide all the details before pricing the structure.")

		if All_Entries_Valid:
			for i in range(OptionPricer.NumberOfOptions):
				Strike = float(OptionPricer.AllStrikes[i].get())
				Time = float(OptionPricer.AllTimes[i].get())
				Spot = float(OptionPricer.AllSpots[i].get())
				Vol = float(OptionPricer.AllVols[i].get())
				OptType = OptionPricer.AllTypes[i].get()
				Opt = Option(Strike,Time,OptType,Spot,Vol)
				OptionPricer.AllOptions.append(Opt)
			
			for i in OptionPricer.AllOptions:
				BlackScholes(i)
	
	#Memory management: destroys all objects created to free memory
	def __del__(self):
		for i in range(OptionPricer.NumberOfOptions):
			OptionPricer.AllFrames.pop().destroy()
			OptionPricer.AllStrikes.pop().destroy()
			OptionPricer.AllTimes.pop().destroy()
			OptionPricer.AllSpots.pop().destroy()
			OptionPricer.AllVols.pop().destroy()
			OptionPricer.AllLabels.pop().destroy()
			del OptionPricer.AllTypes[-1]
			
		if len(OptionPricer.AllOptions)>0:
			for i in range(len(OptionPricer.AllOptions)):
				del OptionPricer.AllOptions[-1]

		OptionPricer.NumberOfOptions=1