import os
import shutil
import hashlib
import time
import argparse
import logging

class FolderSync:
    def __init__(self, source, replica, interval, logfile):
        self.source = source
        self.replica = replica
        self.interval = interval
        self.logfile = logfile

        logging.basicConfig(filename=logfile, level=logging.INFO, format='%(asctime)s - %(message)s')
        logging.getLogger().addHandler(logging.StreamHandler())

    def calculate_md5(self, file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def sync_folders(self, source, replica):
        source_items = set(os.listdir(source))
        replica_items = set(os.listdir(replica))

        # Items to remove from replica
        items_to_remove = replica_items - source_items
        for item in items_to_remove:
            item_path = os.path.join(replica, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                logging.info(f"Removed directory {item_path}")
            else:
                os.remove(item_path)
                logging.info(f"Removed file {item_path}")

        # Items to copy or update in replica
        for item in source_items:
            source_item_path = os.path.join(source, item)
            replica_item_path = os.path.join(replica, item)

            if os.path.isdir(source_item_path):
                if not os.path.exists(replica_item_path):
                    shutil.copytree(source_item_path, replica_item_path)
                    logging.info(f"Copied directory {source_item_path} to {replica_item_path}")
                else:
                    self.sync_folders(source_item_path, replica_item_path)
            else:
                if not os.path.exists(replica_item_path) or self.calculate_md5(source_item_path) != self.calculate_md5(replica_item_path):
                    shutil.copy2(source_item_path, replica_item_path)
                    logging.info(f"Copied file {source_item_path} to {replica_item_path}")

    def start_sync(self):
        while True:
            logging.info("Starting synchronization")
            self.sync_folders(self.source, self.replica)
            logging.info("Synchronization complete")
            time.sleep(self.interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Synchronize two folders.',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('source', type=str, help='Path to the source folder')
    parser.add_argument('replica', type=str, help='Path to the replica folder')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')
    parser.add_argument('logfile', type=str, help='Path to the log file')
    parser.add_argument('-v', '--version', action='version', version='FolderSync 1.0')
    args = parser.parse_args()

    # Print the initial values
    print(f"Source folder: {args.source}")
    print(f"Replica folder: {args.replica}")
    print(f"Synchronization interval (seconds): {args.interval}")
    print(f"Log file path: {args.logfile}")

    folder_sync = FolderSync(args.source, args.replica, args.interval, args.logfile)
    folder_sync.start_sync()
