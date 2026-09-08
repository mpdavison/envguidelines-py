"""Example 07: Parameter Name Matching

Demonstrates using the match_parameters() function to handle naming
inconsistencies across domains, geographies, and languages.

This is useful when:
- Users enter chemical abbreviations (NH3, Cu, Al)
- Dealing with spelling variations (Aluminium vs Aluminum)
- Mapping external parameter names to the database
"""

from guidelinely import match_parameters

# Example 1: Match chemical abbreviations
print("=" * 60)
print("Example 1: Chemical Abbreviations")
print("=" * 60)

abbreviations = ["NH3", "Cu", "Al", "Pb"]
result = match_parameters(abbreviations)

for query_result in result.results:
    print(f"\nQuery: '{query_result.query}'")
    if query_result.matches:
        for match in query_result.matches:
            print(f"  ✓ {match.parameter_specification}")
            print(f"    Confidence: {match.confidence:.2f}")
            print(f"    Match type: {match.match_type}")
            print(f"    Media: {', '.join(match.media_types[:3])}")
            if match.sample_fraction or match.method_speciation:
                print(
                    "    Constituents: parameter="
                    f"{match.parameter}, sample_fraction={match.sample_fraction or '-'}, "
                    f"method_speciation={match.method_speciation or '-'}"
                )
    else:
        print("  ✗ No matches found")

# Example 2: Match with spelling variations using alias strategy
print("\n" + "=" * 60)
print("Example 2: Spelling Variations (Alias Strategy)")
print("=" * 60)

spelling_variants = ["Aluminium", "ammon", "sulphate"]
result = match_parameters(spelling_variants, strategy="alias", threshold=0.3)

for query_result in result.results:
    print(f"\nQuery: '{query_result.query}'")
    for match in query_result.matches[:3]:  # Show top 3 matches
        print(f"  {match.parameter} ({match.confidence:.2f})")

# Example 3: Fast matching without media types
print("\n" + "=" * 60)
print("Example 3: Fast Matching (No Media Types)")
print("=" * 60)

fast_queries = ["copper", "lead", "zinc"]
result = match_parameters(fast_queries, include_media=False)

print(f"Processed {result.total_queries} parameters")
for query_result in result.results:
    match_count = len(query_result.matches)
    print(f"  '{query_result.query}': {match_count} match(es)")

# Example 4: Lower threshold for more matches
print("\n" + "=" * 60)
print("Example 4: Lower Threshold for Fuzzy Matching")
print("=" * 60)

fuzzy_query = ["ammon"]
result = match_parameters(fuzzy_query, threshold=0.3)

query_result = result.results[0]
print(f"Query: '{query_result.query}'")
print(f"Found {len(query_result.matches)} matches:\n")
for match in query_result.matches:
    print(f"  {match.parameter_specification} ({match.confidence:.2f})")

# Example 5: Practical use case - Validate user input
print("\n" + "=" * 60)
print("Example 5: Validating User Input")
print("=" * 60)


def validate_parameter_name(user_input: str, min_confidence: float = 0.8) -> str:
    """Validate and normalize a parameter name from user input."""
    result = match_parameters([user_input])
    matches = result.results[0].matches

    if not matches:
        return f"❌ '{user_input}' not found in database"

    best_match = matches[0]
    if best_match.confidence >= min_confidence:
        return f"✓ '{user_input}' → {best_match.parameter} ({best_match.confidence:.0%})"
    else:
        suggestions = [m.parameter for m in matches[:3]]
        return f"⚠ '{user_input}' is ambiguous. Did you mean: {', '.join(suggestions)}?"


test_inputs = ["NH3", "copper", "alum", "xyz123"]
for user_input in test_inputs:
    print(validate_parameter_name(user_input))
