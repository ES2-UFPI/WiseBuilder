import {
    IconButton,
    Button,
    Stack,
  } from '@chakra-ui/react';

  import { DeleteIcon, EditIcon } from '@chakra-ui/icons';
  import { useRouter } from 'next/router';

  interface AcoesProps {
    id: string;
  }
  
  export default function acoes(props: AcoesProps) {
    function handleEdit(id: string) {
        const router = useRouter();
      
        router.push({
          pathname: '/cadastro-componente',
          query: { id, editar: true }
        });
    }
    return (
        <Stack direction='row' spacing={4}>
            <IconButton
                onClick={() => handleEdit(props.id)}
                bg='gray.200' 
                color ='gray.900'
                aria-label="Editar"
                icon={<EditIcon />}
                size="xs"
                variant="solid"
            />
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