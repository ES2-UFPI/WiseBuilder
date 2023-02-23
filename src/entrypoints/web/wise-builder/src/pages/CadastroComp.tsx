import React, { useState } from 'react';
import { ChakraProvider } from '@chakra-ui/react'
import { Input } from '@chakra-ui/react'
import { Heading } from '@chakra-ui/react'
import { Select } from '@chakra-ui/react'
import { Button, ButtonGroup } from '@chakra-ui/react'
import { Center, Square, Circle } from '@chakra-ui/react'
import {
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
} from '@chakra-ui/react'
import { Grid, GridItem } from '@chakra-ui/react'
import { Switch } from '@chakra-ui/react'
import {
  Flex,
  FormControl,
  FormLabel,
  Stack,
  useColorModeValue,
  HStack,
  IconButton,
} from '@chakra-ui/react';

function App() {
  const [tipo, setTipo] = useState<string>("");
  const [fabricante, setFabricante] = useState<string>("");
  const [socket, setSocket] = useState<number>(0);
  const [cores, setCores] = useState<number>(0);
  const [chipset, setChipset] = useState<number>(0);
  const [tamanho, setTamanho] = useState<number>(0);
  const [slotsRam, setSlotsRam] = useState<number>(0);
  const [usb2, setUsb2] = useState<number>(0);
  const [usb3, setUsb3] = useState<number>(0);
  const [vga, setVga] = useState<number>(0);
  const [display, setDisplay] = useState<number>(0);
  const [hdmi, setHdmi] = useState<number>(0);
  const [pciGen, setPciGen] = useState<number>(0);
  const [pci1, setPci1] = useState<number>(0);
  const [pci4, setPci4] = useState<number>(0);
  const [pci8, setPci8] = useState<number>(0);
  const [pci16, setPci16] = useState<number>(0);
  const [volts, setVolts] = useState<number>(0);
  const [eficiency, setEficiency] = useState<number>(0);
  const [modular, setModular] = useState<number>(0);
  const [baseClock, setBaseClock] = useState<number>(0);
  const [boostClock, setBoostClock] = useState<number>(0);
  const [consumo, setConsumo] = useState<number>(0);
  const [gpuIntegrada, setGpuIntegrada] = useState<string>("");
  const [overclock, setOverclock] = useState<boolean>(false);
  const [vram, setVram] = useState<number>(0);
  const [vramSpd, setVramSpd] = useState<number>(0);
  const [modelo, setModelo] = useState<string>("");
  const [generation, setGeneration] = useState<string>("");
  const [frequency, setFrequency] = useState<number>(0);

 /*  const send = () => {
    const data: Ram = {
      fabricante:fabricante,
      modelo: modelo,
      generation: generation,
      frequency: frequency
    }

    fetch('https://api.npms.io/v2/search?q=react', {method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
        .then() //evento que vai ocorrer se a requisição der certo
        .catch(); //lógica para tratar erro

  } */

  return (
    <ChakraProvider>
      <Flex
      minH={'100vh'}
      align={'center'}
      justify={'center'}
      bg={useColorModeValue('gray.50', 'gray.800')}>
      <Stack
        spacing={4}
        w={'full'}
        maxW={'md'}
        bg={useColorModeValue('white', 'gray.700')}
        rounded={'xl'}
        boxShadow={'lg'}
        p={6}
        my={12}>
        <Heading lineHeight={1.1} fontSize={{ base: '2xl', sm: '3xl' }}>
          Cadastrar Componentes
        </Heading>
        <FormControl id="componentes">
          <FormLabel>Tipo do Componente</FormLabel>
          <Select onChange={(event)=> setTipo(event.target.value)} placeholder='Selecione'>
            <option value='CPU'>CPU</option>
            <option value='GPU'>GPU</option>
            <option value='Placa Mãe'>Placa Mãe</option>
            <option value='Memória RAM'>Memória RAM</option>
            <option value='Fonte'>Fonte</option>
          </Select>
        </FormControl>
        {tipo === 'CPU' && (
          <Stack
            spacing={4}
            w={'full'}
            maxW={'md'}
            rounded={'xl'}
            my={12}>
            <FormControl id="fabricante" isRequired>
              <FormLabel>Fabricante</FormLabel>
              <Input 
                onChange={(event)=> setFabricante(event.target.value)}
                placeholder="Fabricante"
                _placeholder={{ color: 'gray.500' }}
                type="text"
              />
            </FormControl>
            
            <FormControl id="modelo" isRequired>
              <FormLabel>Modelo</FormLabel>
              <Input 
                onChange={(event)=> setModelo(event.target.value)}
                placeholder="Modelo"
                _placeholder={{ color: 'gray.500' }}
                type="text"
              />
            </FormControl>

            <FormControl id="socket" isRequired>
            <FormLabel>Socket</FormLabel>
              <NumberInput onChange={(value)=> setSocket(+value)}>
                <NumberInputField placeholder="Socket" _placeholder={{ color: 'gray.500' }} /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="nucleos" isRequired>
            <FormLabel>Núcleos</FormLabel>
              <NumberInput onChange={(value)=> setCores(+value)}>
                <NumberInputField placeholder="Núcleos" _placeholder={{ color: 'gray.500' }} /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="baseClock" isRequired>
            <FormLabel>Velocidade Base do Clock da CPU</FormLabel>
              <NumberInput onChange={(value)=> setBaseClock(+value)}>
                <NumberInputField placeholder="Velocidade Base do CLock da CPU" _placeholder={{ color: 'gray.500' }} /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="boostClock" isRequired>
            <FormLabel>Velocidade Máxima do Clock da CPU</FormLabel>
              <NumberInput onChange={(value)=> setBoostClock(+value)}>
                <NumberInputField placeholder="Velocidade Máxima do Clock da CPU" _placeholder={{ color: 'gray.500' }} /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="vramSpd" isRequired>
            <FormLabel>Velocidade Máxima do Clock da RAM</FormLabel>
              <NumberInput onChange={(value)=> setVramSpd(+value)}>
                <NumberInputField placeholder="Velocidade Máxima do Clock da RAM" _placeholder={{ color: 'gray.500' }} /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="consumo" isRequired>
            <FormLabel>Consumo</FormLabel>
              <NumberInput onChange={(value)=> setConsumo(+value)}>
                <NumberInputField placeholder="Consumo" _placeholder={{ color: 'gray.500' }} /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="gpuIntegrada" isRequired>
              <FormLabel>GPU Integrada</FormLabel>
              <Input 
                onChange={(event)=> setGpuIntegrada(event.target.value)}
                placeholder="GPU Integrada"
                _placeholder={{ color: 'gray.500' }}
                type="text"
              />
            </FormControl>

            <FormControl id="overclock" isRequired>
              <FormLabel>Suporta OverClock</FormLabel>
              <Switch isChecked={overclock} onChange={()=> overclock? setOverclock(false): setOverclock(true)} />
            </FormControl>
          </Stack>
        )}

        {tipo === 'GPU' && (
          <Stack
            spacing={4}
            w={'full'}
            maxW={'md'}
            rounded={'xl'}
            my={12}>
            <FormControl id="fabricante" isRequired>
              <FormLabel>Fabricante</FormLabel>
              <Input 
                onChange={(event)=> setFabricante(event.target.value)}
                placeholder="Fabricante"
                _placeholder={{ color: 'gray.500' }}
                type="text"
              />
            </FormControl>
            
            <FormControl id="modelo" isRequired>
              <FormLabel>Modelo</FormLabel>
              <Input 
                onChange={(event)=> setModelo(event.target.value)}
                placeholder="Modelo"
                _placeholder={{ color: 'gray.500' }}
                type="text"
              />
            </FormControl>

            <FormControl id="consumo" isRequired>
            <FormLabel>Consumo</FormLabel>
              <NumberInput onChange={(value)=> setConsumo(+value)}>
                <NumberInputField placeholder="Consumo" _placeholder={{ color: 'gray.500' }} /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="vram" isRequired>
            <FormLabel>Capacidade da Memória RAM da CPU</FormLabel>
              <NumberInput onChange={(value)=> setVram(+value)}>
                <NumberInputField placeholder="Velocidade Máxima do Clock da RAM" _placeholder={{ color: 'gray.500' }} /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="vramSpd" isRequired>
            <FormLabel>Velocidade da Memória RAM da CPU</FormLabel>
              <NumberInput onChange={(value)=> setVramSpd(+value)}>
                <NumberInputField placeholder="Velocidade da Memória RAM da CPU" _placeholder={{ color: 'gray.500' }} /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
              </NumberInput>
            </FormControl>
          </Stack>
        )}

        {tipo === 'Placa Mãe' && (
          <Stack
          spacing={4}
          w={'full'}
          maxW={'md'}
          rounded={'xl'}
          my={12}>
          <FormControl id="fabricante" isRequired>
            <FormLabel>Fabricante</FormLabel>
            <Input 
              onChange={(event)=> setFabricante(event.target.value)}
              placeholder="Fabricante"
              _placeholder={{ color: 'gray.500' }}
              type="text"
            />
          </FormControl>
          
          <FormControl id="modelo" isRequired>
            <FormLabel>Modelo</FormLabel>
            <Input 
              onChange={(event)=> setModelo(event.target.value)}
              placeholder="Modelo"
              _placeholder={{ color: 'gray.500' }}
              type="text"
            />
          </FormControl>

          <FormControl id="chipset" isRequired>
          <FormLabel>Chipset</FormLabel>
            <NumberInput onChange={(value)=> setChipset(+value)}>
              <NumberInputField placeholder="Chipset" _placeholder={{ color: 'gray.500' }} /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
            </NumberInput>
          </FormControl>

          <FormControl id="tamanho" isRequired>
          <FormLabel>Tamanho</FormLabel>
            <NumberInput onChange={(value)=> setTamanho(+value)}>
              <NumberInputField placeholder="Tamanho" _placeholder={{ color: 'gray.500' }} /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
            </NumberInput>
          </FormControl>

          <FormControl id="slotsRam" isRequired>
          <FormLabel>Quantidade de Slots de RAM</FormLabel>
            <NumberInput onChange={(value)=> setSlotsRam(+value)}>
              <NumberInputField placeholder="Quantidade de Slots de RAM" _placeholder={{ color: 'gray.500' }} /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
            </NumberInput>
          </FormControl>
        
          <FormControl id="consumo" isRequired>
            <FormLabel>Consumo</FormLabel>
              <NumberInput onChange={(value)=> setConsumo(+value)}>
                <NumberInputField placeholder="Consumo" _placeholder={{ color: 'gray.500' }} /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
              </NumberInput>
          </FormControl>

          <FormControl id="consumo" isRequired>
            <FormLabel>Número de Portas USB 2</FormLabel>
              <NumberInput onChange={(value)=> setUsb2(+value)}>
                <NumberInputField placeholder="Número de Portas USB 2" _placeholder={{ color: 'gray.500' }} /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
              </NumberInput>
          </FormControl>
          
          <label>
            Fabricante
          </label> 
          <Input onChange={(event)=> setFabricante(event.target.value)} />

          <label>
            Modelo
          </label> 
          <Input onChange={(event)=> setModelo(event.target.value)} />

          <label>
            Chipset
          </label> 
          <NumberInput onChange={(value)=> setChipset(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Tamanho
          </label>
          <NumberInput onChange={(value)=> setTamanho(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Quantidade de Slots de RAM
          </label>
          <NumberInput onChange={(value)=> setSlotsRam(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Consumo
          </label> 
          <NumberInput onChange={(value)=> setConsumo(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Número de Portas USB 2
          </label>
          <NumberInput onChange={(value)=> setUsb2(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Número de Portas USB 3
          </label>
          <NumberInput onChange={(value)=> setUsb3(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Número de Portas VGA
          </label>
          <NumberInput onChange={(value)=> setVga(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Número de Portas HDMI
          </label>
          <NumberInput onChange={(value)=> setHdmi(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Número de Portas de Display
          </label>
          <NumberInput onChange={(value)=> setDisplay(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Geração PCIE
          </label>
          <NumberInput onChange={(value)=> setPciGen(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Quantidade PCIE x1
          </label>
          <NumberInput onChange={(value)=> setPci1(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Quantidade PCIE x4
          </label>
          <NumberInput onChange={(value)=> setPci4(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Quantidade PCIE x8
          </label>
          <NumberInput onChange={(value)=> setPci8(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Quantidade PCIE x16
          </label>
          <NumberInput onChange={(value)=> setPci16(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>
        </Stack>
      )}

{tipo === 'Fonte' && (
        <Grid>
          <label>
            Fabricante
          </label> 
          <Input onChange={(event)=> setFabricante(event.target.value)} />

          <label>
            Modelo
          </label> 
          <Input onChange={(event)=> setModelo(event.target.value)} />

          <label>
            Voltagem
          </label> 
          <NumberInput onChange={(value)=> setVolts(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Eficiência
          </label> 
          <NumberInput onChange={(value)=> setEficiency(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Modularidade
          </label> 
          <NumberInput onChange={(value)=> setModular(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>
        </Grid>
      )}

{tipo === 'Memória RAM' && (
      <Grid>
          <label>
            Fabricante
          </label> 
          <Input onChange={(event)=> setFabricante(event.target.value)} />

          <label>
            Modelo
          </label> 
          <Input onChange={(event)=> setModelo(event.target.value)}/>

          <label>
            Geração
          </label> 
          <Input onChange={(event)=> setGeneration(event.target.value)}/> 

          <label>
            Frequência
          </label> 
          <NumberInput onChange={(value)=> setFrequency(+value)}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>
        </Grid>
      )}
        <Stack spacing={6} direction={['column', 'row']}>
          <Button
            bg={'red.400'}
            color={'white'}
            w="full"
            _hover={{
              bg: 'red.500',
            }}>
            Cancel
          </Button>
          <Button
            onClick={()=> ""}
            bg={'blue.400'}
            color={'white'}
            w="full"
            _hover={{
              bg: 'blue.500',
            }}>
            Salvar
          </Button>
        </Stack>
      </Stack>
    </Flex>
    </ChakraProvider>
  );
}

export default App;