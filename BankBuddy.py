from tkinter import *
from chat import get_response, bot_name
import webbrowser

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
BG_WHITE = "#fafcff"
TEXT_COLOR = "#EAECEE"
YELLOW_COLOR = "#ffbb00"
WHITE_COLOR = "#f7faf8"
CURSOR_COLOR = "#946e06"
BLACK_COLOR = "#000712"
RED_COLOR = "#8c0000"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class BankBotApplication:
    
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        
    def run(self):
        self.window.mainloop()
        
    def _setup_main_window(self):
        self.window.title("Your Friendly Chat BOT")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)
        
        window_width = 700
        window_height = 450
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        position_x = int((screen_width - window_width) / 2)
        position_y = int((screen_height - window_height) / 2)
        self.window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Title
        head_label = Label(self.window, bg=BG_WHITE, fg=RED_COLOR,
                           text="BankBuddy", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)
        
        # divider
        line = Label(self.window, width=450, bg=RED_COLOR)
        line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        # Chat View area
        self.text_widget = Text(self.window, width=10, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="hand2", state=DISABLED)
        
        # msg Color
        self.text_widget.tag_configure("user", foreground=WHITE_COLOR, justify='right', lmargin1=15, lmargin2=15)
        self.text_widget.tag_configure("bot", foreground=YELLOW_COLOR, justify='left', lmargin1=50, lmargin2=50)
        self.text_widget.tag_configure("link", foreground="blue", underline=True)
        
        # Insert welcome message
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, f"{bot_name}: Welcome to BankBuddy! How can I assist you today?\n\n", "bot")
        self.text_widget.configure(state=DISABLED)

        # scroll bar
        scrollbar = Scrollbar(self.window, command=self.text_widget.yview)
        scrollbar.place(relheight=0.745, relx=0.01, rely=0.08, relwidth=0.02)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = Label(self.window, bg=WHITE_COLOR, height=80)
        bottom_label.place(relwidth=1, rely=0.825)
        
        # Request area
        self.msg_entry = Entry(bottom_label, bg=BLACK_COLOR, fg=WHITE_COLOR, font=FONT, insertbackground=WHITE_COLOR)
        self.msg_entry.place(relwidth=0.70, relheight=0.04, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
        
        # button
        send_icon = PhotoImage(file="img/icons8-send-60.png") 
        send_button = Button(bottom_label, image=send_icon, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             compound=LEFT, command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.72, rely=0.008, relheight=0.04, relwidth=0.25)
        send_button.configure(cursor="hand2")
        send_button.image = send_icon

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "Me")
        
    def _insert_message(self, msg, sender):
        if not msg:
            return
        
        self.msg_entry.delete(0, END)
        
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1, "user")
        self.text_widget.configure(state=DISABLED)
        
        response = get_response(msg)
        msg2 = f"{bot_name}: {response}\n\n"
        self.text_widget.configure(state=NORMAL)
        
        # Handle response with plain URL at the end
        url_start_idx = response.find("http://")
        if url_start_idx == -1:
            url_start_idx = response.find("https://")

        if url_start_idx != -1:
            pre_link_text = msg2[:url_start_idx]
            url = response[url_start_idx:].split()[0]  # Extract the URL
            post_link_text = msg2[url_start_idx + len(url):]

            self.text_widget.insert(END, pre_link_text, "bot")
            self.text_widget.insert(END, url, ("link",))
            self.text_widget.tag_bind("link", "<Button-1>", lambda e, url=url: webbrowser.open(url))
            self.text_widget.insert(END, post_link_text, "bot")
        else:
            self.text_widget.insert(END, msg2, "bot")
        
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)
        
if __name__ == "__main__":
    app = BankBotApplication()
    app.run()
