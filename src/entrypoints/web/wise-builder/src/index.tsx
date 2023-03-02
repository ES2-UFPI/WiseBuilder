import React from 'react';
import ReactDOM from 'react-dom';
import App from './pages/CadastroComp';
import MenuNav from './components/MenuNav/menuNav';
import { ChakraProvider } from '@chakra-ui/react'

ReactDOM.render(
  <React.StrictMode>
    <ChakraProvider>
      <MenuNav />
      <App />
    </ChakraProvider>
  </React.StrictMode>,
  document.getElementById('root')
);
