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
import { ArrowForwardIcon, ArrowBackIcon, HamburgerIcon } from "@chakra-ui/icons";
import CardProduto from '../../src/components/Card/card-produto';
import { Componente } from '../../src/types/componente';
import StatusIndicator from '../../src/components/Status/status';
import { useRouter } from 'next/router';

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
    type: 'Placa de Vídeo',
    manufacturer: 'Zotac',
    model: '3070',
    price: 100,
    link: 'https://www.kabum.com.br/produto/377636/placa-de-video-rtx-3070-msi-ventus-3x-plus-nvidia-geforce-8gb-gddr6-lhr-dlss-ray-tracing-geforce-rtx-3070-ventus-3x-plus-8g-oc-lhr'
  },
  {
    id: '2',
    type: 'Placa de Vídeo',
    manufacturer: 'Asus',
    model: '1060',
    price: 200
  },
  {
    id: '3',
    type: 'Fonte',
    manufacturer: 'Asus',
    model: 'Pylon',
    price: 500
  },
  {
    id: '4',
    type: 'Fonte',
    manufacturer: 'Asus',
    model: 'Pylon',
    price: 500
  },
  {
    id: '6',
    type: 'Fonte',
    manufacturer: 'Asus',
    model: 'Pylon',
    price: 500
  },
  {
    id: '7',
    type: 'Fonte',
    manufacturer: 'Asus',
    model: 'Pylon',
    price: 500
  }
];

function SugestorComponenteMemoriaRam(busca: string) {
  const router = useRouter();
  const [items, setItems] = useState(mockItems);
  
  function handleClick(prox = false) {
    if (prox){
        router.push('/sugestor-de-componente/fonte');
    }
    else{
        router.back()
    }
  }

  return (  
    <Grid
      h='md'
      templateRows='repeat(3, 1fr)'
      templateColumns='repeat(4, 1fr)'
      gap={3}
      bg={useColorModeValue('gray.50', 'gray.800')}
    >
      <GridItem colSpan={4}>
        <Center>
          <Heading>Sugestor de Componente</Heading>
        </Center>
        <Center>
            <HStack
            pl={6}
            pr={6}
            mt={1}
            spacing={"39"}
            bg={useColorModeValue('white', 'gray.700')}
            rounded={'xl'}
            boxShadow={'lg'}
            >
                <Button variant='ghost' colorScheme="blue" leftIcon={<ArrowBackIcon />} onClick={() => handleClick()}>
                        Voltar
                </Button>
                <Stack>
                    <Heading as='h4' size='md'>
                        Placa mãe
                    </Heading>
                    <Center>
                      <StatusIndicator isActive={false}/>
                    </Center>
                </Stack> 
                <Stack>
                    <Heading as='h4' size='md'>
                        Processador
                    </Heading>
                    <Center>
                      <StatusIndicator isActive={false}/>
                    </Center>
                </Stack> 
                <Stack>
                    <Heading as='h4' size='md'>
                        Memória RAM
                    </Heading>
                    <Center>
                      <StatusIndicator isActive={false}/>
                    </Center>
                </Stack> 
                <Stack>
                    <Heading as='h4' size='md'>
                        Placa de Vídeo
                    </Heading>
                    <Center>
                      <StatusIndicator isActive={true}/>
                    </Center>
                </Stack> 
                <Stack>
                    <Heading as='h4' size='md'>
                        Fonte
                    </Heading>
                    <Center>
                      <StatusIndicator isActive={false}/>
                    </Center>
                </Stack> 
                <Button variant="solid" colorScheme="blue" rightIcon={<ArrowForwardIcon />} onClick={() => handleClick(true)}>
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

export default SugestorComponenteMemoriaRam;
