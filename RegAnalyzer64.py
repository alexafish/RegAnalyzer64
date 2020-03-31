import tkinter as tk
import sys
#from tkinter import ttk

#style = tk.Style()     # Create style
#style.configure("Blue.TFrame", fg="blue") # Set bg color

class RegAnalyzer():
    def __init__(self, obj):
        self.obj = obj
        self.maxDigit = 16
        self.maxBit = 4
        self.bitCount = self.maxDigit*self.maxBit
        self.mightyList = []
        self.bitLabel = []
        self.bitEntry = []
        self.bitValue = []
        self.col = 0
        self.row = 0
        self.shiftBit = tk.IntVar(None, 1)
        self.var = tk.StringVar()
        self.numsys = tk.StringVar(None, "Hex")
        self.initMainPanel(obj)
        self.initFuncButton(obj)
        self.initResultPanel(obj)
        self.initTypeButton(obj)
        self.clearBits()

    def SLBits(self):
        value = int(self.getResult())
        value = (value<<self.getShift()) & 0xFFFFFFFFFFFFFFFF
        self.setResult(value)
        self.calBits(None, None, None)

    def SRBits(self):
        value = int(self.getResult())
        value = (value>>self.getShift()) & 0xFFFFFFFFFFFFFFFF
        self.setResult(value)
        self.calBits(None, None, None)

    def formatBits(self, entry, val):
        if val==1:
            entry.config({"readonlybackground": "Yellow"})
        else:
            entry.config({"readonlybackground": "White"})

    def clearBits(self):
        for bit in range(0, self.bitCount):
            self.bitValue[bit].set(0)
            self.bitEntry[bit].config({"readonlybackground": "White"})
        self.setResult(self.calResult())

    def getShift(self):
        return self.shiftBit.get()

    def getResult(self):
        try:
            if self.numsys.get() == "Dec":
                v=int(self.var.get(), 10)
            elif self.numsys.get() == "Oct":
                v=int(self.var.get(), 8)
            else:
                v=int(self.var.get(), 16)
        except:
            pass
        else:
            return v

    def setResult(self, v):
        if self.numsys.get() == "Dec":
            self.var.set(format(v, 'd'))
        elif self.numsys.get() == "Oct":
            self.var.set(format(v, 'o'))
        else:
            self.var.set(format(v, 'X'))

    def calResult(self):
        bits = self.maxBit*self.maxDigit
        data = 0
        for b in range(bits):
            data = data | self.bitValue[b].get() << (bits-1-b)
        return data

    def calBits(self, a, b, c):
        _v = self.getResult()
        if _v is not None:
            for bit in range(0, self.bitCount):
                v = (_v >> (self.bitCount - bit - 1))&0x1
                self.bitValue[bit].set(v)
                self.formatBits(self.bitEntry[bit], v)

    def handleClick(self, event, entry):
        v=event.get()
        v=(~v)&0x1
        event.set(v)
        #self.var.set(format(self.calResult(), 'X'))
        self.numSysSelect()
        self.formatBits(entry, v)

    def numSysSelect(self):
        self.setResult(self.calResult())

    def exit(self):
        sys.exit(0)

    def initMainPanel(self, obj):
        for digit in range(0, self.maxDigit):
            if digit>7 and self.row==0:
                self.row=self.row+8
                self.col=0
            self.mightyList.append(tk.LabelFrame(obj, text=self.maxDigit-digit-1, labelanchor="se"))
            self.mightyList[digit].grid(column=self.col, row=self.row, padx=6, pady=10)
            for bit in range(0, self.maxBit):
                idx = digit*4+bit
                self.bitLabel.append(tk.Label(self.mightyList[digit], width=3, text=(self.maxDigit-digit-1)*4+(self.maxBit-bit-1)))
                self.bitLabel[idx].grid(column=self.col, row=self.row+1)
                self.bitLabel[idx].configure(anchor="center")
                self.bitValue.append(tk.BooleanVar())
                """ example of write event """
                self.bitEntry.append(tk.Entry(self.mightyList[digit], width=3, textvariable=self.bitValue[idx]))
                self.bitEntry[idx].grid(column=self.col, row=self.row+2, sticky="ew")
                self.bitEntry[idx].bind("<1>", (lambda *_, event=self.bitValue[idx], entry=self.bitEntry[idx]: self.handleClick(event, entry)))    #buttonpress-1
                self.bitEntry[idx].configure(state='readonly')
                self.col=self.col+1

    def initFuncButton(self, obj):
        #swap_button = tk.Button(obj, text="Swap", width=10)
        #swap_button.grid(column=20, row=self.row+1)
        clearButton = tk.Button(obj, text="Clear", width=10, command=self.clearBits)
        clearButton.grid(column=24, row=self.row+1)
        closeButton = tk.Button(obj, text="Close", width=10, command=self.exit)
        closeButton.grid(column=28, row=self.row+1)

    def initResultPanel(self, obj):
        mightyWord = tk.LabelFrame(obj, labelanchor="se")
        mightyWord.grid(column=4, columnspan=20, row=self.row+1)
        wordLabel = tk.Label(mightyWord, text="MSB")
        wordLabel.grid(row=self.row+1, sticky=tk.W)
        wordLabel2 = tk.Label(mightyWord, text="LSB")
        wordLabel2.grid(row=self.row+1, sticky=tk.E)
        self.var.set(format(self.calResult(), 'X'))
        #self.var.trace("w", lambda *_, var=self.var: self.calBits(var))
        self.var.trace("w", self.calBits)
        wordEntry = tk.Entry(mightyWord, width=24, textvariable=self.var)
        wordEntry.grid(row=self.row+2)
        shift = tk.Frame(mightyWord)
        shlButton = tk.Button(shift, text="<< Shift", width=10, command=self.SLBits)
        shlButton.pack(side="left", fill="both", expand="yes")
        shEntry = tk.Entry(shift, width=5, textvariable=self.shiftBit)
        shEntry.pack(side="left", fill="both", expand="yes")
        sfrButton = tk.Button(shift, text="Shift >>", width=10, command=self.SRBits)
        sfrButton.pack(side="left", fill="both", expand="yes")
        shift.grid(column=0, row=self.row+3)

    def initTypeButton(self, obj):
        mighty_radio = tk.LabelFrame(obj, labelanchor="se")
        mighty_radio.grid(column=0, columnspan=12, row=self.row+1, padx=6)
        r1 = tk.Radiobutton(mighty_radio, text='Hex', variable=self.numsys, value='Hex', command=self.numSysSelect)
        r1.grid(column=0, row=self.row+1, padx=6)
        r2 = tk.Radiobutton(mighty_radio, text='Dec', variable=self.numsys, value='Dec', command=self.numSysSelect)
        r2.grid(column=0, row=self.row+2, padx=6)
        r3 = tk.Radiobutton(mighty_radio, text='Oct', variable=self.numsys, value='Oct', command=self.numSysSelect)
        r3.grid(column=0, row=self.row+3, padx=6)

def main():
    """ RegAnalyzer """
    ra = tk.Tk()

    """ icon """
    #ra.iconphoto(False, tk.PhotoImage(file='D:\Python\python_gui\search2.png'))

    """ window title """
    ra.title('Register Analysis. v1.0, AlexHung @ Realtek')

    """ window size """
    ra.geometry('1000x250')

    RegAnalyzer(ra)

    """ main loop, must!!! """
    ra.mainloop()


if __name__ == '__main__':
    main()

