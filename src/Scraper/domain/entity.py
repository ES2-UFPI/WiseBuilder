@dataclass
class MatchesTrackedComponent(Rule):
    # Verifica se o componente é um dos componentes observados
    component_name: str

    def is_broken(self) -> bool:
        # verificar se componente existe
        # return not SearchEngine.get_id_by_name(component_name)
        return False
