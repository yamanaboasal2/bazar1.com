import requests

BASE_URL = "http://localhost:5000"

def menu():
    print("\n===== Bazar.com =====")
    print("1. Search by topic")
    print("2. Get book info")
    print("3. Purchase book")
    print("4. Exit")

while True:
    menu()
    choice = input("Enter your choice: ")

    # 🔍 search
    if choice == "1":
        topic = input("Enter topic: ")
        try:
            res = requests.get(f"{BASE_URL}/search/{topic}")
            data = res.json()
            print("\nResults:")
            for book in data:
                print(f"ID: {book['id']} | Title: {book['title']}")
        except:
            print("Error in search")

    # 📘 info
    elif choice == "2":
        book_id = input("Enter book ID: ")
        try:
            res = requests.get(f"{BASE_URL}/info/{book_id}")
            print("\nBook Info:")
            print(res.json())
        except:
            print("Error in info")

    # 🛒 purchase
    elif choice == "3":
        book_id = input("Enter book ID: ")
        try:
            res = requests.get(f"{BASE_URL}/purchase/{book_id}")
            print("\nResult:")
            print(res.json())
        except:
            print("Error in purchase")

    # ❌ exit
    elif choice == "4":
        print("Goodbye 👋")
        break

    else:
        print("Invalid choice")