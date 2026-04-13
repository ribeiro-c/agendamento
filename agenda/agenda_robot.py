from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime, timedelta
import logging
import os
import json
import time
import random
import traceback

# -------------------------------
# CONFIG
# -------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COOKIES_PATH = "agenda/storage/cookies.json"
DEBUG_DIR = "debug"

os.makedirs(DEBUG_DIR, exist_ok=True)

# -------------------------------
# UTIL
# -------------------------------

def screenshot(page, nome):
    path = os.path.join(DEBUG_DIR, f"{nome}.png")
    page.screenshot(path=path, full_page=True)
    logger.info(f"Screenshot: {path}")

def delay():
    time.sleep(random.uniform(1.0, 2.0))

def executar_com_retry(fn, tentativas=3):
    for i in range(tentativas):
        try:
            return fn()
        except Exception as e:
            logger.warning(f"Tentativa {i+1} falhou: {e}")
            time.sleep(2)
    raise Exception("Falha após retries")

# -------------------------------
# COOKIES
# -------------------------------

def carregar_cookies(context):
    if not os.path.exists(COOKIES_PATH):
        return False
    try:
        with open(COOKIES_PATH, "r") as f:
            cookies = json.load(f)
        context.add_cookies(cookies)
        return True
    except:
        return False

def salvar_cookies(context):
    os.makedirs(os.path.dirname(COOKIES_PATH), exist_ok=True)
    with open(COOKIES_PATH, "w") as f:
        json.dump(context.cookies(), f)

# -------------------------------
# FECHAR TUTORIAL (VERSÃO GOD)
# -------------------------------

def fechar_tutorial(page):
    for i in range(3):
        try:
            logger.info("Tentando fechar tutorial...")

            modal = page.locator(".TutorialInitial")

            if modal.count() > 0:
                if modal.first.is_visible():
                    # botão correto
                    btn = page.locator('[tooltip="Desabilitar tutorial"] button')

                    if btn.count() > 0:
                        btn.first.click(force=True)
                        logger.info("Botão tutorial clicado")

                    else:
                        logger.warning("Botão não encontrado → usando ESC")
                        page.keyboard.press("Escape")

                    time.sleep(1)

            # tentativa extra via ESC sempre
            page.keyboard.press("Escape")

        except Exception as e:
            logger.warning(f"Erro ao fechar tutorial: {e}")

# -------------------------------
# LOGIN
# -------------------------------

def fazer_login(page, context, login, senha):
    logger.info("Iniciando login...")

    page.goto("https://mb4.bernoulli.com.br/login")

    page.wait_for_selector("#re-login", timeout=10000)

    screenshot(page, "01_login")

    page.fill("#re-login", login)
    page.fill("#input-pass", senha)

    delay()

    page.click("button:has-text('ENTRAR')")
    # fechar_tutorial(page)

    # AVANÇAR
    try:
        page.click("button:has-text('AVANÇAR')", timeout=5000)
        fechar_tutorial(page)
        logger.info("Clicou em AVANÇAR")
    except:
        logger.info("Sem botão avançar")

    # BOAS VINDAS
    try:
        page.wait_for_selector("text=Que bom ter você aqui", timeout=10000)
        screenshot(page, "02_boas_vindas")

        page.locator("div").filter(has_text="Que bom ter você aqui").nth(1).click()
        delay()
        page.get_by_role("button").nth(2).click()

        logger.info("Tela de boas-vindas resolvida")
    except:
        logger.info("Sem tela de boas-vindas")

    # fechar_tutorial(page)

    page.goto("https://mb4.bernoulli.com.br/")

    try:
        page.get_by_role("button", name="Minha Área").click(timeout=10000)
    except:
        pass

    salvar_cookies(context)

    screenshot(page, "03_pos_login")

    logger.info("Login concluído")

def garantir_login(page, context, login, senha):
    page.goto("https://mb4.bernoulli.com.br/")

    try:
        page.get_by_role("button", name="Minha Área").wait_for(timeout=5000)
        logger.info("Sessão válida")
    except:
        logger.info("Sessão inválida → login necessário")
        fazer_login(page, context, login, senha)

# -------------------------------
# AGENDA
# -------------------------------

def ir_para_agenda(page):
    logger.info("Indo para agenda...")

    try:
        page.get_by_role("button", name="Minha Área").click(timeout=10000)
        delay()
        page.get_by_role("button", name="Agenda").click(timeout=10000)
    except:
        logger.warning("Falha via menu → URL direta")
        page.goto("https://mb4.bernoulli.com.br/minhaarea/agenda")

    

    screenshot(page, "04_agenda")

    try:
        page.get_by_role("button", name="Calendário").click(timeout=5000)
    except:
        pass

    # fechar_tutorial(page)

    # 🔥 ESPERA INTELIGENTE
    try:
        page.wait_for_selector(".semana-day:not(.outMonth)", timeout=20000)
    except:
        logger.warning("Reload da agenda")
        page.reload()
        # fechar_tutorial(page)
        page.wait_for_selector(".semana-day:not(.outMonth)", timeout=20000)

    logger.info("Agenda carregada")

# -------------------------------
# EXTRAÇÃO COM FILTRO (15 DIAS)
# -------------------------------

def extrair_eventos(page):
    dados = []

    hoje = datetime.now().date()
    inicio = hoje - timedelta(days=7)
    fim = hoje + timedelta(days=7)

    logger.info(f"Intervalo: {inicio} até {fim}")

    dias = page.locator(".semana-day")
    total = dias.count()

    logger.info(f"{total} dias encontrados")

    for i in range(total):
        try:
            dia = dias.nth(i)

            data_iso = dia.get_attribute("data-date")
            if not data_iso:
                continue

            data = datetime.fromisoformat(data_iso.replace("Z", "")).date()

            # 🔥 FILTRO REAL
            if not (inicio <= data <= fim):
                continue

            eventos = dia.locator(".tag-circle")

            if eventos.count() == 0:
                continue

            logger.info(f"Dia com evento: {data}")

            dia.click()

            page.wait_for_selector(".EventItem", timeout=10000)

            itens = page.locator(".EventItem")

            for j in range(itens.count()):
                try:
                    evento = itens.nth(j)
                    evento.click()

                    modal = page.locator(".ModalContent.Event")
                    modal.wait_for()

                    titulo = modal.locator(".title-24-600").inner_text()

                    dados.append({
                        "data": data,
                        "titulo": titulo
                    })

                    logger.info(f"Evento: {titulo}")

                    page.keyboard.press("Escape")
                    delay()

                except Exception as e:
                    logger.warning(f"Erro evento: {e}")

        except Exception as e:
            logger.warning(f"Erro dia: {e}")

    return dados

# -------------------------------
# MAIN
# -------------------------------

def executar(login, senha):
    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(headless=False)

            context = browser.new_context()

            carregar_cookies(context)

            page = context.new_page()

            executar_com_retry(lambda: garantir_login(page, context, login, senha))
            executar_com_retry(lambda: ir_para_agenda(page))

            dados = extrair_eventos(page)

            logger.info(f"Total eventos: {len(dados)}")

            browser.close()

            return dados

    except Exception as e:
        logger.error(f"Erro geral: {e}")
        traceback.print_exc()
        return []

# -------------------------------
# RUN
# -------------------------------

if __name__ == "__main__":
    eventos = executar(
        "cecilia.amaro@soulasalle.com.br",
        "#30Ceci3004"
    )

    print(f"\nEventos: {len(eventos)}")

    for e in eventos[:10]:
        print(f"{e['data']} - {e['titulo']}")