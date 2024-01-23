import React, { useEffect, useState } from 'react';
import { MdFace } from 'react-icons/md';
import { FaCamera } from "react-icons/fa";
import './WelcomeCard.css';
import FileInput from '../FileInputComponent/CustomFileInput';
import Webcam from 'react-webcam';

const LandingPage = (props) => {
  return (
    <div>
      <MdFace className="welcome-icon" />
      <h2 className="welcome-title">Welcome Back!</h2>
      <p className="welcome-text">Use our face detection service to enhance your security.</p>
      <button className="welcome-button" onClick={props.handleOptionOpen}><FaCamera className='camera-icon'/>Initiate Face Detection</button>
    </div>
  );
};

const LiveCameraPage = (props) => {
  return (
    <>
            <Webcam className="live-camera-card" imageSmoothing={props.isStreamLoading} />
            <button style={{width: "16rem"}} onClick={() => {
              console.log("Button clicked");
              props.setIsStreamLoading(false); 
            }}>Close Camera</button>
            <button style={{width: "16rem"}} onClick={() => {
              console.log("Button clicked");
              props.setIsStreamLoading(false); 
            }}>Detect</button>
    </>
  )
}

const ImageSelectedPage = (props) => {
  return (
    <>
    <div className='selected-image-card'>
            {props.image && <img className='selected-image' src={URL.createObjectURL(props.image)} alt="Selected Image" />}
            <button style={{marginTop: "1rem"}} onClick={() => {
              console.log("Button clicked");
              props.setIsImageSelected(false); 
            }}>Cancel</button>

</div>
    </>
  )
}

const OptionPage = (props) => {
  const [isStreamLoading, setIsStreamLoading] = useState(false);
  const [isImageSelected, setIsImageSelected] = useState(false);
  const [file, setFile] = useState(null);

  const handleButtonClick = () => {
    setIsStreamLoading(true);
    props.handleStreamLoad();
  };

  useEffect(() => {
    return () => {
      setIsStreamLoading(false);
    };
  }, []);

  return (
    <>{
      isStreamLoading ? <LiveCameraPage isStreamLoading={isStreamLoading} setIsStreamLoading={setIsStreamLoading}/> :
      isImageSelected? <>
        <ImageSelectedPage image={file} isImageSelected={isImageSelected} setIsImageSelected={setIsImageSelected}/>
      </>:

      <div className='option-card'>
      <h2>Choose an option</h2>
      <button onClick={handleButtonClick} disabled={isStreamLoading}>
        Live Camera
      </button>
      <FileInput setFile={setFile} setIsImageSelected={setIsImageSelected}/>
      </div>
    
      
    }
    
    </>
  );
};


const WelcomeCard = () => {
  const [optionOpen, setOptionOpen] = useState(false);

  const handleOptionOpen = () => {
    setOptionOpen(true);
  };

  const handleStreamLoad = () => {
    // handle stream loading logic here
  };

  return (
    <div className="welcome-card">
      {optionOpen ? <OptionPage handleStreamLoad={handleStreamLoad} handleOptionOpen={handleOptionOpen} /> : <LandingPage handleOptionOpen={handleOptionOpen} />}
    </div>
  );
};

export default WelcomeCard;