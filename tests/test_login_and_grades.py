
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
        login_page = LoginPage(page)
        grade_history_page = GradeHistoryPage(page)

        try:
            await login_page.goto(config.BASE_URL)
            await login_page.login(config.USERNAME, config.PASSWORD)

            await page.goto("https://vtop.vitap.ac.in/vtop/content?")
            # Click the second '' button
            await page.get_by_role("button", name="").nth(1).click()

            # Try to click the first visible 'Examination' button
            examination_buttons = page.locator("button:has-text('Examination')")
            count = await examination_buttons.count()
            clicked = False
            for i in range(count):
                btn = examination_buttons.nth(i)
                if await btn.is_visible():
                    await btn.click(force=True)
                    clicked = True
                    break
            if not clicked:
                log("No visible 'Examination' button found. Trying to click 'Grade History' link directly.")

            # Click the correct 'Grade History' link (second match, sidebar)
            grade_history_locator = page.locator("a[data-url='examinations/examGradeView/StudentGradeHistory']").nth(1)
            await grade_history_locator.wait_for(state="visible", timeout=20000)
            await grade_history_locator.click()
            # Wait for popup and click print button
            page1_promise = page.wait_for_event("popup")
            await page.locator("#printVTOPCoreDocument").click()
            page1 = await page1_promise
            # Right click on 'Fundamentals of Electrical' cell in popup
            await page1.get_by_role("cell", name="Fundamentals of Electrical").click(button="right")
            log("Test completed successfully")
        except Exception as e:
            error(f"Test failed: {e}")
            raise
        finally:
            await browser.close()
