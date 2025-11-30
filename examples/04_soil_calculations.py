"""Soil-Specific Guideline Calculations.

Calculate guidelines for parameters in soil media.
"""

import os

from guidelinely import calculate_batch, calculate_guidelines


def main():
    """Calculate soil guidelines."""

    # Ensure API key is set
    api_key = os.getenv("GUIDELINELY_API_KEY")
    if not api_key:
        print("Error: GUIDELINELY_API_KEY environment variable not set")
        print("Set it with: export GUIDELINELY_API_KEY='your_api_key_here'")
        return

    print("=== Soil Guideline Calculations ===")
    print()

    # Example 1: Single parameter in soil
    print("--- Lead in Soil (Agricultural) ---")
    result = calculate_guidelines(
        parameter="Lead",
        media="soil",
        context={
            "pH": "6.5 1",  # Slightly acidic
            "organic_matter": "3.5 %",  # Moderate organic content
            "cation_exchange_capacity": "15 meq/100g",  # Moderate CEC
        },
    )

    print(f"Total guidelines: {result.total_count}")
    print(f"Context: {result.context}")
    print()

    for g in result.results[:5]:  # Show first 5
        print(f"  {g.value} | {g.receptor} | {g.source}")

    # Example 2: Batch soil calculations
    print("\n--- Multiple Metals in Industrial Soil ---")
    result2 = calculate_batch(
        parameters=["Arsenic", "Cadmium", "Chromium", "Copper", "Lead", "Zinc"],
        media="soil",
        context={
            "pH": "7.2 1",  # Neutral to slightly alkaline
            "organic_matter": "2.0 %",  # Lower organic content (industrial)
            "cation_exchange_capacity": "10 meq/100g",
        },
    )

    print(f"Total guidelines: {result2.total_count}")
    print()

    # Group by receptor type
    by_receptor = {}
    for guideline in result2.results:
        receptor = guideline.receptor
        if receptor not in by_receptor:
            by_receptor[receptor] = []
        by_receptor[receptor].append(guideline)

    print("Grouped by Receptor:")
    for receptor, guidelines in sorted(by_receptor.items()):
        print(f"\n{receptor} ({len(guidelines)} guidelines):")
        # Show unique parameters
        params = sorted(set(g.parameter for g in guidelines))
        print(f"  Parameters: {', '.join(params)}")

    # Example 3: Residential vs Industrial comparison
    print("\n\n=== Residential vs Industrial Soil (Arsenic) ===")
    print()

    contexts = {
        "Residential": {
            "pH": "6.5 1",
            "organic_matter": "4.0 %",
            "cation_exchange_capacity": "18 meq/100g",
        },
        "Industrial": {
            "pH": "7.0 1",
            "organic_matter": "1.5 %",
            "cation_exchange_capacity": "8 meq/100g",
        },
    }

    for land_use, context in contexts.items():
        result = calculate_guidelines(parameter="Arsenic", media="soil", context=context)
        print(f"{land_use}: {result.total_count} guidelines")
        if result.total_count > 0:
            print(f"  First guideline: {result.results[0].value}")


if __name__ == "__main__":
    main()
