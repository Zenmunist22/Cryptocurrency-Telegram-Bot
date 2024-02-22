// theme.js
import { createTheme, alpha, getContrastRatio } from '@mui/material/styles';
const violetBase = '#7F00FF';
const violetMain = alpha(violetBase, 0.7);
const theme = createTheme({
  palette: {
    primary: {
      main: '#22223B'
    },
  },
});

export default theme;
