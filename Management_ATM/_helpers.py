import logging
import os

def configure_logging(log_file='atm.log'):
    """Mengatur konfigurasi logging."""
    try:
        # Pastikan direktori untuk file log ada
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Konfigurasi logging
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("Logging telah dikonfigurasi.")
    except Exception as e:
        print(f"Gagal mengatur logging: {e}")