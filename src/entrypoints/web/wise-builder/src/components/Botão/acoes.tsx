import {
    IconButton,
    Button,
    Stack,
  } from '@chakra-ui/react';

  import { DeleteIcon, EditIcon } from '@chakra-ui/icons';
  
  export default function ServerSecondaryOptions() {
    return (
        <Stack direction='row' spacing={4}>
            <IconButton
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