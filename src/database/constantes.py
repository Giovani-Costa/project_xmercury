KEYSPACE = ""

INSERT_PERSONAGEM = "INSERT INTO personagens (id_personagem, nome, nickname, level, legacy, classe, path, heritage, melancholy, catarse, pe, pe_atual, hp, hp_atual, hp_tipo, reducao_de_dano, bonus_de_proficiencia, pontos_de_sombra, pericias, protecao_forca, bonus_forca, protecao_destreza, bonus_destreza, protecao_constituicao, bonus_constituicao, protecao_inteligencia, bonus_inteligencia, protecao_sabedoria, bonus_sabedoria, protecao_carisma, bonus_carisma, volume_atual, limite_de_volume, resistencia, vulnerabilidade, imunidade, saldo, imagem, tokenn, usuario, id_party)"
INSERT_SKILL = "INSERT INTO skills (id_skill, nome, custo, execucao, descritores, alcance, duracao, ataque, acerto, erro, efeito, especial, gatilho, alvo, carga, id_personagem)"
INSERT_PASSIVA = "INSERT INTO passivas (id_passiva, nome, descricao, id_personagem)"
INSERT_TALENTO = "INSERT INTO talentos (id_talento, nome, descricao, id_personagem)"
INSERT_ITEM = "INSERT INTO itens (id_item, nome, descricao, preco, volume)"
INSERT_CONDICAO = "INSERT INTO condicoes (id_condicao, nome, descricao)"
INSERT_DESCRITOR = "INSERT INTO descritores (id_descritor, nome, tipo, descricao)"
INSERT_PERICIA = (
    "INSERT INTO pericias (id_pericia, nome, descricao, e_vantagem, e_soma, somar)"
)
INSERT_MODIFICADOR = "INSERT INTO modificadores (id_modificador, execucao, nome, descricao, gasto, gasto_tipo)"
INSERT_MODIFICADOR_SKILLS = (
    "INSERT INTO modificadores_skills (id_skill, id_modificador)"
)
INSERT_ITENS_PERSONAGENS = (
    "INSERT INTO itens_personagens (id_item, id_personagem, quantidade)"
)
INSERT_PARTY = "INSERT INTO party (id_party)"
