import customtkinter as ctk

# Global variable to store the calculation string
screen_data = ""


def press_key(user_input):
    """Processes calculator button inputs and returns the updated display text."""
    global screen_data

    if user_input == "=":
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

    elif user_input == "backspace":
        screen_data = screen_data[:-1]

    elif user_input == "c":
        screen_data = ""

    else:
        # Prevent consecutive decimal points (e.g., 5.5.5)
        if user_input == "." and screen_data.endswith("."):
            pass
        else:
            screen_data += user_input

    return screen_data if screen_data != "" else "0"


# --- GUI Layout and Initialization ---

# Initialize the main system window
app = ctk.CTk()
app.title("Dynamic Calc")
app.geometry("350x500")

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
    for col_idx, text in enumerate(row):
        # Special case: Make the '0' button span across 2 columns
        colspan = 2 if text == "0" else 1

        # Local closure function to safely handle specific character mapping
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
            column=col_idx,
            columnspan=colspan,
            padx=5,
            pady=5,
            sticky="nsew",
        )

# Configure layout weights for seamless window resizing responsiveness
for i in range(5):
    button_frame.rowconfigure(i, weight=1)
for i in range(4):
    button_frame.columnconfigure(i, weight=1)

# Start the Framework Main Loop
app.mainloop()