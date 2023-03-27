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
import { useState } from 'react';

export default function tabela (props: TabelaProps) {
    const router = useRouter();
    const [items, setItems] = useState(props.item);
    function handleClick() {
        if (props.link != undefined){
            router.push(props.link);
        }
    }
    return(
        <TableContainer>
            <Card  size='sm'>
                <CardBody>
                    <Stack direction="row" align="center" justify="space-between">
                        <Heading size={'md'}>{props.titulo}</Heading>
                        {props.link &&(
                            <Button onClick={handleClick} size={'sm'} colorScheme='blue' aria-label='Adicionar Componente' leftIcon={<AddIcon />}>Adicionar</Button>
                        )}
                    </Stack>  
                </CardBody>
            </Card>
            <Table variant='striped' size='md'>
                <Thead>
                    <Tr>
                    <Th>ID </Th>
                    <Th>Tipo do Componente</Th>
                    <Th>Fabricante</Th>
                    <Th>Modelo</Th>
                    <Th>Ações</Th>
                    </Tr>
                </Thead>
                <Tbody>
                    {items.map((item) => (
                        <Tr key={item.id}>
                            <Td>{item.id}</Td>
                            <Td>{item.tipo}</Td>
                            <Td>{item.fabricante}</Td>
                            <Td>{item.modelo}</Td>
                            <Td><Acoes id={item.id} edit={props.edit} link={item.link}/></Td>
                        </Tr>
                    ))}
                </Tbody>
            </Table>
        </TableContainer>);
};