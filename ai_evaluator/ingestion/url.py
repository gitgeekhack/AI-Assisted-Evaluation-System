import time
from playwright.sync_api import sync_playwright


def validate_url(url):
    """
    Validates a working prototype URL

    Checks:
    - Accessibility
    - Page load
    - UI elements (buttons, inputs, links)
    - Basic interactions
    - Navigation
    - Data processing signals

    Returns structured validation report
    """

    result = {
        "url": url,
        "accessible": False,
        "loads": False,
        "status_code": None,
        "ui_elements": {
            "buttons": [],
            "inputs": [],
            "links": []
        },
        "flows": {
            "login_detected": False,
            "navigation_working": False,
            "core_actions_detected": False
        },
        "data_processing_signals": [],
        "errors": None
    }

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Step 1: Accessibility
            response = page.goto(url, timeout=15000)

            if response:
                result["accessible"] = True
                result["status_code"] = response.status

            # Step 2: Load check
            page.wait_for_load_state("load", timeout=10000)
            result["loads"] = True

            # Step 3: Extract UI elements
            buttons = page.query_selector_all("button")
            inputs = page.query_selector_all("input")
            links = page.query_selector_all("a")

            result["ui_elements"]["buttons"] = [
                b.inner_text().strip() for b in buttons if b.inner_text()
            ][:10]

            result["ui_elements"]["inputs"] = [
                i.get_attribute("name") or i.get_attribute("placeholder")
                for i in inputs
            ][:10]

            result["ui_elements"]["links"] = [
                l.inner_text().strip() for l in links if l.inner_text()
            ][:10]

            # Step 4: Detect login flow
            login_keywords = ["login", "sign in", "email", "password"]

            if any(
                any(k in (text or "").lower() for k in login_keywords)
                for text in result["ui_elements"]["buttons"] + result["ui_elements"]["inputs"]
            ):
                result["flows"]["login_detected"] = True

            # Step 5: Navigation test
            try:
                if links:
                    links[0].click(timeout=3000)
                    time.sleep(2)
                    result["flows"]["navigation_working"] = True
            except Exception:
                pass

            # Step 6: Core action detection (heuristic)
            action_keywords = ["submit", "run", "predict", "upload", "generate"]

            if any(
                any(k in (text or "").lower() for k in action_keywords)
                for text in result["ui_elements"]["buttons"]
            ):
                result["flows"]["core_actions_detected"] = True

            # Step 7: Data processing signals
            try:
                # Try interacting with input + button
                if inputs and buttons:
                    inputs[0].fill("test input")
                    buttons[0].click(timeout=3000)
                    time.sleep(2)

                    # Check DOM changes
                    content = page.content().lower()

                    signals = ["result", "success", "output", "processed"]

                    detected = [s for s in signals if s in content]

                    result["data_processing_signals"] = detected

            except Exception:
                pass

            browser.close()

    except Exception as e:
        result["errors"] = str(e)

    return result