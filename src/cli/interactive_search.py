from food_search.similarity_manager import FoodSimilarityManager
from display import display_results, suggest_related


def show_help():
    print("\n📖 HELP MENU")
    print("-" * 30)
    print("Search Examples:")
    print("  • 'chocolate dessert' - Find chocolate desserts")
    print("  • 'Italian food'      - Find Italian cuisine")
    print("  • 'low calorie'       - Find lighter options")
    print("\nCommands:")
    print("  • 'help' - Show this menu")
    print("  • 'quit' - Exit")


def handle_search(manager: FoodSimilarityManager, query: str):
    print(f"\n🔍 Searching for '{query}'...")
    results = manager.search(query)
    display_results(results, f"Results for '{query}'")
    if results:
        suggest_related(results)


def run_chatbot(manager: FoodSimilarityManager):
    print("\n" + "=" * 50)
    print("🤖 INTERACTIVE FOOD SEARCH CHATBOT")
    print("=" * 50)
    print("Type a food name or description to search.")
    print("Commands: 'help', 'quit'  |  Ctrl+C to exit")
    print("-" * 50)

    while True:
        try:
            user_input = input("\n🔍 Search: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "q"):
                print("\n👋 Goodbye!")
                break
            elif user_input.lower() in ("help", "h"):
                show_help()
            else:
                handle_search(manager, user_input)
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    print("🍽️  Interactive Food Recommendation System")
    print("=" * 50)
    print("Loading food database...")

    manager = FoodSimilarityManager()
    count = manager.load_and_populate()
    print(f"✅ Loaded {count} food items successfully")

    run_chatbot(manager)


if __name__ == "__main__":
    main()