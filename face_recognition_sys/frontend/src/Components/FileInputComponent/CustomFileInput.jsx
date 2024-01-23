import React, { useState } from 'react';

const FileInput = (props) => {
  

  const handleFileChange = (event) => {
    props.setFile(event.target.files[0]);
    props.setIsImageSelected(true);
  };

  return (
    <input type="file" onChange={handleFileChange} />
  );
};

export default FileInput;