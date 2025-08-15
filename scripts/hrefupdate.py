"""
This script updates recipe descriptions in a database by converting LaTeX-style links and italic text to Markdown format.
It looks for \href{url}{text} and converts it to [text](url), and \textit{text} to *text*.
"""

import re
from recipes2.models import Recipe

# Pattern to match \href{url}{text}
href_pattern = re.compile(r'\\href\{([^}]+)\}\{([^}]+)\}')

# Pattern to match \textit{text} -> *text*
textit_pattern = re.compile(r'\\textit\{([^}]+)\}')

# Only consider recipes containing a backslash for efficiency
recipes = Recipe.objects.filter(description__contains='\\')

for r in recipes:
    original = r.description

    # Convert \href{url}{text} -> [text](url)
    updated = href_pattern.sub(r'[\2](\1)', original)

    # Convert \textit{text} -> *text*
    updated = textit_pattern.sub(r'*\1*', updated)

    if updated != original:
        print(f"Recipe {r.id}:")
        print("Original:")
        print(original)
        print("Suggested Revision:")
        print(updated)
        print("-" * 40)

        # Ask for confirmation
        response = input("Save this revision? [y/N]: ").strip().lower()
        if response == "y":
            r.description = updated
            r.save()
            print(f"Recipe {r.id} updated.\n")
        else:
            print("Skipped.\n")
