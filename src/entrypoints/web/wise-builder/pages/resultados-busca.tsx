import { useEffect, useState } from "react";
import {
  Box,
  Checkbox,
  Divider,
  Flex,
  Grid,
  GridItem,
  Heading,
  HStack,
  Icon,
  ListIcon,
  Stack,
  Text,
  useColorModeValue,
} from "@chakra-ui/react";
import { FiFilter } from "react-icons/fi";
import { AddIcon, CheckCircleIcon, HamburgerIcon } from "@chakra-ui/icons";
import CardProduto from "../src/components/Card/card-produto";
import { Componente } from "../src/types/componente";
import { mockComponent } from "react-dom/test-utils";

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

const mockItems = [
  {
    id: "1",
    type: "Placa de Vídeo",
    manufacturer: "Zotac",
    model: "3070",
    price: 100,
    link:
      "https://www.kabum.com.br/produto/377636/placa-de-video-rtx-3070-msi-ventus-3x-plus-nvidia-geforce-8gb-gddr6-lhr-dlss-ray-tracing-geforce-rtx-3070-ventus-3x-plus-8g-oc-lhr",
  },
  {
    id: "2",
    type: "Placa de Vídeo",
    manufacturer: "Asus",
    model: "1060",
    price: 200,
  },
  {
    id: "3",
    type: "Fonte",
    manufacturer: "Asus",
    model: "Pylon",
    price: 500,
  },
  {
    id: "4",
    type: "Fonte",
    manufacturer: "Asus",
    model: "Pylon",
    price: 500,
  },
  {
    id: "6",
    type: "Fonte",
    manufacturer: "Asus",
    model: "Pylon",
    price: 500,
  },
  {
    id: "7",
    type: "Fonte",
    manufacturer: "Asus",
    model: "Pylon",
    price: 500,
  },
];

function ResultadosBusca() {
  const [components, setComponents] = useState([]);
  const [checkedItems, setCheckedItems] = useState([false, false]);

  async function search(name: string) {
    const apiEndpoint = "http://127.0.0.1:5000/api/v1/search?name=" + name;
    const response = await fetch(apiEndpoint);
    const data = await response.json();
    console.log(data.slice(0, 0 + 4));

    setComponents(data);
  }

  useEffect(() => {
    const query = new URLSearchParams(window.location.search);
    const name = query.get("name");
    search(name);
  }, []);

  const allChecked = checkedItems.every(Boolean);
  const isIndeterminate = checkedItems.some(Boolean) && !allChecked;

  return (
    <Grid
      h="md"
      templateRows="repeat(3, 1fr)"
      templateColumns="repeat(4, 1fr)"
      gap={3}
      bg={useColorModeValue("gray.50", "gray.800")}
    >
      <GridItem rowSpan={2} colSpan={1} margin={3}>
        <Heading as="h4" size="sd" mb={4}>
          Sua pesquisa:
        </Heading>
        <HStack mb={3}>
          <FiFilter />
          <Heading as="h4" size="md">
            Filtrar:
          </Heading>
        </HStack>
        <Flex
          bg={useColorModeValue("white", "gray.700")}
          rounded={"xl"}
          boxShadow={"lg"}
        >
          <Stack margin={3}>
            <Text>
              Tipo de Componente
            </Text>
            <Stack pl={6} mt={1} spacing={1}>
              <Checkbox
                isChecked={checkedItems[0]}
                onChange={(e) =>
                  setCheckedItems([e.target.checked, checkedItems[1]])}
              >
                Placa de vídeo
              </Checkbox>
              <Checkbox
                isChecked={checkedItems[1]}
                onChange={(e) =>
                  setCheckedItems([checkedItems[0], e.target.checked])}
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
                onChange={(e) =>
                  setCheckedItems([e.target.checked, checkedItems[1]])}
              >
                Asus
              </Checkbox>
              <Checkbox
                isChecked={checkedItems[1]}
                onChange={(e) =>
                  setCheckedItems([checkedItems[0], e.target.checked])}
              >
                MSI
              </Checkbox>
              <Checkbox
                isChecked={checkedItems[1]}
                onChange={(e) =>
                  setCheckedItems([checkedItems[0], e.target.checked])}
              >
                ZOTAC
              </Checkbox>
            </Stack>
          </Stack>
        </Flex>
      </GridItem>
      <GridItem rowSpan={20} colSpan={3} margin={3}>
        <CardProduto item={components} />
      </GridItem>
    </Grid>
  );
}

export default ResultadosBusca;
