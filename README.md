# Cobrinha multiplayer

O jogo é uma adaptação multijogador do clássico jogo da cobrinha. Em um mesmo campo, duas cobras competem para ter a maior pontuação.

O jogo possui dois pontos de entrada, o servidor e o cliente. O cliente é um programa interativo com interface de usuário em que é possível iniciar e jogar uma partida. O servidor é uma ferramenta no terminal que aceita conexões de clientes e mantém e sincroniza o estado do jogo, auditando as ações e movimentos dos clientes. Adotamos esse modelo para desacoplar a lógica de negócio do jogo e permitir que hospedemos o servidor em algum serviço de cloud futuramente caso se mostre necessário.

## Desenvolvedores
 - Rian Radeck Santos Costa - 187793
 - Cirilo Max Macedo de Morais Filho - 168838
 - Igor Brito Andrade - 171929
