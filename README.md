XMercury é um bot que automatiza e facilita minha campanha de RPG, girando dados, mostrando fichas, tocando músicas e etc. Os principais sistemas em funcionamentos são:
  
  - Rolagem de dados: Rola qualquer quantidade de dados com qualquer quantidade de lados. O resultado do dado por ser alterado por alguns elementos, como **vantagem**, **desvantagem** ou **bônus**. O sistema de dados participa diretamente do conjunto de comandos *Discord Bot*, mas também faz parte de outros sistemas e comandos, como o de perícias e ataques.
  - Sonoplastia: O *Discord Bot* reproduz efeitos sonoros e  músicas na call que está ocorrendo a campanha do RPG, podendo ser o tema de alguem personagem, música de algum ambiente ou a playlist de batalha. O mestre controla o efeito sonoro que irá tocar com um comando no próprio Discord.
  - Banco de Dados: O projeto utiliza um banco de dados em PostgreSQL, com o seguinte mapeamento:
    - skills(nome, custo, execucao, descritores, alcance, duracao, ataque, acerto, erro, efeito, especial, gatilho, alvo, carga, modifidadores)
    - talentos()
    - passivas()
    - modificadores()
    - personagens()
    - itens()
    - pericias()
    - condicoes()
    - descritores()
    - party()