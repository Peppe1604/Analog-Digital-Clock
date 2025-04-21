# 🕒 Analog-Digital Clock

Un orologio moderno **analogico e digitale**, disponibile sia in versione **Web** (HTML/CSS/JS) che **Desktop** (Python con DearPyGui). Progettato con un’interfaccia elegante, fluide animazioni e supporto ai **fusi orari internazionali**.

---

## Indice

- [Caratteristiche](#caratteristiche)
- [Struttura del progetto](#struttura-del-progetto)
- [Versione Web](#versione-web)
  - [Requisiti](#requisiti)
  - [Avvio](#avvio)
- [Versione Python](#versione-python)
  - [Requisiti](#requisiti-1)
  - [Avvio](#avvio-1)
- [Screenshot](#screenshot)
- [Autore](#autore)

---

## Caratteristiche

- 🔰 Orologio **analogico** con lancette animate in tempo reale
- ⏱️ Visualizzazione **digitale** sincronizzata
- 📱 **Responsive design** per una perfetta resa su ogni dispositivo (Web)
- 🌍 **Supporto multilingua e fusi orari internazionali** (Python)
- 🎨 Interfaccia moderna con **temi personalizzabili**
- ⚙️ Progetto **modulare e facilmente estendibile**

---

## Struttura del progetto

```bash
Analog-Digital-Clock/
│
├── Web_Version/                # Versione Web
│   ├── clock.html              # Interfaccia HTML
│   ├── clock.css               # Stile grafico
│   └── clock.js                # Logica JavaScript
│
└── Python_Version/            # Versione Desktop
    ├── main.py                 # Entry point principale
    ├── gui.py                  # Gestione GUI con DearPyGui
    ├── clock_app.py            # Versione alternativa dell'app
    ├── clock_dearpygui.py      # Implementazione alternativa
    └── timezone_helper.py      # Gestione fusi orari
```

---

## Versione Web

### Requisiti

- Browser moderno (Chrome, Firefox, Edge, Safari)

### Avvio

1. Apri la cartella `Web_Version`
2. Fai doppio clic su `clock.html` oppure aprilo nel browser

---

## Versione Python

### Requisiti

- Python 3.8 o superiore
- Librerie necessarie:
  - [`dearpygui`](https://github.com/hoffstadt/DearPyGui)
  - [`pytz`](https://pypi.org/project/pytz/)

Installa le dipendenze con:

```bash
pip install dearpygui pytz
```

### Avvio

1. Vai nella cartella `Python_Version`
2. Esegui uno degli script disponibili:

```bash
python main.py
```

oppure

```bash
python clock_app.py
```

oppure

```bash
python clock_dearpygui.py
```

---

## Screenshot

### Web Version

![Web Clock Screenshot](Web-Clock.png)

### Python Version

![Python Clock Screenshot](Python-Clock.png)

---

## Autore

**Giuseppe**  
📬 Contributi, domande o suggerimenti? Sentiti libero di aprire una *pull request* o contattarmi!

---

> ⭐ *Se ti piace il progetto, lascia una stella alla repo!*
