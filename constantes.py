KEYSPACE = "xmercury"
ADMS = [766039963736866828, 1119222124368896020, 921158705075077150, 813254664241414144]
MARCH = "<:march:1302059770785824861>"
INSERT_PERSONAGEM = "INSERT INTO xmercury.personagens (id, nome, nickname, level, path, classe, legacy, heritage, melancholy, catarse, pe, pe_atual, hp, hp_atual, hp_tipo, reducao_de_dano, bonus_de_proficiencia, pericias, talentos, passivas, skills, forca, dexterity, constituicao, inteligencia, sabedoria, carisma, pontos_de_sombra, resistencia, vulnerabilidade, imunidade, inventario_itens, inventario_numero, volume_atual, limite_de_volumes, condicoes, saldo, imagem, tokenn, usuario)"
INSERT_SKILL = "INSERT INTO xmercury.skills (id, nome, custo, execucao, descritores, alcance, duracao, ataque, acerto, erro, efeito, especial, gatilho, alvo, carga, modificador_execucao, modificador_nome, modificador_descricao, modificador_gasto, modificador_gasto_tipo)"
INSERT_PASSIVA = "INSERT INTO xmercury.passivas (id, nome, descricao, modificador_execucao, modificador_nome, modificador_descricao, modificador_gasto, modificador_gasto_tipo)"
INSERT_TALENTO = "INSERT INTO xmercury.talentos (id, nome, descricao, modificador_execucao, modificador_nome, modificador_descricao, modificador_gasto, modificador_gasto_tipo)"
INSERT_ITEM = "INSERT INTO xmercury.itens (id, nome, descricao, preco, volume)"
INSERT_CONDICAO = "INSERT INTO xmercury.condicoes (id, nome, descricao)"
INSERT_DESCRITOR = "INSERT INTO xmercury.descritores (id, nome, tipo, descricao)"
INSERT_PERICIA = (
    "INSERT INTO xmercury.pericias (id, nome, descricao, e_vantagem, e_soma, somar)"
)
