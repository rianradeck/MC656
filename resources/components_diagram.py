from diagrams import Diagram
from diagrams.c4 import C4Node, Person, Relationship


def Component(name, technology="", description="", **kwargs):
    component_attributes = {
        "name": name,
        "technology": technology,
        "description": description,
        "type": "Component",
        "fillcolor": "#4a91b9",
    }
    component_attributes.update(kwargs)
    return C4Node(**component_attributes)


graph_attr = {
    "splines": "spline",
}

node_attr = {"height": "2.3", "width": "4"}

node_attr2 = {"height": "1.9", "width": "3.5"}

with Diagram(
    "\n\n\n\nDiagrama de Componentes",
    direction="TB",
    graph_attr=graph_attr,
    outformat="png",
):
    usuario = Person(name="Jogador", description="Usuário final", **node_attr)

    display = Component(
        name="Componente de renderização",
        description="Renderiza informações do jogo",
        **node_attr
    )

    input = Component(
        name="Componente de entrada",
        description="Processa e valida a entrada fornecida",
        **node_attr
    )

    client_network = Component(
        name="Componente de rede do cliente",
        description="Organiza, audita e orquestra a comunicação com o servidor",
        **node_attr
    )

    server_network = Component(
        name="Componente de rede do servidor",
        description="Audita e orquestra a comunicação com o cliente",
        **node_attr
    )

    grid = Component(
        name="Componente de partida",
        description="Armazena informações sobre um estado do grid de uma partida",
        **node_attr
    )

    game_manager = Component(
        name="Componente de gerenciamento de partida",
        description="Manipula e audita informações sobre um estado de jogo"
        ", além de calcular o próximo estado",
        **node_attr
    )

    usuario >> Relationship("Interage via teclado com", style="solid") >> input
    (
        input
        >> Relationship("Envia a decisão do usuário para", style="solid")
        >> client_network
    )
    (
        client_network
        >> Relationship(
            "Envia pacotes para", style="solid", forward=True, reverse=True
        )
        >> server_network
    )
    # client_network >> Relationship("Envia pacotes para", style="solid") >> server_network
    (
        server_network
        >> Relationship(
            "Envia informações sobre mudanças de estado para", style="solid"
        )
        >> game_manager
    )
    (
        game_manager
        >> Relationship("Envia novos estados para", style="solid")
        >> server_network
    )
    (
        client_network
        >> Relationship("Envia novos estados para", style="solid")
        >> grid
    )
    # game_manager >> Relationship("Atualiza novos estados do", style="solid") >> grid
    (
        grid
        >> Relationship("Envia o estado do jogo para", style="solid")
        >> display
    )
    (
        display
        >> Relationship("Envia informações visuais para", style="solid")
        >> usuario
    )
