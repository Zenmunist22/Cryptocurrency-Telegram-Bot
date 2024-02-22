import { Box, Paper, Typography } from "@mui/material";

export default function home(){
    return (
        <>
        <Box component={Paper} elevation={10} sx={{m:5, p: 2}}>
            <Typography variant="h2"> Home Page </Typography>
            <Typography variant="h5"> Navigate using the NavBar on the top</Typography>
        </Box>
        </>
    )
}