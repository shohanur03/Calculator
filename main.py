import customtkinter as ctk

# Global variable to store the calculation string
screen_data = ""


def press_key(user_input):
    """Processes calculator button inputs and returns the updated display text."""
    global screen_data

    # Fix: If screen is empty, ignore equal sign inputs to prevent false errors
    if (user_input == "=" or user_input == "\r") and screen_data == "":
        return "0"

    if user_input == "=" or user_input == "\r":  # '\r' handles the physical Enter key
        try:
            # Handle percentage conversion universally before evaluation
            if "%" in screen_data:
                # Standalone multiplication/division context: e.g., 50*10%
                if "*" in screen_data or "/" in screen_data:
                    screen_data = screen_data.replace("%", "/100")
                else: 
                    # Contextual addition/subtraction: e.g., 100+5%
                    for operator in ["+", "-"]:
                        if operator in screen_data:
                            base, percent_part = screen_data.split(operator)
                            percent_value = percent_part.replace("%", "")
                            # Mathematical conversion: 100 + ((100 * 5) / 100)
                            calculated_percentage = (
                                f"(({base} * {percent_value}) / 100)"
                            )
                            screen_data = (
                                f"{base}{operator}{calculated_percentage}"
                            )
                            break

            # Evaluate the clean mathematical string
            screen_data = str(eval(screen_data))
        except Exception:
            screen_data = "Error"

    elif user_input in ["backspace", "\x08"]:  # '\x08' handles the physical Backspace key
        screen_data = screen_data[:-1]

    elif user_input in ["C", "c", "\x1b"]:  # '\x1b' handles the physical Escape key for Clear
        screen_data = ""

    else:
        # Prevent consecutive decimal points (e.g., 5.5.5)
        if user_input == "." and screen_data.endswith("."):
            pass
        else:
            screen_data += user_input

    return screen_data if screen_data != "" else "0"


def handle_keyboard(event):
    """Intercepts physical keyboard inputs and maps them to the calculator logic."""
    valid_chars = "0123456789+-*/.%="
    
    if event.char in valid_chars:
        updated_text = press_key(event.char)
        display_label.configure(text=updated_text)
    elif event.keysym == "Return":
        updated_text = press_key("=")
        display_label.configure(text=updated_text)
    elif event.keysym == "BackSpace":
        updated_text = press_key("backspace")
        display_label.configure(text=updated_text)
    elif event.keysym in ["Escape", "c", "C"]:
        updated_text = press_key("C")
        display_label.configure(text=updated_text)


# --- GUI Layout and Initialization ---

# Initialize the main system window
app = ctk.CTk()
app.title("Calculator Made by SR Jibon")
app.geometry("350x500")

# Bind global keyboard inputs to the application window
app.bind("<Key>", handle_keyboard)

# Set the theme to match a slick, minimalist styling
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Display Screen (This will show the calculations)
display_label = ctk.CTkLabel(
    master=app, text="0", font=("Arial", 32), anchor="e"
)
display_label.pack(pady=20, padx=20, fill="x")

# --- Button Grid Configuration ---

# 2D list matrix representing the grid layout
buttons = [
    ["C", "%", "backspace", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "="],
]

# Container frame for the button matrix
button_frame = ctk.CTkFrame(master=app)
button_frame.pack(pady=10, padx=20, fill="both", expand=True)

# Loop to dynamically generate and place buttons based on the matrix layout
for row_idx, row in enumerate(buttons):
    actual_col = 0  # Track the exact grid column positioning dynamically
    for col_idx, text in enumerate(row):
        # Special case: Make the '0' button span across 2 columns
        colspan = 2 if text == "0" else 1

        def make_click_handler(char):
            return lambda: display_label.configure(text=press_key(char))

        btn = ctk.CTkButton(
            master=button_frame,
            text=text,
            font=("Arial", 20),
            width=60,
            height=60,
            command=make_click_handler(text),
        )
        
        btn.grid(
            row=row_idx,
            column=actual_col,  # Positions the button at the correct tracked column
            columnspan=colspan,
            padx=5,
            pady=5,
            sticky="nsew",
        )
        
        # Increment the column tracker by the span of the current button
        actual_col += colspan

# Configure layout weights for seamless window resizing responsiveness
for i in range(5):
    button_frame.rowconfigure(i, weight=1)
for i in range(4):
    button_frame.columnconfigure(i, weight=1)

# Start the Framework Main Loop
app.mainloop()