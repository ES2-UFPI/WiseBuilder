import React from 'react';
import { ChakraProvider } from '@chakra-ui/react';
import MenuNav from '../src/components/MenuNav/menuNav';

function App(props: { Component: any; pageProps: any; }) {
    const { Component, pageProps } = props;
  return (
    <ChakraProvider>
        <MenuNav />
        <Component {...pageProps} />
    </ChakraProvider>
  )
}

export default App