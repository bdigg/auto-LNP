import CTkGUI.appgui as appgui
import datetime 
import CTkGUI.db as db 

if __name__ == "__main__":
    app = appgui.App()
    app.mainloop()
    print(datetime.datetime.now())

