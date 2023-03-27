import { useState, useEffect, Component } from 'react';
import { 
    List,
    ListItem,
    ListIcon,
    Flex,
    Stack,
    Heading,
    useColorModeValue,
    Divider,
} from "@chakra-ui/react";
import { AddIcon, CheckCircleIcon } from "@chakra-ui/icons";
import Tabela from '../src/components/Tabela/tabela-listagem';
import { Componente } from '../src/types/componente';

/* async function getItems() {
    const response = await fetch('https://sua-api.com/items');
    const data = await response.json();
    return data;
  }

function ItemList() {
  const [items, setItems] = useState([]);

   useEffect(() => {
    async function fetchData() {
      const data = await getItems();
      setItems(data);
    }
    fetchData();
  }, []); */

const mockItems: Componente[] = [
  {
    id: '1',
    tipo: 'Placa de Vídeo',
    fabricante: 'Zotac',
    modelo: '3070'
  },
  {
    id: '2',
    tipo: 'Placa de Vídeo',
    fabricante: 'Asus',
    modelo: '1060'
  },
  {
    id: '3',
    tipo: 'Fonte',
    fabricante: 'Asus',
    modelo: 'Pylon'
  }
];

function ItemList() {
  const [items, setItems] = useState(mockItems);

  return (
    <Flex
    minH={'100vh'}
    align={'center'}
    justify={'center'}
    bg={useColorModeValue('gray.50', 'gray.800')}>
    <Stack
      spacing={4}
      w={'full'}
      maxW={'80%'}
      bg={useColorModeValue('white', 'gray.700')}
      rounded={'xl'}
      boxShadow={'lg'}
      p={6}
      my={12}>
      <Heading lineHeight={1.1} fontSize={{ base: '2xl', sm: '3xl' }}>
        Listar Componentes
      </Heading>
      <Divider orientation='horizontal' />
      <Tabela titulo="Componentes" link="/cadastrar-componente" item={mockItems} edit={true}/>
    </Stack>
  </Flex>
)};

export default ItemList;
