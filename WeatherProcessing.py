'''By Apollo Hodges and Laura Finkelstein'''

'''
This code uses multiprocessing (mp) to find the temperature in various cities and allows the user to store
this information into a .txt file in the directory of their choosing. The original purpose of this project
was to test the speed of multiprocessing versus multithreading.
'''
import requests
import time
import multiprocessing as mp
import os
import tkinter.filedialog
import tkinter as tk
import tkinter.messagebox as tkmb

def getInfo(city):
    ''' Looks up weather information '''
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},CA,US&units=imperial&appid=ad9a4658cee9d2eee9f77c1d74a34459"
    page = requests.get(url)
    data = page.json()
    temperature = round((data['main']['temp']))
    description = (data['weather'][0]['description'])
    return city, temperature, description


class DialogWin(tk.Toplevel):
    ''' GUI for choices '''
    def __init__(self, master, dict):
        super().__init__(master)
        self.grab_set()
        self.title("Choose a city")
        self._choice = -1
        self.ctrlVar = tk.StringVar()
        self.sortedDict = sorted(dict)
        for key in self.sortedDict:
            str = key + " " + dict[key]
            tk.Radiobutton(self, text=str, variable=self.ctrlVar, value=key).grid(sticky='w')
        self.ctrlVar.set(self.sortedDict[0])

        finish = tk.Button(self, text="ok", command= self._userChoice).grid(sticky='s')



    def _userChoice(self):
        self._choice = self.ctrlVar.get()
        self.destroy()

    def getChoice(self):
        ''' Provide user's choice'''
        return self._choice



class MainWindow(tk.Tk):
    ''' GUI for Weather Look-up '''
    def __init__(self):
        super().__init__()

        self.weatherList = dict()
        self.cityD = {'Berkeley': '(UCB)', 'Cupertino': '(De Anza)', 'Davis': '(UCD)', 'Irvine': '(UCI)',
                      'Los Angeles': '(UCLA)',
                      'Palo Alto': '(Stanford)', 'Sacramento': '(Sac State)', 'San Diego': '(UCSD)',
                      'San Jose': '(SJSU)',
                      'Santa Barbara': '(UCSB)', 'Santa Clara': '(SCU)', 'Santa Cruz': '(UCSC)'}
        start = time.time()
        pool = mp.Pool(processes=12)
        results = pool.map(getInfo, self.cityD)
        for item in results:
            self.weatherList = {item[0]: (item[1], item[2]) for item in results}

        print("Total elapsed time: {:.2f}s".format(time.time() - start))

        self.title("Welcome to the weather app")
        tk.Button(self, text="Choose a city", fg="black", command = lambda : self._cityChoice(self.cityD)).\
            grid(padx=10, pady=10, columnspan=2)
        S = tk.Scrollbar(self)
        self._LB = tk.Listbox(self, height=12, width=50, yscrollcommand=S.set)
        self._LB.grid()
        S.grid(row=1, column=3, sticky="NS")
        S.config(command=self._LB.yview)
        self.protocol("WM_DELETE_WINDOW", self._quitting)


    def _cityChoice(self, city):
        dw = DialogWin(self, city)
        self.wait_window(dw)
        wc = dw.getChoice()
        if wc != -1:
            weatherString = f'{wc}: {self.weatherList[wc][0]} degrees, {self.weatherList[wc][1]}'
            self._LB.insert(tk.END, weatherString)

    def _quitting(self):
        infoList = self._LB.get(0, tk.END)
        if infoList:
            answer = tkmb.askokcancel("Save", "Save your search in a directory of your choice?", parent=self)
            if answer:
                d = tk.filedialog.askdirectory(initialdir='.')
                if d:
                    os.chdir(d)
                    with open('weather.txt', 'w') as fh:
                        for line in infoList:
                            newline = line + '\n'
                            fh.write(newline)

                    tkmb.showinfo('Save', f'File weather.txt has been saved in {d}', parent=self)
        self.destroy()


def main():
    '''Starts the application'''
    a = MainWindow()
    a.mainloop()

    
if __name__ == '__main__':
    main()

