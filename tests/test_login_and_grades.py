
import pytest
from playwright.async_api import async_playwright
from pages.login_page import LoginPage
from pages.grade_history_page import GradeHistoryPage
import config
from utils.logger import log, error

@pytest.mark.asyncio
async def test_login_and_check_grades():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        try:
            await page.goto("https://vtop.vitap.ac.in/vtop/login")
            await page.get_by_role("link", name="Student ").click()
            await page.goto("https://vtop.vitap.ac.in/vtop/login")
            await page.get_by_role("textbox", name="Username").click()
            await page.get_by_role("textbox", name="Username").fill(config.USERNAME)
            await page.get_by_role("textbox", name="Password").click()
            await page.get_by_role("textbox", name="Password").fill(config.PASSWORD)
            # Try to get the CAPTCHA textbox, reload if not found
            captcha_found = False
            for attempt in range(10):
                try:
                    await page.get_by_role("textbox", name="Enter CAPTCHA shown above").wait_for(state="visible", timeout=3000)
                    captcha_found = True
                    break
                except Exception:
                    log(f"Captcha textbox not found, reloading login page (attempt {attempt+1})...")
                    await page.reload()
                    await page.get_by_role("textbox", name="Username").click()
                    await page.get_by_role("textbox", name="Username").fill(config.USERNAME)
                    await page.get_by_role("textbox", name="Password").click()
                    await page.get_by_role("textbox", name="Password").fill(config.PASSWORD)
            if not captcha_found:
                raise Exception("Captcha textbox did not appear after several reloads.")
            await page.get_by_role("textbox", name="Enter CAPTCHA shown above").click()
            log("Please manually enter the captcha in the browser and click Submit/Login. The script will proceed automatically after you log in.")
            # Wait for user to submit/login manually
            # Wait for navigation to indicate login success
            await page.wait_for_url("**/vtop/content?*", timeout=120000)
            await page.get_by_role("button", name="☰").click()
            await page.get_by_role("button", name=" Examination").click()
            await page.get_by_role("link", name=" Grade History").click()
            import time
            time.sleep(10)  # Wait for 10 seconds to allow Grade History to load
            await page.get_by_role("button", name="Close").click()
            # Listen for new tab (context.on("page"))
            new_page = None
            async def handle_new_page(page_obj):
                nonlocal new_page
                new_page = page_obj
            page.context.on("page", handle_new_page)
            await page.locator("#printVTOPCoreDocument").click()
            # Wait for the new tab to open
            for _ in range(30):
                if new_page:
                    break
                import asyncio
                await asyncio.sleep(1)
            if new_page:
                log(f"New tab opened with URL: {new_page.url}")
                # Wait for the new tab to finish loading
                await new_page.wait_for_load_state("networkidle", timeout=30000)
                pdf_path = "LaasyaVundavalli_GradeHistory.pdf"
                await new_page.pdf(path=pdf_path)
                log(f"PDF downloaded as {pdf_path}")
            else:
                error("New tab did not open after clicking print button.")
            log("Test completed successfully")
        except Exception as e:
            error(f"Test failed: {e}")
            raise
        finally:
            await browser.close()
