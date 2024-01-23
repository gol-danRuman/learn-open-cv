import React, { useRef, useState } from 'react';
import Modal from 'react-modal';
import Webcam from "react-webcam";
import FileInput from '../FileInputComponent/CustomFileInput';

const customStyles = {
  content: {
    top: '50%',
    left: '50%',
    right: 'auto',
    bottom: 'auto',
    marginRight: '-50%',
    transform: 'translate(-50%, -50%)',
    backgroundColor: '#fff',
    padding: '20px',
    borderRadius: '5px',
    boxShadow: '0px 0px 10px rgba(0, 0, 0, 0.1)',
  },
};

Modal.setAppElement('#root');

const ModalComponent = () => {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [stream, setStream] = useState(null);
  const [isStreamLoading, setIsStreamLoading] = useState(false);
  const videoRef = useRef(null);

  const openModal = () => {
    setModalIsOpen(true);
  };

  const closeModal = () => {
    setModalIsOpen(false);
    setStream(null);
  };

  const handleStreamLoad = () => {
    setIsStreamLoading(false);
  };

  const handleStreamError = (error) => {
    console.error('Error accessing webcam:', error);
    setIsStreamLoading(false);
  };

  const openCamera = async () => {
    setIsStreamLoading(true);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      setStream(stream);
    } catch (error) {
      handleStreamError(error);
    }
  };

  return (
    <div>
      <button onClick={openModal}>Get Started</button>
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        style={customStyles}
        contentLabel="Modal"
      >
        <h2>Choose an option</h2>
        <button onClick={openCamera} disabled={isStreamLoading}>
        {isStreamLoading ? null: 'Live Camera' }
        </button>
        {isStreamLoading ? <>
            <Webcam imageSmoothing={isStreamLoading} />
            <button onClick={() => {
              console.log("Button clicked");
              setIsStreamLoading(false); 
              setStream(null);
            }}>Close Camera</button>
          </>:null} 
        <FileInput/>
        {/* <button onClick={closeModal}>Upload Photo</button> */}
      </Modal>
    </div>
  );
};

export default ModalComponent;