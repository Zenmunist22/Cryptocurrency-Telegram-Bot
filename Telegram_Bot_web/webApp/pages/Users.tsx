import clientPromise from '../lib/mongodb'
import {useState, useEffect} from "react"
import React from 'react'
import { Button,  ListItemText, Box, Paper, TableContainer, Table, TableBody, TableCell, TableRow, TableHead, Dialog, DialogActions, DialogContent, DialogTitle } from '@mui/material';
import { DataGrid, GridColDef, GridRenderCellParams, GridToolbar, GridValueFormatterParams, GridValueGetterParams } from '@mui/x-data-grid';
import useSWR from 'swr'
import { Typography } from '@mui/material';
import ResponsiveAppBar from '../components/navbar';
import Grid from '@mui/material/Unstable_Grid2'
type user ={
  _id: String,
  name: String,
  chatId: String,
  relatedOrders: String[],
  DateCreated: Date
}


export async function getServerSideProps() {
  try{
    const client = await clientPromise;
    const db = client.db("TheProject");

    const orders = await db
        .collection("Users")
        .find({})
        .toArray();
    
    return {
      props: {
        orders: JSON.parse(JSON.stringify(orders))
      }
    };
  } catch (e) {
      console.error(e)
  }
}



export default function Users({orders}:any) {

  const [relatedModalOpen, setRelatedCartModalOpen] = useState(false);
  const [relatedOrders, setRelatedOrders] = useState<string[]>([]);
  const handleCloseModal = () => {
    setRelatedCartModalOpen(false);
    setRelatedOrders([]);
  };
  const handleViewCart = (relatedOrders: string[]) => {
    setRelatedCartModalOpen(true);
    setRelatedOrders(relatedOrders);
    console.log(relatedOrders);
  }


  const columns: GridColDef[] = [
    {field: 'chatId', width: 300},
    {field: 'name', width: 300},
    {
      field: 'relatedOrders',
      width: 200,
      sortable: false,
      renderCell: (params: GridRenderCellParams<string[]>) => {
        
        
        return (
        <Button variant="outlined"  size="small"
        onClick={() => handleViewCart(params.value)}
        >
          View Orders
        </Button>
      )}
    },
    {
      field: 'DateCreated', width:200,
      valueFormatter: (params: GridValueFormatterParams<Date>) => {
        var date = new Date(params.value)
        var pstDate = date.toLocaleString("en-US", {
          timeZone: "America/Los_Angeles"
        })
        console.log(pstDate)
        return pstDate;
      }
    }
  ]
  
  const getRows = () => {
    return orders.map((User:user, index:number) => ({
      id: index, // You can use a unique identifier if available
      name: User.name,
      chatId: User.chatId,
      relatedOrders: User.relatedOrders,
      DateCreated: User.DateCreated,
      // Add other fields as needed based on your data structure
    }));
  };
  const rows = getRows();

  const getRowsOrderItems = () => {
    return relatedOrders.map((item, index) => 
    {
      return ({
        id: index+1,
        "Index": index+1,
        OrderId: item,
      })
    }
    )
  
    
  };
  const rowsOrderItems = getRowsOrderItems();
  
  return (
    <>
    <Grid container spacing={2}>
      <Grid xs={12}  display={"flex"} justifyContent={"center"}>
        <Box sx={{width:'98%', mt: 3}} component={Paper} elevation={10}>
          <Typography variant="h2" sx={{m:1}}>Users Page</Typography>
          <Typography variant="h5" sx={{ml:1}}>Use this page to view, filter, and edit users</Typography>
        </Box>
      </Grid>
      <Grid xs={12} display={"flex"} justifyContent={"center"} >
        <Box sx={{width:'98%'}} component={Paper} elevation={10} >
          <DataGrid
            columns={columns}
            rows={rows}
            rowHeight={40}
            sx={{
              
            }}
          />
        </Box>
      </Grid>
    
    <Dialog open={relatedModalOpen} onClose={handleCloseModal}>
      <DialogTitle>Related Orders</DialogTitle>
        <DialogContent>
          <DataGrid
            columns={[{field: "Index"}, {field: "OrderId", width: 400}]}
            rows={rowsOrderItems}
            slots={{ toolbar: GridToolbar }} 
          />

        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseModal}>Close</Button>
        </DialogActions>
    </Dialog>
    
    </Grid>
 
    
  </>
    
    
  );
}

