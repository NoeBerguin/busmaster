import csv
import re

# Fonctions nécessaires
def convert_timestamp(timestamp):
    # Convertit le timestamp en un format sans les deux-points
    return timestamp.replace(':', '')

# Fonction pour vérifier si une ligne correspond au format de ligne CAN attendu
def is_can_line(line):
    return bool(re.match(r'\d{2}:\d{2}:\d{2}:\d{4}\s+Rx\s+\d\s+0x[\dA-Fa-f]+', line))


def calculate_offset(messages):
    # Trouve le premier timestamp pour l'utiliser comme offset
    if messages:
        return int(messages[0][0])
    return 0

def adjust_timestamps(messages, offset):
    # Ajuste chaque timestamp en soustrayant l'offset
    for i in range(len(messages)):
        timestamp, message_id_hex, data_format, data_length, data_hex = messages[i]
        adjusted_timestamp = int(timestamp) - offset
        messages[i] = (str(adjusted_timestamp), message_id_hex, data_format, data_length, data_hex)

# Lecture et écriture du fichier CSV initial
chemin_log = "./LOG/JJE_LOG_M1.log"
chemin_csv_sortie = "./output.csv"

messages_can = []
with open(chemin_log, 'r') as log_file:
    for line in log_file:
        if is_can_line(line):
            parts = re.split(r'\s+', line.strip())
            if len(parts) < 9:
                continue
            timestamp = convert_timestamp(parts[0])
            message_id_hex = parts[3]
            data_format = parts[4]
            data_length = int(parts[5])
            hex_data_matches = re.findall(r'([0-9A-Fa-f]{2})', ' '.join(parts[6:6+data_length]))
            if hex_data_matches:
                hex_data_str = ' '.join(hex_data_matches)
                messages_can.append((timestamp, message_id_hex, data_format, data_length, hex_data_str))

# Trier les messages CAN par timestamp pour s'assurer que l'offset est basé sur le premier message
messages_can.sort(key=lambda x: x[0])

# Calculer l'offset basé sur le premier message
offset = calculate_offset(messages_can)

# Ajuster les timestamps des messages
adjust_timestamps(messages_can, offset)

with open(chemin_csv_sortie, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Timestamp', 'Message ID', 'Format', 'Length', 'Data (Hex)'])
    for message in messages_can:
        timestamp, message_id, data_format, data_length, data_hex = message
        csvwriter.writerow([timestamp, message_id, data_format, data_length, data_hex])
