import json
import re
from typing import List, Optional

from openai import OpenAI

from app.models import Product
from app.logger import logger
from app.config import settings
from app.filter import ProductFilter
from app.retriever import Retriever


class RecommendationPipeline:

    def __init__(self, products: List[Product]):

        self.products = products

        self.retriever = Retriever()

        # GROQ CLIENT
        self.client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

        print("\nUSING MODEL:", settings.MODEL_NAME)

    # =========================================
    # MAIN PIPELINE
    # =========================================
    def run(
        self,
        query: str,
        age: int,
        budget: int,
        category: Optional[str] = None
    ):

        logger.info(
            f"Pipeline started | "
            f"query={query} | "
            f"age={age} | "
            f"budget={budget} | "
            f"category={category}"
        )

        # =====================================
        # STEP 1 — FILTERING
        # =====================================
        filter_engine = ProductFilter(self.products)

        filtered_products = filter_engine.filter(
            age=age,
            budget=budget,
            category=category
        )

        print("\n========== FILTERED PRODUCTS ==========\n")

        for p in filtered_products[:10]:
            print(
                p.name,
                "|",
                p.category,
                "|",
                p.age_range
            )

        print("\n=======================================\n")

        if not filtered_products:
            return {
                "message": "No matching products found"
            }

        # =====================================
        # STEP 2 — RETRIEVAL
        # =====================================
        retrieved_products = self.retriever.retrieve(
            query=query,
            products=filtered_products,
            top_k=settings.TOP_K
        )

        print("\n========== RETRIEVED PRODUCTS ==========\n")

        for i, p in enumerate(retrieved_products, start=1):
            print(
                f"{i}. {p.name} | {p.category}"
            )

        print("\n========================================\n")

        if not retrieved_products:
            return {
                "message": "No matching products found"
            }

        # =====================================
        # STEP 3 — GENERATION
        # =====================================
        result = self._generate_with_retry(
            query=query,
            products=retrieved_products
        )

        return result

    # =========================================
    # RETRY WRAPPER
    # =========================================
    def _generate_with_retry(
        self,
        query: str,
        products: List[Product],
        retries: int = 2
    ):

        for attempt in range(retries + 1):

            try:

                raw_output = self._call_llm(
                    query=query,
                    products=products
                )

                print("\n======= RAW OUTPUT =======\n")
                print(raw_output)
                print("\n==========================\n")

                parsed_output = self._safe_json_parse(
                    raw_output
                )

                if self._validate_output(
                    parsed_output,
                    products
                ):

                    logger.info(
                        f"LLM success on attempt {attempt + 1}"
                    )

                    return parsed_output

                logger.warning(
                    "Validation failed"
                )

            except Exception as e:

                print("\nLLM ERROR:", str(e), "\n")

                logger.error(
                    f"LLM generation failed: {str(e)}"
                )

        return {
            "error": "Failed to generate recommendation"
        }

    # =========================================
    # GROQ CALL
    # =========================================
    def _call_llm(
        self,
        query: str,
        products: List[Product]
    ) -> str:

        print("\n========== PRODUCTS SENT TO LLM ==========\n")

        for i, p in enumerate(products, start=1):
            print(
                f"{i}. {p.name} | {p.category}"
            )

        print("\n==========================================\n")

        # =====================================
        # CONTEXT
        # =====================================
        product_context = []

        for rank, p in enumerate(products, start=1):

            product_context.append({
                "retrieval_rank": rank,
                "name": p.name,
                "category": p.category,
                "price": p.price,
                "description": p.description,
                "reviews": p.reviews,
                "safety_info": p.safety_info,
            })

        # =====================================
        # PROMPT
        # =====================================
        prompt = f"""
You are a STRICT AI shopping recommendation system.

IMPORTANT RULES:

1. ONLY recommend from provided products
2. NEVER invent products
3. Prioritize LOWER retrieval_rank
4. retrieval_rank=1 is MOST relevant
5. Use semantic relevance to user query
6. DO NOT recommend unrelated categories
7. RETURN ONLY VALID JSON
8. NO markdown
9. NO explanations
10. NO text outside JSON

USER QUERY:
{query}

RETRIEVED PRODUCTS:
{json.dumps(product_context, indent=2)}

RETURN STRICT JSON ONLY:

{{
  "primary_recommendation": {{
    "name": "",
    "price": 0,
    "reason": ""
  }},
  "alternatives": [
    {{
      "name": "",
      "price": 0,
      "reason": ""
    }}
  ],
  "confidence": 0.0
}}
"""

        print("\nCALLING GROQ API...\n")

        response = self.client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict JSON generator."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content

        print("\n========== RAW LLM OUTPUT ==========\n")
        print(content)
        print("\n===================================\n")

        return content

    # =========================================
    # SAFE JSON PARSER
    # =========================================
    def _safe_json_parse(
        self,
        text: str
    ):

        matches = re.findall(
            r"\{[\s\S]*\}",
            text
        )

        if not matches:
            raise ValueError(
                "No JSON found"
            )

        json_candidate = max(
            matches,
            key=len
        )

        # remove trailing commas
        json_candidate = re.sub(
            r",\s*}",
            "}",
            json_candidate
        )

        json_candidate = re.sub(
            r",\s*]",
            "]",
            json_candidate
        )

        return json.loads(json_candidate)

    # =========================================
    # VALIDATION
    # =========================================
    def _validate_output(
        self,
        output: dict,
        products: List[Product]
    ) -> bool:

        if "primary_recommendation" not in output:
            return False

        allowed_products = {
            p.name.lower(): p
            for p in products
        }

        # =====================================
        # PRIMARY
        # =====================================
        primary = output["primary_recommendation"]

        primary_name = primary["name"].lower()

        matched_primary = None

        for allowed_name in allowed_products:

            if (
                allowed_name in primary_name
                or primary_name in allowed_name
            ):
                matched_primary = allowed_products[
                    allowed_name
                ]
                break

        if not matched_primary:
            return False

        primary["name"] = matched_primary.name
        primary["price"] = matched_primary.price

        if not primary.get("reason"):
            primary["reason"] = (
                "Relevant based on semantic search"
            )

        # =====================================
        # ALTERNATIVES
        # =====================================
        validated_alts = []

        for alt in output.get(
            "alternatives",
            []
        ):

            alt_name = alt["name"].lower()

            matched_alt = None

            for allowed_name in allowed_products:

                if (
                    allowed_name in alt_name
                    or alt_name in allowed_name
                ):
                    matched_alt = allowed_products[
                        allowed_name
                    ]
                    break

            if matched_alt:

                alt["name"] = matched_alt.name
                alt["price"] = matched_alt.price

                if not alt.get("reason"):
                    alt["reason"] = (
                        "Alternative relevant option"
                    )

                validated_alts.append(alt)

        output["alternatives"] = validated_alts

        return True