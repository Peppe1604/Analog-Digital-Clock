// Genera i numeri delle ore lungo il bordo del quadrante
const orologio = document.querySelector('.orologio');
for (let i = 1; i <= 12; i++) {
    const numero = document.createElement('div');
    numero.className = 'numero-orologio';
    numero.textContent = i;
    // Calcola la posizione del numero sul cerchio (12 in alto)
    const angolo = ((i - 3) * 30) * (Math.PI / 180);
    const raggio = 150; // raggio in px per posizionare i numeri
    const x = Math.cos(angolo) * raggio;
    const y = Math.sin(angolo) * raggio;
    numero.style.transform = `translate(-50%, -50%) translate(${x}px, ${y}px)`;
    orologio.appendChild(numero);
}

// Funzione di utilità per formattare i numeri a due cifre
const riempi = n => n.toString().padStart(2, '0');

// Cache degli elementi DOM delle lancette e del digitale
const lancettaOre = document.getElementById('ore');
const lancettaMinuti = document.getElementById('minuti');
const lancettaSecondi = document.getElementById('secondi');
const digitale = document.getElementById('digitale');

// Usa sempre il fuso orario dell'utente rilevato dal browser
const fusoOrario = Intl.DateTimeFormat().resolvedOptions().timeZone;

// Restituisce l'ora corrente nel fuso orario dell'utente
function ottieniOraFuso() {
    const adesso = new Date();
    const opzioni = {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false,
        timeZone: fusoOrario
    };
    // Estrae le parti dell'orario dal formato internazionale
    const parti = new Intl.DateTimeFormat('en-US', opzioni).formatToParts(adesso);
    const ore = parseInt(parti.find(p => p.type === 'hour').value, 10);
    const minuti = parseInt(parti.find(p => p.type === 'minute').value, 10);
    const secondi = parseInt(parti.find(p => p.type === 'second').value, 10);
    // Usa i millisecondi locali per la fluidità delle lancette
    return { ore, minuti, secondi, ms: adesso.getMilliseconds() };
}

// Aggiorna le lancette e l'orario digitale
function aggiornaOrologio() {
    const t = ottieniOraFuso();
    const ore = t.ore;
    const minuti = t.minuti;
    const secondi = t.secondi;
    const ms = t.ms;

    // Calcola gli angoli delle lancette per un movimento fluido
    const angoloSecondi = ((secondi + ms / 1000) / 60) * 360;
    const angoloMinuti = ((minuti + secondi / 60) / 60) * 360;
    const angoloOre = ((ore % 12 + minuti / 60) / 12) * 360;

    // Aggiorna la rotazione delle lancette
    lancettaOre.style.transform = `translate(-50%, 0) rotate(${angoloOre}deg)`;
    lancettaMinuti.style.transform = `translate(-50%, 0) rotate(${angoloMinuti}deg)`;
    lancettaSecondi.style.transform = `translate(-50%, 0) rotate(${angoloSecondi}deg)`;

    // Aggiorna l'orario digitale
    digitale.textContent = `${riempi(ore)}:${riempi(minuti)}:${riempi(secondi)}`;
    requestAnimationFrame(aggiornaOrologio);
}

// Avvia l'orologio
aggiornaOrologio();
