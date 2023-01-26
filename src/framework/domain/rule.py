from dataclasses import dataclass

@dataclass(kw_only=True)
class Rule:
    '''Classe base para as regras de negócio do domínio.'''
    __message: str = 'Regra de negócio violada.'
    
    def get_message(self) -> str:
        return self.__message
    
    def is_broken(self) -> bool:
        pass
    
    def __str__(self):
        return f"{self.__class__.__name__} {self.__message}"


@dataclass
class BusinessRuleValidationException(Exception):
    rule: Rule
    
    def __repr__(self):
        return f"{self.__class__.__name__} ({str(self.rule)})"