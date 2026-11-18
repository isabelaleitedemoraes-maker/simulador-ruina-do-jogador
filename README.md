# Simulador da Ruína do Jogador

Simulador desenvolvido como produto educacional da dissertação de mestrado do Programa de Mestrado Profissional em Matemática em Rede Nacional (PROFMAT), na Universidade de Brasília (UnB).

O programa simula o problema da ruína do jogador. Um apostador começa com um capital inicial e, a cada rodada, ganha ou perde R$ 1,00, até atingir a meta ou perder todo o dinheiro. O objetivo é que o professor possa mostrar aos estudantes, com base na matemática, por que quem joga contra a banca tende à ruína, mesmo quando há momentos de ganho.

## O que o simulador faz

- Desenha, de forma animada, a trajetória do capital de 1 a 10 apostadores ao longo das rodadas, com as linhas da meta (verde) e da ruína (vermelha).
- Indica a rodada em que cada apostador faliu ou atingiu a meta.
- Ao clicar em **Mostrar valores calculados**, simula um grande número de apostadores e compara a probabilidade de ruína e a duração média observadas com os valores teóricos obtidos pelas fórmulas da ruína do jogador.

## Parâmetros

| Campo | Significado |
|---|---|
| Quantidade de jogadores | número de trajetórias desenhadas no gráfico (1 a 10) |
| Capital inicial (R$) | capital com que cada apostador começa |
| Meta (R$) | valor em que o apostador para de jogar, deve ser maior que o capital inicial |
| Chance de ganhar (%) | probabilidade de vencer cada rodada (1 a 99) |
| Nº de apostadores (estatísticas) | número de partidas simuladas para calcular os valores observados |

Por exemplo, com capital inicial de R$ 5,00, meta de R$ 10,00 e chance de ganhar de 45%, a probabilidade teórica de ruína é de aproximadamente 73%, enquanto em um jogo justo (50%) ela é de 50%.

## Requisitos

- Python 3.8 ou superior ([python.org](https://www.python.org/downloads/))
- Biblioteca `matplotlib`

A biblioteca `tkinter`, usada na janela do programa, já vem instalada com o Python no Windows e no macOS. No Linux, pode ser necessário instalá-la (por exemplo, `sudo apt install python3-tk`).

Para instalar o `matplotlib`, abra o terminal e digite

```
pip install matplotlib
```

## Como executar

### Pelo executável (Windows, sem instalar nada)

Para quem não quer instalar o Python, há uma versão executável do simulador para Windows.

1. Acesse a seção **Releases**, no lado direito desta página.
2. Na versão mais recente, baixe o arquivo `ruina_do_jogador.exe`.
3. Dê dois cliques no arquivo para abrir o simulador.

Como o executável não possui assinatura digital, o Windows pode exibir o aviso "O Windows protegeu o computador". Nesse caso, clique em **Mais informações** e depois em **Executar assim mesmo**. Alguns antivírus também podem bloquear o arquivo na primeira vez. Se preferir não usar o executável, siga uma das opções abaixo, que executam o código-fonte.

### Pelo PyCharm

O código foi escrito no PyCharm, da JetBrains, na versão gratuita, por ser um ambiente mais intuitivo para quem está começando.

1. Instale o PyCharm em [jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/download/).
2. Baixe este repositório (botão **Code** e depois **Download ZIP**) e descompacte a pasta.
3. No PyCharm, abra a pasta em **File > Open**.
4. Abra o arquivo `ruina_do_jogador.py` e clique no botão de executar (triângulo verde).

Se o PyCharm avisar que o `matplotlib` não está instalado, clique na sugestão de instalação que aparece no próprio editor.

### Pelo IDLE, ambiente que acompanha o Python

1. Abra o IDLE, que é instalado junto com o Python.
2. Em **File > Open**, abra o arquivo `ruina_do_jogador.py`.
3. Pressione **F5** para executar.

### Pelo terminal

Dentro da pasta do repositório, digite

```
python ruina_do_jogador.py
```

O arquivo `play-button.png` é opcional. Se ele estiver na mesma pasta do código, o botão de iniciar aparece como ícone, e, caso contrário, aparece o botão de texto **▶ Jogar**.

## Relação com a matemática

As funções `prob_ruina_teorica` e `duracao_teorica` implementam as fórmulas da probabilidade de ruína e da duração esperada do jogo, deduzidas no Capítulo 4 da dissertação a partir das cadeias de Markov. A função `simular_partida` reproduz a cadeia de Markov da ruína do jogador, e a função `monte_carlo` repete muitas partidas para estimar as mesmas quantidades, o que permite comparar a frequência observada com a probabilidade calculada (Lei dos Grandes Números).

Quando o jogo é desfavorável e a meta é grande, a potência $(q/p)^N$ fica muito grande. Por isso, nesse caso, o código usa uma forma equivalente da fórmula, obtida multiplicando o numerador e o denominador por $(q/p)^{-N}$, o que evita erros numéricos.

## Uso de inteligência artificial

Durante a Aula 1 da aplicação da sequência didática, percebemos que a janela do programa cortava a parte inferior, onde aparecem os valores calculados, dependendo do tamanho da tela do computador. Como não conseguimos corrigir esse problema sozinhos, utilizamos uma ferramenta de inteligência artificial para identificar a causa e ajustar a organização da janela. A correção foi revisada e testada antes das aulas seguintes. A parte matemática do simulador não foi alterada nessa correção.

## Como citar

SOBRENOME, Isabela. **Simulador da ruína do jogador**. 2026. Produto educacional (Mestrado Profissional em Matemática em Rede Nacional) – Universidade de Brasília, Brasília, 2026. Disponível em: https://github.com/SEU-USUARIO/simulador-ruina-do-jogador.

## Licença

Este projeto está sob a licença MIT. Professores e estudantes podem usar, copiar e adaptar o código livremente, desde que mantenham a referência ao trabalho original.
