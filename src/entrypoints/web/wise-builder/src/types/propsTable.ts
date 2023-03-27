import { Componente } from './componente';

export interface TabelaProps {
    titulo: string,
    edit: boolean,
    link?: string,
    item: Componente[],
};