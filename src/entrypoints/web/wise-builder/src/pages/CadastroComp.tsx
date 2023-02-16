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
      <Center h='100px' color='black'>
        <Heading alignContent = {'center'}>Cadastrar Componentes</Heading>
      </Center>
      
      <label>
        Tipo do Componente
      </label>  
      <Select onChange={(event)=> setTipo(event.target.value)} placeholder='Selecione'>
        <option value='CPU'>CPU</option>
        <option value='GPU'>GPU</option>
        <option value='Placa Mãe'>Placa Mãe</option>
        <option value='Memória RAM'>Memória RAM</option>
        <option value='Fonte'>Fonte</option>
      </Select>
      {tipo === 'CPU' && (
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
            Socket
          </label> 
          <NumberInput onChange={(value)=> setSocket(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Núcleos
          </label>
          <NumberInput onChange={(value)=> setCores(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Velocidade Base do Clock da CPU
          </label>
          <NumberInput onChange={(value)=> setBaseClock(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Velocidade Máxima do Clock da CPU
          </label>
          <NumberInput onChange={(value)=> setBoostClock(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Velocidade Máxima do Clock da RAM
          </label>
          <NumberInput onChange={(value)=> setVramSpd(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Consumo
          </label> 
          <NumberInput onChange={(value)=> setConsumo(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            GPU Integrada
          </label> 
          <Input onChange={(event)=> setGpuIntegrada(event.target.value)} />

          <label>
            Suporta OverClock
          </label> 
            <Switch isChecked={overclock} onChange={()=> overclock? setOverclock(false): setOverclock(true)} />
        </Grid>
      )}

{tipo === 'GPU' && (
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
            Consumo
          </label> 
          <NumberInput onChange={(value)=> setConsumo(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Capacidade da Memória RAM da CPU
          </label> 
          <NumberInput onChange={(value)=> setVram(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>

          <label>
            Velocidade da Memória RAM da CPU
          </label> 
          <NumberInput onChange={(value)=> setVramSpd(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>
        </Grid>
      )}

{tipo === 'Placa Mãe' && (
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
        </Grid>
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
          <NumberInput onChange={(value)=> setFrequency(+value)} defaultValue={0}>
            <NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper>
          </NumberInput>
        </Grid>
      )}

      <Button colorScheme='blue' onClick={()=> ""}> Salvar </Button>
    </ChakraProvider>
  );
}

export default App;