"""Calculate Guidelines for a Single Parameter.

Calculate aluminum guidelines in surface water with specific conditions.
"""

import os

from guidelinely import calculate_guidelines


def main():
    """Calculate aluminum guidelines in surface water."""

    # Ensure API key is set
    api_key = os.getenv("GUIDELINELY_API_KEY")
    if not api_key:
        print("Error: GUIDELINELY_API_KEY environment variable not set")
        print("Set it with: export GUIDELINELY_API_KEY='your_api_key_here'")
        return

    print("=== Calculate Aluminum in Surface Water ===")
    print()

    # Calculate aluminum guidelines in surface water
    result = calculate_guidelines(
        parameter="Aluminum",
        media="surface_water",
        context={
            "pH": "7.0 1",  # pH 7.0 (dimensionless, use "1" as unit)
            "hardness": "100 mg/L",  # 100 mg/L as CaCO3
        },
    )

    # Display summary
    print(f"Total guidelines found: {result.total_count}")
    print(f"Context used: {result.context}")
    print()

    # Display results
    if result.total_count > 0:
        print("Guidelines:")
        print("-" * 80)
        for guideline in result.results:
            print(f"Parameter: {guideline.parameter}")
            print(f"Value: {guideline.value}")
            print(f"Unit: {guideline.unit}")
            print(f"Receptor: {guideline.receptor}")
            print(f"Exposure: {guideline.exposure_duration}")
            print(f"Source: {guideline.source}")
            print(f"Calculated: {guideline.is_calculated}")
            if guideline.lower is not None or guideline.upper is not None:
                print(f"Range: [{guideline.lower}, {guideline.upper}]")
            print("-" * 80)

    # Example with unit conversion
    print("\n=== With Unit Conversion to mg/L ===")
    print()

    result_mg = calculate_guidelines(
        parameter="Aluminum",
        media="surface_water",
        context={"pH": "7.0 1", "hardness": "100 mg/L"},
        target_unit="mg/L",  # Convert to mg/L
    )

    print(f"Total guidelines found: {result_mg.total_count}")
    if result_mg.total_count > 0:
        for guideline in result_mg.results[:3]:  # Show first 3
            print(f"  {guideline.parameter}: {guideline.value} ({guideline.source})")


if __name__ == "__main__":
    main()
