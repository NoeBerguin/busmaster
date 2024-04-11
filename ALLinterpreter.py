import csv
import re
import cantools
import pandas as pd
import sys

class CANLogProcessor:
    def __init__(self, log_path, dbc_path, csv_final_output_path, progress_callback=None):
        self.log_path = log_path
        self.dbc_path = dbc_path
        self.csv_final_output_path = csv_final_output_path
        self.progress_callback = progress_callback  # Callback pour la mise à jour de la progression


    @staticmethod
    def convert_timestamp(timestamp):
        hours, minutes, seconds, micro_part = map(int, timestamp.split(':'))
        total_milliseconds = ((hours * 3600) + (minutes * 60) + seconds) * 1000 + micro_part / 10
        return int(total_milliseconds)

    @staticmethod
    def is_can_line(line):
        return bool(re.match(r'\d{2}:\d{2}:\d{2}:\d{4}\s+Rx\s+\d\s+0x[\dA-Fa-f]+', line))

    def log_to_messages(self):
        messages_can = []
        line_count = sum(1 for _ in open(self.log_path, 'r'))
        processed_lines = 0

        with open(self.log_path, 'r') as log_file:
            for line in log_file:
                processed_lines += 1
                if self.is_can_line(line):
                    parts = re.split(r'\s+', line.strip())
                    if len(parts) < 9:
                        continue
                    timestamp = self.convert_timestamp(parts[0])
                    message_id_hex = parts[3]
                    data_format = parts[4]
                    data_length = int(parts[5])
                    hex_data_matches = re.findall(r'([0-9A-Fa-f]{2})', ' '.join(parts[6:6+data_length]))
                    if hex_data_matches:
                        hex_data_str = ' '.join(hex_data_matches)
                        messages_can.append((timestamp, message_id_hex, data_format, data_length, hex_data_str))
                self.update_progress(processed_lines, line_count)
        return messages_can
    
    def update_progress(self, current, total):
        if self.progress_callback:
            percentage = 100 * (current / total)
            self.progress_callback(percentage)

    @staticmethod
    def print_progress(current, total):
        percentage = 100 * (current / total)
        sys.stdout.write(f'\rProcessing: {percentage:.2f}%')
        sys.stdout.flush()

    def messages_to_csv(self, messages_can):
        db = cantools.database.load_file(self.dbc_path)
        all_signals = ['timestamp'] + [signal.name for message in db.messages for signal in message.signals]
        data_dict = {signal: [] for signal in all_signals}
        last_known_values = {signal: None for signal in all_signals}

        for index, message in enumerate(messages_can):
            timestamp, message_id_hex, _, _, data_hex = message
            if not message_id_hex.startswith('0x'):
                continue
            message_id = int(message_id_hex, 16)
            data_bytes = bytes.fromhex(data_hex)
            try:
                decoded_signals = db.decode_message(message_id, data_bytes)
                last_known_values['timestamp'] = timestamp
                for signal in all_signals[1:]:
                    if signal in decoded_signals:
                        last_known_values[signal] = decoded_signals[signal]
                for signal in all_signals:
                    data_dict[signal].append(last_known_values[signal])
            except (KeyError, ValueError):
                continue
            self.print_progress(index + 1, len(messages_can))

        df = pd.DataFrame(data_dict)
        df.to_csv(self.csv_final_output_path, index=False)
        print(f'\nFichier CSV généré : {self.csv_final_output_path}')

def main():
    log_path = "./LOG/JJElogV74_P0_M5.log"
    dbc_path = './DBC/JJE_CAN_V251.dbc'
    csv_final_output_path = './JJElogV74_P0_M5_complete.csv'
    
    processor = CANLogProcessor(log_path, dbc_path, csv_final_output_path)
    messages_can = processor.log_to_messages()
    processor.messages_to_csv(messages_can)

if __name__ == "__main__":
    main()
