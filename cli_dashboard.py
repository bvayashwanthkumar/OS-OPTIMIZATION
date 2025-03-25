import os

def show_menu():
    while True:
        print("\nOS Optimization Tool")
        print("1. Show System Stats")
        print("2. Optimize Processes")
        print("3. Clean Memory")
        print("4. Clean Disk")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            os.system("monitor.py")
        elif choice == "2":
            os.system("scheduler.py")
        elif choice == "3":
            os.system("memory_optimizer.py")
        elif choice == "4":
            os.system("disk_cleanup.py")
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")

show_menu()
