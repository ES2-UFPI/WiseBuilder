import {
  Button,
  ButtonGroup,
  Card,
  CardBody,
  CardFooter,
  Divider,
  Heading,
  HStack,
  Image,
  Link,
  Stack,
  Text,
  useToast,
} from "@chakra-ui/react";
import { ExternalLinkIcon } from "@chakra-ui/icons";
import Acoes from "../Botão/acoes";
import { cardProdutoProps } from "../../types/propsCardProduto";
import { useRouter } from "next/router";
import { useState } from "react";
import getGridTemplateColumns from "../../common/utils/getGridTemplateColumns";
import { collapseTextChangeRangesAcrossMultipleVersions } from "typescript";
import { Componente } from "../../types/componente";

export default function CardProduto(props: cardProdutoProps) {
  const router = useRouter();
  const toast = useToast();
  const [items, setItems] = useState(props.item);

  function handleClick(link: string | undefined) {
    if (link != undefined) {
      router.push(link);
    } else {
      toast({
        position: "top",
        title: "Link não encontrado",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  }

  const cardGroups = [];

  for (let i = 0; i <= Object.keys(props.item).length; i += 4) {
    const group = props.item.slice(i, i + 4);
    cardGroups.push(group);
  }

  return (
    <>
      {cardGroups.map((group, index) => (
        <div
          key={index}
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(4, 1fr)",
            gridGap: "20px",
          }}
        >
          {group.map((item) =>
            props.selectedFunction && props.selectedItems !== undefined
              ? (
                <Card
                  minW={300}
                  key={item._id}
                  mb={3}
                  onClick={() =>
                    props.selectedFunction && props.selectedFunction(item)}
                  bgColor={props.selectedItems.find((i) =>
                      i._id === item._id
                    ) !==
                      undefined
                    ? "blue.700"
                    : "white"}
                >
                  <CardBody>
                    <Heading
                      size="md"
                      color={props.selectedItems.find((i) =>
                          i._id === item._id
                        ) !== undefined
                        ? "white"
                        : "black"}
                    >
                      {item.manufacturer} {item.model}
                    </Heading>
                    <Text color="pink.300" fontSize="2xl">
                      R$ {item.price}
                    </Text>
                  </CardBody>
                  <Divider
                    color={props.selectedItems.find((i) =>
                        i._id === item._id
                      ) !==
                        undefined
                      ? "white"
                      : "black"}
                  />
                  <CardFooter>
                    <HStack spacing={"5"}>
                      <Button
                        variant="solid"
                        colorScheme={props.selectedItems.find((i) =>
                            i._id === item._id
                          ) !== undefined
                          ? "orange"
                          : "blue"}
                      >
                        Ver Produto
                      </Button>
                      <Link
                        color={props.selectedItems.find((i) =>
                            i._id === item._id
                          ) !== undefined
                          ? "blue.100"
                          : "teal.500"}
                        href={item.link}
                        isExternal
                      >
                        Visitar Oferta <ExternalLinkIcon mx="2px" />
                      </Link>
                    </HStack>
                  </CardFooter>
                </Card>
              )
              : (
                <Card minW={300} key={item._id} mb={3}>
                  <CardBody>
                    <Heading size="md">
                      {item.manufacturer} {item.model}
                    </Heading>
                    <Text color="pink.300" fontSize="2xl">
                      R$ {item.price}
                    </Text>
                  </CardBody>
                  <Divider />
                  <CardFooter>
                    <HStack spacing={"5"}>
                      <Button variant="solid" colorScheme="blue">
                        Ver Produto
                      </Button>
                      <Link color="teal.500" href={item.link} isExternal>
                        Visitar Oferta <ExternalLinkIcon mx="2px" />
                      </Link>
                    </HStack>
                  </CardFooter>
                </Card>
              ) //e15b3be74a55e164e4ca0805f6ec5dc1ffd343a2
          )}
        </div>
      ))}
    </>
  );
}
