import cantools
import pandas as pd

def dbc_to_csv(dbc_path, output_path, csv_output_path):
    db = cantools.database.load_file(dbc_path)
    all_signals = ['timestamp'] + [signal.name for message in db.messages for signal in message.signals]
    data_dict = {signal: [] for signal in all_signals}
    last_known_values = {signal: None for signal in all_signals}  # Dictionnaire pour stocker la dernière valeur connue

    with open(output_path, 'r') as output_file:
        next(output_file)  # Ignorer l'en-tête
        for line in output_file:
            parts = line.strip().split(',')
            if len(parts) != 5:
                continue
            timestamp, message_id_hex, format_type, _, data_hex = parts
            if not message_id_hex.startswith('0x'):
                continue
            message_id = int(message_id_hex, 16)
            data_bytes = bytes.fromhex(data_hex)
            
            try:
                decoded_signals = db.decode_message(message_id, data_bytes)
                last_known_values['timestamp'] = timestamp  # Mettre à jour le timestamp actuel
                for signal in all_signals[1:]:  # Ignorer 'timestamp'
                    if signal in decoded_signals:
                        last_known_values[signal] = decoded_signals[signal]
                    # Pas besoin de else; last_known_values[signal] garde déjà la dernière valeur connue

                # Ajouter les valeurs (actuelles ou dernières connues) dans data_dict
                for signal in all_signals:
                    data_dict[signal].append(last_known_values[signal])
            except (KeyError, ValueError) as e:
                continue  # Ignorer les messages non trouvés ou erreurs de décodage

    df = pd.DataFrame(data_dict)
    df.to_csv(csv_output_path, index=False)
    print(f"Fichier CSV généré : {csv_output_path}")

dbc_path = './DBC/CATL_Protocol_A-CAN_V3.4_210705.dbc'
output_path = './output.csv'
csv_output_path = './CATL/BUSMASTERLogFile_2024-04-10_CATL_Discharge_complete.csv'
dbc_to_csv(dbc_path, output_path, csv_output_path)
