import json
import os
import sys

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from constantes import (
    INSERT_CONDICAO,
    INSERT_ITEM,
    INSERT_PASSIVA,
    INSERT_PERICIA,
    INSERT_PERSONAGEM,
    INSERT_SKILL,
    INSERT_TALENTO,
    KEYSPACE,
)

cloud_config = {"secure_connect_bundle": "database\\secure-connect-xmercury.zip"}

with open("database\\xmercury-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]
bonus_de_proficiencia = 3
level = 5
pe = 15
ataque_especializado = "1d8"
ataque_poderoso = "1d8"

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
with cluster.connect() as session:

    session.execute(f"DROP TABLE {KEYSPACE}.skills")
    session.execute(f"DROP TABLE {KEYSPACE}.talentos")
    session.execute(f"DROP TABLE {KEYSPACE}.passivas")
    session.execute(f"DROP TABLE {KEYSPACE}.personagens")
    session.execute(f"DROP TABLE {KEYSPACE}.itens")
    session.execute(f"DROP TABLE {KEYSPACE}.pericias")
    session.execute(f"DROP TABLE {KEYSPACE}.condicoes")
    session.execute(f"DROP TABLE {KEYSPACE}.party")

    session.execute(
        f"""
    CREATE TABLE {KEYSPACE}.skills (
       id UUID PRIMARY KEY,
       nome TEXT,
       custo INT,
       execucao TEXT,
       descritores TEXT,
       alcance TEXT,
       duracao TEXT,
       ataque TEXT,
       acerto TEXT,
       erro TEXT,
       efeito TEXT,
       especial TEXT,
       gatilho TEXT,
       alvo TEXT,
       carga TEXT,
       modificador_execucao TEXT,
       modificador_nome TEXT,
       modificador_descricao TEXT,
       modificador_gasto INT,
       modificador_gasto_tipo TEXT
    );
    """
    )
    print("SKILLS CRIADA")

    session.execute(
        f"""
    CREATE TABLE {KEYSPACE}.talentos (
       id UUID PRIMARY KEY,
       nome TEXT,
       descricao TEXT,
       modificador_execucao TEXT,
       modificador_nome TEXT,
       modificador_descricao TEXT,
       modificador_gasto INT,
       modificador_gasto_tipo TEXT
    );
    """
    )
    print("TALENTOS CRIADO")

    session.execute(
        f"""
    CREATE TABLE {KEYSPACE}.passivas (
       id UUID PRIMARY KEY,
       nome TEXT,
       descricao TEXT,
       modificador_execucao TEXT,
       modificador_nome TEXT,
       modificador_descricao TEXT,
       modificador_gasto INT,
       modificador_gasto_tipo TEXT
    );
    """
    )
    print("PASSIVAS CRIADA")

    session.execute(
        f"""
    CREATE TABLE {KEYSPACE}.personagens (
       id UUID PRIMARY KEY,
       nome TEXT,
       nickname TEXT,
       level INT,
       legacy TEXT,
       classe TEXT,
       path TEXT,
       heritage TEXT,
       melancholy TEXT,
       catarse INT,
       pe INT,
       pe_atual INT,
       hp INT,
       hp_atual INT,
       hp_tipo TEXT,
       reducao_de_dano INT,
       bonus_de_proficiencia INT,
       pericias LIST<UUID>,
       talentos LIST<UUID>,
       passivas LIST<UUID>,
       skills LIST<UUID>,
       forca LIST<INT>,
       dexterity LIST<INT>,
       constituicao LIST<INT>,
       inteligencia LIST<INT>,
       sabedoria LIST<INT>,
       carisma LIST<INT>,
       pontos_de_sombra INT,
       resistencia LIST<TEXT>,
       vulnerabilidade LIST<TEXT>,
       imunidade LIST<TEXT>,
       inventario_itens LIST<UUID>,
       inventario_numero LIST<INT>,
       volume_atual INT,
       limite_de_volumes INT,
       condicoes LIST<TEXT>,
       saldo INT,
       imagem TEXT,
       tokenn TEXT,
       usuario TEXT
        );"""
    )
    print("PERSONAGENS CRIADA")

    session.execute(
        f"""
    CREATE TABLE {KEYSPACE}.itens (
       id UUID PRIMARY KEY,
       nome TEXT,
       descricao TEXT,
       preco INT,
       volume INT
    );
    """
    )
    print("ITENS CRIADA")

    session.execute(
        f"""
    CREATE TABLE {KEYSPACE}.party (
       id UUID PRIMARY KEY,
       personagens_jogaveis LIST<UUID>,
    );
    """
    )
    print("PARTY CRIADA")

    session.execute(
        f"""
    CREATE TABLE {KEYSPACE}.pericias (
       id UUID PRIMARY KEY,
       nome TEXT,
       descricao TEXT,
       e_vantagem BOOLEAN,
       e_soma BOOLEAN,
       somar LIST<TEXT>,
        );"""
    )
    print("PERÍCIAS CRIADA")

    session.execute(
        f"""
    CREATE TABLE {KEYSPACE}.condicoes (
       id UUID PRIMARY KEY,
       nome TEXT,
       descricao TEXT,
    );
    """
    )
    print("CONDIÇÕES CRIADA\n")

    # -------------------------------------------------------------------------------------------

    # PROMPT PERICIAS

    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (7b32de93-92b1-402a-93fe-c7a295535490, 'Forja', 'Sua maestria na forja é admirável. Você pode forjar ferramentas se tiver os materiais e equipamentos necessários, sendo eles: calor, material, martelo e uma base.', false, false, Null);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (57565a89-08ef-47ce-984a-f95272c58e03, 'Pescaria', 'A pesca fez parte da vida da sua vida. Você possui vantagem em testes de pesca.', true, false, Null);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (98f70eea-9c31-44a4-8c66-2b1eca1a530a, 'Transmutação', 'Se o usuário tiver alguma forma de poder realizar transmutações, ele pode somar seu bônus de proficiência ou algum atributo-chave de conjuração nos testes (INT; SAB; CAR).', false, true, ['bonus_de_proficiencia', 'inteligencia', 'sabedoria', 'carisma']);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (e95b8d53-07d4-47bf-9d99-e23368c2dcba, 'Alquimia', 'O usuário pode criar poções se tiver materiais e equipamentos necessários: matéria-prima, recipiente(opcional), maleta de manipulação, caldeirão e calor ou mesa de síntese.', false, false, Null);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (fc42be7c-bf7b-4fb2-b528-ac30bc0605d6, 'Culinária', 'O usuário pode fazer pratos deliciosos (comidas com efeitos especiais), possui vantagem nos testes de culinária e pode somar seu bônus de proficiência ou algum atributo-chave de conjuração nos testes (INT; SAB; CAR).', true, true, ['bonus_de_proficiencia', 'inteligencia', 'sabedoria', 'carisma']);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (802584f3-85a5-4851-988c-eebe5e1a6d12, 'Geografia', 'O usuário se torna capaz em fazer mapas e nunca esquecer um caminho.', false, false, Null);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (c25f6a18-6b01-423a-9c44-1781f677137d, 'Arcanismo', 'O usuário tem proficiência na área arcâna da magia, como runas, rituais e até mesmo grimórios arcânos. O usuário pode somar seu bônus de proficiência ou algum atributo-chave de conjuração nos testes (INT; SAB; CAR).', false, true, ['bonus_de_proficiencia', 'inteligencia', 'sabedoria', 'carisma']);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (a67da4e1-ba56-4b89-a491-6b0ae5337453, 'Cultura', 'O usuário tem conhecimentos da sociedade, atualidades, costumes e noções culturais ao redor de Opath. O usuário pode somar seu bônus de proficiência ou algum atributo-chave de conjuração nos testes (INT; SAB; CAR).', false, true, ['bonus_de_proficiencia', 'inteligencia', 'sabedoria', 'carisma']);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (1030947f-9e65-476a-b08c-c834a2ddfe7f, 'Diplomacia', 'O usuário possui conhecimentos em barganhas e trocas. O usuário pode somar seu bônus de proficiência ou alguma atributo-chave de conjuração nos testes (INT; SAB; CAR).', false, true, ['bonus_de_proficiencia', 'inteligencia', 'sabedoria', 'carisma']);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (0222604e-cd4d-4077-b19f-7eb7c4e8c927, 'Persuasão', 'O usuário possui conhecimentos em manipulações e tratos. O usuário pode somar seu bônus de proficiência ou alguma atributo-chave de conjuração nos testes (INT; SAB; CAR)', false, true, ['bonus_de_proficiencia', 'inteligencia', 'sabedoria', 'carisma']);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (71850f9a-22d3-441a-b675-8858d8718984, 'Furtividade', 'O usuário sabe bem como se misturar em multidões e pode somar seu bônus de proficiência ou alguma atributo-chave para somar no teste (FOR; DES; CON; INT; SAB; CAR).', false, true, ['bonus_de_proficiencia', 'inteligencia', 'sabedoria', 'carisma']);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (ebaea72e-3d09-487e-a809-360077352a5c, 'Sobrevivência', 'O usuário tem experiência de como é sobreviver no ambiente selvagem e caçar feras. Ele pode somar seu bônus de proficiênica ou alguma atributo-chave para somar no teste (FOR; DES; CON; INT; SAB; CAR).', false, true, ['bonus_de_proficiencia', 'forca', 'destreza', 'constituicao', 'inteligencia', 'sabedoria', 'destreza', 'forca']);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (a052505a-add0-4717-9d30-e382a0741058, 'Intimidação', 'O usuário sabe como fazer alguma criatura sentir medo. Ele pode somar seu bônus de proficiência ou alguma atributo-chave para somar no teste (FOR; CON; CAR).', false, true, ['bonus_de_proficiencia', 'forca', 'constituicao', 'carisma']);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (eab18040-8a73-41a1-ba35-66918c594f97, 'Magitecnologia', 'O usuário possui conhecimentos básicos sobre o funcionamento da magitecnologia e pode realizar testes com vantagens para entender como funciona alguns circuitos magitecnológico e montá-los.', true, false, Null);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (50e3508e-335c-42ef-97cf-1db7a07962c4, 'Malandragem', 'O usuário é esperto e consegue sabotar equipamentos magitecnológicos e arrombar portas', false, false, Null);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (110bf214-eb58-4c0b-8c4c-6eba30302575, 'Medicina', 'O usuário consegue detectar doenças, prestar primeiros socorros e fazer necropsias. O usuário possui um sucesso garantido em primeiros socorros por dia que tiver ataduras ou remédios em seu intentário', false, false, Null);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (3bc86566-ec94-4459-a7fc-2a5d094a1f39, 'Percepção', 'O usuário pode detectar, ouvir ou notar a presença de algo próximo. Ele pode somar seu bônus de proficiência ou alguma atributo-chave para somar no teste (DES; SAB).', false, true, ['bonus_de_proficiencia', 'sabedoria', 'destreza']);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (c57e4a9b-2e9d-4c97-9f6c-0139cd0ddb44, 'Lógica', 'O usuário é esperto e é bom para resolver enigmas. Ele pode somar seu bônus de proficiência ou algum atributo-chave nos testes (INT; SAB).', false, true, ['bonus_de_proficiencia', 'inteligencia', 'sabedoria']);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (d28b4723-1177-46ac-b1f2-bf785330b1a9, 'Disparo', 'O usuário possui uma boa pontaria. Ele pode somar seu bônus de proficiência em disparos com armas de fogo.', false, true, ['bonus_de_proficiencia']);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (c7482295-cb98-49fe-92fd-8266c8675121, 'Briga', 'O usuário é bom de briga. Ele pode somar seu bônus de proficiência ou em testes de acerto corpo a corpo', false, true, ['bonus_de_proficiencia']);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (62ef595a-2f6e-475c-8152-3f36a5c4e695, 'Agilidade', 'O usuário é ágil e consegue desviar de muito ataques. Ele pode somar seu bônus de proficiência em testes de esquiva.', false, true, ['bonus_de_proficiencia']);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (8d72c0e9-5c54-4b4a-b80a-a3b60d8f1309, 'Iniciativa', 'O usuário é veloz e é um dos primeiros a atacar em um combate. Ele pode somar seu bônus de proficiência ou algum atributo-chave nos testes (DES).', false, true, ['bonus_de_proficiencia', 'destreza']);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (d0f44af5-c299-41c2-9e84-72dd9cdb7351, 'Magia', 'O usuário é habilidoso com a magia. Ele pode somar seu bônus de proficiência em testes mágicos.', false, true, ['bonus_de_proficiencia']);"""
    )
    session.execute(
        f"""{INSERT_PERICIA}
    VALUES (89056ec3-8736-4136-a962-e86434799d2c, 'Esgrima', 'O usuário é habilidoso na arte da espada. Ele pode somar seu bônus de proficiência em testes de esgrima.', false, true, ['bonus_de_proficiencia']);"""
    )
    print("PERÍCIAS ADICIONADAS")

    # -------------------------------------------------------------------------------------------

    # PROMPT CONDIÇÕES

    session.execute(
        f"""{INSERT_CONDICAO}
    VALUES (5db1ddaf-b80a-412f-a899-9ecebd4bed7b, 'Agarrado', 'A criatura está ***Contida***.\nA condição termina se: a criatura que está ***Agarrando*** ficar ***Incapacitada***, se um efeito remover a criatura agarrada do alcance do agarrador ou do efeito de agarramento ou se a criatura agarrada vencer um teste de **FOR**.');"""
    )
    session.execute(
        f"""{INSERT_CONDICAO}
    VALUES (f6b7900f-4782-4d6f-8af3-e30e293c4021, 'Agarrando', 'A criatura está ativamente agarrando outro (que está ***Agarrada***).\nUma criatura que está ***Agarrando*** pode mover-se junto da criatura ***Agarrada***, mas tem seu movimento reduzido pela metade.\nA criatura deve ocupar suas duas mãos para manter a condição.\n Ela pode encerrar essa condição a qualquer momento com uma ação livre, encerrando também a condição ***Agarrada*** na outra criatura.');"""
    )
    session.execute(
        f"""{INSERT_CONDICAO}
    VALUES (d77a53e7-0f65-4104-a193-cfaabfed4ca4, 'Amedrontado', 'Uma criatura amedrontada tem **desvantagem** em testes de atributo e ataque.\nA criatura não pode se mover por vontade própria para perto da fonte de seu medo.\n Se não estiver vendo a fonte do medo ela fica parada no local que está.');"""
    )
    session.execute(
        f"""{INSERT_CONDICAO}
    VALUES (4c382c07-d787-497e-8ef7-1736a95aa072, 'Atordoado', 'Uma criatura atordoada está ***Incapacitada***, não pode se mover e só é capaz de balbuciar.');"""
    )

    # -------------------------------------------------------------------------------------------

    # PROMPT DE ITENS GENÉRICOS

    session.execute(
        f"""{INSERT_ITEM}
VALUES (99387f37-b128-4e88-a9e6-ca918a2d4b41, 'Poção de Cura', 'Você recupera 2d4+2 pontos de vida quando bebe esta poção.', 250, 1);"""
    )
    session.execute(
        f"""{INSERT_ITEM}
VALUES (5f219452-0438-40e4-ba90-d28ff16144c9, 'Poção de Cura Maior', 'Você recupera 4d4+4 pontos de vida quando bebe esta poção.', 500, 1);"""
    )

    # -------------------------------------------------------------------------------------------

    # PROMPT CHROLLO

    forca = ["12", "1"]
    destreza = ["12", "1"]
    constituicao = ["13", "2"]
    inteligencia = ["14", "4"]
    sabedoria = ["10", "0"]
    carisma = ["9", "-1"]

    reducao_de_dano = 4

    session.execute(
        f"""{INSERT_PASSIVA}
VALUES (d2808e11-146c-49f1-a631-4d365472a303, 'Ataque Poderoso', 'Você treinou seu corpo para ser capaz de desferir ataques poderosíssimos sempre que ataca. Seus **ATAQUES** com **ARMAS** recebem a seguinte modificação:', 'reacao', 'AMPLIAR + 15', '**Acerto:** você causa +1d8 pontos de dano do mesmo tipo.', 0, 'PE');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (02c0f9f6-a880-496e-98c1-795f4b00c700, 'Ataque de Superioridade', 0, 'acao', 'ATAQUE', '3m.', 'Instantânea.', 'FOR vs FOR', 'Você deve escolher um efeito entre: Deixar o alvo ***Caído***; Pegar um item do alvo; Deixar o alvo ***Agarrado***.', 'None', 'None', 'Você só pode usar essa habilidade em criaturas de seu tamanho ou menor.', 'None', 'Uma criatura.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (a4a7564b-37ed-43f5-bc09-df897ef8e7de, 'Ataque em Sequência', 1, 'acao', 'COMBATENTE', 'Pessoal.', 'Instântanea.', 'None', 'None', 'None', 'Você pode realizar uma combinação de duas habilidades dentre "Ataque Corpo a Corpo", "Ataque à Distância" e "Ataque de Superioridade" como <:acao_livre:1326585198892154901> ação livre.', 'None', 'None', 'Você.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (00a33d61-0ab6-4637-89fd-ccffac04ab3e, 'Transmutar Item', 1, 'acao bonus', 'MÁGICO, CRIAÇÃO', 'Pessoal.', 'Instantânea.', 'None', 'None', 'None', 'O usuário consome um item do inventário para criar um novo item. O item criado deve ser equivalente ao item consumido.', 'Caso o usuário perca o *Tablet de Transmutação* essa habilidade não poderá ser usada.', 'None', 'None', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (135b9b63-dec7-4378-b2a1-a2bfe1350869, 'Corte com a Masked Death', 0, 'acao', 'ATAQUE, ARMA, CORTANTE', '2m.', 'Instatânea.', '1d20 + {int(forca[1])} + 2 + {bonus_de_proficiencia} vs **DES**.', '1d8 + 1d10 + {bonus_de_proficiencia} pontos de dano **CORTANTE**', 'Caso você erre no teste de acerto, você solta a **ARMA** e terá que gastar sua <:acao_bonus:1326585197004722197> Ação Bônus para pegá-la novamente.', 'None', 'None', 'None', 'Uma criatura.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (08f4b428-a138-4edf-b3b7-a82c16aebb6c, 'Disparo com a Shorty Aemondir', 0, 'acao', 'DISPARO, PERFURANTE, ARMA, ESPALHAFATOSO, ATAQUE', '9m.', 'Instantânea.', '1d20 + {int(destreza[1])} + {bonus_de_proficiencia} vs **DES**.', '2d8 + {bonus_de_proficiencia} + 2 pontos de dano.', 'Caso você erre no teste de acerto, você solta a **ARMA** e terá que gastar sua <:acao_bonus:1326585197004722197> Ação Bônus para pegá-la novamente.', 'O usuário aplica +1 nível de ***Shadow Cover***.', 'None', 'None', 'Uma criatura.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (dbe7bcff-b5be-46a1-84e3-cbdf1a368283, 'Masked Death: Fools Blood', 1, 'acao', 'ATAQUE, ARMA, NECRÓTICO, MÁGICO', '3m.', 'Instântanea.', '1d20 + {int(forca[1])} + {bonus_de_proficiencia} + 2 vs **DES**', '2d8 + 1d10 + {bonus_de_proficiencia} de dano **NECRÓTICO**.', 'O encantamento acaba', 'None', 'O usuário precisa ativar o encantamento da espada para usar essa habilidade, usando sangue ou algumas gotas de uma poção de cura nela em uma <:acao_bonus:1326585197004722197> Ação Bônus.', 'None', 'Criaturas em um raio de 2m.', '{bonus_de_proficiencia}', 'None', 'None', 'None', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (429de159-48f9-48ab-870a-850983c4be4b, 'Mortalha Energizante', 0, 'reacao', 'HUMANO', 'Pessoal.', 'Instantânea.', 'None', 'None', 'None', 'Você recebe {bonus_de_proficiencia} pontos de ênfase temporários durante essa cena.', 'Você só pode usar essa habilidade uma vez por descanso.', 'Uma criatura na cena morre', 'None', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (f76dc202-536c-47f6-a9e2-cccb400d9102, 'Empoderamento Biomagitec', 0, 'acao bonus', 'MAGITÉCNICO', 'Toque.', 'Até o final do próximo descanso longo.', 'None', 'None', 'None', 'Você toca um objeto mundano e empodera-o com energia biomagitec. O objeto torna-se uma engenhoca magitec a sua escolha. Se for uma arma, recebe o descritor **MÁGICA**.', 'Você só pode usar essa habilidade uma vez por cena.', 'None', 'None', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (bd083bdf-6021-4680-b5c7-36ca4c4c537d, 'Construção Rápida de Magibot', 1, 'acao bonus', 'MAGITÉCNICO, PROTÓTIPO, CRIAÇÃO', 'None', 'Uma cena.', 'None', 'None', 'None', 'Você empodera peças biomagitec para criar um pequeno autômato chamado magibot.', 'None', 'None', 'Um espaço vago no inventário.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_PASSIVA}
VALUES (d06ff7ac-cad1-49d6-be84-6eb290879dea, 'Tradição Oral', 'Você é capaz de reter uma quantidade infinita de informação, desde que ela tenha sido transmitida oralmente para outra criatura. Você tem **vantagem** em todos os testes de **INT** relacionados a lembrar de fatos ou informações. Caso tenha sucesso no teste, significa que já repassou essa informação para outra criatura.', 'None', 'None', '0', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_PASSIVA}
VALUES (c47f8a5f-9531-4a07-8142-a1c2bc080684, 'Combate com uma Arma', 'Você recebe +1 em todas as **Proteções** físicas e em jogadas de dano enquanto estiver empunhando uma arma em uma mão e estiver com a outra mão livre.', 'None', 'None', '0', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_PASSIVA}
VALUES (60e33837-6378-4ec9-9490-bcc094e15a00, 'Façanha com uma Arma', 'Sua principal estratégia de combate consiste em atacar com precisão e deslocar-se para uma posição vantajosa. Se seu primeiro ataque em um combate for com sua arma, ele resulta em um **acerto crítico**.', 'None', 'None', '0', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_PASSIVA}
VALUES (bdb5a1da-730c-4886-b935-57eb852d4ad4, 'Protótipo Utilitário: Dispositivo de Proteção Avançado', 'Esse pequeno dispositivo é acoplado a uma armadura que você estiver vestindo. Enquanto estiver ativo, ele concede +1 na **redução de dano**', 'None', 'None', '0', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_TALENTO}
VALUES (f4e0b395-33f6-4ad2-97de-0a76bf42f968, 'Transmitir Conhecimento Adquirido', 'Você aperfeiçoou suas técnicas de transmissão de conhecimento. Ao final de uma Cena de Descanso, pode escolher um aliado para receber ***inspiração***, que dura até o próximo descanso longo.', 'None', 'None', '0', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_TALENTO}
VALUES (8173f83f-5ae8-4635-802f-d10d3e897b6e, 'O Preço do Progresso', 'Você recebe proficiência em armas de fogo. Ao usar uma arma de fogo, pode usar **INT** em vez de **DES** em testes de **ATAQUE** e dano.', 'None', 'None', '0', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_TALENTO}
VALUES (2ab46c0f-d69e-4e65-9285-d13c4b32043c, 'No Ponto Certo', 'Atacar com precisão de maneira astuta é sua especialidade. Sempre que atacar com uma arma com o descritor **LEVE**, você pode somar sua **INT** em teste de **ATAQUE** e no dano.', 'None', 'None', '0', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_ITEM}
VALUES (abb1a0d3-d0ac-4bc1-960b-9defa7dadde6, 'Masked Death', 'Uma espada longa com o encantamento *"Fools Blood"*. A espada é bem trabalhada e possui a inscrição "Masked Death" em sua lâmina, que faz referência à banda de seu antigo portador, Zombie. O encantamento precisa de um pouco de sangue ou algumas gotas de poção de cura para ativar suas cargas, depois da ativação a espdada fica vermelha e pode usar a habilidade *"Masked Death: Fools Blood"*.', 500, 2);"""
    )
    session.execute(
        f"""{INSERT_ITEM}
VALUES (938f7ffe-b0ff-4824-97dd-9769ccd35aae, 'Tablet de Transmutação', 'Uma grande invenção de um alquimista alemão do século XV. Um pedaço de ardósia lapidado com adornos metálicos e uma pedra filosofal no centro. A propriedade de reorganização de partículas permite transmutar elementos e até criar ****-*******.', 0, 2);"""
    )
    session.execute(
        f"""{INSERT_ITEM}
VALUES (3cb0873e-4ddf-4c3e-861d-aaf6151c7f17, 'Armadura de Couro Batido', 'Proteção comum entre mercenários e aventureiros inexperientes, reforçada com pequenas placas de couro em locais estratégicos.', 40, 3);"""
    )
    session.execute(
        f"""{INSERT_ITEM}
VALUES (21f4bb82-5741-44eb-ac29-4601f2fa2d9a, 'Armadura Espectral de Warpinier', 'Um espectro da aura da grande armadura de Warpiniier. Vestida por cima de tudo, concede +1 na **redução de dano** e contém os encantamentos: **Manipuladora de Sombras** e **Silenciosa**.', 0, 1);"""
    )
    session.execute(
        f"""{INSERT_ITEM}
VALUES (fa359f98-b7a9-44ed-acea-8e1099a34d83, 'Shorty Aemondir', 'Uma escopeta de ação por alavanca mágica de cano curto. Ela foi encontrada no castelo de Warpinier e provavelmente fazia parte do arsenal de Boris Nosferata. "Algo dentro de mim me dizia que eu precisava muito de uma dessa" — disse Chrollo ao contrá-la.', 750, 3);"""
    )

    pericias = []
    passivas = [
        "d06ff7ac-cad1-49d6-be84-6eb290879dea",
        "f4e0b395-33f6-4ad2-97de-0a76bf42f968",
        "429de159-48f9-48ab-870a-850983c4be4b",
        "60e33837-6378-4ec9-9490-bcc094e15a00",
    ]
    talentos = []
    skills = [
        "a4a7564b-37ed-43f5-bc09-df897ef8e7de",
        "d2808e11-146c-49f1-a631-4d365472a303",
        "02c0f9f6-a880-496e-98c1-795f4b00c700",
        "00a33d61-0ab6-4637-89fd-ccffac04ab3e",
        "135b9b63-dec7-4378-b2a1-a2bfe1350869",
        "dbe7bcff-b5be-46a1-84e3-cbdf1a368283",
        "f76dc202-536c-47f6-a9e2-cccb400d9102",
    ]
    itens = [
        "abb1a0d3-d0ac-4bc1-960b-9defa7dadde6",
        "938f7ffe-b0ff-4824-97dd-9769ccd35aae",
    ]

    session.execute(
        f"""{INSERT_PERSONAGEM}
VALUES (30180fc6-30ba-4f65-a520-53e63bc4ec65, 'Shin NovaChrollo', 'Chrollo', {level}, 'Magitécnico', 'Combatente', 'Humano', 'Pomonas Cycle', 'Para Chrollo, o fim é necessário. Assim como a vida, todo ciclo tem um fim.', 0, {pe}, {pe}, 44, 44, 'hp', {reducao_de_dano}, {bonus_de_proficiencia}, [{", ".join(pericias)}], [{", ".join(talentos)}], [{", ".join(passivas)}], [{", ".join(skills)}], [{", ".join(forca)}], [{", ".join(destreza)}], [{", ".join(constituicao)}], [{", ".join(inteligencia)}], [{", ".join(sabedoria)}], [{", ".join(carisma)}], 5, [], [], [], [{", ".join(itens)}], [1, 1, 1], 15, 19, [], 250, 'chrollo.png', '<:chrollo_token:1384691822584135894>', '766039963736866828');"""
    )

    # -------------------------------------------------------------------------------------------

    # PROMPT JULIUS

    forca = ["11", "1"]
    destreza = ["13", "3"]
    constituicao = ["12", "2"]
    inteligencia = ["11", "1"]
    sabedoria = ["10", "0"]
    carisma = ["9", "-1"]

    reducao_de_dano = 4

    session.execute(
        f"""{INSERT_PASSIVA}       
VALUES (e4d7675d-3cb7-4395-8de0-5c4c17a8cc83, 'Ataque Especializado', 'Você aprendeu a se virar em combate usando astúcia e conhecimento com suas armas. Seus **ATAQUES** com **vantagem** que causam dano recebem a seguinte modificação:', 'reacao', 'ADICIONA', '**Acerto:** Você causa +{ataque_especializado} pontos de dano do mesmo tipo.\n**Especial:** Você só pode causar esse dano adicional uma vez por turno.', 0, 'PE');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (bb85504b-ff0b-4e3f-ae2c-5e0effb87f2b, 'Disparo com a Red Hunter', 0, 'acao', 'DISPARO, PERFURANTE, PRECISO, ARMA, ESPALHAFATOSO, ATAQUE', '18m.', 'Instantânea.', '1d20 + {int(destreza[1])} + {bonus_de_proficiencia} vs **DES**.', '2d8 + {bonus_de_proficiencia} + 2 pontos de dano.', 'Caso você erre no teste de acerto, você solta a **ARMA** e terá que gastar sua <:acao_bonus:1326585197004722197> Ação Bônus para pegá-la novamente.', 'O usuário aplica +1 nível de ***Shadow Cover***.', 'None', 'None', 'Uma criatura.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (8dea83d1-5beb-4c02-a29f-322205850046, 'Corte com a Masked Death', 0, 'acao', 'ATAQUE, ARMA, CORTANTE, VERSÁTIL, ALONGADA', '2m.', 'Instatânea.', '1d20 + {int(forca[1])} vs **DES**.', '1d8 + 1d10 + 2 pontos de dano **CORTANTE**', 'Caso você erre no teste de acerto, você solta a **ARMA** e terá que gastar sua <:acao_bonus:1326585197004722197> Ação Bônus para pegá-la novamente.', 'O usuário aplica +1 nível de ***Shadow Cover***.', 'None', 'None', 'Uma criatura.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (b7864548-2ebe-4823-a884-d1a6455d6a7f, 'Masked Death: Fools Blood', 1, 'acao', 'ATAQUE, ARMA, VERSÁTIL, NECRÓTICO, MÁGICO, ALONGADO', '3m.', 'Instântanea.', '1d20 + {int(forca[1])} + 2 vs **DES**', '2d8 + 1d10 + {int(forca[1])} + 2 de dano **NECRÓTICO**.', 'O encantamento acaba', 'None', 'O usuário precisa ativar o encantamento da espada para usar essa habilidade, usando sangue ou algumas gotas de uma poção de cura nela em uma <:acao_bonus:1326585197004722197> Ação Bônus.', 'O usuário aplica +1 nível de ***Shadow Cover***.', 'Criaturas em um raio de 2m.', '{bonus_de_proficiencia}', 'None', 'None', 'None', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (9079caad-0894-4b94-ad67-e977ff1c41e3, 'Mortalha Energizante', 0, 'reacao', 'HUMANO', 'Pessoal.', 'Instantânea.', 'None', 'None', 'None', 'Você recebe {bonus_de_proficiencia} pontos de ênfase temporários durante essa cena.', 'Você só pode usar essa habilidade uma vez por descanso.', 'Uma criatura na cena morre', 'None', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_PASSIVA}
VALUES (2290cf01-4a66-4fc1-8581-9e24d151509f, 'Tradição Oral', 'Você é capaz de reter uma quantidade infinita de informação, desde que ela tenha sido transmitida oralmente para outra criatura. Você tem **vantagem** em todos os testes de **INT** relacionados a lembrar de fatos ou informações. Caso tenha sucesso no teste, significa que já repassou essa informação para outra criatura.', 'None', 'None', '0', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_TALENTO}
VALUES (94c51d1e-c688-4185-9c62-3f1782fd4651, 'Resistir para Findar', 'Sua proximidade com A Morte fez com que você encontrasse formas de dar o fim. Seus **ATAQUES** recebem a seguinte modificação:', 'reacao', 'ADICIONA', '**Especial:** Você ignora todas as resistências do alvo nesse ataque.', 1, 'PE');"""
    )
    session.execute(
        f"""{INSERT_TALENTO}
VALUES (961e8d2d-c360-4751-9829-7786acf4e6aa, 'Se Dá Certo; Não é Estúpido; é Genial!', 'Diferente dos outros aventureiros, você é considerado proficiente com ataques improvisados, pode usar seus pontos de ênfase neles e causa o dobro dos dados de dano que causariam. Além disso, se a arma for um item pequeno (volume 1 ou menos), recebe o descritor **ARMA** e um descritor à sua escolha entre **ARREMESSÁVEL** ou **LEVE**; se for um item grande (volume 3 ou mais), precisa usá-lo com as duas mãos e ele recebe um descritor à sua escolha entre **ALONGADA** ou **ESPALHAFATOSA**. (Já adicionado na ficha)', 'None', 'None', '0', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_TALENTO}
VALUES (334434be-2ff3-4f94-8813-e1117a017b16, 'Trajado', 'Sempre que estiver vestindo uma armadura leve e não estiver empunhando um escudo, você aumenta a redução da sua armadura em +2. (Já adicionado na ficha)', 'None', 'None', '0', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (8dda14ea-561f-48e6-a55e-2706f348b39e, 'Cambalhota Especializada', 1, 'reacao', 'ESPECIALISTA', 'Pessoal.', 'Instantânea.', 'None', 'None', 'None', 'você fica ***Caído*** e recebe **resistência** contra o dano do ataque.', 'Caso tenha a habilidade *“Resistir com Unhas e Dentes”*, você recupera a sua <:reacao:1326585200519544885> reação', 'Você é acertado por um ataque que não tenha sido realizado com **vantagem**.', 'Você.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (de8f9988-529d-401e-9987-409fab27288a, 'Resistir com Unhas e Dentes', 1, 'reacao', 'ESPECIALISTA', 'Pessoal.', 'Instantâneo.', 'None', 'None', 'None', 'Jogue seu dado de *Ataque Especializado*. Você usa o resultado da jogada para aumentar sua redução contra o dano sofrido.', 'Você só pode usar essa habilidade uma vez por rodada.', 'Você sofre dano.', 'O usuário.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_PASSIVA}
VALUES (7bea74b6-bf1c-4d3d-807d-8498bc2987ba, 'Energia Negativa', 'Todos os seus **ATAQUES** com **ARMA** ou que causem dano **NECRÓTICO** causam +2 pontos de dano. Além disso, sempre que você ou uma de suas **CRIAÇÕES** causarem dano **NECRÓTICO** com um **ATAQUE**, o alvo fica ***Marcado*** ou aumenta essa condição em +1. Além disso, quando uma sombra sob seu controle for eliminado, a criatura que o eliminou recebe a condição ***Marcado***, ou aumenta essa condição em +1. Por fim, sempre que uma criatura ***Marcada*** em até 18m de você morrer, você pode transferir essa condição para você ou para uma sombra sob seu controle.', 'None', 'None', '0', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (685388af-e4d2-4f4f-8b16-029910c08ba6, 'Necromancia Aprimorada', 2, 'acao bonus', 'NECROMANTE, MÁGICO', '9m.', 'None', 'None', 'None', 'None', 'O usuário pode consumir qualquer número de marcas de criaturas para aprimorar qualquer número de sombras que você controle. Você escolhe como distribuir as melhorias por marca.', 'None', 'None', 'Uma sombra controlada pelo usuário.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_PASSIVA}
VALUES (2c09f75c-18ad-40af-bb7c-d3cc01132f42, 'Exército de Sombras', 'O usuário é capaz de invocar um echo sombrio e depois comandá-los em combate. A sombra passa a ser considerado uma **CRIAÇÃO** e não pode agir durante uma cena de combate. Sempre que você se deslocar, suas sombras podem se deslocar uma distância igual à que você deslocou-se. Você pode usar as habilidades *"Erga-se"*, *"Comandar Sombra"* e *"Necromancia Aprimorada"*.', 'None', 'None', '0', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (3fc48458-2834-4610-9337-f9017d5f7489, 'Mortalha Energizante', 0, 'reacao', 'HUMANO', 'Pessoal.', 'Instantânea.', 'None', 'None', 'None', 'Você recebe {bonus_de_proficiencia} pontos de ênfase temporários durante essa cena.', 'Você só pode usar essa habilidade uma vez por descanso.', 'Uma criatura na cena morre', 'None', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (d3c3086e-4324-4a3f-bf3b-135b8acded07, '"Erga-se"', 1, 'acao bonus', 'NECROMANTE, MÁGICO, CRIAÇÃO, SOMBRA', '6m.', 'Até ser destruído ou ser ordenado a voltar ao núcleo ou sombra.', 'None', 'None', 'None', 'Você invoca uma echo sombrio de sua posse.', 'None', 'None', 'Um espaço desocupado no alcance.', 'Ilimitado.', 'reacao', 'ADICIONA', '**Efeito**: você usa a habilidade *"Comandar Sombra"* como <:acao_livre:1326585198892154901> Ação Livre para comandar uma sombra dentro do alcance (podendo ser inclusive um recém invocado).', 2, 'PE');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (e6189aac-5dda-49a7-9d39-d5b7927e5a82, 'Comandar Sombra', 1, 'acao bonus', 'NECROMANTE, MÁGICO, SOMBRA', '9m,', 'Instantânea.', 'None', 'None', 'None', 'Você comanda uma sombra a realisar uma habilidade.', 'None', 'None', 'Uma sombra comandada por você.', 'Ilimitado.', 'reacao', 'ADICIONA', '**Alvo:** Você afeta mais um reanimado controlado por você. É possível aplicar essa modificação mais de uma vez.', 1, 'PE');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (64e4a387-ac93-4146-957f-f38c3f6b6e10, 'Receber Benção', 2, 'acao livre', 'ESPECIALISTA', 'Pessoal.', 'Até o próximo descanso longo.', 'None', 'None', 'None', 'O usuário ativa todas suas benções.', 'O usuário só pode usar essa habilidade no final de uma Cena de Descanso e somente uma vez por cena.', 'None', 'O usuário.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (43d8755b-a5f4-4c4d-8aa5-ee3e235b80a1, 'Alimentos das Chamas', 2, 'acao', 'BENÇÃO, MÁGICO', 'Visão.', 'Instântanea.', 'Mágico vs **CAR**.', 'O usuário descobre o que aquela criatura mais deseja (naquela cena).', 'O usuário só pode usar essa habilidade se tiver usado a habilidade "*Receber Benção"*', 'Nenhuma outra personagem ou criatura sabe que você usou essa habilidade.', 'None', 'None', 'Uma criatura.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (e314977f-8d03-4eba-9b24-9778b689331b, 'Engolfar em Chamas da Vingança', 1, 'acao bonus', 'BENÇÃO, MÁGICO, ÍGNEO', 'Pessoal.', 'Até o fim da próxima cena.', 'None', 'None', 'None', 'Todo o dano que você causar passa a ser **ÍGNEO**.', 'O usuário só pode usar essa habilidade se tiver usado a habilidade *"Receber Benção"*', 'None', 'Você.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_ITEM}
VALUES (d24b8e11-6d39-4228-8211-55f2458fb72c, 'Masked Death', 'Uma espada longa com o encantamento *"Fools Blood"*. A espada é bem trabalhada e possui a inscrição "Masked Death" em sua lâmina, que faz referência à banda de seu antigo portador, Zombie. O encantamento precisa de um pouco de sangue ou algumas gotas de poção de cura para ativar suas cargas, depois da ativação a espdada fica vermelha e pode usar a habilidade *"Masked Death: Fools Blood"*.', 500, 2);"""
    )
    session.execute(
        f"""{INSERT_ITEM}
VALUES (52056c6a-5200-4d16-8ecc-cde1ba3e5cd2, 'Red Hunter', 'Um grande rifre vermelho com detalhes pretos criado apatir da imaginação de seu portador. "Isso me lembra a sniper do Cypher" — disse Chrollo durante o acampamento na Black Rose Forest', 750, 2);"""
    )
    session.execute(
        f"""{INSERT_ITEM}
VALUES (0beb39c2-123a-4d40-b2eb-e011b55028fb, 'Armadura de Couro Batido', 'Proteção comum entre mercenários e aventureiros inexperientes, reforçada com pequenas placas de couro em locais estratégicos.', 40, 3);"""
    )
    session.execute(
        f"""{INSERT_ITEM}
VALUES (c4ae1cca-557b-44ed-977a-7231d4783d36, 'Núcleo Pesado de Fenrir', 'O núcleo marcado que abriga a alma de um grande lobo que viveu nas terras gélidas dos elfos do inverno, Jotunheim. Ele lutou até seu último dia para tentar alimentar e proteger sua matilha, perdendo toda sua sombra batalhando contra feras cada vez maiores.\nAté que em um dia, trouxe o maior banquete que a matilha já havia visto, mas aquele seria o último. Sua pelagem antes branca como a neve, estava banhada em sangue, seu próprio sangue.\nAlém daqueles que Fenrir lutava para proteger, junto dele estava aquela com quem ele muito negociava em seus "últimos momentos"...', 0, 3);"""
    )
    session.execute(
        f"""{INSERT_ITEM}
VALUES (7fd8f8ef-19d4-4556-a6ba-058bd51e86b4, 'Núcleo Pesado de Ashborn', 'O núcleo que abriga a alma do ex-guardião do Darkhold I. Antes, um grande guerreiro que antes servia a rainha e hoje serve a um peão.', 0, 3);"""
    )
    session.execute(
        f"""{INSERT_ITEM}
VALUES (53a9956b-a1e0-44fc-8d8d-6463afbf3339, 'Tabuleta Sombria', 'Após o grupo sair do domínio de Shadow e voltar à Opath, a mana que antes tomava conta da sala, foi de um estado sólido ao líquido de repente, escorrendo pelas paredes até se reunir uma tabuleta no centro da mesma. A tabuleta possui runas arcanas gravadas por todo seu corpo "ᛏᚼᛄ ᚴᛁᛏᚷᚦᛄᛚ ᚤᚠ ᚷ ᛏᚼᚤᚢᛋᚷᚾᚦ ᚱᚤᚤᛘᛋ".', 0, 2 );"""
    )
    session.execute(
        f"""{INSERT_PASSIVA}
VALUES (3764ae33-efde-4191-92c2-d5455c4394e1, 'Hidden Inventory', 'Você é capaz de guardar um item de qualquer volume em sua sombra. Dentro da sombra, o item não pode ser roubado e pode ser colocado ou retirado da sombra com a habilidade *"Hidden Inventory: Solidificar Sombra"*', 'None', 'None', '0', 0, 'None');"""
    )
    session.execute(
        f"""{INSERT_SKILL}
VALUES (a714ddcb-d917-4bc1-a179-97e27661b8f3, 'Hidden Inventory: Solidificar Sombra', 0, 'acao livre', 'MÁGICO, SOMBRIO', 'Pessoal.', 'Instantânea.', 'None', 'None', 'None', 'Ao usar parte da mana da Shadow em sua sombra, ela solidifica e você pode guardar um item dentro dela. Use essa habilidade para guardar um item ou tirá-lo de sua sombra.', 'None', 'None', 'Sua sombra.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    )

    pericias = [
        "c25f6a18-6b01-423a-9c44-1781f677137d",
        "1030947f-9e65-476a-b08c-c834a2ddfe7f",
        "a052505a-add0-4717-9d30-e382a0741058",
        "3bc86566-ec94-4459-a7fc-2a5d094a1f39",
        "d28b4723-1177-46ac-b1f2-bf785330b1a9",
        "c57e4a9b-2e9d-4c97-9f6c-0139cd0ddb44",
    ]
    passivas = [
        "e4d7675d-3cb7-4395-8de0-5c4c17a8cc83",
        "2290cf01-4a66-4fc1-8581-9e24d151509f",
        "7bea74b6-bf1c-4d3d-807d-8498bc2987ba",
        "2c09f75c-18ad-40af-bb7c-d3cc01132f42",
        "3764ae33-efde-4191-92c2-d5455c4394e1",
    ]
    talentos = [
        "94c51d1e-c688-4185-9c62-3f1782fd4651",
        "961e8d2d-c360-4751-9829-7786acf4e6aa",
        "334434be-2ff3-4f94-8813-e1117a017b16",
    ]
    skills = [
        "8dda14ea-561f-48e6-a55e-2706f348b39e",
        "bb85504b-ff0b-4e3f-ae2c-5e0effb87f2b",
        "de8f9988-529d-401e-9987-409fab27288a",
        "8dea83d1-5beb-4c02-a29f-322205850046",
        "b7864548-2ebe-4823-a884-d1a6455d6a7f",
        "685388af-e4d2-4f4f-8b16-029910c08ba6",
        "d3c3086e-4324-4a3f-bf3b-135b8acded07",
        "e6189aac-5dda-49a7-9d39-d5b7927e5a82",
        "a714ddcb-d917-4bc1-a179-97e27661b8f3",
        "64e4a387-ac93-4146-957f-f38c3f6b6e10",
        "e314977f-8d03-4eba-9b24-9778b689331b",
        "43d8755b-a5f4-4c4d-8aa5-ee3e235b80a1",
        "3fc48458-2834-4610-9337-f9017d5f7489",
    ]
    itens = [
        "0beb39c2-123a-4d40-b2eb-e011b55028fb",
        "d24b8e11-6d39-4228-8211-55f2458fb72c",
        "52056c6a-5200-4d16-8ecc-cde1ba3e5cd2",
        "c4ae1cca-557b-44ed-977a-7231d4783d36",
        "7fd8f8ef-19d4-4556-a6ba-058bd51e86b4",
        "53a9956b-a1e0-44fc-8d8d-6463afbf3339",
    ]

    session.execute(
        f"""{INSERT_PERSONAGEM}
VALUES (69fa11c2-ca6a-44b7-93c2-b744d0e98554, 'Julius Wick', 'Julius', {level}, 'Necromante das Sombras', 'Especialista', 'Humano', 'Pomonas Cycle', 'Para Julius, o fim é necessário. Assim como a vida, todo ciclo tem um fim.', 0, {pe}, {pe}, 38, 38, 'hp', {reducao_de_dano}, {bonus_de_proficiencia}, [{", ".join(pericias)}], [{", ".join(talentos)}], [{", ".join(passivas)}], [{", ".join(skills)}], [{", ".join(forca)}], [{", ".join(destreza)}], [{", ".join(constituicao)}], [{", ".join(inteligencia)}], [{", ".join(sabedoria)}], [{", ".join(carisma)}], 5, [], [], [], [{", ".join(itens)}], [1, 1, 1, 1, 1, 1], 15, 19, [], 250, 'julius.png', '<:julius_token:1384691827654918268>', '921158705075077150');"""
    )
    print("JULIUS ADICIONADO")

    # --------------------------------------------------------------------------------------------

    # PROMPT ADAM

    #     session.execute(
    #         f"""{INSERT_PASSIVA}
    # VALUES (aeadbead-f668-46be-9469-b2eecff9cf16, 'Ataque Poderoso', 'Você treinou seu corpo para ser capaz de desferir ataques poderosíssimos sempre que ataca. Seus **ATAQUES** com **ARMAS** recebem a seguinte modificação:', 'reacao', 'AMPLIAR + 15', '**Acerto:** você causa +1d8 pontos de dano do mesmo tipo.', 0, 'PE');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (04df13c9-c079-4d4d-b7a7-6b5264a59114, 'Ataque de Superioridade', 0, 'acao', 'ATAQUE', '3m.', 'Instantânea.', 'FOR vs FOR', 'Você deve escolher um efeito entre: Deixar o alvo ***Caído***; Pegar um item do alvo; Deixar o alvo ***Agarrado***.', 'None', 'None', 'Você só pode usar essa habilidade em criaturas de seu tamanho ou menor.', 'None', 'Uma criatura.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (e7a3b8d2-4f5c-4d91-90b0-3a8e6f9c7d2f, 'Ataque com o Martelo de Guerra', 0, 'acao', 'ATAQUE, CONTUNDENTE, PESADO', '8m.', 'Instatânea.', '1d20 + Bônus de FOR.', '1d16 + Bônus de FOR', 'Caso você erre no teste de acerto, você solta a **ARMA** e terá que gastar sua <:acao_bonus:1326585197004722197> ação bônus para pegá-la novamente.', 'None', 'None', 'None', 'Uma criatura.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (f3b9a7c1-2d8e-4f6a-bc21-7e9d5a1d8e54, 'Soco Desarmado', 0, 'acao', 'ARMA, ATAQUE, CONTUNDENTE, LEVE', '3m.', 'Instatânea.', '1d20 + Bônus de FOR.', '1d8 + Bônus de FOR', 'None', 'None', 'None', 'None', 'Uma criatura.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (b2a9d7f3-8e4d-6c1d-bc71-3e9f7a5d8e54, 'Soco com Manopla', 0, 'acao', 'ARMA, ATAQUE, CONTUNDENTE, PESADO', '5m.', 'Instatânea.', '1d20 + Bônus de FOR.', '1d10 + Bônus de FOR + 2', 'None', 'None', 'Essa habilidade só pode ser usada se o usário tiver usado "*Modificar com Sangue: Conjurar Manoplas"* antes.', 'None', 'Uma criatura.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (3cabe054-e4e3-4a6a-9158-965cf976d10f, 'Rápido como um Raio', 0, 'reacao', 'PUGILISTA', 'Pessoal.', 'None', 'None', 'None', 'None', 'Realiza um _“Ataque corpo a corpo”_  adicional com seu ataque desarmado como uma <:acao_livre:1326585198892154901> ação livre contra uma criatura dentro do seu alcance.', 'Só é possível realizar esse ataque extra uma quantidade de vezes por rodada igual ao seu **bônus de proficiência** e seu custo aumenta em 1 ponto de ênfase para cada vez que for utilizado na mesma rodada.', 'O usuário faz um _“Ataque corpo a corpo”_ como **ATAQUE**', 'None', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_PASSIVA}
    # VALUES (14bcc54c-e187-4954-abd2-785b01d93e33, 'Combate Desarmado', 'Você torna-se proficiente em um tipo especial de ataques desarmados. Enquanto estiver com pelo menos uma mão livre, seus ataques desarmados recebem os descritores  **ARMA**, **CONTUNDENTE** e **LEVE** e causam 1d6 pontos de dano. Você considera que está empunhando seu ataque desarmado e ele recebe o descritor **ARMA** se estiver com pelo menos uma mão livre.', 'None', 'None', '0', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_PASSIVA}
    # VALUES (de754406-5a1b-4889-ae1b-229f7461b919, 'Façanha Desarmada', 'Você sabe golpear de maneira veloz, atacando com manobras perigosas. Seus ataques desarmados recebem a seguinte modificação:', 'reacao', 'ADICIONA', '**Acerto:** após acertar o **ATAQUE**, você pode fazer um "*Ataque de Superioridade"* como <:acao_livre:1326585198892154901> ação livre.', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_TALENTO}
    # VALUES (3a51e8cf-92b1-43f6-9876-f93a4d7e57f1, 'Presas de Warpinier', 'Seu sangue maldito fez com que suas presas se tornassem verdadeiras armas, que podem ser usadas em momentos de adrenalina. Seus **ATAQUES** com o descritor **ARMA** recebem a seguinte modificação:', 'reacao', 'ADICIONA', '**Acerto:** +1d6 pontos de dano **PERFURANTE** e você recebe todos benefícios da característica "*Sangue Maldito"*, mas o alvo não fica com **desvantagem** em testes.', 2, 'PE');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (4cd48055-f7db-4211-9280-5f973711b24a, 'Liderar por Exemplo', 1, 'acao bonus', 'ORC, INSPIRAÇÃO, VOZ', '20m.', '2 turnos.', 'None', 'None', 'None', 'Escolha um atributo. O alvo fica ***Inspirado***. Enquanto estiver ***Inspirado***, ele recebe vantagem sempre que realizar um teste com o atributo.', 'None', 'None', 'Criaturas a sua escolha.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_PASSIVA}
    # VALUES (7986f0dc-c082-4906-838a-36d991dad853, 'Cólera Ardente', 'Seu sangue quente é capaz de servir como combustível para sua ira controlada. Enquanto estiver ***Machucado***, seus **ATAQUES** recebem a seguinte modificação:', 'reacao', 'ADICIONA', '**Acerto:** Além do normal, você causa +1d6 pontos de dano.\n**Especial:** A partir do 5º nível, você pode aplicar essa modificação quantas vezes quiser.', 1, 'PE');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_PASSIVA}
    # VALUES (3f9c1b74-8d2e-4a56-bb1c-2e7f5d8a90e3, 'Sangue Maldito', 'Seu sangue impregnado com a essência de Warpinier concede alguns privilégios. O usuário tem **resistência** a dano **ÁCIDO** e **NECRÓTICO**. Além disso, o usuário recebe a habilidade "*Sede de sangue"*.', 'None', 'None', '0', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (a7d5f3c2-9b8e-4d6a-bc21-3e9f7a1d8e54, 'Modificar com Sangue', 1, 'acao bonus', 'SANGUIR', 'Toque.', 'Uma cena.', 'None', 'None', 'None', 'O equipamento afetado recebe um descritor de equipamento a sua escolha.', 'Você só pode usar essa habilidade uma  vez por cena.', 'None', 'Uma arma.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (27135a3f-ffe8-447a-a810-9aa424b1196c, 'Modificar com Sangue: Conjurar Manoplas', 0, 'acao livre', 'SANGUIR, ARMA, MÁGICO', 'Pessoal.', 'Uma cena.', 'None', 'None', 'None', 'O usuário conjura suas manoplas se sangue.', 'None', 'None', 'None', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (9c521e05-28b3-43ee-9e74-c912ae77b6ff, 'Echo of Pomona: Mashing Impact', 4, 'eop', 'EOP, VOZ', '2m.', 'No mínimo 3 turnos.', 'None', 'None', 'None', 'Adam fica em um estado de ***Concentração Extrema*** por no mínimo três turnos. Após o fim desse tempo, deve ser feito um teste no começo de cada rodada para determinar se o efeito continuará naquele turno.', 'None', 'None', 'Uma criatura.', '1', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_TALENTO}
    # VALUES (65f11dac-d301-4f22-ad47-d9624e817a54, 'Renegociar', 'Para tudo existe um jeitinho, incluindo negociações. Você tem **vantagem** em testes de **CAR**.', 'None', 'None', '0', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_ITEM}
    # VALUES (f151bcbc-7fba-49f1-8ce9-90518c919078, 'Martelo de Guerra de Ferro Varmaniano', 'Um grande martelo de guerra pesado e contundente feito com ferro varmaniano, ideal para destruição. "Slk Adam, coitado do meninux, ficou parecendo o Perna Longa amassado, mas com um pouquinho a mais de gore..." — Disse Chrollo no final da batalha do Quebra-copos.', 322, 5);"""
    #     )
    #     session.execute(
    #         """INSERT INTO xmercury.personagens (id, nome, nickname, level, path, classe, legacy, heritage, melancholy, catarse, pe, pe_atual, hp, hp_atual, hp_tipo, reducao_de_dano, bonus_de_proficiencia, pericias, talentos, passivas, skills, forca, dexterity, constituicao, inteligencia, sabedoria, carisma, pontos_de_sombra, resistencia, vulnerabilidade, imunidade, inventario_itens, inventario_numero, volume_atual, limite_de_volumes, condicoes, saldo, imagem, token, usuario)
    # VALUES (1c773acd-295b-436d-b792-8011e739e527, 'Adam Andrews', 'Adam', 4, 'Pugilista', 'Combatente', 'Orc Sanguir', 'Griphon', 'Você é cria da Fúria, a deusa engolfada em chamas. Por vezes, seu temperamento poderá traí-lo, fazendo com que seja tomado pelo mesmo fogo que consome tudo à sua volta.', 2, 12, 38, 2, 2, [], [65f11dac-d301-4f22-ad47-d9624e817a54], [aeadbead-f668-46be-9469-b2eecff9cf16, 14bcc54c-e187-4954-abd2-785b01d93e33, de754406-5a1b-4889-ae1b-229f7461b919, 3f9c1b74-8d2e-4a56-bb1c-2e7f5d8a90e3], [04df13c9-c079-4d4d-b7a7-6b5264a59114, e7a3b8d2-4f5c-4d91-90b0-3a8e6f9c7d2f, f3b9a7c1-2d8e-4f6a-bc21-7e9d5a1d8e54, b2a9d7f3-8e4d-6c1d-bc71-3e9f7a5d8e54, 3cabe054-e4e3-4a6a-9158-965cf976d10f, 4cd48055-f7db-4211-9280-5f973711b24a, a7d5f3c2-9b8e-4d6a-bc21-3e9f7a1d8e54, 27135a3f-ffe8-447a-a810-9aa424b1196c], [12, 2], [11, 1], [13, 3], [11, 1], [11, 1], [9, -1], 5, ['ÁCIDO', 'NECRÓTICO'], [], [], [0beb39c2-123a-4d40-b2eb-e011b55028fb, f151bcbc-7fba-49f1-8ce9-90518c919078], [1, 1], [], 100, 'adam.png', '1239326132327944313');"""
    #     )
    #     print("ADAM ADICIONADO")

    #     # --------------------------------------------------------------------------------------------

    #     # PROMPT GUNTHER

    #     session.execute(
    #         f"""{INSERT_PASSIVA}
    # VALUES (5bc5ecad-03dd-4e0d-abfe-5fa8bbb80771, 'Ataque Especializado', 'Você aprendeu a se virar em combate usando astúcia e conhecimento com suas armas. Seus **ATAQUES** com **vantagem** que causam dano recebem a seguinte modificação:', 'reacao', 'ADICIONA', '**Acerto:**  Você causa +1d6 pontos de dano do mesmo tipo.\n**Especial:** Você só pode causar esse dano adicional uma vez por turno.', 0, 'PE');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (12cccd1a-79fa-44ac-be51-e2c8ea5c22a3, 'Corte com a Foice e Corrente', 0, 'acao', 'LEVE, ARREMESÁVEL, ATAQUE, CORTANTE, VERSÁTIL, SUPERIOR', '6m.', 'Instatânea.', '1d20 + Bônus de FOR vs FOR.', '1d6 + Bônus de FOR', 'Caso você erre no teste de acerto, você solta a **ARMA** e terá que gastar sua <:acao_bonus:1326585197004722197> Ação Bônus para pegá-la novamente.', 'None', 'None', 'None', 'Uma criatura.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (f53836e1-914b-4ca1-b713-cecd9d518e06, 'Infligir Ferimentos', 1, 'acao', 'SUPERFICIAL, OFENSIVO, ATAQUE, MÁGICO, NECRÓTICO', 'Alcance.', 'Instântanea.', 'Mágico vs CON.', '3d10 pontos de dano **NECRÓTICO**.', 'O alvo sofre metade do dano.', 'None', 'None', 'None', 'Uma criatura.', 'Ilimitado.', 'reacao', 'ADICIONA', '**Acerto:** Aumenta o dano adicional em +2d10. Você pode aplicar essa modificação quantas vezes quiser', 2, 'PE');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (d9f9dab4-913f-416c-9cf6-3690ba853f05, 'Disparo Arcano', 0, 'acao', 'TRUQUE, OFENSIVO, ATAQUE, MÁGICO, ENERGÉTICO', '18m.', 'Instantânea.', 'Mágico vs **FOR**.', 'O alvo sofre 1d10 pontos de dano do tipo **ENERGÉTICO**.', 'None', 'None', 'Você pode lançar um disparo adicional logo após lançar o primeiro, como parte da mesma ação. É necessário repetir o teste de ataque e é permitido escolher um novo alvo.', 'None', 'Uma criatura.', 'Ilimitado.', 'reacao', 'ADICIONA', '**Acerto:** O alvo é empurrado 3m ou tem seu deslocamento reduzido em 3m até o final de seu próximo turno.', 1, 'PC');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (9b195835-4b3b-4d07-9a80-fa4497b61676, 'Convocar Lumine', 1, 'acao', 'TRUQUE, UTILITÁRIO, MÁGICA, CRIAÇÃO', '9m.', 'Uma cena.', 'None', 'None', 'None', 'Lumine usa seu chapéu para voltar para o plano material. Do chapéu, surge algumas patinhas, garras e um pequeno olho brilhante. Ela permanece pela duração da magia ou até quando ela queira ir embora. Você pode usar sua ação para pedir que ela faça algo, podendo interagir com itens e com o ambiente. Ela pode se distânciar de você em até 9m.ß', 'Ela não pode atacar, ativar itens mágicos ou carregar mais de 5 volumes. Além disso, ela  desaparece se ficar a mais de 9m do conjurador ou se você conjurar a magia novamente.', 'None', 'Ponto no alcance.', 'Ilimitado.', 'reacao', 'ADICIONA', '**Especial:** Ela é _**Invisível**_ a ouitras criaturas que não sejam você.', 1, 'PE')"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (59951d9d-3c3e-496b-9491-e7b7554c04ef, 'Transmutar Pacto em Arma', 2, 'acao', 'PACTUADO, MÁGICO', 'Toque.', 'Uma cena.', 'None', 'None', 'None', 'Você canaliza a força de Lumine no objeto. Ele se transforma numa arma que você seja proficiente e você pode usar seu **atributo chave de conjuração**, em vez de **FOR** ou **DES**, para as jogadas de ataque e dano com ela.', 'None', 'None', 'Um objeto mundano que você esteja empunhando.', 'Ilimitado.', 'reacao', 'ADICIONA', '**Efeito:** Você pode dever mais uma obrigação menor para receber vantagem no primeiro ataque que fizer com a arma na cena.', 0, 'PE');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_PASSIVA}
    # VALUES (45c0cd6c-13e5-48fd-af3e-9bd8e98c564f, 'Sangue Maldito', 'Seu sangue impregnado com a essência de Warpinier concede alguns privilégios. O usuário tem **resistência** a dano **ÁCIDO** e **NECRÓTICO**. Além disso, o usuário recebe a habilidade "*Sede de sangue"*.', 'None', 'None', '0', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (cd6acb0f-d656-429b-acf2-4987a61d00dc, 'Modificar com Sangue', 1, 'acao bonus', 'SANGUIR', 'Toque.', 'Uma cena.', 'None', 'None', 'None', 'O equipamento afetado recebe um descritor de equipamento a sua escolha.', 'Você só pode usar essa habilidade uma  vez por cena.', 'None', 'Uma arma.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (88a87ee1-e31f-4985-914e-a040408cf8af, 'Sede de sangue', 0, 'acao bonus', 'SANGUIR', 'Toque.', 'Instântanea.', '1d20 + STR vs FOR', 'None', 'None', 'O usuário morde o alvo no pescoço, infectando-o com a essência de Warpinier, o alvo fica com desvantagens em todos os testes por 24 horas. Além disso, o usuário restaura 5 pontos de HP temporários e pode escolher uma doença, um veneno ou uma  condição (entre _**Atordoado**_, _**Desorientado**_, _**Encantado**_, _**Envenenado**_ ou _**Paralisado**_) que esteja afetando o usuário. Você encerra seu efeito.', 'None', 'None', 'Uma criatura humanoide.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (ccbeb133-a5d9-4ad0-a4d9-00a29b2a6998, 'Alimentos das Chamas', 2, 'acao', 'BENÇÃO, MÁGICO', 'Visão.', 'Instântanea.', 'Mágico vs **CAR**.', 'O usuário descobre o que aquela criatura mais deseja (naquela cena).', 'O usuário só pode usar essa habilidade se tiver usado a habilidade "*Receber Benção"*', 'Nenhuma outra personagem ou criatura sabe que você usou essa habilidade.', 'None', 'None', 'Uma criatura.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         """INSERT INTO xmercury.passivas (id, nome, descricao, modificador_execucao, modif icador_nome, modificador_descricao, modificador_gasto, modificador_gasto_tipo)
    # VALUES (66eed95f-1301-4121-a334-1526177cc8c5, 'Adequar-se ao Meio', 'Após usar a habilidade "*Receber Benção"*,o usuário recebe vantagem em todos os testes que envolvam esconder-se ou misturar-se a multidões.', 'None', 'None', '0', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_TALENTO}
    # VALUES (d34c41e1-2f59-4fb9-9429-7dd122e62b19, 'Crítico Forçado', 'Ao acertar um **ATAQUE**, você pode dever um favor maior para fazer com que esse acerto conte como um acerto crítico. Esse talento só pode ser usado uma vez por dia.', 'None', 'None', '0', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (e7c94b4a-28cb-4a44-956b-1c7ebcf1a0a0, 'Morganas Deathmetal: Sigilo', 1, 'acao', 'ATAQUE, CORTANTE, PESADO, MÁGICO, ARMA', '6m.', 'Instântanea.', '1d20 + Bônus de FOR.', '2d6 + 1d6 de dano escolhido de dano. ', 'A espada cai', 'None', 'Se o usuário estiver ***Machucado***, ele ganha +1 em testes de ataque.\nO usuário deve escolher o tipo de dano (ígneo, frio, ácido ou elétrico) com uma <:acao_bonus:1326585197004722197> ação bônus com antecedência', 'None', 'Criaturas em um raio de 2m.', '{bonus_de_proficiencia}', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (10d0b1df-e399-4d2f-bd8f-01e0f1ad6b89, 'Corte com Morganas Deathmetal', 0, 'acao', 'ATAQUE, CORTANTE, PESADO, ARMA', '6m.', 'Instântanea.', '1d20 + Bônus de FOR.', '2d6 de pontos de dano.', 'A espada cai', 'None', 'Se o usuário estiver ***Machucado***, ele ganha +1 em testes de ataque.', 'None', 'Uma criatura', '2', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_ITEM}
    # VALUES (e6fa95b9-b04c-4f40-88e0-195a0488f0de, 'Foice e corrente', 'Combinação da fo ice ligada a corrente, para ataque versáteis. "Como essa corrente voltou para você depois que o Tristane desamarrou o Clebim?" — Disse Chrollo, questinando a ordem dos fatos durante a batalha contra Warpinier.', 25, 3);"""
    #     )
    #     session.execute(
    #         f"""{INSERT_ITEM}
    # VALUES (9b8e370b-29f3-470f-bd50-e52f8719f76a, 'Morganas Deathmetal', 'Uma espada feita com os restos da antiga guitarra de Morgana. "No dia que você fizer mais de 6 kills com ela a gente conversa..." — Disse Chrollo, concretizando a superioriodade da Masked Death', 350, 3);"""
    #     )
    #     session.execute(
    #         f"""{INSERT_ITEM}
    # VALUES (92dd4242-217d-495c-b761-6d097fd464ec, 'Núcleo leve de Lobo de Sombras', 'Após a morte de Fenrir, os outros lobos da matilha seguiram seus passos, trocaram suas sombras por mais alguns dias de vida. Dia após dia, um lobo caia. Queda após queda, a dama das sombras coletava suas almas.', 0, 2);"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (309f9471-f79c-41b6-a6dc-ad3b02ab3155, 'Presença de Lumine', 0, 'acao bonus', 'PACTUADO, MÁGICO', 'Pessoal.', 'Instantânea.', 'None', 'None', 'Caso algum teste com Lumine de um erro crítico (1), ela não falará com você até o começo da próxima rodada.', 'Através dos símbolos em suas mãos, você possui conexão com Lumine, uma entidade poderosa. Caso você agrade Lumine, poderá pedir favores à ela; podendo pedir itens, pontos de ênfase, pontos de catarse, pontos de vida, etc:\n\nFavores pequenos -> itens básicos, pontos de vida (1d6), informação básica da cena. (todas essas recompensas são apenas para o usuário):\n- Entregar um item básico (Lumine pode aceitar ou não dependendo do item ou da quantidade).\n- Eliminar um inimigo ({vida do inimigo} >= 35)\n- Fazer uma ação honrável\n...\n\nFavores maiores ->  item raro, pontos de vida(2d4 + 2), pontos de catarse(1d3), pontos de ênfase(1d4), informação importante da cena. (todos essas recompensas podem ser para qualquer pessoa da equipe)\n- Entregar um item raro/importante/valioso (Lumine pode aceitar ou não dependendo do item ou da quantidade)\n- Eliminar um inimigo ({vida do inimigo} <= 35)\n - Passar um dia com um combate sem tomar dano\n- Fazer Lumine rir. Para fazer esse favor existe dois meios: O usuário pode contar uma piada ao mestre, se o mestre achar engraçado, o usuário pode pedir sua recompensa; O usuário faz um teste de 1d20 + bônus de **CAR** (podendo usar catarse ou buffs), se o resultado for maior ou igual a 16, o usuário pode pedir sua recompensa.', 'O jogador pode tentar negociar outro favores com o mestre. Caso as duas mãos do usuários sejam danificadas de forma extrema ou coberta com algo espeço, a conexão com Lumine pode ser perdida. Mas caso apenas uma das mãos seja danificada, o usuário fica com **desvantagem** nos testes da habilidade.', 'None', 'None', '4', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         """INSERT INTO xmercury.personagens (id, nome, nickname, level, path, classe, legacy, heritage, melancholy, catarse, pe, pe_atual, hp hp_atual, reducao_de_dano, bonus_de_proficiencia, pericias, talentos, passivas, skills, forca, dexterity, constituicao, inteligencia, sabedoria, carisma, pontos_de_sombra, resistencia, vulnerabilidade, imunidade, inventario_itens, inventario_numero, volume_atual, limite_de_volumes, condicoes, saldo, imagem, usuario)
    # VALUES (e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8, 'Gunther Nosferata', 'Gunther', 4, 'Pactudo', 'Especialista', 'Sanguir', 'Byotir', 'Você precisa ser convidado para entrar em qualquer propriedade que não lhe pertença, a menos que tenha deixado algum objeto pessoal seu lá dentro, sob o cuidado de outra pessoa do local.', 1, 12, 36, 2, 2, [7b32de93-92b1-402a-93fe-c7a295535490, 98f70eea-9c31-44a4-8c66-2b1eca1a530a, d28b4723-1177-46ac-b1f2-bf785330b1a9, 50e3508e-335c-42ef-97cf-1db7a07962c4, e95b8d53-07d4-47bf-9d99-e23368c2dcba, 0222604e-cd4d-4077-b19f-7eb7c4e8c927], [d34c41e1-2f59-4fb9-9429-7dd122e62b19], [45c0cd6c-13e5-48fd-af3e-9bd8e98c564f, 66eed95f-1301-4121-a334-1526177cc8c5], [12cccd1a-79fa-44ac-be51-e2c8ea5c22a3, f53836e1-914b-4ca1-b713-cecd9d518e06, d9f9dab4-913f-416c-9cf6-3690ba853f05, 9b195835-4b3b-4d07-9a80-fa4497b61676, 59951d9d-3c3e-496b-9491-e7b7554c04ef, cd6acb0f-d656-429b-acf2-4987a61d00dc, 88a87ee1-e31f-4985-914e-a040408cf8af, ccbeb133-a5d9-4ad0-a4d9-00a29b2a6998, e7c94b4a-28cb-4a44-956b-1c7ebcf1a0a0, 10d0b1df-e399-4d2f-bd8f-01e0f1ad6b89], [10, 0], [12, 2], [13, 3], [9, -1], [11, 1], [11, 1], 5, ['ÁCIDO', 'NECRÓTICO'], [], [], [e6fa95b9-b04c-4f40-88e0-195a0488f0de, 9b8e370b-29f3-470f-bd50-e52f8719f76a, 5f219452-0438-40e4-ba90-d28ff16144c9, 92dd4242-217d-495c-b761-6d097fd464ec, 0beb39c2-123a-4d40-b2eb-e011b55028fb], [1, 1, 1, 2, 2], [], 960, 'gunther.png', '813254664241414144');"""
    #     )
    #     print("GUNTHER ADICIONADO")

    #     # --------------------------------------------------------------------------------------------

    #     # PROMPT DO VINCENZO

    #     session.execute(
    #         f"""{INSERT_PASSIVA}
    # VALUES (7e7976f6-2e0e-4aea-9f1e-a67f064ca22d, 'Ataque Especializado', 'Você aprendeu a se virar em combate usando astúcia e conhecimento com suas armas. Seus **ATAQUES** com **vantagem** que causam dano recebem a seguinte modificação:', 'reacao', 'ADICIONA', '**Acerto:**  Você causa +1d6 pontos de dano do mesmo tipo.\n**Especial:** Você só pode causar esse dano adicional uma vez por turno.', 0, 'PE');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (f5d276df-a425-4a0f-bf78-2c404dd3a9b7, 'Invocar Companheiro Animal', 0, 'acao livre', 'MESTRE DAS FERAS', 'Pessoal.', 'Instantânea.', 'None', 'None', 'None', 'Você invoca seu companheiro animal A criatura passa a ser considerada uma **CRIAÇÃO** e não pode agir durante uma cena de combate. Sempre que você  se deslocar, seu companheiro pode se deslocar uma distância igual à que você deslocou-se. Seu companheiro animal recebe cargas de vida adicio nais igual ao seu **bônus de prociência** e quando suas  cargas são reduzidas a 0 ou menos ele foge do  combate.', 'Ele pode ser invocado com a forma de um criatura específica, escolha entre: Alpaca, Cavalo, Capivara, Gaviáo Gigante, Jacaré Salgado, Libélula Gigante e Onça. Essa habilidade só pode ser usada uma vez por dia', 'None', 'None', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (9cde6c1c-a4cc-4d37-bf30-9a50d7be39ed, 'Transfigurar Companheiro Animal', 1, 'acao livre', 'MESTRE DAS FERAS', 'Pessoal.', 'Instantânea,', 'None', 'None', 'None', 'Seu companheiro animal toma a forma de outro ser, podendo variar entre: Alpaca, Cavalo, Capivara, Gaviáo Gigante, Jacaré Salgado, Libélula Gigante e Onça.', 'Essa habilidade só pode ser usada uma vez por cena. Ele não pode se transformar em alguma criatura humaniide e criaturas de porte parecido vista pessoalmente podem ser adicionadas à lista.', 'None', 'Seu companheiro animal.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (87632e99-c562-466a-87cf-f07f7542ab9b, 'Comandar Companheiro: Atacar e Machucar', 1, 'acao bonus', 'MESTRE DAS FERAS, VOZ', '18m.', 'Instantânea.', 'Mágico vs **DES**.', '1d10 pontos de dano de acordo com o ataque do companheiro.', 'None', 'Seu companheiro realiza um ataque contra uma criatura adjacente.', 'None', 'None', 'None', 'Ilimitado.', 'reacao', 'ADICIONA', 'Em um acerto, o alvo fica ***Desprotegido*** até o início do seu próximo turno.', 1, 'PE');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (bdcaaf43-93af-4979-b1eb-46bd80798415, 'Comandar Companheiro: Buscar e Entregar', 1, 'acao bonus', 'MESTRE DAS FERAS, VOZ', '9m.', 'Instantânea.', 'None', 'None', 'None', 'Seu companheiro animal pega um item com uma criatura voluntária e entrega para outra, desde que ambas estejam no seu alcance. Também é possível usar esse comando para fazer com que ele busque um item arremessado em alcance.', 'None', 'None', 'None', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (2fb564b1-61d7-49db-b559-1d2cfa7dc217, 'Comandar Companheiro: Ataque de Superioridade', 1, 'acao bonus', 'MESTRE DAS FERAS, VOZ', '9m.', 'Instantânea.', 'FOR vs FOR', 'Você deve escolher um efeito entre: Deixar o alvo ***Caído***; Pegar um item do alvo; Deixar o alvo ***Agarrado***.', 'None', 'None', 'Você só pode usar essa habilidade em criaturas de seu tamanho ou menor.', 'None', 'Uma criatura.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (0f45f5a1-341a-4b80-8850-813c8493a327, 'Comandar Companheiro: Atacar e Machucar', 1, 'acao bonus', 'MESTRE DAS FERAS, VOZ', '18m.', 'Instantânea.', 'None', 'None', 'None', 'Faça um teste de **SAB** vs **DES** para encontrar uma criatura escondida no seu alcance. Se você vencer o teste, seu companheiro animal se desloca para um espaço adjacente ao da criatura e realizar um _“Comandar Companheiro: Atacar e  Machucar”_ como  <:acao_livre:1326585198892154901> ação livre.', 'None', 'None', 'None', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (33738c4e-ac5d-47e0-b5de-4a1fbb894bb6, 'Resistir com Unhas e Dentes', 1, 'reacao', 'ESPECIALISTA', 'Pessoal.', 'Instantâneo.', 'None', 'None', 'None', 'Jogue seu dado de _Ataque Especializado_. Você usa o resultado da jogada para aumentar sua redução contra o dano sofrido.', 'Você só pode usar essa habilidade uma vez por rodada.', 'Você sofre dano.', 'O usuário.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_TALENTO}
    # VALUES (9f6cbd3a-0886-4045-8cd0-54d7e296408e, 'Resistir para Findar', 'Sua proximidade com A Morte fez com que você encontrasse formas de dar o fim. Seus **ATAQUES** recebem a seguinte modificação:', 'reacao', 'ADICIONA', '**Especial:** Você ignora todas as resistências do alvo nesse ataque.', 1, 'PE');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (a37db676-097e-4b8a-854d-8e1115522647, 'Inspirar Através de Palavras', 1, 'reacao', 'ESPECIALISTA, INSPIRAÇÃO, VOZ', '18m.', 'Uma cena.', 'None', 'None', 'None', 'Você inspira o aliado. Enquanto estiver ***Inspirado*** dessa maneira, o aliado pode usar seu dado de _“Ataque Especializado”_ como bônus para um teste a sua escolha. Se o fizer, ele deixa de estar ***Inspirado***.', 'você recupera o uso da sua <:reacao:1326585200519544885> reação. Você só pode usar essa habilidade uma vez por rodada.', 'Você foi bem-sucedido em um teste.', 'Um aliado.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (671efb4c-0ff7-4f4b-9d43-3b3f53ca6d93, 'Avaliar a Natureza do Inimigo', 1, 'acao bonus', 'ESPECIALISTA', '9m.', 'Instantânea.', '**SAB** vs **SAB**.', 'Você descobre uma informação importante sobre o inimigo. Escolha um: sua **Proteção** mais alta ou sua **Proteção** mais  baixa', 'None', 'None', 'None', 'None', 'Uma criatura.', 'Ilimitado.', 'reacao', 'AMPLIAR +15', '**Execução:** Você pode escolher os dois.', 1, 'PE');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (1a65506a-90ab-4943-ab99-a5aaab829dc7, 'Echo of Pomona: Energy Concentration', 4, 'eop', 'EOP, VOZ', '18m.', 'Instantânea.', 'None', '3d10 pontos de dano **ELÉTRICO**.', 'None', 'Vincenzo concentra resquísios da energia de Pomona próximo ao alvo, criando uma esfera de energia que ao acerta deixa o alvo ***Paralisado***', 'None', 'None', 'Criaturas em um diâmetro de 3m.', '1', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_PASSIVA}
    # VALUES (4972805e-8fec-4d83-86d1-f3db62965fb2, 'Pele de Casca', 'Ao tornar-se parte da Corte da Primavera, o usuáario também se conecta com uma das árvores ancestrais de Sarfo e sua pele começa a ficar dura como uma casca de árvore. Você recebe +1 nas suas **proteções** físicas.', 'None', 'None', '0', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_PASSIVA}
    # VALUES (652d92be-b240-48e9-97ef-61ad6e6b2d30, 'Conexão com o Ambiente', 'Você sabe resistir aos percalços do caminho. Você tem **resistência** a dano do tipo **ESPECIAL**,', 'None', 'None', '0', 0, 'None');"""
    #     )
    #     session.execute(
    #         """
    # """
    #     )
    #     session.execute(
    #         """
    # """
    #     )
    #     session.execute(
    #         f"""{INSERT_ITEM}
    # VALUES (7f123601-d48c-4a50-93f2-91fef0b16b60, 'Lâminas Duplas de Aço Varmaniano', 'Um grande par de láminas encontradas na salão de Warpinier. "Como você ficou tão bom em usar duas espadas do nada?" — questionou Chrollo durante a batalha contra a.', 35, 2);"""
    #     )
    #     session.execute(
    #         f"""{INSERT_ITEM}
    # VALUES (0c94309b-cd29-4945-a539-b420ada16652, 'Soul Guitar', 'Um rifre de pólvora disfaçado de guitarra que antes pertencia a Skeleton.', 100, 3);"""
    #     )
    #     session.execute(
    #         f"""{INSERT_ITEM}
    # VALUES (cae511af-c8fc-41de-9a7c-4e09fe281e5f, 'Arco Mágico de Nácar', 'Um arco mágico que você ganhou de Pomona no começo da sua jornada.', 30, 3);"""
    #     )
    #     session.execute(
    #         """
    # """
    #     )

    #     # --------------------------------------------------------------------------------------------

    #     # PROMPT DO TSUKU

    #     session.execute(
    #         f"""{INSERT_PASSIVA}
    # VALUES (7de3b1c4-8f3e-4296-8de1-319e0e794dca, 'Ataque Poderoso', 'Você treinou seu corpo para ser capaz de desferir ataques poderosíssimos sempre que ataca. Seus **ATAQUES** com **ARMAS** recebem a seguinte modificação:', 'reacao', 'AMPLIAR + 15', '**Acerto:** você causa +1d8 pontos de dano do mesmo tipo.', 0, 'PE');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (fd7382c2-dda4-4101-b0b0-4b17c7c5daef, 'Primeira Forma: Ember Aura', 2, 'acao bonus', 'ELEMENTARISTA, ELEMENTAL, ASPECTO, AURA', 'Pessoal.', 'Uma cena.', 'None', 'None', 'None', 'O usuário entra em estado de afinidade com o fogo. Enquanto estiver em afinidade com ele, você recebe **resistência** ao dano **ÍGNEO** e pode somar seu **bônus de proficiência** ao dano de seus ataques com o descrito **ÍGNEO**.', 'None', 'None', 'Pessoal.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (798ba218-6874-48fe-bde8-3264b263291b, 'Segunda Forma: Incendiary Aura', 0, 'acao bonus', 'ELEMENTARISTA, ÍGNEO, MANOBRA ELEMENTAL', 'None', 'Até o final do seu próximo turno.', 'None', 'None', 'None', 'Sempre que for acertado por um  **ATAQUE** corpo a corpo, a criatura que o atacou sofre 2d6 pontos de dano **ÍGNEO**.', 'O usuário precisa estar em afinidade elemental para usar essa habilidade.', 'None', 'Você.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (158702ec-4a4c-495b-8880-eb58f9dc811f, 'Terceira Forma: Incendiary Aura', 0, 'reacao', 'ELEMENTARISTA, ÍGNEO, ASPECTO', 'None', 'Instântanea.', 'None', 'None', 'None', 'O usuário manifesta uma aura ígnea de 3m e todos os aliados dentro da aura recebem resistência a dano **ÍGNEO**. No começo do seu próximo turno você pode usar 1 ponto de ênfase para manter a aura ativada por mais um turno.', 'O usuário precisa estar em afinidade elemental para usar essa habilidade. O usuário pode usar essa habilidade uma vez por cena.', 'Um aliado adjacente é sofre um ataque **ÍGNEO**.', 'Você.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (92b15962-8e60-4fef-9e9c-2301648aa461, 'Quarta Forma: Fire Shoot', 0, 'acao bonus', 'ELEMENTARISTA, ATAQUE, ÍGNEO, MÁGICO, MANOBRA ELEMENTAL', '9m.', 'Instantânea.', 'Mágico vs **DES**.', '1d10 pontos de dano **ÍGNEO**.', 'Metade do dano.', 'None', 'O usuário precisa estar em afinidade elemental para usar essa habilidade.', 'None', 'Uma criatura no alcance.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (fe9dbd56-2cef-4e91-acdb-f3af604fbb6e, 'Quinta Forma: Scorching Flow', 1, 'acao bonus', 'ELEMENTARISTA, ÍGNEO, MANOBRA ELEMENTAL', '9m.', 'Até o final do seu próximo turno.', 'None', 'None', 'None', 'O próximo **ATAQUE** que a criatura acertar causa +1d8 pontos de dano **ÍGNEO** com o qual você está em afinidade.', 'O usuário precisa estar em afinidade elemental para usar essa habilidade.', 'None', 'Uma criatura voluntária.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');      """
    #     )
    #     session.execute(
    #         """
    # """
    #     )
    #     session.execute(
    #         """
    # """
    #     )
    #     session.execute(
    #         f"""{INSERT_SKILL}
    # VALUES (1ebb3ce6-f374-4cae-a7d1-0f4a820a8afc, 'Corte com a Yedo', 0, 'acao', 'ATAQUE, CORTANTE, VERSÁTIL', '6m.', 'Instatânea.', '1d20 + Bônus de FOR vs DES.', '1d8 + 1d10 pontos de dano **CORTANTE**', 'Caso você erre no teste de acerto, você solta a **ARMA** e terá que gastar sua <:acao_bonus:1326585197004722197> Ação Bônus para pegá-la novamente.', 'None', 'None', 'None', 'Uma criatura.', 'Ilimitado.', 'None', 'None', 'None', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_PASSIVA}
    # VALUES (1b3bc403-8932-43b4-a244-e4dd5c134e4c, 'Servo Elemental', 'Você recebe **resistência** a dano **ELÉTRICO**.', 'None', 'None', '0', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_PASSIVA}
    # VALUES (4e784780-03b5-4805-a2c3-602911cb6b5a, 'Mini Guerreiro Dracônico', 'As grandes guerreiros do Kito serviam ao império dracônico como guerreiros letais. Todos os seus **ATAQUES** com o  descritor **LEVE** recebem o descritor **LETAL**.', 'None', 'None', '0', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_PASSIVA}
    # VALUES (3b4d28a9-02eb-4b85-a32b-58987db123a5, 'Um Oitavo de Forma Dracônica', 'O usuário carrega (um pouco) do sangue dos dragões em suas veias. Você é imune à condição ***Amedrontado*** e todos os ataques com o descritor **MEDO** são feitos com **desvantagem** contra você.', 'None', 'None', '0', 0, 'None');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_TALENTO}
    # VALUES (15034448-5eef-4996-bb93-e26f241c26bf, 'Frenesi Flamejante', 'Enquanto estiver em afinidade elemental, seus **ATAQUES** com **ARMA** recebem a seguinte modificação:', 'reacao', 'ADICIONA', 'f**Efeito:** O alvo fica ***Marcado +1***. Caso tenha usado seu *"Ataque Poderoso"*, adicione mais uma marca.\n**Acerto:** O alvo sofre +1d6 pontos de dano **ÍGNEO** para cada contador de ***Marcado*** que ele tiver. A quantidade máxima de dados de dano que podem ser causados dessa maneira é igual ao seu atributo-chave de conjuração.', 1, 'PE');"""
    #     )
    #     session.execute(
    #         f"""{INSERT_ITEM}
    # VALUES (97245586-3669-47a1-87ec-3feeebed3fa6, 'Yedo', 'Espada tradicional de Novahorizon, longa e ligeiramente curva.', 100, 2);"""
    #     )

    # --------------------------------------------------------------------------------------------

    # PROMPT DE ZÊNITE

    # -------------------------------------------------------------------------------------------

    # PROMPT FENRIR

    # --------------------------------------------------------------------------------------------

    # PROMPT ASHBORN

    # --------------------------------------------------------------------------------------------

    # DEFINIR PARTY

    session.execute(
        """INSERT INTO xmercury.party (id, personagens_jogaveis)
    VALUES (8a87e68e-cd9d-46e5-953a-35942487ef1b, [69fa11c2-ca6a-44b7-93c2-b744d0e98554]);"""
    )

    pass
