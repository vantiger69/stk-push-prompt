import React, { useState,useEffect } from 'react';
import axios from 'axios';

function PaymentForm() {
    const [phone, setPhone] = useState('')
    const [amount, setAmount] = useState('')
    const [status, setStatus] = useState('')



    const handleSubmit = async (e) => {
        e.preventDefault();
        try{
            const response = await axios.post('http://127.0.0.1:5000/stk-push',{
                phone_number:phone,
                amount:amount
            });
            
            setStatus(response.data.message || response.data.error);

        }catch (error) {
            console.error(error);
            setStatus("Something went wrong")
        }
        
        setAmount('')
        setPhone('')
    }
    useEffect(() =>{
        if (status) {
            const timer = setTimeout(() =>{
                setStatus('')
            }, 3000);
            return () => clearTimeout(timer)
        }
    }, [status]);
    
    
  return (
    <div>
        <h2>Make payment</h2>
        <form onSubmit={handleSubmit}>
            <input
            type='text'
            placeholder='Phone number'
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            required
            />

            <input
            type='text'
            placeholder='Amount'
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            required
            />

            <button type='submit'>Pay Now</button>

        </form>
        <p>{status}</p>
      
    </div>
  )
}

export default PaymentForm
