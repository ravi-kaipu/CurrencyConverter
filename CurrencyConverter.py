import urllib.request
import time
import tkinter as tk
import sys
from beautiful_soup import HTMLfilter
import json

class CurrecyConversionIndicator(object):
    input_data = {}
    
    @staticmethod
    def import_web():
        """
        Get contents from the page.
        :return:
        """
        url = CurrecyConversionIndicator.input_data["url"]
        req = urllib.request.Request(url, headers={'User-Agent': "Chrome Browser"})
        try:
            fp = urllib.request.urlopen(req, timeout=10)
            mybytes = fp.read()
            return str(mybytes)
        except Exception as e:
            CurrecyConversionIndicator.popupmsg("ERROR: Site is unreachable !!", 12)
            exit(-1)

    def get_current_value():
        """
        Get the currency conversion value from the page, it should be done using
        my version of beautfil_soup module.
        """
        string_html = CurrecyConversionIndicator.import_web()
        cl = HTMLfilter()
        search_out = cl.search(string_html, '<span class="text-success">', 1)
        for m in search_out:
            return(m)

    @staticmethod
    def popupmsg(msg, fontsize=18):
        """
        Display the popup window whenever there is change in currency conversion.
        Window automatically destroyed in 20 seconds.
        """
        popup = tk.Tk()
        screen_width = popup.winfo_screenwidth() / 2.5
        screen_height = popup.winfo_screenheight() / 2.5
        popup.wm_title("{} to {} Conversion - TransferWise".format(CurrecyConversionIndicator.input_data["from_currency"], CurrecyConversionIndicator.input_data["to_currency"]))
        popup.geometry("380x130+{}+{}".format(int(screen_width), int(screen_height)))
        popup.configure(background="#338a47")
        label = tk.Label(popup, text=msg)
        label.configure(font=('Sans', fontsize, 'bold'), background="#338a47", fg="white")
        label.pack(side="top", fill="x", pady=20)
        B1 = tk.Button(popup, text="Dismiss", command = popup.destroy, cursor="hand2")
        B1.configure(font=('Sans','12','bold'),background = 'red', fg="white")
        B1.place(x=150, y=75)
        popup.after(20000, lambda: popup.destroy())
        popup.lift()
        popup.mainloop()

    @staticmethod
    def get_current_time():
        """
        Get current local time
        :return:
        """
        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        return current_time

    @staticmethod
    def printer(data):
        sys.stdout.write("\r\x1b[K" + data.__str__())
        sys.stdout.flush()
        time.sleep(1)

    @staticmethod
    def load_json():
        """
        Fetching the conversion details from file.
        From currency: SEK
        TO currency: INR
        Interval: how frequent we fetch the data from the page.
        """
        input_file = "conversion_details.json"
        with open(input_file, "r") as jsonfile:
            data = json.load(jsonfile)
            return(data)

    @classmethod
    def run(cls):
        cls.input_data = CurrecyConversionIndicator.load_json()
        first_time = False
        min_value = 0
        greatest_value = 0
        while True:
            value = cls.get_current_value()
            if not value:
                cls.popupmsg("Data is not found in the URL", 12)
                time.sleep(60)
                continue
            cls.printer("Current Value: %s, diff:%f, %20s"%(value, abs(float(min_value)- float(value)), cls.get_current_time()))
            # Set your own conditions to get popup display
            if ((value != min_value) or float(value) > greatest_value) or float(value) > greatest_value:
                message = "%s"%value
                if first_time:
                    message = "%s -> %s"%(min_value, value)
                cls.popupmsg(message)
                cls.printer("\033[F")
                print("{} to {}: ".format(cls.input_data["from_currency"], cls.input_data["to_currency"]), value, ", ", cls.get_current_time(), ", variation:", abs(float(min_value)- float(value)))
                min_value = value
                first_time = True
            if float(value) > greatest_value:
                greatest_value = float(value)
            time.sleep(cls.input_data["interval"])

CurrecyConversionIndicator.run()