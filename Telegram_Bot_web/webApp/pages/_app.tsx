import { FC } from 'react';
import { AppProps } from 'next/app';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import theme from '../theme';
import Layout from '../components/layout';
import '../styles/styles.css'
const MyApp: FC<AppProps> = ({ Component, pageProps }) => {
  return (
    <ThemeProvider theme={theme} >
      {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
      <CssBaseline />
      {/* Pass page props to the Component */}
      <Layout>
        <Component {...pageProps} />
      </Layout>
      
      
    </ThemeProvider>
  );
};

export default MyApp;