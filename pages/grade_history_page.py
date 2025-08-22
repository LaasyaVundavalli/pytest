from utils.logger import log

class GradeHistoryPage:
    def __init__(self, page):
        self.page = page

    async def open_grade_history(self):
        log("Opening Grade History")
        await self.page.get_by_role("link", name=" Grade History").click()

    async def print_grades(self):
        log("Clicking print button")
        await self.page.locator("#printVTOPCoreDocument").click()
