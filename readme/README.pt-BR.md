# MiPower — Integração Personalizada do Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** é uma integração do Home Assistant que permite controlar o estado de energia de media players que não suportam o tradicional Wake-on-LAN (WOL), mas que podem ser "acordados" por uma solicitação de emparelhamento Bluetooth. Ele foi especificamente projetado para dispositivos como a Xiaomi Mi Box, mas pode funcionar com outras caixas de Android TV semelhantes.

Esta integração cria uma entidade `switch` (interruptor) no Home Assistant. 
- **Ligar** o interruptor envia uma série de comandos Bluetooth via `bluetoothctl` para acordar o dispositivo.
- **Desligar** o interruptor chama o serviço `media_player.turn_off` para o dispositivo vinculado.
- O estado do interruptor é automaticamente sincronizado com o estado da entidade do media player vinculado.

## 🤝 Apoie

O projeto MiPower é desenvolvido com a visão de adicionar valor à comunidade de código aberto. Seu apoio é vital para manter a continuidade e a velocidade de desenvolvimento deste projeto.

Se você aprecia meu trabalho, pode me apoiar através do GitHub Sponsors ou das seguintes plataformas. Obrigado antecipadamente!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternativamente, você pode ver todas as opções de financiamento clicando no **botão Patrocinador (❤️)** no canto superior direito do repositório.

## Pré-requisitos

- **Home Assistant OS / Supervised / Container:** Esta integração requer uma instalação do Home Assistant baseada em Linux, onde a ferramenta de linha de comando `bluetoothctl` esteja disponível e acessível. Ela **NÃO** funcionará em uma instalação do Home Assistant Core no Windows.

## Instalação via HACS (Recomendado)

Esta integração está disponível como um repositório personalizado no HACS.

1.  Navegue até o seu painel do HACS.
2.  Clique em **Integrations** (Integrações).
3.  Clique no menu de três pontos no canto superior direito e selecione **"Custom repositories"** ("Repositórios Personalizados").
4.  Na caixa de diálogo, insira as seguintes informações:
    - **Repository (Repositório):** `https://github.com/DenizOner/MiPower`
    - **Category (Categoria):** `Integration` (Integração)
5.  Clique em **"Add"** ("Adicionar").
6.  A integração "MiPower" agora aparecerá em sua lista HACS. Clique nela.
7.  Clique no botão **"Download"** ("Baixar") e, em seguida, clique novamente em **"Download"** ("Baixar") na próxima janela.
8.  Após a conclusão do download, **você DEVE reiniciar o Home Assistant** para que a integração seja carregada.

## Instalação Manual

Embora o HACS seja o método recomendado, você também pode instalar a integração manualmente.

1.  Vá para a [página de Lançamentos](https://github.com/DenizOner/MiPower/releases) do repositório e baixe o arquivo `mipower.zip` do lançamento mais recente.
2.  Descompacte o arquivo baixado.
3.  Dentro da pasta descompactada, você encontrará um diretório `custom_components`. Copie a pasta `mipower` de dentro dele.
4.  Cole a pasta `mipower` copiada na pasta `custom_components` em seu diretório de configuração do Home Assistant. Se a pasta `custom_components` não existir, você precisará criá-la.
    - O caminho final deve ser parecido com: `.../config/custom_components/mipower/`
5.  Reinicie o Home Assistant.

## Configuração

Após a reinicialização, você pode adicionar e configurar o interruptor MiPower.

1.  Vá para **Settings > Devices & Services** (Configurações > Dispositivos e Serviços).
2.  Clique no botão **"+ Add Integration"** ("+ Adicionar Integração") no canto inferior direito.
3.  Pesquise por **"MiPower"** e clique nele.

### Configuração Fácil (Recomendado)

Esta é a maneira mais simples de configurar a integração.

1.  Quando solicitado, escolha **"Easy Setup"** ("Configuração Fácil").
2.  A integração descobrirá automaticamente media players habilitados para Bluetooth em seu sistema.
3.  Selecione seu dispositivo de destino (p. ex., "Xiaomi Mi Box 4") na lista suspensa.
4.  Clique em **"Submit"** ("Enviar").

É isso! A integração criará um interruptor vinculado ao seu media player.

### Configuração Avançada

Use este método se a Configuração Fácil não encontrar seu dispositivo ou se você precisar configurar configurações avançadas de tempo desde o início.

1.  **Passo 1: Seleção do Dispositivo**
    - Escolha **"Advanced Setup"** ("Configuração Avançada").
    - Selecione seu media player de destino na lista de *todos* os media players em seu Home Assistant.
2.  **Passo 2: Endereço MAC**
    - A integração tentará encontrar o endereço MAC Bluetooth do dispositivo selecionado. 
    - Se encontrado, ele será pré-preenchido. Verifique se está correto.
    - Se não for encontrado, você deve inserir o endereço MAC Bluetooth do seu dispositivo manualmente.
3.  **Passo 3: Configurações de Tempo**
    - Você pode configurar vários tempos limite (timeouts) e atrasos para os comandos Bluetooth. Para a maioria dos usuários, os valores padrão são suficientes.
4.  Clique em **"Submit"** ("Enviar") para concluir a configuração.

## Opções

Depois de configurar seu interruptor MiPower, você pode ajustar as configurações de tempo a qualquer momento.

1.  Vá para **Settings > Devices & Services** (Configurações > Dispositivos e Serviços).
2.  Encontre a integração MiPower e clique em **"Configure"** ("Configurar").
3.  Ajuste os controles deslizantes para *debounce*, tempos limite e atrasos conforme necessário.

## Explicação das Configurações de Tempo

No menu de configuração ou opções, você pode ajustar o tempo dos comandos Bluetooth. Para a maioria dos usuários, os valores padrão funcionam bem.

- **Turn-On Debounce (Debounce de Ligar):** O tempo mínimo (em segundos) que deve passar antes que o comando 'ligar' possa ser executado novamente. Isso evita o envio excessivo de sinais de despertar para o dispositivo se o interruptor for alternado rapidamente.

- **Turn-Off Debounce (Debounce de Desligar):** O tempo mínimo (em segundos) que deve passar antes que o comando 'desligar' possa ser executado novamente. 

- **Delay Between Commands (Atraso Entre Comandos):** Um atraso muito curto (em segundos) entre o envio de comandos consecutivos para o utilitário `bluetoothctl`. Em alguns sistemas, adicionar uma pequena pausa pode melhorar a confiabilidade.

- **Process Spawn Timeout (Tempo Limite de Criação de Processo):** O tempo máximo (em segundos) para esperar que o processo `bluetoothctl` inicie. Se ele falhar ao iniciar dentro desse tempo, a tentativa de ligar falhará.

- **Pairing Timeout (Tempo Limite de Emparelhamento):** Na lógica de ligação simplificada, este é o tempo a ser aguardado após o envio do comando `pair` antes de assumir o sucesso. Isso dá tempo ao dispositivo para processar o sinal de despertar.

- **Bluetooth Scan Duration (Duração da Varredura Bluetooth):** A duração (em segundos) que a integração fará a varredura por dispositivos Bluetooth antes de tentar enviar o comando de emparelhamento. Uma varredura mais longa pode ajudar a encontrar dispositivos lentos para anunciar sua presença.

## Leia no seu idioma

*   [Afrikaans](README.af.md)
*   [العربية (Arabic)](README.ar.md)
*   [български (Bulgarian)](README.bg.md)
*   [বাংলা (Bengali)](README.bn.md)
*   [Català (Catalan)](README.ca.md)
*   [Čeština (Czech)](README.cs.md)
*   [Dansk (Danish)](README.da.md)
*   [Deutsch (German)](README.de.md)
*   [Deutsch (Schweiz) (German, Switzerland)](README.de-CH.md)
*   [Ελληνικά (Greek)](README.el.md)
*   [English](../README.md)
*   [Español (Spanish)](README.es.md)
*   [Eesti (Estonian)](README.et.md)
*   [Euskara (Basque)](README.eu.md)
*   [فارسی (Persian)](README.fa.md)
*   [Suomi (Finnish)](README.fi.md)
*   [Français (French)](README.fr.md)
*   [Gaeilge (Irish)](README.ga.md)
*   [Galego (Galician)](README.gl.md)
*   [ગુજરાતી (Gujarati)](README.gu.md)
*   [עברית (Hebrew)](README.he.md)
*   [हिन्दी (Hindi)](README.hi.md)
*   [Hrvatski (Croatian)](README.hr.md)
*   [Magyar (Hungarian)](README.hu.md)
*   [Bahasa Indonesia (Indonesian)](README.id.md)
*   [Íslenska (Icelandic)](README.is.md)
*   [Italiano (Italian)](README.it.md)
*   [日本語 (Japanese)](README.ja.md)
*   [ქართული (Georgian)](README.ka.md)
*   [ಕನ್ನಡ (Kannada)](README.kn.md)
*   [한국어 (Korean)](README.ko.md)
*   [Kernewek (Cornish)](README.kw.md)
*   [Lëtzebuergesch (Luxembourgish)](README.lb.md)
*   [Lietuvių (Lithuanian)](README.lt.md)
*   [Latviešu (Latvian)](README.lv.md)
*   [മലയാളം (Malayalam)](README.ml.md)
*   [Монгол (Mongolian)](README.mn.md)
*   [मराठी (Marathi)](README.mr.md)
*   [Bahasa Melayu (Malay)](README.ms.md)
*   [Norsk bokmål (Norwegian Bokmål)](README.nb.md)
*   [नेपाली (Nepali)](README.ne.md)
*   [Nederlands (Dutch)](README.nl.md)
*   [Polski (Polish)](README.pl.md)
*   [Português (Portuguese)](README.pt.md)
*   [Português (Brasil) (Portuguese, Brazil)](README.pt-BR.md)
*   [Română (Romanian)](README.ro.md)
*   [Русский (Russian)](README.ru.md)
*   [Slovenčina (Slovak)](README.sk.md)
*   [Slovenščina (Slovenian)](README.sl.md)
*   [Српски (Serbian)](README.sr.md)
*   [Srpski (latinica) (Serbian, Latin)](README.sr-Latn.md)
*   [Svenska (Swedish)](README.sv.md)
*   [Kiswahili (Swahili)](README.sw.md)
*   [తెలుగు (Telugu)](README.te.md)
*   [ไทย (Thai)](README.th.md)
*   [Türkçe (Turkish)](README.tr.md)
*   [Українська (Ukrainian)](README.uk.md)
*   [اردو (Urdu)](README.ur.md)
*   [Tiếng Việt (Vietnamese)](README.vi.md)
*   [简体中文 (Simplified Chinese)](README.zh-CN.md)
*   [繁體中文 (香港) (Traditional Chinese, Hong Kong)](README.zh-HK.md)

---