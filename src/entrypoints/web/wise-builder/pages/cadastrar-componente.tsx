import React, { use, useState } from "react";
import { Input, useToast } from "@chakra-ui/react";
import { Heading } from "@chakra-ui/react";
import { Select } from "@chakra-ui/react";
import { Button } from "@chakra-ui/react";
import {
  NumberDecrementStepper,
  NumberIncrementStepper,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
} from "@chakra-ui/react";
import { Switch } from "@chakra-ui/react";
import {
  Flex,
  FormControl,
  FormLabel,
  Stack,
  useColorModeValue,
} from "@chakra-ui/react";
import { useRouter } from "next/router";
import { Componente } from "../src/types/componente";
import { Ram } from "../src/types/ram";

interface Props {
  componente?: Componente;
  editar?: boolean;
}

function CadastroComp({ componente, editar }: Props) {
  const toast = useToast();
  const [tipo, setTipo] = useState<string>(componente?.type || "");
  const [fabricante, setFabricante] = useState<string>(
    componente?.manufacturer || "",
  );
  const [socket, setSocket] = useState<string>(componente?.socket || "");
  const [cores, setCores] = useState<number>(componente?.n_cores || 0);
  const [chipset, setChipset] = useState<string>(componente?.chipset || "");
  const [tamanho, setTamanho] = useState<number>(componente?.board_size || 0);
  const [slotsRam, setSlotsRam] = useState<number>(
    componente?.n_ram_slots || 0,
  );
  const [usb2, setUsb2] = useState<number>(componente?.n_usb2 || 0);
  const [usb3, setUsb3] = useState<number>(componente?.n_usb3x || 0);
  const [vga, setVga] = useState<number>(componente?.n_vga || 0);
  const [display, setDisplay] = useState<number>(
    componente?.n_display_port || 0,
  );
  const [hdmi, setHdmi] = useState<number>(componente?.n_hdmi || 0);
  const [pciGen, setPciGen] = useState<number>(componente?.pcie_gen || 0);
  const [pci1, setPci1] = useState<number>(componente?.n_pcie_x1 || 0);
  const [pci4, setPci4] = useState<number>(componente?.n_pcie_x4 || 0);
  const [pci8, setPci8] = useState<number>(componente?.n_pcie_x8 || 0);
  const [pci16, setPci16] = useState<number>(componente?.n_pcie_x16 || 0);
  const [volts, setVolts] = useState<number>(componente?.power || 0);
  const [eficiency, setEficiency] = useState<number>(
    componente?.rate || 0,
  );
  const [modular, setModular] = useState<number>(componente?.modularity || 0);
  const [baseClock, setBaseClock] = useState<number>(
    componente?.base_clock_spd || 0,
  );
  const [boostClock, setBoostClock] = useState<number>(
    componente?.boost_clock_spd || 0,
  );
  const [consumo, setConsumo] = useState<number>(componente?.consumption || 0);
  const [gpuIntegrada, setGpuIntegrada] = useState<string>(
    componente?.integrated_gpu || "",
  );
  const [overclock, setOverclock] = useState<boolean>(
    componente?.overclock || false,
  );
  const [vram, setVram] = useState<number>(componente?.vram || 0);
  const [vramSpd, setVramSpd] = useState<number>(componente?.vram_spd || 0);
  const [modelo, setModelo] = useState<string>(componente?.model || "");
  const [generation, setGeneration] = useState<number>(
    componente?.generation || 0,
  );
  const [frequency, setFrequency] = useState<number>(
    componente?.frequency || 0,
  );

  const [storage, setStorage] = useState<number>(componente?.storage || 0);
  const [io, setIO] = useState<number>(componente?.io || 0);
  const [isHDD, setIsHDD] = useState<boolean>(componente?.is_HDD || false);
  const [rpm, setRpm] = useState<number>(componente?.rpm || 0);
  const [sata, setSata] = useState<number>(componente?.sata || 0);
  const [memoryType, setMemoryType] = useState<number>(
    componente?.memory_type || 0,
  );

  const router = useRouter();
  function handleClick() {
    router.back();
  }

  const send = () => {
    let data;
    let url = "";

    switch (tipo) {
      case "CPU":
        data = {
          manufacturer: fabricante,
          model: modelo,
          socket: socket,
          n_cores: cores,
          base_clock_spd: baseClock,
          boost_clock_spd: boostClock,
          ram_clock_max: vramSpd,
          consumption: consumo,
          integrated_gpu: gpuIntegrada,
          overclock: overclock,
        };
        url = "http://127.0.0.1:5000/api/v1/cpus/";
        break;
      case "GPU":
        data = {
          manufacturer: fabricante,
          model: modelo,
          consumption: consumo,
          vram: vram,
          vram_spd: vramSpd,
        };
        url = "http://127.0.0.1:5000/api/v1/gpus/";
        break;
      case "Placa Mãe":
        data = {
          manufacturer: fabricante,
          model: modelo,
          chipset: chipset,
          board_size: tamanho,
          n_ram_slots: slotsRam,
          consumption: consumo,
          n_usb2: usb2,
          n_usb3x: usb3,
          n_vga: vga,
          n_hdmi: hdmi,
          n_display_port: display,
          pcie_gen: pciGen,
          n_pcie_x1: pci1,
          n_pcie_x4: pci4,
          n_pcie_x8: pci8,
          n_pcie_x16: pci16,
          sata: sata,
          memory_type: memoryType,
        };
        url = "http://127.0.0.1:5000/api/v1/motherboards/";
        break;
      case "Memória RAM":
        data = {
          manufacturer: fabricante,
          model: modelo,
          generation: generation,
          frequency: frequency,
        };
        url = "http://127.0.0.1:5000/api/v1/rams/";
        break;
      case "Armazenamento":
        data = {
          manufacturer: fabricante,
          model: modelo,
          storage: storage,
          io: io,
          is_HDD: isHDD,
          rpm: rpm,
        };
        url = "http://127.0.0.1:5000/api/v1/persistences/";
        break;
      case "Fonte":
        data = {
          manufacturer: fabricante,
          model: modelo,
          power: volts,
          rate: eficiency,
          modularity: modular,
        };
        url = "http://127.0.0.1:5000/api/v1/psus/";
        break;
      default:
        console.log("Tipo de componente inválido");
        return;
    }
    console.log(JSON.stringify(data));
    fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    })
      .then((response) => { //evento que vai ocorrer se a requisição der certo
        if (response.status == 201) {
          toast({
            position: "top",
            title: "Salvo com Sucesso!",
            status: "success",
            duration: 3000,
            isClosable: true,
          });
        } else {
          toast({
            position: "top",
            title: "Erro ao Salvar",
            status: "error",
            duration: 3000,
            isClosable: true,
          });
        }
      })
      .catch((error) => { //lógica para tratar erro
        toast({
          position: "top",
          title: "Erro ao Salvar",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
      });
    router.push("/listar-componente");
  };

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
          Cadastrar Componentes
        </Heading>
        <FormControl id="componentes">
          <FormLabel>Tipo do Componente</FormLabel>
          <Select
            onChange={(event) => setTipo(event.target.value)}
            placeholder="Selecione"
          >
            <option value="CPU">CPU</option>
            <option value="GPU">GPU</option>
            <option value="Placa Mãe">Placa Mãe</option>
            <option value="Memória RAM">Memória RAM</option>
            <option value="Armazenamento">Armazenamento</option>
            <option value="Fonte">Fonte</option>
          </Select>
        </FormControl>
        {tipo === "CPU" && (
          <Stack
            spacing={4}
            w={"full"}
            maxW={"full"}
            rounded={"xl"}
            my={12}
          >
            <FormControl id="fabricante" isRequired>
              <FormLabel>Fabricante</FormLabel>
              <Input
                onChange={(event) => setFabricante(event.target.value)}
                placeholder="Fabricante"
                _placeholder={{ color: "gray.500" }}
                type="text"
              />
            </FormControl>

            <FormControl id="modelo" isRequired>
              <FormLabel>Modelo</FormLabel>
              <Input
                onChange={(event) => setModelo(event.target.value)}
                placeholder="Modelo"
                _placeholder={{ color: "gray.500" }}
                type="text"
              />
            </FormControl>
            <FormControl id="socket" isRequired>
              <FormLabel>Socket</FormLabel>
              <Input
                onChange={(event) => setSocket(event.target.value)}
                placeholder="Socket"
                _placeholder={{ color: "gray.500" }}
                type="text"
              />
            </FormControl>

            <FormControl id="nucleos" isRequired>
              <FormLabel>Núcleos</FormLabel>
              <NumberInput onChange={(value) => setCores(+value)}>
                <NumberInputField
                  placeholder="Núcleos"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="baseClock" isRequired>
              <FormLabel>Velocidade Base do Clock da CPU</FormLabel>
              <NumberInput onChange={(value) => setBaseClock(+value)}>
                <NumberInputField
                  placeholder="Velocidade Base do CLock da CPU"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="boostClock" isRequired>
              <FormLabel>Velocidade Máxima do Clock da CPU</FormLabel>
              <NumberInput onChange={(value) => setBoostClock(+value)}>
                <NumberInputField
                  placeholder="Velocidade Máxima do Clock da CPU"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="vramSpd" isRequired>
              <FormLabel>Velocidade Máxima do Clock da RAM</FormLabel>
              <NumberInput onChange={(value) => setVramSpd(+value)}>
                <NumberInputField
                  placeholder="Velocidade Máxima do Clock da RAM"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="consumo" isRequired>
              <FormLabel>Consumo</FormLabel>
              <NumberInput onChange={(value) => setConsumo(+value)}>
                <NumberInputField
                  placeholder="Consumo"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="gpuIntegrada" isRequired>
              <FormLabel>GPU Integrada</FormLabel>
              <Input
                onChange={(event) => setGpuIntegrada(event.target.value)}
                placeholder="GPU Integrada"
                _placeholder={{ color: "gray.500" }}
                type="text"
              />
            </FormControl>

            <FormControl id="overclock" isRequired>
              <FormLabel>Suporta OverClock</FormLabel>
              <Switch
                isChecked={overclock}
                onChange={() =>
                  overclock ? setOverclock(false) : setOverclock(true)}
              />
            </FormControl>
          </Stack>
        )}

        {tipo === "GPU" && (
          <Stack
            spacing={4}
            w={"full"}
            maxW={"full"}
            rounded={"xl"}
            my={12}
          >
            <FormControl id="fabricante" isRequired>
              <FormLabel>Fabricante</FormLabel>
              <Input
                onChange={(event) => setFabricante(event.target.value)}
                placeholder="Fabricante"
                _placeholder={{ color: "gray.500" }}
                type="text"
              />
            </FormControl>

            <FormControl id="modelo" isRequired>
              <FormLabel>Modelo</FormLabel>
              <Input
                onChange={(event) => setModelo(event.target.value)}
                placeholder="Modelo"
                _placeholder={{ color: "gray.500" }}
                type="text"
              />
            </FormControl>

            <FormControl id="consumo" isRequired>
              <FormLabel>Consumo</FormLabel>
              <NumberInput onChange={(value) => setConsumo(+value)}>
                <NumberInputField
                  placeholder="Consumo"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="vram" isRequired>
              <FormLabel>Capacidade da Memória RAM da CPU</FormLabel>
              <NumberInput onChange={(value) => setVram(+value)}>
                <NumberInputField
                  placeholder="Capacidade da Memória RAM da CPU"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="vramSpd" isRequired>
              <FormLabel>Velocidade da Memória RAM da CPU</FormLabel>
              <NumberInput onChange={(value) => setVramSpd(+value)}>
                <NumberInputField
                  placeholder="Velocidade da Memória RAM da CPU"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>
          </Stack>
        )}

        {tipo === "Placa Mãe" && (
          <Stack
            spacing={4}
            w={"full"}
            maxW={"full"}
            rounded={"xl"}
            my={12}
          >
            <FormControl id="fabricante" isRequired>
              <FormLabel>Fabricante</FormLabel>
              <Input
                onChange={(event) => setFabricante(event.target.value)}
                placeholder="Fabricante"
                _placeholder={{ color: "gray.500" }}
                type="text"
              />
            </FormControl>

            <FormControl id="modelo" isRequired>
              <FormLabel>Modelo</FormLabel>
              <Input
                onChange={(event) => setModelo(event.target.value)}
                placeholder="Modelo"
                _placeholder={{ color: "gray.500" }}
                type="text"
              />
            </FormControl>

            <FormControl id="modelo" isRequired>
              <FormLabel>Chipset</FormLabel>
              <Input
                onChange={(event) => setChipset(event.target.value)}
                placeholder="Chipset"
                _placeholder={{ color: "gray.500" }}
                type="text"
              />
            </FormControl>

            <FormControl id="tamanho" isRequired>
              <FormLabel>Tamanho</FormLabel>
              <NumberInput onChange={(value) => setTamanho(+value)}>
                <NumberInputField
                  placeholder="Tamanho"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="slotsRam" isRequired>
              <FormLabel>Quantidade de Slots de RAM</FormLabel>
              <NumberInput onChange={(value) => setSlotsRam(+value)}>
                <NumberInputField
                  placeholder="Quantidade de Slots de RAM"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="consumo" isRequired>
              <FormLabel>Consumo</FormLabel>
              <NumberInput onChange={(value) => setConsumo(+value)}>
                <NumberInputField
                  placeholder="Consumo"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="usb2" isRequired>
              <FormLabel>Número de Portas USB 2</FormLabel>
              <NumberInput onChange={(value) => setUsb2(+value)}>
                <NumberInputField
                  placeholder="Número de Portas USB 2"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="usb3" isRequired>
              <FormLabel>Número de Portas USB 3</FormLabel>
              <NumberInput onChange={(value) => setUsb3(+value)}>
                <NumberInputField
                  placeholder="Número de Portas USB 3"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="vga" isRequired>
              <FormLabel>Número de Portas VGA</FormLabel>
              <NumberInput onChange={(value) => setVga(+value)}>
                <NumberInputField
                  placeholder="Número de Portas VGA"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="hdmi" isRequired>
              <FormLabel>Número de Portas HDMI</FormLabel>
              <NumberInput onChange={(value) => setHdmi(+value)}>
                <NumberInputField
                  placeholder="Número de Portas HDMI"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="display" isRequired>
              <FormLabel>Número de Portas de Display</FormLabel>
              <NumberInput onChange={(value) => setDisplay(+value)}>
                <NumberInputField
                  placeholder="Número de Portas de Display"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="pciGen" isRequired>
              <FormLabel>Geração PCIE</FormLabel>
              <NumberInput onChange={(value) => setPciGen(+value)}>
                <NumberInputField
                  placeholder="Geração PCIE"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="pci1" isRequired>
              <FormLabel>Quantidade PCIE x1</FormLabel>
              <NumberInput onChange={(value) => setPci1(+value)}>
                <NumberInputField
                  placeholder="Quantidade PCIE x1"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="pci4" isRequired>
              <FormLabel>Quantidade PCIE x4</FormLabel>
              <NumberInput onChange={(value) => setPci4(+value)}>
                <NumberInputField
                  placeholder="Quantidade PCIE x4"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="pci8" isRequired>
              <FormLabel>Quantidade PCIE x8</FormLabel>
              <NumberInput onChange={(value) => setPci8(+value)}>
                <NumberInputField
                  placeholder="Quantidade PCIE x8"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="pci16" isRequired>
              <FormLabel>Quantidade PCIE x16</FormLabel>
              <NumberInput onChange={(value) => setPci16(+value)}>
                <NumberInputField
                  placeholder="Quantidade PCIE x16"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="sata" isRequired>
              <FormLabel>Quantidade PCIE x16</FormLabel>
              <NumberInput onChange={(value) => setSata(+value)}>
                <NumberInputField
                  placeholder="Quantidade de SATA"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>
            <FormControl id="memoryType" isRequired>
              <FormLabel>Quantidade PCIE x16</FormLabel>
              <NumberInput onChange={(value) => setMemoryType(+value)}>
                <NumberInputField
                  placeholder="Geração da memória ram"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>
          </Stack>
        )}

        {tipo === "Fonte" && (
          <Stack
            spacing={4}
            w={"full"}
            maxW={"full"}
            rounded={"xl"}
            my={12}
          >
            <FormControl id="fabricante" isRequired>
              <FormLabel>Fabricante</FormLabel>
              <Input
                onChange={(event) => setFabricante(event.target.value)}
                placeholder="Fabricante"
                _placeholder={{ color: "gray.500" }}
                type="text"
              />
            </FormControl>

            <FormControl id="modelo" isRequired>
              <FormLabel>Modelo</FormLabel>
              <Input
                onChange={(event) => setModelo(event.target.value)}
                placeholder="Modelo"
                _placeholder={{ color: "gray.500" }}
                type="text"
              />
            </FormControl>

            <FormControl id="volts" isRequired>
              <FormLabel>Voltagem</FormLabel>
              <NumberInput onChange={(value) => setVolts(+value)}>
                <NumberInputField
                  placeholder="Voltagem"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="eficiency" isRequired>
              <FormLabel>Eficiência</FormLabel>
              <NumberInput onChange={(value) => setEficiency(+value)}>
                <NumberInputField
                  placeholder="Eficiência"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="modular" isRequired>
              <FormLabel>Modularidade</FormLabel>
              <NumberInput onChange={(value) => setModular(+value)}>
                <NumberInputField
                  placeholder="Modularidade"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>
          </Stack>
        )}

        {tipo === "Memória RAM" && (
          <Stack
            spacing={4}
            w={"full"}
            maxW={"full"}
            rounded={"xl"}
            my={12}
          >
            <FormControl id="fabricante" isRequired>
              <FormLabel>Fabricante</FormLabel>
              <Input
                onChange={(event) => setFabricante(event.target.value)}
                placeholder="Fabricante"
                _placeholder={{ color: "gray.500" }}
                type="text"
              />
            </FormControl>

            <FormControl id="modelo" isRequired>
              <FormLabel>Modelo</FormLabel>
              <Input
                onChange={(event) => setModelo(event.target.value)}
                placeholder="Modelo"
                _placeholder={{ color: "gray.500" }}
                type="text"
              />
            </FormControl>

            <FormControl id="generation" isRequired>
              <FormLabel>Geração</FormLabel>
              <NumberInput onChange={(value) => setGeneration(+value)}>
                <NumberInputField
                  placeholder="Geração"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="frequency" isRequired>
              <FormLabel>Frequência</FormLabel>
              <NumberInput onChange={(value) => setFrequency(+value)}>
                <NumberInputField
                  placeholder="Frequência"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>
          </Stack>
        )}

        {tipo === "Armazenamento" && (
          <Stack
            spacing={4}
            w={"full"}
            maxW={"full"}
            rounded={"xl"}
            my={12}
          >
            <FormControl id="fabricante" isRequired>
              <FormLabel>Fabricante</FormLabel>
              <Input
                onChange={(event) => setFabricante(event.target.value)}
                placeholder="Fabricante"
                _placeholder={{ color: "gray.500" }}
                type="text"
              />
            </FormControl>

            <FormControl id="modelo" isRequired>
              <FormLabel>Modelo</FormLabel>
              <Input
                onChange={(event) => setModelo(event.target.value)}
                placeholder="Modelo"
                _placeholder={{ color: "gray.500" }}
                type="text"
              />
            </FormControl>

            <FormControl id="storage" isRequired>
              <FormLabel>Capacidade</FormLabel>
              <NumberInput onChange={(value) => setStorage(+value)}>
                <NumberInputField
                  placeholder="Geração"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="io" isRequired>
              <FormLabel>Entrada</FormLabel>
              <NumberInput onChange={(value) => setIO(+value)}>
                <NumberInputField
                  placeholder="Entrada"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>

            <FormControl id="is_HDD" isRequired>
              <FormLabel>É HDD</FormLabel>
              <Switch
                isChecked={isHDD}
                onChange={() => isHDD ? setIsHDD(false) : setIsHDD(true)}
              />
            </FormControl>
            <FormControl id="rpm" isRequired>
              <FormLabel>Rotações por minuto</FormLabel>
              <NumberInput onChange={(value) => setRpm(+value)}>
                <NumberInputField
                  placeholder="RPM"
                  _placeholder={{ color: "gray.500" }}
                />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>
          </Stack>
        )}
        <Stack justify={"right"} spacing={6} direction={["column", "row"]}>
          <Button
            onClick={handleClick}
            bg={"red.400"}
            color={"white"}
            w="20%"
            _hover={{
              bg: "red.500",
            }}
          >
            Cancel
          </Button>
          <Button
            onClick={send}
            bg={"blue.400"}
            color={"white"}
            w="20%"
            _hover={{
              bg: "blue.500",
            }}
          >
            Salvar
          </Button>
        </Stack>
      </Stack>
    </Flex>
  );
}

export default CadastroComp;
