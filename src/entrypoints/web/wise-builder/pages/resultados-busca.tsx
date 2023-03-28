import { useEffect, useState } from "react";
import {
  Box,
  Button,
  Checkbox,
  Divider,
  Flex,
  Grid,
  GridItem,
  Heading,
  HStack,
  Icon,
  Input,
  ListIcon,
  Stack,
  Text,
  useColorModeValue,
} from "@chakra-ui/react";
import { FiFilter } from "react-icons/fi";
import { useRouter } from "next/router";
import { AddIcon, CheckCircleIcon, HamburgerIcon } from "@chakra-ui/icons";
import CardProduto from "../src/components/Card/card-produto";
import { Componente } from "../src/types/componente";
import { mockComponent } from "react-dom/test-utils";

function ResultadosBusca() {
  const router = useRouter();

  const [components, setComponents] = useState([]);
  const [checkedItems, setCheckedItems] = useState([false, false]);

  const [busca, setBusca] = useState<string>("");

  function handleClick() {
    router.push({ pathname: "/resultados-busca", query: { name: busca } });
    search();
  }

  async function search() {
    const query = new URLSearchParams(window.location.search);
    const name = query.get("name");
    const apiEndpoint = "http://127.0.0.1:5000/api/v1/search?name=" + name;
    const response = await fetch(apiEndpoint);
    const data = await response.json();
    setComponents(data);
  }

  useEffect(() => {
    search();
  }, []);

  const allChecked = checkedItems.every(Boolean);
  const isIndeterminate = checkedItems.some(Boolean) && !allChecked;

  return (
    <Box position={"relative"} bg={useColorModeValue("gray.50", "gray.800")}>
      <Stack
        flex={{ base: 2, md: 0 }}
        mt={2}
        mr={2}
        justify={"center"}
        direction={"row"}
        spacing={6}
      >
        <Input
          placeholder="Qual componente está buscando?"
          onChange={(event) =>
            setBusca(event.target.value)}
          bg={"gray.100"}
          ml={10}
          border={0}
          color={"gray.500"}
          _placeholder={{
            color: "gray.500",
          }}
        />
        <Button
          fontFamily={"heading"}
          mt={8}
          mr={8}
          bgGradient="linear(to-r, red.400,pink.400)"
          color={"white"}
          onClick={() =>
            handleClick()}
          _hover={{
            bgGradient: "linear(to-r, red.400,pink.400)",
          }}
        >
          Buscar
        </Button>
      </Stack>
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
    </Box>
  );
}

export default ResultadosBusca;
