from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def convert_to_semantic(html):
    soup = BeautifulSoup(html, "html.parser")
    changes = []

    def log_change(tag, new_name):
        # Get classes and id, if available
        classes = " ".join(tag.get("class", []))
        tag_id = tag.get("id", "")

        # Construct original tag HTML
        original_tag_parts = [f"<{tag.name}"]
        if classes:
            original_tag_parts.append(f'class="{classes}"')
        if tag_id:
            original_tag_parts.append(f'id="{tag_id}"')
        original_tag_html = " ".join(original_tag_parts) + ">"

        # Construct new tag HTML
        new_tag_parts = [f"<{new_name}"]
        if classes:
            new_tag_parts.append(f'class="{classes}"')
        if tag_id:
            new_tag_parts.append(f'id="{tag_id}"')
        new_tag_html = " ".join(new_tag_parts) + ">"

        # Check if this change already exists in the changes list
        for change in changes:
            if (
                change["original_tag"] == original_tag_html
                and change["new_tag"] == new_tag_html
            ):
                # If it exists, increment the frequency
                change["frequency"] += 1
                break
        else:
            # If it doesn't exist, add it with a frequency of 1
            changes.append(
                {
                    "original_tag": original_tag_html,
                    "new_tag": new_tag_html,
                    "frequency": 1,
                }
            )

        tag.name = new_name

    # Replace <div> elements with semantic alternatives if the tag name is in their class or id
    for div in soup.find_all("div"):
        if "header" in div.get("class", []) or "header" in div.get("id", []):
            log_change(div, "header")
        elif "footer" in div.get("class", []):
            log_change(div, "footer")
        elif "main" in div.get("class", []):
            log_change(div, "main")
        elif "nav" in div.get("class", []) or "nav" in div.get("id", []):
            log_change(div, "nav")

    # Convert <b> tags to <strong>
    for b_tag in soup.find_all("b"):
        log_change(b_tag, "strong")

    # Convert <i> tags to <em>
    for i_tag in soup.find_all("i"):
        log_change(i_tag, "em")

    # Convert <span> tags used as block elements into <p>
    for span_tag in soup.find_all("span"):
        if "block" in span_tag.get("class", []):  # Example condition
            log_change(span_tag, "p")

    # Can add more rules here depending on specific use case

    # Ensure all img tags have alt attributes
    for img_tag in soup.find_all("img"):
        if not img_tag.get("alt"):
            img_tag["alt"] = "alt text here"
            # Log this change
            original_tag_html = f"<{img_tag.name}>"
            new_tag_html = f'<{img_tag.name} alt="alt text here">'

            # Check if this change already exists in the changes list
            for change in changes:
                if (
                    change["original_tag"] == original_tag_html
                    and change["new_tag"] == new_tag_html
                ):
                    # If it exists, increment the frequency
                    change["frequency"] += 1
                    break
            else:
                # If it doesn't exist, add it with a frequency of 1
                changes.append(
                    {
                        "original_tag": original_tag_html,
                        "new_tag": new_tag_html,
                        "frequency": 1,
                    }
                )

    modified_html = soup.prettify()
    return modified_html, changes


def load_full_page_html(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Launch headless browser
        page = browser.new_page()
        page.goto(url)
        # Wait for the content to load
        page.wait_for_load_state("networkidle")
        # Get the full page content after JavaScript execution
        content = page.content()
        browser.close()
        soup = BeautifulSoup(content, "html.parser")
        return soup.prettify()
