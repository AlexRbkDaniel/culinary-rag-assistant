import json
import pathlib
from typing import Dict, List, Optional

import chromadb
from chromadb.utils import embedding_functions

DATA_PATH = pathlib.Path(__file__).parent.parent.parent / "resources" / "data" / "FoodDataSet.json"
DB_PATH = pathlib.Path(__file__).parent.parent.parent / ".chroma"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COLLECTION_METADATA = {"hnsw:space": "cosine"}


class FoodSimilarityManager:
    def __init__(self, collection_name: str = "food_collection"):
        self.client = chromadb.PersistentClient(path=str(DB_PATH))
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=ef,
            metadata=COLLECTION_METADATA,
        )

    def load_and_populate(self, file_path: pathlib.Path = DATA_PATH) -> int:
        if self.collection.count() > 0:
            count = self.collection.count()
            print(f"Using cached collection ({count} items).")
            return count

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error loading data: {e}")
            return 0

        self._normalize(data)
        self._populate(data)
        print(f"Loaded {len(data)} food items.")
        return len(data)

    def get_cuisines(self) -> List[str]:
        results = self.collection.get(include=["metadatas"])
        return sorted({m["cuisine_type"] for m in results["metadatas"] if m.get("cuisine_type")})

    @staticmethod
    def _normalize(data: List[Dict]) -> None:
        for i, item in enumerate(data):
            item["food_id"] = str(item.get("food_id", i + 1))
            item.setdefault("food_ingredients", [])
            item.setdefault("food_description", "")
            item.setdefault("cuisine_type", "Unknown")
            item.setdefault("food_calories_per_serving", 0)

            features = item.get("food_features")
            item["taste_profile"] = (
                ", ".join(str(v) for v in features.values() if v)
                if isinstance(features, dict)
                else ""
            )

    def _populate(self, items: List[Dict]) -> None:
        documents, metadatas, ids = [], [], []
        used_ids: set = set()

        for i, food in enumerate(items):
            parts = [
                f"Name: {food['food_name']}",
                f"Description: {food.get('food_description', '')}",
                f"Ingredients: {', '.join(food.get('food_ingredients', []))}",
                f"Cuisine: {food.get('cuisine_type', 'Unknown')}",
                f"Cooking method: {food.get('cooking_method', '')}",
            ]
            if food.get("taste_profile"):
                parts.append(f"Taste: {food['taste_profile']}")
            if food.get("food_health_benefits"):
                parts.append(f"Health benefits: {food['food_health_benefits']}")
            nutrition = food.get("food_nutritional_factors")
            if isinstance(nutrition, dict):
                parts.append(f"Nutrition: {', '.join(f'{k}: {v}' for k, v in nutrition.items())}")

            base_id = str(food.get("food_id", i))
            uid, counter = base_id, 1
            while uid in used_ids:
                uid = f"{base_id}_{counter}"
                counter += 1
            used_ids.add(uid)

            documents.append(". ".join(parts))
            ids.append(uid)
            metadatas.append({
                "name": food["food_name"],
                "cuisine_type": food.get("cuisine_type", "Unknown"),
                "ingredients": ", ".join(food.get("food_ingredients", [])),
                "calories": food.get("food_calories_per_serving", 0),
                "description": food.get("food_description", ""),
                "cooking_method": food.get("cooking_method", ""),
                "health_benefits": food.get("food_health_benefits", ""),
                "taste_profile": food.get("taste_profile", ""),
            })

        self.collection.add(documents=documents, metadatas=metadatas, ids=ids)

    def search(
            self,
            query: str,
            n_results: int = 5,
            cuisine_filter: Optional[str] = None,
            max_calories: Optional[int] = None,
    ) -> List[Dict]:
        where = self._build_where(cuisine_filter, max_calories)
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where,
            )
        except Exception as e:
            print(f"Search error: {e}")
            return []

        if not results["ids"][0]:
            return []

        return [
            {
                "food_id": results["ids"][0][i],
                "food_name": results["metadatas"][0][i]["name"],
                "food_description": results["metadatas"][0][i]["description"],
                "cuisine_type": results["metadatas"][0][i]["cuisine_type"],
                "calories": results["metadatas"][0][i]["calories"],
                "similarity_score": round(1 - results["distances"][0][i], 4),
            }
            for i in range(len(results["ids"][0]))
        ]

    @staticmethod
    def _build_where(
            cuisine_filter: Optional[str], max_calories: Optional[int]
    ) -> Optional[Dict]:
        filters = []
        if cuisine_filter:
            filters.append({"cuisine_type": cuisine_filter})
        if max_calories:
            filters.append({"calories": {"$lte": max_calories}})
        if len(filters) == 1:
            return filters[0]
        if len(filters) > 1:
            return {"$and": filters}
        return None