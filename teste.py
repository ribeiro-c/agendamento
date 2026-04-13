import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://mb4.bernoulli.com.br/login")
    page.get_by_role("textbox", name="Login").click()
    page.get_by_role("textbox", name="Login").fill("cecilia.amaro@soulasalle.com.br")
    page.get_by_role("textbox", name="Senha").click()
    page.get_by_role("textbox", name="Senha").fill("#30Ceci3004")
    page.get_by_role("button", name="ENTRAR").click()
    page.get_by_role("button", name="AVANÇAR").click()
    page.goto("https://mb4.bernoulli.com.br/")
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
