import { AccountCircle } from "@mui/icons-material";
import { Box, TextField } from "@mui/material";
import InputAdornment from '@mui/material/InputAdornment';
import theme from '../theme';
function SearchBar(props: any) {
    return (
        <Box>
            <TextField
                color='secondary'
                id="input-with-icon-textfield"
                sx={{background: theme.palette.primary.main,color: theme.palette.primary.contrastText }}
                InputProps={{
                startAdornment: (
                    <InputAdornment position="start">
                    <AccountCircle sx={{color: theme.palette.primary.contrastText }} />
                    </InputAdornment>
                ),
                }}
                variant="outlined"
            />
        </Box>
        
    );
  }
   
export default SearchBar;