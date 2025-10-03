# MiPower — Integração Personalizada do Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** é uma integração do Home Assistant que permite controlar o estado de energia de leitores de multimédia que não suportam o tradicional Wake-on-LAN (WOL), mas que podem ser "acordados" por um pedido de emparelhamento Bluetooth. Foi especificamente concebida para dispositivos como a Xiaomi Mi Box, mas pode funcionar com outras boxes Android TV semelhantes.

Esta integração cria uma entidade `switch` (interruptor) no Home Assistant. 
- **Ligar** o interruptor envia uma série de comandos Bluetooth através de `bluetoothctl` para acordar o dispositivo.
- **Desligar** o interruptor chama o serviço `media_player.turn_off` para o dispositivo ligado.
- O estado do interruptor é automaticamente sincronizado com o estado da entidade do leitor de multimédia ligado.

## Pré-requisitos

- **Home Assistant OS / Supervised / Container:** Esta integração requer uma instalação do Home Assistant baseada em Linux, onde a ferramenta de linha de comandos `bluetoothctl` esteja disponível e acessível. **NÃO** funcionará numa instalação do Home Assistant Core no Windows.

## Instalação via HACS (Recomendado)

Esta integração está disponível como um repositório personalizado no HACS.

1.  Navegue para o seu painel do HACS.
2.  Clique em **Integrations** (Integrações).
3.  Clique no menu de três pontos no canto superior direito e selecione **"Custom repositories"** ("Repositórios Personalizados").
4.  Na caixa de diálogo, introduza as seguintes informações:
    - **Repository (Repositório):** `https://github.com/DenizOner/MiPower`
    - **Category (Categoria):** `Integration` (Integração)
5.  Clique em **"Add"** ("Adicionar").
6.  A integração "MiPower" aparecerá agora na sua lista HACS. Clique nela.
7.  Clique no botão **"Download"** ("Transferir") e, em seguida, clique novamente em **"Download"** ("Transferir") na próxima janela.
8.  Após a conclusão da transferência, **tem de reiniciar o Home Assistant** para que a integração seja carregada.

## Instalação Manual

Embora o HACS seja o método recomendado, também pode instalar a integração manualmente.

1.  Vá para a [página de Lançamentos](https://github.com/DenizOner/MiPower/releases) do repositório e transfira o ficheiro `mipower.zip` da versão mais recente.
2.  Descompacte o ficheiro transferido.
3.  Dentro da pasta descompactada, encontrará um diretório `custom_components`. Copie a pasta `mipower` de dentro dele.
4.  Cole a pasta `mipower` copiada na pasta `custom_components` no seu diretório de configuração do Home Assistant. Se a pasta `custom_components` não existir, terá de a criar.
    - O caminho final deve ser semelhante a: `.../config/custom_components/mipower/`
5.  Reinicie o Home Assistant.

## Configuração

Após reiniciar, pode adicionar e configurar o interruptor MiPower.

1.  Vá para **Settings > Devices & Services** (Definições > Dispositivos e Serviços).
2.  Clique no botão **"+ Add Integration"** ("+ Adicionar Integração") no canto inferior direito.
3.  Procure por **"MiPower"** e clique nele.

### Configuração Fácil (Recomendado)

Esta é a forma mais simples de configurar a integração.

1.  Quando solicitado, escolha **"Easy Setup"** ("Configuração Fácil").
2.  A integração detetará automaticamente os leitores de multimédia ativados por Bluetooth no seu sistema.
3.  Selecione o seu dispositivo alvo (p. ex., "Xiaomi Mi Box 4") na lista pendente.
4.  Clique em **"Submit"** ("Submeter").

É tudo! A integração criará um interruptor ligado ao seu leitor de multimédia.

### Configuração Avançada

Use este método se a Configuração Fácil não encontrar o seu dispositivo ou se precisar de configurar definições de tempo avançadas desde o início.

1.  **Passo 1: Seleção do Dispositivo**
    - Escolha **"Advanced Setup"** ("Configuração Avançada").
    - Selecione o seu leitor de multimédia alvo da lista de *todos* os leitores de multimédia no seu Home Assistant.
2.  **Passo 2: Endereço MAC**
    - A integração tentará encontrar o endereço MAC Bluetooth do dispositivo selecionado. 
    - Se encontrado, será pré-preenchido. Verifique se está correto.
    - Se não for encontrado, tem de introduzir o endereço MAC Bluetooth do seu dispositivo manualmente.
3.  **Passo 3: Definições de Tempo**
    - Pode configurar vários tempos limite e atrasos para os comandos Bluetooth. Para a maioria dos utilizadores, os valores predefinidos são suficientes.
4.  Clique em **"Submit"** ("Submeter") para concluir a configuração.

## Opções

Depois de configurar o seu interruptor MiPower, pode ajustar as definições de tempo a qualquer momento.

1.  Vá para **Settings > Devices & Services** (Definições > Dispositivos e Serviços).
2.  Encontre a integração MiPower e clique em **"Configure"** ("Configurar").
3.  Ajuste os seletores para *debounce*, tempos limite e atrasos conforme necessário.

## Explicação das Definições de Tempo

No menu de configuração ou opções, pode ajustar o tempo dos comandos Bluetooth. Para a maioria dos utilizadores, os valores predefinidos funcionam bem.

- **Turn-On Debounce (Debounce de Ligar):** O tempo mínimo (em segundos) que deve passar antes que o comando 'ligar' possa ser executado novamente. Isto evita o envio excessivo de sinais de despertar para o dispositivo se o interruptor for alternado rapidamente.

- **Turn-Off Debounce (Debounce de Desligar):** O tempo mínimo (em segundos) que deve passar antes que o comando 'desligar' possa ser executado novamente. 

- **Delay Between Commands (Atraso Entre Comandos):** Um atraso muito curto (em segundos) entre o envio de comandos consecutivos para o utilitário `bluetoothctl`. Em alguns sistemas, adicionar uma pequena pausa pode melhorar a fiabilidade.

- **Process Spawn Timeout (Tempo Limite de Criação de Processo):** O tempo máximo (em segundos) para esperar que o processo `bluetoothctl` inicie. Se não conseguir iniciar dentro deste tempo, a tentativa de ligar falhará.

- **Pairing Timeout (Tempo Limite de Emparelhamento):** Na lógica de ligação simplificada, esta é a quantidade de tempo a aguardar após o envio do comando `pair` antes de assumir o sucesso. Dá tempo ao dispositivo para processar o sinal de despertar.

- **Bluetooth Scan Duration (Duração da Análise Bluetooth):** A duração (em segundos) que a integração irá analisar para dispositivos Bluetooth antes de tentar enviar o comando de emparelhamento. Uma análise mais longa pode ajudar a encontrar dispositivos lentos a anunciar a sua presença.

---