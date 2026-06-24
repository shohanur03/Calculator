import flet as ft

# Global variable to store the calculation string
screen_data = ""


def press_key(user_input):
    """Processes calculator button inputs and returns the updated display text."""
    global screen_data

    # Intercept empty screen inputs on operational keys to stop math execution crashes
    if user_input == "=" and screen_data == "":
        return "0"

    if user_input == "=":
        try:
            if "%" in screen_data:
                if "*" in screen_data or "/" in screen_data:
                    screen_data = screen_data.replace("%", "/100")
                else: 
                    for operator in ["+", "-"]:
                        if operator in screen_data:
                            base, percent_part = screen_data.split(operator)
                            percent_value = percent_part.replace("%", "")
                            calculated_percentage = f"(({base} * {percent_value}) / 100)"
                            screen_data = f"{base}{operator}{calculated_percentage}"
                            break
            # Safely evaluate structural formula values
            screen_data = str(eval(screen_data))
        except Exception:
            screen_data = "Error"
            
    elif user_input == "backspace":
        screen_data = screen_data[:-1]
        
    elif user_input == "C":
        screen_data = ""
        
    else:
        # Halt sequential duplicate decimal point entries
        if user_input == "." and screen_data.endswith("."):
            pass
        else:
            screen_data += user_input

    return screen_data if screen_data != "" else "0"


def main(page: ft.Page):
    page.title = "Calculator Made by SR Jibon"
    page.window_width = 350
    page.window_height = 500
    page.bgcolor = "#1A1A1A"
    page.padding = 20

    # UI Element Initialization
    display_label = ft.Text(value="0", size=38, color="white", text_align=ft.TextAlign.RIGHT)
    
    # Concrete coordinate mapping (1.0, 0.0) for cross-platform center-right alignment
    display_container = ft.Container(
        content=display_label,
        alignment=ft.alignment.Alignment(1.0, 0.0),
        padding=10,
        height=80
    )

    def button_clicked(e):
        button_text = e.control.content.value
        logical_input = "backspace" if button_text == "⌫" else button_text
        display_label.value = press_key(logical_input)
        page.update()

    # Highly-Adaptive Keyboard Event Handler
    def handle_keyboard(e: ft.KeyboardEvent):
        valid_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "*", "/", ".", "=", "%"]
        
        # Check if shift modifier is active to override numerical capture manually if needed
        if e.shift and e.key == "5":
            key_pressed = "%"
        elif e.shift and e.key == "8":
            key_pressed = "*"
        elif e.shift and e.key == "=":
            key_pressed = "+"
        else:
            key_pressed = e.key

        # Execution Routing
        if key_pressed in valid_chars:
            display_label.value = press_key(key_pressed)
        elif key_pressed == "Enter":
            display_label.value = press_key("=")
        elif key_pressed == "Backspace":
            display_label.value = press_key("backspace")
        elif key_pressed.upper() == "C" or key_pressed == "Escape":
            display_label.value = press_key("C")
            
        page.update()

    # Bind explicitly to Flet window-level keyboard listener interface
    page.on_keyboard_event = handle_keyboard

    # 2D Structural Array Layer mapping layout rows and columns
    buttons = [
        ["C", "%", "⌫", "/"],
        ["7", "8", "9", "*"],
        ["4", "5", "6", "-"],
        ["1", "2", "3", "+"],
        ["0", ".", "="]
    ]

    grid_rows = []
    for row in buttons:
        row_controls = []
        for text in row:
            btn_expand = 2 if text == "0" else 1
            is_action = text in ["C", "%", "⌫", "/", "*", "-", "+", "="]
            btn_bg = "#1E3A8A" if is_action else "#2D2D2D"
            
            btn = ft.Container(
                content=ft.Text(value=text, size=20, color="white"),
                alignment=ft.alignment.Alignment(0.0, 0.0),
                on_click=button_clicked,
                bgcolor=btn_bg,
                border_radius=8,
                expand=btn_expand,
                height=65
            )
            row_controls.append(btn)
            
        grid_rows.append(ft.Row(controls=row_controls, spacing=8, expand=True))

    page.add(
        display_container,
        ft.Column(controls=grid_rows, spacing=8, expand=True)
    )


if __name__ == "__main__":
    ft.app(target=main)