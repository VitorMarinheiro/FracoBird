# Fraco Bird
Projeto de desenvolvimento de uma **Rede Neural Artificial** criada para aprender a jogar o jogo [FlappyBird](https://flappybird.io/) utilizando a biblioteca [PyGame](https://www.pygame.org/news) do Python. 

![](https://github.com/VitorMarinheiro/FracoBird/blob/main/assets/running.gif)

## Execução
Para realizar a execução do jogo basta utilizar o seguinte comando:

`python3 main.py`

## Configurações adicionais de Execução
O projeto contém o arquivo `config.properties` com alguns campos que servem como parâmetro para a execução da rede neural e do jogo.
Você pode editar os valores e analisar como a rede neural se comporta em cada cenário.

```
[geracoes]
population=50   <- Quantidade de indivíduos que serão treinados em cada geração.

[pygame]
fps=30          <- Taxa de atualização de frames do PyGame.

pipespaw=60     <- Taxa de Spaw dos canos, quanto maior o valor, mais espaçados serão os canos.
```

