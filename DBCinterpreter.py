import cantools
import pandas as pd

def dbc_to_csv(dbc_path, output_path):
    db = cantools.database.load_file(dbc_path)
    # Liste de tous les signaux plus le timestamp
    all_signals = ['timestamp'] + [signal.name for message in db.messages for signal in message.signals]
    # Initialiser une ligne vide avec tous les signaux mis à 0
    current_row = {signal: 0 for signal in all_signals}
    rows = []

    with open(output_path, 'r') as output_file:
        next(output_file)  # Ignorer l'en-tête
        last_timestamp = None
        for line in output_file:
            parts = line.strip().split(',')
            if len(parts) < 5:
                continue
            timestamp, message_id_hex, format_type, _, data_hex = parts
            if not message_id_hex.startswith('0x'):
                continue
            message_id = int(message_id_hex, 16)
            data_bytes = bytes(int(byte, 16) for byte in data_hex.split())

            try:
                decoded_signals = db.decode_message(message_id, data_bytes)
                if timestamp != last_timestamp:
                    if last_timestamp is not None:
                        # Si ce n'est pas la première ligne, ajouter la ligne courante aux lignes complètes
                        rows.append(current_row.copy())
                    # Mettre à jour le timestamp de la ligne courante pour le nouveau message
                    current_row['timestamp'] = timestamp
                    last_timestamp = timestamp
                # Mettre à jour la ligne courante avec les nouveaux signaux décodés
                for signal in decoded_signals:
                    current_row[signal] = decoded_signals[signal]
            except KeyError:
                continue  # Ignorer les messages non trouvés

        # Ne pas oublier d'ajouter la dernière ligne après la fin de la boucle
        rows.append(current_row.copy())

    # Créer le DataFrame à partir des lignes accumulées
    df = pd.DataFrame(rows, columns=all_signals)
    
    csv_path = dbc_path.replace('.dbc', '_filled.csv')
    df.to_csv(csv_path, index=False)
    print(f"Fichier CSV généré : {csv_path}")

dbc_path = './DBC/JJE_CAN_V251.dbc'
output_path = './output.csv'
dbc_to_csv(dbc_path, output_path)
