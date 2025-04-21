import dearpygui.dearpygui as dpg
import pytz
from datetime import datetime
import math

# --- Funzioni di utilità per fusi orari ---

fusi_orari = pytz.all_timezones

def get_lista_paesi():
    # Restituisce la lista dei macro-paesi/aree disponibili nei fusi orari
    return sorted(set([tz.split('/')[0] for tz in fusi_orari if '/' in tz and tz.split('/')[0].isalpha()]))

def get_fusi_per_paese(paese):
    # Restituisce tutti i fusi orari per il paese selezionato
    return [tz for tz in fusi_orari if tz.startswith(paese + "/")]

def get_ora_corrente(nome_fuso):
    # Restituisce la data e ora corrente per il fuso orario scelto
    return datetime.now(pytz.timezone(nome_fuso))

# --- Funzioni grafiche e logica orologio ---

def disegna_orologio():
    """
    Disegna il quadrante dell'orologio analogico e aggiorna il display digitale.
    """
    dpg.delete_item("canvas_orologio", children_only=True)
    fuso_orario = dpg.get_value("combo_fuso")
    adesso = get_ora_corrente(fuso_orario)
    centro_x, centro_y, raggio = 130, 130, 110

    # Disegna il quadrante (blu moderno)
    dpg.draw_circle((centro_x, centro_y), raggio, color=(0,123,255,255), thickness=6, parent="canvas_orologio")
    dpg.draw_circle((centro_x, centro_y), raggio-6, color=(222,242,255,255), thickness=220, fill=(222,242,255,255), parent="canvas_orologio")

    # Tacche delle ore (blu e azzurro alternati)
    for i in range(12):
        angolo = math.radians(i * 30 - 90)
        x1 = centro_x + (raggio - 18) * math.cos(angolo)
        y1 = centro_y + (raggio - 18) * math.sin(angolo)
        x2 = centro_x + (raggio - 38) * math.cos(angolo)
        y2 = centro_y + (raggio - 38) * math.sin(angolo)
        colore_tacca = (0,123,255,255) if i % 2 == 0 else (0,212,255,255)
        dpg.draw_line((x1, y1), (x2, y2), color=colore_tacca, thickness=4, parent="canvas_orologio")

    # Calcola posizione delle lancette
    ora = adesso.hour % 12
    minuti = adesso.minute
    secondi = adesso.second + adesso.microsecond / 1_000_000

    # Lancetta delle ore (blu scuro)
    angolo_ore = math.radians((ora + minuti / 60) * 30 - 90)
    x_ore = centro_x + (raggio - 55) * math.cos(angolo_ore)
    y_ore = centro_y + (raggio - 55) * math.sin(angolo_ore)
    dpg.draw_line((centro_x, centro_y), (x_ore, y_ore), color=(0,82,204,255), thickness=12, parent="canvas_orologio")

    # Lancetta dei minuti (azzurro)
    angolo_minuti = math.radians((minuti + secondi / 60) * 6 - 90)
    x_minuti = centro_x + (raggio - 30) * math.cos(angolo_minuti)
    y_minuti = centro_y + (raggio - 30) * math.sin(angolo_minuti)
    dpg.draw_line((centro_x, centro_y), (x_minuti, y_minuti), color=(0,212,255,255), thickness=7, parent="canvas_orologio")

    # Lancetta dei secondi (blu chiaro)
    angolo_secondi = math.radians(secondi * 6 - 90)
    x_secondi = centro_x + (raggio - 15) * math.cos(angolo_secondi)
    y_secondi = centro_y + (raggio - 15) * math.sin(angolo_secondi)
    dpg.draw_line((centro_x, centro_y), (x_secondi, y_secondi), color=(0,180,255,255), thickness=3, parent="canvas_orologio")

    # Centro dell'orologio (bianco)
    dpg.draw_circle((centro_x, centro_y), 10, color=(255,255,255,255), fill=(255,255,255,255), parent="canvas_orologio")

    # Aggiorna il display digitale
    dpg.set_value("ora_digitale", adesso.strftime("%H:%M:%S"))

def cambio_paese(sender, app_data, user_data):
    """
    Callback quando si cambia il paese: aggiorna la lista dei fusi orari disponibili.
    """
    paese = dpg.get_value("combo_paese")
    fusi = get_fusi_per_paese(paese)
    if fusi:
        dpg.configure_item("combo_fuso", items=fusi, default_value=fusi[0])
    else:
        dpg.configure_item("combo_fuso", items=["UTC"], default_value="UTC")
    disegna_orologio()

def cambio_fuso(sender, app_data, user_data):
    """
    Callback quando si cambia il fuso orario: ridisegna l'orologio.
    """
    disegna_orologio()

def aggiornamento_periodico():
    """
    Aggiorna periodicamente l'orologio ogni pochi frame.
    """
    disegna_orologio()
    dpg.set_frame_callback(dpg.get_frame_count() + 2, aggiornamento_periodico)

def avvia_orologio():
    """
    Inizializza e avvia la GUI dell'orologio.
    """
    dpg.create_context()
    with dpg.font_registry():
        dpg.add_font("C:\\Windows\\Fonts\\seguiemj.ttf", 32, tag="font_grande")

    # Stile personalizzato per le combo
    with dpg.theme(tag="combo_theme") as style:
        with dpg.theme_component(dpg.mvCombo):
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (222,242,255,255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (222,242,255,255))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (0,123,255,255))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (0,82,204,255))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 4)

    paesi = get_lista_paesi()
    paese_default = "Europe"
    fusi_default = get_fusi_per_paese(paese_default)

    with dpg.window(label="Orologio Moderno", width=360, height=540, tag="finestra_principale", no_title_bar=True, no_move=True, no_resize=True):
        # Centra tutto con un gruppo verticale
        with dpg.group(horizontal=False):
            dpg.add_spacer(height=10)
            dpg.add_text("Paese:", color=(0,123,255))
            combo_paese = dpg.add_combo(paesi, default_value=paese_default, callback=cambio_paese, width=220, tag="combo_paese")
            dpg.bind_item_theme(combo_paese, "combo_theme")
            dpg.add_spacer(height=4)
            dpg.add_text("Fuso orario:", color=(0,123,255))
            combo_fuso = dpg.add_combo(fusi_default, default_value=fusi_default[0], callback=cambio_fuso, width=220, tag="combo_fuso")
            dpg.bind_item_theme(combo_fuso, "combo_theme")
            dpg.add_spacer(height=10)
            dpg.add_drawlist(width=260, height=260, tag="canvas_orologio")
            dpg.add_spacer(height=30)
            # Riquadro attorno all'orologio digitale centrato
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=10)
                with dpg.child_window(width=280, height=70, border=True):
                    dpg.add_spacer(height=8)
                    dpg.add_text("", tag="ora_digitale", color=(0,123,255))
                dpg.add_spacer(width=10)
            dpg.add_spacer(height=10)
    dpg.create_viewport(title='Orologio Moderno', width=360, height=540)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.bind_item_font("ora_digitale", "font_grande")
    aggiornamento_periodico()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    avvia_orologio()
