import cantools
import pandas as pd

def dbc_to_csv(dbc_path, output_path):
    db = cantools.database.load_file(dbc_path)
    signals = ['timestamp'] + [signal.name for message in db.messages for signal in message.signals]
    data_dict = {signal: [] for signal in signals}
    last_values = {signal: 0 for signal in signals}  # Initialiser les dernières valeurs à 0

    with open(output_path, 'r') as output_file:
        next(output_file)  # Ignorer l'en-tête
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
                row = {'timestamp': timestamp}
                for signal in signals[1:]:  # Ignorer 'timestamp'
                    if signal in decoded_signals:
                        row[signal] = decoded_signals[signal]
                        last_values[signal] = decoded_signals[signal]  # Mettre à jour la dernière valeur connue
                    else:
                        row[signal] = last_values[signal]  # Utiliser la dernière valeur connue
                for key, value in row.items():
                    data_dict[key].append(value)
            except KeyError:
                # print(f"Message ID {message_id_hex} non trouvé dans le DBC.")
                continue  # Ignorer les messages non trouvés

    # Pas besoin de compléter les colonnes ici car elles sont déjà remplies avec la dernière valeur connue ou zéro
    
    df = pd.DataFrame(data_dict)
    csv_path = dbc_path.replace('.dbc', '_filled.csv')
    df.to_csv(csv_path, index=False)
    print(f"Fichier CSV généré : {csv_path}")

dbc_path = './DBC/can_example.dbc'
output_path = './output.csv'
dbc_to_csv(dbc_path, output_path)