import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, Pango, GdkPixbuf
from pymavlink import mavutil
import time, math

class TransparentWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="pyOSD for OpenIPC FPV")
        self.set_default_size(400, 200)

        # Make the window transparent
        self.set_app_paintable(True)
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
        
        # Allow resizing of the window
        self.set_resizable(True)

        # horizontal and vertical boxes for labels of osd
        hbox = Gtk.Box(spacing=0)
        hbox.set_homogeneous(False)
        vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox_left.set_homogeneous(False)
        vbox_mid = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox_mid.set_homogeneous(False)
        vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox_right.set_homogeneous(False)

        hbox.pack_start(vbox_left, True, True, 0)
        hbox.pack_start(vbox_mid, True, True, 0)
        hbox.pack_start(vbox_right, True, True, 0)

        rssi_icon = Gtk.Image.new_from_file("./icons/rssi_wtfosd.png")
        thr_icon = Gtk.Image.new_from_file("./icons/throttle_evilm1.png")
        roll_icon = Gtk.Image.new_from_file("./icons/roll_wtfosd.png")
        pitch_icon = Gtk.Image.new_from_file("./icons/pitch_wtfosd.png")
        cam_icon = Gtk.Image.new_from_file("./icons/temp_sneaky_origin.png")
        fly_icon = Gtk.Image.new_from_file("./icons/fly_wtfosd_origin.png")
        self.bat_icon = Gtk.Image()
        self.bat_icon.set_from_file("./icons/bat80_evilm1.png")
        self.stick1_icon = Gtk.Image.new_from_file("./icons/dot.png")
        self.stick2_icon = Gtk.Image.new_from_file("./icons/dot.png")
        alt_icon = Gtk.Image.new_from_file("./icons/alt_wtfosd.png")
        speed_icon = Gtk.Image.new_from_file("./icons/speed_wtfosd.png")

        
        # Create labels for displaying OSD information with White text, 100% opacity
        self.arm_label = Gtk.Label(label=" ARM")
        self.arm_label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1))
        self.armtime_label = Gtk.Label(label=" 00:00")
        self.armtime_label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1))
        self.flightmode_label = Gtk.Label(label=" MODE\n")
        self.flightmode_label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1))
        self.battery_label = Gtk.Label(label=" BAT")
        self.battery_label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1)) 
        self.rssi_label = Gtk.Label(label=" RSSI")
        self.rssi_label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1))  
        self.camera_label = Gtk.Label(label=" CAM")
        self.camera_label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1))  
        self.camera_label.set_justify(Gtk.Justification.LEFT)
        self.thr_label = Gtk.Label(label=" THR")
        self.thr_label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1)) 
        self.roll_label = Gtk.Label(label=" ROLL")
        self.roll_label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1)) 
        self.roll_label.get_style_context().add_class("osd-label")
        self.pitch_label = Gtk.Label(label=" PITCH")
        self.pitch_label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1)) 
        self.alt_label = Gtk.Label(label=" ALT")
        self.alt_label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1)) 
        self.speed_label = Gtk.Label(label=" SPEED")
        self.speed_label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1)) 

        
        # Set up the layout with a horizontal box
        rssi_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.rssi_spase = Gtk.Box(spacing=0)
        rssi_box.pack_start(self.rssi_spase, False, True, 0)
        rssi_box.pack_start(rssi_icon, False, True, 0)
        rssi_box.pack_start(self.rssi_label, False, True, 0)
        
        thr_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        thr_box.pack_start(thr_icon, False, False, 0)
        thr_box.pack_start(self.thr_label, False, False, 0)

        roll_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        roll_box.pack_start(roll_icon, False, False, 0)
        roll_box.pack_start(self.roll_label, False, False, 0)

        pitch_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        pitch_box.pack_start(pitch_icon, False, False, 0)
        pitch_box.pack_start(self.pitch_label, False, False, 0)

        self.cam_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.cam_box.pack_start(cam_icon, False, False, 0)
        self.cam_box.pack_start(self.camera_label, False, False, 0)
        
        self.bat_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.bat_box.pack_start(self.bat_icon, False, False, 0)
        self.bat_box.pack_start(self.battery_label, True, True, 0)
        self.bat_box.set_size_request(250, 0)

        self.fly_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.fly_box.pack_start(fly_icon, False, False, 0)
        self.fly_box.pack_start(self.armtime_label, False, False, 0)

        self.alt_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.alt_box.pack_end(self.alt_label, False, False, 0)
        self.alt_box.pack_end(alt_icon, False, False, 0)
        
        self.speed_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.speed_box.pack_end(self.speed_label, False, False, 0)
        self.speed_box.pack_end(speed_icon, False, False, 0)
        
        # sticks boxes
        self.stick1_frame = Gtk.Frame()
        self.stick1_frame.get_style_context().add_class("white-border")  # Add a CSS class for styling
        self.stick1_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.stick1_frame.set_size_request(120, 120)
        self.stick1_frame.add(self.stick1_icon)

        self.stick2_frame = Gtk.Frame()
        self.stick2_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.stick2_box.get_style_context().add_class("white-border")  # Add a CSS class for styling
        self.stick2_frame.set_size_request(120, 120)
        self.stick2_frame.add(self.stick2_icon)

        self.sticks_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.sticks_space = Gtk.Box(spacing=0)
        self.sticks_space2 = Gtk.Box(spacing=0)
        self.sticks_space.set_size_request(100, 0)
        self.sticks_box.pack_start(self.sticks_space, False, False, 0)
        self.sticks_box.pack_start(self.stick1_frame, False, False, 0)
        self.sticks_box.pack_start(self.stick2_frame, False, False, 0)
        self.sticks_box.pack_start(self.sticks_space2, True, True, 0)
        
        # Pack labels in the desired order and position
        # openipc logo
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename="./icons/openipc_logo.png", 
            width=150, 
            height=150, 
            preserve_aspect_ratio=True)
        self.logo = Gtk.Image.new_from_pixbuf(self.pixbuf)
        self.logo.set_alignment(1, 0.5)
        vbox_right.pack_start(self.logo, False, False, 0)

        self.arm_label.set_alignment(0, 0.5)  # xalign left, yalign mid
        self.armtime_label.set_alignment(0, 0.5)
        self.flightmode_label.set_alignment(0, 0.5)
        self.camera_label.set_alignment(0, 0.5)
        self.battery_label.set_alignment(0, 0.5)
        self.thr_label.set_alignment(0, 0.5)
        self.rssi_label.set_alignment(0.5, 0.5)
        rssi_icon.set_alignment(0.5, 0.5)
        self.alt_label.set_alignment(0, 0.5)
        self.speed_label.set_alignment(0, 0.5)
        self.stick1_icon.set_alignment(0, 0)
        self.stick2_icon.set_alignment(0, 0)
        vbox_left.pack_start(self.arm_label, False, False, 0)
        vbox_left.pack_start(self.flightmode_label, False, False, 0)
        vbox_left.pack_start(self.fly_box, False, False, 0)
        vbox_left.pack_start(self.cam_box, False, False, 0)   
        vbox_left.pack_end(self.bat_box, False, False, 0)
        vbox_left.pack_end(roll_box, False, False, 0)
        vbox_left.pack_end(pitch_box, False, False, 0)
        vbox_left.pack_end(thr_box, False, False, 0)
        vbox_mid.pack_start(rssi_box, False, False, 0)
        vbox_mid.pack_end(self.sticks_box, False, False, 0)
        vbox_right.pack_end(self.speed_box, False, False, 0)
        vbox_right.pack_end(self.alt_box, False, False, 0)
        
        self.add(hbox)

        self.mavlink_connection = mavutil.mavlink_connection('udpin:224.0.0.1:14550')
        self.start_time = None  # Variable to hold armed time

        # Start a timer for updating OSD information
        self.update_osd()
        self.update_window()

        # Connect to the window's configure-event to handle resizing
        self.connect("configure-event", self.on_configure_event)

    def update_osd(self):
        # Retrieve OSD information
        msg = self.mavlink_connection.recv_match(blocking=False)
        if msg:
            #print(msg)
            if msg.get_type() == 'HEARTBEAT':
                if msg.custom_mode == 0:
                    self.flightmode_label.set_text('ANGLE\n')
                elif msg.custom_mode == 1:    
                    self.flightmode_label.set_text('ACRO\n')
                if msg.system_status == 4:
                    self.arm_label.set_markup('<span foreground="orange"><b><big>ARMED</big></b></span>'
                    )
                    if self.start_time == None:
                        self.start_time = time.time()  # Record start time when armed
                elif msg.system_status == 3:
                    self.arm_label.set_markup('<span foreground="lightgreen"><b><big>DISARMED</big></b></span>'
                    )
                    self.start_time = None  # Clear start time when disarmed
            elif msg.get_type() == 'SYS_STATUS':
                self.battery_label.set_text(
                    " %.2fV %.2fA" % (msg.voltage_battery/1000.0, msg.current_battery/100.0) 
                )
                if msg.battery_remaining <= 60:
                    self.bat_icon.set_from_file("./icons/bat60_evilm1.png")
                    
                elif msg.battery_remaining <= 40:
                    self.bat_icon.set_from_file("./icons/bat40_evilm1.png")
                    
            elif msg.get_type() == 'RC_CHANNELS_RAW':
                # self.rssi = msg.rssi
                self.rssi_label.set_text(
                    " %d %% " %(msg.rssi / 254.0 * 100.0)
                )
                rc_roll = int(msg.chan1_raw/10-100)
                rc_pitch = int(msg.chan2_raw/10-100)
                rc_yaw = int(msg.chan3_raw/10-100)
                rc_thr = int(msg.chan4_raw/10-100)
                # Calculate desired dot position based on rc_roll and rc_pitch
                self.stick1_icon.set_margin_start(rc_yaw)  # Set x position of dot
                self.stick1_icon.set_margin_top((100-rc_thr))   # Set y position of dot
                self.stick2_icon.set_margin_start(rc_roll)  # Set x position of dot
                self.stick2_icon.set_margin_top((100-rc_pitch))   # Set y position of dot
                #print(rc_roll, rc_pitch, rc_thr, rc_yaw)
            elif msg.get_type() == 'ATTITUDE':
                self.roll_label.set_text(f" {msg.roll * 180 / math.pi:.1f} °")
                self.pitch_label.set_text(f" {msg.pitch * 180 / math.pi:.1f} °")
                #self.yaw = msg.yaw*180/math.pi
            elif msg.get_type() == 'VFR_HUD':
                self.thr_label.set_text(
                    " %d %%" %(msg.throttle)
                )
                if msg.alt == 0.0:
                    self.alt_label.set_text(" %.1f m   " % (msg.alt))
                    self.alt_box.show()
                if msg.airspeed == 0.0:
                    self.speed_label.set_text(" %.1f m/s" % (msg.airspeed))
                    self.speed_box.show()
            # read cam temperature from latest mavfwd and show cam_box on osd
            elif msg.id == 0: #msg.get_type() == 'RAW_IMU': # 
                self.camera_label.set_text(" %d °C" %(msg.temperature / 100))
                self.cam_box.show()
            # elif msg.get_type() == 'GPS_RAW_INT':
            #     print(msg)
            # elif msg.get_type() == 'GLOBAL_POSITION_INT':
            #     print(msg)    
            # elif msg.get_type() == 'GPS_GLOBAL_ORIGIN':
            #     print(msg)       
        
        if self.start_time is not None:
            armed_time = time.time() - self.start_time
            self.armtime_label.set_text(' %02u:%02u' % (int(armed_time)/60, int(armed_time)%60))

        # Update every 5ms
        GLib.timeout_add(10, self.update_osd)
        
    def on_configure_event(self, widget, event):
        # Adjust label font size based on window width
        width = event.width
        font_size = width // 50  # Example: Adjust font size based on 1/50 of window width
        font_desc = Pango.FontDescription()
        font_desc.set_size(font_size * Pango.SCALE)
        self.battery_label.override_font(font_desc)
        self.rssi_label.override_font(font_desc)
        self.camera_label.override_font(font_desc)
        self.thr_label.override_font(font_desc)
        self.roll_label.override_font(font_desc)
        self.pitch_label.override_font(font_desc)
        self.arm_label.override_font(font_desc)
        self.armtime_label.override_font(font_desc)
        self.flightmode_label.override_font(font_desc)
        self.alt_label.override_font(font_desc)
        self.speed_label.override_font(font_desc)
        self.rssi_spase.set_size_request(width/8, 0)
        
    
    def load_css(self):
        # Load CSS file for custom styling
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('styles.css')
        screen = Gdk.Screen.get_default()
        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider,
                                        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
    def update_window(self):
        self.hide()
        self.show()
        GLib.timeout_add(100, self.update_window) # every 0.1s erase the afterimage of osd elements
    
if __name__ == "__main__":
    win = TransparentWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    win.cam_box.hide()
    win.maximize()
    Gtk.main()