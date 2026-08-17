from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Número da pessoa (com código do país e DDD)
numero = "5599999999999"  # exemplo: +55 (Brasil) + DDD + número
mensagem = "Olá, esta é uma mensagem automática!"

# Inicializa o navegador
driver = webdriver.Chrome()  # precisa ter o ChromeDriver instalado
driver.get("https://web.whatsapp.com")

print("Escaneie o QR Code do WhatsApp Web para continuar...")
time.sleep(20)  # tempo para escanear o QR Code

# Abre a conversa pelo link direto
driver.get(f"https://web.whatsapp.com/send?phone={numero}&text={mensagem}")
time.sleep(10)

# Pressiona Enter para enviar
campo_mensagem = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
campo_mensagem.send_keys(Keys.ENTER)

print("Mensagem enviada com sucesso!")
