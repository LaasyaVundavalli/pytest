from utils.logger import log

class LoginPage:
    def __init__(self, page):
        self.page = page

    async def goto(self, url):
        log("Navigating to login page")
        await self.page.goto(url)

    async def login(self, username, password):
        # Go to login page and click login button

        await self.page.goto("https://vtop.vitap.ac.in/vtop/open/page")
        await self.page.get_by_role("button", name="").click()

        # Check if captcha image is present, else reload only the login page (not the full flow)
        log("Checking for captcha image...")
        # Go to login page and click login button once
        await self.page.goto("https://vtop.vitap.ac.in/vtop/open/page")
        await self.page.get_by_role("button", name="").click()

        for attempt in range(10):
            try:
                await self.page.wait_for_selector("img[aria-describedby='button-addon2']", timeout=3000)
                log("Captcha image found.")
                # Fill username and password
                log("Filling in username and password...")
                await self.page.get_by_role("textbox", name="Username").click()
                await self.page.get_by_role("textbox", name="Username").fill(username)
                await self.page.get_by_role("textbox", name="Password").click()
                await self.page.get_by_role("textbox", name="Password").fill(password)
                # Log message for manual captcha entry
                log("Please manually enter the captcha in the browser and click Submit. The script will proceed automatically.")
                import time
                time.sleep(10)
                break
            except Exception:
                log("Captcha not found, reloading login page...")
                await self.page.reload()
                await self.page.get_by_role("button", name="").click()
        else:
            raise Exception("Captcha image did not appear after several reloads.")
