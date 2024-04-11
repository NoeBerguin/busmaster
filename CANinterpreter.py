import csv
import re

def convert_timestamp(timestamp):
    # Découpe le timestamp en ses composantes
    hours, minutes, seconds, micro_part = map(int, timestamp.split(':'))
    # Convertit les heures, minutes et secondes en millisecondes
    # Convertit la partie micro (ici, dixièmes de millisecondes) en millisecondes en divisant par 10
    total_milliseconds = ((hours * 3600) + (minutes * 60) + seconds) * 1000 + micro_part / 10
    return int(total_milliseconds)

# Fonction pour vérifier si une ligne correspond au format de ligne CAN attendu
def is_can_line(line):
    return bool(re.match(r'\d{2}:\d{2}:\d{2}:\d{4}\s+Rx\s+\d\s+0x[\dA-Fa-f]+', line))

# Lecture et écriture du fichier CSV initial
chemin_log = "./LOG/CATL/BUSMASTERLogFile_2024-04-10_CATL_Discharge_complete.log"
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


with open(chemin_csv_sortie, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Timestamp', 'Message ID', 'Format', 'Length', 'Data (Hex)'])
    for message in messages_can:
        timestamp, message_id, data_format, data_length, data_hex = message
        csvwriter.writerow([timestamp, message_id, data_format, data_length, data_hex])
