"""Batch Calculations for Multiple Parameters.

Calculate guidelines for multiple metals in surface water.
"""

import os

from guidelinely import calculate_batch


def main():
    """Batch calculate multiple metal parameters."""

    # Ensure API key is set
    api_key = os.getenv("GUIDELINELY_API_KEY")
    if not api_key:
        print("Error: GUIDELINELY_API_KEY environment variable not set")
        print("Set it with: export GUIDELINELY_API_KEY='your_api_key_here'")
        return

    print("=== Batch Calculate Multiple Metals ===")
    print()

    # Calculate multiple metals in surface water
    result = calculate_batch(
        parameters=["Aluminum", "Copper", "Lead", "Zinc", "Cadmium"],
        media="surface_water",
        context={
            "pH": "7.5 1",  # Slightly alkaline
            "hardness": "150 mg/L",  # Moderately hard water
            "temperature": "15 °C",  # Cool water
            "chloride": "75 mg/L",  # Moderate chloride
        },
    )

    print(f"Total guidelines found: {result.total_count}")
    print(f"Context: {result.context}")
    print()

    # Group by parameter
    by_parameter = {}
    for guideline in result.results:
        param = guideline.parameter
        if param not in by_parameter:
            by_parameter[param] = []
        by_parameter[param].append(guideline)

    # Display grouped results
    for param, guidelines in sorted(by_parameter.items()):
        print(f"\n{param}:")
        print("-" * 60)
        for g in guidelines:
            print(f"  {g.value} | {g.receptor} | {g.exposure_duration} | {g.source}")

    # Example with per-parameter unit conversion
    print("\n\n=== With Per-Parameter Unit Conversion ===")
    print()

    result2 = calculate_batch(
        parameters=[
            "Aluminum",
            {"name": "Copper", "target_unit": "μg/L"},
            {"name": "Lead", "target_unit": "mg/L"},
        ],
        media="surface_water",
        context={"pH": "7.0 1", "hardness": "100 mg/L"},
    )

    print(f"Total guidelines found: {result2.total_count}")

    # Filter to chronic aquatic life guidelines
    print("\n=== Chronic Aquatic Life Guidelines ===")
    chronic_aquatic = [
        g
        for g in result.results
        if g.receptor == "Aquatic Life" and g.exposure_duration == "chronic"
    ]

    for guideline in chronic_aquatic[:10]:  # Show first 10
        upper = guideline.upper if guideline.upper else "unbounded"
        print(f"{guideline.parameter}: ≤{upper} {guideline.unit}")


if __name__ == "__main__":
    main()
