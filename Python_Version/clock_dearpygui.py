import dearpygui.dearpygui as dpg
import pytz
from datetime import datetime
import math

# Ottieni tutte le timezone e la lista dei macro-paesi/aree
timezones = pytz.all_timezones
countries = sorted(set([tz.split('/')[0] for tz in timezones if '/' in tz and tz.split('/')[0].isalpha()]))

def get_timezones_for_country(country):
    # Restituisce tutti i fusi orari per il paese selezionato
    return [tz for tz in timezones if tz.startswith(country + "/")]

def draw_clock():
    """
    Disegna il quadrante dell'orologio analogico e aggiorna il display digitale.
    """
    dpg.delete_item("clock_canvas", children_only=True)
    tz = dpg.get_value("tz_combo")
    now = datetime.now(pytz.timezone(tz))
    cx, cy, r = 130, 130, 110

    # Quadrante
    dpg.draw_circle((cx, cy), r, color=(238,187,195,255), thickness=6, parent="clock_canvas")
    dpg.draw_circle((cx, cy), r-6, color=(184,193,236,255), thickness=220, fill=(184,193,236,255), parent="clock_canvas")

    # Tacche ore
    for i in range(12):
        angle = math.radians(i * 30 - 90)
        x1 = cx + (r - 18) * math.cos(angle)
        y1 = cy + (r - 18) * math.sin(angle)
        x2 = cx + (r - 38) * math.cos(angle)
        y2 = cy + (r - 38) * math.sin(angle)
        dpg.draw_line((x1, y1), (x2, y2), color=(35,41,70,255), thickness=4, parent="clock_canvas")

    # Calcola posizione delle lancette
    hour = now.hour % 12
    minute = now.minute
    second = now.second + now.microsecond / 1_000_000

    # Lancetta ore
    hour_angle = math.radians((hour + minute / 60) * 30 - 90)
    hx = cx + (r - 55) * math.cos(hour_angle)
    hy = cy + (r - 55) * math.sin(hour_angle)
    dpg.draw_line((cx, cy), (hx, hy), color=(238,187,195,255), thickness=12, parent="clock_canvas")

    # Lancetta minuti
    min_angle = math.radians((minute + second / 60) * 6 - 90)
    mx = cx + (r - 30) * math.cos(min_angle)
    my = cy + (r - 30) * math.sin(min_angle)
    dpg.draw_line((cx, cy), (mx, my), color=(35,41,70,255), thickness=7, parent="clock_canvas")

    # Lancetta secondi
    sec_angle = math.radians(second * 6 - 90)
    sx = cx + (r - 15) * math.cos(sec_angle)
    sy = cy + (r - 15) * math.sin(sec_angle)
    dpg.draw_line((cx, cy), (sx, sy), color=(255,216,3,255), thickness=3, parent="clock_canvas")

    # Centro
    dpg.draw_circle((cx, cy), 10, color=(255,255,255,255), fill=(255,255,255,255), parent="clock_canvas")

    # Display digitale
    dpg.set_value("digital_time", now.strftime("%H:%M:%S"))

def on_country_change(sender, app_data, user_data):
    """
    Callback quando si cambia il paese: aggiorna la lista dei fusi orari disponibili.
    """
    country = dpg.get_value("country_combo")
    tzs = get_timezones_for_country(country)
    if tzs:
        dpg.configure_item("tz_combo", items=tzs, default_value=tzs[0])
    else:
        dpg.configure_item("tz_combo", items=["UTC"], default_value="UTC")
    draw_clock()

def on_tz_change(sender, app_data, user_data):
    """
    Callback quando si cambia il fuso orario: ridisegna l'orologio.
    """
    draw_clock()

def periodic_update():
    """
    Aggiorna periodicamente l'orologio ogni pochi frame.
    """
    draw_clock()
    dpg.set_frame_callback(dpg.get_frame_count() + 2, periodic_update)

def run_clock():
    """
    Inizializza e avvia la GUI dell'orologio.
    """
    dpg.create_context()
    # Carica il font per il display digitale
    with dpg.font_registry():
        font_big = dpg.add_font("C:\\Windows\\Fonts\\seguiemj.ttf", 32, tag="font_big")
    with dpg.window(label="Orologio Moderno", width=300, height=440, tag="main_window"):
        # Gruppo verticale per allineare tutto
        with dpg.group(horizontal=False):
            dpg.add_spacer(height=12)
            dpg.add_text("Paese:", color=(238,187,195))
            dpg.add_spacer(height=2)
            dpg.add_combo(
                countries,
                default_value="Europe",
                callback=on_country_change,
                width=220,
                tag="country_combo"
            )
            dpg.add_spacer(height=8)
            dpg.add_text("Fuso orario:", color=(238,187,195))
            dpg.add_spacer(height=2)
            default_tzs = get_timezones_for_country("Europe")
            dpg.add_combo(
                default_tzs,
                default_value=default_tzs[0],
                callback=on_tz_change,
                width=220,
                tag="tz_combo"
            )
            dpg.add_spacer(height=8)
            dpg.add_drawlist(width=260, height=260, tag="clock_canvas")
            dpg.add_spacer(height=8)
            dpg.add_text("", tag="digital_time", color=(238,187,195))

    dpg.create_viewport(title='Orologio Moderno', width=320, height=480)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.bind_item_font("digital_time", "font_big")
    periodic_update()
    dpg.start_dearpygui()
    dpg.destroy_context()
