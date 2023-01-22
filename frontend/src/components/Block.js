import React, { useState } from 'react';
import { Button } from 'react-bootstrap';
import { MILLISECONDS_PY } from '../config';
import Transaction from './Transaction';

// This component provides a toggle button to show or hide the transactions within a block.
// It receives a block object as props and maps through its data to display each transaction.
function ToggleTransactionDisplay({ block }) {
  // State to keep track of whether to display transactions or not
  const [displayTransaction, setDisplayTransaction] = useState(false);
  const { data } = block;

  // Function to toggle the displayTransaction state
  const toggleDisplayTransaction = () => {
    setDisplayTransaction(!displayTransaction);
  }

  // If the displayTransaction state is true, map through the block's data
  // and display each transaction wrapped in a div
  // Also, render a "show less" button
  if (displayTransaction) {
    return (
      <div>
        {
          data.map(transaction => (
            <div key={transaction.id}>
              <hr />
              <Transaction transaction={transaction} />
            </div>
          ))
        }
        <br />
        <Button
          variant="danger"
          size="sm"
          onClick={toggleDisplayTransaction}
        >
          Show Less
        </Button>
      </div>
    )
  }

  // If the displayTransaction state is false, render a "show more" button
  return (
    <div>
      <br />
      <Button
        variant="danger"
        size="sm"
        onClick={toggleDisplayTransaction}
      >
        Show More
      </Button>
    </div>
  )
}

// This component displays the hash and timestamp of a block,
// as well as the toggle button to show the transactions within the block
function Block({ block }) {
  const { timestamp, hash } = block;
  const hashDisplay = `${hash.substring(0, 15)}...`;
  const timestampDisplay = new Date(timestamp / MILLISECONDS_PY).toLocaleString();

  return (
    <div className="Block">
      <div>Hash: {hashDisplay}</div>
      <div>Timestamp: {timestampDisplay}</div>
      <ToggleTransactionDisplay block={block} />
    </div>
  )
}

export default Block;
