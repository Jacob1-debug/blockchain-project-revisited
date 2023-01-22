import React from 'react';

function Transaction({ transaction }) {
  const { input, output } = transaction;
  const recipients = Object.keys(output);

  return (
    <div className="Transaction">
      {/*  The address of the sender  */}
      <div>From: {input.address}</div>
      {/*  Map through all the recipients and display the recipient address and amount sent  */}
      {
        recipients.map(recipient => (
          <div key={recipient}>
            To: {recipient} | Sent: {output[recipient]}
          </div>
        ))
      }
    </div>
  )
}

export default Transaction;
