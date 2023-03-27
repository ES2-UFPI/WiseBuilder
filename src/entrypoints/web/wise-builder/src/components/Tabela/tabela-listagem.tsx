import {
  Button,
  Stack,
  Table,
  TableContainer,
  Tbody,
  Td,
  Tfoot,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react";
import { Card, CardBody, Heading } from "@chakra-ui/react";
import { AddIcon } from "@chakra-ui/icons";
import Acoes from "../Botão/acoes";
import { TabelaProps } from "../../types/propsTable";
import { useRouter } from "next/router";
import { useState } from "react";

export default function tabela(props: TabelaProps) {
  const router = useRouter();
  const [items, setItems] = useState(props.item);
  function handleClick() {
    if (props.link != undefined) {
      router.push(props.link);
    }
  }
  console.log("Items: \n");
  console.log(props.item);

  return (
    <TableContainer>
      <Card size="sm">
        <CardBody>
          <Stack direction="row" align="center" justify="space-between">
            <Heading size={"md"}>{props.titulo}</Heading>
            {props.link && (
              <Button
                onClick={handleClick}
                size={"sm"}
                colorScheme="blue"
                aria-label="Adicionar Componente"
                leftIcon={<AddIcon />}
              >
                Adicionar
              </Button>
            )}
          </Stack>
        </CardBody>
      </Card>
      <Table variant="striped" size="md">
        <Thead>
          <Tr>
            <Th>ID</Th>
            <Th>Tipo do Componente</Th>
            <Th>Fabricante</Th>
            <Th>Modelo</Th>
            <Th>Ações</Th>
          </Tr>
        </Thead>
        <Tbody>
          {props.item.map((item) => (
            <Tr key={item._id}>
              <Td>{item._id}</Td>
              <Td>{item.manufacturer}</Td>
              <Td>{item.manufacturer}</Td>
              <Td>{item.model}</Td>
              <Td>
                <Acoes id={item._id} edit={props.edit} link={item.link} />
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </TableContainer>
  );
}
