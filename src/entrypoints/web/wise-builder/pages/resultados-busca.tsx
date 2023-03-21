import { useState, useEffect } from 'react';
import { 
    Heading,
    Icon,
    ListIcon,
    Flex,
    Box,
    Text,
    Stack,
    Checkbox,
    Grid,
    Divider,
    HStack,
    GridItem,
    useColorModeValue,
} from "@chakra-ui/react";
import { FiFilter } from "react-icons/fi";
import { AddIcon, CheckCircleIcon, HamburgerIcon } from "@chakra-ui/icons";
import CardProduto from '../src/components/Card/card-produto';
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

function ResultadosBusca(busca: string) {
  const [items, setItems] = useState(mockItems);
  const [checkedItems, setCheckedItems] = useState([false, false])

  const allChecked = checkedItems.every(Boolean)
  const isIndeterminate = checkedItems.some(Boolean) && !allChecked

  return (  
    <Grid
      h='md'
      templateRows='repeat(3, 1fr)'
      templateColumns='repeat(4, 1fr)'
      gap={3}
      bg={useColorModeValue('gray.50', 'gray.800')}
    >
      <GridItem rowSpan={2} colSpan={1} margin={3} >
        <Heading as='h4' size='sd' mb={4}>
          Sua pesquisa: 
        </Heading>
        <HStack mb={3}>
          <FiFilter />
          <Heading as='h4' size='md'>
            Filtrar:
          </Heading>
        </HStack>
        <Flex
          bg={useColorModeValue('white', 'gray.700')}
          rounded={'xl'}
          boxShadow={'lg'}
          >
          <Stack margin={3}>
            <Text>
              Tipo de Componente
            </Text>
            <Stack pl={6} mt={1} spacing={1}>
              <Checkbox
                isChecked={checkedItems[0]}
                onChange={(e) => setCheckedItems([e.target.checked, checkedItems[1]])}
              >
                Placa de vídeo
              </Checkbox>
              <Checkbox
                isChecked={checkedItems[1]}
                onChange={(e) => setCheckedItems([checkedItems[0], e.target.checked])}
              >
                Placa mãe
              </Checkbox>
            </Stack>
            <Text>
              Marcas
            </Text>
            <Stack pl={6} mt={1} spacing={1}>
              <Checkbox
                isChecked={checkedItems[0]}
                onChange={(e) => setCheckedItems([e.target.checked, checkedItems[1]])}
              >
                Asus
              </Checkbox>
              <Checkbox
                isChecked={checkedItems[1]}
                onChange={(e) => setCheckedItems([checkedItems[0], e.target.checked])}
              >
                MSI
              </Checkbox>
              <Checkbox
                isChecked={checkedItems[1]}
                onChange={(e) => setCheckedItems([checkedItems[0], e.target.checked])}
              >
                ZOTAC
              </Checkbox>
            </Stack>
          </Stack>
        </Flex>
      </GridItem>
      <GridItem rowSpan={20} colSpan={3} margin={3}>
        <CardProduto item={mockItems}/>
      </GridItem>
    </Grid>
)};

export default ResultadosBusca;
