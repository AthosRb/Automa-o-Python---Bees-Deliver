from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

console = Console()

# CONFIGURAÇÃO DO PERFIL
chrome_profile = Options()
chrome_profile.add_argument(
    r"--user-data-dir=C:\temp\selenium\bees_profile"
)
chrome_profile.add_argument("--profile-directory=Default")

console.clear()

console.print(Panel.fit(
    "[bold cyan]AUTOMAÇÃO BEES DELIVER[/bold cyan]\n"
    "[white]Python + Selenium[/white]\n\n"
    "[green]Status:[/green] Inicializando navegador...",
    border_style="cyan"
))


# INICIAR NAVEGADOR
browser = webdriver.Chrome(options=chrome_profile)
browser.maximize_window()
browser.get("https://deliver-portal.bees-platform.com/")


# TEMPO PARA LOGIN
sleep(6)


try:
    # LOGIN (EMAIL)
    browser.find_element(By.ID, "signInName")
    console.print("[yellow]🔐 Sessão expirada, fazendo login...[/yellow]")


    browser.find_element(By.ID, "next").click()


    sleep(4)


    # LOGIN (SENHA)
    browser.find_element(By.ID, "password").send_keys("------")
    sleep(1)
    browser.find_element(By.ID, "next").click()


    sleep(6)  # TEMPO PARA ACESSAR A TELA INICIAL


except NoSuchElementException:
    console.print("[green]✅ Sessão ativa, login reaproveitado[/green]")

# === SELCIONAR A DATA ===
input("[ENTER] Selecione a data no calendario...")
sleep(2)

# ENTRAR EM "DETALHES DAS ROTAS"
sleep(5)
while True:
    console.rule("[bold blue] 🚀 Iniciando fluxo...[/bold blue]")


    # === BUSCAR MOTORISTA ===
    input("[ENTER] Adicione o nome do motorista no campo de busca!")
    sleep(2)


    # === EXPANDIR LINHA ===
    browser.find_element(
        By.XPATH,"//button[@aria-label='expand row']").click()
    sleep(2)


    poc_card = browser.find_element(
        By.XPATH,"(//div[@data-test-id='poc-card'])[1]"
    )
    sleep(2)
    poc_card.click()
    sleep(2)


    # === EXTRAÇÃO DE DADOS ===
    motorista = browser.find_element(By.XPATH,"//span[normalize-space(.)='Motorista:']/following::span[1]").text


    ajudante = browser.find_element(By.XPATH,"//span[normalize-space(.)='Ajudante:']/following::span[1]").text


    console.print(f"[bold]Motorista:[/bold] [cyan]{motorista}[/cyan]\n"
                  f"[bold]Ajudante:[/bold] [cyan]{ajudante}[/cyan]"
    )



    # === FECHAR DETALHES (X)===
    browser.find_element(
        By.XPATH, "//button[@data-test-id='visit-details-title-close-button']").click()
    sleep(3)


    with Progress(transient=True) as progress:
        tarefa = progress.add_task("[cyan]Processando dados...", total=100)
        for _ in range(100):
            sleep(0.02)
            progress.update(tarefa, advance=1)


    # === ABRIR GOOGLE FORMS ===
    console.print("[magenta] 🌐 Abrindo GOOGLE FORMS...[/magenta]")
    browser.execute_script("window.open('https://forms.gle/N92DZiRurHXcMLck8', '_blank');")
    sleep(4)


    # === GUARDA ABAS ===
    abas = browser.window_handles
    browser.switch_to.window(abas[-1])


    # === NOME MOTORISTA - GOOGLE FORMS ===
    browser.find_element(By.XPATH,"//input[@type='text']").send_keys(motorista)
    sleep(2)


    # === NOME AJUDANTE - GOOGLE FORMS ===
    browser.find_element(By.XPATH,"//textarea[@class='KHxj8b tL9Q4c']").send_keys(ajudante)
    sleep(2)


    # === ADICIONE UMA DATA MANUALMENTE ===
    input("[ENTER] Adicione a data no formulário..")


    # === BOTÃO DE ENVIAR FORMULÁRIO ===
    browser.find_element(
        By.XPATH,"(//span[@class='NPEfkd RveJvd snByac'])[1]").click()
    sleep(2)


    # === VOLTAR PARA O BEES DELIVER ===
    browser.close()
    browser.switch_to.window(abas[0])


    # === PERGUNTA FINAL (S/N) ===
    continuar = input("\nDeseja continuar o fluxo? (S/N):").strip().upper()


    if continuar == "S":
        console.print("[bold blue] 🔁 Reinicinado fluxo... [/bold blue]")
        continue
    elif continuar == "N":
        console.print("[bold red] 🛑 Finalizando automação... [/bold red]")
        break


    else:
        console.print("[bold red] ❌ Opção inválida. Encerrando por segurança. [/bold red]")
        break


# === FINAL FLUXO ===
console.print ("[green] Aguarde um momento... [/green]")
sleep(2)
browser.quit()
console.print("[green] Automação encerrada com sucesso. [/green]")

