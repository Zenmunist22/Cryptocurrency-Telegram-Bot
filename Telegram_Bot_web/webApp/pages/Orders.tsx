import clientPromise from '../lib/mongodb'
import {useState, useEffect} from "react"
import React from 'react'
import { Button,  ListItemText, Box, Paper, TableContainer, Table, TableBody, TableCell, TableRow, TableHead, Dialog, DialogActions, DialogContent, DialogTitle, Alert, Snackbar } from '@mui/material';
import { DataGrid, GridColDef, GridRenderCellParams, GridToolbar, GridValueFormatterParams, GridValueGetterParams } from '@mui/x-data-grid';
import useSWR from 'swr'
import { Typography } from '@mui/material';
import ResponsiveAppBar from '../components/navbar';
import Grid from '@mui/material/Unstable_Grid2'
type order ={
  id: string,
  name: string,
  orderId: string,
  chatId: string,
  cart: String[],
  orderTotalUSD: number,
  orderTotalBTC: number,
  txId: String,
  address:String,
  deliveryInstructions:String,
  status:String,
  tracking: String,
  orderDate:Date
}


export async function getServerSideProps() {
  try{
    const client = await clientPromise;
    const db = client.db("TheProject");
    
    const orders = await db
        .collection("UnpaidOrders")
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



export default function Orders({orders}:any) {

  const [cartModalOpen, setCartModalOpen] = useState(false);
  const [cartItems, setCartItems] = useState<string[]>([]);
  const handleCloseModal = () => {
    setCartModalOpen(false);
    setCartItems([]);
  };
  const handleViewCart = (cartItems: string[]) => {
    setCartModalOpen(true);
    setCartItems(cartItems)
  }

  const updateRow = async (row: order) => {
    const idToUpdate = row.orderId
    const updatedData = {...row};
    try {
      const response = await fetch('/api/update/', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedData),
      });
      const data = await response;
      return row
    }
    catch (error){
      console.error('Error updating document:', error)
    }
    return row

  }
  const columns: GridColDef[] = [
    {field: 'id', width: 100},
    {field: 'orderId', width: 220},
    {field: 'chatId', width: 100},
    {field: 'name', width: 200},
    {
      field: 'Cart',
      width: 150,
      sortable: false,
      renderCell: (params: GridRenderCellParams<string[]>) => {
        
        
        return (
        <Button variant="outlined"  size="small" sx={{m:1}}
        onClick={() => handleViewCart(params.value)}
        >
          View Cart
        </Button>
      )}
    },
    {field: 'Address', width: 400, sortable: false},
    {
      field: 'Status',
      width: 200,
      editable: true,
      type: 'singleSelect',
      valueOptions: ['Awaiting Payment', 'Payment Received', 'Shipping Label Created', 'Shipped'],
    },
    {field: 'USD'},
    {field: 'Satoshi'},
    {field: 'TxId', width:600},
    {field: 'Tracking', width: 150, editable: true},
    {
      field: 'OrderDate',
      width: 200,
      valueFormatter: (params: GridValueFormatterParams<Date>) => {
        var date = new Date(params.value)
        var pstDate = date.toLocaleString("en-US", {
          timeZone: "America/Los_Angeles"
        })
        return pstDate;
      }
    }
  ]
  
  const getRows = () => {
    return orders.map((order:order, index:number) => ({
      id: index, // You can use a unique identifier if available
      name: order.name,
      orderId: order.orderId,
      chatId: order.chatId,
      Cart: order.cart,
      Address: order.address,
      Status: order.status,
      USD: order.orderTotalUSD,
      Satoshi: order.orderTotalBTC,
      TxId: order.txId,
      Tracking: order.tracking,
      
      OrderDate: order.orderDate
      // Add other fields as needed based on your data structure
    }));
  };
  const rows = getRows();

  const getRowsOrderItems = () => {
    return cartItems.map((item, index) => 
    {
      var itemDesc = item.split('|')
      return ({
        id: index,
        Item: itemDesc[0],
        Weight: itemDesc[1],
        QTY: itemDesc[2],
        Price: itemDesc[3],
      })
    }
    )
  
    
  };

  const [open, setOpen] = React.useState(false);

  const handleClick = () => {
    setOpen(true);
  };

 
 const handleClose = (event?: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === 'clickaway') {
      setOpen(false)
      return;
    }

    setOpen(false);
  };
  const rowsOrderItems = getRowsOrderItems();
  return (
    <>
    <Grid container spacing={2}>
      <Grid xs={12}  display={"flex"} justifyContent={"center"}>
        <Box sx={{width:'97%', mt: 3}} component={Paper} elevation={10}>
          <Typography variant="h2" sx={{m:1}}>Orders Page</Typography>
          <Typography variant="h5" sx={{ml:1}}>Use this page to view, filter, and edit orders</Typography>
        </Box>
      </Grid>
      <Grid xs={12} display={"flex"} justifyContent={"center"} >
        <Box sx={{width:'97%'}} component={Paper} elevation={10} >
          <DataGrid
            columns={columns}
            rows={rows}
            rowHeight={40}
            sx={{
              
            }}
            slots={{ toolbar: GridToolbar }}
            processRowUpdate={(updatedRow, originalRow) =>
              {
                return updateRow(updatedRow).then(() => {
                  setOpen(true);
                  console.log(updatedRow)
                  return updatedRow
                })
              }
            
            }
            onProcessRowUpdateError={(error) => {
              console.log(error)
            }}
          />
        </Box>
      </Grid>
    
    <Dialog open={cartModalOpen} onClose={handleCloseModal}>
      <DialogTitle>Cart Items</DialogTitle>
        <DialogContent>
          <DataGrid
            columns={[{field:'Item', width: 200},{field: 'Weight'}, {field:'QTY'}, {field:'Price'}]}
            rows={rowsOrderItems}
          />

        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseModal}>Close</Button>
        </DialogActions>
    </Dialog>
    <Snackbar open={open} autoHideDuration={6000} onClose={handleClose}>
      <Alert onClose={handleClose} severity="success" sx={{ width: '100%' }}>
        This is a success message!
      </Alert>
    </Snackbar>
    </Grid>
 
    
  </>
    
    
  );
}

