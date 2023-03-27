import {
  Card,
  CardBody,
  Image,
  Heading,
  Text,
  Divider,
  CardFooter,
  ButtonGroup,
  Button,
  HStack,
  Link,
  useToast,
} from "@chakra-ui/react";
import { ExternalLinkIcon } from "@chakra-ui/icons";
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
                  {item.tipo} {item.fabricante} {item.modelo}
                </Heading>
                <Text color="pink.300" fontSize="2xl">
                  R$ {item.valor}
                </Text>
              </CardBody>
              <Divider />
              <CardFooter>
                <HStack spacing={'5'}>
                  <Button variant="solid" colorScheme="blue">
                    Ver Produto
                  </Button>
                  <Link color='teal.500' href={item.link} isExternal>
                    Visitar Oferta <ExternalLinkIcon mx='2px' />
                  </Link>
                </HStack>      
              </CardFooter>
            </Card>
          ))}
        </div>
      ))}
    </>
  );
}
