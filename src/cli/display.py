from typing import Dict, List


def display_results(results: List[Dict], title: str = "Search Results", show_details: bool = True) -> None:
    print(f"\n📋 {title}")
    print("=" * 50)
    if not results:
        print("❌ No results found. Try adjusting your search terms or filters.")
        return
    for i, r in enumerate(results, 1):
        score = r["similarity_score"] * 100
        if show_details:
            print(f"\n{i}. 🍽️  {r['food_name']}")
            print(f"   📊 Match Score: {score:.1f}%")
            print(f"   🏷️  Cuisine: {r['cuisine_type']}")
            print(f"   🔥 Calories: {r['calories']}")
            print(f"   📝 {r['food_description']}")
        else:
            print(f"   {i}. {r['food_name']} ({score:.1f}%)")
    print("=" * 50)


def suggest_related(results: List[Dict]) -> None:
    if not results:
        return
    cuisines = list({r["cuisine_type"] for r in results})[:3]
    print("\n💡 Related searches:")
    for cuisine in cuisines:
        print(f"   • '{cuisine} dishes'")
    avg_calories = sum(r["calories"] for r in results) / len(results)
    if avg_calories > 350:
        print("   • Try 'low calorie' for lighter options")
    else:
        print("   • Try 'hearty meal' for more substantial dishes")