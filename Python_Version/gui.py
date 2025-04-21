import dearpygui.dearpygui as dpg
from timezone_helper import get_lista_paesi, get_fusi_per_paese, get_ora_corrente
import math

def disegna_orologio():
    """
    Disegna il quadrante dell'orologio analogico e le sue lancette
    in base al fuso orario selezionato.
    """
    dpg.delete_item("canvas_orologio", children_only=True)
    fuso_orario = dpg.get_value("combo_fuso")
    adesso = get_ora_corrente(fuso_orario)
    centro_x, centro_y, raggio = 180, 180, 160  # Centro e dimensione quadrante

    # Disegna il bordo sfumato blu del quadrante
    for i in range(10, 0, -1):
        colore = (30, 144, min(255 + i*2, 255), 180)
        dpg.draw_circle((centro_x, centro_y), raggio + i, color=colore, thickness=1, parent="canvas_orologio")
    # Bordo esterno blu navy
    dpg.draw_circle((centro_x, centro_y), raggio, color=(25, 25, 112, 255), thickness=6, parent="canvas_orologio")
    # Riempimento quadrante (azzurro chiaro)
    dpg.draw_circle((centro_x, centro_y), raggio-6, color=(240,248,255,255), thickness=220, fill=(240,248,255,255), parent="canvas_orologio")

    # Tacche delle ore (blu navy)
    for i in range(12):
        angolo = math.radians(i * 30 - 90)
        x1 = centro_x + (raggio - 18) * math.cos(angolo)
        y1 = centro_y + (raggio - 18) * math.sin(angolo)
        x2 = centro_x + (raggio - 38) * math.cos(angolo)
        y2 = centro_y + (raggio - 38) * math.sin(angolo)
        dpg.draw_line((x1, y1), (x2, y2), color=(25,25,112,255), thickness=5, parent="canvas_orologio")

    # Tacche dei minuti (azzurro chiaro)
    for i in range(60):
        if i % 5 == 0:
            continue
        angolo = math.radians(i * 6 - 90)
        x1 = centro_x + (raggio - 18) * math.cos(angolo)
        y1 = centro_y + (raggio - 18) * math.sin(angolo)
        x2 = centro_x + (raggio - 28) * math.cos(angolo)
        y2 = centro_y + (raggio - 28) * math.sin(angolo)
        dpg.draw_line((x1, y1), (x2, y2), color=(135,206,250,180), thickness=2, parent="canvas_orologio")

    ora = adesso.hour % 12
    minuti = adesso.minute
    secondi = adesso.second + adesso.microsecond / 1_000_000

    # Lancetta delle ore (azzurro scuro)
    angolo_ore = math.radians((ora + minuti / 60) * 30 - 90)
    x_ore = centro_x + (raggio - 65) * math.cos(angolo_ore)
    y_ore = centro_y + (raggio - 65) * math.sin(angolo_ore)
    dpg.draw_line((centro_x, centro_y), (x_ore, y_ore), color=(0,191,255,255), thickness=13, parent="canvas_orologio")

    # Lancetta dei minuti (blu)
    angolo_minuti = math.radians((minuti + secondi / 60) * 6 - 90)
    x_minuti = centro_x + (raggio - 35) * math.cos(angolo_minuti)
    y_minuti = centro_y + (raggio - 35) * math.sin(angolo_minuti)
    dpg.draw_line((centro_x, centro_y), (x_minuti, y_minuti), color=(0,123,255,255), thickness=8, parent="canvas_orologio")

    # Lancetta dei secondi (azzurro acceso)
    angolo_secondi = math.radians(secondi * 6 - 90)
    x_secondi = centro_x + (raggio - 18) * math.cos(angolo_secondi)
    y_secondi = centro_y + (raggio - 18) * math.sin(angolo_secondi)
    dpg.draw_line((centro_x, centro_y), (x_secondi, y_secondi), color=(0,255,255,255), thickness=3, parent="canvas_orologio")

    # Centro dell'orologio (blu navy e azzurro)
    dpg.draw_circle((centro_x, centro_y), 13, color=(25,25,112,255), fill=(25,25,112,255), parent="canvas_orologio")
    dpg.draw_circle((centro_x, centro_y), 6, color=(0,191,255,255), fill=(0,191,255,255), parent="canvas_orologio")

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
    # Carica il font per eventuale uso futuro (non usato qui)
    with dpg.font_registry():
        dpg.add_font("C:\\Windows\\Fonts\\calibri.ttf", 38, tag="font_digitale")

    # Tema personalizzato per le combo box
    with dpg.theme(tag="combo_theme") as style:
        with dpg.theme_component(dpg.mvCombo):
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (240,248,255,255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (222,242,255,255))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (0,191,255,255))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (25,25,112,255))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 6)

    # Ottieni lista paesi e fusi orari di default
    paesi = get_lista_paesi()
    paese_default = "Europe"
    fusi_default = get_fusi_per_paese(paese_default)

    # Crea la finestra principale e i widget
    with dpg.window(label="Orologio Moderno", width=520, height=700, tag="finestra_principale", no_title_bar=True, no_move=True, no_resize=True):
        with dpg.group(horizontal=False):
            dpg.add_spacer(height=18)
            dpg.add_text("Paese:", color=(0,123,255))
            combo_paese = dpg.add_combo(paesi, default_value=paese_default, callback=cambio_paese, width=250, tag="combo_paese")
            dpg.bind_item_theme(combo_paese, "combo_theme")
            dpg.add_spacer(height=6)
            dpg.add_text("Fuso orario:", color=(0,123,255))
            combo_fuso = dpg.add_combo(fusi_default, default_value=fusi_default[0], callback=cambio_fuso, width=250, tag="combo_fuso")
            dpg.bind_item_theme(combo_fuso, "combo_theme")
            dpg.add_spacer(height=18)
            dpg.add_drawlist(width=360, height=360, tag="canvas_orologio")
            dpg.add_spacer(height=10)
    # Imposta viewport e avvia ciclo principale
    dpg.create_viewport(title='Orologio Moderno', width=520, height=700)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    aggiornamento_periodico()
    dpg.start_dearpygui()
    dpg.destroy_context()
