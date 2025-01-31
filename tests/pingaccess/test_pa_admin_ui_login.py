import os
import unittest

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pingone import common as p1_utils
import pingone_ui as p1_ui


@unittest.skipIf(
    os.environ.get("ENV_TYPE") == "customer-hub",
    "Customer-hub CDE detected, skipping test module",
)
class TestPAAdminUILogin(p1_ui.ConsoleUILoginTestBase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.public_hostname = os.getenv(
            "PA_ADMIN_PUBLIC_HOSTNAME",
            f"https://pingaccess-admin.{os.environ['TENANT_DOMAIN']}",
        )
        cls.username = f"sso-pingaccess-test-user-{cls.tenant_name}"
        cls.password = "2FederateM0re!"
        cls.delete_pingone_user()
        cls.create_pingone_user(role_attribute_name="p1asPingAccessRoles",
                                role_attribute_values=[f"{cls.environment}-pa-admin"])

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.delete_pingone_user()

    def test_user_can_access_pa_admin_console(self):
        # Wait for admin console to be reachable if it has been restarted by another test
        self.wait_until_url_is_reachable(self.public_hostname)
        # Attempt to access the PingAccess Admin console with SSO
        self.pingone_login()
        self.browser.get(self.public_hostname)
        self.browser.implicitly_wait(10)
        try:
            title = self.browser.find_element(
                By.XPATH, "//div[contains(text(), 'Applications')]"
            )
            wait = WebDriverWait(self.browser, timeout=10)
            wait.until(lambda t: title.is_displayed())
            self.assertTrue(
                title.is_displayed(),
                f"PingAccess Admin console 'Applications' page was not displayed when attempting to access {self.public_hostname}. SSO may have failed. Browser contents: {self.browser.page_source}",
            )
        except NoSuchElementException:
            self.fail(
                f"PingAccess Admin console 'Applications' page was not displayed when attempting to access {self.public_hostname}. SSO may have failed. Browser contents: {self.browser.page_source}",
            )


if __name__ == "__main__":
    unittest.main()
