import {
    IconButton,
    Button,
    Stack,
  } from '@chakra-ui/react';

  import { DeleteIcon, EditIcon, ExternalLinkIcon } from '@chakra-ui/icons';
  import { useRouter } from 'next/router';

  interface AcoesProps {
    id: string,
    edit: boolean,
    link?: string;
  }
  
  export default function acoes(props: AcoesProps) {
    const router = useRouter();
    
    function handleFav() {
      if (props.link != undefined){
        router.push(props.link);
    }
  }

    function handleEdit(id: string) {
        router.push({
          pathname: '/cadastro-componente',
          query: { id, editar: true }
        });
    }
    return (
        <Stack direction='row' spacing={4}>
          {props.edit && (
            <IconButton
              onClick={() => handleEdit(props.id)}
              bg='gray.200' 
              color ='gray.900'
              aria-label="Editar"
              icon={<EditIcon />}
              size="xs"
              variant="solid"
            />
          )}

          {props.edit === false && (
            <IconButton
              onClick={() => handleFav()}
              bg='blue' 
              color ='white'
              aria-label="Ver Oferta"
              icon={<ExternalLinkIcon />}
              size="xs"
              variant="solid"
            />
          )}
            
            <IconButton
                bg='red' 
                color ='white'
                aria-label="Deletar"
                icon={<DeleteIcon />}
                size="xs"
                variant="solid"
            />
        </Stack>
  )}