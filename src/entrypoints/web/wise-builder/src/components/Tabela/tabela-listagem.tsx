import {
    Table,
    Thead,
    Tbody,
    Tfoot,
    Tr,
    Th,
    Td,
    TableContainer,
    Button,
    Stack,
  } from '@chakra-ui/react';
import { Card, Heading, CardBody } from '@chakra-ui/react';
import { AddIcon } from "@chakra-ui/icons";
import Acoes from '../Botão/acoes'
import { TabelaProps } from '../../types/propsTable';
import { useRouter } from "next/router";

export default function tabela (props: TabelaProps) {
    const router = useRouter();
    function handleClick() {
        router.push("/cadastrar-componente");
    }
    return(
        <TableContainer>
            <Card  size='sm'>
                <CardBody>
                    <Stack direction="row" align="center" justify="space-between">
                        <Heading size={'md'}>{props.titulo}</Heading>
                        <Button onClick={handleClick} size={'sm'} colorScheme='blue' aria-label='Adicionar Componente' leftIcon={<AddIcon />}>Adicionar</Button>
                    </Stack>  
                </CardBody>
            </Card>
            <Table variant='striped' size='md'>
            <Thead>
                <Tr>
                <Th isNumeric> ID </Th>
                <Th>Tipo do Componente</Th>
                <Th>Fabricante</Th>
                <Th>Modelo</Th>
                <Th>Ações</Th>
                </Tr>
            </Thead>
            <Tbody>
                <Tr>
                <Td isNumeric>1</Td>
                <Td>Placa de Vídeo</Td>
                <Td>Zotac</Td>
                <Td>RTX 3070</Td>
                <Td><Acoes /></Td>
                </Tr>
                <Tr>
                <Td isNumeric>2</Td>
                <Td>Placa de Vídeo</Td>
                <Td>Asus</Td>
                <Td>GTX 1060</Td>
                <Td><Acoes /></Td>
                </Tr>
            </Tbody>
            </Table>
        </TableContainer>);
};