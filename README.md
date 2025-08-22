# Pytest Playwright Automation Framework (Python)

## Overview
This project is a Python-based automation framework using Playwright and Pytest, structured with the Page Object Model (POM) for maintainability and scalability. It includes configuration management (via `config.yaml`), logging, and a clear folder structure.

---

## Configuration
All sensitive data and URLs are stored in `config.yaml` at the project root. Edit this file to set your username, password, and base URL:

```
base_url: "https://vtop.vitap.ac.in/vtop/open/page"
username: "your_username"
password: "your_password"
```

---

## Folder Structure

```
pytest/
│
├── config.py                # Configuration for URLs and credentials
├── pages/                   # Page Object Model (POM) classes
│   ├── login_page.py
│   └── grade_history_page.py
├── tests/                   # Test cases
│   └── test_login_and_grades.py
├── utils/                   # Utility modules
│   └── logger.py
├── logs/                    # (Optional) Log files directory
└── README.md                # Project documentation
```

---

## Setup Instructions

1. **Install Python dependencies:**
   ```powershell
   pip install pytest pytest-asyncio playwright pyyaml
   python -m playwright install
   ```

2. **Project Configuration:**
   - Edit `config.yaml` to set your credentials and base URL. `config.py` loads these values for use in your tests.

4. **Logging:**
   - All major steps are logged using `utils/logger.py` for easier debugging.

5. **Page Object Model (POM):**
   - Each page interaction is encapsulated in its own class under `pages/`.

6. **Test Cases:**
   - All test cases are in the `tests/` folder and use the POM classes.

7. **Running Tests:**
   ```powershell
   pytest tests/test_login_and_grades.py
   ```

---

## Notes
- **CAPTCHA Handling:**
  - CAPTCHA automation is not recommended. For real-world scenarios, use a test environment or mock CAPTCHA if possible.
- **Logs:**
  - You can extend the logger to write to files in the `logs/` directory.
- **Extending the Framework:**
  - Add more POM classes for new pages and more test files as needed.

---

## Example Test Flow
1. Navigates to the login page.
2. Fills in username, password, and CAPTCHA.
3. Logs in and navigates to the grade history page.
4. Clicks the print button for grades.
5. All actions are logged for debugging.

---

## Contact
For questions or contributions, please open an issue or pull request.
