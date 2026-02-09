import os

import constantes
from connect_postgres import PostgresDB
from dotenv import load_dotenv

load_dotenv()
postgres_db = PostgresDB(
    os.getenv("POSTGRES_DB"),
    os.getenv("POSTGRES_USER"),
    os.getenv("POSTGRES_PASSWORD"),
    # os.getenv("POSTGRES_HOST")
    "localhost",
    os.getenv("POSTGRES_PORT"),
)

bonus_de_proficiencia = 3
level = 6
pe = 15
ataque_poderoso_especializado = "1d8"


def calc_liimite_peso(forca: int) -> int:
    base = 16

    if forca <= 0:
        return base - (forca * 2)
    elif forca >= 1:
        return base + (forca * 3)


def calc_hp(constituicao: int, classe: int) -> int:
    if classe == 0:
        base = 10
    elif classe == 1:
        base = 8
    elif classe == 2:
        base = 6
    return int(base + constituicao + ((level - 1) * (constituicao + base // 1.5)))


# -----------------------------

with postgres_db.get_cursor() as cursor:
    cursor.execute(
        f"""DROP TABLE
            itens_personagens,
            pericias_personagens,
            modificadores_skills,
            modificadores,
            skills,
            talentos,
            passivas,
            itens,
            personagens,
            pericias,
            condicoes,
            descritores,
            party;"""
    )

    # -----------------------------

    cursor.execute(
        f"""CREATE TABLE party (
            id_party UUID PRIMARY KEY
            );"""
    )
    print("PARTY CRIADA")

    cursor.execute(
        f"""CREATE TABLE personagens (
            id_personagem UUID PRIMARY KEY,
            nome TEXT,
            nickname TEXT,
            level INTEGER,
            legacy TEXT,
            classe TEXT,
            path TEXT,
            heritage TEXT,
            melancholy TEXT,
            catarse INTEGER,
            pe INTEGER,
            pe_atual INTEGER,
            hp INTEGER,
            hp_atual INTEGER,
            hp_tipo TEXT,
            reducao_de_dano INTEGER,
            bonus_de_proficiencia INTEGER,
            pontos_de_sombra INTEGER,
            pericias UUID[],
            protecao_forca INTEGER,
            bonus_forca INTEGER,
            protecao_destreza INTEGER,
            bonus_destreza INTEGER,
            protecao_constituicao INTEGER,    
            bonus_constituicao INTEGER,
            protecao_inteligencia INTEGER,
            bonus_inteligencia INTEGER,
            protecao_sabedoria INTEGER,
            bonus_sabedoria INTEGER,
            protecao_carisma INTEGER,
            bonus_carisma INTEGER,
            volume_atual INTEGER,
            limite_de_volume INTEGER,
            resistencia TEXT, 
            vulnerabilidade TEXT, 
            imunidade TEXT,
            saldo INTEGER,
            imagem TEXT,
            tokenn TEXT,
            usuario TEXT,
            id_party UUID REFERENCES party(id_party) ON DELETE CASCADE
        );"""
    )
    print("PERSONAGENS CRIADA")

    # -----------------------------

    cursor.execute(
        f"""CREATE TABLE skills (
            id_skill UUID PRIMARY KEY,
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
            id_personagem UUID REFERENCES personagens(id_personagem) ON DELETE CASCADE
        );"""
    )
    print("TABELA SKILLS CRIADA")

    # -----------------------------

    cursor.execute(
        f"""CREATE TABLE talentos (
            id_talento UUID PRIMARY KEY,
            nome TEXT,
            descricao TEXT,
            id_personagem UUID REFERENCES personagens(id_personagem) ON DELETE CASCADE
        );"""
    )
    print("TALENTOS CRIADO")

    # -----------------------------

    cursor.execute(
        f"""CREATE TABLE passivas (
            id_passiva UUID PRIMARY KEY,
            nome TEXT,
            descricao TEXT,
            id_personagem UUID REFERENCES personagens(id_personagem) ON DELETE CASCADE
        );"""
    )
    print("PASSIVAS CRIADA")

    # -----------------------------

    cursor.execute(
        f"""CREATE TABLE modificadores (
            id_modificador UUID PRIMARY KEY,
            nome TEXT,
            descricao TEXT,
            execucao TEXT,
            gasto INTEGER,
            gasto_tipo TEXT
        );"""
    )
    print("TABELA MODIFICADORES CRIADA")

    # -----------------------------

    cursor.execute(
        f"""CREATE TABLE modificadores_skills (
            id_skill UUID NOT NULL REFERENCES skills(id_skill) ON DELETE CASCADE,
            id_modificador UUID NOT NULL REFERENCES modificadores(id_modificador) ON DELETE CASCADE,
            PRIMARY KEY (id_skill, id_modificador)
        );"""
    )
    print("TABELA MODIFICADORES_SKILLS CRIADA")

    # -----------------------------

    cursor.execute(
        f"""CREATE TABLE itens (
            id_item UUID PRIMARY KEY,
            nome TEXT,
            descricao TEXT,
            preco INTEGER,
            volume INT
        );"""
    )
    print("TABELA ITENS CRIADA")

    # -----------------------------

    cursor.execute(
        f"""CREATE TABLE itens_personagens (
        id_item UUID NOT NULL REFERENCES itens(id_item) ON DELETE CASCADE,
            id_personagem UUID NOT NULL REFERENCES personagens(id_personagem) ON DELETE CASCADE,
            quantidade INTEGER,
            PRIMARY KEY (id_item, id_personagem)
            );"""
    )
    print("TABELA ITENS_PERSONAGENS CRIADA")

    # -----------------------------

    cursor.execute(
        f"""CREATE TABLE pericias (
            id_pericia UUID PRIMARY KEY,
            nome TEXT,
            descricao TEXT,
            e_vantagem BOOLEAN,
            e_soma BOOLEAN,
            somar TEXT[]
            );"""
    )
    print("TABELA PERICIAS CRIADA")

    # -----------------------------

    cursor.execute(
        f"""CREATE TABLE pericias_personagens (
            id_pericia UUID NOT NULL REFERENCES pericias(id_pericia) ON DELETE CASCADE,
            id_personagem UUID NOT NULL REFERENCES personagens(id_personagem) ON DELETE CASCADE,
            nivel INTEGER,
            PRIMARY KEY (id_personagem, id_pericia))"""
    )
    print("TABELA PERICIAS_PERSONAGENS CRIADA")

    # -----------------------------

    cursor.execute(
        f"""CREATE TABLE condicoes (
            id_condicao UUID PRIMARY KEY,
            nome TEXT,
            descricao TEXT
            );"""
    )
    print("CONDIÇÕES CRIADA")

    # -----------------------------

    cursor.execute(
        f"""CREATE TABLE descritores (
            id_descritor UUID PRIMARY KEY,
            nome TEXT,
            tipo TEXT,
            descricao TEXT
            );"""
    )
    print("DESCRITORES CRIADO")

    # -------------------------------------------------------------------------------------------

    # PROMPT PERICIAS

    cursor.execute(
        """INSERT INTO pericias (id_pericia, nome, descricao, e_vantagem, e_soma, somar)
 VALUES ('7b32de93-92b1-402a-93fe-c7a295535490', 'Forja', 'Sua maestria na forja é admirável. Você pode forjar ferramentas se tiver os materiais e equipamentos necessários, sendo eles: calor, material, martelo e uma base.', false, false, NULL),
        ('57565a89-08ef-47ce-984a-f95272c58e03', 'Pescaria', 'A pesca fez parte da sua vida. Você possui vantagem em testes de pesca.', true, false, NULL),
        ('98f70eea-9c31-44a4-8c66-2b1eca1a530a', 'Transmutação', 'Se o usuário tiver alguma forma de realizar transmutações, ele pode somar seu bônus de proficiência ou algum atributo-chave de conjuração nos testes (INT; SAB; CAR).', false, true, '{"bonus_de_proficiencia","inteligencia","sabedoria","carisma"}'),
        ('e95b8d53-07d4-47bf-9d99-e23368c2dcba', 'Alquimia', 'O usuário pode criar poções se tiver os materiais e equipamentos necessários: matéria-prima, recipiente (opcional), maleta de manipulação, caldeirão e calor ou mesa de síntese.', false, false, NULL),
        ('fc42be7c-bf7b-4fb2-b528-ac30bc0605d6', 'Culinária', 'O usuário pode fazer pratos deliciosos (comidas com efeitos especiais), possui vantagem nos testes de culinária e pode somar seu bônus de proficiência ou algum atributo-chave de conjuração nos testes (INT; SAB; CAR).', true, true, '{"bonus_de_proficiencia","inteligencia","sabedoria","carisma"}'),
        ('802584f3-85a5-4851-988c-eebe5e1a6d12', 'Geografia', 'O usuário se torna capaz em fazer mapas e nunca esquecer um caminho.', false, false, NULL),
        ('c25f6a18-6b01-423a-9c44-1781f677137d', 'Arcanismo', 'O usuário tem proficiência na área arcâna da magia, como runas, rituais e até mesmo grimórios arcânos. O usuário pode somar seu bônus de proficiência ou algum atributo-chave de conjuração nos testes (INT; SAB; CAR).', false, true, '{"bonus_de_proficiencia","inteligencia","sabedoria","carisma"}'),
        ('a67da4e1-ba56-4b89-a491-6b0ae5337453', 'Cultura', 'O usuário tem conhecimentos da sociedade, atualidades, costumes e noções culturais ao redor de Opath. O usuário pode somar seu bônus de proficiência ou algum atributo-chave de conjuração nos testes (INT; SAB; CAR).', false, true, '{"bonus_de_proficiencia","inteligencia","sabedoria","carisma"}'),
        ('1030947f-9e65-476a-b08c-c834a2ddfe7f', 'Diplomacia', 'O usuário possui conhecimentos em barganhas e trocas. O usuário pode somar seu bônus de proficiência ou algum atributo-chave de conjuração nos testes (INT; SAB; CAR).', false, true, '{"bonus_de_proficiencia","inteligencia","sabedoria","carisma"}'),
        ('0222604e-cd4d-4077-b19f-7eb7c4e8c927', 'Persuasão', 'O usuário possui conhecimentos em manipulações e tratos. O usuário pode somar seu bônus de proficiência ou algum atributo-chave de conjuração nos testes (INT; SAB; CAR).', false, true, '{"bonus_de_proficiencia","inteligencia","sabedoria","carisma"}'),
        ('71850f9a-22d3-441a-b675-8858d8718984', 'Furtividade', 'O usuário sabe bem como se misturar em multidões e pode somar seu bônus de proficiência ou algum atributo-chave para o teste (DES; INT; SAB).', false, true, '{"bonus_de_proficiencia","destreza","inteligencia","sabedoria"}'),
        ('ebaea72e-3d09-487e-a809-360077352a5c', 'Sobrevivência', 'O usuário tem experiência de como é sobreviver no ambiente selvagem e caçar feras. Ele pode somar seu bônus de proficiência ou algum atributo-chave para o teste (FOR; DES; CON; INT; SAB; CAR).', false, true, '{"bonus_de_proficiencia","forca","destreza","constituicao","inteligencia","sabedoria","carisma"}'),
        ('a052505a-add0-4717-9d30-e382a0741058', 'Intimidação', 'O usuário sabe como fazer alguma criatura sentir medo. Ele pode somar seu bônus de proficiência ou algum atributo-chave para o teste (FOR; CON; CAR).', false, true, '{"bonus_de_proficiencia","forca","constituicao","carisma"}'),
        ('eab18040-8a73-41a1-ba35-66918c594f97', 'Magitecnologia', 'O usuário possui conhecimentos básicos sobre o funcionamento da magitecnologia e pode realizar testes com vantagens para entender como funciona alguns circuitos magitecnológicos e montá-los.', true, false, NULL),
        ('50e3508e-335c-42ef-97cf-1db7a07962c4', 'Malandragem', 'O usuário é esperto e consegue sabotar equipamentos magitecnológicos e arrombar portas', false, false, NULL),
        ('110bf214-eb58-4c0b-8c4c-6eba30302575', 'Medicina', 'O usuário consegue detectar doenças, prestar primeiros socorros e fazer necropsias. O usuário possui um sucesso garantido em primeiros socorros por dia que tiver ataduras ou remédios em seu intentário', false, false, NULL),
        ('3bc86566-ec94-4459-a7fc-2a5d094a1f39', 'Percepção', 'O usuário pode detectar, ouvir ou notar a presença de algo próximo. Ele pode somar seu bônus de proficiência ou alguma atributo-chave para somar no teste (DES; SAB).', false, true, '{"bonus_de_proficiencia","sabedoria","destreza"}'),
        ('c57e4a9b-2e9d-4c97-9f6c-0139cd0ddb44', 'Lógica', 'O usuário é esperto e é bom para resolver enigmas. Ele pode somar seu bônus de proficiência ou algum atributo-chave nos testes (INT; SAB).', false, true, '{"bonus_de_proficiencia","inteligencia","sabedoria"}'),
        ('d28b4723-1177-46ac-b1f2-bf785330b1a9', 'Disparo', 'O usuário possui uma boa pontaria. Ele pode somar seu bônus de proficiência em disparos com armas de fogo.', false, true, '{"bonus_de_proficiencia"}'),
        ('c7482295-cb98-49fe-92fd-8266c8675121', 'Briga', 'O usuário é bom de briga. Ele pode somar seu bônus de proficiência ou em testes de acerto corpo a corpo desarmados e *"Ataques de Superioridade"*.', false, true, '{"bonus_de_proficiencia"}'),
        ('62ef595a-2f6e-475c-8152-3f36a5c4e695', 'Agilidade', 'O usuário é ágil e consegue desviar de muitos ataques, escalar com facilidade e realizar movimentos que muitos não conseguiriam. Ele pode somar seu bônus de proficiência em testes de esquiva e movimentos acrobáticos/atléticos.', false, true, '{"bonus_de_proficiencia"}'),
        ('8d72c0e9-5c54-4b4a-b80a-a3b60d8f1309', 'Iniciativa', 'O usuário é veloz e é um dos primeiros a atacar em um combate. Ele pode somar seu bônus de proficiência ou algum atributo-chave nos testes (DES).', false, true, '{"bonus_de_proficiencia","destreza"}'),
        ('d0f44af5-c299-41c2-9e84-72dd9cdb7351', 'Magia', 'O usuário é habilidoso com a magia. Ele pode somar seu bônus de proficiência em testes mágicos.', false, true, '{"bonus_de_proficiencia"}'),
        ('89056ec3-8736-4136-a962-e86434799d2c', 'Esgrima', 'O usuário é habilidoso na arte da espada. Ele pode somar seu bônus de proficiência em testes de esgrima.', false, true, '{"bonus_de_proficiencia"}'),
        ('8baa2e54-e91b-4af4-a2df-fe7806e865da', 'Mentalidade', 'O usuário tem uma mente forte e não é afetado por interências facilmente. Ele pode somar seu bônus de proficiência ou alguma atributo-chave para somar no teste (INT; SAB; CAR) em testes que envolvem resistência mental.', false, true, '{"bonus_de_proficiencia","inteligencia","sabedoria","carisma"}');"""
    )
    print("\nPERÍCIAS ADICIONADAS")

    # -------------------------------------------------------------------------------------------

    # PROMPT CONDIÇÕES

    cursor.execute(
        f"""{constantes.INSERT_CONDICAO}
 VALUES ('5db1ddaf-b80a-412f-a899-9ecebd4bed7b', 'Agarrado', 'A criatura está ***Contida***.\nA condição termina se: a criatura que está ***Agarrando*** ficar ***Incapacitada***, se um efeito remover a criatura agarrada do alcance do agarrador ou do efeito de agarramento ou se a criatura agarrada vencer um teste de **FOR**.'),
        ('f6b7900f-4782-4d6f-8af3-e30e293c4021', 'Agarrando', 'A criatura está ativamente agarrando outro (que está ***Agarrada***).\nUma criatura que está ***Agarrando*** pode mover-se junto da criatura ***Agarrada***, mas tem seu movimento reduzido pela metade.\nA criatura deve ocupar suas duas mãos para manter a condição.\n Ela pode encerrar essa condição a qualquer momento com uma ação livre, encerrando também a condição ***Agarrada*** na outra criatura.'),
        ('d77a53e7-0f65-4104-a193-cfaabfed4ca4', 'Amedrontado', 'Uma criatura amedrontada tem **desvantagem** em testes de atributo e ataque.\nA criatura não pode se mover por vontade própria para perto da fonte de seu medo.\n Se não estiver vendo a fonte do medo ela fica parada no local que está.'),
        ('4c382c07-d787-497e-8ef7-1736a95aa072', 'Atordoado', 'Uma criatura atordoada está ***Incapacitada***, não pode se mover e só é capaz de balbuciar.'),
        ('f1b03b6e-1e18-4d82-9a9a-3d0e9f8c2f11', 'Caído', 'Uma criatura caída tem como única opção de movimento rastejar, a não ser que se levante, encerrando assim a condição.\nA criatura tem **desvantagem** em jogadas de ataque\nAtaques contra a criatura tem **vantagem**.'),
        ('3fa85f64-5717-4562-b3fc-2c963f66afa6', 'Desprotegido', 'Ataques feitos contra a **Proteção** descrita são feitos com vantagem.\nA proteção afetada vem descrita em parênteses após o nome da condição, podendo ser a proteção de um atributo específico, de atributos físicos ou mentais.\nCaso não seja especificado um atributo, a criatura está desprotegida contra ataques que afetem qualquer **Proteção**.\nA condição ***Protegido*** anula essa condição (desde que afete o mesmo atributo).'),
        ('5b02a76b-88e5-4e39-bcc1-30519dfd29b8', 'Desorientado', 'A criatura está ***Desprotegida***.\nTodos os testes que envolvem uso dos sentidos são feitos com **desvantagem**.\nTodos os ataques realizados pela criatura são feitos com **desvantagem**.'),
        ('2c8cf18a-8f8d-4b0c-9b3b-7a1a96b88cb3', 'Em Chamas', 'Essa condição é acompanhada de um contador, que inicia em 1 e pode aumentar.\nA criatura sofre 1d6 pontos de dano **ÍGNEO** no começo do seu turno para cada contador na condição.\nAo final do turno da criatura o contador da condição aumenta em +1.\nEla precisa usar uma ação para apagar as chamas e encerrar a condição (zerando o contador).\nO Mestre pode decidir que outras ações podem apagar as chamas.'),
        ('f0c74a32-2e0a-4a4f-8c89-6b501b3e721d', 'Encantado', 'Uma criatura encantada não pode atacar quem a encantou ou atingir quem a enfeitiçou com ataques usando atributos ou efeitos mágicos.\nQuem encantou tem **vantagem** em qualquer teste de atributo para interagir socialmente com a criatura encantada.'),
        ('7e03f7b3-64c3-4b4c-a51a-4e6ed8c97788', 'Inconsciente', 'Uma criatura inconsciente está ***Incapacitada***, não pode se mover ou falar e não está ciente dos seus arredores.\nA criatura larga qualquer coisa que esteja segurando e fica ***Caída***.\nA criatura está ***Desprotegida***.\nAtaques em área contra as proteções físicas da criatura têm sucesso automático.\nQualquer ataque bem-sucedido contra a criatura é um acerto crítico se o atacante estiver a até 2 metro dela.'),
        ('c8c1c4d1-5c2d-4fa3-8b1b-1ffb6b2a9f7d', 'Inspirado', 'A criatura está sob efeito de alguma habilidade com o descritor **INSPIRAÇÃO**.\nA duração e o efeito da inspiração é determinada pela habilidade que gerou a condição. Caso contrário, dura até final da cena.\nUma criatura só pode estar inspirada com um efeito por vez (terminando o efeito do primeiro).'),
        ('2a50cfb1-6d45-47bb-942a-33fbc1b13b63', 'Invisível', 'Uma criatura invisível não pode ser vista sem ajuda de magia ou de um sentido especial.\nPara propósitos de se esconder, considera-se que a criatura está em área totalmente obscurecida.\nA localização da criatura pode ser detectada, seja por qualquer som que ela emita ou rastros visuais que deixe.\nTestes de ataque contra a criatura têm **desvantagem**, e as jogadas de ataque da criatura têm **vantagem**.'),
        ('b9f40a31-5b7d-4e8a-86de-3c5a9c1a60e4', 'Marcado', 'Criaturas com essa condição estão sob efeito de uma habilidade ou magia que aplicou essa condição.\nEssa condição é acompanhada de um contador, que começa em +1 e aumenta em +1 para cada vez que a condição foi aplicada nessa cena.\nEssa condição desaparece no final de uma cena.\nHabilidades podem fazer referência a essa condição.'),
        ('de6531b0-2898-4c84-98ad-2e5f9b799fb3', 'Machucada', 'Toda criatura com um valor igual ou menor que a metade dos seus pontos de vida totais está machucada.\nHabilidades podem fazer referência a essa condição.'),
        ('e6cb2b31-74b9-4c1b-bf5e-76c3bfb6078a', 'Paralisado', 'Uma criatura paralisada está ***Incapacitada*** e não pode se mover ou falar.\nA criatura está ***Desprotegida***.\nQualquer ataque bem-sucedido contra a criatura é um acerto crítico se o atacante estiver a até 1,5 metro dela.'),
        ('ba56e320-52f8-4e8f-b6b5-9a0d5b72e4f1', 'Petrificado', 'Uma criatura petrificada é transformada, juntamente com qualquer objeto não mágico que esteja vestindo ou carregando, em uma substância sólida e inanimada (geralmente pedra).\nSeu peso aumenta em dez vezes e ela para de envelhecer.\nA criatura está ***Incapacitada***, não pode se mover ou falar, e não está ciente dos seus arredores.\nA criatura está ***Desprotegida***.\nA criatura tem **resistência** contra todos os tipos de dano.\nA criatura é **imune** a veneno e doenças, embora um veneno ou doença que já esteja em seu sistema seja apenas suspenso, e não neutralizado.'),
        ('cd1a71ef-2f45-4ee3-b2dc-4e0c76f91a58', 'Protegido', 'Ataques feitos contra a proteção descrita são feitos com **desvantagem**.\nA proteção afetada vem descrita em parênteses após o nome da condição, podendo ser a proteção de um atributo específico, de atributos físicos ou mentais.\nCaso não seja especificado um atributo, a criatura está protegida contra ataques que afetem qualquer proteção.\nA condição ***Desprotegido*** anula essa condição (desde que afete o mesmo atributo).'),
        ('e1fcb75b-4d7f-4b9b-9477-0f13f3b41a2c', 'Provocado', 'A criatura tem **desvantagem** em testes de atributo enquanto não incluir a criatura que a provocou como alvo.');"""
    )
    print("CONDIÇÕES ADICIONADAS")

    # -------------------------------------------------------------------------------------------

    # PROMPT DE DESCRITORES

    cursor.execute(
        f"""{constantes.INSERT_DESCRITOR}
VALUES ('32dfd367-5efa-42eb-bdc8-55a8097e3aaa', 'ORC', 'Descritor de Origem', 'Alcança um espaço adicional (geralmente de adjacente para 1,5m a mais).'),
       ('d364d1b2-d72a-4f32-8745-8d4e3b6f9fa1', 'CONTROLE', 'Descritor de Categoria', 'Habilidades relacionadas a controle de efeito e condições em criaturas ou em uma área.'),
       ('1f89cf08-c8a6-40f3-9742-a3f2f05d8be7', 'ALONGADA', 'Descritor de Equipamento', 'Alcança um espaço adicional (geralmente de adjacente para 1,5m a mais).'),
       ('a242b7a7-e4bb-4c05-8864-c4d1d744171b', 'ARREMESSÁVEL', 'Descritor de Equipamento', 'Esse descritor faz com que **TAQUES** a distância possam usar **FOR** para ataque e dano. Elas são arremessadas e caem no mesmo espaço do alvo. O alcance do ataque está descrito na própria arma. Caso uma arma receba esse descritor por outro meio, ela tem 9m de alcance.'),
       ('5dc1281b-106a-4f46-9ab3-e7e8c1d6c7f5', 'BARULHENTA', 'Descritor de Equipamento', 'Enquanto for empunhado ou vestido, esse equipamento concede **desvantagem** em todos os testes que envolvam Furtividade.'),
       ('a9d2d895-80cd-4823-8606-558059c0236f', 'COMPOSTO', 'Descritor de Equipamento', '*"Ataques à Distância"* realizados com essa arma permitem que você aplique sua **FOR** às jogadas de dano.'),
       ('3260452d-890d-4034-af65-f7cabfe08b2c', 'DISPARÁVEL', 'Descritor de Equipamento', 'Esse descritor faz com que **ATAQUES** a distância usem munição, que é perdida depois do **ATAQUE**. Esta arma usa o valor de **DES** em vez de **FOR** para calcular ataque e dano. O alcance do ataque está descrito na própria arma. Caso uma arma receba esse descritor por outro meio, ela tem 9m de alcance.'),
       ('0cd312e4-757f-47fc-b60a-31aca5b129a9', 'EFICIENTE', 'Descritor de Equipamento', 'Você recebe **vantagem** no teste da perícia indicada enquanto empunhar a arma.'),
       ('2d30fb47-7a24-4556-b147-4004c1d6af10', 'ELIXIR', 'Descritor de Equipamento', 'Representa um preparo alquímico que pode ser consumido para fazer efeito especial.'),
       ('da500cc6-51e2-461a-81fd-de7caac9c19a', 'ESPALHAFATOSA', 'Descritor de Equipamento', 'Essa arma faz com que seus ataques afetam até duas criaturas adjacentes ao alvo original do **ATAQUE**.'),
       ('230ddf43-b420-4fd6-922e-ad570e20607f', 'GRANADA', 'Descritor de Equipamento', 'Objeto que pode ser arremessado e que causa efeito na criatura que acertar ou espaço que cair.'),
       ('5063b1e6-495f-4f26-8b16-00de482db904', 'LEVE', 'Descritor de Equipamento', 'Uma arma ou habilidade com esse descritor pode utilizar **DES** em vez de **FOR** em testes de ataque e dano.'),
       ('5168cc66-c65a-451e-bb1e-871d2f6f53de', 'LETAL', 'Descritor de Equipamento', 'Ao ter um acerto crítico com essa arma, você causa um dado de dano adicional (além de dobrar os dados).'),
       ('1ca684f0-66bc-445b-acd5-bf82381e4f4a', 'MONTADA', 'Descritor de Equipamento', 'Feita para ser utilizada por combatentes montados. Personagens montadas que atacarem com essa arma causam +1d6 de dano.'),
       ('05602726-6c66-450b-b6ca-d67936a4239d', 'PESADA', 'Descritor de Equipamento', 'Precisa de grande força física para ser utilizada corretamente. Algumas habilidades fazem referência a armas pesadas.'),
       ('bde30cc7-1368-4678-9a62-ed49e087ad87', 'POTENTE', 'Descritor de Equipamento', 'Uma arma ou poder com esse descritor realiza ataques de **FOR** contra **CON** do alvo, ao invés de **DES**.'),
       ('3fae6002-4924-431f-a8e9-de01d23ebde5', 'PRECISO', 'Descritor de Equipamento', 'O atacante recebe +2 em jogadas de ataque com a arma caso não tenha se movido antes de atacar.'),
       ('964389fd-5664-4c07-8359-cfc163dd54e3', 'QUEBRADIÇO', 'Descritor de Equipamento', 'O objeto está quebrando. Se for uma arma, quebra quando o atacante tiver uma falha crítica ou acerto crítico. Se for uma armadura ou escudo, tem sua **redução** reduzida em 1 e quebra quando um atacante conseguir um sucesso crítico.'),
       ('2b91f12a-3099-40d4-88be-fe47c1c247a0', 'RETORNÁVEL', 'Descritor de Equipamento', 'A arma retorna para a mão de seu dono no final do turno em que foi arremessada'),
       ('d450025a-891a-4ad4-8880-a0edc9248272', 'SUPERIOR', 'Descritor de Equipamento', 'O atacante é pode adicionar +3 em testes de "Ataque de Superioridade".'),
       ('77f4ec81-5fca-4270-974a-a7666c85d61f', 'VERSÁTIL', 'Descritor de Equipamento', 'Uma arma de uma mão com esta habilidade pode ser usada com as duas mãos para aumentar seu dano (em parênteses).'),
       ('24013dae-ee81-49c2-b65b-f30f9b9a9234', 'ÁCIDO', 'Descritor de Dano', 'Vômitos de criaturas grotescas, substâncias corrosivas e dano relacionado com demônios e diabretes. Dano relacionado com o elemento Terra.'),
       ('9ef9e5ba-5cc4-4b70-8dc9-8699bdb7bf9f', 'CONTUNDENTE', 'Descritor de Dano', 'Ataques de força e impacto martelos, quedas, constrição e similares causam dano contundente.'),
       ('bc56a097-8858-43ce-81fa-f11221634dd1', 'ALQUÍMICO', 'Descritor Diverso', 'Habilidades, magias ou itens que combinam elementos mágicos, químicos e de engenharia para fabricação de granadas e elixires.')
    ;"""
    )
    print("DESCRITORES ADICIONADOS")

    # -------------------------------------------------------------------------------------------

    # CRIANDO PARTY

    cursor.execute(
        f"""{constantes.INSERT_PARTY}
VALUES ('8a87e68e-cd9d-46e5-953a-35942487ef1b'),
       ('50282f93-2701-43b7-83e5-664d2a1251be');"""
    )

    # -------------------------------------------------------------------------------------------

    # PROMPT CHROLLO

    reducao_de_dano = 4
    forca = ["12", "1"]
    destreza = ["12", "1"]
    constituicao = ["13", "2"]
    inteligencia = ["14", "4"]
    sabedoria = ["10", "0"]
    carisma = ["9", "-1"]
    pericias = "'d0f44af5-c299-41c2-9e84-72dd9cdb7351', '89056ec3-8736-4136-a962-e86434799d2c', '98f70eea-9c31-44a4-8c66-2b1eca1a530a', '7b32de93-92b1-402a-93fe-c7a295535490', 'eab18040-8a73-41a1-ba35-66918c594f97'"

    cursor.execute(
        f"""{constantes.INSERT_PERSONAGEM}
VALUES ('30180fc6-30ba-4f65-a520-53e63bc4ec65', 'Shin NovaChrollo', 'Chrollo', {level}, 'Magitécnico', 'Combatente', 'Humano', 'Pomonas Cycle', 'Para Chrollo, o fim é necessário. Assim como a vida, todo ciclo tem um fim. Sempre que um ciclo se encerrar Chrollo ganha 1 **ponto de catarse**.', 0, {pe}, {pe}, {calc_hp(int(constituicao[1]), 0)}, {calc_hp(int(constituicao[1]), 0)}, 'hp', {reducao_de_dano}, {bonus_de_proficiencia}, 5, ARRAY[{pericias}]::UUID[], {int(forca[0])}, {int(forca[1])}, {int(destreza[0])}, {int(destreza[1])}, {int(constituicao[0])}, {int(constituicao[1])}, {int(inteligencia[0])}, {int(inteligencia[1])}, {int(sabedoria[0])}, {int(sabedoria[1])}, {int(carisma[0])}, {int(carisma[1])}, 10, {calc_liimite_peso(int(forca[1]))}, NULL, NULL, NULL, 220, 'chrollo.png', '<:chrollo_token:1384691822584135894>', '766039963736866828', '8a87e68e-cd9d-46e5-953a-35942487ef1b');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_MODIFICADOR}
VALUES ('ca236d0c-dcdb-4a05-89e7-3322afe2c849', 'reacao', 'AMPLIAR + 15', '**Acerto:** você causa +{ataque_poderoso_especializado} pontos de dano do mesmo tipo.', 0, 'PE');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_SKILL}
VALUES ('02c0f9f6-a880-496e-98c1-795f4b00c700', 'Ataque de Superioridade', 0, 'acao', 'ATAQUE', '2m.', 'Instantânea.', '**FOR** vs **FOR**.', 'Você deve escolher um efeito entre: Deixar o alvo ***Caído***; Pegar um item do alvo; Deixar o alvo ***Agarrado***.', NULL, NULL, 'Você só pode usar essa habilidade em criaturas de seu tamanho ou menor.', NULL, 'Uma criatura.', 'Ilimitado.', '30180fc6-30ba-4f65-a520-53e63bc4ec65'),
       ('a4a7564b-37ed-43f5-bc09-df897ef8e7de', 'Ataque em Sequência', 1, 'acao', 'COMBATENTE', 'Pessoal.', 'Instântanea.', NULL, NULL, NULL, 'Você pode realizar uma combinação de duas habilidades dentre "Ataque Corpo a Corpo", "Ataque à Distância" e "Ataque de Superioridade" como <:acao_livre:1326585198892154901> ação livre.', NULL, NULL, 'Você.', 'Ilimitado.', '30180fc6-30ba-4f65-a520-53e63bc4ec65'),
       ('aeb4b910-9877-4d55-bdc8-811a96ff9a69', 'Pomonas Treasure', 0, 'acao', 'MÁGICO', 'Toque.', 'Instântanea.', NULL, NULL, NULL, 'Você se torna capaz de criar véus de mana a partir das próprias mãos. Esse véu junta dois ou mais objetos de forma natural e sem resíduos. Podendo juntar até mesmo almas à uma receptáculo', NULL, NULL, 'Um objeto.', 'Ilimitado.', '30180fc6-30ba-4f65-a520-53e63bc4ec65'),
       ('00a33d61-0ab6-4637-89fd-ccffac04ab3e', 'Transmutar Item', 1, 'acao bonus', 'MÁGICO, CRIAÇÃO, TRANSMUTAÇÃO', 'Pessoal.', 'Instantânea.', NULL, NULL, NULL, 'O usuário consome um item do inventário para criar um novo item. O item criado deve ser equivalente ao item consumido.', 'Essa habilidade necessita do *Tablet de Transmutação*, e caso o usuário perca-o, essa habilidade não poderá ser usada.', NULL, 'Um espaço vago no inventário.', 'Ilimitado.', '30180fc6-30ba-4f65-a520-53e63bc4ec65'),
       ('135b9b63-dec7-4378-b2a1-a2bfe1350869', 'Corte com a Masked Death', 0, 'acao', 'ATAQUE, ARMA, CORTANTE', '2m.', 'Instatânea.', '1d20 + {int(forca[1])} + 2 + {bonus_de_proficiencia} vs **DES**.', '1d8 + 1d10 + {bonus_de_proficiencia} pontos de dano **CORTANTE**', 'Caso você erre no teste de acerto, você solta a **ARMA** e terá que gastar sua <:acao_bonus:1326585197004722197> Ação Bônus para pegá-la novamente.', NULL, NULL, NULL, 'Uma criatura.', 'Ilimitado.', '30180fc6-30ba-4f65-a520-53e63bc4ec65'),
       ('995f1424-7a51-404f-a8c5-fec283499bff', 'Kamino Fuuga', 2, 'acao', 'ATAQUE, MÁGICO, ÍGNEO', '15m', 'Instântanea.', '1d20 + {int(inteligencia[1])} + {bonus_de_proficiencia} vs **DES**.', '2d6 pontos de dano **ÍGNEO**.', 'Metade do dano.', 'A criatura fica engolfada em chamas. Enquanto estiver dessa forma, ela está **Desprotegida** até usar uma <:acao:1326585196232966225> ação para apagar o fogo.', 'Você só pode usar essa habilidade caso esteja empunhando um pedaço de carvão. Para cada *saco de carvão* que for gasto nessa habilidade, o ataque ganha 1d10 de dano **ÍGNEO**', NULL, 'Criaturas em uma esfera de 3m de raio dentro do alcance.', 'Ilimitado.', '30180fc6-30ba-4f65-a520-53e63bc4ec65'),
       ('dbe7bcff-b5be-46a1-84e3-cbdf1a368283', 'Masked Death: Fools Blood', 1, 'acao', 'ATAQUE, ARMA, NECRÓTICO, MÁGICO', 'Uma espera de 3m de raio.', 'Instântanea.', '1d20 + {int(forca[1])} + {bonus_de_proficiencia} + 2 vs **DES**', '2d8 + 1d10 + {bonus_de_proficiencia} de dano **NECRÓTICO**.', 'O encantamento acaba', NULL, 'O usuário precisa ativar o encantamento da espada para usar essa habilidade, usando sangue ou algumas gotas de uma poção de cura nela em uma <:acao_bonus:1326585197004722197> Ação Bônus.', NULL, 'Criaturas dentro de alcance.', '{bonus_de_proficiencia}', '30180fc6-30ba-4f65-a520-53e63bc4ec65'),
       ('08f4b428-a138-4edf-b3b7-a82c16aebb6c', 'Disparo com a Shorty Aemondir', 0, 'acao', 'DISPARO, PERFURANTE, ARMA, ESPALHAFATOSO, ATAQUE', '9m.', 'Instantânea.', '1d20 + {int(destreza[1])} + {bonus_de_proficiencia} + 1 vs **DES**.', '2d8 + {bonus_de_proficiencia} + 1 pontos de dano.', 'Caso você erre no teste de acerto, você solta a **ARMA** e terá que gastar sua <:acao_bonus:1326585197004722197> Ação Bônus para pegá-la novamente.', NULL, 'Soma +1 ao número de dados do crítico depois de dobrá-los.', NULL, 'Uma criatura.', 'Ilimitado.', '30180fc6-30ba-4f65-a520-53e63bc4ec65'),
       ('429de159-48f9-48ab-870a-850983c4be4b', 'Mortalha Energizante', 0, 'reacao', 'HUMANO', 'Pessoal.', 'Instantânea.', NULL, NULL, NULL, 'Você recebe {bonus_de_proficiencia} pontos de ênfase temporários durante essa cena.', 'Você só pode usar essa habilidade uma vez por descanso.', 'Uma criatura na cena morre', NULL, 'Ilimitado.', '30180fc6-30ba-4f65-a520-53e63bc4ec65'),
       ('f76dc202-536c-47f6-a9e2-cccb400d9102', 'Empoderamento Biomagitec', 0, 'acao bonus', 'MAGITÉCNICO', 'Toque.', 'Até o final do próximo descanso longo.', NULL, NULL, NULL, 'Você toca um objeto mundano e empodera-o com energia biomagitec. O objeto torna-se uma engenhoca biomagitec a sua escolha. Se for uma arma, recebe o descritor **MÁGICA**.', 'Você só pode usar essa habilidade uma vez por cena.', NULL, NULL, 'Ilimitado.', '30180fc6-30ba-4f65-a520-53e63bc4ec65'),
       ('bd083bdf-6021-4680-b5c7-36ca4c4c537d', 'Construção Rápida de Magibot', 1, 'acao bonus', 'MAGITÉCNICO, PROTÓTIPO, CRIAÇÃO', NULL, 'Uma cena.', NULL, NULL, NULL, 'Você empodera peças biomagitec para criar um pequeno autômato chamado magibot.', NULL, NULL, 'Um espaço vago no inventário.', 'Ilimitado.', '30180fc6-30ba-4f65-a520-53e63bc4ec65');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_PASSIVA}
VALUES ('d2808e11-146c-49f1-a631-4d365472a303', 'Ataque Poderoso', 'Você treinou seu corpo para ser capaz de desferir ataques poderosíssimos sempre que ataca. Seus **ATAQUES** com **ARMAS** recebem uma nova modificação.', '30180fc6-30ba-4f65-a520-53e63bc4ec65'),
       ('d06ff7ac-cad1-49d6-be84-6eb290879dea', 'Tradição Oral', 'Você é capaz de reter uma quantidade infinita de informação em seu cérebro. Você tem **vantagem** em todos os testes de **INT** relacionados a lembrar de fatos ou informações.', '30180fc6-30ba-4f65-a520-53e63bc4ec65'),
       ('c47f8a5f-9531-4a07-8142-a1c2bc080684', 'Combate com uma Arma', 'Você recebe +1 em todas as **Proteções** físicas.', '30180fc6-30ba-4f65-a520-53e63bc4ec65'),
       ('60e33837-6378-4ec9-9490-bcc094e15a00', 'Façanha com uma Arma', 'Sua principal estratégia de combate consiste em atacar com precisão e deslocar-se para uma posição vantajosa. Se seu primeiro ataque em um combate for com sua arma, ele é feito com **vantagem**.', '30180fc6-30ba-4f65-a520-53e63bc4ec65'),
       ('342c60ba-f18c-4e74-b37b-adf5e4275007', 'Precisão Vantajosa', 'Existem combatentes que se especializam na arte de extrair o máximo de qualquer situação vantajosa. Você joga um dado de **vantagem** adicional em com seus **ATAQUES** já com **vantagem**, gastando 1 PE no processo, mas ainda deve escolher apenas um para o resultado final.', '30180fc6-30ba-4f65-a520-53e63bc4ec65'),
       ('bdb5a1da-730c-4886-b935-57eb852d4ad4', 'Protótipo Utilitário: Dispositivo de Proteção Avançado', 'Esse pequeno dispositivo é acoplado a uma armadura que você estiver vestindo. Enquanto estiver ativo, ele concede +1 na **redução de dano**', '30180fc6-30ba-4f65-a520-53e63bc4ec65');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_TALENTO}
VALUES ('f4e0b395-33f6-4ad2-97de-0a76bf42f968', 'Transmitir Conhecimento Adquirido', 'Você aperfeiçoou suas técnicas de transmissão de conhecimento. Ao final de uma Cena de Descanso, pode escolher um aliado para receber ***inspiração***, que dura até o próximo descanso longo.', '30180fc6-30ba-4f65-a520-53e63bc4ec65'),
       ('8173f83f-5ae8-4635-802f-d10d3e897b6e', 'O Preço do Progresso', 'Você recebe proficiência em armas de fogo. Ao usar uma arma de fogo, pode usar **INT** em vez de **DES** em testes de **ATAQUE** e dano.', '30180fc6-30ba-4f65-a520-53e63bc4ec65'),
       ('2ab46c0f-d69e-4e65-9285-d13c4b32043c', 'No Ponto Certo', 'Atacar com precisão de maneira astuta é sua especialidade. Sempre que atacar com uma arma com o descritor **LEVE**, você pode somar sua **INT** em teste de **ATAQUE** e no dano.', '30180fc6-30ba-4f65-a520-53e63bc4ec65');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_ITEM}
VALUES ('abb1a0d3-d0ac-4bc1-960b-9defa7dadde6', 'Masked Death', 'Uma espada longa com o encantamento *"Fools Blood"*. A espada é bem trabalhada e possui a inscrição "Masked Death" em sua lâmina, que faz referência à banda de seu antigo portador, Zombie. O encantamento precisa de um pouco de sangue ou algumas gotas de poção de cura para ativar suas cargas, depois da ativação a espdada fica vermelha e pode usar a habilidade *"Masked Death: Fools Blood"*.', 500, 2),
       ('938f7ffe-b0ff-4824-97dd-9769ccd35aae', 'Tablet de Transmutação', 'Uma grande invenção de um alquimista alemão do século XV. Um pedaço de ardósia lapidado com adornos metálicos e uma pedra filosofal no centro. A propriedade de reorganização de partículas permite transmutar elementos e até criar fogo ou outras formar de energia.', 0, 2),
       ('3cb0873e-4ddf-4c3e-861d-aaf6151c7f17', 'Armadura de Couro Batido', 'Proteção comum entre mercenários e aventureiros inexperientes, reforçada com pequenas placas de couro em locais estratégicos.', 40, 3),
       ('21f4bb82-5741-44eb-ac29-4601f2fa2d9a', 'Armadura Espectral de Warpinier', 'Um espectro da aura da grande armadura de Warpiniier. Vestida por cima de tudo, concede +1 na **redução de dano** e contém os encantamentos: **Manipuladora de Sombras** e **Silenciosa**.', 0, 1),
       ('fa359f98-b7a9-44ed-acea-8e1099a34d83', 'Shorty Aemondir', 'Uma escopeta de ação por alavanca mágica de cano curto. Ela foi encontrada no castelo de Warpinier e provavelmente fazia parte do arsenal de Boris Nosferata. "Algo dentro de mim me dizia que eu precisava de uam dessa desde o começo" — disse Chrollo ao contrá-la.', 750, 3);"""
    )
    cursor.execute(
        f"""{constantes.INSERT_ITENS_PERSONAGENS}
 VALUES ('abb1a0d3-d0ac-4bc1-960b-9defa7dadde6', '30180fc6-30ba-4f65-a520-53e63bc4ec65', 1),
        ('938f7ffe-b0ff-4824-97dd-9769ccd35aae', '30180fc6-30ba-4f65-a520-53e63bc4ec65', 1),
        ('3cb0873e-4ddf-4c3e-861d-aaf6151c7f17', '30180fc6-30ba-4f65-a520-53e63bc4ec65', 1),
        ('21f4bb82-5741-44eb-ac29-4601f2fa2d9a', '30180fc6-30ba-4f65-a520-53e63bc4ec65', 1),
        ('fa359f98-b7a9-44ed-acea-8e1099a34d83', '30180fc6-30ba-4f65-a520-53e63bc4ec65', 1);"""
    )
    cursor.execute(
        f"""{constantes.INSERT_MODIFICADOR_SKILLS}
VALUES ('135b9b63-dec7-4378-b2a1-a2bfe1350869', 'ca236d0c-dcdb-4a05-89e7-3322afe2c849'),
       ('dbe7bcff-b5be-46a1-84e3-cbdf1a368283', 'ca236d0c-dcdb-4a05-89e7-3322afe2c849'),
       ('08f4b428-a138-4edf-b3b7-a82c16aebb6c', 'ca236d0c-dcdb-4a05-89e7-3322afe2c849');"""
    )
    print("\nCHROLLO ADICIONADO")

    # -------------------------------------------------------------------------------------------

    # PROMPT JULIUS

    reducao_de_dano = 4
    forca = ["11", "1"]
    destreza = ["13", "3"]
    constituicao = ["12", "2"]
    inteligencia = ["11", "1"]
    sabedoria = ["10", "0"]
    carisma = ["9", "-1"]
    pericias = "'c25f6a18-6b01-423a-9c44-1781f677137d', '1030947f-9e65-476a-b08c-c834a2ddfe7f', 'a052505a-add0-4717-9d30-e382a0741058', '3bc86566-ec94-4459-a7fc-2a5d094a1f39', 'd28b4723-1177-46ac-b1f2-bf785330b1a9', '89056ec3-8736-4136-a962-e86434799d2c'"

    cursor.execute(
        f"""{constantes.INSERT_PERSONAGEM}
VALUES ('69fa11c2-ca6a-44b7-93c2-b744d0e98554', 'Julius Wick', 'Julius', {level}, 'Necromante das Sombras', 'Especialista', 'Humano', 'Pomonas Cycle', 'Para Julius, o fim é necessário. Assim como a vida, todo ciclo tem um fim. Sempre que um ciclo se encerrar Julius ganha 1 **ponto de catarse**.', 0, {pe}, {pe}, {calc_hp(int(constituicao[1]), 1)}, {calc_hp(int(constituicao[1]), 1)}, 'hp', {reducao_de_dano}, {bonus_de_proficiencia}, 5, ARRAY[{pericias}]::UUID[], {int(forca[0])}, {int(forca[1])}, {int(destreza[0])}, {int(destreza[1])}, {int(constituicao[0])}, {int(constituicao[1])}, {int(inteligencia[0])}, {int(inteligencia[1])}, {int(sabedoria[0])}, {int(sabedoria[1])}, {int(carisma[0])}, {int(carisma[1])}, 15, {calc_liimite_peso(int(forca[1]))}, NULL, NULL, NULL, 100, 'julius.png', '<:julius_token:1384691827654918268>', '921158705075077150', '8a87e68e-cd9d-46e5-953a-35942487ef1b');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_MODIFICADOR}
VALUES ('b159c984-f271-4f47-9ced-56ccc0b23390', 'reacao', 'ADICIONA', '**Acerto:**  Você causa +{ataque_poderoso_especializado} pontos de dano do mesmo tipo.\n**Especial:** Você só pode causar esse dano adicional uma vez por turno.', 0, 'PE'),
       ('7dff256a-bf88-4a6f-ad3c-ca03b9235c6a', 'reacao', 'ADICIONA', '**Especial:** Você ignora todas as resistências do alvo nesse ataque.', 1, 'PE'),
       ('d3d60e71-fb0e-4408-a1ac-d305a931c223', 'reacao', 'ADICIONA', '**Efeito**: você usa a habilidade *"Comandar Sombra"* como <:acao_livre:1326585198892154901> Ação Livre para comandar uma sombra dentro do alcance (podendo ser inclusive um recém invocado).', 2, 'PE'),
       ('36b5fe2a-25fb-4a89-a64f-c0ccdd6a47b3', 'reacao', 'ADICIONA', '**Alvo:** Você afeta mais um reanimado controlado por você. É possível aplicar essa modificação mais de uma vez.', 1, 'PE');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_SKILL}
VALUES ('bb85504b-ff0b-4e3f-ae2c-5e0effb87f2b', 'Disparo com a Red Hunter', 0, 'acao', 'DISPARO, PERFURANTE, PRECISO, ARMA, ESPALHAFATOSO, ATAQUE', '18m.', 'Instantânea.', '1d20 + {int(destreza[1])} + {bonus_de_proficiencia} vs **DES**.', '2d8 + {bonus_de_proficiencia} + 2 pontos de dano.', 'Caso você erre no teste de acerto, você solta a **ARMA** e terá que gastar sua <:acao_bonus:1326585197004722197> Ação Bônus para pegá-la novamente.', 'O usuário aplica +1 nível de ***Shadow Cover***.', NULL, NULL, 'Uma criatura.', 'Ilimitado.', '69fa11c2-ca6a-44b7-93c2-b744d0e98554'),
       ('8dea83d1-5beb-4c02-a29f-322205850046', 'Corte com a Masked Death', 0, 'acao', 'ATAQUE, ARMA, CORTANTE, VERSÁTIL, ALONGADA', '2m.', 'Instatânea.', '1d20 + {int(forca[1])} + {bonus_de_proficiencia} vs **DES**.', '1d8 + 1d10 + {bonus_de_proficiencia} + 2 pontos de dano **CORTANTE**', 'Caso você erre no teste de acerto, você solta a **ARMA** e terá que gastar sua <:acao_bonus:1326585197004722197> Ação Bônus para pegá-la novamente.', 'O usuário aplica +1 nível de ***Shadow Cover***.', NULL, NULL, 'Uma criatura.', 'Ilimitado.', '69fa11c2-ca6a-44b7-93c2-b744d0e98554'),
       ('b7864548-2ebe-4823-a884-d1a6455d6a7f', 'Masked Death: Fools Blood', 1, 'acao', 'ATAQUE, ARMA, VERSÁTIL, NECRÓTICO, MÁGICO, ALONGADO', '3m.', 'Instântanea.', '1d20 + {int(forca[1])} + {bonus_de_proficiencia} + 2 vs **DES**', '2d8 + 1d10 + {int(forca[1])} + {bonus_de_proficiencia} + 2 de dano **NECRÓTICO**.', 'O encantamento acaba', NULL, 'O usuário precisa ativar o encantamento da espada para usar essa habilidade, usando sangue ou algumas gotas de uma poção de cura nela em uma <:acao_bonus:1326585197004722197> Ação Bônus.', 'O usuário aplica +1 nível de ***Shadow Cover***.', 'Criaturas dentro de alcance.', '{bonus_de_proficiencia}', '69fa11c2-ca6a-44b7-93c2-b744d0e98554'),
       ('9079caad-0894-4b94-ad67-e977ff1c41e3', 'Mortalha Energizante', 0, 'reacao', 'HUMANO', 'Pessoal.', 'Instantânea.', NULL, NULL, NULL, 'Você recebe {bonus_de_proficiencia} pontos de ênfase temporários durante essa cena.', 'Você só pode usar essa habilidade uma vez por descanso.', 'Uma criatura na cena morre', NULL, 'Ilimitado.', '69fa11c2-ca6a-44b7-93c2-b744d0e98554'),
       ('52471318-ce98-44a9-9503-57164c4d3630', 'Cambalhota Especializada!', 1, 'reacao', 'ESPECIALISTA', 'Pessoal.', 'Instatânea.', NULL, NULL, NULL, 'Você fica ***Caído*** e recebe **resistência** contra o dano do ataque.', NULL, 'Você é acertado por um ataque que não tenha sido realizado com **vantagem**.', 'Você.', 'Ilimitado.', '69fa11c2-ca6a-44b7-93c2-b744d0e98554'),
       ('d234c7bb-82a0-40e4-bda2-8fa4641c5ca2', 'Resistir com Unhas e Dentes', 1, 'reacao', 'ESPECIALISTA', 'Pessoal.', 'Instantâneo.', NULL, NULL, NULL, 'Jogue seu dado de *Ataque Especializado*. Você usa o resultado da jogada para aumentar sua redução contra o dano sofrido.', 'Você só pode usar essa habilidade uma vez por rodada.', 'Você sofre dano.', 'O usuário.', 'Ilimitado.', '69fa11c2-ca6a-44b7-93c2-b744d0e98554'),
       ('685388af-e4d2-4f4f-8b16-029910c08ba6', 'Necromancia Aprimorada', 2, 'acao bonus', 'NECROMANTE, MÁGICO', '9m.', NULL, NULL, NULL, NULL, 'O usuário pode consumir qualquer número de marcas de criaturas para aprimorar qualquer número de sombras que você controle. Você escolhe como distribuir as melhorias por marca.', NULL, NULL, 'Uma sombra controlada pelo usuário.', 'Ilimitado.', '69fa11c2-ca6a-44b7-93c2-b744d0e98554'),
       ('d3c3086e-4324-4a3f-bf3b-135b8acded07', 'Erga-se', 1, 'acao bonus', 'NECROMANTE, MÁGICO, CRIAÇÃO, SOMBRA', '6m.', 'Até ser destruído ou ser ordenado a voltar ao núcleo ou sombra.', NULL, NULL, NULL, 'Você invoca uma echo sombrio de sua posse.', NULL, NULL, 'Um espaço desocupado no alcance.', 'Ilimitado.', '69fa11c2-ca6a-44b7-93c2-b744d0e98554'),
       ('e6189aac-5dda-49a7-9d39-d5b7927e5a82', 'Comandar Sombra', 1, 'acao bonus', 'NECROMANTE, MÁGICO, SOMBRA', '9m,', 'Instantânea.', NULL, NULL, NULL, 'Você comanda uma sombra a realizar uma habilidade.', NULL, NULL, 'Uma sombra comandada por você.', 'Ilimitado.', '69fa11c2-ca6a-44b7-93c2-b744d0e98554'),
       ('64e4a387-ac93-4146-957f-f38c3f6b6e10', 'Receber Benção', 2, 'acao livre', 'ESPECIALISTA', 'Pessoal.', 'Até o próximo descanso longo.', NULL, NULL, NULL, 'O usuário ativa todas suas benções.', 'O usuário só pode usar essa habilidade no final de uma Cena de Descanso e somente uma vez por cena.', NULL, 'O usuário.', 'Ilimitado.', '69fa11c2-ca6a-44b7-93c2-b744d0e98554'),
       ('43d8755b-a5f4-4c4d-8aa5-ee3e235b80a1', 'Alimentos das Chamas', 2, 'acao', 'BENÇÃO, MÁGICO', 'Visão.', 'Instântanea.', 'Mágico vs **CAR**.', 'O usuário descobre o que aquela criatura mais deseja (naquela cena).', 'O usuário só pode usar essa habilidade se tiver usado a habilidade "*Receber Benção"*', 'Nenhuma outra personagem ou criatura sabe que você usou essa habilidade.', NULL, NULL, 'Uma criatura.', 'Ilimitado.', '69fa11c2-ca6a-44b7-93c2-b744d0e98554'),
       ('e314977f-8d03-4eba-9b24-9778b689331b', 'Engolfar em Chamas da Vingança', 1, 'acao bonus', 'BENÇÃO, MÁGICO, ÍGNEO', 'Pessoal.', 'Até o fim da próxima cena.', NULL, NULL, NULL, 'Todo o dano que você causar passa a ser **ÍGNEO**.', 'O usuário só pode usar essa habilidade se tiver usado a habilidade *"Receber Benção"*', NULL, 'Você.', 'Ilimitado.', '69fa11c2-ca6a-44b7-93c2-b744d0e98554');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_PASSIVA}
VALUES ('e4d7675d-3cb7-4395-8de0-5c4c17a8cc83', 'Ataque Especializado', 'Você aprendeu a se virar em combate usando astúcia e conhecimento com suas armas. Seus **ATAQUES** com **vantagem** que causam dano recebem a seguinte modificação:', '69fa11c2-ca6a-44b7-93c2-b744d0e98554'),
       ('1126f58d-581e-42d0-91fd-a008ebe306ec', 'Energia Negativa', 'Todos os seus **ATAQUES** com **ARMA** ou que causem dano **NECRÓTICO** causam +2 pontos de dano. Além disso, sempre que você ou uma de suas **CRIAÇÕES** causarem dano **NECRÓTICO** com um **ATAQUE**, o alvo fica ***Marcado*** ou aumenta essa condição em +1. Além disso, quando uma sombra sob seu controle for eliminado, a criatura que o eliminou recebe a condição ***Marcado***, ou aumenta essa condição em +1. Por fim, sempre que uma criatura ***Marcada*** em até 18m de você morrer, você pode transferir essa condição para você ou para uma sombra sob seu controle.', '69fa11c2-ca6a-44b7-93c2-b744d0e98554'),
       ('2c09f75c-18ad-40af-bb7c-d3cc01132f42', 'Exército de Sombras', 'O usuário é capaz de invocar um echo sombrio e depois comandá-lo em combate. A sombra passa a ser considerado um personagem e não pode agir diretamente durante uma cena de combate. Sempre que você se deslocar, suas sombras podem se deslocar uma distância igual à que você deslocou-se. Você pode usar as habilidades *"Erga-se"*, *"Comandar Sombra"* e *"Necromancia Aprimorada"*.', '69fa11c2-ca6a-44b7-93c2-b744d0e98554'),
       ('e3d01446-1435-4198-a521-0afc5397a348', 'Hidden Inventory', 'Você é capaz de guardar um item em sua sombra. Seu limite de peso aumentou em +4.', '69fa11c2-ca6a-44b7-93c2-b744d0e98554');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_TALENTO}
VALUES ('94c51d1e-c688-4185-9c62-3f1782fd4651', 'Resistir para Findar', 'Sua proximidade com A Morte fez com que você encontrasse formas de dar o fim. Seus **ATAQUES** recebem umaa nova modificação.', '69fa11c2-ca6a-44b7-93c2-b744d0e98554'),
       ('961e8d2d-c360-4751-9829-7786acf4e6aa', 'Se Dá Certo; Não é Estúpido; é Genial!', 'Diferente dos outros aventureiros, você é considerado proficiente com ataques improvisados, pode usar seus pontos de ênfase neles e causa o dobro dos dados de dano que causariam. Além disso, se a arma for um item pequeno (volume 1 ou menos), recebe o descritor **ARMA** e um descritor à sua escolha entre **ARREMESSÁVEL** ou **LEVE**; se for um item grande (volume 3 ou mais), precisa usá-lo com as duas mãos e ele recebe um descritor à sua escolha entre **ALONGADA** ou **ESPALHAFATOSA**.', '69fa11c2-ca6a-44b7-93c2-b744d0e98554'),
       ('334434be-2ff3-4f94-8813-e1117a017b16', 'Trajado', 'Sempre que estiver vestindo uma armadura leve e não estiver empunhando um escudo, você aumenta a redução da sua armadura em +2.', '69fa11c2-ca6a-44b7-93c2-b744d0e98554');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_ITEM}
VALUES ('d24b8e11-6d39-4228-8211-55f2458fb72c', 'Masked Death', 'Uma espada longa com o encantamento *"Fools Blood"*. A espada é bem trabalhada e possui a inscrição "Masked Death" em sua lâmina, que faz referência à banda de seu antigo portador, Zombie. O encantamento precisa de um pouco de sangue ou algumas gotas de poção de cura para ativar suas cargas, depois da ativação a espdada fica vermelha e pode usar a habilidade *"Masked Death: Fools Blood"*.', 500, 2),
       ('52056c6a-5200-4d16-8ecc-cde1ba3e5cd2', 'Red Hunter', 'Um grande rifre vermelho com detalhes pretos criado apatir da imaginação de seu portador. "Isso me lembra a sniper do Cypher" — disse Chrollo durante o acampamento na Black Rose Forest', 750, 2),
       ('0beb39c2-123a-4d40-b2eb-e011b55028fb', 'Armadura de Couro Batido', 'Proteção comum entre mercenários e aventureiros inexperientes, reforçada com pequenas placas de couro em locais estratégicos.', 40, 3),
       ('c4ae1cca-557b-44ed-977a-7231d4783d36', 'Núcleo Pesado de Fenrir', 'O núcleo marcado que abriga a alma de um grande lobo que viveu nas terras gélidas dos elfos do inverno, Jotunheim. Ele lutou até seu último dia para tentar alimentar e proteger sua matilha, perdendo toda sua sombra batalhando contra feras cada vez maiores.\nAté que em um dia, trouxe o maior banquete que a matilha já havia visto, mas aquele seria o último. Sua pelagem antes branca como a neve, estava banhada em sangue, seu próprio sangue.\nAlém daqueles que Fenrir lutava para proteger, junto dele estava aquela com quem ele muito negociava em seus "últimos momentos"...', 0, 3),
       ('7fd8f8ef-19d4-4556-a6ba-058bd51e86b4', 'Núcleo Pesado de Ashborn', 'O núcleo que abriga a alma do ex-guardião do Darkhold I. O verdadeiro desespero de um antigo reino inteiro em formato de um único guerreiro, reino esse que foi varrido pelo tempo.', 0, 3),
       ('53a9956b-a1e0-44fc-8d8d-6463afbf3339', 'Tabuleta Sombria', 'Após o grupo sair do domínio de Shadow e voltar à Opath, a mana que antes tomava conta da sala, foi de um estado sólido ao líquido de repente, escorrendo pelas paredes até se reunir uma tabuleta no centro da mesma. A tabuleta possui runas arcanas gravadas por todo seu corpo "ᚼᚤᛚᛚᚤᚢ ᚴᛁᚦᚷᚦᛄᛚ".', 0, 2);"""
    )
    cursor.execute(
        f"""{constantes.INSERT_ITENS_PERSONAGENS}
VALUES ('d24b8e11-6d39-4228-8211-55f2458fb72c', '69fa11c2-ca6a-44b7-93c2-b744d0e98554', 1),
       ('52056c6a-5200-4d16-8ecc-cde1ba3e5cd2', '69fa11c2-ca6a-44b7-93c2-b744d0e98554', 1),
       ('0beb39c2-123a-4d40-b2eb-e011b55028fb', '69fa11c2-ca6a-44b7-93c2-b744d0e98554', 1),
       ('c4ae1cca-557b-44ed-977a-7231d4783d36', '69fa11c2-ca6a-44b7-93c2-b744d0e98554', 1),
       ('7fd8f8ef-19d4-4556-a6ba-058bd51e86b4', '69fa11c2-ca6a-44b7-93c2-b744d0e98554', 1),
       ('53a9956b-a1e0-44fc-8d8d-6463afbf3339', '69fa11c2-ca6a-44b7-93c2-b744d0e98554', 1);"""
    )
    cursor.execute(
        f"""{constantes.INSERT_MODIFICADOR_SKILLS}
VALUES ('e6189aac-5dda-49a7-9d39-d5b7927e5a82', '36b5fe2a-25fb-4a89-a64f-c0ccdd6a47b3'),
       ('bb85504b-ff0b-4e3f-ae2c-5e0effb87f2b', 'd3d60e71-fb0e-4408-a1ac-d305a931c223'),       
       ('8dea83d1-5beb-4c02-a29f-322205850046', 'd3d60e71-fb0e-4408-a1ac-d305a931c223'),
       ('b7864548-2ebe-4823-a884-d1a6455d6a7f', 'd3d60e71-fb0e-4408-a1ac-d305a931c223'),
       ('bb85504b-ff0b-4e3f-ae2c-5e0effb87f2b', '7dff256a-bf88-4a6f-ad3c-ca03b9235c6a'),
       ('8dea83d1-5beb-4c02-a29f-322205850046', '7dff256a-bf88-4a6f-ad3c-ca03b9235c6a'),
       ('b7864548-2ebe-4823-a884-d1a6455d6a7f', '7dff256a-bf88-4a6f-ad3c-ca03b9235c6a');"""
    )

    print("JULIUS ADICIONADO")

    # --------------------------------------------------------------------------------------------

    # PROMPT ADAM

    reducao_de_dano = 5
    forca = ["12", "2"]
    destreza = ["11", "1"]
    constituicao = ["13", "3"]
    inteligencia = ["11", "1"]
    sabedoria = ["10", "0"]
    carisma = ["9", "-1"]
    pericias = "'c7482295-cb98-49fe-92fd-8266c8675121', '62ef595a-2f6e-475c-8152-3f36a5c4e695', '802584f3-85a5-4851-988c-eebe5e1a6d12', '0222604e-cd4d-4077-b19f-7eb7c4e8c927', 'ebaea72e-3d09-487e-a809-360077352a5c'"

    cursor.execute(
        f"""{constantes.INSERT_PERSONAGEM}
VALUES ('1c773acd-295b-436d-b792-8011e739e527', 'Adam Andrews', 'Adam', {level}, 'Orc Sanguir', 'Combatente', 'Pugilista', 'Griphon Byotr', 'Você é cria da Fúria, a deusa engolfada em chamas. Por vezes, seu temperamento poderá traí-lo, fazendo com que seja tomado pelo mesmo fogo que consome tudo à sua volta. Sempre que entrar no estado de cólera ardente, ganha 1 ponto de catarse.', 0, {pe}, {pe}, {calc_hp(int(constituicao[1]), 0)}, {calc_hp(int(constituicao[1]), 0)}, 'hp', {reducao_de_dano}, {bonus_de_proficiencia}, 5, ARRAY[{pericias}]::UUID[], {int(forca[0])}, {int(forca[1])}, {int(destreza[0])}, {int(destreza[1])}, {int(constituicao[0])}, {int(constituicao[1])}, {int(inteligencia[0])}, {int(inteligencia[1])}, {int(sabedoria[0])}, {int(sabedoria[1])}, {int(carisma[0])}, {int(carisma[1])}, 9, {calc_liimite_peso(int(forca[1])) + 4}, 'ÁCIDO, NECRÓTICO', NULL, NULL, 288, 'adam.png', '<:adam_token:1394716537956466788>', '1239326132327944313', '8a87e68e-cd9d-46e5-953a-35942487ef1b');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_MODIFICADOR}
VALUES ('4e4e6145-0e4b-476b-a161-0aeebd169e19', 'reacao', 'AMPLIAR + 15', '**Acerto:** você causa +{ataque_poderoso_especializado} pontos de dano do mesmo tipo.', 0, 'PE'),
       ('1fdfad97-eec6-4703-af0c-054a3ae09550', 'reacao', 'ADICIONA', '**Acerto:** Você causa +1d6 + 1 pontos de dano quando está ***Machucado***.\n**Especial:** Você pode aplicar essa modificação quantas vezes quiser.', 1, 'PE'),
       ('4666dab1-fc4a-40a5-9971-fba6d0e823f0', 'reacao', 'ADICIONA', '**Acerto:** após acertar o **ATAQUE**, você pode fazer um "*Ataque de Superioridade"* como <:acao_livre:1326585198892154901> ação livre.', 1, 'PE'),
       ('7aebae61-6619-437e-8576-6104f375a3f3', 'reacao', 'ADICIONA', '**Acerto:** +1d6 pontos de dano **PERFURANTE** e você recebe todos benefícios da característica *"Sangue Maldito"*, mas o alvo não fica com **desvantagem** em testes.', 2, 'PE');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_SKILL}
VALUES ('04df13c9-c079-4d4d-b7a7-6b5264a59114', 'Ataque de Superioridade', 0, 'acao', 'ATAQUE, ARMA', '2m.', 'Instantânea.', '1d20 + {int(forca[1])} + {bonus_de_proficiencia} vs **FOR**', 'Você deve escolher um efeito entre: Deixar o alvo ***Caído***; Pegar um item do alvo; Deixar o alvo ***Agarrado***.', NULL, NULL, 'Caso escolher agarrar o inimigo, poderá sugar parte do seu sangue com suas presas, recuperando 5 pontos de vida, eliminando uma condição ruim aplicada a você e deixando o alvo em **desvantagem** no próximo teste. Além disso, só pode usar essa habilidade em criaturas de seu tamanho ou menor.', NULL, 'Uma criatura.', 'Ilimitado.', '1c773acd-295b-436d-b792-8011e739e527'),
       ('e7a3b8d2-4f5c-4d91-90b0-3a8e6f9c7d2f', 'Ataque com o Martelo de Guerra', 0, 'acao', 'ATAQUE, CONTUNDENTE, PESADO, ARMA', '2m.', 'Instatânea.', '1d20 + {int(forca[1])} + {bonus_de_proficiencia} VS **DES**.', '1d12 + {int(forca[1])} + {bonus_de_proficiencia}', 'Caso você erre no teste de acerto, você solta a **ARMA** e terá que gastar sua <:acao_bonus:1326585197004722197> ação bônus para pegá-la novamente.', NULL, NULL, NULL, 'Uma criatura.', 'Ilimitado.', '1c773acd-295b-436d-b792-8011e739e527'),
       ('f3b9a7c1-2d8e-4f6a-bc21-7e9d5a1d8e54', 'Soco Desarmado', 0, 'acao', 'ARMA, ATAQUE, CONTUNDENTE, LEVE', '2m.', 'Instatânea.', '1d20 + {int(forca[1])} + {bonus_de_proficiencia}.', '1d8 + {int(forca[1])} {bonus_de_proficiencia}.', NULL, NULL, 'Após acertar esse ataque, você pode fazer um *Ataque de Superioridade*.', NULL, 'Uma criatura.', 'Ilimitado.', '1c773acd-295b-436d-b792-8011e739e527'),
       ('b2a9d7f3-8e4d-6c1d-bc71-3e9f7a5d8e54', 'Soco com Manopla', 0, 'acao', 'ARMA, ATAQUE, CONTUNDENTE, PESADO', '2m.', 'Instatânea.', '1d20 + {int(forca[1])}', '1d10 + {int(forca[1])} + 2', NULL, NULL, 'Após acertar esse ataque, você pode fazer um *Ataque de Superioridade*. Essa habilidade só pode ser usada se o usário tiver usado "*Modificar com Sangue: Conjurar Manoplas"* antes.', NULL, 'Uma criatura.', 'Ilimitado.', '1c773acd-295b-436d-b792-8011e739e527'),
       ('3cabe054-e4e3-4a6a-9158-965cf976d10f', 'Rápido como um Raio', 0, 'reacao', 'PUGILISTA', 'Pessoal.', NULL, NULL, NULL, NULL, 'Realiza um *"Ataque corpo a corpo"* adicional como uma <:acao_livre:1326585198892154901> ação livre contra uma criatura dentro do seu alcance.', NULL, NULL, NULL, NULL, '1c773acd-295b-436d-b792-8011e739e527'),
       ('4cd48055-f7db-4211-9280-5f973711b24a', 'Liderar por Exemplo', 1, 'acao bonus', 'ORC, INSPIRAÇÃO, VOZ', '20m.', 'Até o começo do seu próximo turno.', NULL, NULL, NULL, 'Escolha um atributo, a equipe fica ***Inspirada***, enquanto estiver ***Inspirado***, ela recebe **vantagem** sempre que realizar um teste com o atributo.', NULL, NULL, 'Criaturas a sua escolha.', 'Ilimitado.', '1c773acd-295b-436d-b792-8011e739e527'),
       ('a7d5f3c2-9b8e-4d6a-bc21-3e9f7a1d8e54', 'Modificar com Sangue', 1, 'acao bonus', 'SANGUIR', 'Toque.', 'Uma cena.', NULL, NULL, NULL, 'O equipamento afetado recebe um **descritor de equipamento** a sua escolha.', 'Você só pode usar essa habilidade uma vez por cena.', NULL, 'Uma arma.', 'Ilimitado.', '1c773acd-295b-436d-b792-8011e739e527'),
       ('27135a3f-ffe8-447a-a810-9aa424b1196c', 'Modificar com Sangue: Conjurar Manoplas', 0, 'acao bonus', 'SANGUIR, MÁGICO', 'Pessoal.', 'Uma cena.', NULL, NULL, NULL, 'O usuário conjura suas manoplas se sangue.', NULL, NULL, NULL, 'Ilimitado.', '1c773acd-295b-436d-b792-8011e739e527'),
       ('9c521e05-28b3-43ee-9e74-c912ae77b6ff', 'Echo of Pomona: Mashing Impact', 4, 'eop', 'EOP, VOZ', 'Pessoal.', 'No mínimo 3 turnos.', NULL, NULL, NULL, 'Adam fica em um estado de ***Concentração Extrema*** por no mínimo três turnos. Após o fim desse tempo, os ataques passam a precisar de testes, mas enquanto não errar no teste de ataque, os ataques continuam sendo críticos.', NULL, NULL, 'Você.', '1.', '1c773acd-295b-436d-b792-8011e739e527');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_PASSIVA}
VALUES ('4497c235-beb6-4391-830e-9e79883637ea', 'Ataque Poderoso', 'Você treinou seu corpo para ser capaz de desferir ataques poderosíssimos sempre que ataca. Seus **ATAQUES** com **ARMAS** recebem uma nova modificação.', '1c773acd-295b-436d-b792-8011e739e527'),
       ('65f11dac-d301-4f22-ad47-d9624e817a54', 'Renegociar', 'Para tudo existe um jeitinho, incluindo negociações. Você tem **vantagem** em testes de **CAR**.', '1c773acd-295b-436d-b792-8011e739e527'),
       ('14bcc54c-e187-4954-abd2-785b01d93e33', 'Combate Desarmado', 'Você torna-se proficiente em um tipo especial de ataques desarmados. Enquanto estiver com pelo menos uma mão livre, seus ataques desarmados recebem os descritores  **ARMA**, **CONTUNDENTE** e **LEVE**.', '1c773acd-295b-436d-b792-8011e739e527'),
       ('de754406-5a1b-4889-ae1b-229f7461b919', 'Façanha Desarmada', 'Você sabe golpear de maneira veloz, atacando com manobras perigosas. Seus ataques desarmados recebem uma modificação', '1c773acd-295b-436d-b792-8011e739e527'),
       ('7986f0dc-c082-4906-838a-36d991dad853', 'Cólera Ardente', 'Seu sangue quente é capaz de servir como combustível para sua ira controlada. Enquanto estiver ***Machucado***, seus **ATAQUES** recebem uma nova modificação.', '1c773acd-295b-436d-b792-8011e739e527'),
       ('4bdd7517-463b-4fb3-a9ad-991742ee45d4', 'Hidden Inventory', 'Você é capaz de guardar um item em sua sombra. Seu limite de peso aumentou em +4.', '1c773acd-295b-436d-b792-8011e739e527');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_TALENTO}
VALUES ('e51b04de-be2f-45dd-b0ac-2be1df797d20', 'Mata-dragão', 'Você recebe **vantagem** em *"Ataques de Superioridade"*. Ao acertar um **ATAQUE** contra uma criatura que você estiver **Agarrando**, você causa +2d6 pontos de dano **CONTUNDENTE**. Por fim, você pode agarrar criaturas maiores que você', '1c773acd-295b-436d-b792-8011e739e527'),
       ('4f91e227-2f58-45e0-b09b-31607c964455', 'Presas de Warpinier', 'Seu sangue maldito fez com que suas presas se tornassem verdadeiras armas, que podem ser usadas em momentos de adrenalina. Seus **ATAQUES** com o descritor **ARMA** recebem uma nova modificação.', '1c773acd-295b-436d-b792-8011e739e527'),
       ('3f9c1b74-8d2e-4a56-bb1c-2e7f5d8a90e3', 'Sangue Maldito', 'Seu sangue impregnado com a essência de Warpinier concede alguns privilégios. O usuário tem **resistência** a dano **ÁCIDO** e **NECRÓTICO**.', '1c773acd-295b-436d-b792-8011e739e527');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_ITEM}
VALUES ('f151bcbc-7fba-49f1-8ce9-90518c919078', 'Martelo de Guerra de Ferro Varmaniano', 'Um grande martelo de guerra pesado e contundente feito com ferro varmaniano, ideal para destruição. "Cê louco Adam, coitado do meninux, ficou parecendo o Perna Longa amassado, mas com um pouquinho a mais de gore..." — disse Chrollo no final da batalha do Quebra-copos de Alberich.', 322, 3),
       ('5222f2d2-1b90-42ae-9115-5973994e9e5b', 'Telefone Biomagitécnico de Chrollo', 'Uma caixa telefônica criada pelo Chrollo para manter contato com o grupo durante ambas as viagens. Para ligá-la basta tirar o fone do apoio o som viajará em os telefones. A caixa aparenta estar mais pesada do que deveria ser...', 0, 2),
       ('f73948ee-b811-4eda-8ac4-46471ae1c068', 'Armadura de Couro Batido', 'Proteção comum entre mercenários e aventureiros inexperientes, reforçada com pequenas placas de couro em locais estratégicos.', 40, 3),
       ('c037d236-b4c2-4cae-b744-60e1512668a8', 'Armadura de Cota de Malha', 'Proteção comum entre aventureiros e cavaleiros, feita com aço comprado em Alberich por Gunther. "Gunther, profidencie uma mesa de encantamentos e estantes de livros, pois encantarei está armadura com Protection IV." — disse Chrollo durante um de seus momentos alcolizado...', 100, 3);"""
    )
    cursor.execute(
        f"""{constantes.INSERT_ITENS_PERSONAGENS}
VALUES ('f151bcbc-7fba-49f1-8ce9-90518c919078', '1c773acd-295b-436d-b792-8011e739e527', 1),
       ('f73948ee-b811-4eda-8ac4-46471ae1c068', '1c773acd-295b-436d-b792-8011e739e527', 1),
       ('c037d236-b4c2-4cae-b744-60e1512668a8', '1c773acd-295b-436d-b792-8011e739e527', 1);"""
    )
    cursor.execute(
        f"""{constantes.INSERT_MODIFICADOR_SKILLS}
VALUES ('f3b9a7c1-2d8e-4f6a-bc21-7e9d5a1d8e54', '4e4e6145-0e4b-476b-a161-0aeebd169e19'),
       ('b2a9d7f3-8e4d-6c1d-bc71-3e9f7a5d8e54', '4e4e6145-0e4b-476b-a161-0aeebd169e19'),
       ('f3b9a7c1-2d8e-4f6a-bc21-7e9d5a1d8e54', '1fdfad97-eec6-4703-af0c-054a3ae09550'),
       ('b2a9d7f3-8e4d-6c1d-bc71-3e9f7a5d8e54', '1fdfad97-eec6-4703-af0c-054a3ae09550'),
       ('f3b9a7c1-2d8e-4f6a-bc21-7e9d5a1d8e54', '4666dab1-fc4a-40a5-9971-fba6d0e823f0'),
       ('b2a9d7f3-8e4d-6c1d-bc71-3e9f7a5d8e54', '4666dab1-fc4a-40a5-9971-fba6d0e823f0'),
       ('f3b9a7c1-2d8e-4f6a-bc21-7e9d5a1d8e54', '7aebae61-6619-437e-8576-6104f375a3f3'),
       ('b2a9d7f3-8e4d-6c1d-bc71-3e9f7a5d8e54', '7aebae61-6619-437e-8576-6104f375a3f3');"""
    )

    print("ADAM ADICIONADO")

    # --------------------------------------------------------------------------------------------

    # PROMPT GUNTHER

    reducao_de_dano = 2
    forca = ["10", "0"]
    destreza = ["12", "2"]    
    constituicao = ["13", "3"]
    inteligencia = ["9", "-1"]
    sabedoria = ["11", "1"]
    carisma = ["11", "1"]
    pericias = "'7b32de93-92b1-402a-93fe-c7a295535490', '98f70eea-9c31-44a4-8c66-2b1eca1a530a', '89056ec3-8736-4136-a962-e86434799d2c', '50e3508e-335c-42ef-97cf-1db7a07962c4', 'd0f44af5-c299-41c2-9e84-72dd9cdb7351','0222604e-cd4d-4077-b19f-7eb7c4e8c927'"

    cursor.execute(
        f"""{constantes.INSERT_PERSONAGEM}
VALUES ('e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8', 'Gunther Nosferata', 'Gunther', {level}, 'Pactuado', 'Especialista', 'Sanguir', 'Byotir', 'Você precisa ser convidado para entrar em qualquer propriedade que não lhe pertença, a menos que tenha deixado algum objeto pessoal seu lá dentro, sob o cuidado de outra pessoa do local. Sempre que for convidado para entrar em algum local, ganha 1 ponto de catarse', 0, {pe}, {pe}, {calc_hp(int(constituicao[1]), 1)}, {calc_hp(int(constituicao[1]), 1)}, 'hp', {reducao_de_dano}, {bonus_de_proficiencia}, 5, ARRAY[{pericias}]::UUID[], {int(forca[0])}, {int(forca[1])}, {int(destreza[0])}, {int(destreza[1])}, {int(constituicao[0])}, {int(constituicao[1])}, {int(inteligencia[0])}, {int(inteligencia[1])}, {int(sabedoria[0])}, {int(sabedoria[1])}, {int(carisma[0])}, {int(carisma[1])}, 10, {calc_liimite_peso(int(forca[1]))}, 'ÁCIDO, NECRÓTICO', NULL, NULL, 960, 'gunther.png', '<:gunther_token:1394716545980174516>', '813254664241414144', '8a87e68e-cd9d-46e5-953a-35942487ef1b');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_MODIFICADOR}
VALUES ('dd1e2e42-46c3-4ae7-b88d-624589d5fbd2', 'reacao', 'ADICIONA', '**Acerto:**  Você causa +{ataque_poderoso_especializado} pontos de dano do mesmo tipo.\n**Especial:** Você só pode causar esse dano adicional uma vez por turno.', 0, 'PE'),
       ('8ede89fe-95c4-4646-84df-9d31e82315fa', 'reacao', 'ADICIONA', '**Acerto:** Aumenta o dano adicional em +2d10. Você pode aplicar essa modificação quantas vezes quiser', 2, 'PE'),
       ('bbfa7ad2-37ec-43bc-b655-9f25f1f877cd', 'reacao', 'ADICIONA', '**Especial:** Ela fica ***Invisível*** a outras criaturas que não sejam você.', 1, 'PE'),
       ('1271001c-9241-4c8a-93be-4ad910f4399b', 'reacao', 'ADICIONA', '**Acerto:** +1d6 pontos de dano **PERFURANTE** e você recebe todos benefícios da característica *"Sangue Maldito"*, mas o alvo não fica com **desvantagem** em testes.', 2, 'PE'),
       ('cf1fa3ff-0ce8-4cda-b3ad-8b41d06223b7', 'reacao', 'ADICIONA', '**Efeito:** Você pode dever mais uma obrigação menor para receber vantagem no primeiro ataque que fizer com a arma na cena.', 0, 'PE');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_PASSIVA}
VALUES ('5bc5ecad-03dd-4e0d-abfe-5fa8bbb80771', 'Ataque Especializado', 'Você aprendeu a se virar em combate usando astúcia e conhecimento com suas armas. Seus **ATAQUES** com **vantagem** que causam dano recebem uma nova modificação.', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8'),
       ('45c0cd6c-13e5-48fd-af3e-9bd8e98c564f', 'Sangue Maldito', 'Seu sangue impregnado com a essência de Warpinier concede alguns privilégios. O usuário tem **resistência** a dano **ÁCIDO** e **NECRÓTICO**. Além disso, o usuário recebe a habilidade *"Sede de sangue"*.', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8'),
       ('66eed95f-1301-4121-a334-1526177cc8c5', 'Adequar-se ao Meio', 'Após usar a habilidade "*Receber Benção"*,o usuário recebe vantagem em todos os testes que envolvam esconder-se ou misturar-se a multidões.', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8'),
       ('3764ae33-efde-4191-92c2-d5455c4394e1', 'Hidden Inventory', 'Você é capaz de guardar um item em sua sombra. Seu limite de peso aumentou em +4.', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_SKILL}
VALUES ('12cccd1a-79fa-44ac-be51-e2c8ea5c22a3', 'Corte com a Foice com Corrente', 0, 'acao', ' ATAQUE, ARMA, LEVE, ARREMESÁVEL, CORTANTE, VERSÁTIL, SUPERIOR', '6m.', 'Instatânea.', '1d20 + {int(forca[1])} + {bonus_de_proficiencia} vs **FOR**.', '1d6 + 1d8 + {int(forca[1])} + {bonus_de_proficiencia}.', 'Caso você erre no teste de acerto, você solta a **ARMA** e terá que gastar sua <:acao_bonus:1326585197004722197> Ação Bônus para pegá-la novamente.', NULL, NULL, NULL, 'Uma criatura.', 'Ilimitado.', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8'),
       ('f53836e1-914b-4ca1-b713-cecd9d518e06', 'Infligir Ferimentos', 1, 'acao', 'ATAQUE, MÁGICO, NECRÓTICO', '1m.', 'Instântanea.', '1d20 + {int(carisma[1])} + {bonus_de_proficiencia} vs **CON**.', '3d10 + {bonus_de_proficiencia} pontos de dano **NECRÓTICO**.', 'O alvo sofre metade do dano.', NULL, NULL, NULL, 'Uma criatura.', 'Ilimitado.', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8'),
       ('d9f9dab4-913f-416c-9cf6-3690ba853f05', 'Disparo Arcano', 0, 'acao', 'ATAQUE, MÁGICO, DISPARO, MÁGICO, ENERGÉTICO', '18m.', 'Instantânea.', '1d20 + {int(carisma[1])} + {bonus_de_proficiencia} vs **FOR**.', 'O alvo sofre 2d10 + {bonus_de_proficiencia} pontos de dano do tipo **ENERGÉTICO**.', NULL, NULL, ' Você atira força mágica, na forma de um disparo arcano na direção do seu inimigo.', NULL, 'Uma criatura.', 'Ilimitado.', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8'),
       ('9b195835-4b3b-4d07-9a80-fa4497b61676', 'Convocar Lumine', 1, 'acao', 'TRUQUE, UTILITÁRIO, MÁGICA, CRIAÇÃO', '9m.', 'Uma cena.', NULL, NULL, NULL, 'Lumine usa seu chapéu para voltar para o plano material. Do chapéu, surge algumas patinhas, garras e um pequeno olho brilhante. Ela permanece pela duração da magia ou até quando ela queira ir embora. Você pode usar sua <:acao_livre:1326585198892154901> Ação Livre para pedir que ela faça algo, podendo interagir com itens e com o ambiente. Ela pode se distânciar de você em até 9m.', 'Ela não pode atacar, ativar itens mágicos ou carregar mais de 5 volumes. Além disso, ela  desaparece se ficar a mais de 9m do conjurador ou se você conjurar a magia novamente.', NULL, 'Ponto no alcance.', 'Ilimitado.', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8'),
       ('59951d9d-3c3e-496b-9491-e7b7554c04ef', 'Transmutar Pacto em Arma', 2, 'acao', 'PACTUADO, MÁGICO', 'Toque.', 'Uma cena.', NULL, NULL, NULL, 'Você canaliza a força de Lumine no objeto. Ele se transforma numa arma que você seja proficiente e você pode usar seu **bônus de proficiência**, em vez de **FOR** ou **DES**, para as jogadas de ataque e dano com ela.', NULL, NULL, 'Um objeto mundano que você esteja empunhando.', 'Ilimitado.', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8'),
       ('cd6acb0f-d656-429b-acf2-4987a61d00dc', 'Modificar com Sangue', 1, 'acao bonus', 'SANGUIR', 'Toque.', 'Uma cena.', NULL, NULL, NULL, 'O equipamento afetado recebe um descritor de equipamento a sua escolha.', 'Você só pode usar essa habilidade uma  vez por cena.', NULL, 'Uma arma.', 'Ilimitado.', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8'),
       ('88a87ee1-e31f-4985-914e-a040408cf8af', 'Sede de sangue', 0, 'acao bonus', 'ATAQUE, SANGUIR', 'Toque.', 'Instântanea.', '1d20 + {int(forca[1])} vs **FOR**', NULL, NULL, 'O usuário morde o alvo no pescoço, infectando-o com a essência de Warpinier, o alvo fica com *desvantagens** em todos os testes por 24 horas. Além disso, o usuário restaura 5 pontos de HP temporários e pode escolher uma doença, um veneno ou uma  condição (entre _**Atordoado**_, _**Desorientado**_, _**Encantado**_, _**Envenenado**_ ou _**Paralisado**_) que esteja afetando o usuário. Você encerra seu efeito.', NULL, NULL, 'Uma criatura humanoide.', 'Ilimitado.', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8'),
       ('e684f3b6-b5ff-44f7-8507-aa8f2e9f9085', 'Cambalhota Especializada!', 1, 'reacao', 'ESPECIALISTA', 'Pessoal.', 'Instatânea.', NULL, NULL, NULL, 'Você fica ***Caído*** e recebe **resistência** contra o dano do ataque.', NULL, 'Você é acertado por um ataque que não tenha sido realizado com **vantagem**.', 'Você.', 'Ilimitado.', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8'),
       ('ccbeb133-a5d9-4ad0-a4d9-00a29b2a6998', 'Alimentos das Chamas', 2, 'acao', 'BENÇÃO, MÁGICO', 'Visão.', 'Instântanea.', '1d20 + {bonus_de_proficiencia} vs **CAR**.', 'O usuário descobre o que aquela criatura mais deseja (naquela cena).', 'O usuário só pode usar essa habilidade se tiver usado a habilidade "*Receber Benção"*', 'Nenhuma outra personagem ou criatura sabe que você usou essa habilidade.', NULL, NULL, 'Uma criatura.', 'Ilimitado.', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8'),
       ('10d0b1df-e399-4d2f-bd8f-01e0f1ad6b89', 'Corte com Morganas Deathmetal', 0, 'acao', 'ATAQUE, CORTANTE, PESADO, ARMA', '6m.', 'Instântanea.', '1d20 + {int(forca[1])}', '2d6 + {bonus_de_proficiencia} de pontos de dano.', 'A espada cai', NULL, 'Se o usuário estiver ***Machucado***, ele ganha +1 em testes de ataque.', NULL, 'Uma criatura', '2', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8'),
       ('e7c94b4a-28cb-4a44-956b-1c7ebcf1a0a0', 'Morganas Deathmetal: Sigilo', 1, 'acao', 'ATAQUE, CORTANTE, PESADO, MÁGICO, ARMA', '6m.', 'Instântanea.', '1d20 + {int(forca[1])} + {bonus_de_proficiencia}.', '2d6 + 1d6 + {bonus_de_proficiencia} de dano escolhido de dano. ', 'A espada cai', NULL, 'Se o usuário estiver ***Machucado***, ele ganha +1 em testes de ataque.\nO usuário deve escolher o tipo de dano (ígneo, frio, ácido ou elétrico) com uma <:acao_bonus:1326585197004722197> ação bônus com antecedência', NULL, 'Criaturas em um raio de 2m.', '{bonus_de_proficiencia}', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8');"""
        #    ('309f9471-f79c-41b6-a6dc-ad3b02ab3155', 'Presença de Lumine', 0, 'acao bonus', 'PACTUADO, MÁGICO', 'Pessoal.', 'Instantânea.', NULL, NULL, 'Ela não falará com você até o começo da próxima rodada.', 'Através dos símbolos em suas mãos, você possui conexão com Lumine, uma entidade poderosa. Caso você agrade Lumine, poderá pedir favores à ela; podendo pedir itens, pontos de ênfase, pontos de catarse, pontos de vida, etc:\n\nFavores pequenos -> itens básicos, pontos de vida (1d6), informação básica da cena. (todas essas recompensas são apenas para o usuário):\n- Entregar um item básico (Lumine pode aceitar ou não dependendo do item ou da quantidade).\n- Eliminar um inimigo ({{vida do inimigo}} >= 35)\n- Fazer uma ação honrável\n...\n\nFavores maiores ->  item raro, pontos de vida(2d4 + 2), pontos de catarse(1d3), pontos de ênfase(1d4), informação importante da cena. (todos essas recompensas podem ser para qualquer pessoa da equipe)\n- Entregar um item raro/importante/valioso (Lumine pode aceitar ou não dependendo do item ou da quantidade)\n- Eliminar um inimigo ({{vida do inimigo}} <= 35)\n - Passar um dia com um combate sem tomar dano\n- Fazer Lumine rir. Para fazer esse favor existe dois meios: O usuário pode contar uma piada ao mestre, se o mestre achar engraçado, o usuário pode pedir sua recompensa; O usuário faz um teste de 1d20 + bônus de **CAR** (podendo usar catarse ou buffs), se o resultado for maior ou igual a 16, o usuário pode pedir sua recompensa.', 'O jogador pode tentar negociar outro favores com o mestre. Caso as duas mãos do usuários sejam danificadas de forma extrema ou coberta com algo espeço, a conexão com Lumine pode ser perdida. Mas caso apenas uma das mãos seja danificada, o usuário fica com **desvantagem** nos testes da habilidade.', NULL, 'Pessoal.', '{bonus_de_proficiencia}', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8')
    )
    cursor.execute(
        f"""{constantes.INSERT_TALENTO}
VALUES ('6b2c8b3b-4c75-4daf-a2de-3f6a0a7a8d83', 'Presas de Warpinier', 'Seu sangue maldito fez com que suas presas se tornassem verdadeiras armas, que podem ser usadas em momentos de adrenalina. Seus **ATAQUES** com o descritor **ARMA** recebem uma nova modificação.', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8'),
       ('d34c41e1-2f59-4fb9-9429-7dd122e62b19', 'Crítico Forçado', 'Ao acertar um **ATAQUE**, você pode dever um favor maior para fazer com que esse acerto conte como um acerto crítico. Esse talento só pode ser usado uma vez por dia.', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8'),
       ('656ed8ac-b6ec-4577-a240-3f63e744242b', 'Especialização Máxima', 'Sempre que você ou um aliado usar seu dado de *"Ataque Especializado"*, você pode dever um favor menor para fazer com que o dado tenha seu valor máximo, sem precisar ser jogado.', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_ITEM}
VALUES ('e6fa95b9-b04c-4f40-88e0-195a0488f0de', 'Foice e Corrente', 'Combinação da fo ice ligada a corrente, para ataque versáteis. "Como essa corrente voltou para você depois que o Tristane desamarrou o Clebim?" — disse Chrollo, questinando a ordem dos fatos durante a batalha contra Warpinier.', 25, 3),
       ('9b8e370b-29f3-470f-bd50-e52f8719f76a', 'Morganas Deathmetal', 'Uma espada feita com os restos da antiga guitarra de Morgana. "No dia que você fizer mais de 6 kills com ela a gente conversa..." — disse Chrollo, concretizando a superioriodade da Masked Death', 350, 3),
       ('99387f37-b128-4e88-a9e6-ca918a2d4b41', 'Poção de Cura Pequena', 'Você recupera 2d4+2 pontos de vida quando bebe esta poção.', 250, 1),
       ('5f219452-0438-40e4-ba90-d28ff16144c9', 'Poção de Cura Média', 'Você recupera 4d4+4 pontos de vida quando bebe esta poção.', 500, 2),
       ('a9cff25f-aa4c-4e49-9f02-3905867f01d2', 'Armadura de Couro Batido', 'Proteção comum entre mercenários e aventureiros inexperientes, reforçada com pequenas placas de couro em locais estratégicos.', 40, 3),
       ('e2201d5c-940d-4e31-9479-c9928ca1e86e', 'Favor Maior', 'Um favor menor que Lumine te deve pode ser trocado usando a habilidade *"Presença de Lumine"*. "Já parou para pensar que os únicos que não tem ma mega relação com alguma entidade sou eu, o Adam e o Vincenzo?" — disse Chrollo durante o último jantar em Alberich.', 0, 0),
       ('79ead6b2-acca-4d7f-aaba-cb4614900afd', 'Favor Menor', 'Um favor maior que Lumine te deve pode ser trocado usando a habilidade *"Presença de Lumine"*. "Se eu não for o próximo a arranjar uma divindade pra me patrocinar, eu pulo do pé de melância..." — disse Chrollo durante o último jantar em Alberich.', 0, 0);"""
    )
    cursor.execute(
        f"""{constantes.INSERT_ITENS_PERSONAGENS}
VALUES ('e6fa95b9-b04c-4f40-88e0-195a0488f0de', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8', 1),
       ('9b8e370b-29f3-470f-bd50-e52f8719f76a', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8', 1),
       ('99387f37-b128-4e88-a9e6-ca918a2d4b41', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8', 3),
       ('5f219452-0438-40e4-ba90-d28ff16144c9', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8', 1),
       ('a9cff25f-aa4c-4e49-9f02-3905867f01d2', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8', 1),
       ('e2201d5c-940d-4e31-9479-c9928ca1e86e', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8', 0),
       ('79ead6b2-acca-4d7f-aaba-cb4614900afd', 'e3f9a5b4-8c6d-4a70-94ff-2b6d2c42e6c8', 0);"""
    )
    cursor.execute(
        f"""{constantes.INSERT_MODIFICADOR_SKILLS}
VALUES ('12cccd1a-79fa-44ac-be51-e2c8ea5c22a3', 'dd1e2e42-46c3-4ae7-b88d-624589d5fbd2'),
       ('f53836e1-914b-4ca1-b713-cecd9d518e06', 'dd1e2e42-46c3-4ae7-b88d-624589d5fbd2'),
       ('d9f9dab4-913f-416c-9cf6-3690ba853f05', 'dd1e2e42-46c3-4ae7-b88d-624589d5fbd2'),
       ('88a87ee1-e31f-4985-914e-a040408cf8af', 'dd1e2e42-46c3-4ae7-b88d-624589d5fbd2'),
       ('e7c94b4a-28cb-4a44-956b-1c7ebcf1a0a0', 'dd1e2e42-46c3-4ae7-b88d-624589d5fbd2'),
       ('10d0b1df-e399-4d2f-bd8f-01e0f1ad6b89', 'dd1e2e42-46c3-4ae7-b88d-624589d5fbd2'),
       ('f53836e1-914b-4ca1-b713-cecd9d518e06', '8ede89fe-95c4-4646-84df-9d31e82315fa'),
       ('9b195835-4b3b-4d07-9a80-fa4497b61676', 'bbfa7ad2-37ec-43bc-b655-9f25f1f877cd'),
       ('12cccd1a-79fa-44ac-be51-e2c8ea5c22a3', '1271001c-9241-4c8a-93be-4ad910f4399b'),
       ('10d0b1df-e399-4d2f-bd8f-01e0f1ad6b89', '1271001c-9241-4c8a-93be-4ad910f4399b'),
       ('e7c94b4a-28cb-4a44-956b-1c7ebcf1a0a0', '1271001c-9241-4c8a-93be-4ad910f4399b'),
       ('59951d9d-3c3e-496b-9491-e7b7554c04ef', 'cf1fa3ff-0ce8-4cda-b3ad-8b41d06223b7');"""
    )

    print("GUNTHER ADICIONADO")

    # --------------------------------------------------------------------------------------------

    # PROMPT DO VINCENZO

    reducao_de_dano = 2
    forca = ["14", "3"]
    destreza = ["13", "2"]
    constituicao = ["12", "1"]
    inteligencia = ["11", "1"]
    sabedoria = ["10", "0"]
    carisma = ["9", "-1"]
    pericias = "'89056ec3-8736-4136-a962-e86434799d2c', 'd0f44af5-c299-41c2-9e84-72dd9cdb7351', '110bf214-eb58-4c0b-8c4c-6eba30302575', 'd28b4723-1177-46ac-b1f2-bf785330b1a9', '71850f9a-22d3-441a-b675-8858d8718984', '62ef595a-2f6e-475c-8152-3f36a5c4e695'"

    cursor.execute(
        f"""{constantes.INSERT_PERSONAGEM}
VALUES ('a69e5fee-70c8-47d2-b8f8-6364f08b87d0', 'Vincenzo LeBlanc', 'Vincenzo', {level}, 'Mestre das Feras', 'Especialista', 'Elfo Instável', 'Corte do Outono e Inverno', 'As pessoas conversam… mas o mundo fala mais alto, e quase ninguém parece escutar. Uma vez por cena, você ganha 1 ponto de catarse sempre que sua leitura exagerada do ambiente ou intenções se distoarem do restante do grupo.', 0, {pe}, {pe}, {calc_hp(int(constituicao[1]), 1)}, {calc_hp(int(constituicao[1]), 1)}, 'hp', {reducao_de_dano}, {bonus_de_proficiencia}, 0, ARRAY[{pericias}]::UUID[], {int(forca[0])}, {int(forca[1])}, {int(destreza[0])}, {int(destreza[1])}, {int(constituicao[0])}, {int(constituicao[1])}, {int(inteligencia[0])}, {int(inteligencia[1])}, {int(sabedoria[0])}, {int(sabedoria[1])}, {int(sabedoria[0])}, {int(sabedoria[1])}, 10, {calc_liimite_peso(int(forca[1])) + 4}, 'ESPECIAL', 'NECRÓTICO', NULL, 100, 'vincenzo.png', '<:vincenzo_token:1394716556382044301>', '1119222124368896020', '8a87e68e-cd9d-46e5-953a-35942487ef1b');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_MODIFICADOR}
VALUES ('6fd6b07d-37f5-4ff2-9dc1-6bd54d33231a', 'reacao', 'ADICIONA', '**Acerto:**  Você causa +{ataque_poderoso_especializado} pontos de dano do mesmo tipo.\n**Especial:** Você só pode causar esse dano adicional uma vez por turno.', 0, 'PE'),
       ('298c79ca-b5a3-4e4c-aa6b-6da9b69f2c92', 'reacao', 'ADICIONA', '**Especial:** na primeira vez que o efeito adicional for acabar, você pode gastar uma <:reacao:1326585200519544885> reação para fazer com que ele dure mais uma rodada.', 1, 'PC'),
       ('db4eebe9-fd7f-4b67-8bf0-580dec107170', 'reacao', 'ADICIONA', '**Efeito:** o alvo recupera +1d8+1 pontos de vida adicionais.', 2, 'PE');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_SKILL}
VALUES ('bdcaaf43-93af-4979-b1eb-46bd80798415', 'Comandar Zênite', 0, 'acao bonus', 'MESTRE DAS FERAS, VOZ', '9m.', 'Instantânea.', NULL, NULL, NULL, 'Zênite realiza uma ação de sua ficha, o PE da habilidade é consumido da sua ficha.', NULL, NULL, NULL, 'Ilimitado.', 'a69e5fee-70c8-47d2-b8f8-6364f08b87d0'),
       ('1d52b8d1-117a-471f-ab86-b33750361670', 'Corte com as Lâminas Duplas', 1, 'acao livre', 'ATAQUE, ARMA, DUPLA, LEVE, CORTANTE', '2m.', 'Instatânea.', '1d20 + {int(forca[1])} + {bonus_de_proficiencia} vs **DES**.', '1d8 + {bonus_de_proficiencia} pontos de dano **CORTANTE**', 'Caso você erre no teste de acerto, você solta a **ARMA** e terá que gastar sua <:acao_bonus:1326585197004722197> Ação Bônus para pegá-la novamente.', NULL, NULL, NULL, 'Uma criatura.', 'Ilimitado.', 'a69e5fee-70c8-47d2-b8f8-6364f08b87d0'),
       ('f7bd9cec-072c-4c27-b575-a8ea5b65642f', 'Disparo com a Soul Guitar', 0, 'acao', 'DISPARO, PERFURANTE, PRECISO, ARMA, ATAQUE', '18m.', 'Instantânea.', '1d20 + {int(destreza[1])} vs **DES**.', '1d8 pontos de dano.', 'Caso você erre no teste de acerto, você solta a **ARMA** e terá que gastar sua <:acao_bonus:1326585197004722197> Ação Bônus para pegá-la novamente.', 'O usuário aplica +1 nível de ***Shadow Cover***.', NULL, NULL, 'Uma criatura.', 'Ilimitado.', 'a69e5fee-70c8-47d2-b8f8-6364f08b87d0'),
       ('1a65506a-90ab-4943-ab99-a5aaab829dc7', 'Echo of Pomona: Energy Concentration', 4, 'eop', 'EOP, VOZ', '18m.', 'Instantânea.', NULL, '3d10 pontos de dano **ELÉTRICO**.', NULL, 'Vincenzo concentra resquísios da energia de Pomona próximo ao alvo, criando uma esfera de energia, que ao acertar, deixa o alvo ***Paralisado***.', NULL, NULL, 'Criaturas em um diâmetro de 3m.', '1.', 'a69e5fee-70c8-47d2-b8f8-6364f08b87d0'),
       ('f6de97df-ce9b-4c2a-a985-564dd3f84460', 'Cambalhota Especializada!', 1, 'reacao', 'ESPECIALISTA', 'Pessoal.', 'Instatânea.', NULL, NULL, NULL, 'Você fica ***Caído*** e recebe **resistência** contra o dano do ataque.', NULL, 'Você é acertado por um ataque que não tenha sido realizado com **vantagem**.', 'Você.', 'Ilimitado.', 'a69e5fee-70c8-47d2-b8f8-6364f08b87d0'),
       ('4f7af3fe-0880-4463-b0f3-2991d70ff34a', 'Curar Ferimentos', 1, 'acao', 'SUPERFICIAL, CONTROLE, MÁGICO, CURA', 'Toque.', 'Instantânea.', NULL, NULL, NULL, 'O alvo recupera uma quantidade de pontos de vida igual a 2d8 + {bonus_de_proficiencia}.', 'Essa magia não tem efeito sobre mortos-vivos ou constructos e cura apenas uma carga de vida de invocações.', NULL, 'Uma criatura.', 'Ilimitado,', 'a69e5fee-70c8-47d2-b8f8-6364f08b87d0'),
       ('7e18ed9c-d9e6-4d6d-b14d-fded08dd779d', 'Raio Elemental de Terra', 0, 'acao', 'TRUQUE, OFENSIVO, ATAQUE, MÁGICO, ELEMENTAL', '18m.', 'Instantânea.', '1dd20 + {int(inteligencia[1])} + {bonus_de_proficiencia}', '2d8 + {bonus_de_proficiencia}', NULL, 'O alvo fica **Desprotegido (Físico)** contra o próximo ataque contra uma **Proteção** física que sofrer até o final do seu próximo turno.', NULL, NULL, 'Uma criatura.', 'Ilimitado.', 'a69e5fee-70c8-47d2-b8f8-6364f08b87d0');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_PASSIVA}
VALUES ('dea6225c-1812-4d1d-b1c8-a24fe7167734', 'Eco Instável', 'Pomona usou suas últimas energias para trazer seu echo devolta para Opath, isso resultou em uma estranha instabilidade para seu echo. Você possui as características de duas heranças de seu legado.', 'a69e5fee-70c8-47d2-b8f8-6364f08b87d0'),
       ('2a580620-ac28-4f5c-9c5c-0573cf3f602b', 'Façanha de Duas Armas', 'Você é como um tornado, atacando seus oponentes com ataques rápidos com suas armas irmãs. Alguns de seus *"Cortes com as Lâminas Duplas"* recebem uma nova modificação.', 'a69e5fee-70c8-47d2-b8f8-6364f08b87d0'),
       ('4972805e-8fec-4d83-86d1-f3db62965fb2', 'Pele de Casca', 'Ao tornar-se parte da Corte da Primavera, o usuáario também se conecta com uma das árvores ancestrais de Sarfo e sua pele começa a ficar dura como uma casca de árvore. Você recebe +1 nas suas **proteções** físicas.', 'a69e5fee-70c8-47d2-b8f8-6364f08b87d0'),
       ('652d92be-b240-48e9-97ef-61ad6e6b2d30', 'Conexão com o Ambiente', 'Você sabe resistir aos percalços do caminho. Você tem **resistência** a dano do tipo **ESPECIAL**.', 'a69e5fee-70c8-47d2-b8f8-6364f08b87d0'),
       ('d6a15410-35cd-4c43-beff-79a244e0208a', 'Negue a Escuridão', 'Ao tornar-se um devoto dA Morte, você abandona seus pontos de sombra. A partir desse momento, não pode mais negociar com essa entidade. Os pontos de sombra abandonados tornam-se Efígies, as Moedas dA Morte, que aparecem magicamente no seu bolso. Enquanto tiver Efígies, você pode recuperar PV normalmente, mas é vulnerável a dano **NECRÓTICO**. Quando não tiver mais Efígies, não pode mais recuperar pontos de vida (exceto por descanso), e quando for reduzido a 0 pontos de vida ou menos, você morre instantaneamente. Sempre que for para o corredor da morte, antes de fazer o teste de morte, você pode escolher gastar uma de suas Efígies. Se o fizer, você retorna com 1 PV.', 'a69e5fee-70c8-47d2-b8f8-6364f08b87d0'),
       ('35551e36-345c-4b08-ad7e-c58b4f1e3da2', 'Companheiro Animal', 'Você criou um vínculo forte com uma criatura que age como seu companheiro animal, Zênite, um animal metamorfo. ', 'a69e5fee-70c8-47d2-b8f8-6364f08b87d0'),
       ('a1101a8a-0996-4b82-a4b0-35c4dfe32dcd', 'Hidden Inventory', 'Você é capaz de guardar um item em sua sombra. Seu limite de peso aumentou em +4.', 'a69e5fee-70c8-47d2-b8f8-6364f08b87d0');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_TALENTO}
VALUES ('6b033703-6269-4997-8fb5-a52c155a57d8', 'Explorador Feral', 'Seu companheiro animal passa a poder ocupar uma função durante Cenas de Exploração. Por fim, seu companheiro animal ignora terreno difícil natural.', 'a69e5fee-70c8-47d2-b8f8-6364f08b87d0');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_ITEM}
VALUES ('7f123601-d48c-4a50-93f2-91fef0b16b60', 'Lâminas Duplas de Aço Varmaniano', 'Um grande par de láminas estranhamente leves encontradas na salão de Warpinier. "Como você ficou tão bom em usar duas espadas do nada?" — questionou Chrollo durante a batalha contra a Facção Sanguir.', 330, 4),
       ('0c94309b-cd29-4945-a539-b420ada16652', 'Soul Guitar', 'Um rifre de pólvora disfaçado de guitarra que antes pertencia a Skeleton.', 100, 3),
       ('57c9c80e-10e2-4659-9cbc-1e1a4812ad56', 'Armadura de Couro Batido', 'Proteção comum entre mercenários e aventureiros inexperientes, reforçada com pequenas placas de couro em locais estratégicos.', 40, 3),
       ('18c8a946-3e2a-4f2f-ac79-d56c6764e3f9', 'Efígies', 'São as moedas dA Morte, frutos da sua rejeição à Sombra.', 0, 0);"""
    )
    cursor.execute(
        f"""{constantes.INSERT_ITENS_PERSONAGENS}
VALUES ('7f123601-d48c-4a50-93f2-91fef0b16b60', 'a69e5fee-70c8-47d2-b8f8-6364f08b87d0', 1),
       ('0c94309b-cd29-4945-a539-b420ada16652', 'a69e5fee-70c8-47d2-b8f8-6364f08b87d0', 1),
       ('57c9c80e-10e2-4659-9cbc-1e1a4812ad56', 'a69e5fee-70c8-47d2-b8f8-6364f08b87d0', 1),
       ('18c8a946-3e2a-4f2f-ac79-d56c6764e3f9', 'a69e5fee-70c8-47d2-b8f8-6364f08b87d0', 5);"""
    )
    cursor.execute(
        f"""{constantes.INSERT_MODIFICADOR_SKILLS}
VALUES ('135b9b63-dec7-4378-b2a1-a2bfe1350869', '6fd6b07d-37f5-4ff2-9dc1-6bd54d33231a'),
       ('f7bd9cec-072c-4c27-b575-a8ea5b65642f', '6fd6b07d-37f5-4ff2-9dc1-6bd54d33231a'),
       ('7e18ed9c-d9e6-4d6d-b14d-fded08dd779d', '298c79ca-b5a3-4e4c-aa6b-6da9b69f2c92'),
       ('4f7af3fe-0880-4463-b0f3-2991d70ff34a', 'db4eebe9-fd7f-4b67-8bf0-580dec107170');"""
    )
    print("VINCENZO ADICIONADO")

    # --------------------------------------------------------------------------------------------

    # PROMPT DO TSUKO

    reducao_de_dano = 0
    forca = ["14", "3"]
    destreza = ["12", "1"]
    constituicao = ["13", "2"]
    inteligencia = ["11", "1"]
    sabedoria = ["10", "0"]
    carisma = ["9", "-1"]
    pericias = "'a052505a-add0-4717-9d30-e382a0741058', '50e3508e-335c-42ef-97cf-1db7a07962c4', '3bc86566-ec94-4459-a7fc-2a5d094a1f39', '62ef595a-2f6e-475c-8152-3f36a5c4e695', '89056ec3-8736-4136-a962-e86434799d2c'"

    cursor.execute(
        f"""{constantes.INSERT_PERSONAGEM}
VALUES ('7eac7b56-f4d4-4177-89d6-748da17b531c', 'Hangetsu Tsuko', 'Tsuko', {level}, 'Tatsunoko', 'Combatente', 'Elementarista', 'Cromático', '', 0, {pe}, {pe}, {calc_hp(int(constituicao[1]), 0)}, {calc_hp(int(constituicao[1]), 0)}, 'hp', {reducao_de_dano}, {bonus_de_proficiencia}, 5, ARRAY[{pericias}]::UUID[], {int(forca[0])}, {int(forca[1])}, {int(destreza[0])}, {int(destreza[1])}, {int(constituicao[0])}, {int(constituicao[1])}, {int(inteligencia[0])}, {int(inteligencia[1])}, {int(sabedoria[0])}, {int(sabedoria[1])}, {int(carisma[0])}, {int(carisma[1])}, 5, {calc_liimite_peso(int(forca[1]))}, 'GÉLIDO, ÍGENO', 'vulnerabilidade', NULL, 100, 'tsuko.png', '<:tsuko_token:1394716553278394438>', '1296616660454604830', '8a87e68e-cd9d-46e5-953a-35942487ef1b');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_MODIFICADOR}
VALUES ('b236cf6b-4008-4308-adba-f669f5da7d57', 'reacao', 'AMPLIAR + 15', '**Acerto:** você causa +2d8 pontos de dano do mesmo tipo.', 0, 'PE'),
       ('eb226b4a-1f19-495c-92d9-e7388a55aebe', 'reacao', 'ADICIONA', '**Efeito:** O alvo fica ***Marcado +1***. Caso tenha usado seu *"Ataque Poderoso"*, adicione mais uma marca.\n**Acerto:** O alvo sofre +1d6 pontos de dano **ÍGNEO** para cada contador de ***Marcado*** que ele tiver. A quantidade máxima de dados de dano que podem ser causados dessa maneira é igual ao seu atributo-chave de conjuração.', 1, 'PE');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_SKILL}
VALUES ('fb6a3cc7-2021-41d7-8042-f0daf35e78b7', 'Ataque de Superioridade', 0, 'acao', 'ATAQUE', '2m.', 'Instantânea.', '1d20 + {int(forca[1])} vs **FOR**.', 'Você deve escolher um efeito entre: Deixar o alvo ***Caído***; Pegar um item do alvo; Deixar o alvo ***Agarrado***.', NULL, NULL, 'Você só pode usar essa habilidade em criaturas de seu tamanho ou menor.', NULL, 'Uma criatura.', 'Ilimitado.', '7eac7b56-f4d4-4177-89d6-748da17b531c'),
       ('d7fa1a69-9bfc-4e27-8a1b-d406a64d754c', 'Nenrō', 2, 'acao bonus', 'ELEMENTARISTA, ELEMENTAL, ASPECTO, AURA', 'Pessoal.', 'Uma cena.', NULL, NULL, NULL, 'O usuário entra em estado de afinidade com o fogo, confrome oo caminho do Enken-ryū. Enquanto estiver em afinidade com ele, você recebe **resistência** ao dano **ÍGNEO** e pode somar seu **bônus de proficiência** ao dano de seus ataques com o descritor **ÍGNEO**.', NULL, NULL, 'Pessoal.', 'Ilimitado.', '7eac7b56-f4d4-4177-89d6-748da17b531c'),
       ('798ba218-6874-48fe-bde8-3264b263291b', 'Primeira Forma: Enkō', 0, 'acao bonus', 'ELEMENTARISTA, ÍGNEO, MANOBRA ELEMENTAL', NULL, 'Até o final do seu próximo turno.', NULL, NULL, NULL, 'Sempre que for acertado por um  **ATAQUE** corpo a corpo, a criatura que o atacou sofre 2d6 pontos de dano **ÍGNEO**.', 'O usuário precisa estar em afinidade elemental para usar essa habilidade.', NULL, 'Você.', 'Ilimitado.', '7eac7b56-f4d4-4177-89d6-748da17b531c'),
       ('158702ec-4a4c-495b-8880-eb58f9dc811f', 'Segunda Forma: Honōki', 0, 'reacao', 'ELEMENTARISTA, ÍGNEO, ASPECTO', NULL, 'Instântanea.', NULL, NULL, NULL, 'O usuário manifesta uma aura ígnea de 3m e todos os aliados dentro da aura recebem resistência a dano **ÍGNEO**. No começo do seu próximo turno você pode usar 1 ponto de ênfase para manter a aura ativada por mais um turno.', 'O usuário precisa estar em afinidade elemental para usar essa habilidade. O usuário pode usar essa habilidade uma vez por cena.', 'Um aliado adjacente é sofre um ataque **ÍGNEO**.', 'Você.', 'Ilimitado.', '7eac7b56-f4d4-4177-89d6-748da17b531c'),
       ('92b15962-8e60-4fef-9e9c-2301648aa461', 'Terceira Forma: Kiretsu', 0, 'acao bonus', 'ELEMENTARISTA, ATAQUE, ÍGNEO, MÁGICO, MANOBRA ELEMENTAL', '9m.', 'Instantânea.', '1d20 + {bonus_de_proficiencia} + {int(forca[1])} vs **DES**.', '2d10 + {bonus_de_proficiencia} pontos de dano **ÍGNEO**.', 'Metade do dano.', NULL, 'O usuário precisa estar em afinidade elemental para usar essa habilidade.', NULL, 'Uma criatura no alcance.', 'Ilimitado.', '7eac7b56-f4d4-4177-89d6-748da17b531c'),
       ('fe9dbd56-2cef-4e91-acdb-f3af604fbb6e', 'Quarta Forma: Kenryùgako', 1, 'acao bonus', 'ELEMENTARISTA, ÍGNEO, MANOBRA ELEMENTAL', '9m.', 'Até o final do seu próximo turno.', NULL, NULL, NULL, 'O próximo **ATAQUE** que a criatura acertar causa +1d8 pontos de dano **ÍGNEO** com o qual você está em afinidade.', 'O usuário precisa estar em afinidade elemental para usar essa habilidade.', NULL, 'Uma criatura voluntária.', 'Ilimitado.', '7eac7b56-f4d4-4177-89d6-748da17b531c'),
       ('ff536b2a-be78-4f92-8cba-3d1ab1a1942a', 'Quinta Forma: Sanretsuzan', 1, 'acao', 'ELEMENTARISTA, ÍGNEO, MANOBRA ELEMENTAL, ATAQUE', '2m.', 'Instatânea.', '1d20 + {int(forca[1])} + {bonus_de_proficiencia} vs **DES**.', '2d12 + 1d10 + {bonus_de_proficiencia} pontos de dano **ÍGNEO**', 'Caso você erre no teste de acerto, você solta a **ARMA** e terá que gastar sua <:acao_bonus:1326585197004722197> Ação Bônus para pegá-la novamente.', NULL, 'O usuário precisa estar em afinidade elemental para usar essa habilidade.', NULL, 'Uma criatura.', 'Ilimitado.', '7eac7b56-f4d4-4177-89d6-748da17b531c'),
       ('1ebb3ce6-f374-4cae-a7d1-0f4a820a8afc', 'Corte com a Yedo', 0, 'acao', 'ATAQUE, CORTANTE, VERSÁTIL', '2m.', 'Instatânea.', '1d20 + {int(forca[1])} + {bonus_de_proficiencia} vs **DES**.', '1d8 + 1d10 + {bonus_de_proficiencia} pontos de dano **CORTANTE**', 'Caso você erre no teste de acerto, você solta a **ARMA** e terá que gastar sua <:acao_bonus:1326585197004722197> Ação Bônus para pegá-la novamente.', NULL, NULL, NULL, 'Uma criatura.', 'Ilimitado.', '7eac7b56-f4d4-4177-89d6-748da17b531c');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_PASSIVA}
VALUES ('c596b6bf-dde3-4df0-b662-647874bb7d83', 'Ataque Poderoso', 'Você treinou seu corpo para ser capaz de desferir ataques poderosíssimos sempre que ataca. Seus **ATAQUES** com **ARMAS** recebem uma nova modificação.', '7eac7b56-f4d4-4177-89d6-748da17b531c'),
       ('6bc14a6b-d6d6-41eb-8093-c23c3a123ce4', 'Combate com uma Arma', 'Você recebe +1 em todas as **Proteções** físicas e em jogadas de dano enquanto estiver empunhando uma arma em uma mão e estiver com a outra mão livre.', '7eac7b56-f4d4-4177-89d6-748da17b531c'),
       ('2a928811-7aba-404f-8da7-88a59d039e89', 'Façanha com uma Arma', 'Sua principal estratégia de combate consiste em atacar com precisão e deslocar-se para uma posição vantajosa. Se seu primeiro ataque em um combate for com sua arma, ele será feito com **vantagem**.', '7eac7b56-f4d4-4177-89d6-748da17b531c'),
       ('1b3bc403-8932-43b4-a244-e4dd5c134e4c', 'Servo Elemental', 'Você recebe **resistência** a dano **ELÉTRICO**.', '7eac7b56-f4d4-4177-89d6-748da17b531c'),
       ('4e784780-03b5-4805-a2c3-602911cb6b5a', 'Mini Guerreiro Dracônico', 'Os grandes guerreiros do Enken-ryū foram treinados com diversos tipos de armamentos. Todos os seus **ATAQUES** com o  descritor **LEVE** recebem o descritor **LETAL**.', '7eac7b56-f4d4-4177-89d6-748da17b531c'),
       ('3b4d28a9-02eb-4b85-a32b-58987db123a5', 'Um Oitavo de Forma Dracônica', 'O usuário carrega (um pouco) do sangue dos dragões em suas veias. Você é imune à condição ***Amedrontado*** e todos os ataques com o descritor **MEDO** são feitos com **desvantagem** contra você.', '7eac7b56-f4d4-4177-89d6-748da17b531c');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_TALENTO}
VALUES ('4ce34a98-ee22-4dc1-b17b-933d6b1f1e8d', 'Golpe Ainda Mais Poderoso', 'Seu *"Ataque Poderoso"* fica mais rápido, mais intenso, mais legal… bem, mais poderoso! Você aumenta o dano extra em mais um dado do mesmo tipo.', '7eac7b56-f4d4-4177-89d6-748da17b531c'),
       ('15034448-5eef-4996-bb93-e26f241c26bf', 'Frenesi Flamejante', 'Enquanto estiver em afinidade elemental, seus **ATAQUES** com **ARMA** recebem uma nova modificação', '7eac7b56-f4d4-4177-89d6-748da17b531c');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_ITEM}
VALUES ('97245586-3669-47a1-87ec-3feeebed3fa6', 'Yedo', 'Espada tradicional do Dojo Enken-ryū, longa e ligeiramente curva.', 100, 2),
       ('e8149810-d9c4-4e2b-903a-5ee1c13f9094', 'Armadura de Couro Batido', 'Proteção comum entre mercenários e aventureiros inexperientes, reforçada com pequenas placas de couro em locais estratégicos.', 40, 3);"""
    )
    cursor.execute(
        f"""{constantes.INSERT_ITENS_PERSONAGENS}
VALUES ('97245586-3669-47a1-87ec-3feeebed3fa6', '7eac7b56-f4d4-4177-89d6-748da17b531c', 1),
       ('e8149810-d9c4-4e2b-903a-5ee1c13f9094', '7eac7b56-f4d4-4177-89d6-748da17b531c', 1);"""
    )
    cursor.execute(
        f"""{constantes.INSERT_MODIFICADOR_SKILLS}
VALUES ('1ebb3ce6-f374-4cae-a7d1-0f4a820a8afc', 'b236cf6b-4008-4308-adba-f669f5da7d57'),
       ('1ebb3ce6-f374-4cae-a7d1-0f4a820a8afc', 'eb226b4a-1f19-495c-92d9-e7388a55aebe');"""
    )

    print("TSUKO ADICIONADO")
    
    # --------------------------------------------------------------------------------------------

    # PROMPT DO HYLLER

    reducao_de_dano = 2
    forca = ["13", "3"]
    destreza = ["12", "2"]
    constituicao = ["11", "1"]
    inteligencia = ["11", "1"]
    sabedoria = ["10", "0"]
    carisma = ["9", "-1"]
    pericias = "'89056ec3-8736-4136-a962-e86434799d2c', 'c25f6a18-6b01-423a-9c44-1781f677137d', '71850f9a-22d3-441a-b675-8858d8718984', '8d72c0e9-5c54-4b4a-b80a-a3b60d8f1309', '62ef595a-2f6e-475c-8152-3f36a5c4e695'"

    cursor.execute(
        f"""{constantes.INSERT_PERSONAGEM}
VALUES ('a38675f6-b1d5-427b-b5a6-dbb46eefee16', 'Hyller Wick', 'Hyller', {level}, 'Humano', 'Combatente', 'Assassino das Sombras', 'Pomonas Cycle', 'Para Hyller, o fim é necessário. Assim como a vida, todo ciclo tem um fim. Sempre que um ciclo se encerrar Hyller ganha 1 **ponto de catarse**.', 0, {pe}, {pe}, {calc_hp(int(constituicao[1]), 0)}, {calc_hp(int(constituicao[1]), 0)}, 'hp', {reducao_de_dano}, {bonus_de_proficiencia}, 5, ARRAY[{pericias}]::UUID[], {int(forca[0])}, {int(forca[1])}, {int(destreza[0])}, {int(destreza[1])}, {int(constituicao[0])}, {int(constituicao[1])}, {int(inteligencia[0])}, {int(inteligencia[1])}, {int(sabedoria[0])}, {int(sabedoria[1])}, {int(carisma[0])}, {int(carisma[1])}, 7, {calc_liimite_peso(int(forca[1]))}, NULL, NULL, NULL, 100, 'hyller.png', '<:hiller_token:1394716547561558106>', '902236993331798117', '8a87e68e-cd9d-46e5-953a-35942487ef1b');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_MODIFICADOR}
VALUES ('6745815c-0467-485e-8e9a-f196be672116', 'reacao', 'AMPLIAR + 15', '**Acerto:** você causa +1d8 pontos de dano do mesmo tipo.', 0, 'PE'),
       ('27c10bb7-7349-479e-ad27-92dd1f224688', 'reacao', 'ADICIONA', '**Especial:** você recebe **vantagem** no ataque. Até o início de seu próximo turno, você está **Desprotegido*** contra o próximo ataque que sofrer.', 0, 'PE'),    
       ('143fec26-003e-4aa8-b714-ec772d81a772', 'reacao', 'ADICIONA', '**Acerto:** você causa dano normal, como se tivesse feito um ataque com sua **ARMA**.', 1, 'PE'),
       ('ee86b756-f804-42f4-97d4-b80455d0cf94', 'reacao', 'ADICIONA', '**Especial:** você ignora todas as **resistências** do alvo nesse ataque.', 1, 'PE'),
       ('20c8c0f1-7e2a-4f8d-8c3a-7b5e4f2c1a9d', 'reacao', 'ADICIONA', '**Acerto:** o alvo fica ***Desprotegido*** em um atributo específico até o início do seu próximo turno.', 2, 'PE'),
       ('c4635b70-1975-46f7-8299-7b3ae0107b99', 'reacao', 'ADICIONA', '**Acerto:** você causa +1d6 pontos de dano **VENENOSO**. Você pode aplicar essa modificação mais de uma vez.', 1, 'PE'),
       ('1f00d09f-9a0f-44ac-a461-1c0ce6dc4b98', 'reacao', 'ADICIONA', '**Acerto:** o deslocamento do alvo é reduzido à metade até o início do seu próximo turno.', 3, 'PE'),
       ('f2f3e2e3-1c4e-4f7b-8f4a-5e2b6d9c8a7b', 'reacao', 'ADICIONA', '**Efeito:** o bônus de acerto em testes de ataque aumenta em +1. Você pode aplicar essa modificação mais de uma vez.', 2, 'PE');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_SKILL}
VALUES ('c0c3a5dd-a713-4992-9759-5e83d50cd4f5', 'Ataque de Superioridade', 0, 'acao', 'ATAQUE', '2m.', 'Instantânea.', '1d20 + {int(forca[1])} vs **FOR**.', 'Você deve escolher um efeito entre: Deixar o alvo ***Caído***; Pegar um item do alvo; Deixar o alvo ***Agarrado***.', NULL, NULL, 'Você só pode usar essa habilidade em criaturas de seu tamanho ou menor.', NULL, 'Uma criatura.', 'Ilimitado.', 'a38675f6-b1d5-427b-b5a6-dbb46eefee16'),
       ('a01d8257-492b-47ea-9dde-60fc895cb95f', 'Corte com o Espadão do Warpinier', 0, 'acao', 'ATAQUE, CORTANTE, PESADA', '2m.', 'Instatânea.', '1d20 + {int(forca[1])} + {bonus_de_proficiencia} + 2 vs **DES**.', '2d10 + 3 + {bonus_de_proficiencia} pontos de dano **CORTANTE**', 'Caso você erre no teste de acerto, você solta a **ARMA** e terá que gastar sua <:acao_bonus:1326585197004722197> Ação Bônus para pegá-la novamente. Se a **ARMA** não estiver na forma de espadão, você não pode usar essa habilidade.', NULL, 'O *"Ataque Poderoso"* recupera 1d4 pontos de PE.', NULL, 'Uma criatura.', 'Ilimitado.', 'a38675f6-b1d5-427b-b5a6-dbb46eefee16'),
       ('c1952dc6-07c5-4863-8344-50e95a20d731', 'Corte com a Katana', 1, 'acao livre', 'ATAQUE, CORTANTE, VERSÁTIL', '2m.', 'Instatânea.', '1d20 + {int(forca[1])} + {bonus_de_proficiencia} vs **DES**.', '1d8 + {bonus_de_proficiencia} pontos de dano **CORTANTE**', 'Caso você erre no teste de acerto, você solta a **ARMA** e terá que gastar sua <:acao_bonus:1326585197004722197> Ação Bônus para pegá-la novamente. Se a **ARMA** não estiver na forma de katana, você não pode usar essa habilidade.', NULL, NULL, NULL, 'Uma criatura.', 'Ilimitado.', 'a38675f6-b1d5-427b-b5a6-dbb46eefee16'),
       ('e7e60fba-2c6c-47c5-952c-07094f5560e1', 'Pomonas Treasure', 0, 'acao', 'MÁGICO', 'Toque.', 'Instântanea.', NULL, NULL, NULL, 'Você se torna capaz de criar véus de mana a partir das próprias mãos. Esse véu junta dois ou mais objetos de forma natural e sem resíduos. Podendo juntar até mesmo almas à uma receptáculo', NULL, NULL, 'Um objeto.', 'Ilimitado.', 'a38675f6-b1d5-427b-b5a6-dbb46eefee16'),
       ('c39d8b2d-b737-4274-8b76-158af3b49a9e', 'Transformação em Sombra', 0, 'acao livre', 'SOMBRA', 'Pessoal.', 'Instantânea.', NULL, NULL, NULL, 'Você se transforma em uma sombra e pode se mover sem ser detectado.', NULL, NULL, NULL, 'Ilimitado.', 'a38675f6-b1d5-427b-b5a6-dbb46eefee16'),
       ('bc73722a-56d0-4413-bf7c-a713fb96385c', 'Mortalha Energizante', 0, 'reacao', 'HUMANO', 'Pessoal.', 'Instantânea.', NULL, NULL, NULL, 'Você recebe {bonus_de_proficiencia} pontos de ênfase temporários durante essa cena.', 'Você só pode usar essa habilidade uma vez por descanso.', 'Uma criatura na cena morre', NULL, 'Ilimitado.', 'a38675f6-b1d5-427b-b5a6-dbb46eefee16'),
       ('26b0ad66-bc38-4d01-925f-0dd4f8fe8376', 'Armamento Tóxico', 1, 'acao_bonus', 'ASSASSINO', 'Toque.', 'Até o início do seu próximo turno.', NULL, NULL, NULL, 'Você consome uma de suas toxinas para imbuí-la em uma **ARMA** que esteja tocando. Ela fornece +1 em testes de **ATAQUE**. Além disso, você pode aplicar uma ou mais modificações da lista de incrementos tóxicos aos seus **ATAQUES** com a arma (escolhidos quando você imbui a toxina na arma).', NULL, NULL, 'Uma arma dentro do alcance.', 'Ilimitado.', 'a38675f6-b1d5-427b-b5a6-dbb46eefee16'),
       ('90db7ed6-3d12-47c6-8a29-02152da71353', 'Montar Arsenal de Warpinier', 0, 'acao livre', 'CONTROLE', 'Toque.', 'Instantânea.', NULL, NULL, NULL, 'Você muda a forma do seu espadão para katana ou vice-versa.', NULL, NULL, 'O Espdadão de Warpinier.', 'Ilimitado.', 'a38675f6-b1d5-427b-b5a6-dbb46eefee16');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_PASSIVA}
VALUES ('8d875318-a42f-45ef-b3c3-6cfced6b6f1b', 'Ataque Poderoso', 'Você treinou seu corpo para ser capaz de desferir ataques poderosíssimos sempre que ataca. Seus **ATAQUES** com **ARMAS** recebem uma nova modificação.', 'a38675f6-b1d5-427b-b5a6-dbb46eefee16'),
       ('aef70f86-3820-4f78-abac-b7fa3266e902', 'Façanha com Duas Armas', 'Você é como um tornado, atacando seus oponentes com ataques rápidos com suas armas irmãs. Seus **ATAQUES** com **ARMA** recebem uma nova modificação.', 'a38675f6-b1d5-427b-b5a6-dbb46eefee16'),
       ('71a067ff-02de-4bcf-9fbf-608c0f348615', 'Façanha com Arma Pesada', 'Você é um verdadeiro guerreiro de armas pesadas. Seus **ATAQUES** com **ARMAS PESADAS** recebem uma nova modificação.', 'a38675f6-b1d5-427b-b5a6-dbb46eefee16'),
       ('65a8b463-942d-4a9f-bdcd-1b0ea8ecdaaa', 'Preparado Para Ação', 'Você recebe uma ação bônus <:acao_bonus:1326585197004722197> adicional no primeiro turno de combate.', 'a38675f6-b1d5-427b-b5a6-dbb46eefee16');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_TALENTO}
VALUES ('7969745f-7aad-4532-8c71-56b377369f32', 'Assassino Eficiente', 'Você sabe como otimizar o uso dos seus recursos e aproveitar as oportunidades. Você recebe 2 pontos de ênfase temporários sempre que causar um acerto crítico ou eliminar um inimigo com um **ATAQUE**. É possível receber um total de pontos de ênfase temporários dessa maneira {level} vezes por cena.', 'a38675f6-b1d5-427b-b5a6-dbb46eefee16'),
       ('80b1d4a3-9dc8-4b89-85c1-4cba327c680c', 'Assassino Marcial', 'Você tem treinamento de batalha excelente e sabe usar isso para cumprir sua função. Sempre que causar dano com seu *"Ataque Poderoso"* você deixa o alvo ***Envenenado***.', 'a38675f6-b1d5-427b-b5a6-dbb46eefee16'),
       ('72d48456-7618-404f-9159-1d7c597fe868', 'Resistir para Findar', 'Sua proximidade com A Sombra fez com que você encontrasse formas de dar o fim. Seus **ATAQUES** recebem uma nova modificação.', 'a38675f6-b1d5-427b-b5a6-dbb46eefee16');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_ITEM}
VALUES ('6f04bed2-c06e-4f4b-90d0-39cbd15aff12', 'Espadão do Warpinier', 'Antiga espada usada por Warpinier com seu avatar durante a batalha contra o Titan Slayer. "Acho que dá pra melhorar essa espadona com um toque de ciência." — disse Chrollo antes da ida de Hyller para NovaHorizon.', 500, 4),
       ('6406b636-d707-408f-b21a-9cde54a89d98', 'Armadura de Couro Batido', 'Proteção comum entre mercenários e aventureiros inexperientes, reforçada com pequenas placas de couro em locais estratégicos.', 40, 3);"""
    )
    cursor.execute(
        f"""{constantes.INSERT_ITENS_PERSONAGENS}
VALUES ('6f04bed2-c06e-4f4b-90d0-39cbd15aff12', 'a38675f6-b1d5-427b-b5a6-dbb46eefee16', 1),
       ('6406b636-d707-408f-b21a-9cde54a89d98', 'a38675f6-b1d5-427b-b5a6-dbb46eefee16', 1);"""
    )
    cursor.execute(
    f"""{constantes.INSERT_MODIFICADOR_SKILLS}
VALUES ('c0c3a5dd-a713-4992-9759-5e83d50cd4f5', '143fec26-003e-4aa8-b714-ec772d81a772'),
       ('c0c3a5dd-a713-4992-9759-5e83d50cd4f5', '6745815c-0467-485e-8e9a-f196be672116'),
       ('a01d8257-492b-47ea-9dde-60fc895cb95f', '6745815c-0467-485e-8e9a-f196be672116'),
       ('c1952dc6-07c5-4863-8344-50e95a20d731', '6745815c-0467-485e-8e9a-f196be672116'),
       ('a01d8257-492b-47ea-9dde-60fc895cb95f', 'f2f3e2e3-1c4e-4f7b-8f4a-5e2b6d9c8a7b'),
       ('c1952dc6-07c5-4863-8344-50e95a20d731', 'f2f3e2e3-1c4e-4f7b-8f4a-5e2b6d9c8a7b'),
       ('a01d8257-492b-47ea-9dde-60fc895cb95f', '27c10bb7-7349-479e-ad27-92dd1f224688');"""
)

    #    ('a01d8257-492b-47ea-9dde-60fc895cb95f', 'ee86b756-f804-42f4-97d4-b80455d0cf94'),
    #    ('c1952dc6-07c5-4863-8344-50e95a20d731', 'ee86b756-f804-42f4-97d4-b80455d0cf94'),
    #    ('a01d8257-492b-47ea-9dde-60fc895cb95f', '20c8c0f1-7e2a-4f8d-8c3a-7b5e4f2c1a9d'),
    #    ('c1952dc6-07c5-4863-8344-50e95a20d731', '20c8c0f1-7e2a-4f8d-8c3a-7b5e4f2c1a9d'),
    #    ('a01d8257-492b-47ea-9dde-60fc895cb95f', 'c4635b70-1975-46f7-8299-7b3ae0107b99'),
    #    ('c1952dc6-07c5-4863-8344-50e95a20d731', 'c4635b70-1975-46f7-8299-7b3ae0107b99'),
    #    ('a01d8257-492b-47ea-9dde-60fc895cb95f', '1f00d09f-9a0f-44ac-a461-1c0ce6dc4b98'),
    #    ('c1952dc6-07c5-4863-8344-50e95a20d731', '1f00d09f-9a0f-44ac-a461-1c0ce6dc4b98'),
       
    print("HYLLER ADICIONADO")

    # --------------------------------------------------------------------------------------------

#     # PROMPT DO MAX

#     reducao_de_dano = 2
#     forca = ["11", "1"]
#     destreza = ["12", "2"]
#     constituicao = ["11", "1"]
#     inteligencia = ["10", "0"]
#     sabedoria = ["13", "3"]
#     carisma = ["9", "-1"]


#     f"""{constantes.INSERT_PERSONAGEM}
# VALUES (e3c79d34-cfb3-418f-b382-32b12fe2dafa, 'Max', 'Max', {level}, 'Protetor do Arquipélago', 'Ocultista', 'Corvino', 'Vigília', 'malancolia.', 0, {pe}, {pe}, {calc_hp(int(constituicao[1])), 2}, {calc_hp(int(constituicao[1])), 2}, 'hp', {reducao_de_dano}, {bonus_de_proficiencia}, {int(forca[0])}, {int(forca[1])}, {int(destreza[0])}, {int(destreza[1])}, {int(constituicao[0])}, {int(constituicao[1])}, {int(inteligencia[0])}, {int(inteligencia[1])}, {int(sabedoria[0])}, {int(sabedoria[1])}, {int(carisma[0])}, {int(carisma[1])}, , {calc_liimite_peso(int(forca[1]))}, NULL, NULL, NULL, 100, 'max.png', '<>', '862452682107387904', '8a87e68e-cd9d-46e5-953a-35942487ef1b');"""
#     cursor.execute(
#         f"""{constantes.INSERT_SKILL}
# VALUES ('543c5e5f-34af-4c11-88f1-1c3e3da8c2d3', 'Estocada com Tridente', 0, 'acao', 'PERFURANTE', '1m.', 'Instantânea.', '1d20 ', 'acerto', 'erro', 'efeito', 'especial', 'gatilho', 'alvo.', 'Ilimitado.', '');"""
#     )
#     print("MAX ADICIONADO")

    # --------------------------------------------------------------------------------------------

    # PROMPT DE ZÊNITE

    reducao_de_dano = 2
    forca = ["12", "2"]
    destreza = ["13", "1"]
    constituicao = ["11", "1"]
    inteligencia = ["8", "-2"]
    sabedoria = ["10", "0"]
    carisma = ["10", "0"]
    pericias = "'ebaea72e-3d09-487e-a809-360077352a5c', '71850f9a-22d3-441a-b675-8858d8718984', '3bc86566-ec94-4459-a7fc-2a5d094a1f39'"

    cursor.execute(
        f"""{constantes.INSERT_PERSONAGEM}
VALUES('3328a565-9f71-48f1-a0ef-dbdc403e8640', 'Zênite', NULL, {level}, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, {bonus_de_proficiencia}, {bonus_de_proficiencia}, 'carga', {reducao_de_dano}, {bonus_de_proficiencia}, 5, ARRAY[{pericias}]::UUID[], {int(forca[0])}, {int(forca[1])}, {int(destreza[0])}, {int(destreza[1])}, {int(constituicao[0])}, {int(constituicao[1])}, {int(inteligencia[0])}, {int(inteligencia[1])}, {int(sabedoria[0])}, {int(sabedoria[1])}, {int(carisma[0])}, {int(carisma[1])}, 0, {calc_liimite_peso(int(forca[1]))}, NULL, NULL, NULL, 0, 'zenite.png', '<TOKEN>', NULL, '8a87e68e-cd9d-46e5-953a-35942487ef1b');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_MODIFICADOR}
VALUES ('10f0d9e4-97d9-4b07-89e1-a3cbf1513bf2', 'reacao', 'ADICIONA', 'Em um acerto, o alvo fica ***Desprotegido*** até o início do seu próximo turno.', 1, 'PE');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_SKILL}
VALUES ('9cde6c1c-a4cc-4d37-bf30-9a50d7be39ed', 'Transfigurar Companheiro Animal', 1, 'acao livre', 'MESTRE DAS FERAS', 'Pessoal.', 'Instantânea,', NULL, NULL, NULL, 'Seu companheiro animal toma a forma de outro ser, podendo variar entre os descritos em *"Criatura Metamorfa"*', 'Essa habilidade só pode ser usada uma vez por cena.', NULL, 'Zênite.', '{bonus_de_proficiencia}.', '3328a565-9f71-48f1-a0ef-dbdc403e8640'),
       ('87632e99-c562-466a-87cf-f07f7542ab9b', 'Atacar e Machucar: Lobo', 1, 'acao', 'MESTRE DAS FERAS, PERFURANTE, ATAQUE', '2m.', 'Instantânea.', '1d20 + {int(forca[1])} vs **DES**.', '1d10 + 1d6 pontos de dano **PERFURANTE**.', NULL, 'Caso o teste tenha resultado em 17 ou mais, o alvo fica ***Caído***.', 'Essa habilidade só poder ser usada caso Zênite esteja na forma de Lobo.', NULL, NULL, 'Ilimitado.', '3328a565-9f71-48f1-a0ef-dbdc403e8640'),
       ('786fdf9d-9e83-41c1-a9da-4e8324178820', 'Atacar e Machucar: Onça', 1, 'acao', 'MESTRE DAS FERAS, PERFURANTE, ATAQUE', '2m.', 'Instantânea.', '1d20 + {int(forca[1])} + 5 vs **DES**.', '1d8 + 1d6 pontos de dano **PERFURANTE**.', NULL, 'Caso o 1d20 do teste tenha resultado em 15 ou mais, o alvo fica ***Caído***.', 'Essa habilidade só poder ser usada caso Zênite esteja na forma de Onça.', NULL, NULL, 'Ilimitado.', '3328a565-9f71-48f1-a0ef-dbdc403e8640'),
       ('3ec736b8-7081-4b9f-8f5a-cb92875c3b6a', 'Atacar e Machucar: Gavião Gigante', 1, 'acao', 'MESTRE DAS FERAS, ESPECIAL, ATAQUE', '2m.', 'Instantânea.', '1d20 + {int(forca[1])} + 3 vs **DES**.', '1d12 pontos de dano **ESPECIAL**.', NULL, 'Caso o 1d20 do teste tenha resultado em 15 ou mais, o alvo fica ***Caído***.', 'Essa habilidade só poder ser usada caso Zênite esteja na forma de Gavião Gigante.', NULL, NULL, 'Ilimitado.', '3328a565-9f71-48f1-a0ef-dbdc403e8640'),
       ('666ee7b5-4e56-45c7-bc5a-4e84bbfd7407', 'Buscar e Entregar', 1, 'acao', 'MESTRE DAS FERAS', '9m.', 'Instantânea.', NULL, NULL, NULL, 'Zênite pega um item com uma criatura voluntária e entrega para outra, desde que ambas estejam no seu alcance. Também é possível usar esse comando para fazer com que ele busque um item arremessado em alcance.', NULL, NULL, NULL, 'Ilimitado.', '3328a565-9f71-48f1-a0ef-dbdc403e8640'),
       ('2fb564b1-61d7-49db-b559-1d2cfa7dc217', 'Ataque de Superioridade', 1, 'acao', 'MESTRE DAS FERAS, ATAQUE', '2m.', 'Instantânea.', '1d20 + {int(forca[1])} vs **FOR**.', 'Você deve escolher um efeito entre: Deixar o alvo ***Caído***; Pegar um item do alvo; Deixar o alvo ***Agarrado***.', NULL, NULL, 'Você só pode usar essa habilidade em criaturas de seu tamanho ou menor.', NULL, 'Uma criatura.', 'Ilimitado.', '3328a565-9f71-48f1-a0ef-dbdc403e8640');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_PASSIVA}
VALUES ('ade80068-99cd-4a61-b7c5-fdf12071560c', 'Criatura Metamorfa', 'Zênite é uma criatura mística capaz de se transformar em outras criaturas que ela já temha visto (Lobo, Onça, Gavião Gigante e Cavalo). Ela pode mudar de forma usandoa habilidade *"Transfigurar Companheiro Animal"*.', '3328a565-9f71-48f1-a0ef-dbdc403e8640');"""
    )
    print("\nZÊNITE ADICIONADA")


    # -------------------------------------------------------------------------------------------

    # PROMPT FENRIR

    reducao_de_dano = 2
    forca = ["13", "3"]
    destreza = ["14", "2"]
    constituicao = ["11", "1"]
    inteligencia = ["8", "-2"]
    sabedoria = ["10", "0"]
    carisma = ["11", "1"]
    pericias = "'c7482295-cb98-49fe-92fd-8266c8675121', 'a052505a-add0-4717-9d30-e382a0741058', 'ebaea72e-3d09-487e-a809-360077352a5c'"

    cursor.execute(f"""{constantes.INSERT_PERSONAGEM}
    VALUES ('73939ac9-83ac-481e-a855-ca02380ba48f', 'Fenrir, o Lobo do Ragnarok', 'Fenrir', {level}, 'Sombra', 'Combatente', 'Echo Sombrio', 'Aprisionado', 'Para Echos sombrios aprisionados, nada dói mais do que ver aliados sofrendo. Caso um aliado seja derrotado enquando um echo sombrio estiver em campo, o grupo inteiro ganha 1 **ponto de catarse**.', 0, {pe}, {pe}, {bonus_de_proficiencia}, {bonus_de_proficiencia}, 'carga', {reducao_de_dano}, {bonus_de_proficiencia}, 0, ARRAY[{pericias}]::UUID[], {int(forca[0])}, {int(forca[1])}, {int(destreza[0])}, {int(destreza[1])}, {int(constituicao[0])}, {int(constituicao[1])}, {int(inteligencia[0])}, {int(inteligencia[1])}, {int(sabedoria[0])}, {int(sabedoria[1])}, {int(carisma[0])}, {int(carisma[1])}, 0, {calc_liimite_peso(int(forca[1]))}, 'ELÉTRICO, VENENOSO, NECRÓTICO', null, null, 0, 'fenrir.png', '<:fenrir_token:1394716544507838624>', null, '50282f93-2701-43b7-83e5-664d2a1251be');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_MODIFICADOR}
    VALUES ('c72f296d-a120-4fd1-8ab1-ad3dff651f38', 'reacao', 'AMPLIAR + 15', '**Acerto:** você causa +1d8 pontos de dano do mesmo tipo.', 0, 'PE');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_SKILL}
    VALUES ('63ee6fbd-083e-49e1-b2e9-b04bf1c75288', 'Shadow Steps', 2, 'acao bonus', 'SOMBRIO', '18m.', 'Instantânea.', null, null, null, 'Fenrir se esconde na sombras e avança pra trás de qualquer criatura dentro do alcance. O alvo fica ***Desprotegido***.', null, null, 'Qualquer criatura dentro do alcance.', 'Ilimitado.', '73939ac9-83ac-481e-a855-ca02380ba48f'),
           ('98495aca-df8c-4205-8161-f248b3070e4e', 'Presas do Ragnarok', 0, 'acao', 'ATAQUE, PERFURANTE, ARMA', '2m.', 'Instantânea.', '1d20 + {int(forca[1])} + {bonus_de_proficiencia}.', '1d12 + {bonus_de_proficiencia} pontos de dano **PERFURANTE**.', 'Fenrir perde sua <:acao_bonus:1326585197004722197> Ação Bônus.', null, null, null, 'Uma criatura dentro do alcance.', 'Ilimitado.', '73939ac9-83ac-481e-a855-ca02380ba48f');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_PASSIVA}
    VALUES ('a76815f8-d7ca-4e95-b999-41046dfd455a', 'Bruto', 'Os ataques realizam acertos críticos com 19-20.', '73939ac9-83ac-481e-a855-ca02380ba48f'),
           ('e02e3acd-dba6-422f-b8a5-c9bafcc6a9d5', 'Ataque Poderoso', 'Você treinou seu corpo para ser capaz de desferir ataques poderosíssimos sempre que ataca. Seus **ATAQUES** com **ARMAS** recebem uma nova modificação.', '73939ac9-83ac-481e-a855-ca02380ba48f');"""
    )
    cursor.execute(
        f"""{constantes.INSERT_MODIFICADOR_SKILLS}
    VALUES ('98495aca-df8c-4205-8161-f248b3070e4e', 'c72f296d-a120-4fd1-8ab1-ad3dff651f38');"""
    )
    print("FENRIR ADICIONADO")

# #     # --------------------------------------------------------------------------------------------

# #     # PROMPT ASHBORN

# #     forca = ["12", "2"]
# #     destreza = ["18", "5"]
# #     constituicao = ["10", "0"]
# #     inteligencia = ["10", "0"]
# #     sabedoria = ["16", "3"]
# #     carisma = ["12", "2"]

# #     reducao_de_dano = 0

# #     pericias = [
# #         "d0f44af5-c299-41c2-9e84-72dd9cdb7351",
# #         "a052505a-add0-4717-9d30-e382a0741058",
# #         "3bc86566-ec94-4459-a7fc-2a5d094a1f39",
# #     ]

# #     (
# #         f"""{constantes.INSERT_PERSONAGEM}
# # VALUES (0add69b7-771e-4580-a11b-bf1a75d35aa9, 'Ashborn, o Guardião do Darkhold I', 'Ashborn', {level}, 'Sombra', 'Ocultista', 'Echo Sombrio', 'Aprisionado', 'Para Echos sombrios aprisionados, nada dói mais do que ver aliados sofrendo. Caso um aliado seja derrotado enquando um echo sombrio estiver em campo, o grupo inteiro ganha 1 **ponto de catarse**.', 0, {pe}, {pe}, 5, 5, 'carga', {reducao_de_dano}, {bonus_de_proficiencia}, [{", ".join(pericias)}], [{", ".join(talentos)}], [{", ".join(passivas)}], [{", ".join(skills)}], [{", ".join(forca)}], [{", ".join(destreza)}], [{", ".join(constituicao)}], [{", ".join(inteligencia)}], [{", ".join(sabedoria)}], [{", ".join(carisma)}], 0, ['ELÉTRICO'], [], ['VENENOSO'], [{", ".join(itens)}], [1], 4, 19, [], 250, 'ashborn.png', '<:ashborn_token:1394716539915079731>', NULL);"""
# #     )

# # --------------------------------------------------------------------------------------------

# # PROMPT SABRINA

# forca = ["10", "0"]
# destreza = ["10", "0"]
# constituicao = ["10", "0"]
# inteligencia = ["10", "0"]
# sabedoria = ["10", "0"]
# carisma = ["10", "0"]

# reducao_de_dano = 2

# (
#     f"""{constantes.INSERT_PASSIVA}
# VALUES (c6a8fe1d-1b36-4482-9765-3919abcbea45, 'Procedimento Arcano', 'O usuário aprende um truque mágico a sua escolha. Além disso, aprende e pode conjurar uma magia de camada superficial. Você deve gastar pontos de ênfase normalmente para conjurar essa magia.', None, None, None, 0, None);"""
# )

# pericias = []
# passivas = ["c6a8fe1d-1b36-4482-9765-3919abcbea45"]
# talentos = []
# skills = []
# itens = []

# (
#     f"""{constantes.INSERT_PERSONAGEM}
# VALUES (30180fc6-30ba-4f65-a520-53e63bc4ec65, 'Sabrina', 'Chrollo', {level}, 'Magitécnico', 'Combatente', 'Humano', 'Pomonas Cycle', 'Para Chrollo, o fim é necessário. Assim como a vida, todo ciclo tem um fim.', 0, {pe}, {pe}, 44, 44, 'hp', {reducao_de_dano}, {bonus_de_proficiencia}, [{", ".join(pericias)}], [{", ".join(talentos)}], [{", ".join(passivas)}], [{", ".join(skills)}], [{", ".join(forca)}], [{", ".join(destreza)}], [{", ".join(constituicao)}], [{", ".join(inteligencia)}], [{", ".join(sabedoria)}], [{", ".join(carisma)}], 5, [], [], [], [{", ".join(itens)}], [1, 1, 1, 1, 1], 15, 19, [], 250, 'chrollo.png', '<:chrollo_token:1384691822584135894>', '766039963736866828');"""
# )

# #  --------------------------------------------------------------------------------------------

# TEMPLATE

# reducao_de_dano = 0
# forca = ["0", "0"]
# destreza = ["0", "0"]
# constituicao = ["0", "0"]
# inteligencia = ["0", "0"]
# sabedoria = ["0", "0"]
# carisma = ["0", "0"]
# pericias = ""

# cursor.execute(
#     f"""{constantes.INSERT_PERSONAGEM}
# VALUES ('', 'nome', 'nickname', {level}, 'legacy', 'classe', 'path', 'heritage', 'melancholy', catarse, {pe}, {pe}, {calc_hp(int(constituicao[1]), 0)}, {calc_hp(int(constituicao[1]), 0)}, hp_tipo, {reducao_de_dano}, {bonus_de_proficiencia}, ARRAY[{pericias}]::UUID[], {int(forca[0])}, {int(forca[1])}, {int(destreza[0])}, {int(destreza[1])}, {int(constituicao[0])}, {int(constituicao[1])}, {int(inteligencia[0])}, {int(inteligencia[1])}, {int(sabedoria[0])}, {int(sabedoria[1])}, {int(carisma[0])}, {int(carisma[1])}, volume_atual, {calc_liimite_peso(int(forca[1]))}, 'resistencia', 'vulnerabilidade', 'imunidade', 100, 'imagem.png', '<>', 'usuario', '8a87e68e-cd9d-46e5-953a-35942487ef1b');"""
# )
# cursor.execute(
#     f"""{constantes.INSERT_MODIFICADOR}
#     VALUES ('', 'nome', 'descricao', 'execucao', gasto, 'PE');"""
# )
# cursor.execute(
#     f"""{constantes.INSERT_SKILL}
#  VALUES ('', 'nome', 0, 'acao', 'descritor', 'alcance', 'duracao', 'ataque', 'acerto', 'erro', 'efeito', 'especial', 'gatilho', 'alvo.', 'Ilimitado.', '');"""
# )
# cursor.execute(
#     f"""{constantes.INSERT_PASSIVA}
# VALUES ('', '', '', '');"""
# )
# cursor.execute(
#     f"""{constantes.INSERT_TALENTO}
# VALUES ('', '', '', '');"""
# )
# cursor.execute(
#     f"""{constantes.INSERT_ITEM}
# VALUES ('', '', '', 000, 0, '');"""
# )
# cursor.execute(
#     f"""{constantes.INSERT_ITENS_PERSONAGENS}
# VALUES ('', '', 0);"""
# )
# cursor.execute(
#     f"""{constantes.INSERT_MODIFICADOR_SKILLS}
# VALUES ('', '');"""
# )
# print("\n ADICIONADO")
