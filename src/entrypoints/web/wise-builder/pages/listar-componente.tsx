import { Component, useEffect, useState } from "react";
import {
  Divider,
  Flex,
  Heading,
  List,
  ListIcon,
  ListItem,
  Stack,
  useColorModeValue,
} from "@chakra-ui/react";
import { AddIcon, CheckCircleIcon } from "@chakra-ui/icons";
import Tabela from "../src/components/Tabela/tabela-listagem";
import { Componente } from "../src/types/componente";

async function getComponentByType(component: string) {
  const apiEndpoint = "http://127.0.0.1:5000/api/v1/";
  const response = await fetch(apiEndpoint + component);
  const data = await response.json();
  return data;
}

function ItemList() {
  const [components, setComponents] = useState<any>([]);

  useEffect(() => {
    async function getAllComponents() {
      const componentTypes = [
        "cpus",
        "gpus",
        "motherboards",
        "rams",
        "persistences",
        "psus",
      ];

      let allComponents = await Promise.all(
        componentTypes.map(getComponentByType),
      );
      setComponents(allComponents.flat(1));
    }
    getAllComponents();
    console.log("Componetes:")
    console.log(components);
  }, []);
  return (
    <Flex
      minH={"100vh"}
      align={"center"}
      justify={"center"}
      bg={useColorModeValue("gray.50", "gray.800")}
    >
      <Stack
        spacing={4}
        w={"full"}
        maxW={"80%"}
        bg={useColorModeValue("white", "gray.700")}
        rounded={"xl"}
        boxShadow={"lg"}
        p={6}
        my={12}
      >
        <Heading lineHeight={1.1} fontSize={{ base: "2xl", sm: "3xl" }}>
          Listar Componentes
        </Heading>
        <Divider orientation="horizontal" />
        <Tabela
          titulo="Componentes"
          link="/cadastrar-componente"
          item={components}
          edit={true}
        />
      </Stack>
    </Flex>
  );
}

export default ItemList;
