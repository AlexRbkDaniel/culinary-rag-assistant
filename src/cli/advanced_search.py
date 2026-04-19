from food_search.similarity_manager import FoodSimilarityManager
from display import display_results

DEMONSTRATIONS = [
    {"title": "Italian Cuisine Search",      "query": "creamy pasta",    "cuisine_filter": "Italian",  "max_calories": None},
    {"title": "Low-Calorie Healthy Options", "query": "healthy meal",    "cuisine_filter": None,       "max_calories": 300},
    {"title": "Asian Light Dishes",          "query": "light fresh meal","cuisine_filter": "Japanese", "max_calories": 250},
]


def show_help():
    print("\n📖 ADVANCED SEARCH HELP")
    print("=" * 40)
    print("  1. Basic Search       - Standard similarity search")
    print("  2. Cuisine Filter     - Search within a specific cuisine")
    print("  3. Calorie Filter     - Search under a calorie limit")
    print("  4. Combined Filters   - Cuisine + calorie filter together")
    print("  5. Demonstrations     - Predefined search examples")
    print("\nTips:")
    print("  • Use descriptive terms: 'creamy', 'spicy', 'light'")
    print("  • Combine ingredients: 'chicken vegetables'")
    print("  • Filter by calories for dietary goals")


def perform_basic_search(manager: FoodSimilarityManager):
    print("\n🔍 BASIC SIMILARITY SEARCH")
    print("-" * 30)
    query = input("Enter search query: ").strip()
    if not query:
        print("❌ Please enter a search term.")
        return
    display_results(manager.search(query), "Basic Search Results")


def perform_cuisine_search(manager: FoodSimilarityManager):
    print("\n🍽️  CUISINE-FILTERED SEARCH")
    print("-" * 30)
    cuisines = manager.get_cuisines()
    for i, c in enumerate(cuisines, 1):
        print(f"  {i}. {c}")

    query = input("\nEnter search query: ").strip()
    if not query:
        print("❌ Please enter a search term.")
        return

    raw = input("Enter cuisine number or name: ").strip()
    if raw.isdigit() and 1 <= int(raw) <= len(cuisines):
        cuisine = cuisines[int(raw) - 1]
    elif raw:
        cuisine = raw
    else:
        print("❌ Invalid cuisine selection.")
        return

    display_results(manager.search(query, cuisine_filter=cuisine), f"Cuisine-Filtered Results ({cuisine})")


def perform_calorie_search(manager: FoodSimilarityManager):
    print("\n🔥 CALORIE-FILTERED SEARCH")
    print("-" * 30)
    query = input("Enter search query: ").strip()
    if not query:
        print("❌ Please enter a search term.")
        return

    raw = input("Enter maximum calories (or Enter to skip): ").strip()
    max_calories = int(raw) if raw.isdigit() else None

    label = f"under {max_calories} cal" if max_calories else "any calories"
    display_results(manager.search(query, max_calories=max_calories), f"Calorie-Filtered Results ({label})")


def perform_combined_search(manager: FoodSimilarityManager):
    print("\n🎯 COMBINED FILTERS SEARCH")
    print("-" * 30)
    query = input("Enter search query: ").strip()
    if not query:
        print("❌ Please enter a search term.")
        return

    cuisine = input("Cuisine type (or Enter to skip): ").strip() or None
    raw = input("Maximum calories (or Enter to skip): ").strip()
    max_calories = int(raw) if raw.isdigit() else None

    parts = []
    if cuisine:
        parts.append(f"cuisine: {cuisine}")
    if max_calories:
        parts.append(f"max cal: {max_calories}")
    label = ", ".join(parts) if parts else "no filters"

    display_results(
        manager.search(query, cuisine_filter=cuisine, max_calories=max_calories),
        f"Combined Results ({label})",
    )


def run_demonstrations(manager: FoodSimilarityManager):
    print("\n📊 SEARCH DEMONSTRATIONS")
    print("=" * 40)
    for i, demo in enumerate(DEMONSTRATIONS, 1):
        print(f"\n{i}. {demo['title']}")
        print(f"   Query: '{demo['query']}'")
        parts = []
        if demo["cuisine_filter"]:
            parts.append(f"Cuisine: {demo['cuisine_filter']}")
        if demo["max_calories"]:
            parts.append(f"Max Cal: {demo['max_calories']}")
        if parts:
            print(f"   Filters: {', '.join(parts)}")

        display_results(
            manager.search(demo["query"], cuisine_filter=demo["cuisine_filter"],
                           max_calories=demo["max_calories"], n_results=3),
            demo["title"],
            show_details=False,
        )
        input("\n⏸️  Press Enter to continue...")


def run_advanced_search(manager: FoodSimilarityManager):
    print("\n" + "=" * 50)
    print("🔧 ADVANCED SEARCH WITH FILTERS")
    print("=" * 50)
    print("  1. Basic similarity search")
    print("  2. Cuisine-filtered search")
    print("  3. Calorie-filtered search")
    print("  4. Combined filters search")
    print("  5. Demonstration mode")
    print("  6. Help")
    print("  7. Exit")
    print("-" * 50)

    actions = {
        "1": perform_basic_search,
        "2": perform_cuisine_search,
        "3": perform_calorie_search,
        "4": perform_combined_search,
        "5": run_demonstrations,
        "6": lambda _: show_help(),
    }

    while True:
        try:
            choice = input("\n📋 Select option (1-7): ").strip()
            if choice == "7":
                print("👋 Goodbye!")
                break
            action = actions.get(choice)
            if action:
                action(manager)
            else:
                print("❌ Invalid option. Please select 1-7.")
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    print("🔬 Advanced Food Search System")
    print("=" * 50)
    print("Loading food database...")

    manager = FoodSimilarityManager(collection_name="advanced_food_search")
    count = manager.load_and_populate()
    print(f"✅ Loaded {count} food items successfully")

    run_advanced_search(manager)


if __name__ == "__main__":
    main()