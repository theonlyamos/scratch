import tkinter as tk

app = tk.Tk()
app.title("Scrollbar with Frame Example")

# Create a Frame to hold content
frame = tk.Frame(app)
frame.pack(fill=tk.BOTH, expand=True)

# Create a Canvas to hold widgets and enable scrolling
canvas = tk.Canvas(frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a Scrollbar and associate it with the Canvas
scrollbar = tk.Scrollbar(frame, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)

# Create a Frame to hold widgets within the Canvas
scrollable_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Add widgets to the scrollable frame
for i in range(30):
    label = tk.Label(scrollable_frame, text=f"Label {i}")
    label.pack()

# Configure the Canvas to scroll
scrollable_frame.update_idletasks()  # Update the scrollable_frame size
canvas.config(scrollregion=canvas.bbox("all"))

app.mainloop()
