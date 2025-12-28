from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the file
        filepath = os.path.abspath("index.html")
        page.goto(f"file://{filepath}")

        # Define the selectors for the boxes we modified
        # Note: We didn't add IDs, so we have to use CSS classes or structure selectors
        # "Status Box" is the div with border, p-2, mb-4, box-no-break containing "Discharge Status"
        # "General Info" is the div with border, mb-4, box-no-break containing "General Information:"

        # We can just check if there are elements with the class .box-no-break
        # and if they have the correct computed style.

        elements = page.query_selector_all(".box-no-break")

        if len(elements) < 3:
            print(f"Error: Expected at least 3 elements with .box-no-break, found {len(elements)}")
            exit(1)

        print(f"Found {len(elements)} elements with .box-no-break class.")

        for i, handle in enumerate(elements):
            # Check computed style
            break_inside = handle.evaluate("el => getComputedStyle(el).breakInside")
            # page-break-inside might return 'avoid' or empty depending on browser support mapping
            # but modern chromium maps break-inside.

            print(f"Element {i}: break-inside = {break_inside}")

            if break_inside != "avoid":
                print(f"Error: Element {i} does not have break-inside: avoid")
                exit(1)

        print("Verification successful: All marked boxes have break-inside: avoid")
        browser.close()

if __name__ == "__main__":
    run()
