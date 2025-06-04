from _user_auth import UserManagement
from _transaction_ops import TransactionManagement
from _helpers import configure_logging

def main():
    configure_logging('atm.log')
    atm = UserManagement()

    if not atm.authenticate_user():
        return

    while True:
        print("\nMenu:")
        print("1. Cek Saldo")
        print("2. Tarik Tunai")
        print("3. Setor Tunai")
        print("4. Transfer")
        print("5. Ubah PIN")
        print("6. Riwayat Transaksi")
        print("7. Keluar")
        choice = input("Pilih menu: ").strip()

        if choice == '1':
            atm.check_balance()
        elif choice == '2':
            amount = int(input("Masukkan jumlah: "))
            atm.withdraw(amount)
        elif choice == '3':
            amount = int(input("Masukkan jumlah: "))
            atm.deposit(amount)
        elif choice == '4':
            atm.transfer()
        elif choice == '5':
            atm.change_pin()
        elif choice == '6':
            atm.view_transactions()
        elif choice == '7':
            atm.logout()
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()