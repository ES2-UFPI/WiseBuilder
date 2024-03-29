import {
    Flex,
    Box,
    FormControl,
    FormLabel,
    Input,
    InputGroup,
    HStack,
    InputRightElement,
    Stack,
    Button,
    Heading,
    Text,
    useColorModeValue,
    Link,
  } from '@chakra-ui/react';
  import { useState } from 'react';
  import { ViewIcon, ViewOffIcon } from '@chakra-ui/icons';
  
  export default function SignupCard() {
    const [showPassword, setShowPassword] = useState(false);
    const [nome, setNome] = useState<string>("");
    const [sobreNome, setSobreNome] = useState<string>("");
    const [email, setEmail] = useState<string>("");
    const [senha, setSenha] = useState<string>("");
  
    return (
      <Flex
        minH={'100vh'}
        align={'center'}
        justify={'center'}
        bg={useColorModeValue('gray.50', 'gray.800')}>
        <Stack spacing={8} mx={'auto'} maxW={'lg'} py={12} px={6}>
          <Heading fontSize={'4xl'} textAlign={'center'}>
              Cadastre-se
          </Heading>
          <Box
            rounded={'lg'}
            bg={useColorModeValue('white', 'gray.700')}
            boxShadow={'lg'}
            p={8}>
            <Stack spacing={4}>
              <HStack>
                <Box>
                  <FormControl id="firstName" isRequired>
                    <FormLabel>Nome</FormLabel>
                    <Input type="text" onChange={(event)=> setNome(event.target.value)}/>
                  </FormControl>
                </Box>
                <Box>
                  <FormControl id="lastName">
                    <FormLabel>Sobrenome</FormLabel>
                    <Input type="text" onChange={(event)=> setSobreNome(event.target.value)}/>
                  </FormControl>
                </Box>
              </HStack>
              <FormControl id="email" isRequired>
                <FormLabel>Email</FormLabel>
                <Input type="email" onChange={(event)=> setEmail(event.target.value)}/>
              </FormControl>
              <FormControl id="password" isRequired>
                <FormLabel>Senha</FormLabel>
                <InputGroup>
                  <Input type={showPassword ? 'text' : 'password'} onChange={(event)=> setSenha(event.target.value)}/>
                  <InputRightElement h={'full'}>
                    <Button
                      variant={'ghost'}
                      onClick={() =>
                        setShowPassword((showPassword) => !showPassword)
                      }>
                      {showPassword ? <ViewIcon /> : <ViewOffIcon />}
                    </Button>
                  </InputRightElement>
                </InputGroup>
              </FormControl>
              <Stack spacing={10} pt={2}>
                <Button
                  loadingText="Submitting"
                  size="lg"
                  bg={'blue.400'}
                  color={'white'}
                  _hover={{
                    bg: 'blue.500',
                  }}>
                  Cadastre-se
                </Button>
              </Stack>
              <Stack pt={6}>
                <Text align={'center'}>
                  Já possui uma conta? <Link color={'blue.400'} href='/authentication/login'>Login</Link>
                </Text>
              </Stack>
            </Stack>
          </Box>
        </Stack>
      </Flex>
    );
  }