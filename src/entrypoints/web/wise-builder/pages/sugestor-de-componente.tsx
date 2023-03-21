import { useState, useEffect } from 'react';
import { 
    Heading,
    Icon,
    Center,
    Flex,
    Box,
    Text,
    Stack,
    keyframes,
    Button,
    Grid,
    Divider,
    HStack,
    GridItem,
    useColorModeValue,
} from "@chakra-ui/react";
import { ArrowForwardIcon, CheckCircleIcon, HamburgerIcon } from "@chakra-ui/icons";
import CardProduto from '../src/components/Card/card-produto';
import { Componente } from '../src/types/componente';
import React from 'react';
import StatusIndicator from '../src/components/Status/status';

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
    modelo: '3070',
    valor: 100,
    link: 'https://www.kabum.com.br/produto/377636/placa-de-video-rtx-3070-msi-ventus-3x-plus-nvidia-geforce-8gb-gddr6-lhr-dlss-ray-tracing-geforce-rtx-3070-ventus-3x-plus-8g-oc-lhr'
  },
  {
    id: '2',
    tipo: 'Placa de Vídeo',
    fabricante: 'Asus',
    modelo: '1060',
    valor: 200
  },
  {
    id: '3',
    tipo: 'Fonte',
    fabricante: 'Asus',
    modelo: 'Pylon',
    valor: 500
  },
  {
    id: '4',
    tipo: 'Fonte',
    fabricante: 'Asus',
    modelo: 'Pylon',
    valor: 500
  },
  {
    id: '6',
    tipo: 'Fonte',
    fabricante: 'Asus',
    modelo: 'Pylon',
    valor: 500
  },
  {
    id: '7',
    tipo: 'Fonte',
    fabricante: 'Asus',
    modelo: 'Pylon',
    valor: 500
  }
];

function SugestorComponente(busca: string) {
  const [items, setItems] = useState(mockItems);

  return (  
    <Grid
      h='md'
      templateRows='repeat(3, 1fr)'
      templateColumns='repeat(4, 1fr)'
      gap={3}
      bg={useColorModeValue('gray.50', 'gray.800')}
    >
      <GridItem colSpan={4}>
        <Heading>Sugestor de Componente</Heading>
        <Center>
            <HStack
            pl={6}
            mt={1}
            spacing={'200'}
            bg={useColorModeValue('white', 'gray.700')}
            rounded={'xl'}
            boxShadow={'lg'}
          >
                <Stack>
                    <Heading as='h4' size='md'>
                        Placa mãe
                    </Heading>
                    <StatusIndicator></StatusIndicator>
                </Stack> 
                <Stack>
                    <Heading as='h4' size='md'>
                        Processador
                    </Heading>
                    <StatusIndicator></StatusIndicator>
                </Stack> 
                <Stack>
                    <Heading as='h4' size='md'>
                        Memória RAM
                    </Heading>
                    <StatusIndicator></StatusIndicator>
                </Stack> 
                <Stack>
                    <Heading as='h4' size='md'>
                        Placa de Vídeo
                    </Heading>
                    <StatusIndicator></StatusIndicator>
                </Stack> 
                <Stack>
                    <Heading as='h4' size='md'>
                        Fonte
                    </Heading>
                    <StatusIndicator></StatusIndicator>
                </Stack> 
                <Button variant="solid" colorScheme="blue" rightIcon={<ArrowForwardIcon />}>
                        Próximo
                </Button>
            </HStack>
        </Center>
      </GridItem>
      <GridItem rowSpan={20} colSpan={3} margin={3}>
        <CardProduto item={mockItems}/>
      </GridItem>
    </Grid>
)};

export default SugestorComponente;