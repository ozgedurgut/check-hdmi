import os

def check_hdmi_connection(self):
    command = "xrandr | grep -w connected | grep -v primary"
    # return information about attached external monitors
    external_monitors = os.popen(command).read()
    if external_monitors:
        if not self.display_move_ok:
            self.join_display(external_monitors)
    else:
        self.display_move_ok = False

def join_display(self, external_monitors):
    try:
        monitor_positions = []
        for line in external_monitors.splitlines():
            if ' connected' in line:
                parts = line.split()
                monitor_name = parts[0]
                for part in parts:
                    if '+' in part and 'x' in part:
                        position = part
                        monitor_positions.append((monitor_name, position))
                        break
        # plots the positions of the monitors
        window_id = 0
        window_exist_command = "wmctrl -lx"
        # To use the wmctrl command, you need to install it according to your device's architecture.
        window_exist = os.popen(window_exist_command).read()
        window_list = window_exist.split("\n")
        for window in window_list:
            if 'Your Window Name' in window:
                parts = window.split()
                window_id = parts[0]

        monitor, position = monitor_positions[0]
        pos_parts = position.split('+')
        if len(pos_parts) >= 3:
            x = pos_parts[1]
            y = pos_parts[2]
            print("x: "+x)
            print("y: "+y)

        # To use the xdotool command, you need to install it according to your device's architecture.
        print(f"xdotool windowmove {window_id} {x} {y}")
        os.system(f"xdotool windowmove {window_id} {x} {y}")

        print("display move ok")
        self.display_move_ok = True

        user_home = os.path.expanduser("~")
        destination_path = os.path.join(user_home, "gnome-randr.py")
        if os.path.exists(destination_path):
            os.system("python3 ~/gnome-randr.py --output DSI-1 --off")
            #     DSI-1 : Name of the device whose screen you want to dim
        else:
            print("gnome-randr.py not found")

    except Exception as e:
        print(f"display move fail: {e} ")
