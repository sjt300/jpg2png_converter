from tkinter import *
from tkinter.filedialog import askopenfilenames, askdirectory
from PIL import Image, ImageTk
file_list = []

root = Tk()
root.title("jpg2pngConverter")
root.geometry("800x800")
# list box to display files that are being considered
file_list_box = Listbox(root)
file_list_box.pack(fill=BOTH, expand=True)
# base frame to house the buttons
base_frame = Frame(root)
# canvas to display thumbnail when item is double-clicked
thumb_canvas = Canvas(root)


class Commands:
    def __init__(self, li, box, canvas):
        self.li = li
        self.box = box
        self.canvas = canvas

    def clear(self):
        self.li = []
        file_list_box.delete(0, END)
        self.canvas.destroy()

    def populate_box(self):
        self.box.delete(0, END)
        for i in self.li:
            self.box.insert(END, i)

    def add_file(self):
        files = askopenfilenames(initialdir="/", title="Select File(s)", filetypes=(("JPG files", "*.jpg"),
                                                                                    ("all files", "*.*")))
        for i in files:
            self.li.append(i)
        self.populate_box()

    def remove(self):
        if self.box.curselection() != ():
            self.li.remove(self.box.get(self.box.curselection()[0:]))
            self.box.delete(self.box.curselection())

    def convert(self):
        if self.li != []:
            directory = askdirectory()
            for jpg in self.li:
                img = Image.open(jpg)
                img.save(directory + "/" + jpg.split("/")[-1][:-3] + "png", "png")

    def preview_img(self, event):
        try:
            self.canvas.destroy()
            self.canvas = Canvas(root)
            img = Image.open(self.box.get(self.box.curselection()[0]))
            img.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(img)
            thumb_lbl = Label(self.canvas, image=photo)
            thumb_lbl.image = photo
            thumb_lbl.pack()
            self.canvas.pack()
        except IndexError:
            return 0


inst = Commands(file_list, file_list_box, thumb_canvas)
inst.populate_box()

clear_btn = Button(base_frame, text="Clear", command=inst.clear)
clear_btn.grid(row=0, column=0)
add_file_btn = Button(base_frame, text="Add File(s)", command=inst.add_file)
add_file_btn.grid(row=0, column=1)
remove_file_btn = Button(base_frame, text="Remove File", command=inst.remove)
remove_file_btn.grid(row=0, column=2)
convert_btn = Button(base_frame, text="Convert", command=inst.convert)
convert_btn.grid(row=0, column=3)
exit_button = Button(base_frame, text="Exit", command=root.destroy)
exit_button.grid(row=0, column=4)
help_lbl = Label(base_frame, text="Double Click File for Preview")
help_lbl.grid(row=1, column=0, columnspan=5)
base_frame.pack()


file_list_box.bind("<Double-Button-1>", inst.preview_img)

root.mainloop()