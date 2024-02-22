import type { NextApiRequest, NextApiResponse } from 'next'
import clientPromise from '../../lib/mongodb';

type order = {
  _id: string,
  orderID: string,
  cart: String[],
  orderTotalUSD: number,
  orderTotalBTC: number,
  address:String,
  deliveryInstructions:String,
  status:String,
  orderDate:Date
}
type ResponseData = {
  message: string
}
 
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ResponseData>
) {

  if (req.method === 'PUT'){
    delete req.body.id;
    const client = await clientPromise
    const db = client.db('TheProject')
    try{
      const result = db.collection('UnpaidOrders').updateOne(
        {orderID: req.body.orderID},
        {$set: {"status": req.body.Status, "tracking": req.body.Tracking}}
      );
      await result
    }
    catch (e){
      console.error('Error updating document:', e)
      res.status(500).json({ message: 'Internal Server Error!' })
    }


    res.status(200).json({ message: 'Hello from Next.js!' })
  }
  else{
    res.status(200).json({ message: 'Hello from Next.js!' })
  }
  
}