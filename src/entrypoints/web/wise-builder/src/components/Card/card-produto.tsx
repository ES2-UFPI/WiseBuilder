import {
  Button,
  ButtonGroup,
  Card,
  CardBody,
  CardFooter,
  Divider,
  Heading,
  Image,
  Stack,
  TableContainer,
  Text,
  useToast,
} from "@chakra-ui/react";
import { AddIcon } from "@chakra-ui/icons";
import Acoes from "../Botão/acoes";
import { cardProdutoProps } from "../../types/propsCardProduto";
import { useRouter } from "next/router";
import { useState } from "react";
import getGridTemplateColumns from "../../common/utils/getGridTemplateColumns";

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

  for (let i = 0; i < items.length; i += 4) {
    const group = items.slice(i, i + 4);
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
          {group.map((item) => (
            <Card minW={300} key={item.id} mb={3}>
              <CardBody>
                <Heading size="md">
                  {item.type} {item.manufacturer} {item.model}
                </Heading>
                <Text color="pink.300" fontSize="2xl">
                  R$ {item.price}
                </Text>
              </CardBody>
              <Divider />
              <CardFooter>
                <ButtonGroup spacing="2">
                  <Button variant="solid" colorScheme="blue">
                    Ver Produto
                  </Button>
                  <Button
                    variant="ghost"
                    colorScheme="blue"
                    onClick={() => handleClick(item.link)}
                  >
                    Visitar Oferta
                  </Button>
                </ButtonGroup>
              </CardFooter>
            </Card>
          ))}
        </div>
      ))}
    </>
  );
}
