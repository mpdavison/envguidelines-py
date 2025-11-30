"""Advanced Filtering and Analysis Workflow.

Demonstrate filtering, grouping, and analysis of guideline results.
"""

import os
from collections import defaultdict

from guidelinely import calculate_batch


def main():
    """Advanced filtering and analysis workflow."""

    # Ensure API key is set
    api_key = os.getenv("GUIDELINELY_API_KEY")
    if not api_key:
        print("Error: GUIDELINELY_API_KEY environment variable not set")
        print("Set it with: export GUIDELINELY_API_KEY='your_api_key_here'")
        return

    print("=== Advanced Workflow: Comprehensive Water Quality Analysis ===")
    print()

    # Comprehensive batch calculation
    result = calculate_batch(
        parameters=[
            "Aluminum",
            "Ammonia",
            "Arsenic",
            "Cadmium",
            "Chloride",
            "Chromium",
            "Copper",
            "Iron",
            "Lead",
            "Mercury",
            "Nickel",
            "Selenium",
            "Silver",
            "Zinc",
        ],
        media="surface_water",
        context={
            "pH": "7.5 1",
            "hardness": "150 mg/L",
            "temperature": "15 °C",
            "chloride": "75 mg/L",
        },
    )

    print(f"Total guidelines retrieved: {result.total_count}")
    print(f"Context: {result.context}")
    print()

    # Analysis 1: Count by source
    print("=== Guidelines by Source ===")
    by_source = defaultdict(int)
    for g in result.results:
        by_source[g.source] += 1

    for source, count in sorted(by_source.items(), key=lambda x: x[1], reverse=True):
        print(f"  {source}: {count}")

    # Analysis 2: Calculated vs Static guidelines
    print("\n=== Calculated vs Static Guidelines ===")
    calculated = sum(1 for g in result.results if g.is_calculated)
    static = sum(1 for g in result.results if not g.is_calculated)
    print(f"  Calculated: {calculated}")
    print(f"  Static: {static}")
    print(f"  Percentage calculated: {calculated/result.total_count*100:.1f}%")

    # Analysis 3: Group by receptor and exposure
    print("\n=== By Receptor and Exposure Duration ===")
    by_receptor_exposure = defaultdict(lambda: defaultdict(int))
    for g in result.results:
        by_receptor_exposure[g.receptor][g.exposure_duration] += 1

    for receptor, exposures in sorted(by_receptor_exposure.items()):
        print(f"\n{receptor}:")
        for exposure, count in sorted(exposures.items()):
            print(f"  {exposure}: {count}")

    # Analysis 4: Most stringent guidelines (aquatic life, chronic)
    print("\n=== Most Stringent Chronic Aquatic Life Guidelines ===")
    chronic_aquatic = [
        g
        for g in result.results
        if g.receptor == "Aquatic Life" and g.exposure_duration == "chronic" and g.upper is not None
    ]

    # Group by parameter and find minimum upper bound
    most_stringent = {}
    for g in chronic_aquatic:
        param = g.parameter
        if param not in most_stringent or g.upper < most_stringent[param]["upper"]:
            most_stringent[param] = {
                "upper": g.upper,
                "unit": g.unit,
                "source": g.source,
                "value": g.value,
            }

    for param, info in sorted(most_stringent.items()):
        print(f"  {param}: ≤{info['upper']} {info['unit']} ({info['source']})")

    # Analysis 5: Parameters with widest range of guidelines
    print("\n=== Parameters with Most Guideline Diversity ===")
    param_counts = defaultdict(int)
    for g in result.results:
        param_counts[g.parameter] += 1

    top_params = sorted(param_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    for param, count in top_params:
        print(f"  {param}: {count} guidelines")

    # Analysis 6: Temperature-dependent calculations
    print("\n=== Temperature Sensitivity Analysis ===")
    print("Comparing Ammonia at different temperatures...")

    temps = ["5 °C", "15 °C", "25 °C"]
    ammonia_results = {}

    for temp in temps:
        temp_result = calculate_batch(
            parameters=["Ammonia"],
            media="surface_water",
            context={
                "pH": "7.5 1",
                "hardness": "150 mg/L",
                "temperature": temp,
                "chloride": "75 mg/L",
            },
        )
        ammonia_results[temp] = temp_result
        print(f"  {temp}: {temp_result.total_count} guidelines")


if __name__ == "__main__":
    main()
