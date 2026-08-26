Claro. Vou ajustar o trecho para ficar com cara de **README.md de projeto**, mais organizado, profissional e fácil de seguir no Windows. Também corrigi os comandos que ficaram quebrados no texto.

# 🐍 Configuração do Python e yt-dlp no Windows

Este guia explica como instalar e configurar o **Python**, o **pip** e o **yt-dlp** no Windows utilizando o **PowerShell**.

---

## 1. Instalar o Python

Abra o **PowerShell** como usuário normal e execute:

```powershell
winget install Python.Python.3.13
```

Aguarde a instalação terminar.

### ⚠️ Se o comando apresentar erro

Se aparecer alguma mensagem de erro durante a instalação, **não tente outros comandos aleatoriamente**.

Copie e envie exatamente a mensagem apresentada pelo PowerShell para identificar o problema e utilizar o comando correto.

---

## 2. Reiniciar o PowerShell

Depois que a instalação terminar:

1. Feche completamente o PowerShell.
2. Abra o PowerShell novamente.
3. Verifique se o Python foi instalado corretamente.

Execute:

```powershell
python --version
```

O resultado esperado será parecido com:

```text
Python 3.13.x
```

Se aparecer a versão do Python, a instalação foi concluída com sucesso.

---

## 3. Verificar o pip

O `pip` é o gerenciador utilizado para instalar pacotes e bibliotecas do Python.

Execute:

```powershell
python -m pip --version
```

O resultado deverá ser semelhante a:

```text
pip 25.x.x from ... (python 3.13)
```

---

## 4. Instalar o yt-dlp

Com o Python e o pip funcionando, instale ou atualize o **yt-dlp**:

```powershell
python -m pip install -U yt-dlp
```

Aguarde a instalação terminar.

---

## 5. Verificar o yt-dlp

Depois da instalação, execute:

```powershell
python -m yt_dlp --version
```

Se aparecer um número de versão, por exemplo:

```text
2026.x.x
```

o `yt-dlp` está instalado corretamente.

---

## 6. Teste completo

Execute os comandos abaixo, um por vez:

```powershell
python --version
```

```powershell
python -m pip --version
```

```powershell
python -m yt_dlp --version
```

Se os três comandos retornarem suas respectivas versões, o ambiente está pronto para executar os scripts Python do projeto.

---

## 🛠️ Solução de problemas

### Python não é reconhecido

Se aparecer algo parecido com:

```text
'python' não é reconhecido como um comando interno ou externo
```

feche o PowerShell, abra novamente e tente:

```powershell
py --version
```

Se `py` funcionar, também é possível executar o pip usando:

```powershell
py -m pip --version
```

E instalar o yt-dlp com:

```powershell
py -m pip install -U yt-dlp
```

### Winget não encontra o Python

Primeiro pesquise os pacotes disponíveis:

```powershell
winget search Python
```

Depois procure pelo pacote oficial do Python e faça a instalação utilizando o ID correspondente.

---

## 🚀 Próximo passo

Depois que Python, pip e yt-dlp estiverem funcionando, você poderá executar os scripts Python deste projeto.

Para executar um arquivo Python:

```powershell
python nome_do_script.py
```

Exemplo:

```powershell
python main.py
```

---

## 📌 Resumo rápido

```powershell
winget install Python.Python.3.13
```

Feche e abra o PowerShell novamente.

```powershell
python --version
```

```powershell
python -m pip --version
```

```powershell
python -m pip install -U yt-dlp
```

```powershell
python -m yt_dlp --version
```

Se todos os comandos funcionarem, o ambiente Python está pronto.
