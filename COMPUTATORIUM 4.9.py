from colorama import init, Fore, Style
import math

init(autoreset=True)

cronologia = []

colpi = {
    100: (".22 LR", 50, 2, 99, 5, 2),
    120: ("9mm", 50, 2, 99, 5, 2),
    150: (".45ACP", 40, 1, 80, 2, 2),
    160: ("10.2x22(.40 S&W)", 50, 1, 99, 5, 1),
    170: ("5.7x28", 50, 1, 99, 5, 1),
    200: ("9x39", 300, 1, 400, 5, 1),
    250: (".357 Magnum", 50, 1, 150, 2, 5),
    300: (".44 Magnum", 75, 1, 175, 2, 5),
    333: ("4C-P", 100, 1, 120, 2, 2),
    350: ("5.56x45", 475, 1, 550, 2, 5),
    400: ("7.62x39", 300, 1, 400, 2, 5),
    444: (".410 Bore", 20, 5, 30, 7, 5),
    450: ("ÆX-PWR", 150, 1, 200, 2, 2),
    475: ("7.62x51", 700, 1, 800, 2, 5),
    500: ("7.62x54", 800, 1, 1000, 2, 5),
    550: ("7.62×63(.30-06)", 800, 1, 1000, 2, 5),
    555: ("12 gauge", 50, 2, 70, 5, 5),
    575: ("4C-AR", 800, 1, 1000, 2, 5),
    600: (".300", 1100, 1, 1200, 2, 1),
    666: ("10 gauge", 50, 2, 70, 5, 5),
    750: (".338 Lapua", 1500, 1, 1600, 2, 1),
    777: ("ÆX-ARWR", 900, 1, 1200, 2, 5),
    888: ("4C-MG", 800, 1, 1000, 2, 5),
    900: (".408 Cheytac", 2000, 1, 2100, 2, 1),
    1000: (".50 BMG", 1500, 1, 1600, 2, 1),
    1111: ("ÆX-MGWR", 950, 1, 1100, 2, 5),
    1500: ("ÆX-SHGWR", 70, 2, 100, 5, 5),
    2000: ("ÆX-SWR", 2200, 1, 2500, 2, 1),
}

munizioni_bonus = {
    "N": (0, ""),
    "FP": (5, "Punta piatta"),
    "FMJ": (5, "Full Metal Jacket"),
    "HP": (5, "Hollow Point"),
    "AP": (10, "Armor Piercing"),
    "HS": (10, "Hypersonic")
}

abbreviazioni_parti = {
    "t": "Testa",
    "b": "Busto",
    "bd": "Braccio dx",
    "bs": "Braccio sx",
    "gd": "Gamba dx",
    "gs": "Gamba sx"
}

abbreviazioni_armature = {
    "dyneema": "Dyneema",
    "spectra": "Spectra",
    "kevlar": "Kevlar",
    "tawron": "Tawron",
    "ceramica": "Ceramica Balistica",
    "titanio": "Titanio",
    "acciaio": "Acciaio Balistico",
    "asg": "ASG"
}

armature = {
    "Dyneema": {"Protezione": 9, "Resistenza": 6, "Peso": 2, "Calibro": "7.62x54", "PV": 3000},
    "Spectra": {"Protezione": 8, "Resistenza": 5, "Peso": 3, "Calibro": ".410 Bore", "PV": 2220},
    "Kevlar": {"Protezione": 7, "Resistenza": 4, "Peso": 3, "Calibro": "7.62x39", "PV": 1600},
    "Tawron": {"Protezione": 6, "Resistenza": 3, "Peso": 4, "Calibro": "5.56x45", "PV": 1050},
    "Ceramica Balistica": {"Protezione": 10, "Resistenza": 1, "Peso": 4, "Calibro": "7.62x63", "PV": 550},
    "Titanio": {"Protezione": 7, "Resistenza": 7, "Peso": 7, "Calibro": "7.62x39", "PV": 3850},
    "Acciaio Balistico": {"Protezione": 9, "Resistenza": 8, "Peso": 8, "Calibro": "7.62x54", "PV": 4400},
    "ASG": {"Protezione": 5, "Resistenza": 3, "Peso": 5, "Calibro": "9x39", "PV": 600},
}

def calcola_malus(distanza, gittata_util, malus_1, soglia, malus_2, malus_danno):
    """
    Calcola i malus in base alla distanza.
    """
    if distanza <= gittata_util:
        return 0, 0
    elif distanza <= soglia:
        return malus_1 * (distanza - gittata_util), 0
    else:
        return malus_1 * (soglia - gittata_util) + malus_2 * (distanza - soglia), malus_danno * (distanza - soglia)

def calcola_danno(abilita_arma, danno_base, precisione, colpi_sparati, distanza, munizione_code, circostanza_precisione, armatura):
    """
    Calcola il danno totale in base ai parametri forniti, tenendo conto dell'armatura.
    """
    precisione_arma = (abilita_arma * 10) // 2
    precisione_totale = precisione + precisione_arma + circostanza_precisione
    
    # Limita la precisione totale al massimo di 100%
    precisione_totale = min(precisione_totale, 100)
    
    colpi_a_segno = math.floor(colpi_sparati * (precisione_totale / 100))
    
    malus_precisione, malus_danno = calcola_malus(distanza, *colpi[danno_base][1:])
    precisione_totale -= malus_precisione
    
    danno_normale = danno_base * colpi_a_segno
    bonus_munizione = munizioni_bonus.get(munizione_code, (0, ""))[0]
    danno_munizione = bonus_munizione * colpi_a_segno

    danno_totale = (danno_normale + danno_munizione)
    danno_totale -= (danno_totale * malus_danno / 100)

    malus_precisione_totale = colpi_a_segno * (100 - precisione_totale) // 100
    danno_finale = danno_totale - malus_precisione_totale

    if precisione_totale >= 100:
        danno_finale *= 2

    # Calcolo danno armatura
    pv_armatura = 0
    danno_armatura = 0
    
    # Se un'armatura è specificata e non è vuota
    if armatura and armatura.strip():
        armatura_completa = abbreviazioni_armature.get(armatura[:3].lower(), armatura)
        protezione = armature[armatura_completa]["Protezione"]
        resistenza = armature[armatura_completa]["Resistenza"]
        pv_armatura = armature[armatura_completa]["PV"]

        danno_armatura = danno_finale
        danno_armatura -= (danno_armatura * protezione / 100)
        pv_armatura -= danno_armatura

        if pv_armatura <= 0:
            danno_armatura = danno_finale
        else:
            danno_armatura = 0

    return round(danno_finale), precisione_totale, colpi_a_segno, bonus_munizione, munizioni_bonus.get(munizione_code, ("", ""))[1], pv_armatura, danno_armatura

def aggiorna_punti_vita(punti_vita, danno, bersagli):
    """
    Aggiorna i punti vita delle parti del corpo specificate in 'bersagli' in base al danno ricevuto.
    """
    danno_per_parte = danno // len(bersagli)
    for parte in bersagli:
        punti_vita[parte] = max(punti_vita[parte] - danno_per_parte, 0)

def formattazione_punti_vita(punti_vita):
    """
    Restituisce una stringa con la formattazione dei punti vita, evidenziando in rosso le parti con 0 punti vita.
    """
    return " - ".join(
        [Fore.RED + abbreviazione.upper() + Style.RESET_ALL if punti_vita[parte] == 0 else abbreviazione.upper() + ":" + str(punti_vita[parte])
         for abbreviazione, parte in abbreviazioni_parti.items()]
    )

def inserisci_dati():
    """
    Inserisce i dati dell'utente e calcola il danno.
    """
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "\n==============================================================================================================")
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "░█████╗░░█████╗░███╗░░░███╗██████╗░██╗░░░██╗████████╗░█████╗░████████╗░█████╗░██████╗░██╗██╗░░░██╗███╗░░░███╗")
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "██╔══██╗██╔══██╗████╗░████║██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██║██║░░░██║████╗░████║")
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "██║░░╚═╝██║░░██║██╔████╔██║██████╔╝██║░░░██║░░░██║░░░███████║░░░██║░░░██║░░██║██████╔╝██║██║░░░██║██╔████╔██║")
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "██║░░██╗██║░░██║██║╚██╔╝██║██╔═══╝░██║░░░██║░░░██║░░░██╔══██║░░░██║░░░██║░░██║██╔══██╗██║██║░░░██║██║╚██╔╝██║")
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░░░░░╚██████╔╝░░░██║░░░██║░░██║░░░██║░░░╚█████╔╝██║░░██║██║╚██████╔╝██║░╚═╝░██║")
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "==============================================================================================================")
    stato = input(Fore.LIGHTGREEN_EX + "Buono o Cattivo (B/C): ")
    nome = input(Fore.LIGHTGREEN_EX + "Nome: ")

    punti_vita = {
        "Testa": 100,
        "Busto": 100,
        "Braccio dx": 100,
        "Braccio sx": 100,
        "Gamba dx": 100,
        "Gamba sx": 100
    }

    try:
        colpi_sparati = int(input(Fore.LIGHTGREEN_EX + "Numero Colpi Sparati: "))
        bersaglio = input(Fore.LIGHTGREEN_EX + "Bersaglio: ")
        parti_colpite = input(Fore.LIGHTGREEN_EX + "Parti Colpite: ").split(", ")
        parti_colpite = [abbreviazioni_parti[parte] for parte in parti_colpite]
        
        # Nuova logica per verificare se ogni parte è corazzata
        armatura_finale = ""
        for parte in parti_colpite:
            corazzato = input(Fore.LIGHTGREEN_EX + f"Parte {parte} Corazzata? (S/N): ").upper()
            if corazzato == 'S':
                armatura = input(Fore.LIGHTGREEN_EX + f"Modello Corazza per {parte}: ").strip().lower()
                armatura_finale = abbreviazioni_armature.get(armatura[:3], armatura)
                break  # Usa la prima armatura trovata
        
        abilita_arma = int(input(Fore.LIGHTGREEN_EX + "Abilità Nelle Armi (+1 a +10): "))
        precisione = int(input(Fore.LIGHTGREEN_EX + "Precisione (%): "))
        circ_precisione = int(input(Fore.LIGHTGREEN_EX + "Circostanza Precisione (%): "))
        danno_base = int(input(Fore.LIGHTGREEN_EX + "Danno Base Arma: "))
        munizione = input(Fore.LIGHTGREEN_EX + "Munizioni Avanzate: ").upper()
        distanza = int(input(Fore.LIGHTGREEN_EX + "Distanza Dal Bersaglio (m): "))

        if munizione not in munizioni_bonus:
            raise ValueError("Tipo di munizione non valido.")
        if abilita_arma < 1 or abilita_arma > 10:
            raise ValueError("Abilità fuori range.")
        if precisione < 10 or precisione > 100:
            raise ValueError("Precisione fuori range.")
        if colpi_sparati < 1:
            raise ValueError("Colpi sparati deve essere almeno 1.")
        if not set(parti_colpite).issubset(punti_vita.keys()):
            raise ValueError("Parti colpite non valide. Seleziona dalla lista: t, b, bd, bs, gd, gs.")
        
        # Se nessuna parte è corazzata, non passare alcuna armatura
        if not armatura_finale:
            armatura_finale = ""

        danno_finale, precisione_totale, colpi_a_segno, bonus_munizione, tipo_munizione, pv_armatura, danno_armatura = calcola_danno(
            abilita_arma, danno_base, precisione, colpi_sparati, distanza, munizione, circ_precisione, armatura_finale
        )
        colpo_associato = colpi.get(danno_base, ("Sconosciuto",))[0]

        # Aggiorna i punti vita in base al danno ricevuto
        aggiorna_punti_vita(punti_vita, danno_finale - danno_armatura, parti_colpite)

        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + f"\nDanno finale calcolato: {danno_finale}")
        print(Fore.LIGHTGREEN_EX + f"Precisione totale: {precisione_totale}%")
        print(Fore.LIGHTGREEN_EX + f"Munizione speciale: {tipo_munizione if munizione != 'N' else 'Nessuna'} (+{bonus_munizione} per colpo)")
        print(Fore.LIGHTGREEN_EX + f"PV Armatura rimanenti: {pv_armatura}")

        # Usa armatura_finale per la descrizione
        riepilogo = (
            Fore.LIGHTGREEN_EX +
            f"{nome} ({'Buono' if stato.lower() == 'b' else 'Cattivo'}) - "
            f"Abilità: {abilita_arma}, Danno Base: {danno_base} ({colpo_associato}), "
            f"Precisione: {precisione_totale}%, Colpi Sparati: {colpi_sparati} ({colpi_a_segno} a segno), "
            f"Munizione: {tipo_munizione if munizione != 'N' else 'Normale'}, "
            f"Distanza: {distanza}m -> Danno Finale: {danno_finale}"
        )
        riepilogo += f"\nBersaglio: {bersaglio}\nCorazza: {armatura_finale or 'Nessuna'}\n" + formattazione_punti_vita(punti_vita) + f"\nPV Armatura rimanenti: {pv_armatura}"
        print(Fore.LIGHTGREEN_EX + "\n" + riepilogo)
        cronologia.append(riepilogo)

    except ValueError as e:
        print(Fore.RED + f"Errore: {e}")
        inserisci_dati()

def mostra_cronologia():
    """
    Mostra la cronologia dei calcoli effettuati.
    """
    print(Fore.LIGHTGREEN_EX + "\n=== CRONOLOGIA ===")
    if cronologia:
        for i, voce in enumerate(cronologia, 1):
            print(Fore.LIGHTGREEN_EX + f"{i}. {voce}")
    else:
        print(Fore.YELLOW + "Nessun calcolo effettuato.")

def esegui_programma():
    """
    Esegue il programma principale.
    """
    while True:
        inserisci_dati()
        mostra_cronologia()
        if input(Fore.LIGHTGREEN_EX + "\nVuoi fare un altro calcolo? (s/n): ").lower() != 's':
            break

try:
    esegui_programma()
except Exception as e:
    print(Fore.RED + f"Errore sconosciuto: {e}")
input(Fore.LIGHTGREEN_EX + "\nPremi invio per uscire...")