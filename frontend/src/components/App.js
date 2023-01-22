import React, { useState, useEffect } from 'react';
import logo from '../assets/logo.png';
import { API_BASE_URL } from '../config';
import Blockchain from './Blockchain';

"""
This code is a React.js component that renders the UI of an application called "pychain".
The component fetches information about a wallet from an API endpoint, and then displays the wallet's 
address and balance. The component also renders another component called "Blockchain" which is likely responsible for 
displaying information about the blockchain. The component uses the React Hooks 'useState' and 'useEffect' to manage 
the component's state and to fetch the wallet information from the API.
"""

function App() {
  // useState hook to set the state for the wallet info
  const [walletInfo, setWalletInfo] = useState({});

  // useEffect hook to fetch wallet information from the server and update the state
  useEffect(() => {
    // Fetch wallet info from the server
    fetch(`${API_BASE_URL}/wallet/info`)
      // parse the json response
      .then(response => response.json())
      // update the state with the wallet info
      .then(json => setWalletInfo(json));
  }, []);

  // destructuring the state to get address and balance
  const { address, balance } = walletInfo;

  // return the JSX for the app
  return (
    <div className="App">
      {/* logo image */}
      <img className="logo" src={logo} alt="application-logo" />
      {/* Welcome message */}
      <h3>Welcome to pychain</h3>
      <br />
      {/* Display the wallet information */}
      <div className="WalletInfo">
        <div>Address: {address}</div>
        <div>Balance: {balance}</div>
      </div>
      <br />
      {/* Display the blockchain */}
      <Blockchain />
    </div>
  );
}

export default App;
