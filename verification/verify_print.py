from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        filepath = os.path.abspath("index.html")
        page.goto(f"file://{filepath}")

        # Take a screenshot of the whole page (print preview area)
        # We need to target the print area to make sure we see the boxes

        # Locate the General Info box
        # We can locate by text inside it
        general_info = page.locator("text=General Information:")
        # Get the parent container
        box = general_info.locator("..") # Parent

        # Screenshot the box specifically to show it renders correctly
        box.screenshot(path="verification/general_info_box.png")

        # Locate the Status Box
        status_box = page.locator("text=Discharge Status:").locator("xpath=../../../../..") # Tricky with tables.
        # Easier: .box-no-break containing "Discharge Status"

        # Let's just screenshot the whole print area
        page.locator("#print-area").screenshot(path="verification/print_area.png")

        browser.close()

if __name__ == "__main__":
    run()
