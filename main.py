from converter import CurrencyConverter

if __name__ == "__main__":
    converter = CurrencyConverter()

    print("--- Welcome to Python Currency CLI ---")
    base = input("Enter your base currency? (e.g. EUR): ").upper()

    try:
        converter.fetch_rates(base)
    except Exception as e:
        print(f"Failed to start: {e}")
        exit()
    
    while True:
        print("\nOptions: [1] Convert [2] View History [3] Exit")
        choice = input("Select a number mann: ")

        if choice == "1":
            amount = int(input("How much you want to convert, maan? "))
            target_curr = input("To what you want to convert it, maan? ").upper()
            total = converter.convert(amount, base, target_curr)
            print(f"{total} is in {target_curr} from {base}")
        
        elif choice == "2":
            print(converter.get_history())
        
        elif choice == "3":
            print("Goodbye, Aikhan!")
            break


